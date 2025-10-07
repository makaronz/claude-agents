# Azure FSI Landing Zone Agent - Quick Start

Get started with the Azure FSI Landing Zone Agent in 10 minutes.

## ⚡ Prerequisites Checklist

Before starting, ensure you have:

- [ ] **Node.js & npm** installed
- [ ] **Claude Code CLI v2.0.1+** installed
- [ ] **Azure CLI** installed
- [ ] **Bicep** installed
- [ ] **Python 3.10+** installed
- [ ] **Anthropic API key** (from https://console.anthropic.com)
- [ ] **Azure subscription** with Owner/Contributor permissions
- [ ] **Logged in to Azure** (`az login`)

## 🚀 Quick Install (5 minutes)

```bash
# 1. Install Claude Code CLI (REQUIRED - v2.0.1+)
npm install -g @anthropic-ai/claude-code@latest
claude --version  # Should show 2.0.1 or later

# 2. Clone repository
git clone https://github.com/frntn/claude-agents.git
cd claude-agents/agents/azure-fsi-landingzone

# 3. Install Python dependencies
uv pip sync uv.lock         # if present
# or resolve the latest versions
uv pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
vim .env  # Add your ANTHROPIC_API_KEY and AZURE_SUBSCRIPTION_ID

# 5. Start the agent
python agent.py
```

## 💬 First Interaction (2 minutes)

Once the agent starts, try these commands:

```
You: Check Azure prerequisites
```

Expected: Agent validates Azure CLI, Bicep, and authentication ✅

```
You: List FSI compliance requirements
```

Expected: Agent shows GDPR, DORA, PSD2, MiFID II requirements 📋

```
You: Generate Bicep template for hub-vnet
```

Expected: Agent generates `templates/hub-vnet.bicep` 📄

```
You: quit
```

Expected: Agent disconnects gracefully 👋

## 🔧 Troubleshooting

### ❌ Error: "unknown option '--setting-sources'"

**Cause**: You have Claude Code v1.x (old version)

**Fix**:
```bash
npm install -g @anthropic-ai/claude-code@latest
claude --version  # Must be 2.0.1+
```

### ❌ Error: "ImportError: attempted relative import"

**Cause**: Running from wrong directory

**Fix**:
```bash
cd agents/azure-fsi-landingzone
python agent.py
```

### ❌ Error: "Failed to connect to Claude Agent SDK"

**Cause**: Missing or invalid `ANTHROPIC_API_KEY`

**Fix**:
```bash
# Check .env file exists
ls -la .env

# Verify API key is set
grep ANTHROPIC_API_KEY .env

# Get a new key from: https://console.anthropic.com
```

### ❌ Agent hangs/freezes

**Possible causes**:
1. Claude Code CLI version too old (update to 2.0.1+)
2. Missing `.env` file (copy from `.env.example`)
3. Network connectivity issues (check internet connection)

**Debug**:
```bash
# Run with debug output
claude --debug python agent.py
```

## 📚 Next Steps

Once the agent is working:

1. **Read the full workflow**: See [WORKFLOW.md](WORKFLOW.md) for complete deployment guide
2. **Customize config**: Edit `config.yaml` for your organization
3. **Deploy infrastructure**: Follow Day 1-5 in WORKFLOW.md
4. **Review compliance**: Use the compliance checker agent

## 🆘 Getting Help

- **Documentation**: [README.md](README.md)
- **Full workflow**: [WORKFLOW.md](WORKFLOW.md)
- **Issues**: https://github.com/frntn/claude-agents/issues

## 🎯 Version Requirements

| Component | Minimum Version | Recommended |
|-----------|----------------|-------------|
| **Claude Code CLI** | **2.0.1** | Latest |
| Python | 3.10 | 3.12 |
| Azure CLI | 2.50.0 | Latest |
| Bicep | 0.24.0 | Latest |
| Node.js | 18.x | 20.x LTS |

**Critical**: Claude Code CLI v2.0.1+ is required. Version 1.x will NOT work.
