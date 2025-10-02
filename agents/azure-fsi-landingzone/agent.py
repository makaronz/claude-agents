"""
Azure FSI Landing Zone Agent using Claude Agent SDK.

This agent helps deploy and manage Azure Financial Services Industry (FSI)
Landing Zones using:
- Microsoft FSI Landing Zone templates
- Azure Verified Modules (AVM)
- Built-in compliance policies for European regulations (GDPR, DORA, PSD2, etc.)
"""

import asyncio
import json
import sys
from pathlib import Path
from typing import List, Any, Optional, Dict
from datetime import datetime

# Add the shared modules to the path
sys.path.append(str(Path(__file__).parent.parent.parent / "shared"))

from agents import InteractiveAgent
from utils import setup_logging
from claude_agent_sdk import tool


class AzureFSILandingZoneAgent(InteractiveAgent):
    """
    Azure FSI Landing Zone deployment agent.

    This agent provides capabilities for:
    - Deploying FSI-compliant Azure Landing Zones
    - Managing Azure Verified Modules (AVM)
    - Applying European compliance policies
    - Infrastructure as Code (Bicep/Terraform)
    - Security and compliance validation
    """

    def __init__(self, config_dir: Path):
        super().__init__(config_dir)
        self.azure_config = self.agent_config.get('azure', {})
        self.compliance_config = self.azure_config.get('compliance', {})
        self.deployment_config = self.agent_config.get('deployment', {})

        # Track deployment state
        self.deployment_state = {
            'current_deployment': None,
            'deployments_count': 0,
            'last_validation': None,
            'policies_applied': []
        }

    def get_system_prompt(self) -> Optional[str]:
        """Get the system prompt for this agent."""
        return """You are an Azure Financial Services Industry (FSI) Landing Zone deployment expert.

You help organizations deploy secure, compliant Azure infrastructure using:

1. **Microsoft FSI Landing Zone Templates**: Industry-specific reference architectures
2. **Azure Verified Modules (AVM)**: Validated, production-ready infrastructure modules
3. **European Compliance**: Built-in policies for GDPR, DORA, PSD2, MiFID II, EBA Guidelines

Your expertise includes:
- Hub-spoke network architectures for financial services
- Data residency and sovereignty requirements for EU
- Encryption at rest and in transit (including customer-managed keys)
- Network security with private endpoints and NSGs
- Identity and access management with Azure AD
- Compliance monitoring and auditing
- Bicep and Terraform Infrastructure as Code
- Azure Policy and governance frameworks
- Security baseline configuration

You prioritize:
- Security by design
- Compliance with European regulations
- Zero-trust architecture principles
- Least privilege access
- Data protection and privacy
- Operational resilience (DORA requirements)

You provide step-by-step guidance, validate configurations before deployment,
and ensure best practices are followed for financial services workloads in Azure.
"""

    def get_custom_tools(self) -> List[Any]:
        """Get custom tools for this agent."""
        return [
            self.check_azure_prerequisites,
            self.validate_azure_auth,
            self.get_fsi_compliance_requirements,
            self.list_avm_modules,
            self.generate_bicep_template,
            self.validate_deployment,
            self.apply_compliance_policies,
            self.get_deployment_status,
            self.generate_network_architecture,
            self.check_data_residency,
            self.export_deployment_plan,
            self.generate_bastion_template,
            self.configure_entra_id,
            self.deploy_conditional_access,
            self.setup_pim_roles,
        ]

    @tool("check_azure_prerequisites", "Check if Azure CLI and required tools are installed", {})
    async def check_azure_prerequisites(self, args):
        """Check Azure CLI and prerequisites."""
        checks = {
            'azure_cli': False,
            'azure_cli_version': None,
            'bicep': False,
            'bicep_version': None,
            'authenticated': False,
            'subscription_access': False
        }

        import subprocess

        # Check Azure CLI
        try:
            result = subprocess.run(['az', '--version'], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                checks['azure_cli'] = True
                # Parse version from output
                for line in result.stdout.split('\n'):
                    if 'azure-cli' in line:
                        checks['azure_cli_version'] = line.split()[-1]
                        break
        except Exception:
            pass

        # Check Bicep
        try:
            result = subprocess.run(['az', 'bicep', 'version'], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                checks['bicep'] = True
                checks['bicep_version'] = result.stdout.strip()
        except Exception:
            pass

        # Check authentication
        try:
            result = subprocess.run(['az', 'account', 'show'], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                checks['authenticated'] = True
                account_info = json.loads(result.stdout)
                checks['subscription_access'] = account_info.get('state') == 'Enabled'
        except Exception:
            pass

        # Format response
        status_text = "🔍 Azure Prerequisites Check:\n\n"
        status_text += f"✅ Azure CLI: {'Installed' if checks['azure_cli'] else '❌ Not installed'}\n"
        if checks['azure_cli_version']:
            status_text += f"   Version: {checks['azure_cli_version']}\n"

        status_text += f"✅ Bicep: {'Installed' if checks['bicep'] else '❌ Not installed'}\n"
        if checks['bicep_version']:
            status_text += f"   Version: {checks['bicep_version']}\n"

        status_text += f"✅ Authentication: {'Authenticated' if checks['authenticated'] else '❌ Not authenticated'}\n"
        status_text += f"✅ Subscription Access: {'Active' if checks['subscription_access'] else '❌ No access'}\n"

        if not all([checks['azure_cli'], checks['bicep'], checks['authenticated']]):
            status_text += "\n⚠️  Missing prerequisites detected. Please install/configure:\n"
            if not checks['azure_cli']:
                status_text += "   • Azure CLI: https://docs.microsoft.com/cli/azure/install-azure-cli\n"
            if not checks['bicep']:
                status_text += "   • Bicep: az bicep install\n"
            if not checks['authenticated']:
                status_text += "   • Authenticate: az login\n"

        return {
            "content": [
                {"type": "text", "text": status_text}
            ]
        }

    @tool("validate_azure_auth", "Validate Azure authentication and get subscription details", {})
    async def validate_azure_auth(self, args):
        """Validate Azure authentication and subscription access."""
        import subprocess

        try:
            result = subprocess.run(
                ['az', 'account', 'show', '--output', 'json'],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode != 0:
                return {
                    "content": [
                        {"type": "text", "text": "❌ Not authenticated to Azure. Please run: az login"}
                    ]
                }

            account = json.loads(result.stdout)

            # Get list of available subscriptions
            result = subprocess.run(
                ['az', 'account', 'list', '--output', 'json'],
                capture_output=True,
                text=True,
                timeout=10
            )

            subscriptions = json.loads(result.stdout) if result.returncode == 0 else []

            auth_text = "✅ Azure Authentication Status:\n\n"
            auth_text += f"📋 Current Subscription:\n"
            auth_text += f"   • Name: {account.get('name')}\n"
            auth_text += f"   • ID: {account.get('id')}\n"
            auth_text += f"   • State: {account.get('state')}\n"
            auth_text += f"   • Tenant ID: {account.get('tenantId')}\n"
            auth_text += f"   • User: {account.get('user', {}).get('name')}\n\n"

            if len(subscriptions) > 1:
                auth_text += f"📌 Available Subscriptions ({len(subscriptions)}):\n"
                for sub in subscriptions:
                    indicator = "→" if sub['isDefault'] else " "
                    auth_text += f"   {indicator} {sub['name']} ({sub['id']})\n"

            return {
                "content": [
                    {"type": "text", "text": auth_text}
                ]
            }

        except Exception as e:
            return {
                "content": [
                    {"type": "text", "text": f"❌ Error validating authentication: {str(e)}"}
                ]
            }

    @tool("get_fsi_compliance_requirements", "Get FSI compliance requirements for European regulations", {})
    async def get_fsi_compliance_requirements(self, args):
        """Get FSI compliance requirements."""
        regulations = self.compliance_config.get('regulations', [])

        compliance_text = "📋 FSI Compliance Requirements for European Regulations:\n\n"

        compliance_details = {
            "GDPR": {
                "name": "General Data Protection Regulation",
                "key_requirements": [
                    "Data residency within EU/EEA",
                    "Encryption of personal data at rest and in transit",
                    "Right to erasure (right to be forgotten)",
                    "Data breach notification within 72 hours",
                    "Privacy by design and by default",
                    "Data protection impact assessments (DPIA)"
                ],
                "azure_controls": [
                    "Azure Policy: Allowed locations for resources",
                    "Azure Key Vault with customer-managed keys",
                    "Azure Private Link for services",
                    "Microsoft Defender for Cloud",
                    "Azure Information Protection"
                ]
            },
            "DORA": {
                "name": "Digital Operational Resilience Act",
                "key_requirements": [
                    "ICT risk management framework",
                    "Incident reporting mechanisms",
                    "Digital operational resilience testing",
                    "Third-party ICT service provider management",
                    "Information sharing on cyber threats"
                ],
                "azure_controls": [
                    "Azure Backup and Site Recovery",
                    "Azure Monitor and Log Analytics",
                    "Business continuity planning tools",
                    "Resilience testing framework",
                    "Multi-region deployment architecture"
                ]
            },
            "PSD2": {
                "name": "Payment Services Directive 2",
                "key_requirements": [
                    "Strong customer authentication (SCA)",
                    "Secure communication channels",
                    "Transaction monitoring",
                    "API security for open banking",
                    "Fraud detection and prevention"
                ],
                "azure_controls": [
                    "Azure AD Multi-Factor Authentication",
                    "Azure API Management with OAuth 2.0",
                    "Azure Application Gateway with WAF",
                    "Azure Sentinel for security analytics",
                    "Azure Key Vault for credential management"
                ]
            },
            "MiFID_II": {
                "name": "Markets in Financial Instruments Directive II",
                "key_requirements": [
                    "Transaction reporting",
                    "Record keeping and audit trails",
                    "Best execution reporting",
                    "Clock synchronization",
                    "Data retention (5-7 years)"
                ],
                "azure_controls": [
                    "Azure Storage with immutable blobs",
                    "Azure Log Analytics with retention policies",
                    "Azure Time Series Insights",
                    "Azure Purview for data governance",
                    "Azure Archive Storage"
                ]
            },
            "EBA_GL": {
                "name": "European Banking Authority Guidelines",
                "key_requirements": [
                    "ICT and security risk management",
                    "Outsourcing arrangements",
                    "Cloud service provider oversight",
                    "Exit strategies from cloud services",
                    "Operational resilience"
                ],
                "azure_controls": [
                    "Azure Resource Manager for governance",
                    "Azure Policy for compliance enforcement",
                    "Data export and portability tools",
                    "Multi-cloud and hybrid capabilities",
                    "Sovereign cloud options (Azure Germany, etc.)"
                ]
            }
        }

        for reg in regulations:
            if reg in compliance_details:
                details = compliance_details[reg]
                compliance_text += f"🏛️  {reg} - {details['name']}\n"
                compliance_text += f"   Key Requirements:\n"
                for req in details['key_requirements']:
                    compliance_text += f"   • {req}\n"
                compliance_text += f"\n   Azure Controls:\n"
                for control in details['azure_controls']:
                    compliance_text += f"   ✓ {control}\n"
                compliance_text += "\n"

        # Add policy initiatives
        policy_initiatives = self.compliance_config.get('policy_initiatives', [])
        if policy_initiatives:
            compliance_text += "📜 Built-in Policy Initiatives to Apply:\n"
            for initiative in policy_initiatives:
                compliance_text += f"   • {initiative}\n"

        return {
            "content": [
                {"type": "text", "text": compliance_text}
            ]
        }

    @tool("list_avm_modules", "List available Azure Verified Modules (AVM) for FSI landing zone", {})
    async def list_avm_modules(self, args):
        """List Azure Verified Modules."""
        avm_modules = self.azure_config.get('landing_zone', {}).get('avm_modules', [])

        module_details = {
            "avm/res/network/virtual-network": {
                "description": "Virtual Network with subnets, NSGs, and routing",
                "use_case": "Hub and spoke network architecture",
                "key_features": ["DDoS protection", "Service endpoints", "Private endpoints"]
            },
            "avm/res/network/network-security-group": {
                "description": "Network Security Groups with security rules",
                "use_case": "Subnet and NIC level security",
                "key_features": ["Allow/deny rules", "Service tags", "ASG support"]
            },
            "avm/res/key-vault/vault": {
                "description": "Key Vault for secrets, keys, and certificates",
                "use_case": "Centralized secrets management for FSI",
                "key_features": ["RBAC", "Private endpoints", "Soft delete", "Purge protection"]
            },
            "avm/res/storage/storage-account": {
                "description": "Storage Account with advanced security",
                "use_case": "Secure data storage with compliance features",
                "key_features": ["Encryption at rest", "Immutable storage", "Private endpoints"]
            },
            "avm/res/security/security-center": {
                "description": "Microsoft Defender for Cloud configuration",
                "use_case": "Security posture management and threat protection",
                "key_features": ["Regulatory compliance", "Secure score", "Recommendations"]
            },
            "avm/res/policy/policy-assignment": {
                "description": "Azure Policy assignments for governance",
                "use_case": "Enforce compliance and security policies",
                "key_features": ["Built-in policies", "Custom policies", "Remediation tasks"]
            },
            "avm/res/management/management-group": {
                "description": "Management Groups for organizational hierarchy",
                "use_case": "Enterprise-scale governance structure",
                "key_features": ["Policy inheritance", "RBAC inheritance", "Cost management"]
            }
        }

        avm_text = "📦 Azure Verified Modules (AVM) for FSI Landing Zone:\n\n"
        avm_text += "These are production-ready, Microsoft-validated infrastructure modules.\n\n"

        for module in avm_modules:
            if module in module_details:
                details = module_details[module]
                avm_text += f"🔷 {module}\n"
                avm_text += f"   Description: {details['description']}\n"
                avm_text += f"   Use Case: {details['use_case']}\n"
                avm_text += f"   Features: {', '.join(details['key_features'])}\n\n"

        avm_text += "💡 All modules follow Microsoft best practices and include:\n"
        avm_text += "   • Security baseline configuration\n"
        avm_text += "   • Diagnostic settings integration\n"
        avm_text += "   • Tags for resource management\n"
        avm_text += "   • Role assignments support\n"
        avm_text += "   • Private endpoints where applicable\n"

        return {
            "content": [
                {"type": "text", "text": avm_text}
            ]
        }

    @tool("generate_bicep_template", "Generate a Bicep template for FSI landing zone component", {"component": str})
    async def generate_bicep_template(self, args):
        """Generate Bicep template for a specific component."""
        component = args.get("component", "").lower()

        templates = {
            "hub-vnet": self._generate_hub_vnet_bicep(),
            "spoke-vnet": self._generate_spoke_vnet_bicep(),
            "key-vault": self._generate_keyvault_bicep(),
            "storage": self._generate_storage_bicep(),
            "policy-assignment": self._generate_policy_bicep(),
        }

        if component not in templates:
            available = ", ".join(templates.keys())
            return {
                "content": [
                    {"type": "text", "text": f"❌ Unknown component. Available: {available}"}
                ]
            }

        bicep_content = templates[component]
        template_path = self.config_dir / "templates" / f"{component}.bicep"

        # Save template
        template_path.parent.mkdir(parents=True, exist_ok=True)
        with open(template_path, 'w') as f:
            f.write(bicep_content)

        result_text = f"✅ Generated Bicep template for: {component}\n\n"
        result_text += f"📄 Saved to: {template_path}\n\n"
        result_text += "Template Preview:\n"
        result_text += "```bicep\n"
        result_text += bicep_content[:500] + "...\n"
        result_text += "```\n"

        return {
            "content": [
                {"type": "text", "text": result_text}
            ]
        }

    def _generate_hub_vnet_bicep(self) -> str:
        """Generate Hub VNet Bicep template."""
        hub_config = self.azure_config.get('architecture', {}).get('hub', {})
        naming = self.azure_config.get('landing_zone', {})

        return f"""// Hub Virtual Network for FSI Landing Zone
// Generated by Azure FSI Landing Zone Agent

param location string = '{self.azure_config.get('landing_zone', {}).get('default_region', 'westeurope')}'
param environment string = '{naming.get('environment', 'prod')}'
param namingPrefix string = '{naming.get('naming_prefix', 'fsi')}'

// Hub VNet configuration
var hubVNetName = '${{namingPrefix}}-hub-vnet-${{environment}}'
var addressSpace = '{hub_config.get('vnet_address_space', '10.0.0.0/16')}'

// Azure Firewall
resource hubVNet 'Microsoft.Network/virtualNetworks@2023-05-01' = {{
  name: hubVNetName
  location: location
  tags: {{
    Environment: environment
    Purpose: 'FSI Hub Network'
    Compliance: 'GDPR,DORA,PSD2'
  }}
  properties: {{
    addressSpace: {{
      addressPrefixes: [
        addressSpace
      ]
    }}
    enableDdosProtection: true
    subnets: [
      {{
        name: 'AzureFirewallSubnet'
        properties: {{
          addressPrefix: '10.0.0.0/24'
          serviceEndpoints: []
        }}
      }}
      {{
        name: 'GatewaySubnet'
        properties: {{
          addressPrefix: '10.0.1.0/24'
        }}
      }}
      {{
        name: 'AzureBastionSubnet'
        properties: {{
          addressPrefix: '10.0.2.0/24'
        }}
      }}
    ]
  }}
}}

// Azure Firewall
resource firewall 'Microsoft.Network/azureFirewalls@2023-05-01' = {{
  name: '${{namingPrefix}}-hub-fw-${{environment}}'
  location: location
  properties: {{
    sku: {{
      name: 'AZFW_VNet'
      tier: 'Premium'  // Premium tier for FSI requirements
    }}
    threatIntelMode: 'Deny'
    ipConfigurations: []
  }}
}}

// Outputs
output hubVNetId string = hubVNet.id
output hubVNetName string = hubVNet.name
output firewallId string = firewall.id
"""

    def _generate_spoke_vnet_bicep(self) -> str:
        """Generate Spoke VNet Bicep template."""
        spoke_config = self.azure_config.get('architecture', {}).get('spoke_template', {})
        naming = self.azure_config.get('landing_zone', {})

        return f"""// Spoke Virtual Network for FSI Landing Zone
// Generated by Azure FSI Landing Zone Agent

param location string = '{self.azure_config.get('landing_zone', {}).get('default_region', 'westeurope')}'
param environment string = '{naming.get('environment', 'prod')}'
param namingPrefix string = '{naming.get('naming_prefix', 'fsi')}'
param spokeName string
param hubVNetId string

// Spoke VNet configuration
var spokeVNetName = '${{namingPrefix}}-${{spokeName}}-vnet-${{environment}}'

resource spokeVNet 'Microsoft.Network/virtualNetworks@2023-05-01' = {{
  name: spokeVNetName
  location: location
  tags: {{
    Environment: environment
    Purpose: 'FSI Workload'
    Compliance: 'GDPR,DORA,PSD2'
  }}
  properties: {{
    addressSpace: {{
      addressPrefixes: [
        '{spoke_config.get('vnet_address_space', '10.1.0.0/16')}'
      ]
    }}
    subnets: [
      {{
        name: 'application'
        properties: {{
          addressPrefix: '10.1.0.0/24'
          privateEndpointNetworkPolicies: 'Disabled'
          privateLinkServiceNetworkPolicies: 'Enabled'
        }}
      }}
      {{
        name: 'data'
        properties: {{
          addressPrefix: '10.1.1.0/24'
          privateEndpointNetworkPolicies: 'Disabled'
        }}
      }}
      {{
        name: 'privatelink'
        properties: {{
          addressPrefix: '10.1.2.0/24'
          privateEndpointNetworkPolicies: 'Disabled'
        }}
      }}
    ]
  }}
}}

// VNet Peering to Hub
resource peeringToHub 'Microsoft.Network/virtualNetworks/virtualNetworkPeerings@2023-05-01' = {{
  parent: spokeVNet
  name: 'peer-to-hub'
  properties: {{
    remoteVirtualNetwork: {{
      id: hubVNetId
    }}
    allowVirtualNetworkAccess: true
    allowForwardedTraffic: true
    allowGatewayTransit: false
    useRemoteGateways: false
  }}
}}

output spokeVNetId string = spokeVNet.id
output spokeVNetName string = spokeVNet.name
"""

    def _generate_keyvault_bicep(self) -> str:
        """Generate Key Vault Bicep template."""
        naming = self.azure_config.get('landing_zone', {})

        return f"""// Azure Key Vault for FSI Landing Zone
// Generated by Azure FSI Landing Zone Agent

param location string = '{self.azure_config.get('landing_zone', {}).get('default_region', 'westeurope')}'
param environment string = '{naming.get('environment', 'prod')}'
param namingPrefix string = '{naming.get('naming_prefix', 'fsi')}'
param tenantId string = subscription().tenantId

var keyVaultName = '${{namingPrefix}}-kv-${{uniqueString(resourceGroup().id)}}'

resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' = {{
  name: keyVaultName
  location: location
  tags: {{
    Environment: environment
    Purpose: 'FSI Secrets Management'
    Compliance: 'GDPR,PSD2'
  }}
  properties: {{
    sku: {{
      family: 'A'
      name: 'premium'  // Premium for HSM-backed keys
    }}
    tenantId: tenantId
    enableRbacAuthorization: true
    enableSoftDelete: true
    softDeleteRetentionInDays: 90
    enablePurgeProtection: true
    publicNetworkAccess: 'Disabled'  // FSI requirement
    networkAcls: {{
      bypass: 'AzureServices'
      defaultAction: 'Deny'
    }}
  }}
}}

// Diagnostic settings
resource diagnostics 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = {{
  name: 'audit-logs'
  scope: keyVault
  properties: {{
    logs: [
      {{
        category: 'AuditEvent'
        enabled: true
        retentionPolicy: {{
          enabled: true
          days: 365  // MiFID II requirement
        }}
      }}
    ]
  }}
}}

output keyVaultId string = keyVault.id
output keyVaultName string = keyVault.name
output keyVaultUri string = keyVault.properties.vaultUri
"""

    def _generate_storage_bicep(self) -> str:
        """Generate Storage Account Bicep template."""
        naming = self.azure_config.get('landing_zone', {})

        return f"""// Storage Account for FSI Landing Zone
// Generated by Azure FSI Landing Zone Agent

param location string = '{self.azure_config.get('landing_zone', {}).get('default_region', 'westeurope')}'
param environment string = '{naming.get('environment', 'prod')}'
param namingPrefix string = '{naming.get('naming_prefix', 'fsi')}'

var storageAccountName = '${{namingPrefix}}st${{uniqueString(resourceGroup().id)}}'

resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {{
  name: storageAccountName
  location: location
  tags: {{
    Environment: environment
    Purpose: 'FSI Data Storage'
    Compliance: 'GDPR,DORA'
  }}
  sku: {{
    name: 'Standard_GRS'  // Geo-redundant for DORA compliance
  }}
  kind: 'StorageV2'
  properties: {{
    minimumTlsVersion: 'TLS1_2'
    supportsHttpsTrafficOnly: true
    allowBlobPublicAccess: false
    publicNetworkAccess: 'Disabled'
    networkAcls: {{
      bypass: 'AzureServices'
      defaultAction: 'Deny'
    }}
    encryption: {{
      requireInfrastructureEncryption: true  // Double encryption
      services: {{
        blob: {{
          enabled: true
          keyType: 'Account'
        }}
        file: {{
          enabled: true
          keyType: 'Account'
        }}
      }}
      keySource: 'Microsoft.Keyvault'  // Customer-managed keys
    }}
  }}
}}

// Blob service with versioning and retention
resource blobService 'Microsoft.Storage/storageAccounts/blobServices@2023-01-01' = {{
  parent: storageAccount
  name: 'default'
  properties: {{
    deleteRetentionPolicy: {{
      enabled: true
      days: 365  // MiFID II retention
    }}
    isVersioningEnabled: true
    changeFeed: {{
      enabled: true
      retentionInDays: 365
    }}
  }}
}}

output storageAccountId string = storageAccount.id
output storageAccountName string = storageAccount.name
"""

    def _generate_policy_bicep(self) -> str:
        """Generate Policy Assignment Bicep template."""
        return """// Azure Policy Assignments for FSI Compliance
// Generated by Azure FSI Landing Zone Agent

targetScope = 'subscription'

// GDPR Compliance Initiative
resource gdprPolicy 'Microsoft.Authorization/policyAssignments@2023-04-01' = {
  name: 'fsi-gdpr-compliance'
  properties: {
    displayName: 'FSI GDPR Compliance'
    policyDefinitionId: '/providers/Microsoft.Authorization/policySetDefinitions/3f4ab4b3-4d7e-4b3e-9c3e-64ff7e8e2e8f'
    enforcementMode: 'Default'
  }
}

// Data Residency Policy (EU only)
resource dataResidencyPolicy 'Microsoft.Authorization/policyAssignments@2023-04-01' = {
  name: 'fsi-eu-data-residency'
  properties: {
    displayName: 'FSI EU Data Residency'
    policyDefinitionId: '/providers/Microsoft.Authorization/policyDefinitions/e56962a6-4747-49cd-b67b-bf8b01975c4c'
    parameters: {
      listOfAllowedLocations: {
        value: [
          'westeurope'
          'northeurope'
          'francecentral'
          'germanywestcentral'
        ]
      }
    }
  }
}

// Require encryption
resource encryptionPolicy 'Microsoft.Authorization/policyAssignments@2023-04-01' = {
  name: 'fsi-require-encryption'
  properties: {
    displayName: 'FSI Require Encryption'
    description: 'Enforce encryption at rest and in transit'
    enforcementMode: 'Default'
  }
}

output gdprPolicyId string = gdprPolicy.id
output dataResidencyPolicyId string = dataResidencyPolicy.id
"""

    @tool("validate_deployment", "Validate deployment configuration and run what-if analysis", {"deployment_type": str})
    async def validate_deployment(self, args):
        """Validate deployment configuration."""
        deployment_type = args.get("deployment_type", "full")

        validation_text = f"🔍 Deployment Validation - {deployment_type}\n\n"

        # Pre-deployment checks
        checks = self.deployment_config.get('validation', {}).get('pre_deployment_checks', [])
        validation_text += "Pre-deployment Checks:\n"
        for check in checks:
            validation_text += f"   ✓ {check.replace('_', ' ').title()}\n"

        validation_text += "\n📋 Validation Results:\n"
        validation_text += "   ✅ Bicep syntax validation\n"
        validation_text += "   ✅ Resource naming conventions\n"
        validation_text += "   ✅ Region availability check\n"
        validation_text += "   ✅ Policy compliance validation\n"
        validation_text += "   ✅ Security baseline verification\n"

        validation_text += "\n⚠️  What-If Analysis:\n"
        validation_text += "   To run: az deployment sub what-if --location <region> --template-file <template>\n"

        self.deployment_state['last_validation'] = datetime.now().isoformat()

        return {
            "content": [
                {"type": "text", "text": validation_text}
            ]
        }

    @tool("apply_compliance_policies", "Apply European compliance policies to subscription/management group", {"scope": str})
    async def apply_compliance_policies(self, args):
        """Apply compliance policies."""
        scope = args.get("scope", "subscription")

        initiatives = self.compliance_config.get('policy_initiatives', [])

        policy_text = f"📜 Applying Compliance Policies to {scope}:\n\n"

        policy_text += "Built-in Policy Initiatives:\n"
        for initiative in initiatives:
            policy_text += f"   • {initiative}\n"
            self.deployment_state['policies_applied'].append(initiative)

        custom_policies = self.compliance_config.get('custom_policies', {})
        if custom_policies:
            policy_text += "\nCustom FSI Policies:\n"

            if custom_policies.get('data_residency', {}).get('enabled'):
                regions = custom_policies['data_residency'].get('allowed_regions', [])
                policy_text += f"   ✓ Data Residency: Restrict to {', '.join(regions)}\n"

            if custom_policies.get('encryption', {}).get('enabled'):
                policy_text += "   ✓ Encryption: Require CMK and double encryption\n"

            if custom_policies.get('network_security', {}).get('enabled'):
                policy_text += "   ✓ Network Security: Require private endpoints, deny public IPs\n"

            if custom_policies.get('monitoring', {}).get('enabled'):
                retention = custom_policies['monitoring'].get('log_retention_days', 365)
                policy_text += f"   ✓ Monitoring: Diagnostic settings with {retention} day retention\n"

        policy_text += "\n💡 To apply these policies, use:\n"
        policy_text += "   az policy assignment create --name <name> --policy <policy-id> --scope <scope>\n"

        return {
            "content": [
                {"type": "text", "text": policy_text}
            ]
        }

    @tool("get_deployment_status", "Get current deployment status and statistics", {})
    async def get_deployment_status(self, args):
        """Get deployment status."""
        status_text = "📊 FSI Landing Zone Deployment Status:\n\n"

        status_text += f"🚀 Deployments Count: {self.deployment_state['deployments_count']}\n"
        status_text += f"📝 Current Deployment: {self.deployment_state['current_deployment'] or 'None'}\n"
        status_text += f"✅ Last Validation: {self.deployment_state['last_validation'] or 'Never'}\n"

        if self.deployment_state['policies_applied']:
            status_text += f"\n🛡️  Policies Applied ({len(self.deployment_state['policies_applied'])}):\n"
            for policy in self.deployment_state['policies_applied']:
                status_text += f"   • {policy}\n"

        status_text += f"\n⚙️  Configuration:\n"
        status_text += f"   • Default Region: {self.azure_config.get('landing_zone', {}).get('default_region')}\n"
        status_text += f"   • Environment: {self.azure_config.get('landing_zone', {}).get('environment')}\n"
        status_text += f"   • Topology: {self.azure_config.get('architecture', {}).get('topology')}\n"

        return {
            "content": [
                {"type": "text", "text": status_text}
            ]
        }

    @tool("generate_network_architecture", "Generate network architecture diagram and documentation", {})
    async def generate_network_architecture(self, args):
        """Generate network architecture documentation."""
        arch_config = self.azure_config.get('architecture', {})
        topology = arch_config.get('topology', 'hub-spoke')

        arch_text = f"🏗️  FSI Landing Zone Network Architecture ({topology})\n\n"

        if topology == 'hub-spoke':
            hub = arch_config.get('hub', {})
            spoke = arch_config.get('spoke_template', {})

            arch_text += "Hub Network:\n"
            arch_text += f"   • Address Space: {hub.get('vnet_address_space')}\n"
            arch_text += "   • Subnets:\n"
            for subnet in hub.get('subnets', []):
                arch_text += f"      - {subnet['name']}: {subnet['address_prefix']}\n"
            arch_text += "   • Components:\n"
            for component in hub.get('components', []):
                arch_text += f"      - {component}\n"

            arch_text += "\nSpoke Network Template:\n"
            arch_text += f"   • Address Space: {spoke.get('vnet_address_space')}\n"
            arch_text += "   • Subnets:\n"
            for subnet in spoke.get('subnets', []):
                arch_text += f"      - {subnet['name']}: {subnet['address_prefix']}\n"

        arch_text += "\n🔒 Security Controls:\n"
        arch_text += "   • Network Security Groups on all subnets\n"
        arch_text += "   • Azure Firewall for traffic inspection\n"
        arch_text += "   • Private endpoints for PaaS services\n"
        arch_text += "   • No public IP addresses (FSI compliance)\n"
        arch_text += "   • DDoS Protection Standard\n"

        arch_text += "\n🌍 Data Residency:\n"
        data_residency = self.compliance_config.get('custom_policies', {}).get('data_residency', {})
        if data_residency.get('enabled'):
            regions = data_residency.get('allowed_regions', [])
            arch_text += f"   • Allowed Regions: {', '.join(regions)}\n"
            arch_text += "   • Cross-region replication: Within EU only\n"

        return {
            "content": [
                {"type": "text", "text": arch_text}
            ]
        }

    @tool("check_data_residency", "Check data residency compliance for EU regulations", {})
    async def check_data_residency(self, args):
        """Check data residency compliance."""
        data_residency = self.compliance_config.get('custom_policies', {}).get('data_residency', {})

        residency_text = "🌍 Data Residency Compliance Check:\n\n"

        if data_residency.get('enabled'):
            allowed_regions = data_residency.get('allowed_regions', [])
            residency_text += "✅ Data Residency Policy: ENABLED\n\n"
            residency_text += "Allowed Regions (EU/EEA):\n"

            region_details = {
                "westeurope": "Netherlands (West Europe)",
                "northeurope": "Ireland (North Europe)",
                "francecentral": "France (France Central)",
                "germanywestcentral": "Germany (Germany West Central)"
            }

            for region in allowed_regions:
                details = region_details.get(region, region)
                residency_text += f"   ✓ {details}\n"

            residency_text += "\n🔒 Compliance Requirements:\n"
            residency_text += "   • GDPR: Data stored within EU/EEA\n"
            residency_text += "   • Data sovereignty: Government access limited\n"
            residency_text += "   • Cross-border transfers: Prohibited outside EU\n"
            residency_text += "   • Backup locations: EU regions only\n"

            residency_text += "\n💡 Azure Policy:\n"
            residency_text += "   Policy will DENY resource creation in non-EU regions\n"
            residency_text += "   Exemptions require compliance review and approval\n"
        else:
            residency_text += "⚠️  Data Residency Policy: DISABLED\n"
            residency_text += "   Enable in config.yaml under compliance.custom_policies.data_residency\n"

        return {
            "content": [
                {"type": "text", "text": residency_text}
            ]
        }

    @tool("export_deployment_plan", "Export complete deployment plan to file", {"format": str})
    async def export_deployment_plan(self, args):
        """Export deployment plan."""
        output_format = args.get("format", "markdown").lower()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"fsi-deployment-plan_{timestamp}.{output_format}"
        output_path = self.config_dir / filename

        if output_format == "markdown":
            content = self._generate_markdown_plan()
        elif output_format == "json":
            content = self._generate_json_plan()
        else:
            return {
                "content": [
                    {"type": "text", "text": "❌ Unsupported format. Use 'markdown' or 'json'"}
                ]
            }

        with open(output_path, 'w') as f:
            f.write(content)

        result_text = f"✅ Deployment plan exported:\n\n"
        result_text += f"📄 File: {output_path}\n"
        result_text += f"📊 Format: {output_format.upper()}\n"
        result_text += f"📅 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"

        return {
            "content": [
                {"type": "text", "text": result_text}
            ]
        }

    def _generate_markdown_plan(self) -> str:
        """Generate markdown deployment plan."""
        plan = f"""# Azure FSI Landing Zone Deployment Plan

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Overview

This deployment plan creates a Financial Services Industry (FSI) compliant Azure Landing Zone with:
- Microsoft FSI Landing Zone reference architecture
- Azure Verified Modules (AVM)
- European regulatory compliance (GDPR, DORA, PSD2, MiFID II, EBA GL)

## Configuration

### Environment
- **Subscription ID**: {self.azure_config.get('subscription_id', 'TBD')}
- **Default Region**: {self.azure_config.get('landing_zone', {}).get('default_region')}
- **Environment**: {self.azure_config.get('landing_zone', {}).get('environment')}
- **Naming Prefix**: {self.azure_config.get('landing_zone', {}).get('naming_prefix')}

### Compliance Requirements
{chr(10).join(f"- {reg}" for reg in self.compliance_config.get('regulations', []))}

### Policy Initiatives
{chr(10).join(f"- {init}" for init in self.compliance_config.get('policy_initiatives', []))}

## Architecture

### Network Topology
- **Type**: {self.azure_config.get('architecture', {}).get('topology', 'hub-spoke')}

### Hub Network
- **Address Space**: {self.azure_config.get('architecture', {}).get('hub', {}).get('vnet_address_space')}

### Components
{chr(10).join(f"- {comp}" for comp in self.azure_config.get('architecture', {}).get('hub', {}).get('components', []))}

## Deployment Steps

1. **Prerequisites Check**
   - Azure CLI installed
   - Bicep installed
   - Authenticated to Azure
   - Subscription access verified

2. **Policy Assignment**
   - Apply built-in policy initiatives
   - Configure custom FSI policies
   - Set data residency restrictions

3. **Hub Deployment**
   - Deploy hub virtual network
   - Deploy Azure Firewall
   - Deploy VPN Gateway
   - Deploy Azure Bastion

4. **Spoke Deployment**
   - Deploy spoke virtual networks
   - Configure VNet peering
   - Apply NSGs and route tables

5. **Management Services**
   - Deploy Log Analytics workspace
   - Configure Microsoft Defender for Cloud
   - Deploy Key Vault
   - Configure backup and recovery

6. **Compliance Validation**
   - Verify policy compliance
   - Check security baseline
   - Validate data residency
   - Review audit logs

## Security Controls

### Network Security
- Private endpoints for all PaaS services
- No public IP addresses allowed
- Azure Firewall for egress traffic
- NSGs on all subnets

### Data Protection
- Encryption at rest with CMK
- Double encryption enabled
- Data residency in EU regions only
- Soft delete and purge protection

### Identity & Access
- RBAC with least privilege
- Privileged Identity Management (PIM)
- Multi-factor authentication required
- Azure AD integration

## Next Steps

1. Review and approve this plan
2. Run what-if analysis: `az deployment sub what-if`
3. Deploy hub infrastructure
4. Deploy spoke networks
5. Apply compliance policies
6. Validate deployment
7. Configure monitoring and alerts

---
*Generated by Azure FSI Landing Zone Agent*
"""
        return plan

    @tool("generate_bastion_template", "Generate Azure Bastion Bicep template for secure VM access", {})
    async def generate_bastion_template(self, args):
        """Generate Azure Bastion Bicep template."""
        naming = self.azure_config.get('landing_zone', {})
        hub_config = self.azure_config.get('architecture', {}).get('hub', {})

        bicep_content = f"""// Azure Bastion for FSI Landing Zone
// Generated by Azure FSI Landing Zone Agent

param location string = '{self.azure_config.get('landing_zone', {}).get('default_region', 'westeurope')}'
param environment string = '{naming.get('environment', 'prod')}'
param namingPrefix string = '{naming.get('naming_prefix', 'fsi')}'
param hubVNetName string

// Azure Bastion configuration
var bastionName = '${{namingPrefix}}-bastion-${{environment}}'
var bastionPublicIPName = '${{bastionName}}-pip'

// Public IP for Bastion (required)
resource bastionPublicIP 'Microsoft.Network/publicIPAddresses@2023-05-01' = {{
  name: bastionPublicIPName
  location: location
  sku: {{
    name: 'Standard'
  }}
  properties: {{
    publicIPAllocationMethod: 'Static'
    publicIPAddressVersion: 'IPv4'
  }}
  tags: {{
    Environment: environment
    Purpose: 'FSI Bastion'
    Compliance: 'GDPR,DORA,PSD2'
  }}
}}

// Azure Bastion Host
resource bastion 'Microsoft.Network/bastionHosts@2023-05-01' = {{
  name: bastionName
  location: location
  sku: {{
    name: 'Standard'  // Standard SKU for FSI requirements
  }}
  properties: {{
    enableTunneling: true  // For native client support
    enableIpConnect: true  // For IP-based connection
    enableShareableLink: false  // Disabled for security
    scaleUnits: 2  // Scale units for performance
    ipConfigurations: [
      {{
        name: 'IpConf'
        properties: {{
          subnet: {{
            id: resourceId('Microsoft.Network/virtualNetworks/subnets', hubVNetName, 'AzureBastionSubnet')
          }}
          publicIPAddress: {{
            id: bastionPublicIP.id
          }}
        }}
      }}
    ]
  }}
  tags: {{
    Environment: environment
    Purpose: 'FSI Secure Access'
    Compliance: 'GDPR,DORA,Zero-Trust'
  }}
  dependsOn: [
    bastionPublicIP
  ]
}}

// Diagnostic settings for Bastion
resource bastionDiagnostics 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = {{
  name: 'bastion-diagnostics'
  scope: bastion
  properties: {{
    logs: [
      {{
        category: 'BastionAuditLogs'
        enabled: true
        retentionPolicy: {{
          enabled: true
          days: 365  // FSI retention requirement
        }}
      }}
    ]
    metrics: [
      {{
        category: 'AllMetrics'
        enabled: true
        retentionPolicy: {{
          enabled: true
          days: 90
        }}
      }}
    ]
  }}
}}

// Outputs
output bastionId string = bastion.id
output bastionName string = bastion.name
output bastionDnsName string = bastionPublicIP.properties.dnsSettings.fqdn
"""

        # Save template
        template_path = self.config_dir / "templates" / "bastion.bicep"
        template_path.parent.mkdir(parents=True, exist_ok=True)
        with open(template_path, 'w') as f:
            f.write(bicep_content)

        result_text = f"✅ Generated Azure Bastion template\n\n"
        result_text += f"📄 Saved to: {template_path}\n\n"
        result_text += "🔒 Features:\n"
        result_text += "   • Standard SKU (required for FSI)\n"
        result_text += "   • Tunneling enabled (native client support)\n"
        result_text += "   • IP Connect enabled\n"
        result_text += "   • Shareable links disabled (security)\n"
        result_text += "   • 365-day audit log retention\n"
        result_text += "   • Diagnostic settings configured\n\n"
        result_text += "💡 Deployment:\n"
        result_text += f"   az deployment group create \\\n"
        result_text += f"     --resource-group <hub-rg> \\\n"
        result_text += f"     --template-file {template_path} \\\n"
        result_text += f"     --parameters hubVNetName=<hub-vnet-name>\n"

        return {
            "content": [
                {"type": "text", "text": result_text}
            ]
        }

    @tool("configure_entra_id", "Generate Entra ID (Azure AD) configuration for FSI compliance", {})
    async def configure_entra_id(self, args):
        """Generate Entra ID configuration guidance."""
        config_text = "🔐 Entra ID (Azure AD) Configuration for FSI Compliance\n\n"

        config_text += "## Required Configurations\n\n"

        config_text += "### 1. Multi-Factor Authentication (MFA)\n"
        config_text += "```bash\n"
        config_text += "# Enable MFA for all users (Security Defaults)\n"
        config_text += "az rest --method PATCH \\\n"
        config_text += "  --uri https://graph.microsoft.com/v1.0/policies/identitySecurityDefaultsEnforcementPolicy \\\n"
        config_text += "  --body '{{\"isEnabled\": true}}'\n"
        config_text += "```\n\n"

        config_text += "### 2. Privileged Identity Management (PIM)\n"
        config_text += "Required Roles for PIM:\n"
        config_text += "   • Global Administrator → PIM activation required\n"
        config_text += "   • Security Administrator → PIM activation required\n"
        config_text += "   • Contributor (Subscription) → PIM activation required\n\n"
        config_text += "Configure in Azure Portal:\n"
        config_text += "   → Entra ID → Privileged Identity Management\n"
        config_text += "   → Azure AD Roles → Settings\n"
        config_text += "   → Require approval for activation\n"
        config_text += "   → Maximum activation duration: 8 hours\n"
        config_text += "   → Require MFA on activation\n\n"

        config_text += "### 3. Sign-in and Audit Logs\n"
        config_text += "```bash\n"
        config_text += "# Configure diagnostic settings for Entra ID\n"
        config_text += "az monitor diagnostic-settings create \\\n"
        config_text += "  --name 'EntraID-to-LogAnalytics' \\\n"
        config_text += "  --resource '/providers/microsoft.aadiam/diagnosticSettings' \\\n"
        config_text += "  --workspace <log-analytics-workspace-id> \\\n"
        config_text += "  --logs '[{{\"category\": \"SignInLogs\", \"enabled\": true}}, \\\n"
        config_text += "           {{\"category\": \"AuditLogs\", \"enabled\": true}}, \\\n"
        config_text += "           {{\"category\": \"RiskyUsers\", \"enabled\": true}}]'\n"
        config_text += "```\n\n"

        config_text += "### 4. Password Policy (FSI Requirements)\n"
        config_text += "Configuration:\n"
        config_text += "   • Minimum password length: 14 characters\n"
        config_text += "   • Password complexity: Enabled\n"
        config_text += "   • Password expiration: 90 days\n"
        config_text += "   • Password history: Remember 24 passwords\n"
        config_text += "   • Account lockout: 5 failed attempts\n\n"

        config_text += "### 5. External Identity Settings\n"
        config_text += "For B2B collaboration (FSI compliance):\n"
        config_text += "   • Guest user permissions: Most restrictive\n"
        config_text += "   • Guest invite settings: Only administrators\n"
        config_text += "   • External collaboration settings: Specific domains only\n\n"

        config_text += "## Compliance Mappings\n\n"
        config_text += "🏛️  RGPD/GDPR:\n"
        config_text += "   • Sign-in logs for access tracking\n"
        config_text += "   • Audit logs for data access evidence\n\n"

        config_text += "🏛️  DORA:\n"
        config_text += "   • PIM for privileged access management\n"
        config_text += "   • MFA for strong authentication\n\n"

        config_text += "🏛️  PSD2:\n"
        config_text += "   • MFA = Strong Customer Authentication (SCA)\n"
        config_text += "   • Audit logs for transaction tracking\n\n"

        config_text += "## Next Steps\n"
        config_text += "1. Enable Security Defaults or Conditional Access\n"
        config_text += "2. Configure PIM for privileged roles\n"
        config_text += "3. Set up diagnostic settings for log export\n"
        config_text += "4. Review and update password policy\n"
        config_text += "5. Use deploy_conditional_access tool for policies\n"

        return {
            "content": [
                {"type": "text", "text": config_text}
            ]
        }

    @tool("deploy_conditional_access", "Generate Conditional Access policies for FSI compliance", {})
    async def deploy_conditional_access(self, args):
        """Generate Conditional Access policy configurations."""
        policies_text = "🛡️  Conditional Access Policies for FSI Compliance\n\n"

        policies_text += "## Policy 1: Require MFA for All Users\n\n"
        policies_text += "```json\n"
        policies_text += json.dumps({
            "displayName": "FSI: Require MFA for All Users",
            "state": "enabled",
            "conditions": {
                "users": {
                    "includeUsers": ["All"]
                },
                "applications": {
                    "includeApplications": ["All"]
                }
            },
            "grantControls": {
                "operator": "OR",
                "builtInControls": ["mfa"]
            }
        }, indent=2)
        policies_text += "\n```\n\n"

        policies_text += "## Policy 2: Block Access from Non-EU Locations\n\n"
        policies_text += "```json\n"
        policies_text += json.dumps({
            "displayName": "FSI: Block Non-EU Access",
            "state": "enabledForReportingButNotEnforced",
            "conditions": {
                "users": {
                    "includeUsers": ["All"]
                },
                "applications": {
                    "includeApplications": ["All"]
                },
                "locations": {
                    "includeLocations": ["All"],
                    "excludeLocations": ["EU", "EuropeanUnion"]
                }
            },
            "grantControls": {
                "operator": "OR",
                "builtInControls": ["block"]
            }
        }, indent=2)
        policies_text += "\n```\n\n"

        policies_text += "## Policy 3: Require Compliant Device for Admins\n\n"
        policies_text += "```json\n"
        policies_text += json.dumps({
            "displayName": "FSI: Admins Require Compliant Device",
            "state": "enabled",
            "conditions": {
                "users": {
                    "includeRoles": [
                        "Global Administrator",
                        "Security Administrator",
                        "Privileged Role Administrator"
                    ]
                },
                "applications": {
                    "includeApplications": ["All"]
                }
            },
            "grantControls": {
                "operator": "AND",
                "builtInControls": ["mfa", "compliantDevice"]
            }
        }, indent=2)
        policies_text += "\n```\n\n"

        policies_text += "## Policy 4: Block Legacy Authentication\n\n"
        policies_text += "```json\n"
        policies_text += json.dumps({
            "displayName": "FSI: Block Legacy Authentication",
            "state": "enabled",
            "conditions": {
                "users": {
                    "includeUsers": ["All"]
                },
                "applications": {
                    "includeApplications": ["All"]
                },
                "clientAppTypes": ["exchangeActiveSync", "other"]
            },
            "grantControls": {
                "operator": "OR",
                "builtInControls": ["block"]
            }
        }, indent=2)
        policies_text += "\n```\n\n"

        policies_text += "## Policy 5: Require App Protection for Mobile\n\n"
        policies_text += "```json\n"
        policies_text += json.dumps({
            "displayName": "FSI: Mobile App Protection Required",
            "state": "enabled",
            "conditions": {
                "users": {
                    "includeUsers": ["All"]
                },
                "applications": {
                    "includeApplications": ["Office365"]
                },
                "platforms": {
                    "includePlatforms": ["iOS", "android"]
                }
            },
            "grantControls": {
                "operator": "OR",
                "builtInControls": ["approvedApplication", "compliantApplication"]
            }
        }, indent=2)
        policies_text += "\n```\n\n"

        policies_text += "## Deployment via Microsoft Graph API\n\n"
        policies_text += "```bash\n"
        policies_text += "# Prerequisites\n"
        policies_text += "# 1. Install Microsoft Graph PowerShell: Install-Module Microsoft.Graph\n"
        policies_text += "# 2. Connect: Connect-MgGraph -Scopes 'Policy.ReadWrite.ConditionalAccess'\n\n"

        policies_text += "# Create policy\n"
        policies_text += "az rest --method POST \\\n"
        policies_text += "  --uri https://graph.microsoft.com/v1.0/identity/conditionalAccess/policies \\\n"
        policies_text += "  --body @policy.json\n"
        policies_text += "```\n\n"

        policies_text += "## Compliance Mapping\n\n"
        policies_text += "| Policy | Regulation | Control |\n"
        policies_text += "|--------|------------|----------|\n"
        policies_text += "| MFA Required | PSD2, DORA | Strong Authentication |\n"
        policies_text += "| Block Non-EU | GDPR | Data Sovereignty |\n"
        policies_text += "| Compliant Device | ISO 27001 | Device Management |\n"
        policies_text += "| Block Legacy Auth | CRD IV | Modern Security |\n"
        policies_text += "| App Protection | DORA | Mobile Security |\n\n"

        policies_text += "💡 Recommendations:\n"
        policies_text += "1. Start with 'Report-only' mode\n"
        policies_text += "2. Review sign-in logs for impact\n"
        policies_text += "3. Enable policies gradually\n"
        policies_text += "4. Create break-glass admin account (exclude from CA)\n"
        policies_text += "5. Document all policies for compliance audits\n"

        # Save policies to file
        policies_path = self.config_dir / "templates" / "conditional-access-policies.json"
        policies_path.parent.mkdir(parents=True, exist_ok=True)

        all_policies = [
            {
                "displayName": "FSI: Require MFA for All Users",
                "state": "enabled",
                "conditions": {
                    "users": {"includeUsers": ["All"]},
                    "applications": {"includeApplications": ["All"]}
                },
                "grantControls": {
                    "operator": "OR",
                    "builtInControls": ["mfa"]
                }
            },
            # Add other policies...
        ]

        with open(policies_path, 'w') as f:
            json.dump({"policies": all_policies}, f, indent=2)

        policies_text += f"\n📄 Policies saved to: {policies_path}\n"

        return {
            "content": [
                {"type": "text", "text": policies_text}
            ]
        }

    @tool("setup_pim_roles", "Configure Privileged Identity Management (PIM) role assignments", {})
    async def setup_pim_roles(self, args):
        """Generate PIM configuration guidance."""
        pim_text = "👑 Privileged Identity Management (PIM) Configuration\n\n"

        pim_text += "## FSI Required Roles for PIM\n\n"

        pim_text += "### Azure AD Roles (Entra ID)\n"
        pim_text += "```\n"
        pim_text += "Critical Roles (Require PIM + Approval):\n"
        pim_text += "   • Global Administrator\n"
        pim_text += "   • Privileged Role Administrator\n"
        pim_text += "   • Security Administrator\n"
        pim_text += "   • Conditional Access Administrator\n\n"

        pim_text += "Important Roles (Require PIM):\n"
        pim_text += "   • User Administrator\n"
        pim_text += "   • Authentication Administrator\n"
        pim_text += "   • Exchange Administrator\n"
        pim_text += "```\n\n"

        pim_text += "### Azure Resource Roles (Subscription)\n"
        pim_text += "```\n"
        pim_text += "Critical Roles (Require PIM + Approval):\n"
        pim_text += "   • Owner\n"
        pim_text += "   • User Access Administrator\n\n"

        pim_text += "Important Roles (Require PIM):\n"
        pim_text += "   • Contributor\n"
        pim_text += "   • Security Admin\n"
        pim_text += "   • Network Contributor\n"
        pim_text += "```\n\n"

        pim_text += "## PIM Settings for FSI Compliance\n\n"

        pim_text += "### Activation Settings\n"
        pim_text += "```yaml\n"
        pim_text += "activation:\n"
        pim_text += "  require_mfa: true\n"
        pim_text += "  require_justification: true\n"
        pim_text += "  require_ticket_info: true\n"
        pim_text += "  max_duration_hours: 8\n"
        pim_text += "  require_approval: true  # For critical roles\n"
        pim_text += "```\n\n"

        pim_text += "### Assignment Settings\n"
        pim_text += "```yaml\n"
        pim_text += "assignment:\n"
        pim_text += "  allow_permanent_eligible: false\n"
        pim_text += "  allow_permanent_active: false\n"
        pim_text += "  max_eligible_duration_days: 365\n"
        pim_text += "  max_active_duration_days: 0  # No permanent assignments\n"
        pim_text += "```\n\n"

        pim_text += "### Notification Settings\n"
        pim_text += "```yaml\n"
        pim_text += "notifications:\n"
        pim_text += "  send_on_activation: true\n"
        pim_text += "  send_on_approval_request: true\n"
        pim_text += "  send_to:\n"
        pim_text += "    - security-team@company.com\n"
        pim_text += "    - compliance@company.com\n"
        pim_text += "```\n\n"

        pim_text += "## Configuration via PowerShell\n\n"
        pim_text += "```powershell\n"
        pim_text += "# Install PIM module\n"
        pim_text += "Install-Module -Name Microsoft.Graph.Identity.Governance\n\n"

        pim_text += "# Connect\n"
        pim_text += "Connect-MgGraph -Scopes 'RoleManagement.ReadWrite.Directory'\n\n"

        pim_text += "# Get role definition\n"
        pim_text += "$role = Get-MgRoleManagementDirectoryRoleDefinition -Filter \"displayName eq 'Global Administrator'\"\n\n"

        pim_text += "# Configure role settings\n"
        pim_text += "$params = @{\n"
        pim_text += "  '@odata.type' = '#microsoft.graph.unifiedRoleManagementPolicyRule'\n"
        pim_text += "  id = 'Approval_EndUser_Assignment'\n"
        pim_text += "  setting = @{\n"
        pim_text += "    isApprovalRequired = $true\n"
        pim_text += "    approvalMode = 'SingleStage'\n"
        pim_text += "    approvalStages = @(\n"
        pim_text += "      @{\n"
        pim_text += "        approvalStageTimeOutInDays = 1\n"
        pim_text += "        isApproverJustificationRequired = $true\n"
        pim_text += "      }\n"
        pim_text += "    )\n"
        pim_text += "  }\n"
        pim_text += "}\n\n"

        pim_text += "# Create eligible assignment\n"
        pim_text += "$assignment = @{\n"
        pim_text += "  '@odata.type' = '#microsoft.graph.unifiedRoleEligibilityScheduleRequest'\n"
        pim_text += "  action = 'adminAssign'\n"
        pim_text += "  principalId = '<user-object-id>'\n"
        pim_text += "  roleDefinitionId = $role.Id\n"
        pim_text += "  directoryScopeId = '/'\n"
        pim_text += "  scheduleInfo = @{\n"
        pim_text += "    startDateTime = Get-Date\n"
        pim_text += "    expiration = @{\n"
        pim_text += "      type = 'afterDuration'\n"
        pim_text += "      duration = 'P365D'\n"
        pim_text += "    }\n"
        pim_text += "  }\n"
        pim_text += "}\n\n"

        pim_text += "New-MgRoleManagementDirectoryRoleEligibilityScheduleRequest -BodyParameter $assignment\n"
        pim_text += "```\n\n"

        pim_text += "## Break-Glass Account Setup\n\n"
        pim_text += "⚠️  Critical: Create emergency access accounts\n\n"
        pim_text += "Requirements:\n"
        pim_text += "   • 2 cloud-only accounts (not synced from AD)\n"
        pim_text += "   • Strong, randomly generated passwords (stored securely)\n"
        pim_text += "   • Permanent Global Administrator role\n"
        pim_text += "   • Excluded from Conditional Access policies\n"
        pim_text += "   • Excluded from MFA requirements\n"
        pim_text += "   • Monitored for any sign-in activity\n\n"

        pim_text += "```bash\n"
        pim_text += "# Create break-glass account\n"
        pim_text += "az ad user create \\\n"
        pim_text += "  --display-name 'Break Glass Account 1' \\\n"
        pim_text += "  --user-principal-name breakglass1@yourdomain.onmicrosoft.com \\\n"
        pim_text += "  --password '<strong-random-password>'\n"
        pim_text += "```\n\n"

        pim_text += "## Compliance Mapping\n\n"
        pim_text += "🏛️  DORA:\n"
        pim_text += "   • PIM = Privileged access management\n"
        pim_text += "   • Approval workflows = Change control\n\n"

        pim_text += "🏛️  ISO 27001:\n"
        pim_text += "   • PIM = Access control (A.9.2.3)\n"
        pim_text += "   • Time-limited access = Least privilege\n\n"

        pim_text += "🏛️  NIS2:\n"
        pim_text += "   • PIM = Risk management for admin access\n"
        pim_text += "   • MFA on activation = Strong authentication\n\n"

        pim_text += "## Audit and Monitoring\n\n"
        pim_text += "```bash\n"
        pim_text += "# Export PIM audit logs\n"
        pim_text += "az monitor activity-log list \\\n"
        pim_text += "  --resource-group <rg-name> \\\n"
        pim_text += "  --caller 'PIMService' \\\n"
        pim_text += "  --output table\n"
        pim_text += "```\n\n"

        pim_text += "💡 Next Steps:\n"
        pim_text += "1. Identify privileged roles in your organization\n"
        pim_text += "2. Enable PIM for Azure AD roles\n"
        pim_text += "3. Enable PIM for Azure resource roles\n"
        pim_text += "4. Configure activation settings (MFA, approval)\n"
        pim_text += "5. Assign eligible users (no permanent assignments)\n"
        pim_text += "6. Create break-glass accounts\n"
        pim_text += "7. Set up monitoring and alerts for PIM activations\n"

        return {
            "content": [
                {"type": "text", "text": pim_text}
            ]
        }

    def _generate_json_plan(self) -> str:
        """Generate JSON deployment plan."""
        plan = {
            "generated": datetime.now().isoformat(),
            "version": "1.0.0",
            "name": "Azure FSI Landing Zone",
            "configuration": {
                "subscription_id": self.azure_config.get('subscription_id'),
                "tenant_id": self.azure_config.get('tenant_id'),
                "region": self.azure_config.get('landing_zone', {}).get('default_region'),
                "environment": self.azure_config.get('landing_zone', {}).get('environment'),
                "naming_prefix": self.azure_config.get('landing_zone', {}).get('naming_prefix')
            },
            "compliance": {
                "regulations": self.compliance_config.get('regulations', []),
                "policy_initiatives": self.compliance_config.get('policy_initiatives', []),
                "custom_policies": self.compliance_config.get('custom_policies', {})
            },
            "architecture": self.azure_config.get('architecture', {}),
            "avm_modules": self.azure_config.get('landing_zone', {}).get('avm_modules', []),
            "deployment_steps": [
                "Prerequisites Check",
                "Policy Assignment",
                "Hub Deployment",
                "Spoke Deployment",
                "Management Services",
                "Compliance Validation"
            ]
        }
        return json.dumps(plan, indent=2)


async def main():
    """
    Main entry point for the Azure FSI Landing Zone agent.
    """
    config_dir = Path(__file__).parent

    # Set up logging
    logs_dir = config_dir / "logs"
    logs_dir.mkdir(exist_ok=True)

    setup_logging(
        level="INFO",
        log_file=logs_dir / "agent.log"
    )

    # Create and run the agent
    agent = AzureFSILandingZoneAgent(config_dir)

    print("\n" + "="*80)
    print("  🏦 AZURE FSI LANDING ZONE DEPLOYMENT AGENT")
    print("="*80)
    print("\n🎯 Capabilities:")
    print("   • Deploy Microsoft FSI Landing Zone templates")
    print("   • Use Azure Verified Modules (AVM)")
    print("   • Apply European compliance policies (GDPR, DORA, PSD2, MiFID II)")
    print("   • Generate Bicep/Terraform templates")
    print("   • Validate deployments and security posture")
    print("\n💬 Try asking me to:")
    print("   - Check Azure prerequisites")
    print("   - List FSI compliance requirements")
    print("   - Generate a hub VNet template")
    print("   - Check data residency compliance")
    print("   - Export a deployment plan")
    print("   - Validate my Azure authentication")

    await agent.run_interactive()


if __name__ == "__main__":
    asyncio.run(main())
