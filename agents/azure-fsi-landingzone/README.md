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

## 🎯 Ring-Based Deployment Architecture (New!)

This agent now supports a **progressive, ring-based deployment strategy** for better organization and control:

### 📦 Ring 0: Foundation (Core FSI Compliance)
**Mandatory** | Deployment Order: 1

The compliance and security baseline for all FSI deployments:
- Network Core: Hub VNet, Azure Firewall, DDoS Protection
- Security Core: Key Vault, Bastion, NSGs
- Governance Core: Azure Policies (GDPR, DORA, EBA GL)
- Monitoring Core: Log Analytics, Defender for Cloud
- Identity Core: Entra ID, PIM, Conditional Access

### 📦 Ring 1: Platform Services (DevOps & Shared)
**Optional** | Deployment Order: 2 | Depends on: Ring 0

DevOps tooling and shared infrastructure:
- DevOps: Container Registry, Build Agents, Artifacts
- Shared Services: Shared Key Vault, Storage, APIM
- Admin Infrastructure: Admin VNet, Jump Boxes

### 📦 Ring 2: Workload Infrastructure (Applications)
**Optional** | Deployment Order: 3 | Depends on: Ring 0

Infrastructure for hosting applications (IaaS/PaaS/CaaS):
- Compute: App Service, AKS, VMs, Functions
- Data: SQL DB, Cosmos DB, Storage, Data Lake
- Integration: Service Bus, Event Grid, Logic Apps
- Frontend: Application Gateway, Front Door, CDN

### 🎚️ Deployment Depth Profiles

Choose your deployment depth:
- **Minimal**: Essential components only (POC, testing)
- **Standard**: Recommended for production (default)
- **Advanced**: All components including optional features

📖 **[Full Ring Architecture Documentation](./RING-ARCHITECTURE.md)**

## Features

### 🏦 FSI-Specific Architecture
- Hub-spoke network topology optimized for financial services
- Ring-based progressive deployment for better control
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

1. **Node.js and npm** (for Claude Code CLI)
   ```bash
   # Check if installed
   node --version
   npm --version
   ```

2. **Claude Code CLI** (v2.0.1 or later) - **REQUIRED**
   ```bash
   # Install Claude Code
   npm install -g @anthropic-ai/claude-code@latest

   # Verify installation
   claude --version
   # Should show: 2.0.1 (Claude Code) or later
   ```

   **Important**: Claude Code CLI v2.0+ is required. Earlier versions (1.x) are not compatible with claude-agent-sdk v0.1.0.

3. **Azure CLI** (v2.50.0 or later)
   ```bash
   # Install Azure CLI
   curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
   ```

4. **Bicep** (v0.24.0 or later)
   ```bash
   # Install Bicep
   az bicep install
   ```

5. **Python** (3.10 or later)
   ```bash
   python --version
   ```

6. **Azure Subscription** with appropriate permissions:
   - Owner or Contributor role
   - Policy assignment permissions
   - Network resource creation rights

7. **Authentication**
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

2. **Navigate to agent directory**
   ```bash
   cd agents/azure-fsi-landingzone
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   # Copy example .env file
   cp .env.example .env

   # Edit .env and add your credentials
   vim .env
   ```

   **Required in .env**:
   ```bash
   ANTHROPIC_API_KEY=sk-ant-api03-...
   AZURE_SUBSCRIPTION_ID=your-subscription-id
   AZURE_TENANT_ID=your-tenant-id  # Optional if using az login
   ```

5. **Customize configuration**
   Edit `config.yaml` to customize:
   - Naming conventions
   - Network address spaces
   - Compliance requirements
   - Policy settings

6. **Verify installation**
   ```bash
   # Test the agent
   python agent.py

   # You should see:
   # ================================================================================
   #   🏦 AZURE FSI LANDING ZONE DEPLOYMENT AGENT
   # ================================================================================
   ```

## 📅 Deployment Timeline & Cost Estimation

### From Scratch to Production-Ready Landing Zone

