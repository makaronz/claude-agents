# Quick Start - Ring-Based Deployment

## 🚀 5-Minute Quick Start

### Scenario 1: Complete FSI Landing Zone (All Rings)

Deploy a full FSI-compliant landing zone with all rings and standard depth.

```bash
# 1. Start the agent
python agents/azure-fsi-landingzone/agent.py

# 2. In the agent conversation:
```

**Agent Interaction:**
```
You: Set project name to "contoso-banking"

Agent: ✅ Project name set: contoso-banking
📁 All generated assets will be saved to:
   /path/to/agents/azure-fsi-landingzone/contoso-banking/

You: List available deployment rings

Agent: [Shows all rings with details]

You: Select all deployment rings

Agent: ✅ Selected deployment rings:
   ✓ ring0_foundation
   ✓ ring1_platform
   ✓ ring2_workload

You: Set deployment depth to standard

Agent: ✅ Deployment depth set to: STANDARD

You: Generate ring deployment

Agent: 🚀 Generating deployment templates for selected rings...
[Creates all files in contoso-banking/ folder]

✅ Generated 15 files
📁 Output directory: contoso-banking/
```

**Generated Structure:**
```
contoso-banking/
├── deploy.sh                       # Deployment orchestration
├── ring0_foundation/
│   ├── DEPLOYMENT.md
│   ├── hub-vnet.bicep
│   ├── azure-firewall.bicep
│   ├── key-vault-core.bicep
│   ├── log-analytics-workspace.bicep
│   └── ... (12 more files)
├── ring1_platform/
│   ├── DEPLOYMENT.md
│   ├── container-registry.bicep
│   └── ... (6 more files)
└── ring2_workload/
    ├── DEPLOYMENT.md
    ├── spoke-vnet-app.bicep
    └── ... (8 more files)
```

---

### Scenario 2: Minimal Foundation Only (Quick POC)

Deploy only the mandatory compliance baseline for testing.

**Agent Interaction:**
```
You: Set project name to "poc-compliance"

You: Select ring0_foundation only

You: Set deployment depth to minimal

You: Generate ring deployment
```

**Result:**
```
poc-compliance/
├── deploy.sh
└── ring0_foundation/
    ├── DEPLOYMENT.md
    ├── hub-vnet.bicep               # Only mandatory components
    ├── azure-firewall.bicep
    ├── key-vault-core.bicep
    ├── log-analytics-workspace.bicep
    ├── defender-for-cloud.bicep
    └── azure-policies.bicep
```

---

### Scenario 3: Foundation + Workloads (Skip DevOps)

Deploy compliance baseline and application infrastructure, but skip the DevOps ring.

**Agent Interaction:**
```
You: Set project name to "app-platform"

You: Select rings: ring0_foundation, ring2_workload

You: Set deployment depth to standard

You: Generate ring deployment
```

**Result:**
```
app-platform/
├── deploy.sh
├── ring0_foundation/              # Compliance baseline
│   └── ... (full standard deployment)
└── ring2_workload/                 # Application infrastructure
    ├── DEPLOYMENT.md
    ├── spoke-vnet-app.bicep
    ├── storage-accounts.bicep
    ├── app-service-plan.bicep
    └── sql-database.bicep
```

---

## 📋 Command Reference

### Project Setup
| Command | Purpose |
|---------|---------|
| `Set project name to "{name}"` | Create project folder |
| `List deployment rings` | View all rings and components |

### Ring Selection
| Command | Purpose |
|---------|---------|
| `Select all rings` | Deploy Ring 0, 1, and 2 |
| `Select ring0_foundation only` | Deploy only Ring 0 |
| `Select rings: ring0_foundation, ring2_workload` | Deploy Ring 0 and 2 |

### Deployment Configuration
| Command | Purpose |
|---------|---------|
| `Set deployment depth to minimal` | Essential components only |
| `Set deployment depth to standard` | Recommended for production |
| `Set deployment depth to advanced` | All components |

### Generate Templates
| Command | Purpose |
|---------|---------|
| `Generate ring deployment` | Create all templates for selected rings |

---

## 🎯 Common Workflows

### Workflow A: Progressive Deployment (Recommended)

**Phase 1 - Foundation (Week 1)**
```
1. Set project name to "mybank-lz"
2. Select ring0_foundation only
3. Set depth to standard
4. Generate ring deployment
5. Review and deploy Ring 0
6. Validate compliance policies
```

**Phase 2 - Platform (Week 2)**
```
1. Select rings: ring0_foundation, ring1_platform
2. Generate ring deployment
3. Deploy Ring 1
4. Set up CI/CD pipelines
```

