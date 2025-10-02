# Getting Started with Claude Agents

This guide will help you get started with creating and using Claude agents in this repository.

## Prerequisites

- Python 3.8 or higher
- An Anthropic API key
- Basic familiarity with Python and async programming

## Installation

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone <your-repo-url>
   cd claude-agents
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env and add your Anthropic API key
   ```

## Creating Your First Agent

1. **Copy the template**:
   ```bash
   cp -r agents/agent-template agents/my-first-agent
   cd agents/my-first-agent
   ```

2. **Customize the configuration**:
   Edit `config.yaml` to set your agent's name and behavior:
   ```yaml
   name: "my-first-agent"
   description: "My first Claude agent"
   ```

3. **Implement your agent logic**:
   Edit `agent.py` and customize the `process_message` method:
   ```python
   async def process_message(self, message: str) -> str:
       # Your custom logic here
       return f"I processed: {message}"
   ```

4. **Run your agent**:
   ```bash
   python agent.py
   ```

## Directory Structure

```
your-agent/
├── agent.py           # Main agent implementation
├── config.yaml        # Agent configuration
├── requirements.txt   # Agent-specific dependencies
├── tools/             # Custom MCP tools
│   └── __init__.py
├── logs/              # Log files (created automatically)
└── README.md          # Agent documentation
```

## Next Steps

- Read the [Agent Development Guide](agent-guide.md) for advanced features
- Check out the [examples](../examples/) directory for inspiration
- Learn about [deployment options](deployment.md)

## Common Issues

### API Key Issues
If you get API key errors, make sure:
- Your `.env` file contains a valid `ANTHROPIC_API_KEY`
- The API key starts with `sk-ant-`
- You have sufficient API credits

### Import Errors
If you get import errors:
- Make sure you're in the correct virtual environment
- Install dependencies with `pip install -r requirements.txt`
- Check that the shared utilities are in the correct path

### Permission Errors
If you get permission errors when creating log files:
- Make sure the agent directory is writable
- Check that the `logs/` directory can be created