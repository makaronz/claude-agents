# Azure FSI Landing Zone Agent - Quick Start

Get started with the Azure FSI Landing Zone Agent in 10 minutes.

## ⚡ Prerequisites Checklist

Before starting, ensure you have:

- [ ] **Node.js & npm** installed (v18+)
- [ ] **Claude Code CLI v2.0.1+** installed
- [ ] **Azure CLI** installed (v2.50.0+)
- [ ] **Bicep** installed (v0.24.0+)
- [ ] **Python 3.10+** installed
- [ ] **Anthropic API key** (from https://console.anthropic.com)
- [ ] **Azure subscription** with Owner/Contributor permissions
- [ ] **Logged in to Azure** (`az login`)

## 🚀 Quick Install (5 minutes)

### Step 1: Install Claude Code CLI (REQUIRED - v2.0.1+)

```bash
npm install -g @anthropic-ai/claude-code@latest
```

**Verify installation:**
```bash
claude --version
```
Expected output: `2.0.1` or later ✅

### Step 2: Clone Repository

```bash
git clone https://github.com/frntn/claude-agents.git
cd claude-agents/agents/azure-fsi-landingzone
```

**Verify location:**
```bash
pwd
ls -la agent.py config.yaml requirements.txt
```
Expected: All 3 files should exist ✅

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Verify installation:**
```bash
python -c "import claude_agent_sdk; print('SDK installed:', claude_agent_sdk.__version__)"
```
Expected: `SDK installed: 0.1.0` or later ✅

### Step 4: Configure Environment

```bash
cp .env.example .env
```

**Edit `.env` file** (use `nano`, `vim`, or your preferred editor):
```bash
nano .env
```

**Required values to set:**
```bash
# Get subscription ID
az account show --query id -o tsv

# Get tenant ID
az account show --query tenantId -o tsv

# Get API key from: https://console.anthropic.com/settings/keys
```

**Your `.env` should look like:**
```bash
AZURE_SUBSCRIPTION_ID=12345678-1234-1234-1234-123456789abc
AZURE_TENANT_ID=87654321-4321-4321-4321-cba987654321
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**Verify configuration:**
```bash
grep -v '^#' .env | grep -v '^$'
```
Expected: 3 lines with actual values (no "your-xxx-here" placeholders) ✅

### Step 5: Start the Agent

**Solo Mode (default)** - Single agent handles all tasks:
```bash
python agent.py
```

**Squad Mode** - Multi-agent collaboration (Architect, Security, Network, DevOps):
```bash
python agent.py --squad
```

Expected output:
```
Starting Azure FSI Landing Zone Agent...
Connected to Claude Agent SDK
Agent ready. Type 'quit' to exit.

You:
```

## 💬 First Interactions

### Test 1: Check Prerequisites

```
You: Check Azure prerequisites and show my subscription details
```

**Expected output:**
- ✅ Azure CLI version
- ✅ Bicep version
- ✅ Current subscription name and ID
- ✅ Authentication status

### Test 2: List Compliance Frameworks

```
You: What compliance frameworks do you support?
```

**Expected output:**
- GDPR (Data Protection)
- DORA (Digital Operational Resilience)
- PSD2 (Payment Services Directive)
- MiFID II (Markets in Financial Instruments)
- ISO 27001, NIS2, CRD IV/CRR, ACPR, LCB-FT

### Test 3: Show Deployment Options

```
You: What deployment strategies are available?
```

**Expected output:**
- `full-rings` - Complete hub-spoke (4 rings)
- `shared-hub` - Minimal hub + spokes (recommended for free tier)
- `minimal` - Single VNet (sandbox/dev)

### Test 4: Squad Mode Demo (only if running with `--squad`)

```
You: Delegate a security review of my current Azure setup
```

**Expected output:**
- 🔄 Delegating to Security specialist...
- 📊 Security findings
- ⚠️ Recommendations

### Exit Agent

```
You: quit
```

Expected: `Disconnecting... Goodbye!` 👋

## 🔧 Troubleshooting

### ❌ Error: "unknown option '--setting-sources'"

**Cause**: Claude Code CLI v1.x (incompatible)

**Fix:**
```bash
# Uninstall old version
npm uninstall -g @anthropic-ai/claude-code

# Install latest
npm install -g @anthropic-ai/claude-code@latest

# Verify
claude --version  # Must show 2.0.1+
```

### ❌ Error: "ImportError: attempted relative import"

**Cause**: Running from wrong directory

**Fix:**
```bash
# Check current directory
pwd

# Should be: /path/to/claude-agents/agents/azure-fsi-landingzone
# If not, navigate to it:
cd /path/to/claude-agents/agents/azure-fsi-landingzone

# Verify required files exist
ls agent.py config.yaml .env
```

### ❌ Error: "Failed to connect to Claude Agent SDK"

**Cause 1**: Missing or invalid `ANTHROPIC_API_KEY`

**Fix:**
```bash
# Check .env file exists
ls -la .env

# Verify API key format (should start with sk-ant-api03-)
grep ANTHROPIC_API_KEY .env

# Get a new key from: https://console.anthropic.com/settings/keys
```

**Cause 2**: `.env` file not loaded

**Fix:**
```bash
# Ensure .env is in same directory as agent.py
ls -la .env agent.py

# Both files should be in agents/azure-fsi-landingzone/
```

### ❌ Error: "ModuleNotFoundError: No module named 'claude_agent_sdk'"

**Cause**: Python dependencies not installed

**Fix:**
```bash
# Ensure you're in the agent directory
cd agents/azure-fsi-landingzone

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "import claude_agent_sdk"
```

### ❌ Error: "Azure authentication failed"

**Cause**: Not logged into Azure CLI

**Fix:**
```bash
# Login to Azure
az login

# Verify authentication
az account show

# Set default subscription (if multiple)
az account set --subscription "Your-Subscription-Name"
```

### ❌ Agent hangs/freezes

**Possible causes**:
1. Claude Code CLI version too old (< 2.0.1)
2. Missing/invalid `.env` file
3. Network connectivity issues
4. API key rate limit exceeded

**Debug steps:**
```bash
# 1. Check Claude Code version
claude --version  # Must be 2.0.1+

# 2. Verify .env contents (redacted)
grep -v '^#' .env | sed 's/=.*/=***REDACTED***/'

# 3. Test network connectivity
curl -I https://api.anthropic.com

# 4. Check API key is valid
# Visit: https://console.anthropic.com/settings/keys

# 5. Run with verbose logging (if supported)
python agent.py --squad  # Try with explicit flag
```

### ❌ Squad mode doesn't seem to work

**Cause**: Squad mode not enabled

**Verify:**
```bash
# Agent should show specialist sub-agents at startup
python agent.py --squad

# Expected output should mention:
# - Architect agent
# - Security agent
# - Network agent
# - DevOps agent
```

**Test squad delegation:**
```
You: What specialists are available in squad mode?
```

Expected: List of 4 specialist agents ✅

## 📚 Next Steps

Once the agent is working, explore these workflows:

### 1. **Deploy Basic Infrastructure (Solo Mode)**
```bash
python agent.py
```
```
You: Deploy a minimal FSI-compliant VNet in westeurope for dev environment
```

### 2. **Complex Deployment (Squad Mode)**
```bash
python agent.py --squad
```
```
You: Design and deploy a full hub-spoke Landing Zone with GDPR compliance for production
```
Expected: Architect coordinates with Security, Network, and DevOps specialists

### 3. **Compliance Audit**
```
You: Run a DORA compliance check on subscription [subscription-id]
```

### 4. **Customize Configuration**
Edit `config.yaml` for your organization:
```bash
nano config.yaml
```
Key sections:
- `deployment.strategy` - Choose: full-rings, shared-hub, minimal
- `azure.compliance.frameworks` - Enable/disable compliance checks
- `azure.regions` - Set preferred Azure regions

### 5. **Read Full Documentation**
- **Architecture**: [docs/azure-fsi/architecture/rings.md](../../architecture/rings.md)
- **Compliance**: [docs/azure-fsi/compliance/frameworks.md](../../compliance/frameworks.md)
- **Deployment Workflow**: [WORKFLOW.md](WORKFLOW.md) (Day 1-5 deployment guide)
- **Agent README**: [README.md](../../README.md)

## 🆘 Getting Help

- **Documentation Index**: [docs/azure-fsi/README.md](../README.md)
- **Squad Mode Guide**: [docs/azure-fsi/guides/squad-mode.md](squad-mode.md)
- **Troubleshooting**: See above or [README.md](../../README.md#troubleshooting)
- **Report Issues**: https://github.com/frntn/claude-agents/issues
- **Ask Agent**: Your agent can explain its own capabilities! Try: `You: What can you do?`

## 🎯 Version Requirements

| Component | Minimum Version | Recommended | Check Command |
|-----------|----------------|-------------|---------------|
| **Claude Code CLI** | **2.0.1** | Latest | `claude --version` |
| Python | 3.10 | 3.12 | `python --version` |
| Azure CLI | 2.50.0 | Latest | `az version` |
| Bicep | 0.24.0 | Latest | `az bicep version` |
| Node.js | 18.x | 20.x LTS | `node --version` |

**⚠️ Critical**: Claude Code CLI v2.0.1+ is required. Version 1.x will NOT work.

## 📋 Quick Reference

### Start Commands
```bash
# Solo mode (default)
python agent.py

# Squad mode (multi-agent)
python agent.py --squad

# Get help
python agent.py --help
```

### Useful Prompts
```
# Check Azure environment
You: Verify Azure CLI, Bicep, and authentication status

# List capabilities
You: What can you help me with?

# Squad mode check (only in squad mode)
You: List all specialist agents

# Compliance frameworks
You: Show all supported FSI compliance frameworks

# Generate Bicep template
You: Create a hub VNet template with Azure Firewall

# Exit
You: quit
```
