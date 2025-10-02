# Azure Compliance Checker Agent

An AI-powered compliance validation agent for Azure infrastructure, built with Claude Agent SDK.

## Overview

This agent validates Azure infrastructure against user-defined compliance controls for French Financial Services regulations. It automatically checks Azure resources, policies, and configurations to ensure regulatory compliance.

### Supported Regulations

- **ACPR** (Autorité de Contrôle Prudentiel et de Résolution) - Gouvernance SI
- **CRD IV / CRR** - Capital Requirements Directive/Regulation
- **LCB-FT / AMLD5** - Anti-Money Laundering Directive (5th EU Directive)
- **RGPD / CNIL** - GDPR and French Data Protection Authority
- **ISO 27001 / SOC 2** - Information Security Management Standards
- **DORA** (2025) - Digital Operational Resilience Act
- **NIS2** (2024/25) - Network and Information Security Directive

## Features

### 🔍 Automated Compliance Validation
- Load compliance checklists from YAML files
- Validate Azure resources against control requirements
- Check Azure Policy assignments and configurations
- Verify security settings (encryption, private endpoints, etc.)
- Automated evidence collection

### 📊 Comprehensive Reporting
- Generate compliance reports with pass/fail status
- Evidence-based validation results
- Compliance rate by regulation
- Gap analysis and remediation plans
- Export to Markdown or JSON

### 🎯 French FSI Focus
- Pre-built checklist for French financial regulations
- Mapping of regulatory requirements to Azure controls
- Support for ACPR, CNIL, AMF, ACAM requirements
- European data residency validation

### 🛠️ Flexible Control Definition
- YAML-based control checklists
- Custom control validation
- Manual verification workflow support
- Extensible validation logic

## Agent Capabilities

### Custom Tools (10 total)

1. **list_available_checklists** - List all compliance checklists
2. **load_compliance_checklist** - Load a checklist from file
3. **validate_control** - Validate a specific control by index
4. **validate_all_controls** - Validate all controls in checklist
5. **check_azure_resource** - Check specific Azure resource types
6. **generate_compliance_report** - Generate detailed compliance report
7. **get_compliance_summary** - Get summary by regulation
8. **get_remediation_plan** - Get remediation steps for failures
9. **export_audit_report** - Export audit report (Markdown/JSON)
10. **validate_custom_control** - Validate custom YAML control

## Prerequisites

1. **Azure CLI** (authenticated)
   ```bash
   az login
   az account set --subscription <subscription-id>
   ```

2. **Python 3.10+** with dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. **Anthropic API Key**
   ```bash
   export ANTHROPIC_API_KEY="your-key-here"
   ```

## Quick Start

### 1. Run the Agent

```bash
cd agents/azure-compliance-checker
python agent.py
```

### 2. Basic Workflow

```
💬 You: List available checklists

🤖 Agent: [Shows available compliance checklists]

💬 You: Load french-fsi-regulations.yaml

🤖 Agent: [Loads checklist with 24 controls across 7 regulations]

💬 You: Validate all controls

🤖 Agent: [Validates all controls, shows progress and summary]

💬 You: Generate compliance report

🤖 Agent: [Creates detailed Markdown report with evidence]

💬 You: Get remediation plan

🤖 Agent: [Lists failed controls with remediation steps]
```

## Compliance Checklist Format

Checklists are defined in YAML format in the `checklists/` directory.

### Example Control

```yaml
checklist:
  - reglementation: "RGPD / CNIL"
    exigence: "Protection données"
    preuve: "Certificat chiffrement DB"
    controle: "Activer TDE (Transparent Data Encryption) sur SQL MI"
    azure_resources:
      - type: "Microsoft.Sql/managedInstances/databases"
        required: true
        validation:
          - property: "properties.transparentDataEncryption.state"
            check: "equals"
            value: "Enabled"
```

### Control Structure

- **reglementation**: Regulatory framework (e.g., "RGPD / CNIL")
- **exigence**: Requirement description
- **preuve**: Evidence required for auditors
- **controle**: Control to be validated
- **azure_resources**: List of Azure resource types to check
  - **type**: Azure resource type (e.g., `Microsoft.KeyVault/vaults`)
  - **required**: Whether the resource must exist (boolean)
  - **validation**: List of property validations
    - **property**: JSON path to property
    - **check**: Validation type (`equals`, `exists`, `contains`, `greaterThan`, etc.)
    - **value**: Expected value

### Validation Types

- **exists**: Property must exist
- **equals**: Property must equal specific value
- **contains**: Property must contain substring/value
- **containsAny**: Property must contain any of the values
- **greaterThan**: Numeric comparison
- **greaterThanOrEqual**: Numeric comparison
- **in**: Value must be in list

