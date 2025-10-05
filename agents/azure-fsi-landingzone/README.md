# Azure FSI Landing Zone Agent (Mono-Agent)

An AI-powered deployment agent for Azure Financial Services Industry (FSI) Landing Zones.

## Overview

This is the **mono-agent** implementation - best for quick template generation and simple deployments.

**Key Features:**
- Fast template generation using Bicep + Azure Verified Modules (AVM)
- Ring-based deployment strategy (Ring 0/1/2)
- European compliance (GDPR, DORA, PSD2, MiFID II, EBA GL)
- Simple, focused operation
- Lower cost (single agent invocation)

## Quick Start

```bash
cd agents/azure-fsi-landingzone
python agent.py
```

Example prompts:
- "Generate Ring 0 foundation templates for FSI Landing Zone"
- "Create a hub VNet with Azure Firewall"
- "List available deployment rings"

## When to Use This Agent

✅ **Use this agent when:**
- You need quick template generation
- Your task is simple and focused
- You're getting started with FSI Landing Zones
- You prefer simplicity over depth
- You want lower cost

❌ **Consider the Squad instead when:**
- You need comprehensive security/compliance review
- You want expert analysis across multiple domains
- You're preparing for production deployment
- You need drift detection

## Documentation

**All documentation has been centralized. See:**

📚 **[Complete Azure FSI Documentation](../../docs/azure-fsi/)**

### Quick Links
- **[Quick Start Guide](../../docs/azure-fsi/guides/quickstart-mono.md)**
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
- Azure CLI (for deployment)
- Anthropic API key

See the [main documentation](../../docs/azure-fsi/) for detailed requirements.

---

**Part of the [Claude Agents Repository](../../README.md)**
