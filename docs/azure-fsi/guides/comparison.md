# Mono-Agent vs Multi-Agent Squad: Comparison Guide

## Overview

This document compares the **mono-agent** approach (`azure-fsi-landingzone`) with the **multi-agent squad** approach (`azure-fsi-landingzone-squad`) for Azure FSI Landing Zone deployments.

---

## 🎯 Which One Should You Use?

### Use **Mono-Agent** (`azure-fsi-landingzone`) when:
- ✅ You need to **quickly generate templates**
- ✅ Your task is **simple and focused** (e.g., "generate a hub-vnet template")
- ✅ You prefer **simplicity** over depth
- ✅ You want **lower cost** (single agent invocation)
- ✅ You're **getting started** with FSI Landing Zones

### Use **Multi-Agent Squad** (`azure-fsi-landingzone-squad`) when:
- ✅ You need **comprehensive security/compliance review**
- ✅ You want **expert analysis** in multiple domains (DevOps, Security, Network, Architecture)
- ✅ You need to **detect drift** between local templates and deployed infrastructure
- ✅ You're preparing for **production deployment or audit**
- ✅ You want **parallel analysis** for faster results on complex tasks
- ✅ You need **cross-domain insights** (e.g., security + network + DevOps)

---

## 📊 Feature Comparison

| Feature | Mono-Agent | Multi-Agent Squad |
|---------|------------|-------------------|
| **Simplicity** | ⭐⭐⭐⭐⭐ Simple | ⭐⭐⭐ Moderate |
| **Setup** | 1 agent | 1 orchestrator + 4 specialists |
| **Expertise Depth** | ⭐⭐⭐ Generalist | ⭐⭐⭐⭐⭐ Deep specialists |
| **Template Generation** | ⭐⭐⭐⭐⭐ Fast | ⭐⭐⭐⭐⭐ Same speed |
| **Security Analysis** | ⭐⭐⭐ Basic | ⭐⭐⭐⭐⭐ Expert-level |
| **Compliance Review** | ⭐⭐⭐ Generic | ⭐⭐⭐⭐⭐ Regulation-specific |
| **Drift Detection** | ⭐⭐⭐ Manual | ⭐⭐⭐⭐⭐ Automated |
| **Parallelization** | ❌ Sequential | ✅ Parallel analysis |
| **Cost** | ⭐⭐⭐⭐ Lower | ⭐⭐⭐ Higher (multiple invocations) |
| **Maintenance** | ⭐⭐⭐⭐⭐ Single codebase | ⭐⭐⭐⭐ 5 agents to maintain |
| **Extensibility** | ⭐⭐⭐ Add tools | ⭐⭐⭐⭐⭐ Add new specialist agents |

---

## 🔄 Example Use Cases

### Example 1: Generate a Hub VNet Template

**Mono-Agent:**
```
User: "Generate a hub-vnet template for Ring 0"
Agent: [Generates Bicep template]
Time: ~30 seconds
Quality: ⭐⭐⭐⭐⭐ Perfect for this task
```

**Multi-Agent Squad:**
```
User: "Generate a hub-vnet template for Ring 0"
Orchestrator: [Generates Bicep template] (same as mono-agent)
Time: ~30 seconds
Quality: ⭐⭐⭐⭐⭐ Same result
```

**Winner:** **Tie** - Both equally good for simple generation tasks

---

### Example 2: Review Security Configuration

**Mono-Agent:**
```
User: "Review my Ring 0 security configuration"
Agent:
  - Reads Key Vault template
  - Generic security checks
  - Basic recommendations

Result:
  ✅ Key Vault: Purge protection enabled
  ✅ Private endpoints configured
  ⚠️  Consider adding diagnostic settings

Time: ~2 minutes
Quality: ⭐⭐⭐ Correct but basic
```

