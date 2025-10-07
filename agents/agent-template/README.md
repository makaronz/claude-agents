# Agent Template

This is a template for creating new Claude agents. Copy this directory and customize it for your specific use case.

## Structure

- `agent.py` - Main agent implementation
- `config.yaml` - Agent-specific configuration
- `tools/` - Custom MCP tools for this agent
- `README.md` - Agent documentation
- `requirements.txt` - Agent-specific dependencies

## Quick Start

1. Copy this template:
   ```bash
   cp -r agents/agent-template agents/my-new-agent
   cd agents/my-new-agent
   ```

2. Customize the configuration:
   - Edit `config.yaml` with your agent's details
   - Update `agent.py` with your implementation
   - Add any custom tools in the `tools/` directory

3. Install dependencies:
   ```bash
   uv pip sync uv.lock         # if you have a lock file
   # or bootstrap from requirements
   uv pip install -r requirements.txt
   ```

4. Run your agent:
   ```bash
   python agent.py
   ```

## Customization

- **Agent Name**: Update the `name` field in `config.yaml`
- **Tools**: Add custom MCP tools in the `tools/` directory
- **Behavior**: Modify the agent logic in `agent.py`
- **Dependencies**: Add any additional packages to `requirements.txt`
