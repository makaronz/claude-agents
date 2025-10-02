"""
Tests for the Claude agents repository structure and shared utilities.
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import patch

# Add shared utilities to path
repo_root = Path(__file__).parent.parent
sys.path.append(str(repo_root / "shared"))

from utils import load_config, validate_config, get_logger, setup_logging


class TestSharedUtils:
    """Test the shared utilities."""
    
    def test_get_logger(self):
        """Test logger creation."""
        logger = get_logger("test")
        assert logger.name == "test"
    
    @patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'sk-ant-test123', 'AGENT_NAME': 'test-agent'})
    def test_load_config(self):
        """Test configuration loading."""
        config = load_config()
        assert config['anthropic_api_key'] == 'sk-ant-test123'
        assert config['agent_name'] == 'test-agent'
    
    def test_validate_config_valid(self):
        """Test configuration validation with valid config."""
        config = {
            'anthropic_api_key': 'sk-ant-valid-key-12345',
            'agent_name': 'test-agent',
            'mcp_server_port': 3000
        }
        errors = validate_config(config)
        assert len(errors) == 0
    
    def test_validate_config_invalid(self):
        """Test configuration validation with invalid config."""
        config = {
            'anthropic_api_key': 'invalid-key',
            'agent_name': 'invalid name!',
            'mcp_server_port': 99999
        }
        errors = validate_config(config)
        assert len(errors) > 0


class TestDirectoryStructure:
    """Test that the directory structure is correct."""
    
    def test_agents_directory_exists(self):
        """Test that agents directory exists."""
        agents_dir = repo_root / "agents"
        assert agents_dir.exists()
        assert agents_dir.is_dir()
    
    def test_shared_directory_exists(self):
        """Test that shared directory exists."""
        shared_dir = repo_root / "shared"
        assert shared_dir.exists()
        assert shared_dir.is_dir()
    
    def test_template_agent_exists(self):
        """Test that template agent exists."""
        template_dir = repo_root / "agents" / "agent-template"
        assert template_dir.exists()
        assert (template_dir / "agent.py").exists()
        assert (template_dir / "config.yaml").exists()
        assert (template_dir / "README.md").exists()
    
    def test_example_agent_exists(self):
        """Test that example agent exists."""
        example_dir = repo_root / "agents" / "example-agent"
        assert example_dir.exists()
        assert (example_dir / "agent.py").exists()
        assert (example_dir / "config.yaml").exists()
        assert (example_dir / "README.md").exists()
    
    def test_documentation_exists(self):
        """Test that documentation exists."""
        docs_dir = repo_root / "docs"
        assert docs_dir.exists()
        assert (docs_dir / "getting-started.md").exists()
        assert (docs_dir / "agent-guide.md").exists()


if __name__ == "__main__":
    pytest.main([__file__])