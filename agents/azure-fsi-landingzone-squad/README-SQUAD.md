# Azure FSI Landing Zone - Multi-Agent Squad

🎯 **Expert-level FSI Landing Zone analysis through specialized AI agent collaboration**

## What is This?

This is the **multi-agent squad version** of the Azure FSI Landing Zone agent. Instead of one generalist agent, you get a **team of 4 specialist agents** that collaborate:

- 🚀 **DevOps Specialist** - CI/CD, deployment automation, rollback strategies
- 🔒 **Security Specialist** - Compliance (GDPR, DORA, PSD2), policies, hardening
- 🌐 **Network Specialist** - Hub-spoke topology, firewall, connectivity
- 🏗️ **Architect Specialist** - Synthesis, best practices, recommendations

## Why Use Multi-Agent Squad?

✅ **Deep expertise** in each domain (vs generalist knowledge)
✅ **Parallel analysis** for faster complex reviews (2-3x speed)
✅ **Cross-domain insights** (e.g., security + network issues)
✅ **Comprehensive audits** for production readiness
✅ **Compliance validation** (GDPR, DORA, PSD2, MiFID II)

## When to Use This vs Mono-Agent?

| Use Case | Mono-Agent | Multi-Agent Squad |
|----------|------------|-------------------|
| Quick template generation | ✅ | ✅ |
| Security audit | ⚠️ Basic | ✅ Expert |
| Compliance review (GDPR, DORA) | ⚠️ Generic | ✅ Regulation-specific |
| Full deployment review | ⚠️ Sequential | ✅ Parallel |
| Drift detection | ⚠️ Manual | ✅ Automated |
| Pre-PROD validation | ⚠️ | ✅ Recommended |

**See [COMPARISON.md](./COMPARISON.md) for detailed comparison.**

## Quick Start

```bash
# Run the orchestrator (coordinates the squad)
python orchestrator.py

# Or run individual specialists for testing
python sub-agents/security/agent.py
python sub-agents/devops/agent.py
```

## Example Usage

```
User: "Review my Ring 0 deployment for production readiness"

Orchestrator: Coordinating specialist review...

┌─ Security Specialist ─────────────────────┐
│ ✅ Key Vault: Purge protection enabled    │
│ ❌ CRITICAL: Diagnostic settings missing  │
│ ⚠️  NSG: Port 22 open to internet        │
│ Compliance Score: 65/100 (GDPR issues)   │
└───────────────────────────────────────────┘

┌─ Network Specialist ──────────────────────┐
│ ✅ Hub-Spoke: Correctly configured        │
│ ⚠️  Firewall: Only 2 rules defined       │
│ ❌ NSG: Port 22 allows 0.0.0.0/0         │
└───────────────────────────────────────────┘

┌─ Architect Synthesis ─────────────────────┐
│ Production Readiness: 6/10 (NOT READY)    │
│                                           │
│ 🔴 BLOCKERS:                              │
│  1. Close NSG port 22 (use Bastion)      │
│  2. Enable Key Vault diagnostics (GDPR)  │
│                                           │
│ Timeline: 2-3 days to fix                │
└───────────────────────────────────────────┘
```

## Architecture

```
            USER
              ↓
        ORCHESTRATOR
              ↓
    ┌─────────┼─────────┐
    ▼         ▼         ▼
 DevOps  Security  Network  → ARCHITECT
                               (Synthesis)
```

**See [MULTI-AGENT-ARCHITECTURE.md](./MULTI-AGENT-ARCHITECTURE.md) for details.**

## Sub-Agents

### 1. DevOps Specialist
**Focus:** CI/CD pipelines, deployment automation, rollback

**Tools:**
- `analyze_deployment_scripts` - Reviews deploy.sh, pipelines
- `review_pipeline_security` - Checks for hardcoded secrets
- `check_rollback_capability` - Validates rollback mechanisms
- `validate_cicd_configuration` - FSI compliance checks

### 2. Security Specialist
**Focus:** GDPR, DORA, PSD2 compliance, security hardening

**Tools:**
- `audit_key_vault_security` - Key Vault configuration audit
- `analyze_nsg_rules` - NSG vulnerability detection
- `check_compliance_policies` - Policy compliance validation
- `validate_encryption_config` - Encryption at rest/in transit
- `review_iam_configuration` - Entra ID, PIM, RBAC review

### 3. Network Specialist
**Focus:** Hub-spoke topology, Azure Firewall, connectivity

**Tools:**
- `analyze_network_topology` - Hub-spoke design review
- `review_firewall_rules` - Firewall policy validation
- `check_private_endpoints` - Private Link configuration
- `validate_routing_tables` - UDR and BGP review

### 4. Architect Specialist
**Focus:** Overall design, synthesis, best practices

**Tools:**
- `synthesize_analysis` - Consolidates multi-agent findings
- `recommend_improvements` - Prioritized action items
- `estimate_costs` - Cost analysis per ring
- `assess_scalability` - Future-proofing recommendations

## Cost Comparison

| Task Type | Mono-Agent | Multi-Agent Squad |
|-----------|------------|-------------------|
| Simple (1 template) | $0.001 | $0.001 (same) |
| Complex review | $0.05 | $0.15 (3x cost, 10x value) |

**Worth it?** For production deployments and compliance audits: **Absolutely!**

## Documentation

- 📖 [COMPARISON.md](./COMPARISON.md) - Mono vs Multi comparison
- 🏗️ [MULTI-AGENT-ARCHITECTURE.md](./MULTI-AGENT-ARCHITECTURE.md) - Architecture details
- 🎯 [RING-ARCHITECTURE.md](./RING-ARCHITECTURE.md) - Ring deployment strategy
- 🚀 [QUICKSTART-RINGS.md](./QUICKSTART-RINGS.md) - Getting started guide

## License

Same as parent project.

---

**TL;DR**: Need expert-level FSI Landing Zone analysis? Use the squad. Need quick templates? Use [mono-agent](../azure-fsi-landingzone/). Or use both! 🎉
