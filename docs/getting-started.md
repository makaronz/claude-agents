# Getting Started with Claude Agents

This guide will help you get started with creating and using Claude agents built with the official Claude Agent SDK.

## Prerequisites

- Python 3.10 or higher
- Node.js (required for Claude Code CLI)
- An Anthropic API key
- Basic familiarity with Python and async programming

## Installation

1. **Clone the repository and run setup**:
   ```bash
   git clone <your-repo-url>
   cd claude-agents
   ./scripts/setup.sh
   ```

2. **Activate the virtual environment**:
   ```bash
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Claude Code CLI** (if not already installed):
   ```bash
   npm install -g @anthropic-ai/claude-code
   ```

4. **Set up your API key**:
   ```bash
   cp .env.example .env
   # Edit .env and add your ANTHROPIC_API_KEY
   ```

## Try the Example Agent

Before creating your own agent, try the example to see how it works:

```bash
cd agents/example-agent
python agent.py
```

The example agent demonstrates:
- Custom tools (status, time, text analysis)
- Interactive conversation
- Claude Agent SDK integration

## Creating Your First Agent

1. **Copy the template**:
   ```bash
   cp -r agents/agent-template agents/my-first-agent
   cd agents/my-first-agent
   ```

2. **Customize the configuration** in `config.yaml`:
   ```yaml
   name: "my-first-agent"
   description: "My first Claude agent using the SDK"
   model: "claude-sonnet-4-5"
   allowed_tools:
     - "Read"
     - "Write"
   ```

3. **Implement your agent** by editing `agent.py`:
   
   **Custom System Prompt:**
   ```python
   def get_system_prompt(self) -> Optional[str]:
       return "You are a helpful assistant specialized in..."
   ```
   
   **Add Custom Tools:**
   ```python
   @tool("my_tool", "Description", {"param": str})
   async def my_custom_tool(self, args):
       result = f"Processed: {args['param']}"
       return {"content": [{"type": "text", "text": result}]}
   
   def get_custom_tools(self) -> List[Any]:
       return [self.my_custom_tool]
   ```

4. **Run your agent**:
   ```bash
   python agent.py
   ```

## Agent Structure

```
my-agent/
├── agent.py           # Main agent class (inherits from InteractiveAgent)
├── config.yaml        # Agent configuration (model, tools, etc.)
├── requirements.txt   # Agent-specific dependencies
├── logs/              # Log files (created automatically)
└── README.md          # Agent documentation
```

## Key Concepts

### Base Classes

- **BaseClaudeAgent**: Core agent functionality with Claude Agent SDK
- **InteractiveAgent**: Adds interactive conversation capabilities

### Custom Tools

Use the `@tool` decorator to create custom MCP tools:

```python
from claude_agent_sdk import tool

@tool("tool_name", "Tool description", {"param_name": param_type})
async def my_tool(self, args):
    # Tool implementation
    return {"content": [{"type": "text", "text": "Result"}]}
```

### Configuration

Agents are configured via `config.yaml`:
- `name`: Agent name
- `model`: Claude model to use 
- `allowed_tools`: Built-in tools the agent can use
- `system_prompt`: Optional system prompt override

## Next Steps

1. **Explore the example agent** to understand capabilities
2. **Read the [Agent Development Guide](agent-guide.md)** for advanced features
3. **Check the [Claude Agent SDK documentation](https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-python)**
4. **Learn about [deployment options](deployment.md)**

## Common Issues

### Claude Code CLI Issues
```bash
# Install or update Claude Code CLI
npm install -g @anthropic-ai/claude-code

# Verify installation
claude-code --version
```

### API Key Issues
- Ensure your `.env` file has a valid `ANTHROPIC_API_KEY`
- API keys should start with `sk-ant-`
- Verify you have sufficient API credits

### Import Errors
- Make sure you're in the correct virtual environment
- Run `pip install -r requirements.txt` to install dependencies
- Check that the shared modules are accessible

### Permission Issues
- Ensure the agent directory is writable
- The `logs/` directory should be creatable by the agent

## Getting Help

- **Claude Agent SDK Docs**: https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-python
- **Example Agents**: Check the `agents/` directory for working examples
- **Issues**: Create an issue in this repository for bugs or questions