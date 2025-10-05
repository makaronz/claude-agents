# Agent Development Guide

This guide covers advanced topics for developing Claude agents.

## Agent Architecture

### Base Agent Class

All agents should inherit from a base structure that provides:
- Configuration management
- Logging setup
- Error handling
- Message processing pipeline

### Configuration System

Agents use a hierarchical configuration system:
1. Default values in code
2. Agent-specific `config.yaml`
3. Environment variables (highest priority)

### Logging

The shared logging utility provides:
- Structured logging with timestamps
- Log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- File and console output
- Automatic log rotation

## Custom Tools

### Creating MCP Tools

1. **Define your tool** in `tools/__init__.py`:
   ```python
   def my_custom_tool(param1: str, param2: int) -> Dict[str, Any]:
       \"\"\"My custom tool description.\"\"\"
       # Tool implementation
       return {"result": "success"}
   ```

2. **Register the tool**:
   ```python
   def get_available_tools() -> List[Dict[str, Any]]:
       return [
           {
               "name": "my_custom_tool",
               "description": "Description of what the tool does",
               "parameters": {
                   "param1": {"type": "string", "description": "First parameter"},
                   "param2": {"type": "integer", "description": "Second parameter"}
               },
               "function": my_custom_tool
           }
       ]
   ```

### Tool Best Practices

- **Clear descriptions**: Tools should have clear, descriptive names and documentation
- **Type hints**: Use proper type hints for parameters and return values
- **Error handling**: Handle errors gracefully and return meaningful error messages
- **Validation**: Validate input parameters before processing

## Agent Communication

### Message Processing Pipeline

1. **Input validation**: Check message format and length
2. **Context preparation**: Prepare context for the Claude API
3. **API call**: Send request to Claude
4. **Response processing**: Format and validate the response
5. **Output generation**: Return the processed response

### Async Best Practices

- Use `async/await` for I/O operations
- Handle timeouts and connection errors
- Implement proper cleanup in finally blocks

## Testing

### Unit Tests

Create unit tests for your agent logic:
```python
import pytest
from your_agent import YourAgent

@pytest.mark.asyncio
async def test_process_message():
    agent = YourAgent(test_config)
    response = await agent.process_message("test message")
    assert response is not None
```

### Integration Tests

Test the full agent workflow:
```python
@pytest.mark.asyncio
async def test_full_workflow():
    agent = YourAgent(test_config)
    await agent.initialize()
    response = await agent.process_message("Hello")
    assert "Hello" in response
```

## Performance Optimization

### Caching

Implement caching for expensive operations:
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def expensive_operation(input_data: str) -> str:
    # Expensive computation
    return result
```

### Connection Pooling

Use connection pooling for external APIs:
```python
import aiohttp

async with aiohttp.ClientSession() as session:
    async with session.get(url) as response:
        data = await response.json()
```

### Memory Management

- Clean up resources in `__del__` methods
- Use weak references where appropriate
- Monitor memory usage in long-running agents

## Deployment Considerations

### Environment Variables

Always use environment variables for:
- API keys and secrets
- URLs and endpoints
- Feature flags
- Configuration overrides

### Error Handling

Implement comprehensive error handling:
```python
try:
    result = await api_call()
except APIError as e:
    logger.error(f"API error: {e}")
    return error_response(e)
except Exception as e:
    logger.exception(f"Unexpected error: {e}")
    return generic_error_response()
```

### Monitoring

Add monitoring and metrics:
- Request/response times
- Error rates
- API usage
- Resource consumption

## Advanced Features

### Multi-Agent Coordination

For complex scenarios involving multiple agents:
- Use message queues for communication
- Implement coordination protocols
- Handle state synchronization

### Streaming Responses

For real-time interactions:
```python
async def stream_response(self, message: str):
    async for chunk in self.claude_client.stream(message):
        yield chunk
```

### Plugin System

Create a plugin architecture:
```python
class PluginManager:
    def __init__(self):
        self.plugins = []
    
    def register_plugin(self, plugin):
        self.plugins.append(plugin)
    
    async def execute_plugins(self, context):
        for plugin in self.plugins:
            await plugin.execute(context)
```