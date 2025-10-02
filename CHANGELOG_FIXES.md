# Changelog - Bug Fixes and Documentation Updates

**Date**: 2025-10-02  
**Issue**: Agent startup failure due to import errors and Claude Code CLI version incompatibility

## Issues Fixed

### 1. Import Error: Relative Imports
**Problem**: `ImportError: attempted relative import with no known parent package`

**Root Cause**: Incorrect relative imports in `shared/agents.py`

**Fix**: [shared/agents.py](shared/agents.py)
```python
# Before
from .logging import get_logger
from .config import load_config

# After
from .utils.logging import get_logger
from .utils.config import load_config
```

### 2. Tool Name Access Error
**Problem**: `AttributeError: 'SdkMcpTool' object has no attribute '__name__'`

**Root Cause**: Trying to access `__name__` on decorated tool objects

**Fix**: [shared/agents.py](shared/agents.py:93-96)
```python
# Before
tool_name = f"mcp__agent_tools__{tool_func.__name__}"

# After
tool_name = f"mcp__agent_tools__{tool_obj.name}"
```

### 3. Environment Variables Not Loaded
**Problem**: `ANTHROPIC_API_KEY` not being loaded from `.env` file

**Root Cause**: Missing `load_dotenv()` call in agent startup

**Fix**: [agents/azure-fsi-landingzone/agent.py](agents/azure-fsi-landingzone/agent.py:19-20)
```python
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(Path(__file__).parent / ".env")
```

### 4. Claude Code CLI Version Incompatibility
**Problem**: `error: unknown option '--setting-sources'`

**Root Cause**: 
- User had Claude Code CLI v1.0.64 (old)
- `claude-agent-sdk` v0.1.0 requires Claude Code CLI v2.0.1+ with `--setting-sources` support

**Fix**: Upgraded Claude Code CLI
```bash
npm install -g @anthropic-ai/claude-code@latest
# Updated from 1.0.64 to 2.0.1
```

### 5. Path Configuration
**Problem**: Incorrect sys.path manipulation for imports

**Fix**: [agents/azure-fsi-landingzone/agent.py](agents/azure-fsi-landingzone/agent.py:22-23)
```python
# Before
sys.path.append(str(Path(__file__).parent.parent.parent / "shared"))
from agents import InteractiveAgent

# After
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from shared.agents import InteractiveAgent
```

## Documentation Updates

### 1. WORKFLOW.md
**Added**:
- Claude Code CLI installation step (v2.0.1+ requirement)
- `.env` file configuration instructions
- Comprehensive troubleshooting section with 6 common errors

**Location**: [agents/azure-fsi-landingzone/WORKFLOW.md](agents/azure-fsi-landingzone/WORKFLOW.md)

### 2. README.md
**Updated**:
- Prerequisites section with Claude Code CLI requirement
- Installation steps with `.env` configuration
- Version requirements table
- Verification steps

**Location**: [agents/azure-fsi-landingzone/README.md](agents/azure-fsi-landingzone/README.md)

### 3. requirements.txt
**Updated**:
- Pinned minimum versions for all dependencies
- Added comment about Claude Code CLI requirement
- Added installation instructions in comments

**Location**: [agents/azure-fsi-landingzone/requirements.txt](agents/azure-fsi-landingzone/requirements.txt)

### 4. QUICKSTART.md (New)
**Created**: Quick start guide with:
- Prerequisites checklist
- 5-minute installation steps
- First interaction examples
- Troubleshooting for 4 common errors
- Version requirements table

**Location**: [agents/azure-fsi-landingzone/QUICKSTART.md](agents/azure-fsi-landingzone/QUICKSTART.md)

### 5. Root README.md
**Updated**:
- Requirements section with Claude Code CLI v2.0.1+ requirement
- Added warning about version compatibility

**Location**: [README.md](README.md)

## Version Requirements (Updated)

| Component | Minimum Version | Installed/Tested |
|-----------|----------------|------------------|
| **Claude Code CLI** | **2.0.1** | 2.0.1 ✅ |
| claude-agent-sdk | 0.1.0 | 0.1.0 ✅ |
| Python | 3.10 | 3.12.10 ✅ |
| Node.js | 18.x | 23.11.0 ✅ |
| Azure CLI | 2.50.0 | Latest ✅ |
| Bicep | 0.24.0 | Latest ✅ |

## Testing

### Verification Steps
```bash
# 1. Check Claude Code version
claude --version
# Output: 2.0.1 (Claude Code)

# 2. Verify agent starts successfully
cd agents/azure-fsi-landingzone
python agent.py
# Output: Agent banner with "Connected to Claude Agent SDK"

# 3. Test quit command
echo "quit" | python agent.py
# Output: Graceful shutdown with "Goodbye!"
```

### Test Results
✅ Agent starts without errors  
✅ SDK connects successfully  
✅ Agent accepts commands  
✅ Graceful shutdown works  

## Breaking Changes

None - all fixes are backward compatible within the same major version.

## Migration Guide

For users with old installations:

1. **Update Claude Code CLI**:
   ```bash
   npm install -g @anthropic-ai/claude-code@latest
   ```

2. **Pull latest code**:
   ```bash
   git pull origin main
   ```

3. **Create .env file** (if you were using environment variables):
   ```bash
   cd agents/azure-fsi-landingzone
   cp .env.example .env
   vim .env  # Add your ANTHROPIC_API_KEY
   ```

4. **Test**:
   ```bash
   python agent.py
   ```

## Lessons Learned

1. **Always specify minimum versions** in requirements.txt for critical dependencies
2. **Document external tool requirements** (like Claude Code CLI) prominently
3. **Version compatibility matters** - SDKs and CLIs must be in sync
4. **Environment variable loading** should be explicit, not implicit
5. **Relative imports** need careful handling in multi-level package structures

## References

- Claude Agent SDK: https://github.com/anthropics/claude-agent-sdk-python
- Claude Code CLI: https://www.npmjs.com/package/@anthropic-ai/claude-code
- Issue Discussion: In-session troubleshooting (2025-10-02)
