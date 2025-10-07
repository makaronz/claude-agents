# AVM Implementation Changelog

## 2025-10-07: Actual AVM Integration

### Summary
Implemented **actual** Azure Verified Modules (AVM) usage in Bicep template generation. Previously, the agent only referenced AVM in documentation but generated custom resources.

### Changes Made

#### 1. Updated Bicep Template Generators
All template generation methods now use AVM modules from Bicep Public Registry:

| Method | Line | Change |
|--------|------|--------|
| `_generate_hub_vnet_bicep()` | 1273 | Now uses `br/public:avm/res/network/virtual-network:0.1.8` and `br/public:avm/res/network/azure-firewall:0.3.0` |
| `_generate_spoke_vnet_bicep()` | 1349 | Now uses `br/public:avm/res/network/virtual-network:0.1.8` with peering |
| `_generate_keyvault_bicep()` | 1415 | Now uses `br/public:avm/res/key-vault/vault:0.6.2` |
| `_generate_storage_bicep()` | 1473 | Now uses `br/public:avm/res/storage/storage-account:0.9.1` |
| `_generate_policy_bicep()` | 1535 | Uses native resources (AVM module not available) |

#### 2. Updated System Prompt
**File**: `agents/azure-fsi-landingzone/agent.py` (lines 189-202)

Added explicit AVM module references to system prompt:
```
All generated Bicep templates use AVM modules from the official Bicep Public Registry:
- Virtual Networks: br/public:avm/res/network/virtual-network:0.1.8
- Azure Firewall: br/public:avm/res/network/azure-firewall:0.3.0
- Key Vault: br/public:avm/res/key-vault/vault:0.6.2
- Storage Accounts: br/public:avm/res/storage/storage-account:0.9.1
```

#### 3. Created Validation Test Script
**File**: `agents/azure-fsi-landingzone/test_avm_templates.py`

Automated Bicep template validation using Azure CLI:
- Validates all 5 template types
- Uses `az bicep build` for syntax checking
- Reports pass/fail for each template

**Test Results**: ✅ 5/5 templates valid

#### 4. Added Documentation
**File**: `docs/azure-fsi/implementation/avm-usage.md`

Comprehensive documentation covering:
- AVM modules used with versions
- Before/after code examples
- Benefits of AVM
- FSI compliance features
- Deployment examples

### Before vs After

#### Before
```bicep
// Custom resource definition
resource hubVNet 'Microsoft.Network/virtualNetworks@2023-05-01' = {
  name: hubVNetName
  location: location
  properties: {
    addressSpace: { addressPrefixes: [addressSpace] }
    subnets: [...]
  }
}
```

#### After
```bicep
// Using AVM module from Bicep Public Registry
module hubVNet 'br/public:avm/res/network/virtual-network:0.1.8' = {
  name: 'deploy-hub-vnet'
  params: {
    name: hubVNetName
    location: location
    addressPrefixes: [addressSpace]
    subnets: [...]
  }
}
```

### Benefits

1. **Microsoft Validation**: All modules are tested by Microsoft
2. **Consistent Outputs**: Standardized output names (`resourceId`, `name`)
3. **Built-in Features**: Diagnostic settings, RBAC, tags management
4. **Versioning**: Semantic versioning for reproducibility
5. **Best Practices**: Follow Azure design patterns automatically

### Compatibility Notes

- **Bicep CLI**: Requires `az bicep` to be installed
- **Registry Access**: Templates will download modules from `mcr.microsoft.com` on first use
- **Version Pinning**: All modules use explicit versions (e.g., `:0.1.8`)
- **Policy Assignments**: Use native resources until AVM module becomes available

### Testing

Run validation tests:
```bash
cd agents/azure-fsi-landingzone
python test_avm_templates.py
```

### Files Modified

1. `agents/azure-fsi-landingzone/agent.py` - Core implementation (5 methods + system prompt)
2. `agents/azure-fsi-landingzone/test_avm_templates.py` - New validation script
3. `docs/azure-fsi/implementation/avm-usage.md` - New documentation
4. `CHANGELOG_AVM.md` - This file

### Next Steps

1. Monitor AVM releases for new modules (NSG, Bastion, Log Analytics)
2. Update to newer AVM versions as they're released
3. Consider parameterizing AVM versions in `config.yaml`
4. Create composite modules for common FSI patterns

### References

- [Azure Verified Modules](https://aka.ms/AVM)
- [Bicep Registry](https://github.com/Azure/bicep-registry-modules)
- [AVM Module Index](https://azure.github.io/Azure-Verified-Modules/)

---

**Status**: ✅ Complete - All templates validated and working
