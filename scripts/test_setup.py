#!/usr/bin/env python3
"""
Test script to verify Claude Agent SDK integration.

This script tests the basic functionality of our agent infrastructure
without requiring an API key.
"""

import asyncio
import sys
from pathlib import Path

# Add shared modules to path
sys.path.append(str(Path(__file__).parent / "shared"))

from agents import BaseClaudeAgent
from utils import setup_logging, load_config, validate_config


async def test_agent_creation():
    """Test that we can create an agent without errors."""
    print("🧪 Testing agent creation...")
    
    try:
        # Create a mock config directory
        config_dir = Path(__file__).parent / "agents" / "example-agent"
        
        if not config_dir.exists():
            print("❌ Example agent directory not found")
            return False
        
        # Create agent
        agent = BaseClaudeAgent(config_dir)
        print(f"✅ Agent created successfully: {agent.agent_config.get('name', 'Unknown')}")
        
        # Test configuration loading
        options = agent.get_agent_options()
        print(f"✅ Agent options configured: {options.model or 'default model'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Agent creation failed: {e}")
        return False


def test_configuration():
    """Test configuration loading and validation."""
    print("🧪 Testing configuration...")
    
    try:
        # Test config loading
        config = load_config()
        print("✅ Configuration loaded successfully")
        
        # Test validation (will show missing API key as expected)
        errors = validate_config(config)
        if "Missing required field: anthropic_api_key" in errors:
            print("✅ Configuration validation working (API key missing as expected)")
        else:
            print("✅ Configuration validation passed")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False


def test_imports():
    """Test that all required modules can be imported."""
    print("🧪 Testing imports...")
    
    try:
        # Test Claude Agent SDK imports
        from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, tool
        print("✅ Claude Agent SDK imports successful")
        
        # Test our shared modules
        from shared import BaseClaudeAgent, InteractiveAgent
        print("✅ Shared module imports successful")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import test failed: {e}")
        print("💡 Make sure you've run: uv pip sync uv.lock (or bootstrap with 'uv pip install -r requirements.txt')")
        return False
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False


async def main():
    """Run all tests."""
    print("🚀 Claude Agents Test Suite")
    print("="*40)
    
    # Setup logging for tests
    setup_logging("INFO")
    
    tests = [
        ("Import Tests", test_imports),
        ("Configuration Tests", test_configuration),
        ("Agent Creation", test_agent_creation),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 20)
        
        if asyncio.iscoroutinefunction(test_func):
            result = await test_func()
        else:
            result = test_func()
        
        if result:
            passed += 1
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your setup is ready.")
        print("\n🏃 Next steps:")
        print("1. Add your ANTHROPIC_API_KEY to .env")
        print("2. Try: cd agents/example-agent && python agent.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
