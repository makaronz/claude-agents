# Example Agent

This is a concrete example of a Claude agent that demonstrates the basic structure and functionality.

## What This Agent Does

The example agent is a simple conversational assistant that:
- Responds to user messages with helpful information
- Demonstrates proper logging and configuration
- Shows how to use the shared utilities
- Provides examples of custom tools

## Features

- ✅ Basic conversation handling
- ✅ Structured logging
- ✅ Configuration management
- ✅ Error handling
- ✅ Custom tool integration

## Usage

1. **Set up the environment** (from the repository root):
   ```bash
   ./scripts/setup.sh
   source venv/bin/activate
   ```

2. **Configure your API key** in `.env`:
   ```
   ANTHROPIC_API_KEY=your_api_key_here
   ```

3. **Run the agent**:
   ```bash
   cd agents/example-agent
   python agent.py
   ```

4. **Interact with the agent**:
   - Type messages and get responses
   - Try commands like "help" or "status"
   - Type "quit" to exit

## Customization

This example agent can be used as a starting point for more complex agents. You can:
- Modify the conversation logic in `process_message()`
- Add new tools in the `tools/` directory  
- Update the configuration in `config.yaml`
- Add specialized functionality for your use case