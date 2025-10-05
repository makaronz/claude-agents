# Azure FSI Landing Zone Agent (Multi-Agent Squad)

Expert-level FSI Landing Zone analysis through specialized AI agent collaboration.

## Overview

This is the **multi-agent squad** implementation - a team of specialist AI agents that collaborate to provide expert-level analysis and recommendations.

**The Squad:**
- 🏗️ **Architect Agent**: Holistic design and architectural recommendations
- 🚀 **DevOps Agent**: CI/CD pipelines and deployment automation
- 🔒 **Security Agent**: Security posture and compliance analysis
- 🌐 **Network Agent**: Network design and connectivity review

## Quick Start

```bash
cd agents/azure-fsi-landingzone-squad
python agent.py
```

Example prompts:
- "Review my entire FSI Landing Zone deployment for production readiness"
- "Analyze security posture for Ring 0 foundation"
- "Detect drift between local templates and deployed Azure resources"
- "Generate comprehensive compliance report"

## When to Use This Agent

✅ **Use this agent when:**
- You need comprehensive security/compliance review
- You want expert analysis across multiple domains
- You need drift detection between local templates and deployed infrastructure
- You're preparing for production deployment or audit
- You want parallel analysis for faster results on complex tasks
- You need cross-domain insights (security + network + DevOps)

❌ **Consider the Mono-Agent instead when:**
- You just need quick template generation
- Your task is simple and focused
- You're getting started with FSI Landing Zones
- You prefer simplicity over depth

## How It Works

The orchestrator agent coordinates specialist agents to provide multi-dimensional analysis:

```
User Request
     ↓
Orchestrator
     ├→ DevOps Agent   (parallel analysis)
     ├→ Security Agent (parallel analysis)
     ├→ Network Agent  (parallel analysis)
     └→ Architect Agent (synthesizes all inputs)
     ↓
Consolidated Report
```

## Documentation

**All documentation has been centralized. See:**

📚 **[Complete Azure FSI Documentation](../../docs/azure-fsi/)**

### Quick Links
- **[Quick Start Guide](../../docs/azure-fsi/guides/quickstart-squad.md)**
- **[Multi-Agent Architecture](../../docs/azure-fsi/architecture/multi-agent.md)**
- **[Ring Architecture](../../docs/azure-fsi/architecture/rings.md)**
- **[Deployment Workflow](../../docs/azure-fsi/guides/workflow.md)**
- **[Mono vs Squad Comparison](../../docs/azure-fsi/guides/comparison.md)**
- **[Changelog](../../docs/azure-fsi/changelog.md)**

## Configuration

Copy `.env.example` to `.env` and add your `ANTHROPIC_API_KEY`:

```bash
cp .env.example .env
# Edit .env and add your API key
```

## Requirements

- Python 3.10+
- Claude Agent SDK v0.1.0+
- Azure CLI (for deployment and drift detection)
- Anthropic API key

See the [main documentation](../../docs/azure-fsi/) for detailed requirements.

## Key Features

### Specialist Expertise
Each agent brings deep domain knowledge:
- **DevOps**: Azure DevOps, GitHub Actions, deployment automation
- **Security**: Azure Defender, Key Vault, compliance policies
- **Network**: VNets, Firewall, NSGs, private endpoints
- **Architect**: Design patterns, cost optimization, governance

### Parallel Analysis
Multiple agents work concurrently for faster results on complex tasks.

### Drift Detection
Compare local Bicep templates with actual deployed Azure resources to identify configuration drift.

### Comprehensive Reports
Consolidated analysis across all domains with actionable recommendations.

---

**Part of the [Claude Agents Repository](../../README.md)**
