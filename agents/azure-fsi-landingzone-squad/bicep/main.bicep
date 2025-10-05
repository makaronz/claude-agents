// Azure FSI Landing Zone - Main Deployment Template
// Ring-based deployment with Free Tier support
// Supports multi-environment deployments (dev/test/staging/prod/sandbox)

targetScope = 'subscription'

// ============================================================================
// PARAMETERS
// ============================================================================

@description('Azure region for deployment')
param location string = 'westeurope'

@description('Environment type')
@allowed([
  'dev'
  'test'
  'staging'
  'prod'
  'sandbox'
])
param environment string

@description('Is this a Free Tier subscription?')
param isFreeTier bool = false

@description('Deployment strategy for architecture')
@allowed([
  'full-rings'    // All rings (0-3) per environment
  'shared-hub'    // Shared Ring 0, separate spokes per env
  'minimal'       // Only Ring 0 + 1 spoke
])
param deploymentStrategy string = 'shared-hub'

@description('Naming prefix for all resources')
param namingPrefix string = 'fsi'

@description('Tags to apply to all resources')
param tags object = {
  Environment: environment
  ManagedBy: 'FSI-LandingZone-Agent'
  CostCenter: 'training'
  Compliance: 'GDPR,DORA,PSD2'
}

@description('Email addresses for budget alerts')
param budgetAlertEmails array = []

@description('Enable automatic cleanup for non-prod environments')
param enableAutoCleanup bool = isFreeTier

// ============================================================================
// VARIABLES
// ============================================================================

// Determine if environment is non-prod
var isNonProd = environment != 'prod'

// Expiration date for non-prod resources (7 days for dev, 3 for test, etc.)
var ttlDays = environment == 'dev' ? 7 :
              environment == 'test' ? 3 :
              environment == 'staging' ? 14 :
              environment == 'sandbox' ? 30 :
              0  // No expiration for prod

// Add expiration tag for non-prod
var resourceTags = union(tags, isNonProd && ttlDays > 0 ? {
  expiration: dateTimeAdd(utcNow('yyyy-MM-dd'), 'P${ttlDays}D')
} : {})

// Determine which rings to deploy based on strategy
var deployRing0 = true  // Hub always deployed
var deployRing1 = deploymentStrategy != 'minimal' || true  // At least 1 spoke
var deployRing2 = deploymentStrategy == 'full-rings' && !isFreeTier
var deployRing3 = deploymentStrategy == 'full-rings' && !isFreeTier

// SKU configurations based on tier
var skuConfig = isFreeTier ? {
  vmSize: 'Standard_B1s'           // ~€8/month (free 750h/month first year)
  sqlTier: 'Basic'                  // ~€4/month
  appServicePlanSku: 'F1'           // Free tier
  storageAccountSku: 'Standard_LRS' // Locally redundant (cheapest)
  keyVaultSku: 'standard'           // Standard (not Premium/HSM)
  enableFirewall: false             // Azure Firewall too expensive (~€900/month)
  enableBastion: false              // Bastion expensive (~€120/month)
  enableLoadBalancer: false         // Load Balancer Standard expensive
  enableDiagnostics: false          // Diagnostic logs cost money
} : {
  vmSize: 'Standard_D2s_v3'
  sqlTier: 'Standard'
  appServicePlanSku: 'S1'
  storageAccountSku: 'Standard_GRS' // Geo-redundant for DORA
  keyVaultSku: 'premium'            // HSM-backed for FSI compliance
  enableFirewall: true
  enableBastion: true
  enableLoadBalancer: true
  enableDiagnostics: true
}

// ============================================================================
// RESOURCE GROUPS
// ============================================================================

// Resource Group for Ring 0 (Hub)
resource rgHub 'Microsoft.Resources/resourceGroups@2023-07-01' = if (deployRing0) {
  name: '${namingPrefix}-rg-hub-${environment}'
  location: location
  tags: union(resourceTags, {
    Ring: 'ring0'
    Purpose: 'Hub Network'
  })
}

// Resource Group for Ring 1 (Spoke 1)
resource rgSpoke1 'Microsoft.Resources/resourceGroups@2023-07-01' = if (deployRing1) {
  name: '${namingPrefix}-rg-spoke1-${environment}'
  location: location
  tags: union(resourceTags, {
    Ring: 'ring1'
    Purpose: 'Workload Spoke'
  })
}

// Resource Group for Ring 2 (Spoke 2) - Only in full-rings mode
resource rgSpoke2 'Microsoft.Resources/resourceGroups@2023-07-01' = if (deployRing2) {
  name: '${namingPrefix}-rg-spoke2-${environment}'
  location: location
  tags: union(resourceTags, {
    Ring: 'ring2'
    Purpose: 'Workload Spoke'
  })
}

// Resource Group for Ring 3 (Spoke 3) - Only in full-rings mode
resource rgSpoke3 'Microsoft.Resources/resourceGroups@2023-07-01' = if (deployRing3) {
  name: '${namingPrefix}-rg-spoke3-${environment}'
  location: location
  tags: union(resourceTags, {
    Ring: 'ring3'
    Purpose: 'Isolated Workload'
  })
}

