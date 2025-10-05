# Free Tier Deployment Guide for Azure FSI Landing Zone

## Overview

The Azure FSI Landing Zone agents now support automatic adaptation to Azure Free Tier subscriptions, enabling cost-effective learning and proof-of-concept deployments while maintaining FSI compliance principles.

## Subscription Tier Detection

### Automatic Detection

The system automatically detects your Azure subscription type using the `detect-free-tier.sh` script:

```bash
cd agents/azure-fsi-landingzone
./scripts/detect-free-tier.sh
```

**Detected Offer Types:**
- `MS-AZR-0044P` → Azure Free Trial (30 days)
- `MS-AZR-0170P` → Azure for Students
- `MS-AZR-0144P` → Azure for Students Starter
- `MS-AZR-0148P` → Pay-As-You-Go (Standard)
- `MS-AZR-0017P` → Enterprise Agreement (Standard)

### Manual Override

You can manually specify the tier when deploying:

```bash
az deployment sub create \
  --location westeurope \
  --template-file bicep/main.bicep \
  --parameters isFreeTier=true environment=dev
```

## Architecture Adaptation Matrix

### Environments × Rings × Free Tier

| Environment | Free Tier Strategy | Standard Strategy | TTL (Auto-Cleanup) |
|-------------|-------------------|-------------------|-------------------|
| **dev** | Shared Hub + 1 Spoke | Shared Hub + 1-2 Spokes | 7 days |
| **test** | Minimal (Hub only) | Shared Hub + 1 Spoke | 3 days |
| **staging** | N/A (too expensive) | Shared Hub + 2 Spokes | 14 days |
| **prod** | ❌ Not recommended | Full Rings (0-3) | ∞ (permanent) |
| **sandbox** | Minimal (Hub only) | Shared Hub + 1 Spoke | 30 days |

### Deployment Strategies

#### 1. **Full Rings** (Standard only)
- Deploys all rings (Ring 0 + Ring 1/2/3) per environment
- Each environment gets complete architecture
- ❌ **Not compatible with Free Tier** (too expensive)
- Best for: Production, multi-workload environments

#### 2. **Shared Hub** ✅ Recommended for Free Tier
- Single Ring 0 (Hub) shared across environments
- Separate spokes (Ring 1+) per environment
- Cost-optimized while maintaining isolation
- Best for: Dev/test environments, cost optimization

#### 3. **Minimal** ✅ Ideal for Free Tier POC
- Only Ring 0 (Hub) + 1 spoke
- Simplest architecture
- Perfect for learning and proof-of-concept
- Best for: Learning, proof-of-concept, demos

## Free Tier Restrictions & Adaptations

### ❌ Disabled Services (Too Expensive)

The following services are **automatically disabled** in Free Tier mode:

| Service | Monthly Cost | Free Tier Alternative |
|---------|-------------|----------------------|
| Azure Firewall | ~€900/month | Network Security Groups (NSGs) |
| Azure Bastion | ~€120/month | Just-in-time VM access |
| Standard Load Balancer | ~€20/month | Basic Load Balancer (if needed) |
| Application Gateway | ~€200/month | None (use NSGs) |
| Premium SQL Database | ~€400/month | Basic SQL (€4/month) |
| Premium Key Vault (HSM) | ~€500/month | Standard Key Vault |

### ✅ Enabled Free Tier Services

| Service | SKU | Monthly Cost | Notes |
|---------|-----|-------------|-------|
| Virtual Machines | B1s | ~€8/month | 750h free first year |
| SQL Database | Basic | ~€4/month | 250GB storage |
| App Service | F1 (Free) | €0 | Limited features |
| Storage Account | Standard_LRS | ~€1/month | Locally redundant |
| Key Vault | Standard | ~€0.02/month | Per operation pricing |
| VNet / NSG | N/A | €0 | Always free |

### 🛡️ Cost Guardrails (Automatic)

When Free Tier is detected, the following guardrails are **automatically applied**:

1. **Budget Alerts**
   - €5 threshold (50% warning)
   - €10 threshold (final warning)
   - Alerts sent to configured emails

2. **Resource Restrictions**
   - Azure Policy blocks expensive SKUs
   - Deny Premium SQL, Firewall, Load Balancer
   - Prevent accidental costly deployments

3. **Auto-Cleanup**
   - Non-prod resources expire after TTL
   - Tags added: `expiration=YYYY-MM-DD`
   - Daily cleanup runbook (optional)

4. **Diagnostics Disabled**
   - Log Analytics disabled by default
   - Saves ~€2-5/month in ingestion costs
   - Can be re-enabled manually if needed

## Deployment Examples

### Example 1: Dev Environment (Free Tier)

```bash
# 1. Detect subscription tier
cd agents/azure-fsi-landingzone
./scripts/detect-free-tier.sh

# 2. Deploy with Free Tier settings
az deployment sub create \
  --location westeurope \
  --template-file bicep/main.bicep \
  --parameters \
    environment=dev \
    isFreeTier=true \
    deploymentStrategy=shared-hub \
    namingPrefix=fsi-demo \
    budgetAlertEmails='["you@example.com"]'
```

**Expected Output:**
- 1 Hub VNet (Ring 0)
- 1 Spoke VNet (Ring 1)
- Network Security Groups
- Budget with alerts
- Expiration tags (7 days)
- Total cost: ~€10-15/month

### Example 2: Production Environment (Standard)

