#!/usr/bin/env python3
"""
Test script to generate and validate AVM-based Bicep templates.
"""

import sys
import os
import tempfile
import subprocess
from pathlib import Path

# Add parent directory to path to import agent module
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agent import AzureFSILandingZoneAgent


def validate_bicep_template(template_content: str, template_name: str) -> bool:
    """Validate a Bicep template using Azure CLI."""
    print(f"\n{'='*80}")
    print(f"Testing: {template_name}")
    print(f"{'='*80}")

    # Create temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.bicep', delete=False) as f:
        f.write(template_content)
        temp_path = f.name

    try:
        # Try to build the template
        result = subprocess.run(
            ['az', 'bicep', 'build', '--file', temp_path],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            print(f"✅ {template_name}: Valid Bicep template")
            return True
        else:
            print(f"❌ {template_name}: Bicep validation failed")
            print(f"Error: {result.stderr}")
            return False

    except Exception as e:
        print(f"❌ {template_name}: Exception during validation: {e}")
        return False
    finally:
        # Cleanup
        os.unlink(temp_path)
        json_path = temp_path.replace('.bicep', '.json')
        if os.path.exists(json_path):
            os.unlink(json_path)


def main():
    """Main test function."""
    print("🧪 Testing Azure FSI Landing Zone AVM Templates")
    print("="*80)

    # Initialize agent (synchronously for testing)
    config_dir = Path(__file__).parent
    agent = AzureFSILandingZoneAgent(config_dir)

    # Test templates
    templates = {
        "Hub VNet": agent._generate_hub_vnet_bicep(),
        "Spoke VNet": agent._generate_spoke_vnet_bicep(),
        "Key Vault": agent._generate_keyvault_bicep(),
        "Storage Account": agent._generate_storage_bicep(),
        "Policy Assignment": agent._generate_policy_bicep(),
    }

    results = {}
    for name, template in templates.items():
        results[name] = validate_bicep_template(template, name)

    # Summary
    print(f"\n{'='*80}")
    print("📊 SUMMARY")
    print(f"{'='*80}")

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for name, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {name}")

    print(f"\nTotal: {passed}/{total} templates valid")

    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