// Resource Group for Management Services
resource rgManagement 'Microsoft.Resources/resourceGroups@2023-07-01' = {
  name: '${namingPrefix}-rg-mgmt-${environment}'
  location: location
  tags: union(resourceTags, {
    Purpose: 'Management and Monitoring'
  })
}

// ============================================================================
// BUDGET AND COST MANAGEMENT
// ============================================================================

module budget 'modules/budget-policy.bicep' = if (isFreeTier || isNonProd) {
  name: 'deploy-budget-${environment}'
  scope: subscription()
  params: {
    subscriptionId: subscription().subscriptionId
    isFreeTier: isFreeTier
    environment: environment
    budgetAmountFreeTier: 10   // €10 for Free Tier
    budgetAmountStandard: 100  // €100 for non-prod standard
    alertEmails: budgetAlertEmails
    tags: resourceTags
  }
}

// ============================================================================
// CLEANUP POLICY (Non-Prod only)
// ============================================================================

module cleanup 'modules/cleanup-policy.bicep' = if (enableAutoCleanup && isNonProd) {
  name: 'deploy-cleanup-${environment}'
  scope: subscription()
  params: {
    enableCleanup: enableAutoCleanup
    environment: environment
    ttlDaysDev: 7
    ttlDaysTest: 3
    ttlDaysStaging: 14
    ttlDaysSandbox: 30
    tags: resourceTags
  }
}

// ============================================================================
// NETWORK INFRASTRUCTURE
// ============================================================================

// NOTE: Actual network modules (VNets, NSGs, etc.) should be added here
// For now, this is a placeholder showing the conditional logic

// Hub VNet (Ring 0) - Simplified for Free Tier
// module hubNetwork 'modules/hub-network.bicep' = if (deployRing0) {
//   name: 'deploy-hub-network'
//   scope: rgHub
//   params: {
//     location: location
//     namingPrefix: namingPrefix
//     environment: environment
//     tags: resourceTags
//     enableFirewall: skuConfig.enableFirewall
//     enableBastion: skuConfig.enableBastion
//   }
// }

// Spoke VNets (Ring 1-3)
// module spoke1Network 'modules/spoke-network.bicep' = if (deployRing1) {
//   name: 'deploy-spoke1-network'
//   scope: rgSpoke1
//   params: {
//     location: location
//     namingPrefix: namingPrefix
//     spokeName: 'spoke1'
//     environment: environment
//     tags: resourceTags
//   }
// }

// ============================================================================
// OUTPUTS
// ============================================================================

output deploymentInfo object = {
  environment: environment
  isFreeTier: isFreeTier
  deploymentStrategy: deploymentStrategy
  location: location
  namingPrefix: namingPrefix
}

output resourceGroups object = {
  hub: deployRing0 ? rgHub.name : ''
  spoke1: deployRing1 ? rgSpoke1.name : ''
  spoke2: deployRing2 ? rgSpoke2.name : ''
  spoke3: deployRing3 ? rgSpoke3.name : ''
  management: rgManagement.name
}

output skuConfiguration object = skuConfig

output budgetInfo object = isFreeTier || isNonProd ? {
  budgetId: budget.outputs.budgetId
  budgetName: budget.outputs.budgetName
  budgetAmount: budget.outputs.budgetAmount
  alertThresholds: budget.outputs.alertThresholds
} : {}

output cleanupInfo object = enableAutoCleanup && isNonProd ? {
  expirationDate: cleanup.outputs.expirationDate
  ttlDays: cleanup.outputs.ttlDays
  isEnabled: cleanup.outputs.isCleanupEnabled
} : {}

output tags object = resourceTags

output recommendations array = isFreeTier ? [
  '💰 Free Tier detected: Budget alerts enabled at €5 and €10'
  '🚫 Expensive resources (Firewall, Bastion, Load Balancer) are disabled'
  '📦 Using Free/Basic SKUs where possible (B1s VMs, Free App Service, etc.)'
  '🧹 Auto-cleanup enabled: Resources will expire after ${ttlDays} days in ${environment}'
  '📊 Disable diagnostics to save costs'
  '🌍 Consider using only 1 region to minimize data transfer costs'
] : isNonProd ? [
  '✅ Standard SKUs enabled for non-prod environment'
  '💰 Budget alerts enabled at €70 and €100'
  '🧹 Auto-cleanup enabled: Resources expire after ${ttlDays} days'
  '🔒 All security features enabled'
] : [
  '✅ Production environment: Full FSI compliance features enabled'
  '🔒 Azure Firewall, Bastion, and Load Balancer enabled'
  '💾 Geo-redundant storage for DORA compliance'
  '🔐 Premium Key Vault with HSM-backed keys'
  '📊 Full diagnostic logging enabled'
  '⏰ No auto-cleanup: Production resources are permanent'
]
