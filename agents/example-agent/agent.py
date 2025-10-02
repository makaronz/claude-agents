"""
Example Claude agent implementation using Claude Agent SDK.

This agent demonstrates the structure and functionality of a Claude agent
using the official Claude Agent SDK with custom tools and interactive features.
"""

import asyncio
import sys
from pathlib import Path
from typing import List, Any, Optional
from datetime import datetime

# Add the shared modules to the path
sys.path.append(str(Path(__file__).parent.parent.parent / "shared"))

from agents import InteractiveAgent
from utils import setup_logging
from claude_agent_sdk import tool


class ExampleAgent(InteractiveAgent):
    """
    Example Claude agent using Claude Agent SDK.
    
    This agent demonstrates:
    - Custom system prompts
    - Custom MCP tools
    - Interactive conversation capabilities
    - Proper logging and configuration
    """
    
    def __init__(self, config_dir: Path):
        super().__init__(config_dir)
        self.start_time = datetime.now()
        self.message_count = 0
    
    def get_system_prompt(self) -> Optional[str]:
        """Get the system prompt for this agent."""
        return (
            "You are an example Claude agent built with the Claude Agent SDK. "
            "You are helpful, friendly, and demonstrate various agent capabilities. "
            "You have access to custom tools and can help users understand how "
            "Claude agents work. You keep track of conversation statistics and "
            "can provide information about your capabilities."
        )
    
    def get_custom_tools(self) -> List[Any]:
        """Get custom tools for this agent."""
        return [
            self.get_agent_status,
            self.get_current_time,
            self.count_words,
            self.reverse_text,
        ]
    
    @tool("get_agent_status", "Get current status and statistics for this agent", {})
    async def get_agent_status(self, args):
        """Get agent status and statistics."""
        uptime = datetime.now() - self.start_time
        
        status_info = {
            "name": self.agent_config.get('name', 'Example Agent'),
            "version": self.agent_config.get('version', '1.0.0'),
            "uptime_seconds": uptime.total_seconds(),
            "messages_processed": self.message_count,
            "started_at": self.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            "custom_tools": len(self.get_custom_tools())
        }
        
        status_text = "🤖 Agent Status:\n"
        for key, value in status_info.items():
            status_text += f"• {key.replace('_', ' ').title()}: {value}\n"
        
        return {
            "content": [
                {"type": "text", "text": status_text}
            ]
        }
    
    @tool("get_current_time", "Get the current date and time", {})
    async def get_current_time(self, args):
        """Get current date and time."""
        now = datetime.now()
        time_info = {
            "current_time": now.strftime('%Y-%m-%d %H:%M:%S'),
            "iso_format": now.isoformat(),
            "weekday": now.strftime('%A'),
            "timezone": str(now.astimezone().tzinfo)
        }
        
        time_text = "🕐 Current Time Information:\n"
        for key, value in time_info.items():
            time_text += f"• {key.replace('_', ' ').title()}: {value}\n"
        
        return {
            "content": [
                {"type": "text", "text": time_text}
            ]
        }
    
    @tool("count_words", "Count words, characters, and lines in text", {"text": str})
    async def count_words(self, args):
        """Count words, characters, and lines in provided text."""
        text = args.get("text", "")
        
        stats = {
            "characters": len(text),
            "characters_no_spaces": len(text.replace(" ", "")),
            "words": len(text.split()),
            "lines": len(text.splitlines()),
            "paragraphs": len([p for p in text.split('\n\n') if p.strip()])
        }
        
        stats_text = f"📊 Text Statistics for: '{text[:50]}{'...' if len(text) > 50 else ''}'\n"
        for key, value in stats.items():
            stats_text += f"• {key.replace('_', ' ').title()}: {value}\n"
        
        return {
            "content": [
                {"type": "text", "text": stats_text}
            ]
        }
    
    @tool("reverse_text", "Reverse the provided text", {"text": str})
    async def reverse_text(self, args):
        """Reverse the provided text."""
        text = args.get("text", "")
        reversed_text = text[::-1]
        
        result_text = f"🔄 Text Reversal:\n• Original: {text}\n• Reversed: {reversed_text}"
        
        return {
            "content": [
                {"type": "text", "text": result_text}
            ]
        }
    
    async def query(self, prompt: str):
        """Override query to track message count."""
        self.message_count += 1
        self.logger.info(f"Processing message #{self.message_count}: {prompt[:50]}...")
        
        async for message in super().query(prompt):
            yield message


async def main():
    """
    Main entry point for the example agent.
    """
    config_dir = Path(__file__).parent
    
    # Set up logging
    logs_dir = config_dir / "logs"
    logs_dir.mkdir(exist_ok=True)
    
    setup_logging(
        level="INFO",
        log_file=logs_dir / "agent.log"
    )
    
    # Create and run the agent
    agent = ExampleAgent(config_dir)
    
    print("\n🎉 Welcome to the Example Claude Agent!")
    print("This agent demonstrates Claude Agent SDK capabilities including:")
    print("• Custom tools for status, time, text analysis")
    print("• Interactive conversation")
    print("• Proper logging and configuration")
    print("\nTry asking me to:")
    print("- Check my status")
    print("- Get the current time") 
    print("- Count words in some text")
    print("- Reverse some text")
    print("- Or just have a normal conversation!")
    
    await agent.run_interactive()


if __name__ == "__main__":
    asyncio.run(main())