"""
Example Claude agent implementation.

This agent demonstrates the basic structure and functionality of a Claude agent
using the shared utilities and template structure.
"""

import asyncio
import sys
from pathlib import Path
from typing import Dict, Any
from datetime import datetime

# Add the shared utilities to the path
sys.path.append(str(Path(__file__).parent.parent.parent / "shared"))

from utils import setup_logging, get_logger, load_config, validate_config


class ExampleAgent:
    """
    Example Claude agent that demonstrates basic functionality.
    
    This agent provides a simple conversational interface and shows
    how to use the shared utilities and configuration system.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the example agent.
        
        Args:
            config: Agent configuration dictionary
        """
        self.config = config
        self.logger = get_logger(__name__)
        self.name = config.get("agent_name", "example-agent")
        self.start_time = datetime.now()
        self.message_count = 0
        
        self.logger.info(f"Initializing {self.name}")
        
        # Available commands
        self.commands = {
            "help": self._help_command,
            "status": self._status_command,
            "config": self._config_command,
            "time": self._time_command
        }
    
    async def initialize(self) -> None:
        """
        Initialize the agent (async setup).
        """
        self.logger.info("Agent initialization complete")
        print(f"\n🤖 {self.name} initialized successfully!")
        print("Type 'help' for available commands or just chat with me.")
    
    async def process_message(self, message: str) -> str:
        """
        Process a message and return a response.
        
        Args:
            message: Input message to process
            
        Returns:
            Agent response
        """
        self.message_count += 1
        self.logger.info(f"Processing message #{self.message_count}: {message[:50]}...")
        
        # Check if it's a command
        if message.lower().strip() in self.commands:
            response = await self.commands[message.lower().strip()]()
        else:
            # Regular conversation
            response = await self._process_conversation(message)
        
        self.logger.info("Message processed successfully")
        return response
    
    async def _process_conversation(self, message: str) -> str:
        """
        Process a regular conversational message.
        
        Args:
            message: User message
            
        Returns:
            Agent response
        """
        # Simple conversational responses
        message_lower = message.lower()
        
        if any(greeting in message_lower for greeting in ["hello", "hi", "hey"]):
            return f"Hello! I'm {self.name}. How can I help you today?"
        
        elif any(word in message_lower for word in ["how are you", "how's it going"]):
            uptime = datetime.now() - self.start_time
            return f"I'm doing well! I've been running for {uptime.seconds} seconds and have processed {self.message_count} messages."
        
        elif any(word in message_lower for word in ["what can you do", "capabilities"]):
            return ("I'm an example Claude agent! I can:\n"
                   "• Have conversations with you\n"
                   "• Respond to commands (try 'help')\n"
                   "• Show my status and configuration\n"
                   "• Demonstrate proper logging and error handling")
        
        elif "weather" in message_lower:
            return "I don't have access to real weather data, but I hope it's nice where you are! 🌞"
        
        elif any(word in message_lower for word in ["thank", "thanks"]):
            return "You're welcome! I'm happy to help."
        
        else:
            return (f"Thanks for your message! I'm a simple example agent, so I might not have "
                   f"specific knowledge about '{message}', but I'm here to chat. "
                   f"Try typing 'help' to see what I can do!")
    
    async def _help_command(self) -> str:
        """Show available commands."""
        return ("Available commands:\n"
               "• help - Show this help message\n"
               "• status - Show agent status\n"
               "• config - Show configuration info\n"
               "• time - Show current time\n"
               "• quit - Exit the agent\n\n"
               "Or just chat with me normally!")
    
    async def _status_command(self) -> str:
        """Show agent status."""
        uptime = datetime.now() - self.start_time
        return (f"Agent Status:\n"
               f"• Name: {self.name}\n"
               f"• Uptime: {uptime.seconds} seconds\n"
               f"• Messages processed: {self.message_count}\n"
               f"• Started: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    async def _config_command(self) -> str:
        """Show configuration information."""
        return (f"Configuration:\n"
               f"• Agent name: {self.config.get('agent_name', 'N/A')}\n"
               f"• Log level: {self.config.get('log_level', 'N/A')}\n"
               f"• MCP server port: {self.config.get('mcp_server_port', 'N/A')}\n"
               f"• MCP server host: {self.config.get('mcp_server_host', 'N/A')}")
    
    async def _time_command(self) -> str:
        """Show current time."""
        now = datetime.now()
        return f"Current time: {now.strftime('%Y-%m-%d %H:%M:%S')}"
    
    async def run(self) -> None:
        """
        Main agent run loop.
        """
        self.logger.info("Starting agent run loop")
        
        print(f"\n{'='*50}")
        print(f"  {self.name.upper()} - Example Claude Agent")
        print(f"{'='*50}")
        print("\nI'm ready to chat! Type 'quit' to exit.")
        
        while True:
            try:
                user_input = input(f"\n💬 You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print(f"\n👋 {self.name}: Goodbye! Thanks for chatting.")
                    break
                
                if user_input:
                    response = await self.process_message(user_input)
                    print(f"\n🤖 {self.name}: {response}")
                    
            except KeyboardInterrupt:
                print(f"\n\n👋 {self.name}: Goodbye! (Interrupted)")
                break
            except Exception as e:
                self.logger.error(f"Error processing input: {e}")
                print(f"\n❌ {self.name}: Sorry, I encountered an error: {e}")


async def main():
    """
    Main entry point for the example agent.
    """
    # Load configuration
    config_dir = Path(__file__).parent
    config = load_config(config_dir)
    
    # Override agent name for this example
    config["agent_name"] = "example-agent"
    
    # Validate configuration
    errors = validate_config(config)
    if errors:
        print("❌ Configuration errors:")
        for error in errors:
            print(f"  • {error}")
        print("\nPlease check your .env file and configuration.")
        return
    
    # Set up logging
    logs_dir = config_dir / "logs"
    logs_dir.mkdir(exist_ok=True)
    
    setup_logging(
        level=config.get("log_level", "INFO"),
        log_file=logs_dir / "agent.log"
    )
    
    # Create and run agent
    agent = ExampleAgent(config)
    await agent.initialize()
    await agent.run()


if __name__ == "__main__":
    asyncio.run(main())