### Manual Verification

For controls requiring manual verification:

```yaml
  - reglementation: "LCB-FT / AMLD5"
    exigence: "KYC/KYB"
    preuve: "Rapports KYC clients/garants"
    controle: "Intégrer Dotfile/ComplyAdvantage aux workflows"
    manual_verification: true
    notes: "Verify integration with KYC/KYB provider"
```

## Included Checklist: French FSI Regulations

The agent includes a comprehensive checklist covering:

### ACPR – Gouvernance SI (3 controls)
- ✅ Continuité (PRA/DRP)
- ✅ Journalisation
- ✅ Gouvernance Cloud

### CRD IV / CRR (3 controls)
- ✅ Gestion incidents
- ✅ Disponibilité
- ✅ Traçabilité

### LCB-FT / AMLD5 (3 controls)
- ✅ KYC/KYB
- ✅ Screening sanctions
- ✅ Preuve audit AML

### RGPD / CNIL (4 controls)
- ✅ Protection données
- ✅ Sécurité clés
- ✅ Souveraineté
- ✅ Traçabilité accès

### ISO 27001 / SOC 2 (3 controls)
- ✅ Contrôles sécurité
- ✅ Preuves conformité
- ✅ Détection incidents

### DORA (2025) (3 controls)
- ✅ Résilience IT
- ✅ Cyber incidents
- ✅ Réponse incidents

### NIS2 (2024/25) (3 controls)
- ✅ Inventaire actifs
- ✅ Gestion vulnérabilités
- ✅ Risk Management

**Total: 24 controls across 7 regulatory frameworks**

## Usage Examples

### Example 1: Full Compliance Audit

```
You: Load french-fsi-regulations.yaml
Agent: ✅ Loaded 24 controls across 7 regulations

You: Validate all controls
Agent: [Validates all controls]
      📊 Compliance Rate: 87.5%
      ✅ Passed: 21
      ❌ Failed: 2
      ⚠️  Manual: 1

You: Generate compliance report
Agent: ✅ Report saved to: reports/compliance_report_20250102_143000.md

You: Get remediation plan
Agent: 🔧 Remediation Plan (2 Failed Controls)
      1. RGPD / CNIL: Souveraineté
         Action: Apply Azure Policy for EU-only locations
      2. ISO 27001: Contrôles sécurité
         Action: Enable ISO 27001 policy initiative
```

### Example 2: Check Specific Resource

```
You: Check Azure resource Microsoft.KeyVault/vaults

Agent: 🔍 Checking Azure Resource Type: Microsoft.KeyVault/vaults

       Found: 3 resource(s)

       1. fsi-kv-prod
          • Location: westeurope
          • Resource Group: fsi-security-rg
          • SKU: Premium

       2. fsi-kv-dev
          • Location: francecentral
          • Resource Group: fsi-dev-rg
          • SKU: Standard
```

### Example 3: Validate Custom Control

```
You: Validate this custom control:
reglementation: "Custom Policy"
exigence: "Network Security"
preuve: "NSG rules configured"
controle: "Check NSG exists"
azure_resources:
  - type: "Microsoft.Network/networkSecurityGroups"
    required: true

Agent: ✅ Control validated
       Found 15 Network Security Groups
       Status: PASSED
```

## Generated Reports

### Compliance Report Structure

```markdown
# Azure Compliance Report

**Generated**: 2025-01-02 14:30:00

## Executive Summary

- **Total Controls**: 24
- **Passed**: 21 (87.5%)
- **Failed**: 2 (8.3%)
- **Manual Review**: 1 (4.2%)

## Compliance by Regulation

### RGPD / CNIL
- **Compliance Rate**: 75.0%
- **Passed**: 3/4

### DORA (2025)
- **Compliance Rate**: 100.0%
- **Passed**: 3/3

## Detailed Results

### ✅ Control #1: Protection données
**Regulation**: RGPD / CNIL
**Status**: PASSED

- Found: 2 SQL Managed Instance databases
- TDE Status: Enabled
- Evidence: Transparent Data Encryption active
```

## Integration with FSI Landing Zone

This compliance agent complements the [Azure FSI Landing Zone Agent](../azure-fsi-landingzone/README.md):

1. **Deploy** infrastructure using FSI Landing Zone agent
2. **Validate** compliance using Compliance Checker agent
3. **Remediate** gaps identified in compliance reports
4. **Re-validate** after remediation
5. **Generate** audit reports for regulators

### Workflow

```
┌─────────────────────────┐
│ FSI Landing Zone Agent  │ → Deploy compliant infrastructure
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ Compliance Checker      │ → Validate against regulations
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ Remediation             │ → Fix identified gaps
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ Re-validation & Report  │ → Audit-ready evidence
└─────────────────────────┘
```

