"""
Base agent class using the Claude Agent SDK.

This provides a foundation for creating Claude agents with proper SDK integration,
configuration management, and tool support.
"""

import asyncio
from typing import Dict, Any, List, Optional, AsyncIterator
from pathlib import Path
import yaml

from claude_agent_sdk import (
    ClaudeSDKClient,
    ClaudeAgentOptions,
    AssistantMessage,
    UserMessage,
    ResultMessage,
    TextBlock,
    ToolUseBlock,
    ToolResultBlock,
    create_sdk_mcp_server,
    tool
)

from .utils.logging import get_logger
from .utils.config import load_config


class BaseClaudeAgent:
    """
    Base class for Claude agents using the official Claude Agent SDK.
    
    This class provides a foundation for creating agents with:
    - Claude Agent SDK integration
    - Configuration management
    - Custom tool support
    - Proper error handling and logging
    """
    
    def __init__(self, config_dir: Optional[Path] = None):
        """
        Initialize the base agent.
        
        Args:
            config_dir: Directory containing agent configuration files
        """
        self.config_dir = config_dir or Path.cwd()
        self.config = load_config(self.config_dir)
        self.logger = get_logger(self.__class__.__name__)
        
        # Load agent-specific config if available
        self.agent_config = self._load_agent_config()
        
        # Initialize client as None - will be created when needed
        self.client: Optional[ClaudeSDKClient] = None
        self.is_connected = False
        
        self.logger.info(f"Initialized {self.__class__.__name__}")
    
    def _load_agent_config(self) -> Dict[str, Any]:
        """Load agent-specific configuration from config.yaml."""
        config_file = self.config_dir / "config.yaml"
        if config_file.exists():
            with open(config_file, 'r') as f:
                return yaml.safe_load(f) or {}
        return {}
    
    def get_agent_options(self) -> ClaudeAgentOptions:
        """
        Get Claude Agent options for this agent.
        
        Override this method to customize agent behavior.
        
        Returns:
            ClaudeAgentOptions configured for this agent
        """
        # Get custom tools if available
        mcp_servers = {}
        custom_tools = self.get_custom_tools()
        if custom_tools:
            server = create_sdk_mcp_server(
                name=self.agent_config.get('name', 'agent-tools'),
                version=self.agent_config.get('version', '1.0.0'),
                tools=custom_tools
            )
            mcp_servers['agent_tools'] = server
        
        # Build allowed tools list
        allowed_tools = self.agent_config.get('allowed_tools', [])
        if custom_tools:
            # Add MCP tool names for custom tools
            for tool_obj in custom_tools:
                # SdkMcpTool objects have a 'name' attribute
                tool_name = f"mcp__agent_tools__{tool_obj.name}"
                allowed_tools.append(tool_name)
        
        return ClaudeAgentOptions(
            system_prompt=self.get_system_prompt(),
            allowed_tools=allowed_tools,
            mcp_servers=mcp_servers,
            max_turns=self.agent_config.get('max_turns'),
            cwd=self.config_dir,
            model=self.agent_config.get('model'),
            permission_mode=self.agent_config.get('permission_mode', 'default'),
            setting_sources=None  # Disable setting sources to avoid CLI incompatibility
        )
    
    def get_system_prompt(self) -> Optional[str]:
        """
        Get the system prompt for this agent.
        
        Override this method to provide a custom system prompt.
        
        Returns:
            System prompt string or None
        """
        return self.agent_config.get('system_prompt')
    
    def get_custom_tools(self) -> List[Any]:
        """
        Get custom tools for this agent.
        
        Override this method to provide custom MCP tools.
        
        Returns:
            List of tool functions decorated with @tool
        """
        return []
    
    async def connect(self) -> None:
        """Connect to the Claude Agent SDK."""
        if self.is_connected:
            return
        
        options = self.get_agent_options()
        self.client = ClaudeSDKClient(options)
        await self.client.connect()
        self.is_connected = True
        self.logger.info("Connected to Claude Agent SDK")
    
    async def disconnect(self) -> None:
        """Disconnect from the Claude Agent SDK."""
        if self.client and self.is_connected:
            await self.client.disconnect()
            self.is_connected = False
            self.logger.info("Disconnected from Claude Agent SDK")
    
    async def query(self, prompt: str) -> AsyncIterator[Any]:
        """
        Send a query to Claude and yield response messages.
        
        Args:
            prompt: The prompt to send to Claude
            
        Yields:
            Response messages from Claude
        """
        if not self.is_connected:
            await self.connect()
        
        self.logger.info(f"Sending query: {prompt[:100]}...")
        
        await self.client.query(prompt)
        
        async for message in self.client.receive_response():
            yield message
    
    async def process_message(self, message: str) -> str:
        """
        Process a single message and return a text response.
        
        This is a convenience method that handles the most common use case
        of sending a message and getting a text response back.
        
        Args:
            message: Input message to process
            
        Returns:
            Text response from Claude
        """
        response_parts = []
        
        async for msg in self.query(message):
            if isinstance(msg, AssistantMessage):
                for block in msg.content:
                    if isinstance(block, TextBlock):
                        response_parts.append(block.text)
        
        return "\n".join(response_parts)
    
    async def __aenter__(self):
        """Support for async context manager."""
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Support for async context manager."""
        await self.disconnect()


class InteractiveAgent(BaseClaudeAgent):
    """
    Interactive agent that provides a conversation loop.
    
    This extends BaseClaudeAgent with interactive capabilities for
    command-line conversations with users.
    """
    
    def __init__(self, config_dir: Optional[Path] = None):
        super().__init__(config_dir)
        self.conversation_history = []
    
    def display_message(self, message: Any) -> None:
        """
        Display a message to the user.
        
        Args:
            message: Message to display
        """
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(f"\n🤖 Claude: {block.text}")
                elif isinstance(block, ToolUseBlock):
                    print(f"\n🔧 Using tool: {block.name}")
                    if hasattr(block, 'input') and block.input:
                        print(f"   Input: {block.input}")
        elif isinstance(message, ResultMessage):
            if message.total_cost_usd and message.total_cost_usd > 0:
                print(f"\n💰 Cost: ${message.total_cost_usd:.4f}")
            if message.duration_ms:
                print(f"⏱️  Duration: {message.duration_ms}ms")
    
    async def run_interactive(self) -> None:
        """
        Run an interactive conversation loop.
        
        This method provides a simple interactive interface where users
        can chat with the agent.
        """
        agent_name = self.agent_config.get('name', 'Claude Agent')
        
        print(f"\n{'='*60}")
        print(f"  {agent_name.upper()} - Interactive Mode")
        print(f"{'='*60}")
        print(f"\nHello! I'm {agent_name}. Type 'quit' or 'exit' to end our conversation.")
        
        if self.agent_config.get('description'):
            print(f"\n{self.agent_config['description']}")
        
        async with self:
            while True:
                try:
                    user_input = input(f"\n💬 You: ").strip()
                    
                    if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                        print(f"\n👋 {agent_name}: Goodbye! Thanks for chatting.")
                        break
                    
                    if not user_input:
                        continue
                    
                    # Send query and display responses
                    async for message in self.query(user_input):
                        self.display_message(message)
                    
                except KeyboardInterrupt:
                    print(f"\n\n👋 {agent_name}: Goodbye! (Interrupted)")
                    break
                except Exception as e:
                    self.logger.error(f"Error processing input: {e}")
                    print(f"\n❌ Sorry, I encountered an error: {e}")


async def create_agent_from_config(config_dir: Path) -> BaseClaudeAgent:
    """
    Create an agent from a configuration directory.
    
    Args:
        config_dir: Directory containing agent configuration
        
    Returns:
        Configured agent instance
    """
    return BaseClaudeAgent(config_dir)