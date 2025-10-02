"""
Validation utilities for Claude agents.
"""

import re
from typing import Any, Dict, List


def validate_config(config: Dict[str, Any]) -> List[str]:
    """
    Validate agent configuration.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        List of validation errors (empty if valid)
    """
    errors = []
    
    # Validate required fields
    required_fields = ["anthropic_api_key", "agent_name"]
    for field in required_fields:
        if not config.get(field):
            errors.append(f"Missing required field: {field}")
    
    # Validate API key format
    if config.get("anthropic_api_key"):
        if not validate_api_key(config["anthropic_api_key"]):
            errors.append("Invalid Anthropic API key format")
    
    # Validate agent name
    if config.get("agent_name"):
        if not re.match(r"^[a-zA-Z0-9_-]+$", config["agent_name"]):
            errors.append("Agent name must contain only alphanumeric characters, hyphens, and underscores")
    
    # Validate port number
    if config.get("mcp_server_port"):
        port = config["mcp_server_port"]
        if not isinstance(port, int) or port < 1 or port > 65535:
            errors.append("MCP server port must be between 1 and 65535")
    
    return errors


def validate_api_key(api_key: str) -> bool:
    """
    Validate Anthropic API key format.
    
    Args:
        api_key: API key to validate
        
    Returns:
        True if valid format, False otherwise
    """
    # Anthropic API keys typically start with 'sk-ant-' and are base64-like
    if not api_key.startswith("sk-ant-"):
        return False
    
    # Check minimum length (typical Anthropic keys are longer)
    if len(api_key) < 20:
        return False
    
    return True