## Configuration

See [config.yaml](config.yaml) for configuration options:

```yaml
compliance:
  # Validation settings
  validation:
    strict_mode: false      # Fail on warnings
    skip_manual: false      # Skip manual controls
    parallel: false         # Parallel validation
    cache_duration: 300     # Cache results (seconds)

  # Report settings
  reports:
    default_format: "markdown"
    include_evidence: true
    include_remediation: true
    compliance_warning_threshold: 80
    compliance_critical_threshold: 50
```

## Azure Resource Types Validated

The agent can validate these Azure resource types (and more):

### Security & Governance
- `Microsoft.Authorization/policyAssignments`
- `Microsoft.Security/pricings`
- `Microsoft.Security/assessments`
- `Microsoft.SecurityInsights/alertRules`
- `Microsoft.SecurityInsights/incidents`

### Identity & Access
- `Microsoft.KeyVault/vaults`
- `Microsoft.Insights/diagnosticSettings`

### Data Protection
- `Microsoft.Sql/servers/databases`
- `Microsoft.Sql/managedInstances/databases`
- `Microsoft.Storage/storageAccounts`
- `Microsoft.Storage/storageAccounts/blobServices/containers`

### Monitoring & Recovery
- `Microsoft.OperationalInsights/workspaces`
- `Microsoft.RecoveryServices/vaults`
- `Microsoft.Insights/metricAlerts`

### Automation
- `Microsoft.Logic/workflows`
- `Microsoft.Automation/automationAccounts/runbooks`

## Troubleshooting

### Azure CLI Not Authenticated
```bash
# Re-authenticate
az login

# Verify
az account show
```

### No Resources Found
```bash
# Check subscription
az account show

# List all resources
az resource list --output table

# Check resource type syntax
az provider show --namespace Microsoft.KeyVault --query "resourceTypes[].resourceType"
```

### Validation Timeout
```yaml
# Increase timeout in config.yaml
compliance:
  azure:
    query_timeout: 60  # Increase from 30 to 60 seconds
```

### Permission Issues
```bash
# Check your roles
az role assignment list --assignee <your-upn> --all

# Required: Reader role minimum
# Recommended: Security Reader for compliance data
```

## Creating Custom Checklists

### 1. Create YAML File

```bash
# Create new checklist
touch checklists/my-custom-regulations.yaml
```

### 2. Define Controls

```yaml
checklist:
  - reglementation: "My Regulation"
    exigence: "Requirement description"
    preuve: "Evidence needed"
    controle: "What to validate"
    azure_resources:
      - type: "Microsoft.ResourceType"
        required: true
        validation:
          - property: "properties.setting"
            check: "equals"
            value: "expected_value"
```

### 3. Load and Validate

```
You: Load my-custom-regulations.yaml
Agent: ✅ Loaded checklist

You: Validate all controls
Agent: [Validates your custom controls]
```

## Best Practices

### 1. Regular Validation
- Run compliance checks weekly
- Validate after infrastructure changes
- Schedule automated validation (CI/CD)

### 2. Evidence Collection
- Keep generated reports for audits
- Archive reports with timestamps
- Document remediation actions

### 3. Continuous Improvement
- Update checklists when regulations change
- Add new controls as requirements evolve
- Review and refine validation logic

### 4. Collaboration
- Share checklists across teams
- Version control checklist files
- Document custom controls

## Limitations

### Current Limitations
1. **Azure CLI dependency**: Requires Azure CLI and authentication
2. **Property validation**: Basic validation logic (can be enhanced)
3. **No real-time monitoring**: Point-in-time validation only
4. **Manual controls**: Some controls require manual verification
5. **Resource Graph**: Not yet implemented (coming soon)

### Planned Enhancements
- [ ] Azure Resource Graph integration (faster queries)
- [ ] Advanced property validation (JSONPath, complex logic)
- [ ] Continuous monitoring mode
- [ ] Policy-as-Code generation
- [ ] Integration with GRC tools (Delve, Scytale)
- [ ] Multi-subscription support
- [ ] HTML report format
- [ ] Dashboard visualization

## Support

For issues or questions:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review the example checklist format
3. Test with a simple custom control
4. Check Azure CLI authentication and permissions

## License

[Add license information]

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add your controls or enhancements
4. Submit a pull request

### Contributing Checklists

We welcome contributions of compliance checklists for:
- Other EU regulations (e.g., MiCA, DAC8)
- Industry-specific requirements
- Country-specific regulations
- Internal compliance frameworks

---

**⚠️ Important**: This agent provides automated compliance validation but does not replace legal or regulatory advice. Always consult with your compliance and legal teams for regulatory interpretation and audit preparation.