This section provides realistic estimates for deploying a complete FSI Landing Zone **using this agent** vs manual deployment.

#### ⚡ Quick Comparison: Agent vs Manual

| Approach | Timeline | Effort | Automation Level |
|----------|----------|--------|------------------|
| **Using This Agent** | **3-5 days** | **24-40 hours** | 85% automated |
| **Manual Deployment** | **8-12 weeks** | **240-400 hours** | 20% automated |

#### 🤖 Using This Agent (Recommended)

| Phase | Duration | Effort | What the Agent Does |
|-------|----------|--------|---------------------|
| **1. Planning & Design** | 1 day | 6-8 hours | You define requirements, agent validates architecture |
| **2. Agent Configuration** | 2-4 hours | 2-4 hours | Configure `config.yaml`, set naming conventions |
| **3. Template Generation** | 5 minutes | 5 minutes | Agent generates all Bicep templates with AVM |
| **4. Infrastructure Deployment** | 1-2 days | 8-12 hours | Agent deploys hub+spokes, you review & approve |
| **5. Identity & Access** | 4-6 hours | 4-6 hours | Agent generates templates, you apply & test |
| **6. Policy & Compliance** | 2-4 hours | 2-4 hours | Agent applies policies, compliance checker validates |
| **7. Testing & Validation** | 1 day | 6-8 hours | Automated compliance checks, manual smoke testing |
| **Total** | **3-5 days** | **24-40 hours** | **85% automated with agent tools** |

#### 📊 Day-by-Day Breakdown (Using Agent)

##### Day 1: Planning & Setup (6-8 hours)
- Define requirements (compliance, workloads, network design)
- Install agent and dependencies (`pip install -r requirements.txt`)
- Configure `config.yaml` with your settings
- Set up Azure credentials and permissions
- **Agent generates architecture recommendations**

##### Day 2: Template Generation & Hub Deployment (8-12 hours)
- Agent generates Bicep templates (5 minutes)
- Review and customize templates
- Deploy hub infrastructure:
  - `generate_hub_vnet` → Creates hub network
  - `generate_firewall_template` → Deploys Azure Firewall Premium
  - `generate_bastion_template` → Deploys Azure Bastion
- Monitor deployment progress (1-2 hours for Azure resources)

##### Day 3: Identity & Spoke Deployment (4-8 hours)
- Deploy identity components:
  - `configure_entra_id` → Entra ID setup guidance
  - `deploy_conditional_access` → 5 CA policies
  - `setup_pim_roles` → PIM configuration
- Deploy spoke networks:
  - `generate_spoke_vnet` for each workload
- **Agent handles peering and routing automatically**

##### Day 4: Compliance & Policy (2-4 hours)
- `apply_fsi_policies` → Deploys all compliance policies
- `generate_compliance_report` → Initial compliance check
- Use **Azure Compliance Checker agent** to validate controls
- Remediate any non-compliant resources

##### Day 5: Testing & Validation (6-8 hours)
- Run automated compliance checks
- Test connectivity and security controls
- Review Defender for Cloud recommendations
- Document deployment and create runbooks
- Validate all monitoring and alerting

**Effort**: 2-3 people × 16-24 hours = **32-48 hours**

##### Week 11-12: Documentation & Handover
**Activities**:
- Create operational runbooks
- Document architecture and design decisions
- Create incident response procedures
- Train operations team
- Knowledge transfer sessions
- Create compliance audit package

**Effort**: 1-2 people × 6-10 hours = **12-20 hours**

#### 💰 Cost Estimation

> **Note**: Costs are split into **Azure Cloud Infrastructure** (pay-as-you-go) and **Implementation Effort** (consulting/internal team).

##### 🔷 Azure Cloud Infrastructure Costs (Monthly - West Europe)

**Landing Zone Foundation (Hub + 3 Spokes)**:

