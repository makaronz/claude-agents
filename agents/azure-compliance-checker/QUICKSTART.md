# Quick Start - Azure Compliance Checker

Validate your Azure infrastructure against French FSI regulations in 5 minutes.

## Prerequisites (2 minutes)

### 1. Azure CLI Authentication
```bash
# Login to Azure
az login

# Set subscription
az account set --subscription "<your-subscription-id>"

# Verify
az account show
```

### 2. Python Dependencies
```bash
cd agents/azure-compliance-checker
uv pip sync uv.lock         # if present
# or resolve the latest versions
uv pip install -r requirements.txt
```

### 3. API Key
```bash
export ANTHROPIC_API_KEY="your-key-here"
```

## Quick Validation (3 minutes)

### 1. Start the Agent
```bash
python agent.py
```

### 2. Run Compliance Check

```
================================================================================
  📋 AZURE COMPLIANCE CHECKER AGENT
================================================================================

💬 You: List available checklists

🤖 Claude: 📋 Available Compliance Checklists:

1. **french-fsi-regulations.yaml**
   • Controls: 24
   • Path: checklists/french-fsi-regulations.yaml

💬 You: Load french-fsi-regulations.yaml

🤖 Claude: ✅ Loaded Checklist: french-fsi-regulations.yaml

📊 Summary:
   • Total Controls: 24
   • Regulations Covered: 7

🏛️  Regulations:
   • ACPR – Gouvernance SI: 3 controls
   • CRD IV / CRR: 3 controls
   • LCB-FT / AMLD5: 3 controls
   • RGPD / CNIL: 4 controls
   • ISO 27001 / SOC 2: 3 controls
   • DORA (2025): 3 controls
   • NIS2 (2024/25): 3 controls

💡 Next steps:
   - Use validate_all_controls to check all controls
   - Use validate_control to check a specific control
   - Use generate_compliance_report to create a report

💬 You: Validate all controls

🤖 Claude: 🔍 Validating All Controls (24 total)
Started: 2025-10-02 14:30:00
================================================================================

Control #1: ACPR – Gouvernance SI - Continuité (PRA/DRP): PASSED
Control #2: ACPR – Gouvernance SI - Journalisation: PASSED
Control #3: ACPR – Gouvernance SI - Gouvernance Cloud: FAILED
Control #4: CRD IV / CRR - Gestion incidents: PASSED
...
Control #24: NIS2 (2024/25) - Risk Management: PASSED

================================================================================
📊 Validation Summary:
   ✅ Passed: 21
   ❌ Failed: 2
   ⚠️  Manual: 1
   📈 Total: 24

   🎯 Compliance Rate: 87.5%

💡 Use generate_compliance_report to create detailed report

💬 You: Generate compliance report

🤖 Claude: ✅ Compliance report generated:

📄 File: reports/compliance_report_20250102_143045.md
📅 Date: 2025-10-02 14:30:45
📊 Controls: 24

Summary:
   ✅ Passed: 21
   ❌ Failed: 2
   ⚠️  Manual: 1

💬 You: Get remediation plan

🤖 Claude: 🔧 Remediation Plan (2 Failed Controls)

1. **ACPR – Gouvernance SI**: Gouvernance Cloud
   Priority: HIGH
   Action: Review control details and implement required Azure resources

2. **RGPD / CNIL**: Souveraineté
   Priority: HIGH
   Action: Review control details and implement required Azure resources

💡 Recommended Actions:
1. Review each failed control's requirements
2. Deploy missing Azure resources
3. Configure Azure Policy assignments
4. Enable security features (Defender, Sentinel, etc.)
5. Re-run validation after remediation

💬 You: Export audit report to json

🤖 Claude: ✅ Audit report exported:

📄 File: reports/audit_report_20250102_143100.json
📊 Format: JSON
📅 Date: 2025-10-02 14:31:00

💬 You: quit

👋 azure-compliance-checker: Goodbye! Thanks for chatting.
```

