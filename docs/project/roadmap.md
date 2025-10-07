# Claude Agents Repository - Roadmap

**Last Updated**: October 2025
**Repository Version**: 1.0.0

This document tracks the high-level evolution of the Claude Agents repository, including completed milestones, current focus, and planned enhancements.

---

## 🎯 Vision

Build a comprehensive collection of production-ready Claude agents for enterprise infrastructure automation, compliance validation, and operational excellence, with a focus on Financial Services Industry (FSI) requirements.

---

## ✅ Completed (October 2025)

### Foundation (Week 1)
- ✅ Repository structure established
- ✅ Shared utilities and base classes (`BaseClaudeAgent`, `InteractiveAgent`)
- ✅ Agent template for rapid development
- ✅ Example agent with custom tools demonstration
- ✅ Documentation framework (AGENTS.md, getting-started guides)

### Azure FSI Landing Zone Agent (Week 1-2)
- ✅ **Created**: Full-featured FSI Landing Zone deployment agent
- ✅ **Technology Stack Decision**: Bicep + AVM (documented rationale)
- ✅ **11 Custom Tools**: Prerequisites checking, template generation, compliance validation
- ✅ **Compliance Focus**: GDPR, DORA, PSD2, MiFID II, EBA Guidelines
- ✅ **Architecture**: Hub-spoke topology with security baselines
- ✅ **Templates**: Hub VNet, Spoke VNet, Key Vault, Storage, Policies
- ✅ **European Data Residency**: EU-only region enforcement
- ✅ **Alignment Analysis**: 95% aligned with Microsoft FSI Landing Zone
- ✅ **4 Landing Zone Types**: Corp, Online, Confidential Corp, Confidential Online
- ✅ **Documentation**: README, QUICKSTART, ALIGNMENT analysis
- ✅ **Configuration**: Comprehensive YAML with all FSI requirements

### Azure Compliance Checker Agent (Week 2)
- ✅ **Created**: Automated compliance validation agent
- ✅ **10 Custom Tools**: Checklist management, validation, reporting
- ✅ **French FSI Regulations**: ACPR, CRD IV/CRR, LCB-FT/AMLD5, RGPD/CNIL, ISO 27001, DORA, NIS2
- ✅ **24 Controls**: Pre-built compliance checklist
- ✅ **YAML Format**: User-defined control definitions
- ✅ **Azure Resource Validation**: Automated resource querying and property checking
- ✅ **Evidence Collection**: Audit-ready reports
- ✅ **Reporting**: Markdown and JSON export formats
- ✅ **Gap Analysis**: Remediation plans for failed controls
- ✅ **Documentation**: README, QUICKSTART guides

### Integration
- ✅ **FSI Landing Zone + Compliance Checker**: Complete deploy-validate-remediate workflow
- ✅ **MCP Integration**: Azure Landing Zones Library docs added to mcp.json

---

## 🚧 In Progress (Current - October 2025)

### Azure FSI Landing Zone Enhancements (Week 2-3)

#### Identity & Access Management ✅ COMPLETED
- ✅ **Azure Bastion Deployment**: Bicep template generator for secure VM access
- ✅ **Entra ID Configuration**: Tools for identity management setup
- ✅ **Conditional Access Policies**: Template-based policy deployment
- ✅ **PIM Role Assignments**: Privileged Identity Management automation

**Status**: COMPLETED (2025-10-02)

**Completed Deliverables**:
- ✅ 4 new tools: `generate_bastion_template`, `configure_entra_id`, `deploy_conditional_access`, `setup_pim_roles`
- ✅ Bastion Bicep template (Standard SKU, tunneling, 365-day logs)
- ✅ 5 Conditional Access policy templates (JSON)
- ✅ PIM configuration guidance with PowerShell scripts
- ✅ Break-glass account setup documentation
- ✅ Compliance mappings to PSD2, GDPR, DORA, ISO 27001, NIS2
- ✅ Agent now has 15 total tools (up from 11)

#### Azure Verified Modules (AVM) Integration ✅ COMPLETED
- ✅ **Actual AVM Usage**: Replaced custom Bicep resources with official AVM modules from Bicep Public Registry
- ✅ **Hub VNet Template**: Using `br/public:avm/res/network/virtual-network:0.1.8`
- ✅ **Spoke VNet Template**: Using `br/public:avm/res/network/virtual-network:0.1.8` with peering
- ✅ **Azure Firewall Template**: Using `br/public:avm/res/network/azure-firewall:0.3.0`
- ✅ **Key Vault Template**: Using `br/public:avm/res/key-vault/vault:0.6.2`
- ✅ **Storage Account Template**: Using `br/public:avm/res/storage/storage-account:0.9.1`
- ✅ **System Prompt Updated**: Added explicit AVM module references
- ✅ **Validation Test Suite**: Created automated Bicep template validation (5/5 passing)
- ✅ **Documentation**: Comprehensive AVM usage guide with before/after examples

