# Azure FSI Landing Zone Agent

An AI-powered deployment agent for Azure Financial Services Industry (FSI) Landing Zones, built with Claude Agent SDK.

## Overview

This agent helps financial institutions deploy compliant, secure Azure infrastructure using:

- **Microsoft FSI Landing Zone Templates**: Industry-specific reference architectures
- **Azure Verified Modules (AVM)**: Production-ready, Microsoft-validated infrastructure modules
- **European Compliance**: Built-in policies for GDPR, DORA, PSD2, MiFID II, and EBA Guidelines

## 📌 Technology Stack Decision (October 2025)

### Why Bicep + AVM (Not Terraform ALZ)?

This agent uses **Bicep with Azure Verified Modules (AVM)** as the primary Infrastructure as Code approach. Here's why:

#### ✅ **Official Microsoft Recommendation**
- Microsoft's **FSI Landing Zone** is built with **Bicep + AVM**
- **Bicep AVM for Platform Landing Zone (ALZ)** is Microsoft's strategic direction (GA expected August 2025)
- Official Microsoft compliance documentation assumes Bicep deployments

#### ✅ **Simplicity**
- **Azure-native**: No external tooling beyond Azure CLI + Bicep
- **Simpler syntax**: More readable than Terraform/HCL
- **Fewer dependencies**: No Terraform state management complexity
- **Faster learning curve**: Especially for Azure-focused teams

#### ✅ **Trust & Support**
- **Microsoft officially supports AVM** (as of 2024)
- **Direct support path**: Issues go directly to Microsoft product teams
- **Verified and validated**: All modules follow Microsoft security baselines
- **Regular updates**: Aligned with Azure service releases

#### ✅ **Compliance & Audit**
- **Microsoft Cloud Security Benchmark (MCSB)**: Native integration
- **Regulatory compliance**: Built-in policy initiatives (GDPR, PCI-DSS, NIST, etc.)
- **Audit trail**: Bicep deployments are fully traceable in Azure Activity Log
- **Compliance mappings**: Microsoft provides mappings for Bicep-based deployments

#### 🔄 **What About Terraform?**

**Terraform ALZ Provider (`Azure/alz`)**: Available but not recommended for this use case because:
- ❌ **Adds complexity**: Requires managing Terraform in addition to Azure CLI
- ❌ **Different mental model**: HCL syntax vs Azure-native Bicep
- ❌ **Same underlying modules**: Uses the same AVM modules, just different syntax
- ❌ **Not FSI-first**: Microsoft's FSI guidance is Bicep-centric
- ⚠️ **Dual maintenance**: Would require maintaining both Bicep and Terraform templates

**When to use Terraform**:
- Your organization has a Terraform-first policy
- Multi-cloud deployments required (AWS + Azure)
- Existing Terraform expertise and tooling investment

**Note**: If Terraform is required, AVM modules work with both. However, for pure Azure FSI deployments, Bicep is simpler and officially recommended.