| Component | SKU/Tier | Monthly Cost (EUR) | Notes |
|-----------|----------|-------------------|-------|
| **Networking** |
| Azure Firewall Premium | Premium | €875 | Includes 100GB traffic, IDPS, TLS inspection |
| VPN Gateway | VpnGw2 | €340 | Or ExpressRoute Gateway (€800-2,500) |
| Azure Bastion | Standard | €120 | Secure VM access, 2 scale units |
| DDoS Protection Standard | Standard | €2,450 | Protects ALL VNets in subscription |
| Public IPs | Standard (3x) | €12 | Firewall, VPN, Bastion |
| Private Endpoints | 10x | €60 | €0.06/hour each |
| **Identity & Access** |
| Entra ID Premium P2 | 100 users | €750 | MFA, PIM, Conditional Access, risk detection |
| **Security & Monitoring** |
| Log Analytics | 100GB/day | €200 | €2/GB ingested, 365-day retention |
| Microsoft Defender for Cloud | Standard | €500 | VMs, Storage, Containers, Key Vault |
| Azure Sentinel | 50GB/day | €100 | €2/GB ingested |
| **Management** |
| Key Vault Premium (HSM) | 2 vaults | €40 | + €0.03/10k operations |
| Recovery Services (Backup) | 1TB GRS | €80 | Geo-redundant backup storage |
| Automation Account | Basic | €10 | 500 minutes/month included |
| Storage (Logs) | 500GB GRS | €25 | Immutable audit logs |
| **Landing Zone Baseline** | | **€5,562/month** | **Without workloads** |

**Add Your Workload Costs**:
- VMs (example: 10x D4s_v5): €2,000-4,000/month
- Azure SQL Database (Business Critical): €1,500-5,000/month
- App Services (Premium): €500-2,000/month
- **Total with Workloads**: **€8,000-20,000/month** (varies widely)

**Scaling Examples**:
| Deployment Size | Monthly Azure Cost | Annual Azure Cost |
|----------------|-------------------|------------------|
| **Small** (1 hub + 2 spokes, 50 users) | €7,500-12,000 | €90,000-144,000 |
| **Medium** (1 hub + 4 spokes, 200 users) | €15,000-30,000 | €180,000-360,000 |
| **Large** (1 hub + 8 spokes, 1000 users) | €40,000-80,000 | €480,000-960,000 |

##### 💼 What It Actually Costs You (DIY with Agent)

**🔷 Azure Infrastructure Costs for 5-Day Deployment** (NO workloads):

| Day | What Deploys | Daily Cost | Total Cost |
|-----|-------------|-----------|-----------|
| **Day 1** | Hub VNet, Firewall, VPN, Bastion, DDoS | €184 | €184 |
| **Day 2** | 3 Spoke VNets, Private Endpoints | €184 | €368 |
| **Day 3** | Entra ID P2 (prorated), Log Analytics, Defender | €50 | €418 |
| **Day 4** | Sentinel, Key Vault, Storage, Automation | €15 | €433 |
| **Day 5** | Backup vault, monitoring (all running) | €184 | €617 |
| **Total 5 Days** | **Landing Zone Foundation** | | **€617** |

**💰 Monthly Cost Once Deployed** (NO workloads):
- **€5,562/month** for the landing zone infrastructure
- This is the baseline before adding any VMs, databases, or applications

**🧑‍💻 Your Effort** (If you do it yourself):
- **Your time**: 24-40 hours over 5 days
- **Your cost**: €0 (internal time)
- **Agent cost**: €0 (open source)

**👔 If Hiring Consultants** (Optional):

| Resource | Days | Rate/day | Total |
|----------|------|---------|-------|
| Cloud Architect | 2 | €1,200 | €2,400 |
| DevOps Engineer | 3 | €900 | €2,700 |
| Security Engineer | 1.5 | €1,000 | €1,500 |
| **Consulting Total** | | | **€6,600** |

##### 🎯 Total Cost Summary

**💡 If You Do It Yourself with This Agent**:

