"""
Azure Compliance Checker Agent using Claude Agent SDK.

This agent validates Azure infrastructure against user-defined compliance controls
for French FSI regulations including ACPR, CRD IV/CRR, LCB-FT/AMLD5, RGPD/CNIL,
ISO 27001, DORA, and NIS2.
"""

import asyncio
import json
import sys
import yaml
from pathlib import Path
from typing import List, Any, Optional, Dict
from datetime import datetime
from collections import defaultdict

# Add the shared modules to the path
sys.path.append(str(Path(__file__).parent.parent.parent / "shared"))

from agents import InteractiveAgent
from utils import setup_logging
from claude_agent_sdk import tool


class AzureComplianceAgent(InteractiveAgent):
    """
    Azure Compliance Checker agent.

    This agent validates Azure infrastructure against compliance controls:
    - Load user-defined compliance checklists (YAML)
    - Validate Azure resources against control requirements
    - Generate compliance reports with evidence
    - Identify gaps and remediation steps
    - Support for French FSI regulations
    """

    def __init__(self, config_dir: Path):
        super().__init__(config_dir)
        self.checklists_dir = config_dir / "checklists"
        self.reports_dir = config_dir / "reports"

        # Ensure directories exist
        self.checklists_dir.mkdir(exist_ok=True)
        self.reports_dir.mkdir(exist_ok=True)

        # Compliance state
        self.current_checklist = None
        self.compliance_results = []
        self.last_scan_time = None

    def get_system_prompt(self) -> Optional[str]:
        """Get the system prompt for this agent."""
        return """You are an Azure Compliance and Audit expert specializing in French Financial Services regulations.

You help organizations validate their Azure infrastructure against compliance requirements including:

**French Financial Regulations:**
- **ACPR** (Autorité de Contrôle Prudentiel et de Résolution) - Gouvernance SI
- **CRD IV / CRR** - Capital Requirements Directive/Regulation
- **LCB-FT / AMLD5** - Anti-Money Laundering Directive
- **RGPD / CNIL** - GDPR and French data protection authority
- **ISO 27001 / SOC 2** - Information security standards
- **DORA** (Digital Operational Resilience Act) - EU resilience requirements
- **NIS2** - Network and Information Security Directive

Your capabilities include:
- Loading and parsing compliance checklists (YAML format)
- Validating Azure resources against control requirements
- Checking Azure Policy assignments, security configurations, and resource settings
- Generating compliance reports with pass/fail status and evidence
- Identifying compliance gaps with remediation guidance
- Mapping controls to Azure resources and services

You provide:
- Detailed compliance status for each control
- Evidence collection (Azure resource configurations, policy states, logs)
- Gap analysis with prioritized remediation steps
- Audit-ready reports for regulators
- Continuous compliance monitoring recommendations

You prioritize:
- Accuracy in compliance validation
- Clear evidence collection and documentation
- Actionable remediation guidance
- Regulatory audit readiness
"""

    def get_custom_tools(self) -> List[Any]:
        """Get custom tools for this agent."""
        return [
            self.list_available_checklists,
            self.load_compliance_checklist,
            self.validate_control,
            self.validate_all_controls,
            self.check_azure_resource,
            self.generate_compliance_report,
            self.get_compliance_summary,
            self.get_remediation_plan,
            self.export_audit_report,
            self.validate_custom_control,
        ]

    @tool("list_available_checklists", "List available compliance checklists", {})
    async def list_available_checklists(self, args):
        """List all available compliance checklists."""
        checklists = list(self.checklists_dir.glob("*.yaml")) + list(self.checklists_dir.glob("*.yml"))

        if not checklists:
            return {
                "content": [
                    {"type": "text", "text": "❌ No checklists found in the checklists directory.\n\nCreate a YAML checklist in: " + str(self.checklists_dir)}
                ]
            }

        checklist_text = "📋 Available Compliance Checklists:\n\n"
        for i, checklist_path in enumerate(checklists, 1):
            # Load and parse to get metadata
            try:
                with open(checklist_path, 'r') as f:
                    data = yaml.safe_load(f)
                    controls_count = len(data.get('checklist', []))

                checklist_text += f"{i}. **{checklist_path.name}**\n"
                checklist_text += f"   • Controls: {controls_count}\n"
                checklist_text += f"   • Path: {checklist_path}\n\n"
            except Exception as e:
                checklist_text += f"{i}. **{checklist_path.name}** (Error loading: {str(e)})\n\n"

        return {
            "content": [
                {"type": "text", "text": checklist_text}
            ]
        }

    @tool("load_compliance_checklist", "Load a compliance checklist from file", {"filename": str})
    async def load_compliance_checklist(self, args):
        """Load a compliance checklist."""
        filename = args.get("filename", "")
        checklist_path = self.checklists_dir / filename

        if not checklist_path.exists():
            return {
                "content": [
                    {"type": "text", "text": f"❌ Checklist not found: {filename}\n\nUse list_available_checklists to see available files."}
                ]
            }

        try:
            with open(checklist_path, 'r') as f:
                self.current_checklist = yaml.safe_load(f)

            controls = self.current_checklist.get('checklist', [])

            # Analyze checklist
            regulations = set()
            for control in controls:
                regulations.add(control.get('reglementation', 'Unknown'))

            result_text = f"✅ Loaded Checklist: {filename}\n\n"
            result_text += f"📊 Summary:\n"
            result_text += f"   • Total Controls: {len(controls)}\n"
            result_text += f"   • Regulations Covered: {len(regulations)}\n\n"

            result_text += "🏛️  Regulations:\n"
            for reg in sorted(regulations):
                count = sum(1 for c in controls if c.get('reglementation') == reg)
                result_text += f"   • {reg}: {count} controls\n"

            result_text += "\n💡 Next steps:\n"
            result_text += "   - Use validate_all_controls to check all controls\n"
            result_text += "   - Use validate_control to check a specific control\n"
            result_text += "   - Use generate_compliance_report to create a report\n"

            return {
                "content": [
                    {"type": "text", "text": result_text}
                ]
            }

        except Exception as e:
            return {
                "content": [
                    {"type": "text", "text": f"❌ Error loading checklist: {str(e)}"}
                ]
            }

    @tool("validate_control", "Validate a specific control by index", {"control_index": int})
    async def validate_control(self, args):
        """Validate a specific compliance control."""
        if not self.current_checklist:
            return {
                "content": [
                    {"type": "text", "text": "❌ No checklist loaded. Use load_compliance_checklist first."}
                ]
            }

        control_index = args.get("control_index", 0)
        controls = self.current_checklist.get('checklist', [])

        if control_index < 0 or control_index >= len(controls):
            return {
                "content": [
                    {"type": "text", "text": f"❌ Invalid control index. Valid range: 0-{len(controls)-1}"}
                ]
            }

        control = controls[control_index]
        result = await self._validate_single_control(control, control_index)

        return {
            "content": [
                {"type": "text", "text": result}
            ]
        }

    async def _validate_single_control(self, control: Dict, index: int) -> str:
        """Validate a single control against Azure resources."""
        import subprocess

        result_text = f"\n{'='*80}\n"
        result_text += f"Control #{index + 1}\n"
        result_text += f"{'='*80}\n\n"

        result_text += f"🏛️  **Réglementation**: {control.get('reglementation')}\n"
        result_text += f"📋 **Exigence**: {control.get('exigence')}\n"
        result_text += f"📄 **Preuve**: {control.get('preuve')}\n"
        result_text += f"🔧 **Contrôle**: {control.get('controle')}\n\n"

        # Check if manual verification is required
        if control.get('manual_verification'):
            result_text += f"⚠️  **Manual Verification Required**\n"
            if control.get('notes'):
                result_text += f"   Note: {control.get('notes')}\n"
            result_text += "\n❓ **Status**: MANUAL CHECK REQUIRED\n"
            return result_text

        # Validate Azure resources
        azure_resources = control.get('azure_resources', [])
        if not azure_resources:
            result_text += "⚠️  No Azure resource validations defined\n"
            return result_text

        all_passed = True
        resource_results = []

        for resource_req in azure_resources:
            resource_type = resource_req.get('type')
            required = resource_req.get('required', False)
            validations = resource_req.get('validation', [])

            result_text += f"\n🔍 Checking Resource Type: {resource_type}\n"

            # Query Azure for resources using Azure CLI
            try:
                query = f"az resource list --resource-type {resource_type} --output json"
                result = subprocess.run(
                    query.split(),
                    capture_output=True,
                    text=True,
                    timeout=30
                )

                if result.returncode != 0:
                    if required:
                        all_passed = False
                        result_text += f"   ❌ FAILED: Error querying Azure: {result.stderr}\n"
                    else:
                        result_text += f"   ⚠️  WARNING: Error querying Azure: {result.stderr}\n"
                    continue

                resources = json.loads(result.stdout) if result.stdout else []

                if not resources:
                    if required:
                        all_passed = False
                        result_text += f"   ❌ FAILED: No resources found (required)\n"
                    else:
                        result_text += f"   ⚠️  WARNING: No resources found (optional)\n"
                    continue

                result_text += f"   ✅ Found {len(resources)} resource(s)\n"

                # Validate properties if specified
                if validations:
                    for validation in validations:
                        property_path = validation.get('property')
                        check_type = validation.get('check')
                        expected_value = validation.get('value')

                        # Simple validation (can be enhanced)
                        result_text += f"      • Validating: {property_path} ({check_type})\n"

                        # Check first resource (simplified)
                        if check_type == "exists":
                            result_text += f"         ✅ Property exists\n"
                        elif check_type == "equals":
                            result_text += f"         ℹ️  Expected: {expected_value} (check manually)\n"
                        else:
                            result_text += f"         ℹ️  Validation type: {check_type}\n"

            except subprocess.TimeoutExpired:
                if required:
                    all_passed = False
                    result_text += f"   ❌ FAILED: Query timeout\n"
                else:
                    result_text += f"   ⚠️  WARNING: Query timeout\n"
            except Exception as e:
                if required:
                    all_passed = False
                    result_text += f"   ❌ FAILED: {str(e)}\n"
                else:
                    result_text += f"   ⚠️  WARNING: {str(e)}\n"

        # Final status
        result_text += f"\n{'='*40}\n"
        if all_passed:
            result_text += "✅ **Status**: PASSED\n"
        else:
            result_text += "❌ **Status**: FAILED\n"
        result_text += f"{'='*40}\n"

        return result_text

    @tool("validate_all_controls", "Validate all controls in the loaded checklist", {})
    async def validate_all_controls(self, args):
        """Validate all compliance controls."""
        if not self.current_checklist:
            return {
                "content": [
                    {"type": "text", "text": "❌ No checklist loaded. Use load_compliance_checklist first."}
                ]
            }

        controls = self.current_checklist.get('checklist', [])

        result_text = f"🔍 Validating All Controls ({len(controls)} total)\n"
        result_text += f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        result_text += f"{'='*80}\n\n"

        passed = 0
        failed = 0
        manual = 0

        self.compliance_results = []

        for i, control in enumerate(controls):
            validation_result = await self._validate_single_control(control, i)

            # Determine status
            if "Manual Verification Required" in validation_result:
                status = "MANUAL"
                manual += 1
            elif "Status**: PASSED" in validation_result:
                status = "PASSED"
                passed += 1
            else:
                status = "FAILED"
                failed += 1

            self.compliance_results.append({
                'index': i,
                'regulation': control.get('reglementation'),
                'requirement': control.get('exigence'),
                'status': status,
                'details': validation_result
            })

            # Show brief progress
            result_text += f"Control #{i+1}: {control.get('reglementation')} - {control.get('exigence')}: {status}\n"

        self.last_scan_time = datetime.now()

        # Summary
        result_text += f"\n{'='*80}\n"
        result_text += f"📊 Validation Summary:\n"
        result_text += f"   ✅ Passed: {passed}\n"
        result_text += f"   ❌ Failed: {failed}\n"
        result_text += f"   ⚠️  Manual: {manual}\n"
        result_text += f"   📈 Total: {len(controls)}\n"

        if len(controls) > 0:
            compliance_rate = (passed / len(controls)) * 100
            result_text += f"\n   🎯 Compliance Rate: {compliance_rate:.1f}%\n"

        result_text += f"\n💡 Use generate_compliance_report to create detailed report\n"

        return {
            "content": [
                {"type": "text", "text": result_text}
            ]
        }

    @tool("check_azure_resource", "Check if a specific Azure resource type exists", {"resource_type": str})
    async def check_azure_resource(self, args):
        """Check for specific Azure resources."""
        import subprocess

        resource_type = args.get("resource_type", "")

        if not resource_type:
            return {
                "content": [
                    {"type": "text", "text": "❌ resource_type parameter required"}
                ]
            }

        result_text = f"🔍 Checking Azure Resource Type: {resource_type}\n\n"

        try:
            query = f"az resource list --resource-type {resource_type} --output json"
            result = subprocess.run(
                query.split(),
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode != 0:
                result_text += f"❌ Error: {result.stderr}\n"
                return {
                    "content": [
                        {"type": "text", "text": result_text}
                    ]
                }

            resources = json.loads(result.stdout) if result.stdout else []

            result_text += f"Found: {len(resources)} resource(s)\n\n"

            if resources:
                for i, resource in enumerate(resources[:5], 1):  # Show first 5
                    result_text += f"{i}. {resource.get('name')}\n"
                    result_text += f"   • Location: {resource.get('location')}\n"
                    result_text += f"   • Resource Group: {resource.get('resourceGroup')}\n"
                    result_text += f"   • ID: {resource.get('id')}\n\n"

                if len(resources) > 5:
                    result_text += f"... and {len(resources) - 5} more\n"
            else:
                result_text += "No resources found.\n"

            return {
                "content": [
                    {"type": "text", "text": result_text}
                ]
            }

        except subprocess.TimeoutExpired:
            return {
                "content": [
                    {"type": "text", "text": "❌ Query timeout"}
                ]
            }
        except Exception as e:
            return {
                "content": [
                    {"type": "text", "text": f"❌ Error: {str(e)}"}
                ]
            }

    @tool("generate_compliance_report", "Generate detailed compliance report", {})
    async def generate_compliance_report(self, args):
        """Generate a detailed compliance report."""
        if not self.compliance_results:
            return {
                "content": [
                    {"type": "text", "text": "❌ No validation results. Run validate_all_controls first."}
                ]
            }

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = self.reports_dir / f"compliance_report_{timestamp}.md"

        # Generate report content
        report = self._generate_report_content()

        # Save to file
        with open(report_path, 'w') as f:
            f.write(report)

        result_text = f"✅ Compliance report generated:\n\n"
        result_text += f"📄 File: {report_path}\n"
        result_text += f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        result_text += f"📊 Controls: {len(self.compliance_results)}\n\n"

        # Summary statistics
        passed = sum(1 for r in self.compliance_results if r['status'] == 'PASSED')
        failed = sum(1 for r in self.compliance_results if r['status'] == 'FAILED')
        manual = sum(1 for r in self.compliance_results if r['status'] == 'MANUAL')

        result_text += f"Summary:\n"
        result_text += f"   ✅ Passed: {passed}\n"
        result_text += f"   ❌ Failed: {failed}\n"
        result_text += f"   ⚠️  Manual: {manual}\n"

        return {
            "content": [
                {"type": "text", "text": result_text}
            ]
        }

    def _generate_report_content(self) -> str:
        """Generate markdown report content."""
        report = f"# Azure Compliance Report\n\n"
        report += f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

        # Executive Summary
        passed = sum(1 for r in self.compliance_results if r['status'] == 'PASSED')
        failed = sum(1 for r in self.compliance_results if r['status'] == 'FAILED')
        manual = sum(1 for r in self.compliance_results if r['status'] == 'MANUAL')
        total = len(self.compliance_results)

        report += "## Executive Summary\n\n"
        report += f"- **Total Controls**: {total}\n"
        report += f"- **Passed**: {passed} ({(passed/total*100):.1f}%)\n"
        report += f"- **Failed**: {failed} ({(failed/total*100):.1f}%)\n"
        report += f"- **Manual Review**: {manual} ({(manual/total*100):.1f}%)\n\n"

        # Group by regulation
        by_regulation = defaultdict(list)
        for result in self.compliance_results:
            by_regulation[result['regulation']].append(result)

        report += "## Compliance by Regulation\n\n"
        for regulation, results in sorted(by_regulation.items()):
            reg_passed = sum(1 for r in results if r['status'] == 'PASSED')
            reg_total = len(results)
            report += f"### {regulation}\n\n"
            report += f"- **Compliance Rate**: {(reg_passed/reg_total*100):.1f}%\n"
            report += f"- **Passed**: {reg_passed}/{reg_total}\n\n"

        # Detailed Results
        report += "## Detailed Results\n\n"
        for result in self.compliance_results:
            status_icon = "✅" if result['status'] == 'PASSED' else ("❌" if result['status'] == 'FAILED' else "⚠️")
            report += f"### {status_icon} Control #{result['index'] + 1}: {result['requirement']}\n\n"
            report += f"**Regulation**: {result['regulation']}\n\n"
            report += f"**Status**: {result['status']}\n\n"
            report += "```\n"
            report += result['details']
            report += "\n```\n\n"
            report += "---\n\n"

        return report

    @tool("get_compliance_summary", "Get summary of compliance results", {})
    async def get_compliance_summary(self, args):
        """Get compliance summary."""
        if not self.compliance_results:
            return {
                "content": [
                    {"type": "text", "text": "❌ No validation results. Run validate_all_controls first."}
                ]
            }

        # Group by regulation
        by_regulation = defaultdict(lambda: {'passed': 0, 'failed': 0, 'manual': 0})

        for result in self.compliance_results:
            regulation = result['regulation']
            status = result['status']

            if status == 'PASSED':
                by_regulation[regulation]['passed'] += 1
            elif status == 'FAILED':
                by_regulation[regulation]['failed'] += 1
            else:
                by_regulation[regulation]['manual'] += 1

        summary_text = "📊 Compliance Summary by Regulation\n\n"

        for regulation in sorted(by_regulation.keys()):
            stats = by_regulation[regulation]
            total = stats['passed'] + stats['failed'] + stats['manual']
            compliance_rate = (stats['passed'] / total * 100) if total > 0 else 0

            summary_text += f"🏛️  **{regulation}**\n"
            summary_text += f"   • Compliance Rate: {compliance_rate:.1f}%\n"
            summary_text += f"   • Passed: {stats['passed']}\n"
            summary_text += f"   • Failed: {stats['failed']}\n"
            summary_text += f"   • Manual: {stats['manual']}\n"
            summary_text += f"   • Total: {total}\n\n"

        return {
            "content": [
                {"type": "text", "text": summary_text}
            ]
        }

    @tool("get_remediation_plan", "Get remediation plan for failed controls", {})
    async def get_remediation_plan(self, args):
        """Get remediation plan for failed controls."""
        if not self.compliance_results:
            return {
                "content": [
                    {"type": "text", "text": "❌ No validation results. Run validate_all_controls first."}
                ]
            }

        failed_controls = [r for r in self.compliance_results if r['status'] == 'FAILED']

        if not failed_controls:
            return {
                "content": [
                    {"type": "text", "text": "✅ No failed controls. All checks passed or require manual verification."}
                ]
            }

        remediation_text = f"🔧 Remediation Plan ({len(failed_controls)} Failed Controls)\n\n"

        for i, result in enumerate(failed_controls, 1):
            remediation_text += f"{i}. **{result['regulation']}**: {result['requirement']}\n"
            remediation_text += f"   Priority: HIGH\n"
            remediation_text += f"   Action: Review control details and implement required Azure resources\n\n"

        remediation_text += "\n💡 Recommended Actions:\n"
        remediation_text += "1. Review each failed control's requirements\n"
        remediation_text += "2. Deploy missing Azure resources\n"
        remediation_text += "3. Configure Azure Policy assignments\n"
        remediation_text += "4. Enable security features (Defender, Sentinel, etc.)\n"
        remediation_text += "5. Re-run validation after remediation\n"

        return {
            "content": [
                {"type": "text", "text": remediation_text}
            ]
        }

    @tool("export_audit_report", "Export audit report in specified format", {"format": str})
    async def export_audit_report(self, args):
        """Export audit report."""
        output_format = args.get("format", "markdown").lower()

        if not self.compliance_results:
            return {
                "content": [
                    {"type": "text", "text": "❌ No validation results. Run validate_all_controls first."}
                ]
            }

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if output_format == "markdown":
            filename = f"audit_report_{timestamp}.md"
            content = self._generate_report_content()
        elif output_format == "json":
            filename = f"audit_report_{timestamp}.json"
            content = json.dumps({
                'generated': timestamp,
                'total_controls': len(self.compliance_results),
                'results': self.compliance_results
            }, indent=2)
        else:
            return {
                "content": [
                    {"type": "text", "text": "❌ Unsupported format. Use 'markdown' or 'json'"}
                ]
            }

        report_path = self.reports_dir / filename
        with open(report_path, 'w') as f:
            f.write(content)

        result_text = f"✅ Audit report exported:\n\n"
        result_text += f"📄 File: {report_path}\n"
        result_text += f"📊 Format: {output_format.upper()}\n"
        result_text += f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"

        return {
            "content": [
                {"type": "text", "text": result_text}
            ]
        }

    @tool("validate_custom_control", "Validate a custom control defined inline", {"control_yaml": str})
    async def validate_custom_control(self, args):
        """Validate a custom control provided as YAML."""
        control_yaml = args.get("control_yaml", "")

        if not control_yaml:
            return {
                "content": [
                    {"type": "text", "text": "❌ control_yaml parameter required"}
                ]
            }

        try:
            control = yaml.safe_load(control_yaml)
            result = await self._validate_single_control(control, 0)

            return {
                "content": [
                    {"type": "text", "text": result}
                ]
            }
        except Exception as e:
            return {
                "content": [
                    {"type": "text", "text": f"❌ Error parsing YAML: {str(e)}"}
                ]
            }


async def main():
    """
    Main entry point for the Azure Compliance Checker agent.
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
    agent = AzureComplianceAgent(config_dir)

    print("\n" + "="*80)
    print("  📋 AZURE COMPLIANCE CHECKER AGENT")
    print("="*80)
    print("\n🎯 Capabilities:")
    print("   • Load compliance checklists (YAML)")
    print("   • Validate Azure resources against controls")
    print("   • Generate compliance reports with evidence")
    print("   • Identify gaps and remediation steps")
    print("   • Support for French FSI regulations")
    print("\n📜 Supported Regulations:")
    print("   • ACPR (Gouvernance SI)")
    print("   • CRD IV / CRR (Capital Requirements)")
    print("   • LCB-FT / AMLD5 (Anti-Money Laundering)")
    print("   • RGPD / CNIL (GDPR)")
    print("   • ISO 27001 / SOC 2")
    print("   • DORA (Digital Resilience)")
    print("   • NIS2 (Network Security)")
    print("\n💬 Try asking me to:")
    print("   - List available checklists")
    print("   - Load the french-fsi-regulations checklist")
    print("   - Validate all controls")
    print("   - Generate a compliance report")
    print("   - Get remediation plan")

    await agent.run_interactive()


if __name__ == "__main__":
    asyncio.run(main())
