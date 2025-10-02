# Agents Documentation

This repository provides a comprehensive framework for building Claude agents using the official Claude Agent SDK. This document serves as your guide to understanding, developing, and maintaining agents within this codebase.

## Table of Contents

1. [What are Claude Agents?](#what-are-claude-agents)
2. [Agent Architecture](#agent-architecture)
3. [Creating Your First Agent](#creating-your-first-agent)
4. [Agent Development Guidelines](#agent-development-guidelines)
5. [Tool Development](#tool-development)
6. [Configuration Management](#configuration-management)
7. [Testing Your Agents](#testing-your-agents)
8. [Deployment & Production](#deployment--production)
9. [Troubleshooting](#troubleshooting)
10. [Contributing](#contributing)
    - [Documentation Requirements](#documentation-requirements)
    - [Changelog Guidelines](#changelog-documentation-optional-but-recommended)

## What are Claude Agents?

Claude agents are autonomous AI systems built on top of Claude that can:

- **Execute multi-step workflows** with planning and reasoning
- **Use tools and APIs** to interact with external systems
- **Maintain conversation context** across multiple interactions
- **Make decisions** based on available information and defined goals
- **Handle complex tasks** that require multiple capabilities

### Key Characteristics

- **Autonomous**: Can work independently with minimal human intervention
- **Tool-enabled**: Can use custom tools to extend capabilities
- **Context-aware**: Maintains state and memory across interactions
- **Configurable**: Behavior can be customized through configuration
- **Extensible**: New capabilities can be added through custom tools

## Agent Architecture

Our agent framework is built on several key components:

```
Agent Architecture
├── BaseClaudeAgent          # Core agent functionality
├── InteractiveAgent         # Conversation interface
├── Tools System            # Custom tool definitions
├── Configuration          # YAML-based settings
└── Shared Utilities      # Common functions and helpers
```

### Core Components

#### BaseClaudeAgent
The foundation class that provides:
- Claude client initialization
- Tool registration and management
- Configuration loading
- Error handling and logging
- Context management

#### InteractiveAgent
Extends BaseClaudeAgent with:
- Conversation loop management
- User input handling
- Response formatting
- Session state management

#### Tools System
- **Custom Tools**: Define specific capabilities for your agent
- **Tool Registration**: Automatic discovery and registration
- **Parameter Validation**: Type-safe tool parameters
- **Error Handling**: Graceful failure management

## Creating Your First Agent

### Step 1: Use the Agent Template

```bash
# Copy the template
cp -r agents/agent-template agents/my-new-agent
cd agents/my-new-agent
```

### Step 2: Configure Your Agent

Edit `config.yaml`:

```yaml
agent:
  name: "My New Agent"
  description: "Description of what your agent does"
  model: "claude-3-5-sonnet-20241022"
  max_tokens: 1000

tools:
  # List the tools your agent should have access to
  enabled:
    - "get_current_time"
    - "analyze_text"
    - "custom_tool"

logging:
  level: "INFO"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

### Step 3: Customize Your Agent

Edit `agent.py` to add your custom logic:

```python
from shared.agents import BaseClaudeAgent, InteractiveAgent
from claude_agent_sdk import tool
import asyncio

class MyNewAgent(BaseClaudeAgent):
    """Custom agent for specific domain tasks."""
    
    def __init__(self, config_path: str = "config.yaml"):
        super().__init__(config_path)
        self.setup_custom_tools()
    
    @tool
    def my_custom_tool(self, input_text: str) -> str:
        """
        Custom tool that processes input text.
        
        Args:
            input_text: The text to process
            
        Returns:
            Processed result
        """
        # Your custom logic here
        return f"Processed: {input_text}"
    
    async def run_custom_workflow(self, task: str):
        """Execute a custom workflow for the given task."""
        # Your workflow logic here
        pass

# Interactive mode
class MyInteractiveAgent(InteractiveAgent, MyNewAgent):
    """Interactive version of MyNewAgent."""
    pass

if __name__ == "__main__":
    agent = MyInteractiveAgent()
    asyncio.run(agent.run_interactive())
```

### Step 4: Test Your Agent

```bash
# Run your agent
python agent.py

# Or test specific functionality
python -c "
import asyncio
from agent import MyNewAgent

async def test():
    agent = MyNewAgent()
    result = await agent.my_custom_tool('test input')
    print(result)

asyncio.run(test())
"
```

## Agent Development Guidelines

### Best Practices

1. **Clear Purpose**: Each agent should have a well-defined, specific purpose
2. **Modular Design**: Break complex functionality into smaller, reusable tools
3. **Error Handling**: Implement robust error handling for all operations
4. **Documentation**: Document all tools and methods clearly
5. **Testing**: Write tests for your agent's core functionality
6. **Configuration**: Make agents configurable rather than hard-coded

### Code Organization

```
agents/your-agent/
├── agent.py           # Main agent implementation
├── config.yaml        # Agent configuration
├── tools/             # Custom tools (if many)
│   ├── __init__.py
│   ├── data_tools.py
│   └── api_tools.py
├── tests/             # Agent-specific tests
│   └── test_agent.py
└── README.md          # Agent documentation
```

### Naming Conventions

- **Agents**: Use descriptive names like `DataAnalysisAgent`, `CustomerServiceAgent`
- **Tools**: Use verb-noun format like `analyze_sentiment`, `fetch_weather_data`
- **Methods**: Use clear, descriptive names with proper async/await patterns
- **Variables**: Use snake_case for variables and functions

## Tool Development

### Creating Custom Tools

Tools are the building blocks of agent capabilities. Here's how to create effective tools:

```python
from claude_agent_sdk import tool
from typing import List, Dict, Optional

@tool
def analyze_data(data: List[Dict], analysis_type: str = "summary") -> Dict:
    """
    Analyze a dataset and return insights.
    
    Args:
        data: List of dictionaries containing the data to analyze
        analysis_type: Type of analysis to perform ("summary", "trends", "anomalies")
        
    Returns:
        Dictionary containing analysis results
        
    Raises:
        ValueError: If data format is invalid
        NotImplementedError: If analysis_type is not supported
    """
    if not data:
        raise ValueError("Data cannot be empty")
    
    if analysis_type not in ["summary", "trends", "anomalies"]:
        raise NotImplementedError(f"Analysis type '{analysis_type}' not supported")
    
    # Your analysis logic here
    result = {
        "type": analysis_type,
        "data_points": len(data),
        "results": {}
    }
    
    return result
```

### Tool Design Principles

1. **Single Responsibility**: Each tool should do one thing well
2. **Clear Interface**: Use type hints and descriptive parameter names
3. **Error Handling**: Handle edge cases gracefully
4. **Documentation**: Provide clear docstrings with examples
5. **Validation**: Validate inputs before processing
6. **Idempotency**: Tools should produce consistent results for the same inputs

### Common Tool Patterns

#### Data Processing Tools
```python
@tool
def process_csv_data(file_path: str, operation: str) -> Dict:
    """Process CSV data with specified operation."""
    pass

@tool
def filter_data(data: List[Dict], criteria: Dict) -> List[Dict]:
    """Filter data based on criteria."""
    pass
```

#### API Integration Tools
```python
@tool
def fetch_api_data(endpoint: str, params: Optional[Dict] = None) -> Dict:
    """Fetch data from external API."""
    pass

@tool
def send_notification(message: str, channel: str) -> bool:
    """Send notification to specified channel."""
    pass
```

#### File Operations Tools
```python
@tool
def read_file_content(file_path: str) -> str:
    """Read and return file content."""
    pass

@tool
def save_results(data: Dict, output_path: str) -> bool:
    """Save results to file."""
    pass
```

## Configuration Management

### Configuration Structure

Each agent uses a YAML configuration file with the following structure:

```yaml
# Agent Identity and Behavior
agent:
  name: "Agent Name"
  description: "What the agent does"
  model: "claude-3-5-sonnet-20241022"  # Claude model to use
  max_tokens: 1000                     # Response length limit
  temperature: 0.7                     # Response creativity (0.0-1.0)

# Tool Configuration
tools:
  enabled:
    - "tool_name_1"
    - "tool_name_2"
  
  permissions:
    file_access: true
    network_access: false
    
  settings:
    timeout: 30
    retry_attempts: 3

# Logging Configuration
logging:
  level: "INFO"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file: "logs/agent.log"

# Custom Configuration
custom:
  api_endpoints:
    primary: "https://api.example.com"
    fallback: "https://backup-api.example.com"
  
  data_sources:
    - "source1.csv"
    - "source2.json"
```

### Environment Variables

Use environment variables for sensitive configuration:

```bash
# .env file
ANTHROPIC_API_KEY=your_api_key_here
DATABASE_URL=postgresql://user:pass@localhost/db
API_SECRET_KEY=your_secret_key
```

Access in your agent:

```python
import os
from shared.utils.config import load_config

class MyAgent(BaseClaudeAgent):
    def __init__(self, config_path: str = "config.yaml"):
        super().__init__(config_path)
        self.api_key = os.getenv("API_SECRET_KEY")
        self.db_url = os.getenv("DATABASE_URL")
```

## Testing Your Agents

### Test Structure

Create comprehensive tests for your agents:

```python
# tests/test_my_agent.py
import pytest
import asyncio
from unittest.mock import Mock, patch
from agents.my_agent.agent import MyNewAgent

class TestMyNewAgent:
    
    @pytest.fixture
    def agent(self):
        """Create agent instance for testing."""
        return MyNewAgent("test_config.yaml")
    
    def test_agent_initialization(self, agent):
        """Test agent initializes correctly."""
        assert agent.config is not None
        assert agent.client is not None
    
    @pytest.mark.asyncio
    async def test_custom_tool(self, agent):
        """Test custom tool functionality."""
        result = await agent.my_custom_tool("test input")
        assert "Processed" in result
    
    @pytest.mark.asyncio
    async def test_error_handling(self, agent):
        """Test error handling in tools."""
        with pytest.raises(ValueError):
            await agent.my_custom_tool("")
    
    @patch('external_api.call')
    @pytest.mark.asyncio
    async def test_api_integration(self, mock_api, agent):
        """Test API integration with mocking."""
        mock_api.return_value = {"status": "success"}
        result = await agent.call_external_api()
        assert result["status"] == "success"
```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_my_agent.py

# Run with coverage
pytest --cov=agents tests/

# Run tests for specific agent
pytest tests/test_my_agent.py -v
```

### Test Configuration

Create separate test configurations:

```yaml
# test_config.yaml
agent:
  name: "Test Agent"
  model: "claude-3-haiku-20240307"  # Faster model for tests
  max_tokens: 100

logging:
  level: "DEBUG"
  
tools:
  enabled:
    - "test_tool"
```

## Deployment & Production

### Production Checklist

Before deploying your agent to production:

- [ ] **Security Review**: Ensure no sensitive data is logged
- [ ] **Error Handling**: All edge cases are handled gracefully
- [ ] **Rate Limiting**: API calls are properly rate limited
- [ ] **Monitoring**: Logging and metrics are in place
- [ ] **Configuration**: Production config is separate from development
- [ ] **Testing**: All tests pass and coverage is adequate
- [ ] **Documentation**: README and usage instructions are complete

### Deployment Options

#### Local Deployment
```bash
# Set production environment
export ENVIRONMENT=production

# Install dependencies
pip install -r requirements.txt

# Run agent
python agents/my-agent/agent.py
```

#### Docker Deployment
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "agents/my-agent/agent.py"]
```

#### Cloud Deployment
Consider platforms like:
- **AWS Lambda**: For event-driven agents
- **Google Cloud Run**: For containerized agents
- **Heroku**: For simple web-based agents
- **Railway**: For quick deployments

### Monitoring and Logging

Implement proper monitoring:

```python
import logging
from shared.utils.logger import setup_logger

class ProductionAgent(BaseClaudeAgent):
    def __init__(self, config_path: str = "config.yaml"):
        super().__init__(config_path)
        self.logger = setup_logger("production_agent")
    
    async def execute_task(self, task: str):
        self.logger.info(f"Starting task: {task}")
        try:
            result = await self.process_task(task)
            self.logger.info(f"Task completed successfully: {task}")
            return result
        except Exception as e:
            self.logger.error(f"Task failed: {task}, Error: {str(e)}")
            raise
```

## Troubleshooting

### Common Issues

#### 1. Agent Won't Start
**Symptoms**: Import errors, configuration errors
**Solutions**:
- Check Python path and virtual environment
- Verify all dependencies are installed
- Validate configuration file syntax
- Check environment variables

#### 2. Tools Not Working
**Symptoms**: Tools not found, permission errors
**Solutions**:
- Verify tool registration in config
- Check tool permissions
- Validate tool parameters and types
- Review tool implementation for errors

#### 3. API Rate Limiting
**Symptoms**: 429 errors, timeout issues
**Solutions**:
- Implement exponential backoff
- Add rate limiting to tool calls
- Use appropriate model for task complexity
- Cache responses when possible

#### 4. Memory Issues
**Symptoms**: Out of memory errors, slow performance
**Solutions**:
- Optimize conversation context management
- Implement context truncation
- Use streaming for large responses
- Monitor memory usage

### Debug Mode

Enable debug mode for detailed logging:

```python
# Set debug configuration
import logging
logging.basicConfig(level=logging.DEBUG)

# Or in config.yaml
logging:
  level: "DEBUG"
```

### Performance Optimization

- **Model Selection**: Use appropriate model for task complexity
- **Context Management**: Keep conversation context focused and relevant
- **Tool Efficiency**: Optimize tool implementations for speed
- **Caching**: Cache expensive operations when possible
- **Async Operations**: Use async/await for I/O operations

## Contributing

### Contributing Guidelines

When contributing to this repository:

1. **Fork and Branch**: Create a feature branch from main
2. **Follow Standards**: Use existing code style and patterns
3. **Add Tests**: Include tests for new functionality
4. **Document Changes**: Update relevant documentation (see below)
5. **Test Thoroughly**: Ensure all tests pass
6. **Submit PR**: Create a detailed pull request

### Documentation Requirements

**⚠️ IMPORTANT**: When making changes to agents, tools, or infrastructure, you **MUST** update the relevant documentation.

#### What to Update

Update documentation when you:
- **Fix bugs**: Document the issue and solution in troubleshooting sections
- **Add features**: Update README, usage examples, and configuration docs
- **Change dependencies**: Update requirements.txt and installation instructions
- **Modify APIs**: Update tool documentation and code examples
- **Update prerequisites**: Update all installation and setup guides
- **Change configuration**: Update config examples and documentation

#### Required Documentation Updates

For each change, update these files as relevant:

1. **Agent-specific README** (`agents/your-agent/README.md`)
   - Prerequisites and version requirements
   - Installation instructions
   - Configuration options
   - Usage examples
   - Troubleshooting section

2. **WORKFLOW.md** (if applicable)
   - Step-by-step deployment guides
   - Command examples
   - Expected outputs
   - Troubleshooting for workflow-specific issues

3. **requirements.txt**
   - Pin minimum versions for dependencies
   - Add comments for critical version requirements
   - Document external tool dependencies (e.g., Claude Code CLI)

4. **Root README.md**
   - Update global prerequisites if they change
   - Update agent list if adding/removing agents
   - Update version requirements table

5. **QUICKSTART.md** (if it exists)
   - Quick installation steps
   - Common troubleshooting for new users

#### Changelog Documentation (Optional but Recommended)

For significant changes, bug fixes, or breaking changes, create or update a changelog:

**Create**: `CHANGELOG_<TOPIC>.md` or add to existing `CHANGELOG.md`

Include:
- **Date** of the change
- **Issue description** (what was broken/missing)
- **Root cause** (why it happened)
- **Fix details** (what was changed, with code snippets)
- **Testing** (how to verify the fix)
- **Migration guide** (for breaking changes)

**Example**: See [`CHANGELOG_FIXES.md`](CHANGELOG_FIXES.md) for reference.

#### Documentation Checklist

Before submitting your PR, verify:

- [ ] All affected README files updated
- [ ] Installation/setup instructions reflect new requirements
- [ ] Troubleshooting section includes common errors (if applicable)
- [ ] Version requirements documented (minimum and tested versions)
- [ ] Code examples updated and tested
- [ ] Configuration examples valid
- [ ] Changelog created (for significant changes)
- [ ] Related documentation cross-referenced

#### Documentation Quality Standards

Good documentation should:
- ✅ Be **concise** and **scannable** (use bullet points, tables, checklists)
- ✅ Include **working code examples** (test them!)
- ✅ Provide **troubleshooting** for common issues
- ✅ Specify **exact versions** for dependencies
- ✅ Use **clear section headers** for easy navigation
- ✅ Include **before/after** examples for fixes
- ✅ Provide **verification steps** to test the changes

#### When Changelog is Required

Create/update changelog for:
- 🔴 **Breaking changes** (API changes, dependency updates)
- 🟡 **Bug fixes** (especially if users may encounter the bug)
- 🟢 **New features** (significant new capabilities)
- 🔵 **Security fixes** (any security-related changes)
- ⚪ **Infrastructure changes** (CI/CD, build process)

#### Example Documentation Update

```markdown
# Example: Adding a new tool to an agent

## Files to Update

1. agents/my-agent/README.md
   - Add tool to "Available Tools" section
   - Add usage example
   - Add any prerequisites

2. agents/my-agent/config.yaml
   - Add tool to enabled tools list (if needed)

3. AGENTS.md (this file)
   - Add tool pattern to "Common Tool Patterns" (if novel)

4. CHANGELOG.md or CHANGELOG_FEATURES.md
   - Document what the tool does
   - Provide usage example
   - Note any new dependencies
```

### Code Style

- Follow PEP 8 for Python code style
- Use type hints for all function parameters and returns
- Write clear, descriptive commit messages
- Include docstrings for all classes and methods
- Use meaningful variable and function names

### Review Process

All contributions go through:
1. Automated testing (CI/CD)
2. Code review by maintainers
3. Documentation review
4. Security review for production code

### Getting Help

- **Issues**: Use GitHub issues for bugs and feature requests
- **Discussions**: Use GitHub discussions for questions
- **Documentation**: Check existing documentation first
- **Examples**: Review example agents for patterns

## Resources

### Additional Documentation

- [Claude Agent SDK Documentation](https://github.com/anthropics/claude-agent-sdk-python)
- [Claude API Documentation](https://docs.anthropic.com/)
- [MCP (Model Context Protocol) Specification](https://spec.modelcontextprotocol.io/)

### Example Use Cases

- **Customer Service**: Automated support with escalation
- **Data Analysis**: Process and analyze datasets
- **Content Creation**: Generate articles, reports, summaries
- **Research Assistant**: Gather and synthesize information
- **Code Review**: Analyze code quality and suggest improvements
- **Project Management**: Task tracking and status updates

### Community

- Join the Claude developers community
- Share your agents and get feedback
- Contribute to open source agent tools
- Participate in agent development discussions

---

*This documentation is maintained by the repository contributors. For the most up-to-date information, please check the repository's main documentation and the official Claude Agent SDK documentation.*