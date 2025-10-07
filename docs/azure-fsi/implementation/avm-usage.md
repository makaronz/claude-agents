# Azure Verified Modules (AVM) Implementation

## Overview

The Azure FSI Landing Zone agent now **actually uses** Azure Verified Modules (AVM) from the Bicep Public Registry when generating infrastructure templates.

Previously, the agent only *referenced* AVM in documentation but generated custom Bicep resources. As of this update, all generated templates leverage official Microsoft-validated AVM modules.

## AVM Modules Used

| Component | AVM Module | Version | Registry Path |
|-----------|-----------|---------|---------------|
| **Virtual Networks** | `avm/res/network/virtual-network` | 0.1.8 | `br/public:avm/res/network/virtual-network:0.1.8` |
| **Azure Firewall** | `avm/res/network/azure-firewall` | 0.3.0 | `br/public:avm/res/network/azure-firewall:0.3.0` |
| **Key Vault** | `avm/res/key-vault/vault` | 0.6.2 | `br/public:avm/res/key-vault/vault:0.6.2` |
| **Storage Account** | `avm/res/storage/storage-account` | 0.9.1 | `br/public:avm/res/storage/storage-account:0.9.1` |
| **Policy Assignments** | *Native resources* | N/A | AVM module not yet available |

## Example: Hub VNet Template

### Before (Custom Resources)
```bicep
resource hubVNet 'Microsoft.Network/virtualNetworks@2023-05-01' = {
  name: hubVNetName
  location: location
  properties: {
    addressSpace: {
      addressPrefixes: [addressSpace]
    }
    subnets: [...]
  }
}
```

### After (AVM Module)
```bicep
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

## Benefits of Using AVM

### 1. **Microsoft Validation**
- All AVM modules are tested and maintained by Microsoft
- Follow Azure best practices and design patterns
- Regular security updates and bug fixes

### 2. **Consistent Output Structure**
- Standardized output names (e.g., `resourceId`, `name`)
- Predictable parameter names across modules
- Better template composability

### 3. **Built-in Features**
- Diagnostic settings integration
- RBAC role assignments
- Private endpoints support
- Tags management
- Lock resources

### 4. **Versioning & Stability**
- Semantic versioning (e.g., `0.1.8`)
- Pin to specific versions for reproducibility
- Upgrade path documented

## Implementation Details

### Template Generation Methods Updated

All Bicep generation methods in [agent.py](../../../agents/azure-fsi-landingzone/agent.py) have been updated:

1. **`_generate_hub_vnet_bicep()`** (line 1273)
   - Uses `avm/res/network/virtual-network` for hub VNet
   - Uses `avm/res/network/azure-firewall` for Azure Firewall

2. **`_generate_spoke_vnet_bicep()`** (line 1349)
   - Uses `avm/res/network/virtual-network` for spoke VNets
   - Includes peering configuration via AVM parameters

3. **`_generate_keyvault_bicep()`** (line 1415)
   - Uses `avm/res/key-vault/vault`
   - Configures diagnostic settings, soft delete, purge protection

4. **`_generate_storage_bicep()`** (line 1473)
   - Uses `avm/res/storage/storage-account`
   - Includes blob service configuration for compliance

5. **`_generate_policy_bicep()`** (line 1535)
   - Uses native Azure resources (AVM module not available yet)
   - Will be migrated when `avm/res/authorization/policy-assignment` becomes available

### System Prompt Updated

The agent's system prompt ([agent.py:189-202](../../../agents/azure-fsi-landingzone/agent.py#L189)) now explicitly states:

> All generated Bicep templates use AVM modules from the official Bicep Public Registry

This ensures Claude knows to generate AVM-based templates.

## Validation

All generated templates have been validated using Azure CLI:

```bash
cd agents/azure-fsi-landingzone
python test_avm_templates.py
```

**Results:**
- ✅ Hub VNet: Valid
- ✅ Spoke VNet: Valid
- ✅ Key Vault: Valid
- ✅ Storage Account: Valid
- ✅ Policy Assignment: Valid

## FSI Compliance Features

AVM modules are configured with Financial Services Industry requirements:

### Key Vault
- **SKU**: `premium` (HSM-backed keys)
- **Soft Delete**: Enabled (90 days retention)
- **Purge Protection**: Enabled
- **Public Access**: Disabled
- **Network ACLs**: Deny by default

### Storage Account
- **SKU**: `Standard_GRS` (geo-redundant for DORA)
- **TLS**: Minimum 1.2
- **Public Access**: Disabled
- **Encryption**: Infrastructure encryption enabled
- **Retention**: 365 days (MiFID II)

### Virtual Networks
- **DDoS Protection**: Configurable
- **Service Endpoints**: Enabled for critical services
- **Private Endpoints**: Subnet for private link

## Deployment Example

To deploy a hub VNet using the generated template:

```bash
# Generate template
cd agents/azure-fsi-landingzone
python agent.py
> "Generate a hub VNet template"

# Deploy
az deployment group create \
  --resource-group rg-fsi-hub-prod \
  --template-file crelog/hub-vnet.bicep \
  --parameters location=francecentral
```

The Bicep CLI will automatically download the AVM modules from the public registry during deployment.

## Future Enhancements

1. **Add more AVM modules** as they become available:
   - Network Security Groups (`avm/res/network/network-security-group`)
   - Log Analytics Workspace (`avm/res/operational-insights/workspace`)
   - Azure Bastion (`avm/res/network/bastion-host`)

2. **Parameterize AVM versions** in `config.yaml` for easier updates

3. **Create composite modules** that combine multiple AVM modules for common patterns

## References

- [Azure Verified Modules](https://aka.ms/AVM)
- [Bicep Public Registry](https://github.com/Azure/bicep-registry-modules)
- [AVM Module Index](https://azure.github.io/Azure-Verified-Modules/)
- [FSI Landing Zone Documentation](https://learn.microsoft.com/en-us/industry/financial-services/fsi-lz)

---

*Last updated: 2025-10-07*
