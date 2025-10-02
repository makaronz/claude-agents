"""
Template agent implementation using Claude Agent SDK.

This is a template for creating Claude agents using the official Claude Agent SDK.
Customize this file to implement your specific agent behavior.
"""

import asyncio
import sys
from pathlib import Path
from typing import List, Any, Optional

# Add the shared modules to the path
sys.path.append(str(Path(__file__).parent.parent.parent / "shared"))

from agents import BaseClaudeAgent, InteractiveAgent
from utils import setup_logging
from claude_agent_sdk import tool


class TemplateAgent(InteractiveAgent):
    """
    Template agent class using Claude Agent SDK.
    
    This is a basic implementation that can be customized for specific use cases.
    Inherits from InteractiveAgent to provide conversation capabilities.
    """
    
    def get_system_prompt(self) -> Optional[str]:
        """
        Get the system prompt for this agent.
        
        Override this method to provide a custom system prompt.
        """
        return (
            "You are a helpful template agent. You can assist with various tasks and "
            "demonstrate the capabilities of the Claude Agent SDK. You have access to "
            "custom tools and can help users understand how to build their own agents."
        )
    
    def get_custom_tools(self) -> List[Any]:
        """
        Get custom tools for this agent.
        
        Override this method to add custom MCP tools for your agent.
        """
        return [
            self.example_tool,
            self.get_agent_info,
        ]
    
    @tool("example_tool", "An example custom tool that processes text", {"text": str})
    async def example_tool(self, args):
        """Example custom tool that processes text."""
        text = args.get("text", "")
        processed_text = f"Processed: {text.upper()} (length: {len(text)})"
        
        return {
            "content": [
                {"type": "text", "text": processed_text}
            ]
        }
    
    @tool("get_agent_info", "Get information about this agent", {})
    async def get_agent_info(self, args):
        """Get information about this agent."""
        info = {
            "name": self.agent_config.get('name', 'Template Agent'),
            "version": self.agent_config.get('version', '1.0.0'),
            "description": self.agent_config.get('description', 'A template agent'),
            "custom_tools": len(self.get_custom_tools()),
            "config_dir": str(self.config_dir)
        }
        
        info_text = "\n".join([f"{k}: {v}" for k, v in info.items()])
        
        return {
            "content": [
                {"type": "text", "text": f"Agent Information:\n{info_text}"}
            ]
        }


async def main():
    """
    Main entry point for the template agent.
    """
    config_dir = Path(__file__).parent
    
    # Set up logging
    setup_logging(
        level="INFO",
        log_file=config_dir / "logs" / "agent.log"
    )
    
    # Create and run the agent
    agent = TemplateAgent(config_dir)
    await agent.run_interactive()


if __name__ == "__main__":
    asyncio.run(main())