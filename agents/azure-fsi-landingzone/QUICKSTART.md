# Quick Start Guide - Azure FSI Landing Zone Agent

Get started with deploying an Azure FSI Landing Zone in 10 minutes.

## Prerequisites (5 minutes)

### 1. Install Azure CLI
```bash
# Linux/WSL
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# macOS
brew install azure-cli

# Verify installation
az --version
```

### 2. Install Bicep
```bash
az bicep install
az bicep version
```

### 3. Authenticate to Azure
```bash
# Login
az login

# Set your subscription
az account set --subscription "<your-subscription-id>"

# Verify
az account show
```

### 4. Install Python Dependencies
```bash
cd agents/azure-fsi-landingzone
pip install -r requirements.txt
```

### 5. Configure Environment
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and set:
# - AZURE_SUBSCRIPTION_ID
# - AZURE_TENANT_ID
# - ANTHROPIC_API_KEY

# Linux/macOS
export ANTHROPIC_API_KEY="your-key-here"
```

## Quick Deployment (5 minutes)

### 1. Start the Agent
```bash
python agent.py
```

### 2. Basic Conversation Flow

**Step 1: Check Prerequisites**
```
You: Check Azure prerequisites
```
The agent validates Azure CLI, Bicep, and authentication.

**Step 2: Understand Compliance**
```
You: What FSI compliance requirements do I need to meet?
```
Learn about GDPR, DORA, PSD2, MiFID II, and EBA Guidelines.

**Step 3: Generate Hub Network**
```
You: Generate Bicep template for hub-vnet
```
Creates a hub virtual network template with Azure Firewall.

**Step 4: Generate Spoke Network**
```
You: Generate Bicep template for spoke-vnet
```
Creates a spoke network template for workloads.

**Step 5: Create Key Vault**
```
You: Generate Bicep template for key-vault
```
Creates a secure Key Vault with HSM support.

**Step 6: Export Deployment Plan**
```
You: Export deployment plan to markdown
```
Generates a comprehensive deployment document.

## Deploy to Azure

After generating templates, deploy them:

### Deploy Hub Infrastructure
```bash
# Create resource group
az group create \
  --name fsi-hub-rg \
  --location westeurope

# Deploy hub network
az deployment group create \
  --name fsi-hub-deployment \
  --resource-group fsi-hub-rg \
  --template-file templates/hub-vnet.bicep
```

### Deploy Spoke Infrastructure
```bash
# Create resource group
az group create \
  --name fsi-spoke-rg \
  --location westeurope

# Deploy spoke network
az deployment group create \
  --name fsi-spoke-deployment \
  --resource-group fsi-spoke-rg \
  --template-file templates/spoke-vnet.bicep \
  --parameters spokeName=workload1 hubVNetId=<hub-vnet-id>
```

### Apply Compliance Policies
```bash
# Using the agent
You: Apply compliance policies to subscription
```

Then manually apply using Azure CLI:
```bash
az policy assignment create \
  --name fsi-gdpr-compliance \
  --policy-set-definition "<policy-set-id>" \
  --scope "/subscriptions/<subscription-id>"
```

## Common Agent Commands

### Infrastructure Generation
- `Generate Bicep template for hub-vnet` - Hub network
- `Generate Bicep template for spoke-vnet` - Spoke network
- `Generate Bicep template for key-vault` - Secure Key Vault
- `Generate Bicep template for storage` - Compliant storage
- `Generate Bicep template for policy-assignment` - Compliance policies

### Validation & Planning
- `Validate deployment for full` - Pre-deployment validation
- `Check data residency compliance` - EU data residency check
- `Get deployment status` - Current deployment state
- `Export deployment plan to markdown` - Full deployment plan

### Compliance & Security
- `Get FSI compliance requirements` - Regulatory details
- `List available AVM modules` - Azure Verified Modules
- `Check data residency` - EU compliance validation
- `Apply compliance policies to subscription` - Policy guidance

### Azure Operations
- `Check Azure prerequisites` - Validate setup
- `Validate Azure authentication` - Check credentials
- `Generate network architecture` - Architecture docs

## Example Session

```bash
$ python agent.py

