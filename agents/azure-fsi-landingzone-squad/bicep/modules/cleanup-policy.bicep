// Automatic Cleanup Policy for Non-Prod Environments
// Uses Azure Policy to automatically delete resources after TTL expires

targetScope = 'subscription'

@description('Enable automatic cleanup for non-prod environments')
param enableCleanup bool = true

@description('Environment type')
@allowed([
  'dev'
  'test'
  'staging'
  'prod'
  'sandbox'
])
param environment string = 'dev'

@description('TTL in days for dev environment (default: 7)')
param ttlDaysDev int = 7

@description('TTL in days for test environment (default: 3)')
param ttlDaysTest int = 3

@description('TTL in days for staging environment (default: 14)')
param ttlDaysStaging int = 14

@description('TTL in days for sandbox environment (default: 30)')
param ttlDaysSandbox int = 30

@description('Tags to apply to policy')
param tags object = {
  Environment: environment
  ManagedBy: 'FSI-LandingZone-Agent'
}

// Determine TTL based on environment
var ttlDays = environment == 'dev' ? ttlDaysDev :
              environment == 'test' ? ttlDaysTest :
              environment == 'staging' ? ttlDaysStaging :
              environment == 'sandbox' ? ttlDaysSandbox :
              0  // No cleanup for prod

var isNonProd = environment != 'prod'

// Calculate expiration date from now
var expirationDate = dateTimeAdd(utcNow('yyyy-MM-dd'), 'P${ttlDays}D')

// Azure Policy: Add expiration tag to all resources
resource addExpirationTagPolicy 'Microsoft.Authorization/policyDefinitions@2023-04-01' = if (enableCleanup && isNonProd) {
  name: 'add-expiration-tag-${environment}'
  properties: {
    displayName: 'Add Expiration Tag to Resources (${environment})'
    description: 'Automatically adds an expiration tag to all resources in ${environment} environment'
    policyType: 'Custom'
    mode: 'Indexed'
    metadata: {
      category: 'Tags'
      version: '1.0.0'
      environment: environment
    }
    parameters: {
      expirationDate: {
        type: 'String'
        metadata: {
          displayName: 'Expiration Date'
          description: 'Date when resources should be deleted (YYYY-MM-DD)'
        }
        defaultValue: expirationDate
      }
    }
    policyRule: {
      if: {
        allOf: [
          {
            field: 'tags[\'expiration\']'
            exists: 'false'
          }
          {
            field: 'tags[\'environment\']'
            equals: environment
          }
        ]
      }
      then: {
        effect: 'modify'
        details: {
          roleDefinitionIds: [
            '/providers/Microsoft.Authorization/roleDefinitions/b24988ac-6180-42a0-ab88-20f7382dd24c'  // Contributor
          ]
          operations: [
            {
              operation: 'add'
              field: 'tags[\'expiration\']'
              value: '[parameters(\'expirationDate\')]'
            }
          ]
        }
      }
    }
  }
}

// Assign the add expiration tag policy
resource addExpirationTagAssignment 'Microsoft.Authorization/policyAssignments@2023-04-01' = if (enableCleanup && isNonProd) {
  name: 'assign-expiration-tag-${environment}'
  properties: {
    displayName: 'Add Expiration Tags (${environment})'
    description: 'Ensures all resources in ${environment} have an expiration tag'
    policyDefinitionId: addExpirationTagPolicy.id
    enforcementMode: 'Default'
    parameters: {
      expirationDate: {
        value: expirationDate
      }
    }
    metadata: {
      assignedBy: 'FSI-LandingZone-Agent'
      environment: environment
    }
  }
  identity: {
    type: 'SystemAssigned'
  }
  location: deployment().location
}

// Role assignment for the policy managed identity
resource policyRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (enableCleanup && isNonProd) {
  name: guid(subscription().id, addExpirationTagAssignment.name, 'Contributor')
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', 'b24988ac-6180-42a0-ab88-20f7382dd24c')  // Contributor
    principalId: addExpirationTagAssignment.identity.principalId
    principalType: 'ServicePrincipal'
  }
}

// Azure Policy: Audit resources past expiration
resource auditExpiredResourcesPolicy 'Microsoft.Authorization/policyDefinitions@2023-04-01' = if (enableCleanup && isNonProd) {
  name: 'audit-expired-resources-${environment}'
  properties: {
    displayName: 'Audit Expired Resources (${environment})'
    description: 'Audits resources that have passed their expiration date in ${environment}'
    policyType: 'Custom'
    mode: 'Indexed'
    metadata: {
      category: 'Compliance'
      version: '1.0.0'
      environment: environment
    }
    policyRule: {
      if: {
        allOf: [
          {
            field: 'tags[\'expiration\']'
            exists: 'true'
          }
          {
            value: '[lessOrEquals(field(\'tags[expiration]\'), utcNow(\'yyyy-MM-dd\'))]'
            equals: true
          }
        ]
      }
      then: {
        effect: 'audit'
      }
    }
  }
}

// Assign the audit expired resources policy
resource auditExpiredResourcesAssignment 'Microsoft.Authorization/policyAssignments@2023-04-01' = if (enableCleanup && isNonProd) {
  name: 'assign-audit-expired-${environment}'
  properties: {
    displayName: 'Audit Expired Resources (${environment})'
    description: 'Identifies resources that should be cleaned up in ${environment}'
    policyDefinitionId: auditExpiredResourcesPolicy.id
    enforcementMode: 'Default'
    metadata: {
      assignedBy: 'FSI-LandingZone-Agent'
      environment: environment
    }
  }
}

// Note: Actual deletion should be handled by an Azure Automation Runbook or Logic App
// This module only provides the policy framework for tagging and auditing

// Output cleanup script for Azure Automation
var cleanupScript = '''
# Azure Automation Runbook for Resource Cleanup
# This script deletes resources that have passed their expiration date

param(
    [Parameter(Mandatory=$true)]
    [string]$SubscriptionId,

    [Parameter(Mandatory=$true)]
    [string]$Environment
)

# Connect to Azure (using Automation Account Managed Identity)
Connect-AzAccount -Identity

# Set subscription context
Set-AzContext -SubscriptionId $SubscriptionId

# Get current date
$today = Get-Date -Format "yyyy-MM-dd"

# Find all resources with expiration tag
$expiredResources = Get-AzResource -TagName "expiration" | Where-Object {
    $_.Tags["expiration"] -le $today -and
    $_.Tags["environment"] -eq $Environment
}

Write-Output "Found $($expiredResources.Count) expired resources in $Environment environment"

# Delete expired resources
foreach ($resource in $expiredResources) {
    Write-Output "Deleting expired resource: $($resource.Name) (expires: $($resource.Tags['expiration']))"

    try {
        Remove-AzResource -ResourceId $resource.ResourceId -Force
        Write-Output "  ✓ Deleted successfully"
    }
    catch {
        Write-Error "  ✗ Failed to delete: $_"
    }
}

Write-Output "Cleanup completed for $Environment environment"
'''

// Outputs
output expirationDate string = isNonProd ? expirationDate : 'N/A (prod environment)'
output ttlDays int = ttlDays
output isCleanupEnabled bool = enableCleanup && isNonProd
output policyAssignmentId string = enableCleanup && isNonProd ? addExpirationTagAssignment.id : ''
output auditPolicyAssignmentId string = enableCleanup && isNonProd ? auditExpiredResourcesAssignment.id : ''
output cleanupRunbookScript string = cleanupScript
output recommendedSchedule string = 'Daily at 02:00 UTC'