```bash
az deployment sub create \
  --location westeurope \
  --template-file bicep/main.bicep \
  --parameters \
    environment=prod \
    isFreeTier=false \
    deploymentStrategy=full-rings \
    namingPrefix=fsi-prod \
    budgetAlertEmails='["team@company.com"]'
```

**Expected Output:**
- Full ring architecture (Ring 0-3)
- Azure Firewall + Bastion
- Premium Key Vault (HSM)
- Geo-redundant storage
- No expiration tags
- Total cost: ~€1,000-2,000/month

### Example 3: Using the Agent

```bash
cd agents/azure-fsi-landingzone
python agent.py
```

**Interactive Prompts:**
1. **Project name**: `my-fsi-demo`
2. **Detect subscription tier**: Agent runs detection script
3. **Environment type**: `dev`
4. **Deployment strategy**: `shared-hub` (recommended for Free Tier)

The agent will:
- Generate Bicep templates adapted to Free Tier
- Create budget and cleanup policies
- Provide deployment scripts
- Show cost estimates

## Resource Tags

All resources deployed in Free Tier mode receive these tags:

```yaml
tags:
  Environment: dev|test|staging|sandbox
  ManagedBy: FSI-LandingZone-Agent
  CostCenter: training
  Compliance: GDPR,DORA,PSD2
  expiration: "2025-10-12"  # Non-prod only
```

## Compliance Mapping

### Free Tier Limitations vs FSI Requirements

| FSI Requirement | Free Tier Solution | Standard Solution |
|-----------------|-------------------|-------------------|
| Network Segmentation | ✅ NSGs | ✅ Azure Firewall + NSGs |
| Encryption at rest | ✅ Standard Key Vault | ✅ Premium Key Vault (HSM) |
| Encryption in transit | ✅ TLS 1.2 | ✅ TLS 1.2 |
| Geo-redundancy (DORA) | ⚠️ Single region | ✅ GRS Storage |
| Bastion/Secure Access | ⚠️ JIT VM Access | ✅ Azure Bastion |
| Audit Logs | ⚠️ Basic logging | ✅ Full Log Analytics |

**Legend:**
- ✅ Fully compliant
- ⚠️ Partial compliance (acceptable for dev/test)
- ❌ Not compliant (not available in Free Tier)

### Recommendations

**For Production:**
- ❌ **Do NOT use Free Tier** for production FSI workloads
- ✅ Use Standard/Enterprise subscription
- ✅ Enable full security features
- ✅ Meet all GDPR, DORA, PSD2, MiFID II requirements

**For Dev/Test:**
- ✅ Free Tier acceptable for learning and POC
- ⚠️ Document compliance gaps
- ⚠️ Use for non-sensitive data only
- ⚠️ Understand auto-cleanup policies

## Cost Estimates

### Free Tier Monthly Costs

| Scenario | Resources | Est. Monthly Cost |
|----------|-----------|------------------|
| **Minimal (POC)** | 1 Hub + 1 Spoke, 1 VM B1s | €8-12 |
| **Dev Environment** | 1 Hub + 1 Spoke, 2 VMs B1s, SQL Basic | €15-25 |
| **Test Environment** | 1 Hub + 2 Spokes, 3 VMs B1s, SQL Basic | €25-40 |

**Notes:**
- First year: 750h free VM hours (≈1 VM free)
- Storage costs are minimal (~€1/month)
- Outbound data transfer: Free within EU
- Always monitor actual costs in Cost Management

### Standard Deployment Costs

| Scenario | Resources | Est. Monthly Cost |
|----------|-----------|------------------|
| **Production (Full)** | Full rings, Firewall, Bastion, Premium KV | €1,000-2,000 |
| **Production (Minimal)** | Shared hub, Premium KV, Bastion | €500-800 |

## Troubleshooting

### Quota Exceeded

**Problem:** Deployment fails with "Quota exceeded" error

**Solution:**
```bash
# Check quotas
az vm list-usage --location westeurope --output table

# Request quota increase (Standard subscriptions only)
az support tickets create ...
```

### Budget Alerts Not Received

**Problem:** Budget alerts configured but not receiving emails

**Solution:**
1. Check email addresses in `budgetAlertEmails` parameter
2. Verify budget was created: `az consumption budget list`
3. Check spam folder
4. Ensure Cost Management is enabled on subscription

### Auto-Cleanup Disabled Resources

**Problem:** Resources deleted before I was done

**Solution:**
1. Check expiration tag: `az resource show ... --query tags.expiration`
2. Extend expiration:
   ```bash
   az tag update --resource-id <id> \
     --operation merge \
     --tags expiration=2025-12-31
   ```
3. Remove expiration tag to prevent cleanup:
   ```bash
   az tag update --resource-id <id> \
     --operation delete \
     --tags expiration
   ```

## Next Steps

1. **Run detection**: `./scripts/detect-free-tier.sh`
2. **Choose environment**: dev, test, or sandbox
3. **Deploy**: Use agent or Bicep directly
4. **Monitor costs**: Check Cost Management daily
5. **Learn**: Experiment with FSI-compliant architecture
6. **Upgrade**: Move to Standard for production workloads

## Additional Resources

- [Azure Free Account FAQ](https://azure.microsoft.com/free/free-account-faq/)
- [Azure FSI Landing Zone Documentation](../README.md)
- [Ring Architecture Guide](rings.md)
- [Deployment Workflow](../guides/workflow.md)
