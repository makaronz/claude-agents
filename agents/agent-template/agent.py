"""
Template agent implementation.

This is a basic template for creating Claude agents. Customize this file
to implement your specific agent behavior.
"""

import asyncio
import sys
from pathlib import Path
from typing import Dict, Any, List

# Add the shared utilities to the path
sys.path.append(str(Path(__file__).parent.parent.parent / "shared"))

from utils import setup_logging, get_logger, load_config, validate_config


class TemplateAgent:
    """
    Template agent class.
    
    This is a basic implementation that can be customized for specific use cases.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the agent with configuration.
        
        Args:
            config: Agent configuration dictionary
        """
        self.config = config
        self.logger = get_logger(__name__)
        self.name = config.get("agent_name", "template-agent")
        
        self.logger.info(f"Initializing {self.name} agent")
    
    async def initialize(self) -> None:
        """
        Initialize the agent (async setup).
        
        Override this method to add custom initialization logic.
        """
        self.logger.info("Agent initialization complete")
    
    async def process_message(self, message: str) -> str:
        """
        Process a message and return a response.
        
        Args:
            message: Input message to process
            
        Returns:
            Agent response
        """
        self.logger.info(f"Processing message: {message[:50]}...")
        
        # This is where you would implement your agent's main logic
        # For now, just return a simple response
        response = f"Hello! I'm {self.name}. I received your message: {message}"
        
        self.logger.info("Message processed successfully")
        return response
    
    async def run(self) -> None:
        """
        Main agent run loop.
        
        Override this method to implement your agent's main behavior.
        """
        self.logger.info("Starting agent run loop")
        
        # Example: simple interactive loop
        print(f"\n{self.name} is ready! Type 'quit' to exit.")
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("Goodbye!")
                    break
                
                if user_input:
                    response = await self.process_message(user_input)
                    print(f"\n{self.name}: {response}")
                    
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                self.logger.error(f"Error processing input: {e}")
                print(f"Sorry, I encountered an error: {e}")


async def main():
    """
    Main entry point for the agent.
    """
    # Load configuration
    config_dir = Path(__file__).parent
    config = load_config(config_dir)
    
    # Validate configuration
    errors = validate_config(config)
    if errors:
        print("Configuration errors:")
        for error in errors:
            print(f"  - {error}")
        return
    
    # Set up logging
    setup_logging(
        level=config.get("log_level", "INFO"),
        log_file=config_dir / "logs" / "agent.log"
    )
    
    # Create and run agent
    agent = TemplateAgent(config)
    await agent.initialize()
    await agent.run()


if __name__ == "__main__":
    asyncio.run(main())