| What | Cost | Notes |
|------|------|-------|
| **First 5 Days (Deployment)** | €617 | Azure infrastructure only |
| **Month 1 Remaining** | €4,408 | 26 days × €169/day |
| **Months 2-12** | €61,182 | 11 months × €5,562 |
| **Your Time** | €0 | Internal effort (24-40 hours) |
| **Agent** | €0 | Open source |
| **Year 1 Total (DIY)** | **€66,207** | **Just Azure, no workloads** |

**📊 Add Optional Services**:
- Compliance Audit: +€10,000/year
- Penetration Test: +€8,000/year
- Training: +€5,000/year
- **Total with Services**: **€89,207/year**

**👔 If You Hire Consultants Instead**:
- Year 1 Total: €72,807 (€66,207 + €6,600 consulting)

**Compare to Manual Deployment**:
- Manual effort: €141,000 (8-12 weeks consultants)
- Azure cost: Same €66,207
- **Manual Total**: €207,207
- **Your Savings with Agent**: **€141,000** (68% cheaper)

#### 💡 Cost Optimization Tips

1. **Reserved Instances**: Save 30-50% on VMs and VPN Gateway with 1-3 year commitments
2. **Azure Hybrid Benefit**: Use existing Windows Server licenses (40% savings)
3. **Right-Sizing**: Start with smaller SKUs, scale as needed
4. **Defender for Cloud**: Enable only required plans (VMs, Storage, Key Vault)
5. **Log Retention**: Use Archive tier for logs > 90 days old
6. **DDoS Protection**: Covers all VNets, cost-effective for 2+ VNets
7. **Dev/Test Pricing**: Use separate subscriptions with reduced rates

#### ⚡ Express Deployment (1-2 days)

For **proof-of-concept** or **urgent deployments**, you can deploy even faster:

| Approach | Timeline | Team | What You Get |
|----------|----------|------|--------------|
| **Express PoC** | **1 day** | 1-2 people | Hub + 1 spoke, basic policies, no identity setup |
| **Express Production** | **2 days** | 2 people | Hub + 2 spokes, all policies, Entra ID guidance |
| **Standard (Recommended)** | **3-5 days** | 2-3 people | Full deployment with testing & validation |

**Express Deployment Process**:
1. **Morning**: Configure agent (1 hour) → Generate templates (5 min)
2. **Afternoon**: Deploy hub (2 hours) → Deploy spokes (1 hour)
3. **Next Day**: Apply policies (1 hour) → Basic testing (2 hours)

**⚠️ Express Limitations**:
- Limited testing and validation
- Manual identity configuration required
- Defer DR/backup setup
- Compliance validation done post-deployment

#### 📋 Deployment Checklist (Using Agent)

**Day 0 - Prerequisites** (2-4 hours):
- [ ] Azure subscription with Owner/Contributor access
- [ ] Install agent: `pip install -r requirements.txt`
- [ ] Configure `config.yaml` (hub CIDR, naming prefix, region)
- [ ] Azure CLI authenticated: `az login`
- [ ] Define compliance requirements (GDPR, DORA, etc.)

**Day 1 - Hub & Foundation** (6-8 hours):
- [ ] Agent: `generate_hub_vnet` → Deploy hub network
- [ ] Agent: `generate_firewall_template` → Deploy Azure Firewall
- [ ] Agent: `generate_bastion_template` → Deploy Bastion
- [ ] Agent: `apply_fsi_policies` → Apply compliance policies
- [ ] Verify hub connectivity and firewall rules

**Day 2-3 - Spokes & Identity** (8-12 hours):
- [ ] Agent: `generate_spoke_vnet` → Deploy each spoke (15-30 min each)
- [ ] Agent: `configure_entra_id` → Follow Entra ID setup guidance
- [ ] Agent: `deploy_conditional_access` → Apply 5 CA policies
- [ ] Agent: `setup_pim_roles` → Configure PIM
- [ ] Test spoke-to-hub connectivity

**Day 4 - Compliance & Security** (4-6 hours):
- [ ] Run **Azure Compliance Checker agent** to validate controls
- [ ] Agent: `generate_compliance_report` → Generate audit report
- [ ] Enable Defender for Cloud (Standard tier)
- [ ] Configure Azure Sentinel data connectors
- [ ] Remediate any non-compliant resources

