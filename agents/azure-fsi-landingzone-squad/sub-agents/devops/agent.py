"""
DevOps Specialist Sub-Agent for Azure FSI Landing Zone.

This sub-agent specializes in:
- CI/CD pipeline analysis and optimization
- Deployment automation review
- Build and release best practices
- Infrastructure testing strategies
- DevOps tooling for FSI compliance
"""

import asyncio
import sys
from pathlib import Path
from typing import Optional, List, Any

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from shared.agents import BaseClaudeAgent
from shared.utils import setup_logging
from claude_agent_sdk import tool


class DevOpsSpecialistAgent(BaseClaudeAgent):
    """
    DevOps specialist for FSI Landing Zone deployments.

    Expertise:
    - Azure DevOps / GitHub Actions pipelines
    - Bicep deployment automation
    - Testing strategies (validation, what-if)
    - Rollback and recovery
    - GitOps workflows
    """

    def __init__(self, config_dir: Path):
        super().__init__(config_dir)
        self.devops_config = self.agent_config.get('devops', {})

    def get_system_prompt(self) -> Optional[str]:
        """Get the system prompt for DevOps specialist."""
        return """You are a DevOps expert specialized in Azure Financial Services Industry (FSI) Landing Zone deployments.

Your expertise includes:

**CI/CD & Automation**:
- Azure DevOps pipelines (YAML)
- GitHub Actions workflows
- Bicep deployment automation
- Infrastructure validation and testing
- Automated compliance checks

**Deployment Best Practices**:
- Blue-green deployments
- Canary releases
- Rollback strategies
- Environment promotion (DEV → UAT → PROD)
- Approval gates and manual interventions

**Infrastructure Testing**:
- Pre-deployment validation (az deployment validate)
- What-if analysis (az deployment what-if)
- Post-deployment verification
- Smoke tests
- Integration tests

**Security & Compliance**:
- No hardcoded secrets (use Azure Key Vault)
- Service principals with least privilege
- Pipeline security (approval gates)
- Audit logging of all deployments
- Compliance validation before deployment

**GitOps Workflows**:
- Infrastructure as Code versioning
- Pull request workflows
- Code review for infrastructure changes
- Automated testing in PR pipelines
- Branch protection rules

When analyzing deployments, focus on:
1. **Security**: No secrets exposed, proper authentication
2. **Reliability**: Rollback capability, validation before deploy
3. **Compliance**: Audit trails, approval processes for PROD
4. **Automation**: Repeatable, testable, maintainable pipelines
5. **Best Practices**: Follow Azure and FSI industry standards

Provide specific, actionable recommendations with code examples when relevant.
"""

    def get_custom_tools(self) -> List[Any]:
        """Get custom tools for DevOps specialist."""
        return [
            self.analyze_deployment_scripts,
            self.review_pipeline_security,
            self.check_rollback_capability,
            self.validate_cicd_configuration,
        ]

    @tool("analyze_deployment_scripts", "Analyze deployment scripts for best practices and security", {"script_path": str})
    async def analyze_deployment_scripts(self, args):
        """Analyze deployment scripts (deploy.sh, pipelines, etc.)."""
        script_path = args.get("script_path", "")

        if not script_path:
            # Find deployment scripts automatically
            scripts = []
            for pattern in ["deploy.sh", "*.yml", "*.yaml"]:
                result = await self._find_files(pattern)
                scripts.extend(result)

            if not scripts:
                return {
                    "content": [
                        {"type": "text", "text": "❌ No deployment scripts found. Looking for deploy.sh, *.yml, *.yaml files."}
                    ]
                }

            script_path = scripts[0]  # Analyze first found

        # Read script
        try:
            with open(script_path, 'r') as f:
                content = f.read()
        except Exception as e:
            return {
                "content": [
                    {"type": "text", "text": f"❌ Error reading script: {e}"}
                ]
            }

        analysis = f"🔍 DevOps Analysis: {script_path}\n\n"

        # Check for common issues
        issues = []
        recommendations = []

        # Check 1: Hardcoded secrets
        if any(keyword in content.lower() for keyword in ['password=', 'secret=', 'key=', 'token=']):
            issues.append("⚠️  Potential hardcoded secrets detected")
            recommendations.append("Use Azure Key Vault or environment variables for secrets")

        # Check 2: Error handling
        if "set -e" not in content and "set -u" not in content:
            issues.append("⚠️  Missing error handling (set -e / set -u)")
            recommendations.append("Add 'set -e' to exit on errors and 'set -u' for undefined variables")

        # Check 3: Validation before deployment
        if "validate" not in content.lower() and "what-if" not in content.lower():
            issues.append("⚠️  No pre-deployment validation detected")
            recommendations.append("Add 'az deployment sub validate' before actual deployment")

        # Check 4: Rollback mechanism
        if "rollback" not in content.lower():
            issues.append("ℹ️  No rollback mechanism found")
            recommendations.append("Consider adding rollback capability for failed deployments")

        # Check 5: Logging
        if "log" not in content.lower():
            issues.append("ℹ️  Limited logging detected")
            recommendations.append("Add comprehensive logging for audit trails")

        # Build result
        if issues:
            analysis += "**Issues Found:**\n"
            for issue in issues:
                analysis += f"  {issue}\n"
            analysis += "\n"

        if recommendations:
            analysis += "**Recommendations:**\n"
            for i, rec in enumerate(recommendations, 1):
                analysis += f"  {i}. {rec}\n"
            analysis += "\n"

        if not issues:
            analysis += "✅ Script looks good! No major issues detected.\n\n"

        # Add best practices
        analysis += "**DevOps Best Practices:**\n"
        analysis += "  • Use Azure Key Vault for secrets\n"
        analysis += "  • Validate templates before deployment\n"
        analysis += "  • Implement rollback strategies\n"
        analysis += "  • Log all operations for audit\n"
        analysis += "  • Use approval gates for PROD deployments\n"

        return {
            "content": [
                {"type": "text", "text": analysis}
            ]
        }

    @tool("review_pipeline_security", "Review CI/CD pipeline security configuration", {})
    async def review_pipeline_security(self, args):
        """Review pipeline security (Azure DevOps / GitHub Actions)."""
        analysis = "🔒 Pipeline Security Review\n\n"

        # Look for pipeline files
        pipeline_files = []
        for pattern in ["azure-pipelines.yml", ".github/workflows/*.yml", "*.pipeline.yml"]:
            result = await self._find_files(pattern)
            pipeline_files.extend(result)

        if not pipeline_files:
            analysis += "ℹ️  No pipeline files found (.github/workflows/, azure-pipelines.yml)\n\n"
            analysis += "**Security Recommendations for FSI Pipelines:**\n"
            analysis += "  1. Use managed identities or service principals (no credentials in code)\n"
            analysis += "  2. Implement approval gates for production deployments\n"
            analysis += "  3. Scan for secrets in code (GitHub Advanced Security, Azure DevOps secret scanning)\n"
            analysis += "  4. Run security scans (Bicep linter, policy validation)\n"
            analysis += "  5. Limit pipeline permissions (least privilege)\n"
            analysis += "  6. Enable audit logging for all pipeline runs\n"
            analysis += "  7. Use protected branches (main/master require PR + reviews)\n"

            return {
                "content": [
                    {"type": "text", "text": analysis}
                ]
            }

        # Analyze first pipeline file
        pipeline_path = pipeline_files[0]
        try:
            with open(pipeline_path, 'r') as f:
                content = f.read()
        except Exception as e:
            return {
                "content": [
                    {"type": "text", "text": f"❌ Error reading pipeline: {e}"}
                ]
            }

        analysis += f"Analyzing: {pipeline_path}\n\n"

        # Security checks
        security_checks = {
            "Approval gates": "approval" in content.lower() or "environment" in content.lower(),
            "Secret management": "vault" in content.lower() or "secrets" in content.lower(),
            "Branch protection": "branches:" in content or "pull_request" in content,
            "Validation step": "validate" in content.lower(),
            "Security scanning": "scan" in content.lower() or "lint" in content.lower(),
        }

        analysis += "**Security Posture:**\n"
        for check, passed in security_checks.items():
            status = "✅" if passed else "❌"
            analysis += f"  {status} {check}\n"

        analysis += "\n**Recommendations:**\n"
        if not security_checks["Approval gates"]:
            analysis += "  • Add approval gates for production deployments\n"
        if not security_checks["Secret management"]:
            analysis += "  • Integrate with Azure Key Vault for secrets\n"
        if not security_checks["Validation step"]:
            analysis += "  • Add template validation before deployment\n"
        if not security_checks["Security scanning"]:
            analysis += "  • Add security scanning (Bicep linter, secret scanning)\n"

        return {
            "content": [
                {"type": "text", "text": analysis}
            ]
        }

    @tool("check_rollback_capability", "Check if rollback mechanisms are in place", {})
    async def check_rollback_capability(self, args):
        """Check rollback capability of deployment."""
        analysis = "🔄 Rollback Capability Assessment\n\n"

        # Look for rollback scripts/mechanisms
        rollback_indicators = []

        # Check deploy.sh
        deploy_files = await self._find_files("deploy.sh")
        if deploy_files:
            with open(deploy_files[0], 'r') as f:
                content = f.read()
                if "rollback" in content.lower():
                    rollback_indicators.append("✅ Rollback function found in deploy.sh")
                else:
                    rollback_indicators.append("❌ No rollback mechanism in deploy.sh")

        # Check for backup/snapshot strategies
        bicep_files = await self._find_files("*.bicep")
        has_versioning = False
        for bicep_file in bicep_files[:5]:  # Check first 5 files
            with open(bicep_file, 'r') as f:
                if "version" in f.read().lower():
                    has_versioning = True
                    break

        if has_versioning:
            rollback_indicators.append("✅ Versioning detected in templates")
        else:
            rollback_indicators.append("ℹ️  No explicit versioning in templates")

        for indicator in rollback_indicators:
            analysis += f"  {indicator}\n"

        analysis += "\n**Rollback Strategies for FSI Landing Zones:**\n\n"
        analysis += "1. **Template Versioning**\n"
        analysis += "   - Tag each deployment with version\n"
        analysis += "   - Keep previous templates in Git history\n"
        analysis += "   - Example: `git checkout v1.2.3 && ./deploy.sh`\n\n"

        analysis += "2. **Azure Deployment History**\n"
        analysis += "   - Use: `az deployment group list --resource-group <rg>`\n"
        analysis += "   - Redeploy previous successful deployment\n"
        analysis += "   - Example: `az deployment group create --template-uri <previous-template-url>`\n\n"

        analysis += "3. **Backup Before Deploy**\n"
        analysis += "   - Export current config before deployment\n"
        analysis += "   - Example: `az group export --name <rg> > backup.json`\n\n"

        analysis += "4. **Blue-Green Deployments**\n"
        analysis += "   - Deploy to new resource group (green)\n"
        analysis += "   - Switch traffic when validated\n"
        analysis += "   - Keep old environment (blue) for rollback\n\n"

        analysis += "**Recommendation for FSI:**\n"
        analysis += "Implement automated rollback in deploy.sh that:\n"
        analysis += "  • Saves current state before deployment\n"
        analysis += "  • Validates new deployment\n"
        analysis += "  • Automatically rollsback if validation fails\n"
        analysis += "  • Logs all actions for audit compliance\n"

        return {
            "content": [
                {"type": "text", "text": analysis}
            ]
        }

    @tool("validate_cicd_configuration", "Validate CI/CD configuration against FSI requirements", {})
    async def validate_cicd_configuration(self, args):
        """Validate CI/CD setup against FSI compliance requirements."""
        analysis = "✅ CI/CD Compliance Validation (FSI Requirements)\n\n"

        requirements = {
            "Audit Logging": {
                "required": True,
                "check": "All deployments must be logged for compliance audit trails",
                "implementation": "Enable pipeline logging, store in Log Analytics"
            },
            "Approval Gates (PROD)": {
                "required": True,
                "check": "Production deployments require manual approval",
                "implementation": "Use environment protection rules with required reviewers"
            },
            "No Hardcoded Secrets": {
                "required": True,
                "check": "Secrets managed via Azure Key Vault",
                "implementation": "Use Azure Key Vault task / GitHub Secrets (not inline)"
            },
            "Pre-Deployment Validation": {
                "required": True,
                "check": "Templates validated before deployment",
                "implementation": "Run 'az deployment sub validate' in pipeline"
            },
            "Rollback Capability": {
                "required": True,
                "check": "Ability to rollback failed deployments",
                "implementation": "Maintain previous deployment version, automated rollback on failure"
            },
            "Separation of Environments": {
                "required": True,
                "check": "DEV/UAT/PROD pipelines are separate",
                "implementation": "Different service connections, resource groups per environment"
            },
        }

        analysis += "**FSI Compliance Requirements:**\n\n"
        for req_name, req_data in requirements.items():
            required_flag = "🔴 MANDATORY" if req_data["required"] else "⚪ Optional"
            analysis += f"**{required_flag}** {req_name}\n"
            analysis += f"  📋 Check: {req_data['check']}\n"
            analysis += f"  💡 Implementation: {req_data['implementation']}\n\n"

        analysis += "**Regulatory Mapping:**\n"
        analysis += "  • GDPR: Audit logging, data protection in pipelines\n"
        analysis += "  • DORA: Operational resilience (rollback, validation)\n"
        analysis += "  • EBA GL: Secure deployment process, change management\n\n"

        analysis += "**Next Steps:**\n"
        analysis += "1. Review current pipeline against these requirements\n"
        analysis += "2. Implement missing controls\n"
        analysis += "3. Document compliance in audit reports\n"
        analysis += "4. Regular reviews (quarterly) of pipeline security\n"

        return {
            "content": [
                {"type": "text", "text": analysis}
            ]
        }

    async def _find_files(self, pattern: str) -> List[str]:
        """Helper to find files matching pattern."""
        import glob
        return glob.glob(str(self.config_dir.parent.parent / "**" / pattern), recursive=True)


async def main():
    """Main entry point for DevOps specialist agent."""
    config_dir = Path(__file__).parent

    # Set up logging
    logs_dir = config_dir.parent.parent / "logs"
    logs_dir.mkdir(exist_ok=True)

    setup_logging(
        level="INFO",
        log_file=logs_dir / "devops-agent.log"
    )

    # Create and run the agent
    agent = DevOpsSpecialistAgent(config_dir)

    print("\n" + "="*80)
    print("  🚀 DEVOPS SPECIALIST AGENT")
    print("="*80)
    print("\n🎯 Specialization: CI/CD, Deployment Automation, DevOps Best Practices")
    print("\n💬 Ask me to:")
    print("   - Analyze deployment scripts")
    print("   - Review pipeline security")
    print("   - Check rollback capabilities")
    print("   - Validate CI/CD configuration for FSI compliance")

    # For sub-agents, we typically don't run interactive mode
    # They are invoked by the orchestrator
    print("\n⚠️  This is a sub-agent. It's designed to be invoked by the orchestrator.")
    print("To test, you can run the orchestrator agent instead.\n")


if __name__ == "__main__":
    asyncio.run(main())