**Status**: COMPLETED (2025-10-07)

**Completed Deliverables**:
- ✅ 5 Bicep template generators updated to use AVM modules (agent.py lines 1273-1610)
- ✅ System prompt reflects actual AVM usage (agent.py lines 189-202)
- ✅ Validation script: `agents/azure-fsi-landingzone/test_avm_templates.py`
- ✅ Documentation: `docs/azure-fsi/implementation/avm-usage.md`
- ✅ Changelog: `CHANGELOG_AVM.md`
- ✅ All templates validated with Azure CLI (`az bicep build`)

---

## 📋 Planned (Q1 2025)

### Azure FSI Landing Zone Agent

#### Q1 2025 Priorities

**High Priority**
- [ ] **PowerShell Bootstrap Script**: Generate ALZ PowerShell module bootstrap (from ALIGNMENT.md gap analysis)
- [ ] **Landing Zone Type Templates**: Pre-configured Bicep for Corp/Online/Confidential (from ALIGNMENT.md)
- [ ] **Multi-Subscription Support**: Deploy across multiple subscriptions
- [ ] **Terraform Option**: Optional Terraform generation (for Terraform-first organizations)

**Medium Priority**
- [ ] **CI/CD Pipeline Templates**: Azure DevOps and GitHub Actions workflows
- [ ] **Confidential Computing**: Templates for confidential VMs and containers
- [ ] **Network Security**: Advanced NSG rule generation and validation
- [ ] **Monitoring Dashboards**: Pre-built Azure Monitor workbooks for FSI

**Low Priority**
- [ ] **SWIFT Compliance**: Optional SWIFT CSP-CSCF v2022 policy templates
- [ ] **Cost Estimation**: Azure pricing calculator integration
- [ ] **Deployment History**: Track and manage deployments
- [ ] **Rollback Capabilities**: Automated rollback for failed deployments

### Azure Compliance Checker Agent

#### Q1 2025 Priorities

**High Priority**
- [ ] **Azure Resource Graph**: Faster queries using Resource Graph instead of Azure CLI
- [ ] **Advanced Validation**: JSONPath support for complex property checks
- [ ] **Multi-Subscription**: Validate across multiple subscriptions
- [ ] **Continuous Monitoring**: Schedule automated compliance scans

**Medium Priority**
- [ ] **Custom Validation Logic**: Python-based custom validators
- [ ] **Policy-as-Code Generation**: Auto-generate Azure Policy from controls
- [ ] **GRC Tool Integration**: Delve, Scytale, ServiceNow connectors
- [ ] **HTML Reports**: Web-based compliance dashboards

**Low Priority**
- [ ] **Email Notifications**: Automated compliance report distribution
- [ ] **Trend Analysis**: Track compliance over time
- [ ] **Remediation Automation**: Auto-fix simple compliance gaps
- [ ] **API Endpoint**: REST API for integration

### New Agents (Q1-Q2 2025)

**Planned Agents**
- [ ] **Azure Cost Optimization Agent**: FinOps automation and recommendations
- [ ] **Azure Security Posture Agent**: Continuous security assessment
- [ ] **Azure Backup Validation Agent**: DR testing and validation
- [ ] **Azure Policy Generator Agent**: Interactive policy creation
- [ ] **Multi-Cloud Compliance Agent**: AWS and GCP support

---

## 🔮 Future Considerations (Q2+ 2025)

### Platform Enhancements
- [ ] **Agent Orchestration**: Multi-agent workflows and coordination
- [ ] **Web UI**: Browser-based interface for agents
- [ ] **Agent Marketplace**: Community-contributed agents
- [ ] **Testing Framework**: Automated agent testing

### Compliance & Governance
- [ ] **Additional Regulations**: MiCA, DAC8, CSRD for ESG
- [ ] **Industry Verticals**: Healthcare (HIPAA), Insurance (Solvency II)
- [ ] **Global Regulations**: US (SOX, FINRA), APAC (MAS, HKMA)

