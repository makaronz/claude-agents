"""
Configuration utilities for Claude agents.
"""

import os
from typing import Any, Dict, Optional
from pathlib import Path
from dotenv import load_dotenv


def load_config(config_dir: Optional[Path] = None) -> Dict[str, Any]:
    """
    Load configuration from environment variables and .env files.
    
    Args:
        config_dir: Directory containing .env file (defaults to current directory)
        
    Returns:
        Dictionary of configuration values
    """
    # Load .env file if it exists
    if config_dir:
        env_file = config_dir / ".env"
    else:
        env_file = Path(".env")
    
    if env_file.exists():
        load_dotenv(env_file)
    
    return {
        "anthropic_api_key": get_env_var("ANTHROPIC_API_KEY"),
        "agent_name": get_env_var("AGENT_NAME", "claude-agent"),
        "agent_version": get_env_var("AGENT_VERSION", "1.0.0"),
        "log_level": get_env_var("LOG_LEVEL", "INFO"),
        "mcp_server_port": int(get_env_var("MCP_SERVER_PORT", "3000")),
        "mcp_server_host": get_env_var("MCP_SERVER_HOST", "localhost"),
    }


def get_env_var(key: str, default: Optional[str] = None) -> str:
    """
    Get environment variable with optional default.
    
    Args:
        key: Environment variable name
        default: Default value if variable is not set
        
    Returns:
        Environment variable value or default
        
    Raises:
        ValueError: If variable is not set and no default provided
    """
    value = os.getenv(key, default)
    if value is None:
        raise ValueError(f"Environment variable {key} is required but not set")
    return value