#### 📚 **References**
- [FSI Landing Zone Overview](https://learn.microsoft.com/en-us/industry/financial-services/fsi-lz) - Microsoft's official FSI guidance (uses Bicep + AVM)
- [Azure Verified Modules](https://azure.github.io/Azure-Verified-Modules/) - Official AVM documentation
- [Bicep Landing Zone Design](https://learn.microsoft.com/en-us/azure/architecture/landing-zones/bicep/landing-zone-bicep) - Architecture guidance
- [AVM Pattern Module for ALZ (Terraform)](https://github.com/Azure/terraform-azurerm-avm-ptn-alz) - If Terraform is required

#### 🎯 **Decision Summary**

| Criteria | Bicep + AVM | Terraform + AVM |
|----------|-------------|-----------------|
| **Simplicity** | ✅ Azure-native | ⚠️ External tooling |
| **FSI Alignment** | ✅ Microsoft recommended | ⚠️ Alternative path |
| **Compliance** | ✅ Native MCSB integration | ✅ Same policies, more complex |
| **Support** | ✅ Direct Microsoft support | ✅ Community + Microsoft |
| **Learning Curve** | ✅ Lower for Azure teams | ⚠️ Requires HCL knowledge |
| **Maintenance** | ✅ Single IaC language | ⚠️ Dual language complexity |

**Recommendation**: Use **Bicep + AVM** (current implementation) for FSI Landing Zones on Azure.

## Features

### 🏦 FSI-Specific Architecture
- Hub-spoke network topology optimized for financial services
- Secure network segmentation (application, data, management tiers)
- Azure Firewall Premium for advanced threat protection
- VPN Gateway and Azure Bastion for secure connectivity

### 🌍 European Regulatory Compliance
- **GDPR**: Data protection and privacy controls
- **DORA**: Digital operational resilience requirements
- **PSD2**: Strong customer authentication and API security
- **MiFID II**: Transaction reporting and audit trails
- **EBA Guidelines**: Cloud security and outsourcing requirements

### 🔒 Security Controls
- Data residency restricted to EU regions
- Encryption at rest with customer-managed keys (CMK)
- Double encryption for sensitive data
- Private endpoints for all PaaS services
- No public IP addresses (deny policy)
- Microsoft Defender for Cloud (Standard tier)

### 🛠️ Infrastructure as Code
- Bicep templates for Azure-native deployments
- Terraform support (optional)
- What-if analysis before deployment
- Automated validation and compliance checks

### 📦 Azure Verified Modules
Pre-configured modules for:
- Virtual Networks with security baselines
- Network Security Groups
- Azure Key Vault with HSM support
- Storage Accounts with immutable storage
- Azure Policy assignments
- Management Groups

## Prerequisites

1. **Azure CLI** (v2.50.0 or later)
   ```bash
   # Install Azure CLI
   curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
   ```

2. **Bicep** (v0.24.0 or later)
   ```bash
   # Install Bicep
   az bicep install
   ```

3. **Python** (3.10 or later)
   ```bash
   python --version
   ```

4. **Azure Subscription** with appropriate permissions:
   - Owner or Contributor role
   - Policy assignment permissions
   - Network resource creation rights

5. **Authentication**
   ```bash
   # Login to Azure
   az login

   # Set subscription
   az account set --subscription <subscription-id>
   ```

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd claude-agents
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   # Set Azure credentials
   export AZURE_SUBSCRIPTION_ID="<your-subscription-id>"
   export AZURE_TENANT_ID="<your-tenant-id>"

   # Set Anthropic API key
   export ANTHROPIC_API_KEY="<your-api-key>"
   ```

4. **Customize configuration**
   Edit `agents/azure-fsi-landingzone/config.yaml` to customize:
   - Naming conventions
   - Network address spaces
   - Compliance requirements
   - Policy settings

## Usage

### Interactive Mode

Run the agent interactively:

```bash
cd agents/azure-fsi-landingzone
python agent.py
```

### Example Conversations

**Check Prerequisites**
```
You: Check Azure prerequisites
Agent: [Validates Azure CLI, Bicep, authentication, and subscription access]
```

**View Compliance Requirements**
```
You: What are the FSI compliance requirements for GDPR?
Agent: [Details GDPR requirements and Azure controls]
```

**Generate Infrastructure Templates**
```
You: Generate a Bicep template for the hub VNet
Agent: [Creates and saves hub-vnet.bicep with FSI configurations]
```

**Validate Data Residency**
```
You: Check data residency compliance for EU
Agent: [Validates EU data residency policies and allowed regions]
```

**Export Deployment Plan**
```
You: Export deployment plan to markdown
Agent: [Generates comprehensive deployment plan document]
```

## Agent Capabilities

### Custom Tools (15 total)

#### Infrastructure & Prerequisites
1. **check_azure_prerequisites**
   - Validates Azure CLI installation
   - Checks Bicep availability
   - Verifies authentication status
   - Confirms subscription access

2. **validate_azure_auth**
   - Shows current subscription details
   - Lists available subscriptions
   - Displays user/service principal info

#### Compliance & Requirements
3. **get_fsi_compliance_requirements**
   - Details European regulations (GDPR, DORA, PSD2, MiFID II, EBA)
   - Lists Azure controls for each regulation
   - Shows policy initiatives to apply

4. **list_avm_modules**
   - Displays available Azure Verified Modules
   - Describes module features and use cases
   - Shows security baseline configurations

5. **generate_bicep_template**
   - Creates Bicep templates for components:
     - `hub-vnet`: Hub virtual network
     - `spoke-vnet`: Spoke virtual networks
     - `key-vault`: Azure Key Vault with HSM
     - `storage`: Storage accounts with compliance features
     - `policy-assignment`: Compliance policies

6. **validate_deployment**
   - Runs pre-deployment validation checks
   - Performs what-if analysis
   - Verifies naming conventions
   - Checks resource availability

7. **apply_compliance_policies**
   - Applies built-in policy initiatives
   - Configures custom FSI policies
   - Enforces data residency
   - Sets encryption requirements

8. **get_deployment_status**
   - Shows deployment statistics
   - Lists applied policies
   - Displays configuration summary

9. **generate_network_architecture**
   - Documents hub-spoke architecture
   - Lists security controls
   - Shows subnet design
   - Details data residency configuration

10. **check_data_residency**
    - Validates EU data residency settings
    - Lists allowed Azure regions
    - Shows compliance requirements

11. **export_deployment_plan**
    - Generates deployment documentation (Markdown/JSON)
    - Includes architecture diagrams
    - Lists deployment steps
    - Documents security controls

#### Identity & Access Management (NEW)
12. **generate_bastion_template**
    - Creates Azure Bastion Bicep template
    - Standard SKU with tunneling support
    - 365-day audit log retention
    - IP connect and native client support

13. **configure_entra_id**
    - Entra ID (Azure AD) configuration guidance
    - MFA enablement for all users
    - Sign-in and audit log export
    - Password policy for FSI requirements
    - B2B collaboration settings

14. **deploy_conditional_access**
    - Generates 5 Conditional Access policies:
      - Require MFA for all users
      - Block non-EU locations
      - Require compliant devices for admins
      - Block legacy authentication
      - App protection for mobile devices
    - Compliance mapping to PSD2, GDPR, DORA
    - Microsoft Graph API deployment scripts

15. **setup_pim_roles**
    - Privileged Identity Management configuration
    - Critical role identification (Global Admin, Security Admin, etc.)
    - PIM activation settings (MFA, approval, duration)
    - Break-glass account setup guidance
    - PowerShell configuration scripts
    - Compliance mapping to DORA, ISO 27001, NIS2

## Configuration

### Key Configuration Sections

#### Azure Settings (`azure`)
```yaml
azure:
  landing_zone:
    template_source: "microsoft"
    fsi_template_version: "latest"
    use_avm_modules: true
    default_region: "westeurope"
    naming_prefix: "fsi"
    environment: "prod"
```

#### Compliance (`azure.compliance`)
```yaml
compliance:
  regulations:
    - "GDPR"
    - "DORA"
    - "PSD2"
    - "MiFID_II"
    - "EBA_GL"

  policy_initiatives:
    - "Azure_Security_Benchmark"
    - "GDPR"
    - "PCI_DSS_v4"
```

#### Network Architecture (`azure.architecture`)
```yaml
architecture:
  topology: "hub-spoke"
  hub:
    vnet_address_space: "10.0.0.0/16"
    components:
      - "azure-firewall"
      - "vpn-gateway"
      - "bastion"
```

#### Security (`security`)
```yaml
security:
  secrets:
    use_key_vault: true
    rotate_secrets: true
  rbac:
    enforce_least_privilege: true
    require_pim: true
    require_mfa: true
```

## Deployment Workflow

### 1. Prerequisites
```bash
# Check prerequisites
python agent.py
> Check Azure prerequisites
```

### 2. Plan
```bash
# Generate deployment plan
> Export deployment plan to markdown

# Review the plan
cat fsi-deployment-plan_*.md
```

### 3. Validate
```bash
# Validate configuration
> Validate deployment for full

# Check compliance
> Check data residency compliance
> Get FSI compliance requirements
```

### 4. Generate Templates
```bash
# Generate Bicep templates
> Generate Bicep template for hub-vnet
> Generate Bicep template for spoke-vnet
> Generate Bicep template for key-vault
```

### 5. Deploy
```bash
# Deploy hub (manual step after generation)
az deployment sub create \
  --name fsi-hub-deployment \
  --location westeurope \
  --template-file templates/hub-vnet.bicep

# Deploy policies
> Apply compliance policies to subscription
```

### 6. Verify
```bash
# Check deployment status
> Get deployment status

# Verify compliance
az policy state list --filter "complianceState eq 'NonCompliant'"
```

## Generated Templates

### Hub Virtual Network
- Azure Firewall Premium
- VPN Gateway
- Azure Bastion
- DDoS Protection Standard
- Network Security Groups

### Spoke Virtual Network
- Application subnet
- Data subnet
- Private Link subnet
- VNet peering to hub
- Route tables

### Key Vault
- Premium tier (HSM-backed keys)
- RBAC authorization
- Soft delete and purge protection
- Private endpoints
- Audit logging (365-day retention)

### Storage Account
- Geo-redundant storage (GRS)
- Customer-managed keys
- Double encryption
- Immutable storage
- Versioning and change feed
- Private endpoints

### Policy Assignments
- GDPR compliance initiative
- EU data residency restrictions
- Encryption requirements
- Network security controls
- Monitoring and diagnostics

## Compliance Mapping

### GDPR
- **Data Residency**: EU regions only
- **Encryption**: CMK, double encryption
- **Privacy**: Private endpoints, no public access
- **Audit**: 365-day log retention
- **Breach Notification**: Azure Monitor alerts

### DORA
- **Resilience**: Geo-redundant storage, backup
- **Testing**: Multi-region deployment capability
- **Monitoring**: Log Analytics, Defender for Cloud
- **Third-party**: Managed service provider controls

### PSD2
- **Authentication**: Azure AD MFA
- **API Security**: API Management with OAuth 2.0
- **Monitoring**: Application Insights, Sentinel
- **Fraud Detection**: Azure Sentinel analytics

### MiFID II
- **Audit Trails**: Immutable audit logs
- **Retention**: 5-7 year retention policies
- **Reporting**: Log Analytics queries
- **Time Sync**: Azure time synchronization

### EBA Guidelines
- **Cloud Governance**: Azure Policy framework
- **Exit Strategy**: Data export tools
- **Risk Management**: Security Center
- **Oversight**: Management groups, RBAC

## Troubleshooting

### Azure CLI Not Found
```bash
# Install Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

### Bicep Not Installed
```bash
az bicep install
az bicep version
```

### Authentication Failed
```bash
# Re-authenticate
az login --tenant <tenant-id>

# Verify account
az account show
```

### Insufficient Permissions
```bash
# Check your role assignments
az role assignment list --assignee <your-upn> --all

# Required roles:
# - Owner or Contributor on subscription
# - Resource Policy Contributor for policies
```

### Region Not Available
```bash
# Check available regions
az account list-locations --query "[?metadata.regionCategory=='Recommended'].name" -o table

# Verify service availability in region
az provider show --namespace Microsoft.Network --query "resourceTypes[?resourceType=='virtualNetworks'].locations"
```

### Policy Conflicts
```bash
# List policy assignments
az policy assignment list

# Check compliance state
az policy state list --filter "complianceState eq 'NonCompliant'"

# Remediate non-compliant resources
az policy remediation create --name <remediation-name> --policy-assignment <assignment-id>
```

## Best Practices

### Security
- Always use private endpoints for PaaS services
- Enable Microsoft Defender for Cloud Standard tier
- Implement just-in-time (JIT) VM access
- Use Privileged Identity Management (PIM) for admin access
- Enable MFA for all users
- Rotate secrets every 90 days

### Networking
- Never expose resources to the internet
- Use Azure Firewall for egress traffic filtering
- Implement network segmentation (application/data/management)
- Enable DDoS Protection Standard on hub VNet
- Use Azure Bastion instead of public RDP/SSH

### Compliance
- Run what-if analysis before deployments
- Validate policy compliance regularly
- Maintain audit logs for required retention periods
- Document compliance controls
- Perform regular security assessments

### Operations
- Use Infrastructure as Code (Bicep/Terraform)
- Implement CI/CD pipelines for deployments
- Tag all resources for cost management
- Enable diagnostic settings on all resources
- Set up Azure Monitor alerts

## Reference Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    AZURE SUBSCRIPTION                        │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │              HUB VIRTUAL NETWORK                   │    │
│  │  ┌──────────────┐  ┌──────────────┐              │    │
│  │  │    Azure     │  │      VPN     │              │    │
│  │  │   Firewall   │  │    Gateway   │              │    │
│  │  └──────────────┘  └──────────────┘              │    │
│  │  ┌──────────────┐  ┌──────────────┐              │    │
│  │  │    Azure     │  │     DDoS     │              │    │
│  │  │   Bastion    │  │  Protection  │              │    │
│  │  └──────────────┘  └──────────────┘              │    │
│  └────────────────────────────────────────────────────┘    │
│           │                      │                          │
│           │                      │                          │
│  ┌────────▼──────────┐  ┌───────▼─────────┐               │
│  │  SPOKE VNet 1     │  │  SPOKE VNet 2   │               │
│  │  (Workload A)     │  │  (Workload B)   │               │
│  │                   │  │                 │               │
│  │  ┌─────────────┐  │  │  ┌───────────┐  │               │
│  │  │ Application │  │  │  │Application│  │               │
│  │  └─────────────┘  │  │  └───────────┘  │               │
│  │  ┌─────────────┐  │  │  ┌───────────┐  │               │
│  │  │    Data     │  │  │  │   Data    │  │               │
│  │  └─────────────┘  │  │  └───────────┘  │               │
│  │  ┌─────────────┐  │  │  ┌───────────┐  │               │
│  │  │Private Link │  │  │  │ Private   │  │               │
│  │  └─────────────┘  │  │  │   Link    │  │               │
│  └───────────────────┘  └───────────────┘                 │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │         MANAGEMENT & SECURITY SERVICES             │    │
│  │                                                      │    │
│  │  • Log Analytics Workspace                          │    │
│  │  • Microsoft Defender for Cloud                     │    │
│  │  • Azure Key Vault                                  │    │
│  │  • Recovery Services Vault                          │    │
│  │  • Azure Policy                                     │    │
│  │  • Azure Monitor                                    │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## Microsoft FSI Landing Zone Alignment

✅ **This agent is 95% aligned with Microsoft's official FSI Landing Zone architecture.**

See [ALIGNMENT.md](ALIGNMENT.md) for detailed analysis including:
- ✅ All core policy controls (Sovereignty, Transparency, Resilience, Service Design)
- ✅ Compliance with PCI-DSS 4.0, NIST SP 800-53 Rev. 5
- ✅ European regulations (GDPR, DORA, PSD2, MiFID II, EBA)
- ⚠️ Minor gaps documented with action plan

**Key Landing Zone Types** (from Microsoft FSI LZ):
- **Corp**: Non-internet facing, non-confidential workloads
- **Online**: Internet facing, non-confidential workloads
- **Confidential Corp**: Non-internet facing with confidential computing
- **Confidential Online**: Internet facing with confidential computing

Configure these in [config.yaml](config.yaml) under `architecture.landing_zone_types`.

## Additional Resources

### Microsoft FSI Documentation
- [FSI Landing Zone Overview](https://learn.microsoft.com/en-us/industry/financial-services/fsi-lz) - Official FSI guidance
- [FSI Architecture](https://learn.microsoft.com/en-us/industry/financial-services/fsi-lz-arch) - Architecture details
- [FSI Policy Controls](https://learn.microsoft.com/en-us/industry/financial-services/fsi-policy-controls) - Policy frameworks
- [FSI Governance](https://learn.microsoft.com/en-us/industry/financial-services/infra-governance-fsi) - Governance requirements

### Azure Documentation
- [Azure Verified Modules](https://azure.github.io/Azure-Verified-Modules/) - Official AVM docs
- [Azure Landing Zones](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/)
- [Bicep Landing Zone Design](https://learn.microsoft.com/en-us/azure/architecture/landing-zones/bicep/landing-zone-bicep)
- [Azure Security Benchmark](https://learn.microsoft.com/security/benchmark/azure/)

### Compliance
- [GDPR Compliance](https://learn.microsoft.com/compliance/regulatory/gdpr)
- [Azure Compliance Offerings](https://learn.microsoft.com/azure/compliance/)
- [Microsoft Trust Center](https://www.microsoft.com/trust-center)

### Tools
- [Bicep Documentation](https://learn.microsoft.com/azure/azure-resource-manager/bicep/)
- [Azure Policy](https://learn.microsoft.com/azure/governance/policy/)
- [Azure CLI Reference](https://learn.microsoft.com/cli/azure/)

## Support

For issues or questions:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review Azure documentation
3. Open an issue in the repository
4. Contact Azure support for subscription-specific issues

## License

[Add license information]

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

**⚠️ Important**: This agent generates infrastructure templates and provides guidance. Always review generated code and configurations before deploying to production. Ensure compliance with your organization's security and governance policies.