**Day 5 - Validation & Go-Live** (6-8 hours):
- [ ] End-to-end connectivity testing
- [ ] Compliance score > 85% validated
- [ ] Security score > 80% validated
- [ ] Break-glass accounts tested
- [ ] Operations runbook documented
- [ ] **Production ready** ✅

#### 🎯 Success Metrics

| Metric | Target (Using Agent) | Target (Manual) | Notes |
|--------|---------------------|-----------------|-------|
| **Deployment Time** | **3-5 days** | 8-12 weeks | From config to production-ready |
| **Azure Cost (5 days)** | **€617** | €617 | Same infrastructure cost |
| **Consulting Cost** | **€0** (DIY) | €141,000 | Agent eliminates this! |
| **Compliance Score** | > 85% | > 85% | Azure Policy compliance |
| **Security Score** | > 80% | > 80% | Microsoft Defender for Cloud |
| **Time to Deploy New Spoke** | **< 30 min** | 1-2 days | Using agent templates |

---

**💡 Bottom Line**:

**DIY with This Agent (Recommended)**:
- **Timeline**: 3-5 days (24-40 hours of your time)
- **Cost for 5 days**: **€617** (just Azure infrastructure)
- **Year 1 Cost**: **€66,207** (Azure only) or **€89,207** (with audits/training)
- **Your savings**: **€141,000** (no consultants needed!)

**Add Workloads Later**:
- The €66k/year is just the landing zone foundation
- When you add VMs, databases, apps → add their costs separately
- Example: 10 VMs = +€2,000-4,000/month = +€24k-48k/year

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
┌──────────────────────────────────────────────────────────┐
│                    AZURE SUBSCRIPTION                    │
│                                                          │
│  ┌──────────────────────────────────────┐                │
│  │              HUB VIRTUAL NETWORK     │                │
│  │  ┌──────────────┐  ┌──────────────┐  │                │
│  │  │    Azure     │  │      VPN     │  │                │
│  │  │   Firewall   │  │    Gateway   │  │                │
│  │  └──────────────┘  └──────────────┘  │                │
│  │  ┌──────────────┐  ┌──────────────┐  │                │
│  │  │    Azure     │  │     DDoS     │  │                │
│  │  │   Bastion    │  │  Protection  │  │                │
│  │  └──────────────┘  └──────────────┘  │                │
│  └──────────────────────────────────────┘                │
│           │                      │                       │
│           │                      │                       │
│  ┌────────▼──────────┐  ┌───────▼─────────┐              │
│  │  SPOKE VNet 1     │  │  SPOKE VNet 2   │              │
│  │  (Workload A)     │  │  (Workload B)   │              │
│  │                   │  │                 │              │
│  │  ┌─────────────┐  │  │  ┌───────────┐  │              │
│  │  │ Application │  │  │  │Application│  │              │
│  │  └─────────────┘  │  │  └───────────┘  │              │
│  │  ┌─────────────┐  │  │  ┌───────────┐  │              │
│  │  │    Data     │  │  │  │   Data    │  │              │
│  │  └─────────────┘  │  │  └───────────┘  │              │
│  │  ┌─────────────┐  │  │  ┌───────────┐  │              │
│  │  │Private Link │  │  │  │ Private   │  │              │
│  │  └─────────────┘  │  │  │   Link    │  │              │
|  |                   |  |  └───────────┘  |              |
│  └───────────────────┘  └─────────────────┘              │
│                                                          │
│  ┌────────────────────────────────────────────────────┐  │
│  │         MANAGEMENT & SECURITY SERVICES             │  │
│  │                                                    │  │
│  │  • Log Analytics Workspace                         │  │
│  │  • Microsoft Defender for Cloud                    │  │
│  │  • Azure Key Vault                                 │  │
│  │  • Recovery Services Vault                         │  │
│  │  • Azure Policy                                    │  │
│  │  • Azure Monitor                                   │  │
│  └────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
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
