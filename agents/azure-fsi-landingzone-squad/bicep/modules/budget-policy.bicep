// Budget and Cost Management Policy for Free Tier
// Automatically creates budgets with alerts for Free Tier subscriptions

targetScope = 'subscription'

@description('Subscription ID for budget creation')
param subscriptionId string = subscription().subscriptionId

@description('Enable Free Tier budget and alerts')
param isFreeTier bool = true

@description('Environment type')
@allowed([
  'dev'
  'test'
  'staging'
  'prod'
  'sandbox'
])
param environment string = 'dev'

@description('Budget amount in EUR for Free Tier (default: 10)')
param budgetAmountFreeTier int = 10

@description('Budget amount in EUR for Standard deployments (default: 100)')
param budgetAmountStandard int = 100

@description('Email addresses for budget alerts (comma-separated)')
param alertEmails array = []

@description('Tags to apply to budget')
param tags object = {
  Environment: environment
  CostCenter: 'training'
  ManagedBy: 'FSI-LandingZone-Agent'
}

// Determine budget amount based on tier
var budgetAmount = isFreeTier ? budgetAmountFreeTier : budgetAmountStandard

// Budget name
var budgetName = 'budget-${environment}-${isFreeTier ? 'freetier' : 'standard'}'

// Alert thresholds (percentage of budget)
var alertThresholds = isFreeTier ? [
  50  // 5€ for Free Tier (50% of 10€)
  80  // 8€ for Free Tier (80% of 10€)
  100 // 10€ for Free Tier (100% of 10€)
] : [
  70  // 70€ for Standard (70% of 100€)
  90  // 90€ for Standard (90% of 100€)
  100 // 100€ for Standard (100% of 100€)
]

// Budget resource
resource budget 'Microsoft.Consumption/budgets@2023-05-01' = if (isFreeTier) {
  name: budgetName
  properties: {
    category: 'Cost'
    amount: budgetAmount
    timeGrain: 'Monthly'
    timePeriod: {
      startDate: '2025-01-01'  // Start date (update as needed)
      endDate: '2030-12-31'    // Far future end date
    }
    filter: {
      dimensions: {
        name: 'ResourceGroupName'
        operator: 'In'
        values: [
          '*'  // All resource groups in subscription
        ]
      }
    }
    notifications: {
      // Alert at 50% (or 70% for standard)
      Alert1: {
        enabled: true
        operator: 'GreaterThan'
        threshold: alertThresholds[0]
        contactEmails: alertEmails
        contactRoles: [
          'Owner'
          'Contributor'
        ]
        thresholdType: 'Forecasted'
      }
      // Alert at 80% (or 90% for standard)
      Alert2: {
        enabled: true
        operator: 'GreaterThan'
        threshold: alertThresholds[1]
        contactEmails: alertEmails
        contactRoles: [
          'Owner'
          'Contributor'
        ]
        thresholdType: 'Actual'
      }
      // Alert at 100%
      Alert3: {
        enabled: true
        operator: 'GreaterThan'
        threshold: alertThresholds[2]
        contactEmails: alertEmails
        contactRoles: [
          'Owner'
          'Contributor'
        ]
        thresholdType: 'Actual'
      }
    }
  }
}

// Cost Management Export (optional - for detailed analysis)
resource costExport 'Microsoft.CostManagement/exports@2023-03-01' = if (isFreeTier) {
  name: 'export-${environment}-costs'
  scope: subscription()
  properties: {
    schedule: {
      recurrence: 'Daily'
      recurrencePeriod: {
        from: '2025-01-01T00:00:00Z'
        to: '2030-12-31T23:59:59Z'
      }
      status: 'Active'
    }
    format: 'Csv'
    deliveryInfo: {
      destination: {
        resourceId: ''  // TODO: Add storage account resource ID if needed
        container: 'cost-exports'
        rootFolderPath: environment
      }
    }
    definition: {
      type: 'ActualCost'
      timeframe: 'MonthToDate'
      dataSet: {
        granularity: 'Daily'
        configuration: {
          columns: [
            'Date'
            'ResourceGroup'
            'ResourceType'
            'Cost'
            'Currency'
          ]
        }
      }
    }
  }
}

// Azure Policy: Deny expensive SKUs in Free Tier
resource denyExpensiveSkusPolicy 'Microsoft.Authorization/policyDefinitions@2023-04-01' = if (isFreeTier) {
  name: 'deny-expensive-skus-freetier'
  properties: {
    displayName: 'Deny Expensive SKUs in Free Tier'
    description: 'Prevents deployment of expensive Azure resources in Free Tier subscriptions'
    policyType: 'Custom'
    mode: 'All'
    metadata: {
      category: 'Cost Management'
      version: '1.0.0'
    }
    policyRule: {
      if: {
        anyOf: [
          // Deny Azure Firewall (expensive)
          {
            allOf: [
              {
                field: 'type'
                equals: 'Microsoft.Network/azureFirewalls'
              }
            ]
          }
          // Deny Premium SQL Database
          {
            allOf: [
              {
                field: 'type'
                equals: 'Microsoft.Sql/servers/databases'
              }
              {
                field: 'Microsoft.Sql/servers/databases/sku.tier'
                in: [
                  'Premium'
                  'BusinessCritical'
                ]
              }
            ]
          }
          // Deny Load Balancer Standard SKU
          {
            allOf: [
              {
                field: 'type'
                equals: 'Microsoft.Network/loadBalancers'
              }
              {
                field: 'Microsoft.Network/loadBalancers/sku.name'
                equals: 'Standard'
              }
            ]
          }
          // Deny Application Gateway (expensive)
          {
            field: 'type'
            equals: 'Microsoft.Network/applicationGateways'
          }
          // Deny VMs with Premium storage
          {
            allOf: [
              {
                field: 'type'
                equals: 'Microsoft.Compute/virtualMachines'
              }
              {
                field: 'Microsoft.Compute/virtualMachines/storageProfile.osDisk.managedDisk.storageAccountType'
                in: [
                  'Premium_LRS'
                  'Premium_ZRS'
                ]
              }
            ]
          }
        ]
      }
      then: {
        effect: 'deny'
      }
    }
  }
}

// Assign the policy to subscription (only in Free Tier)
resource policyAssignment 'Microsoft.Authorization/policyAssignments@2023-04-01' = if (isFreeTier) {
  name: 'assign-deny-expensive-skus'
  properties: {
    displayName: 'Deny Expensive SKUs (Free Tier)'
    description: 'Enforces cost controls by denying expensive SKUs in Free Tier subscription'
    policyDefinitionId: denyExpensiveSkusPolicy.id
    enforcementMode: 'Default'
    metadata: {
      assignedBy: 'FSI-LandingZone-Agent'
      environment: environment
    }
  }
}

// Outputs
output budgetId string = isFreeTier ? budget.id : ''
output budgetName string = isFreeTier ? budget.name : ''
output budgetAmount int = budgetAmount
output policyAssignmentId string = isFreeTier ? policyAssignment.id : ''
output alertThresholds array = alertThresholds
