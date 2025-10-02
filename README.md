# Claude Agents Repository

A collection of Claude agents built using the Claude Agent SDK and Model Context Protocol (MCP).

## Repository Structure

```
claude-agents/
├── agents/                 # Individual agent implementations
│   ├── agent-template/     # Template for new agents
│   └── example-agent/      # Example agent implementation
├── shared/                 # Shared utilities and components
│   ├── utils/             # Common utility functions
│   ├── tools/             # Reusable MCP tools
│   └── configs/           # Shared configuration files
├── docs/                  # Documentation
│   ├── getting-started.md # Getting started guide
│   ├── agent-guide.md     # How to create agents
│   └── deployment.md     # Deployment instructions
├── scripts/               # Build and deployment scripts
├── tests/                 # Test files
└── examples/              # Example implementations and demos
```

## Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd claude-agents
   ```

2. **Set up the environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Create your first agent**
   ```bash
   cp -r agents/agent-template agents/my-first-agent
   cd agents/my-first-agent
   # Edit the configuration and implementation files
   ```

## Available Agents

<!-- List your agents here as you create them -->
- **agent-template**: Template for creating new agents
- **example-agent**: Basic example showing agent structure

## Contributing

1. Use the `agent-template` as a starting point for new agents
2. Follow the established directory structure
3. Add documentation for your agents
4. Include tests for your implementations

## Requirements

- Python 3.8+
- Claude Agent SDK
- Model Context Protocol (MCP) support

## License

[Add your license information here]