### Integration
- [ ] **Terraform Cloud**: Integration with Terraform Enterprise
- [ ] **Azure DevOps**: Native DevOps extension
- [ ] **GitHub Actions**: Reusable workflow components
- [ ] **Slack/Teams**: ChatOps integration

### Advanced Features
- [ ] **Natural Language IaC**: Describe infrastructure in plain language
- [ ] **Drift Detection**: Identify configuration drift
- [ ] **Impact Analysis**: What-if for policy and config changes
- [ ] **Automated Remediation**: Self-healing infrastructure

---

## 📊 Progress Metrics

### October 2025 Summary

| Category | Metric | Value |
|----------|--------|-------|
| **Agents** | Total Agents | 4 (template, example, fsi-lz, compliance) |
| **Tools** | Custom Tools Created | 21 (11 FSI LZ + 10 Compliance) |
| **Lines of Code** | Python | ~3,500 |
| **Documentation** | Pages | 15+ (READMEs, guides, alignment docs) |
| **Compliance** | Regulations Covered | 12+ (GDPR, DORA, PSD2, ACPR, etc.) |
| **Controls** | Automated Checks | 24 (French FSI checklist) |
| **Templates** | Infrastructure | 5 Bicep templates |

---

## 🎯 Success Criteria

### Q1 2025 Goals
- ✅ 2 production-ready FSI agents (deployed and documented)
- 🚧 Complete identity and access management automation
- [ ] 100% alignment with Microsoft FSI Landing Zone architecture
- [ ] Community adoption (GitHub stars, issues, PRs)
- [ ] Real-world FSI deployment (at least 1 organization)

### Q2 2025 Goals
- [ ] 5+ production agents across different domains
- [ ] Multi-cloud support (Azure + AWS/GCP)
- [ ] Community contributions (external agent submissions)
- [ ] Enterprise features (RBAC, audit trails, SaaS option)

---

## 🤝 Contributing

We welcome contributions! Priority areas for community involvement:

1. **Compliance Checklists**: Add regulations for other countries/industries
2. **Templates**: Contribute Bicep/Terraform modules
3. **Agents**: New domain-specific agents
4. **Documentation**: Translations, tutorials, case studies
5. **Testing**: Unit tests, integration tests, real-world validation

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📝 Change Log

### 2025-10-07: Azure Verified Modules (AVM) Integration
- ✅ Implemented actual AVM module usage from Bicep Public Registry
- ✅ Updated 5 Bicep template generators (Hub VNet, Spoke VNet, Key Vault, Storage, Policies)
- ✅ Updated system prompt with AVM module references
- ✅ Created validation test suite (5/5 templates passing)
- ✅ Documented AVM implementation in `docs/azure-fsi/implementation/avm-usage.md`
- ✅ Created `CHANGELOG_AVM.md` with detailed changes

### 2025-10-02: Identity & Access Management
- ✅ Added Bastion template generator
- ✅ Added Entra ID configuration tools
- ✅ Added Conditional Access policies
- ✅ Added PIM role assignment helper

### 2025-10-02: Azure Compliance Checker Agent
- ✅ Created compliance validation agent
- ✅ Added 24 controls for French FSI regulations
- ✅ Implemented 10 custom validation tools
- ✅ YAML-based checklist format
- ✅ Markdown and JSON reporting

### 2025-10-02: FSI Landing Zone Alignment
- ✅ Validated alignment with Microsoft FSI LZ
- ✅ Documented 4 landing zone types (Corp, Online, Confidential)
- ✅ Added SWIFT compliance option
- ✅ Created ALIGNMENT.md with gap analysis
- ✅ 95% alignment score achieved

### 2025-10-01: Azure FSI Landing Zone Agent
- ✅ Created FSI Landing Zone deployment agent
- ✅ Implemented 11 custom tools
- ✅ Bicep + AVM architecture
- ✅ European compliance focus (GDPR, DORA, PSD2, MiFID II)
- ✅ Hub-spoke network templates
- ✅ Comprehensive documentation

### 2025-10-01: Repository Initialization
- ✅ Established repository structure
- ✅ Created base agent classes
- ✅ Built agent template
- ✅ Example agent with custom tools
- ✅ Documentation framework

---

## 📞 Feedback

Have suggestions for the roadmap? Please:
- Open an issue with tag `roadmap`
- Join discussions in GitHub Discussions
- Submit PRs with new ideas

---

**Next Review**: February 2025
**Maintained by**: Repository Contributors
