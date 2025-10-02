# Claude Agents Repository

A collection of Claude agents built using the official **Claude Agent SDK** for Python.

## Repository Structure

```
claude-agents/
├── agents/                 # Individual agent implementations
│   ├── agent-template/     # Template for new agents
│   └── example-agent/      # Example agent with custom tools
├── shared/                 # Shared utilities and base classes
│   ├── agents.py          # BaseClaudeAgent and InteractiveAgent classes
│   ├── utils/             # Common utility functions
│   └── configs/           # Shared configuration files
├── docs/                  # Documentation
│   ├── getting-started.md # Getting started guide
│   ├── agent-guide.md     # How to create agents
│   └── deployment.md     # Deployment instructions
├── scripts/               # Build and deployment scripts
├── tests/                 # Test files
└── examples/              # Example implementations and demos
```

## Features

✨ **Built with Claude Agent SDK**: Uses the official Python SDK for Claude agents  
🛠️ **Custom Tools**: Easy creation of custom MCP tools using decorators  
🤖 **Interactive Agents**: Ready-to-use interactive conversation interfaces  
⚙️ **Configuration Management**: YAML-based configuration with environment overrides  
📝 **Comprehensive Logging**: Structured logging with file and console output  
🎯 **Type Safety**: Full type hints and validation  

## Quick Start

1. **Clone and set up the environment**
   ```bash
   git clone <repository-url>
   cd claude-agents
   ./scripts/setup.sh
   source venv/bin/activate
   ```

2. **Configure your API key**
   ```bash
   cp .env.example .env
   # Edit .env and add your ANTHROPIC_API_KEY
   ```

3. **Try the example agent**
   ```bash
   cd agents/example-agent
   python agent.py
   ```

4. **Create your first custom agent**
   ```bash
   cp -r agents/agent-template agents/my-first-agent
   cd agents/my-first-agent
   # Edit config.yaml and agent.py
   python agent.py
   ```

## Available Agents

- **🏗️ agent-template**: Complete template for creating new agents with custom tools
- **🎯 example-agent**: Feature-rich example showing Claude Agent SDK capabilities
- **🏦 azure-fsi-landingzone**: Azure Financial Services Industry Landing Zone deployment agent with European compliance (GDPR, DORA, PSD2, MiFID II)
- **📋 azure-compliance-checker**: Automated compliance validation agent for French FSI regulations (ACPR, CRD IV/CRR, LCB-FT, RGPD, ISO 27001, DORA, NIS2)

## Requirements

- **Python 3.10+**
- **Node.js 18+** (for Claude Code CLI)
- **Claude Code CLI v2.0.1+**: `npm install -g @anthropic-ai/claude-code@latest` ⚠️ **REQUIRED**
- **Claude Agent SDK v0.1.0+**: `pip install claude-agent-sdk>=0.1.0`
- **Anthropic API key** (from https://console.anthropic.com)

**Important**: Claude Code CLI v2.0.1+ is required for the claude-agent-sdk to work. Version 1.x is not compatible.

## Key Components

### BaseClaudeAgent
Base class providing:
- Claude Agent SDK integration
- Configuration management  
- Custom tool support
- Async context manager support

### InteractiveAgent
Extends BaseClaudeAgent with:
- Interactive conversation loops
- Message display formatting
- Command-line interface

### Custom Tools
Create custom tools using the `@tool` decorator:

```python
from claude_agent_sdk import tool

@tool("my_tool", "Description of what it does", {"param": str})
async def my_custom_tool(args):
    return {"content": [{"type": "text", "text": "Result"}]}
```

## Contributing

1. Use the `agent-template` as a starting point
2. Follow the established directory structure  
3. Add comprehensive documentation
4. Include tests for custom functionality
5. Use type hints throughout

## License

[Add your license information here]