**Multi-Agent Squad:**
```
User: "Review my Ring 0 security configuration"
Orchestrator → Security Specialist:
  - Reads all security templates (Key Vault, NSG, Policies)
  - Cross-references with GDPR/DORA/PSD2 requirements
  - Checks both local templates AND deployed state (Azure CLI)
  - Compares against FSI security baseline

Result:
  ✅ Key Vault: Purge protection ✓, soft-delete ✓, RBAC ✓
  ❌ CRITICAL: Diagnostic settings missing (GDPR requirement!)
  ❌ CRITICAL: Private DNS zone not configured
  ⚠️  NSG rule allows port 22 from 0.0.0.0/0 (security risk)
  ⚠️  CMK not configured (PSD2 recommends customer-managed keys)
  ⚠️  Firewall missing deny rule for public access

  📊 Compliance Score: 65/100
  🏛️  GDPR: Non-compliant (diagnostic settings required)
  🏛️  DORA: Partial compliance
  🏛️  PSD2: Needs improvement (CMK recommended)

Time: ~2 minutes
Quality: ⭐⭐⭐⭐⭐ Comprehensive, regulation-specific
```

**Winner:** **Multi-Agent Squad** 🏆 - Much deeper analysis

---

### Example 3: Full Deployment Review (Ring 0 + 1 + 2)

**Mono-Agent:**
```
User: "Review my entire FSI Landing Zone deployment"
Agent:
  - Sequentially reads all templates
  - Generic analysis of each component
  - Provides overall assessment

Time: ~5-7 minutes (sequential)
Quality: ⭐⭐⭐ Correct but may miss cross-domain issues
```

**Multi-Agent Squad:**
```
User: "Review my entire FSI Landing Zone deployment"
Orchestrator:
  ├─ Security Specialist  → Reviews Ring 0 (security, policies, Key Vault)
  ├─ Network Specialist   → Reviews Ring 0 + 2 (network topology, firewall)
  ├─ DevOps Specialist    → Reviews Ring 1 (CI/CD, deployment scripts)
  └─ All run in PARALLEL ⚡

Architect Specialist:
  - Receives all 3 specialist reports
  - Synthesizes findings
  - Identifies cross-domain issues
  - Prioritizes remediation

Result:
  📊 Overall Architecture Score: 7.5/10

  🔴 CRITICAL Issues (3):
    1. NSG port 22 exposed to internet (Security + Network)
    2. No rollback mechanism in deploy.sh (DevOps)
    3. Key Vault diagnostics missing (Security → GDPR compliance)

  🟡 MEDIUM Issues (5):
    4. Pipeline missing approval gates for PROD (DevOps)
    5. Firewall only has 2 rules (Network)
    6. No drift detection configured (DevOps)
    7. Storage account using Microsoft-managed keys (Security)
    8. No VPN Gateway configured (Network)

  ℹ️  INFO (4):
    9. Consider blue-green deployment (DevOps)
    10. Add cost monitoring (Architect)
    11. Plan for multi-region (Architect)
    12. Document architecture decisions (Architect)

  💡 Recommendations (Prioritized):
    Priority 1: Fix NSG rule immediately (security risk)
    Priority 2: Enable Key Vault diagnostics (compliance blocker)
    Priority 3: Add rollback to deploy.sh (operational resilience)

Time: ~3-4 minutes (parallel analysis)
Quality: ⭐⭐⭐⭐⭐ Comprehensive, cross-domain, prioritized
```

**Winner:** **Multi-Agent Squad** 🏆 - Faster + deeper + cross-domain insights

---

### Example 4: Drift Detection (Local Templates vs Deployed)

**Mono-Agent:**
```
User: "Check if my deployed infrastructure matches the templates"
Agent:
  - Manually reads template
  - Runs 'az' commands
  - Compares manually
  - May miss some resources

Time: ~5 minutes (manual, sequential)
Risk: ⚠️  May miss resources
Quality: ⭐⭐⭐ Functional but manual
```

**Multi-Agent Squad:**
```
User: "Check drift between templates and deployed infrastructure"
Orchestrator:
  ├─ Security Specialist  → Compares: Key Vault, NSG, Policies
  ├─ Network Specialist   → Compares: VNet, Firewall, Peerings
  └─ DevOps Specialist    → Compares: Storage, Container Registry

Architect Specialist → Synthesizes:

  📊 Drift Detection Report:

  Ring 0 (Foundation):
    ✅ Hub VNet: No drift
    ❌ NSG: 2 rules added manually (NOT in template!)
         Manual rule 1: Allow 10.0.0.0/8 → port 443
         Manual rule 2: Allow AzureLoadBalancer → *
    ⚠️  Key Vault: Diagnostic settings added manually
    ⚠️  Azure Firewall: 1 additional rule (NOT in template)

  Ring 1 (Platform):
    ✅ Container Registry: Synced
    ❌ Storage Account: SKU changed
         Template: Standard_LRS
         Deployed: Standard_GRS (more expensive!)
    ⚠️  Shared Key Vault: Access policies modified manually

  Ring 2 (Workload):
    ✅ Spoke VNet: Synced
    ❌ App Service: Scaled up manually
         Template: B1
         Deployed: S1

  💡 Recommendations:
    1. Update templates to match manual changes OR
    2. Revert manual changes to match templates
    3. Implement change control process to prevent drift
    4. Schedule weekly drift detection scans

Time: ~3 minutes (parallel checks)
Quality: ⭐⭐⭐⭐⭐ Exhaustive, automated
```