================================================================================
  🏦 AZURE FSI LANDING ZONE DEPLOYMENT AGENT
================================================================================

🎯 Capabilities:
   • Deploy Microsoft FSI Landing Zone templates
   • Use Azure Verified Modules (AVM)
   • Apply European compliance policies (GDPR, DORA, PSD2, MiFID II)
   • Generate Bicep/Terraform templates
   • Validate deployments and security posture

💬 Try asking me to:
   - Check Azure prerequisites
   - List FSI compliance requirements
   - Generate a hub VNet template
   - Check data residency compliance
   - Export a deployment plan
   - Validate my Azure authentication

================================================================
  AZURE-FSI-LANDINGZONE - Interactive Mode
================================================================

Hello! I'm azure-fsi-landingzone. Type 'quit' or 'exit' to end our conversation.

💬 You: Check Azure prerequisites

🤖 Claude: I'll check your Azure prerequisites.

🔧 Using tool: check_azure_prerequisites

🤖 Claude: 🔍 Azure Prerequisites Check:

✅ Azure CLI: Installed
   Version: 2.54.0

✅ Bicep: Installed
   Version: 0.24.24

✅ Authentication: Authenticated

✅ Subscription Access: Active

All prerequisites are met! You're ready to deploy.

💬 You: Generate Bicep template for hub-vnet

🔧 Using tool: generate_bicep_template
   Input: {'component': 'hub-vnet'}

🤖 Claude: ✅ Generated Bicep template for: hub-vnet

📄 Saved to: /path/to/templates/hub-vnet.bicep

Template Preview:
```bicep
// Hub Virtual Network for FSI Landing Zone
// Generated by Azure FSI Landing Zone Agent

param location string = 'westeurope'
param environment string = 'prod'
...
```

💬 You: Export deployment plan to markdown

🔧 Using tool: export_deployment_plan
   Input: {'format': 'markdown'}

🤖 Claude: ✅ Deployment plan exported:

📄 File: fsi-deployment-plan_20250102_143022.md
📊 Format: MARKDOWN
📅 Generated: 2025-10-02 14:30:22

The plan includes:
• Architecture overview
• Compliance requirements
• Network topology
• Security controls
• Step-by-step deployment guide

💬 You: quit

👋 azure-fsi-landingzone: Goodbye! Thanks for chatting.
```

## Next Steps

1. **Review Generated Templates**
   - Check `templates/` directory
   - Customize parameters as needed
   - Validate Bicep syntax: `az bicep build -f template.bicep`

2. **Run What-If Analysis**
   ```bash
   az deployment group what-if \
     --resource-group <rg-name> \
     --template-file templates/hub-vnet.bicep
   ```

3. **Deploy Infrastructure**
   - Start with hub network
   - Deploy management services
   - Add spoke networks for workloads

4. **Apply Policies**
   - Use agent to identify required policies
   - Apply via Azure Policy
   - Monitor compliance in Azure Portal

5. **Validate Compliance**
   - Check Azure Security Center
   - Review compliance dashboard
   - Verify data residency settings

## Troubleshooting

### "Azure CLI not found"
```bash
# Install Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

### "Not authenticated"
```bash
az login
az account set --subscription "<subscription-id>"
```

### "Bicep not installed"
```bash
az bicep install
```

### "Import error: claude_agent_sdk"
```bash
pip install claude-agent-sdk
```

### "Permission denied"
Ensure you have:
- Contributor or Owner role on subscription
- Resource Policy Contributor for policy assignments

## Tips

- **Start Small**: Deploy hub first, then add spokes
- **Use What-If**: Always run what-if before actual deployment
- **Review Policies**: Understand policy impact before applying
- **Check Costs**: Use Azure Pricing Calculator for estimates
- **Test in Dev**: Deploy to dev subscription first
- **Document Changes**: Keep track of customizations
- **Use Tags**: Tag all resources for management

## Support

- Agent Documentation: [README.md](README.md)
- Azure Documentation: https://docs.microsoft.com/azure
- FSI Landing Zones: https://aka.ms/fsi-landing-zones
- Issues: Open an issue in the repository

---

**Ready to deploy?** Start the agent with `python agent.py` and begin your conversation!
