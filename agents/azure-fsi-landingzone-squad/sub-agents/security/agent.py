"""
Security Specialist Sub-Agent for Azure FSI Landing Zone.

This sub-agent specializes in:
- FSI compliance validation (GDPR, DORA, PSD2, etc.)
- Security policies analysis
- Key Vault configuration review
- Network security assessment
- Entra ID and access control
"""

import asyncio
import sys
import json
from pathlib import Path
from typing import Optional, List, Any

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from shared.agents import BaseClaudeAgent
from shared.utils import setup_logging
from claude_agent_sdk import tool


class SecuritySpecialistAgent(BaseClaudeAgent):
    """
    Security specialist for FSI Landing Zone compliance.

    Expertise:
    - GDPR, DORA, PSD2, MiFID II, EBA Guidelines
    - Azure Policies and governance
    - Key Vault, secrets management
    - Network security (NSGs, Firewall)
    - Entra ID, PIM, Conditional Access
    """

    def __init__(self, config_dir: Path):
        super().__init__(config_dir)
        self.security_config = self.agent_config.get('security', {})

    def get_system_prompt(self) -> Optional[str]:
        """Get the system prompt for Security specialist."""
        return """You are a Security and Compliance expert specialized in Azure Financial Services Industry (FSI) Landing Zones.

Your expertise includes:

**FSI Compliance Frameworks**:
- GDPR (General Data Protection Regulation)
- DORA (Digital Operational Resilience Act)
- PSD2 (Payment Services Directive 2)
- MiFID II (Markets in Financial Instruments Directive)
- EBA Guidelines (European Banking Authority)
- ISO 27001, NIST frameworks

**Security Controls**:
- Azure Policies for compliance enforcement
- Key Vault configuration (purge protection, soft delete, RBAC)
- Network Security Groups (NSG) rules validation
- Azure Firewall policies
- Private endpoints for PaaS services
- Encryption at rest and in transit (CMK preferred)
- No public IP addresses (deny policy)

**Identity & Access Management**:
- Entra ID (Azure AD) configuration
- Privileged Identity Management (PIM)
- Conditional Access policies
- Multi-Factor Authentication (MFA)
- RBAC with least privilege
- Service principals security

**Data Protection**:
- Data residency (EU regions only)
- Customer-managed keys (CMK)
- Double encryption for sensitive data
- Data classification and handling
- Backup and disaster recovery
- Immutable storage for audit logs

**Security Baseline**:
- Microsoft Cloud Security Benchmark (MCSB)
- Azure Security Center / Defender for Cloud
- Security posture assessment
- Vulnerability management
- Threat protection

When analyzing infrastructure, focus on:
1. **Compliance**: Map controls to GDPR/DORA/PSD2 requirements
2. **Security**: Identify vulnerabilities and misconfigurations
3. **Best Practices**: Follow Microsoft and industry standards
4. **Auditability**: Ensure all actions are logged and traceable
5. **Defense in Depth**: Multiple layers of security

Provide specific findings with:
- Severity (Critical, High, Medium, Low, Info)
- Compliance mapping (which regulation requires this)
- Remediation steps with code examples
- References to official documentation
"""

    def get_custom_tools(self) -> List[Any]:
        """Get custom tools for Security specialist."""
        return [
            self.audit_key_vault_security,
            self.analyze_nsg_rules,
            self.check_compliance_policies,
            self.validate_encryption_config,
            self.review_iam_configuration,
        ]

    @tool("audit_key_vault_security", "Audit Azure Key Vault security configuration", {})
    async def audit_key_vault_security(self, args):
        """Audit Key Vault security settings."""
        analysis = "🔐 Key Vault Security Audit\n\n"

        # Check local Key Vault templates
        kv_files = await self._find_files("*key-vault*.bicep")

        if not kv_files:
            analysis += "ℹ️  No Key Vault templates found locally\n\n"
        else:
            analysis += f"**Local Templates Analysis** ({len(kv_files)} files)\n\n"

            for kv_file in kv_files[:3]:  # Analyze first 3
                with open(kv_file, 'r') as f:
                    content = f.read()

                analysis += f"📄 {Path(kv_file).name}:\n"

                checks = {
                    "Soft Delete": "enableSoftDelete" in content and "true" in content,
                    "Purge Protection": "enablePurgeProtection" in content and "true" in content,
                    "RBAC": "enableRbacAuthorization" in content and "true" in content,
                    "Network ACLs": "networkAcls" in content,
                    "Private Endpoint": "privateEndpoint" in content.lower(),
                    "Diagnostic Settings": "diagnosticSettings" in content or "Microsoft.Insights" in content,
                }

                for check_name, passed in checks.items():
                    status = "✅" if passed else "❌"
                    analysis += f"  {status} {check_name}\n"

                analysis += "\n"

        # FSI Requirements
        analysis += "**FSI Compliance Requirements:**\n\n"

        requirements = {
            "GDPR": [
                "✅ Soft delete enabled (90 days retention)",
                "✅ Purge protection enabled (prevent permanent deletion)",
                "✅ Diagnostic logs forwarded to Log Analytics",
                "✅ Access logged for audit trails"
            ],
            "PSD2": [
                "✅ Customer-managed keys (CMK) for sensitive data",
                "✅ RBAC authorization (no access policies)",
                "✅ Private endpoint (no public access)",
                "✅ Network restrictions (deny by default)"
            ],
            "DORA": [
                "✅ Backup and recovery capability (soft delete)",
                "✅ Operational resilience (geo-redundant)",
                "✅ Monitoring and alerting (diagnostic settings)",
                "✅ Access control (MFA + PIM)"
            ]
        }

        for framework, reqs in requirements.items():
            analysis += f"**{framework}:**\n"
            for req in reqs:
                analysis += f"  {req}\n"
            analysis += "\n"

        # Recommendations
        analysis += "**Security Recommendations:**\n"
        analysis += "1. Enable purge protection (MANDATORY for FSI)\n"
        analysis += "2. Use RBAC instead of access policies\n"
        analysis += "3. Configure private endpoints (no public access)\n"
        analysis += "4. Enable diagnostic settings with 365-day retention\n"
        analysis += "5. Use Premium SKU for HSM-backed keys\n"
        analysis += "6. Implement key rotation policies\n"
        analysis += "7. Use separate Key Vaults per environment (DEV/UAT/PROD)\n"

        return {
            "content": [
                {"type": "text", "text": analysis}
            ]
        }

    @tool("analyze_nsg_rules", "Analyze Network Security Group rules for vulnerabilities", {})
    async def analyze_nsg_rules(self, args):
        """Analyze NSG rules for security issues."""
        analysis = "🛡️ Network Security Group (NSG) Analysis\n\n"

        # Check local NSG templates
        nsg_files = await self._find_files("*nsg*.bicep")

        if not nsg_files:
            analysis += "ℹ️  No NSG templates found\n\n"
        else:
            analysis += f"**Local NSG Templates** ({len(nsg_files)} files)\n\n"

            for nsg_file in nsg_files[:3]:
                with open(nsg_file, 'r') as f:
                    content = f.read()

                analysis += f"📄 {Path(nsg_file).name}:\n"

                # Check for dangerous patterns
                dangerous_patterns = {
                    "Port 22 (SSH) open to internet": ("22" in content and "0.0.0.0" in content),
                    "Port 3389 (RDP) open to internet": ("3389" in content and "0.0.0.0" in content),
                    "Port 80 (HTTP) allowed": ("80" in content and "Allow" in content),
                    "Wildcard source (*)": ("*" in content and "sourceAddressPrefix" in content),
                    "Allow Any protocol": ("protocol" in content.lower() and "\\*" in content),
                }

                issues_found = []
                for pattern_name, detected in dangerous_patterns.items():
                    if detected:
                        issues_found.append(f"    ⚠️  {pattern_name}")

                if issues_found:
                    analysis += "  **Security Issues:**\n"
                    analysis += "\n".join(issues_found) + "\n"
                else:
                    analysis += "  ✅ No obvious security issues detected\n"

                analysis += "\n"

        # Best practices
        analysis += "**FSI NSG Best Practices:**\n\n"

        best_practices = [
            "1. **Deny by Default**: Default rule should deny all traffic",
            "2. **No Public Ports**: SSH/RDP only via Azure Bastion (no direct internet access)",
            "3. **Specific Sources**: Use specific IP ranges, never 0.0.0.0/0 or *",
            "4. **Service Tags**: Use Azure service tags instead of IP ranges",
            "5. **Application Security Groups**: Group VMs by role/function",
            "6. **Logging**: Enable NSG flow logs for audit and threat detection",
            "7. **Review Regularly**: Audit rules quarterly for compliance"
        ]

        for practice in best_practices:
            analysis += f"  {practice}\n"

        analysis += "\n**Critical Rules for FSI:**\n"
        analysis += "  ❌ DENY: Port 22 (SSH) from Internet\n"
        analysis += "  ❌ DENY: Port 3389 (RDP) from Internet\n"
        analysis += "  ❌ DENY: Any port from 0.0.0.0/0\n"
        analysis += "  ✅ ALLOW: Azure Bastion subnet → Management subnet\n"
        analysis += "  ✅ ALLOW: Application subnet → Database subnet (specific ports)\n"
        analysis += "  ✅ ALLOW: AzureLoadBalancer service tag\n"

        return {
            "content": [
                {"type": "text", "text": analysis}
            ]
        }

    @tool("check_compliance_policies", "Check Azure Policy compliance status", {})
    async def check_compliance_policies(self, args):
        """Check compliance with Azure Policies."""
        analysis = "📜 Azure Policy Compliance Check\n\n"

        # Check local policy templates
        policy_files = await self._find_files("*polic*.bicep")

        if policy_files:
            analysis += f"**Policy Templates Found** ({len(policy_files)} files)\n\n"

            for policy_file in policy_files[:3]:
                with open(policy_file, 'r') as f:
                    content = f.read()

                analysis += f"📄 {Path(policy_file).name}:\n"

                # Check for FSI-specific policies
                fsi_policies = {
                    "Data Residency (EU)": "location" in content.lower() and ("europe" in content.lower() or "france" in content.lower()),
                    "Encryption Required": "encryption" in content.lower(),
                    "Private Endpoints": "privateEndpoint" in content,
                    "No Public IPs": "publicIP" in content and "Deny" in content,
                    "Diagnostic Settings": "diagnosticSettings" in content,
                }

                for policy_name, detected in fsi_policies.items():
                    status = "✅" if detected else "⚪"
                    analysis += f"  {status} {policy_name}\n"

                analysis += "\n"

        # Compliance frameworks
        analysis += "**Required Policy Initiatives for FSI:**\n\n"

        initiatives = {
            "GDPR": "Enforce data protection and privacy controls",
            "Azure Security Benchmark": "Microsoft Cloud Security Benchmark (MCSB)",
            "CIS Azure Foundations": "Center for Internet Security best practices",
            "NIST SP 800-53": "US government security controls",
            "ISO 27001": "Information security management",
        }

        for initiative, description in initiatives.items():
            analysis += f"  📋 **{initiative}**\n"
            analysis += f"     {description}\n\n"

        # Custom policies for FSI
        analysis += "**Custom Policies for European FSI:**\n\n"

        custom_policies = [
            {
                "name": "Data Residency (EU Only)",
                "effect": "Deny",
                "requirement": "GDPR Article 44 - Transfers outside EU",
                "config": "Allowed locations: westeurope, northeurope, francecentral, germanywestcentral"
            },
            {
                "name": "Require Customer-Managed Keys",
                "effect": "Deny",
                "requirement": "PSD2 - Strong authentication and encryption",
                "config": "All encryption must use CMK from Key Vault"
            },
            {
                "name": "Deny Public IPs",
                "effect": "Deny",
                "requirement": "EBA Guidelines - Network isolation",
                "config": "No public IP addresses allowed (use Private Link)"
            },
            {
                "name": "Require Diagnostic Settings",
                "effect": "Audit",
                "requirement": "DORA - Operational resilience monitoring",
                "config": "All resources must send logs to Log Analytics"
            },
        ]

        for policy in custom_policies:
            analysis += f"  🔒 **{policy['name']}**\n"
            analysis += f"     Effect: {policy['effect']}\n"
            analysis += f"     Requirement: {policy['requirement']}\n"
            analysis += f"     Config: {policy['config']}\n\n"

        analysis += "**Next Steps:**\n"
        analysis += "1. Deploy policy initiatives at subscription/management group level\n"
        analysis += "2. Run compliance scan: `az policy state list --filter \"complianceState eq 'NonCompliant'\"`\n"
        analysis += "3. Remediate non-compliant resources\n"
        analysis += "4. Schedule quarterly compliance reviews\n"

        return {
            "content": [
                {"type": "text", "text": analysis}
            ]
        }

    @tool("validate_encryption_config", "Validate encryption configuration (at rest & in transit)", {})
    async def validate_encryption_config(self, args):
        """Validate encryption settings."""
        analysis = "🔐 Encryption Configuration Validation\n\n"

        # Check storage accounts
        storage_files = await self._find_files("*storage*.bicep")

        if storage_files:
            analysis += "**Storage Account Encryption:**\n\n"

            for storage_file in storage_files[:3]:
                with open(storage_file, 'r') as f:
                    content = f.read()

                encryption_checks = {
                    "HTTPS Only": "supportsHttpsTrafficOnly" in content and "true" in content,
                    "TLS 1.2 Minimum": "minimumTlsVersion" in content and "TLS1_2" in content,
                    "Infrastructure Encryption": "requireInfrastructureEncryption" in content,
                    "CMK (Customer-Managed Keys)": "keySource" in content and "Microsoft.Keyvault" in content,
                    "Blob Versioning": "isVersioningEnabled" in content,
                }

                analysis += f"📄 {Path(storage_file).name}:\n"
                for check, passed in encryption_checks.items():
                    status = "✅" if passed else "❌"
                    analysis += f"  {status} {check}\n"
                analysis += "\n"

        # Encryption requirements by regulation
        analysis += "**Encryption Requirements by Regulation:**\n\n"

        analysis += "**GDPR (Article 32 - Security of Processing):**\n"
        analysis += "  ✅ Encryption of personal data at rest\n"
        analysis += "  ✅ Encryption in transit (TLS 1.2+)\n"
        analysis += "  ✅ Pseudonymization where applicable\n"
        analysis += "  ✅ Regular testing of security measures\n\n"

        analysis += "**PSD2 (Strong Customer Authentication):**\n"
        analysis += "  ✅ Customer-managed keys (CMK) recommended\n"
        analysis += "  ✅ Double encryption for payment data\n"
        analysis += "  ✅ Secure communication channels (TLS 1.2+)\n"
        analysis += "  ✅ Key rotation policies\n\n"

        analysis += "**DORA (ICT Risk Management):**\n"
        analysis += "  ✅ Encryption for operational resilience\n"
        analysis += "  ✅ Backup encryption (geo-redundant)\n"
        analysis += "  ✅ Encryption key management procedures\n"
        analysis += "  ✅ Regular encryption audits\n\n"

        # Best practices
        analysis += "**Encryption Best Practices for FSI:**\n\n"

        best_practices = [
            "1. Use Premium SKU Key Vault for HSM-backed keys",
            "2. Enable double encryption for highly sensitive data",
            "3. Use customer-managed keys (CMK) instead of Microsoft-managed",
            "4. Rotate keys regularly (e.g., every 90 days)",
            "5. Enable soft delete and purge protection on Key Vault",
            "6. Use TLS 1.2 minimum (disable TLS 1.0/1.1)",
            "7. Encrypt backups and snapshots",
            "8. Use Azure Disk Encryption for VM disks",
            "9. Enable encryption in transit for all PaaS services",
            "10. Document encryption strategy for compliance audits"
        ]

        for practice in best_practices:
            analysis += f"  {practice}\n"

        return {
            "content": [
                {"type": "text", "text": analysis}
            ]
        }

    @tool("review_iam_configuration", "Review Identity and Access Management configuration", {})
    async def review_iam_configuration(self, args):
        """Review IAM (Entra ID, RBAC, PIM) configuration."""
        analysis = "👤 Identity & Access Management Review\n\n"

        # Check for Entra ID / Conditional Access templates
        iam_files = await self._find_files("*entra*.bicep") + await self._find_files("*conditional*.json")

        if iam_files:
            analysis += f"**IAM Templates Found** ({len(iam_files)} files)\n\n"

            for iam_file in iam_files[:3]:
                analysis += f"📄 {Path(iam_file).name}\n"
                with open(iam_file, 'r') as f:
                    content = f.read()

                # Check for key IAM features
                iam_features = {
                    "MFA Required": "mfa" in content.lower(),
                    "Conditional Access": "conditionalAccess" in content,
                    "PIM (Privileged Identity Management)": "pim" in content.lower() or "privileged" in content.lower(),
                    "RBAC": "roleAssignment" in content or "rbac" in content.lower(),
                }

                for feature, detected in iam_features.items():
                    status = "✅" if detected else "⚪"
                    analysis += f"  {status} {feature}\n"
                analysis += "\n"

        # FSI IAM requirements
        analysis += "**FSI IAM Requirements:**\n\n"

        analysis += "**1. Multi-Factor Authentication (MFA)**\n"
        analysis += "   • Requirement: PSD2, DORA\n"
        analysis += "   • All users must enable MFA\n"
        analysis += "   • Use Conditional Access to enforce\n"
        analysis += "   • Block legacy authentication\n\n"

        analysis += "**2. Privileged Identity Management (PIM)**\n"
        analysis += "   • Requirement: DORA, EBA GL\n"
        analysis += "   • Just-in-time admin access\n"
        analysis += "   • Maximum activation: 8 hours\n"
        analysis += "   • Approval required for Global Admin\n"
        analysis += "   • MFA on activation\n\n"

        analysis += "**3. Conditional Access Policies**\n"
        analysis += "   • Block access from non-EU locations (GDPR)\n"
        analysis += "   • Require compliant devices\n"
        analysis += "   • Require MFA for all cloud apps\n"
        analysis += "   • Block legacy authentication protocols\n"
        analysis += "   • Session controls for sensitive apps\n\n"

        analysis += "**4. RBAC (Role-Based Access Control)**\n"
        analysis += "   • Least privilege principle\n"
        analysis += "   • No permanent Owner assignments\n"
        analysis += "   • Use built-in roles when possible\n"
        analysis += "   • Regular access reviews (quarterly)\n"
        analysis += "   • Separation of duties\n\n"

        # Break-glass account
        analysis += "**⚠️  Break-Glass Account (Emergency Access):**\n"
        analysis += "   • Create 2 cloud-only accounts\n"
        analysis += "   • Permanent Global Administrator\n"
        analysis += "   • Excluded from Conditional Access\n"
        analysis += "   • Excluded from MFA\n"
        analysis += "   • Credentials in physical safe\n"
        analysis += "   • Monitored for any sign-in activity\n\n"

        # Compliance mapping
        analysis += "**Compliance Mapping:**\n"
        analysis += "   🏛️  **GDPR**: Data access control, audit logging\n"
        analysis += "   🏛️  **DORA**: Privileged access management, resilience\n"
        analysis += "   🏛️  **PSD2**: Strong customer authentication (MFA)\n"
        analysis += "   🏛️  **EBA GL**: Identity governance, access reviews\n\n"

        analysis += "**Next Steps:**\n"
        analysis += "1. Enable Security Defaults or Conditional Access\n"
        analysis += "2. Configure PIM for all privileged roles\n"
        analysis += "3. Create break-glass accounts\n"
        analysis += "4. Set up Conditional Access policies\n"
        analysis += "5. Schedule quarterly access reviews\n"

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
    """Main entry point for Security specialist agent."""
    config_dir = Path(__file__).parent

    # Set up logging
    logs_dir = config_dir.parent.parent / "logs"
    logs_dir.mkdir(exist_ok=True)

    setup_logging(
        level="INFO",
        log_file=logs_dir / "security-agent.log"
    )

    # Create agent
    agent = SecuritySpecialistAgent(config_dir)

    print("\n" + "="*80)
    print("  🔒 SECURITY SPECIALIST AGENT")
    print("="*80)
    print("\n🎯 Specialization: FSI Compliance, Security Policies, Hardening")
    print("\n💬 Ask me to:")
    print("   - Audit Key Vault security")
    print("   - Analyze NSG rules for vulnerabilities")
    print("   - Check compliance policies (GDPR, DORA, PSD2)")
    print("   - Validate encryption configuration")
    print("   - Review IAM configuration (Entra ID, PIM)")

    print("\n⚠️  This is a sub-agent. It's designed to be invoked by the orchestrator.")
    print("To test, you can run the orchestrator agent instead.\n")


if __name__ == "__main__":
    asyncio.run(main())
