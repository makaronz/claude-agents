"""
Custom MCP tools for the template agent.

Add your custom tools here. Each tool should be a function that can be
called by the agent to perform specific tasks.
"""

from typing import Any, Dict, List


def example_tool(input_data: str) -> Dict[str, Any]:
    """
    Example custom tool.
    
    Args:
        input_data: Input data for the tool
        
    Returns:
        Tool result
    """
    return {
        "result": f"Processed: {input_data}",
        "status": "success"
    }


def get_available_tools() -> List[Dict[str, Any]]:
    """
    Get list of available tools for this agent.
    
    Returns:
        List of tool definitions
    """
    return [
        {
            "name": "example_tool",
            "description": "An example tool that processes input data",
            "parameters": {
                "input_data": {
                    "type": "string",
                    "description": "Data to process"
                }
            },
            "function": example_tool
        }
    ]