**Phase 3 - Workloads (Week 3+)**
```
1. Select all rings
2. Generate ring deployment
3. Deploy Ring 2
4. Deploy applications
```

---

### Workflow B: Rapid Deployment (All at Once)

**For Experienced Teams**
```
1. Set project name to "fasttrack-lz"
2. Select all rings
3. Set depth to standard
4. Generate ring deployment
5. Review all templates
6. Run ./deploy.sh
```

---

### Workflow C: Cost-Conscious POC

**Minimal Cost Deployment**
```
1. Set project name to "poc-minimal"
2. Select ring0_foundation only
3. Set depth to minimal
4. Generate ring deployment
5. Deploy only mandatory components
```

**Cost Savings:**
- ✅ No VPN Gateway (if not needed)
- ✅ No advanced features
- ✅ Minimal SKUs where possible
- ✅ Single region deployment

---

## 🔍 What Gets Generated?

### For Each Ring

#### `DEPLOYMENT.md`
Deployment guide specific to the ring:
- Component list (mandatory vs optional)
- Deployment commands
- Validation steps

#### Component Bicep Files
Individual `.bicep` files for each component:
- `hub-vnet.bicep`
- `azure-firewall.bicep`
- `key-vault-core.bicep`
- etc.

### Project-Level Files

#### `deploy.sh`
Main deployment orchestration script:
```bash
#!/bin/bash
# Checks prerequisites
# Deploys Ring 0
# Deploys Ring 1 (if selected)
# Deploys Ring 2 (if selected)
```

---

## 🎓 Next Steps After Generation

### 1. Review Generated Files
```bash
cd contoso-banking/
ls -la
cat ring0_foundation/DEPLOYMENT.md
```

### 2. Customize Parameters
Edit component files to adjust:
- Resource naming
- IP address ranges
- SKU sizes
- Regional preferences

### 3. Validate Templates
```bash
# Validate Ring 0 before deployment
cd ring0_foundation/
az deployment sub validate \
  --location francecentral \
  --template-file hub-vnet.bicep
```

### 4. Deploy Rings Sequentially
```bash
# Deploy Ring 0 first
cd ring0_foundation/
./deploy.sh

# Then Ring 1 (if applicable)
cd ../ring1_platform/
./deploy.sh

# Finally Ring 2 (if applicable)
cd ../ring2_workload/
./deploy.sh
```

### 5. Verify Compliance
```bash
# Check policy compliance
az policy state list \
  --resource-group <rg-name> \
  --query "[?complianceState=='NonCompliant']"
```

---

## 💡 Pro Tips

### 🎯 Tip 1: Start Small
Always start with Ring 0 in minimal depth first, then expand.

### 🎯 Tip 2: Use Git
Commit generated templates to version control:
```bash
cd contoso-banking/
git init
git add .
git commit -m "Initial FSI Landing Zone templates"
```

### 🎯 Tip 3: Separate Projects for Environments
```bash
# Development
Set project name to "mybank-dev"

# Production
Set project name to "mybank-prod"
```

### 🎯 Tip 4: Review DEPLOYMENT.md Files
Each ring has specific deployment guidance. Read them before deploying!

### 🎯 Tip 5: Validate Before Deploying
Always use `az deployment sub validate` before actual deployment.

---

## 🆘 Troubleshooting

### "Project name not set" Error
**Solution:** Run `Set project name to "{name}"` first

### "No rings selected" Error
**Solution:** Run `Select rings: ...` or `Select all rings`

### Missing Dependencies Warning
**Example:** Ring 1 requires Ring 0
**Solution:** Either:
- Add Ring 0 to selection: `Select rings: ring0_foundation, ring1_platform`
- Or deploy Ring 0 first, then Ring 1 separately

### File Already Exists
**Solution:** The agent won't overwrite existing files. Either:
- Delete the project folder and regenerate
- Use a different project name
- Manually merge changes

---

## 📚 Additional Resources

- **[RING-ARCHITECTURE.md](./RING-ARCHITECTURE.md)** - Detailed ring architecture
- **[CHANGELOG-RINGS.md](./CHANGELOG-RINGS.md)** - What's new in v2.0
- **[WORKFLOW.md](./WORKFLOW.md)** - Complete deployment workflows
- **[config.yaml](./config.yaml)** - Ring configuration reference

---

## 🎉 You're Ready!

You now have everything you need to deploy a ring-based FSI Landing Zone. Start with Scenario 2 (Minimal Foundation) for a quick test, then progress to Scenario 1 for production.

Happy deploying! 🚀