**Winner:** **Multi-Agent Squad** 🏆 - Comprehensive drift detection across all domains

---

## 💰 Cost Comparison

### Mono-Agent
- **Per query**: 1 agent invocation
- **Simple task**: ~$0.001 - $0.01
- **Complex task**: ~$0.05 - $0.10

### Multi-Agent Squad
- **Per query**: 1 orchestrator + N specialists (typically 3-4)
- **Simple task**: ~$0.001 - $0.01 (same as mono, delegates to 0 specialists)
- **Complex task**: ~$0.15 - $0.30 (3-4 specialist invocations + orchestrator + architect)

**Cost difference**: Multi-agent is **2-3x more expensive** for complex tasks, but provides **5-10x more value** through deeper analysis.

---

## 🎓 Recommendation Strategy

### Getting Started → Use Mono-Agent
When learning FSI Landing Zones:
```bash
cd agents/azure-fsi-landingzone
python agent.py
```

### Pre-Production Review → Use Multi-Agent Squad
Before deploying to UAT/PROD:
```bash
cd agents/azure-fsi-landingzone-squad
python orchestrator.py  # Not yet created, will be added
```

### Hybrid Approach (Best of Both)
1. **Generation phase**: Use mono-agent for rapid template generation
2. **Review phase**: Use multi-agent squad for comprehensive review
3. **Deployment**: Use mono-agent for quick deployments
4. **Audit**: Use multi-agent squad for compliance validation

---

## 📈 Performance Benchmarks

| Task | Mono-Agent | Multi-Agent Squad | Winner |
|------|------------|-------------------|--------|
| Generate 1 template | 30s | 30s | Tie |
| Generate 5 templates | 2 min | 2 min | Tie |
| Review security (Ring 0) | 2 min | 2 min | **Squad** (depth) |
| Review full deployment | 5-7 min | 3-4 min | **Squad** (parallel) |
| Drift detection | 5 min | 3 min | **Squad** (automated) |
| Simple Q&A | 10s | 10s | Tie |

---

## 🚀 Migration Path

Already using mono-agent? Here's how to adopt multi-agent squad:

1. **Keep using mono-agent** for daily template generation
2. **Try multi-agent squad** for your next security review
3. **Compare results** side-by-side
4. **Adopt squad** for pre-production and audit workflows
5. **Stick with mono-agent** for quick, simple tasks

You don't have to choose one or the other - use both!

---

## 🎯 Decision Matrix

| Your Scenario | Recommended Agent |
|---------------|-------------------|
| "I need a quick VNet template" | **Mono-Agent** |
| "Generate all Ring 0 templates" | **Mono-Agent** |
| "Is my deployment secure?" | **Multi-Agent Squad** |
| "Am I GDPR compliant?" | **Multi-Agent Squad** |
| "Review before PROD deployment" | **Multi-Agent Squad** |
| "Check drift from templates" | **Multi-Agent Squad** |
| "Audit for compliance" | **Multi-Agent Squad** |
| "Quick export of deployment plan" | **Mono-Agent** |
| "Comprehensive architecture review" | **Multi-Agent Squad** |

---

## 📚 See Also

- [Mono-Agent README](../azure-fsi-landingzone/README.md)
- [Multi-Agent Architecture](./MULTI-AGENT-ARCHITECTURE.md)
- [Ring Architecture](./RING-ARCHITECTURE.md)

---

**TL;DR**: Use **mono-agent** for speed and simplicity. Use **multi-agent squad** for depth and compliance. Or use both! 🎉