## Common Commands

### List Checklists
```
You: List available checklists
```

### Load Checklist
```
You: Load french-fsi-regulations.yaml
```

### Validate All
```
You: Validate all controls
```

### Validate Specific Control
```
You: Validate control 0
```
(Control indices start at 0)

### Check Specific Resource
```
You: Check Azure resource Microsoft.KeyVault/vaults
```

### Get Summary
```
You: Get compliance summary
```

### Generate Report
```
You: Generate compliance report
```

### Get Remediation
```
You: Get remediation plan
```

### Export Report
```
You: Export audit report to markdown
You: Export audit report to json
```

## Example: Check Key Vault Compliance

```
💬 You: Check Azure resource Microsoft.KeyVault/vaults

🤖 Claude: 🔍 Checking Azure Resource Type: Microsoft.KeyVault/vaults

Found: 2 resource(s)

1. fsi-prod-kv
   • Location: westeurope
   • Resource Group: fsi-security-rg
   • ID: /subscriptions/.../resourceGroups/fsi-security-rg/providers/Microsoft.KeyVault/vaults/fsi-prod-kv

2. fsi-dev-kv
   • Location: francecentral
   • Resource Group: fsi-dev-rg
   • ID: /subscriptions/.../resourceGroups/fsi-dev-rg/providers/Microsoft.KeyVault/vaults/fsi-dev-kv
```

## Example: Validate Custom Control

```
💬 You: Validate this custom control:
reglementation: "Internal Policy"
exigence: "Storage Encryption"
preuve: "Storage accounts encrypted"
controle: "Verify encryption enabled"
azure_resources:
  - type: "Microsoft.Storage/storageAccounts"
    required: true
    validation:
      - property: "properties.encryption.services.blob.enabled"
        check: "equals"
        value: true

🤖 Claude: [Validates the custom control and shows results]
```

## Reading Reports

### Markdown Report
```bash
cat reports/compliance_report_20250102_143045.md
```

### JSON Report
```bash
cat reports/audit_report_20250102_143100.json | jq
```

## Integration with Landing Zone Agent

### Workflow

1. **Deploy Infrastructure**
   ```bash
   cd ../azure-fsi-landingzone
   python agent.py
   # Deploy your FSI landing zone
   ```

2. **Validate Compliance**
   ```bash
   cd ../azure-compliance-checker
   python agent.py
   # Load french-fsi-regulations.yaml
   # Validate all controls
   ```

3. **Remediate Gaps**
   ```bash
   # Review remediation plan
   # Fix identified issues
   ```

4. **Re-validate**
   ```bash
   # Validate all controls again
   # Generate audit report
   ```

## Troubleshooting

### "Not authenticated to Azure"
```bash
az login
az account show
```

### "No resources found"
Check you're in the right subscription:
```bash
az account list --output table
az account set --subscription "<subscription-name>"
```

### "Permission denied"
Ensure you have at least Reader role:
```bash
az role assignment list --assignee <your-email> --all
```

### "Validation timeout"
Some queries take longer. This is normal. The agent will report timeout and continue.

## Tips

1. **Start Small**: Validate a single control first to test connectivity
2. **Check Resources**: Use "Check Azure resource" to verify resources exist
3. **Review Reports**: Generated reports include detailed evidence
4. **Iterate**: Fix issues and re-validate
5. **Export**: Export to JSON for integration with other tools

## Next Steps

1. Review the generated compliance report
2. Address failed controls
3. Set up automated validation (CI/CD)
4. Create custom checklists for your needs
5. Integrate with your GRC tools

## Support

- Full documentation: [README.md](README.md)
- Example checklist: [french-fsi-regulations.yaml](checklists/french-fsi-regulations.yaml)
- Configuration: [config.yaml](config.yaml)

---

**Ready to validate?** Start the agent with `python agent.py`
