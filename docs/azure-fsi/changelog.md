# Azure FSI Landing Zone Agents - Changelog

This changelog covers updates to both the mono-agent and multi-agent squad implementations.

---

## Version 2.0.0 - Ring-Based Deployment Strategy

**Date**: October 2025

### 🎯 Major Features Added

#### 1. **Ring-Based Architecture**
- Implemented 3-tier ring deployment strategy (Ring 0, Ring 1, Ring 2)
- Each ring represents a logical layer of infrastructure
- Progressive deployment with dependency management
- See [Ring Architecture Documentation](architecture/rings.md)

#### 2. **Deployment Depth Profiles**
- **Minimal**: Essential components only for quick POCs
- **Standard**: Recommended components for production (default)
- **Advanced**: All components including optional features

#### 3. **New Agent Tools**

##### `list_deployment_rings()`
Lists all available rings with their components, dependencies, and descriptions.

##### `select_deployment_rings(rings="...")`
Select which rings to deploy:
- `rings="all"` - Deploy all rings
- `rings="ring0_foundation"` - Deploy only Ring 0
- `rings="ring0_foundation,ring2_workload"` - Deploy Ring 0 and Ring 2

##### `set_ring_depth(depth="...")`
Set deployment depth:
- `depth="minimal"` - Only mandatory components
- `depth="standard"` - Mandatory + recommended (default)
- `depth="advanced"` - All components

##### `generate_ring_deployment()`
Generates all templates and files for selected rings with chosen depth.

#### 4. **Project Organization**
- All generated assets now organized by project name
- Ring-based folder structure within each project
- Each ring has its own subfolder with components

#### 5. **Multi-Agent Squad Implementation**
- Added specialist agents: Architect, DevOps, Network, Security
- Orchestrator coordinates parallel analysis
- Expert-level recommendations across domains
- See [Multi-Agent Architecture](architecture/multi-agent.md)

---

## Ring Definitions

### **Ring 0: Foundation (Core FSI Compliance)**
- **Purpose**: Mandatory compliance and security baseline
- **Key Components**:
  - Network Core: Hub VNet, Azure Firewall, DDoS Protection
  - Security Core: Key Vault, Bastion, NSGs
  - Governance Core: Management Groups, Azure Policies
  - Monitoring Core: Log Analytics, Defender for Cloud
  - Identity Core: Entra ID, PIM, Conditional Access

### **Ring 1: Platform Services (DevOps & Shared Infrastructure)**
- **Purpose**: DevOps tooling and shared services
- **Key Components**:
  - DevOps Infrastructure: Container Registry, Artifact Storage
  - CI/CD Infrastructure: Build Agents, Pipelines
  - Shared Services: Key Vault, Storage, API Management
  - Admin Infrastructure: Admin VNet, Jump Boxes

### **Ring 2: Workload Infrastructure (Application Layer)**
- **Purpose**: Application hosting services
- **Key Components**:
  - Compute Services: Spoke VNet, App Services, AKS, VMs
  - Data Services: SQL, Cosmos DB, Storage
  - Integration: Service Bus, Event Grid, Logic Apps

---

## Version 1.0.0 - Initial Release

**Date**: September 2025

### Features
- Initial Azure FSI Landing Zone agent implementation
- Bicep + Azure Verified Modules (AVM) based templates
- European compliance focus (GDPR, DORA, PSD2, MiFID II, EBA GL)
- Default `francecentral` region deployment
- Basic template generation capabilities

---

## Bug Fixes

### 2025-10-02: Import and Startup Issues

#### 1. Import Error: Relative Imports
**Problem**: `ImportError: attempted relative import with no known parent package`

**Root Cause**: Incorrect relative imports in `shared/agents.py`

**Fix**: Updated imports to use correct paths:
```python
# Before
from .logging import get_logger
from .config import load_config

# After
from .utils.logging import get_logger
from .utils.config import load_config
```

#### 2. Tool Name Access Error
**Problem**: `AttributeError: 'SdkMcpTool' object has no attribute '__name__'`

**Root Cause**: Trying to access `__name__` on decorated tool objects

**Fix**: Use `tool_obj.name` instead:
```python
# Before
tool_name = f"mcp__agent_tools__{tool_func.__name__}"

# After
tool_name = f"mcp__agent_tools__{tool_obj.name}"
```

#### 3. Environment Variables Not Loaded
**Problem**: `ANTHROPIC_API_KEY` not being loaded from `.env` file

**Root Cause**: Missing `load_dotenv()` call in agent startup

**Fix**: Added explicit dotenv loading:
```python
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(Path(__file__).parent / ".env")
```

**Testing**: Verified by running `python agent.py` after the fix

---

## Migration Guides

### Upgrading to Ring-Based Architecture (v2.0.0)

If you were using v1.0.0 agents:

1. **Review Ring Architecture**: Read the [Ring Architecture](architecture/rings.md) documentation
2. **Choose Deployment Profile**: Decide between minimal/standard/advanced depth
3. **Update Workflows**: Adjust deployment scripts to use ring-based approach
4. **Project Organization**: Regenerate templates into the new project-based structure

### Breaking Changes in v2.0.0
- Generated file structure changed to ring-based organization
- New tools added that may require updated workflows
- Project name now required for organizing generated assets

---

*For detailed usage and guides, see the [guides directory](guides/).*
