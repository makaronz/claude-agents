#!/bin/bash
# detect-free-tier.sh
# Azure Free Tier Detection Script for FSI Landing Zone
# Automatically detects subscription type and enforces cost guardrails

set -e  # Exit on error
set -u  # Exit on undefined variable

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to log messages
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_success() {
    echo -e "${BLUE}[SUCCESS]${NC} $1"
}

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    log_error "Azure CLI not found. Please install it first."
    exit 1
fi

# Check if authenticated
if ! az account show &> /dev/null; then
    log_error "Not authenticated to Azure. Please run 'az login' first."
    exit 1
fi

log_info "🔍 Vérification du type d'abonnement Azure..."

# Get subscription details
subscriptionId=$(az account show --query "id" -o tsv)
subscriptionName=$(az account show --query "name" -o tsv)
offerType=$(az account show --query "offerType" -o tsv)
state=$(az account show --query "state" -o tsv)

log_info "📋 Abonnement actuel:"
echo "   • Nom: $subscriptionName"
echo "   • ID: $subscriptionId"
echo "   • Type d'offre: $offerType"
echo "   • État: $state"
echo ""

# Determine if Free Tier based on offer type
isFreeTier=false
tierDescription=""

case "$offerType" in
    "MS-AZR-0044P")
        isFreeTier=true
        tierDescription="Azure Free Trial (30 jours)"
        ;;
    "MS-AZR-0170P")
        isFreeTier=true
        tierDescription="Azure for Students"
        ;;
    "MS-AZR-0144P")
        isFreeTier=true
        tierDescription="Azure for Students Starter"
        ;;
    "MS-AZR-0148P")
        isFreeTier=false
        tierDescription="Pay-As-You-Go"
        ;;
    "MS-AZR-0017P")
        isFreeTier=false
        tierDescription="Enterprise Agreement"
        ;;
    "MS-AZR-0063P")
        isFreeTier=false
        tierDescription="Pay-As-You-Go Dev/Test"
        ;;
    *)
        log_warn "Type d'offre non reconnu: $offerType"
        tierDescription="Type d'offre: $offerType"
        # Par défaut, considérer comme non Free Tier pour éviter les restrictions inutiles
        isFreeTier=false
        ;;
esac

echo ""
if [ "$isFreeTier" = true ]; then
    log_warn "🟡 Mode Free Tier détecté: $tierDescription"
    log_warn "   → Activation des garde-fous de coûts"
    log_warn "   → Limitation des SKUs disponibles"
    log_warn "   → Budgets et alertes automatiques activés"
else
    log_success "🟢 Mode Standard détecté: $tierDescription"
    log_info "   → SKUs complètes disponibles"
    log_info "   → Pas de restrictions Free Tier"
fi

echo ""

# Check available quotas (optional - can take time)
log_info "🔍 Vérification des quotas disponibles..."

# Get VM quotas for common regions
commonRegions=("westeurope" "northeurope" "francecentral")
quotaWarnings=()

for region in "${commonRegions[@]}"; do
    # Get total cores quota for Standard BS Family (common in free tier)
    coresQuota=$(az vm list-usage --location "$region" --query "[?localName=='Standard BS Family vCPUs'].currentValue" -o tsv 2>/dev/null || echo "N/A")
    coresLimit=$(az vm list-usage --location "$region" --query "[?localName=='Standard BS Family vCPUs'].limit" -o tsv 2>/dev/null || echo "N/A")

    if [ "$coresQuota" != "N/A" ] && [ "$coresLimit" != "N/A" ]; then
        echo "   • $region: $coresQuota/$coresLimit vCPUs utilisés (Standard BS Family)"

        # Warn if quota is limited (typical for free tier)
        if [ "$coresLimit" -lt 10 ]; then
            quotaWarnings+=("$region: Quota limité ($coresLimit vCPUs) - Free Tier probable")
        fi
    fi
done

echo ""

# Additional heuristics for Free Tier detection
if [ ${#quotaWarnings[@]} -gt 0 ]; then
    log_warn "⚠️  Indices supplémentaires de Free Tier détectés:"
    for warning in "${quotaWarnings[@]}"; do
        echo "   • $warning"
    done
    echo ""

    # Override detection if quotas are very limited
    if [ "$isFreeTier" = false ]; then
        log_warn "🔄 Correction: Quotas limités détectés, activation des garde-fous Free Tier"
        isFreeTier=true
    fi
fi

# Export results to configuration file
configFile="./deployment-config.json"

log_info "📝 Export de la configuration..."

cat > "$configFile" <<EOF
{
  "detectedAt": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "subscription": {
    "id": "$subscriptionId",
    "name": "$subscriptionName",
    "offerType": "$offerType",
    "state": "$state"
  },
  "tier": {
    "isFreeTier": $isFreeTier,
    "description": "$tierDescription"
  },
  "quotas": {
    "regions": [
$(for region in "${commonRegions[@]}"; do
    coresQuota=$(az vm list-usage --location "$region" --query "[?localName=='Standard BS Family vCPUs'].currentValue" -o tsv 2>/dev/null || echo "0")
    coresLimit=$(az vm list-usage --location "$region" --query "[?localName=='Standard BS Family vCPUs'].limit" -o tsv 2>/dev/null || echo "0")
    echo "      {\"region\": \"$region\", \"used\": $coresQuota, \"limit\": $coresLimit}"
    [ "$region" != "${commonRegions[-1]}" ] && echo ","
done)
    ]
  },
  "guardrails": {
    "budgetEnabled": $isFreeTier,
    "skuRestrictions": $isFreeTier,
    "autoCleanup": $isFreeTier,
    "diagnosticsDisabled": $isFreeTier
  }
}
EOF

log_success "✅ Configuration exportée vers: $configFile"
echo ""

# Export simple flag for quick checks
echo "$isFreeTier" > ./isFreeTier.flag

log_info "📊 Résumé de la détection:"
echo "   • Free Tier: $([ "$isFreeTier" = true ] && echo "OUI" || echo "NON")"
echo "   • Fichier de config: $configFile"
echo "   • Flag rapide: ./isFreeTier.flag"
echo ""

# Display next steps based on tier
if [ "$isFreeTier" = true ]; then
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    log_warn "⚠️  RECOMMANDATIONS POUR FREE TIER:"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "   1. 💰 Créer un budget avec alertes (5€, 10€)"
    echo "   2. 🚫 Éviter les ressources coûteuses (Firewall, SQL Premium, Load Balancer)"
    echo "   3. 📦 Utiliser uniquement les SKUs gratuits/légers (B1s, Free tier services)"
    echo "   4. 🧹 Activer le nettoyage automatique des environnements non-prod (7 jours)"
    echo "   5. 📊 Désactiver les diagnostics non essentiels"
    echo "   6. 🌍 Limiter aux régions Europe (moins de réplication)"
    echo ""
    log_info "💡 Pour déployer en mode Free Tier:"
    echo "   az deployment sub create \\"
    echo "     --location westeurope \\"
    echo "     --template-file main.bicep \\"
    echo "     --parameters isFreeTier=true env=dev"
    echo ""
else
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    log_success "✅ DÉPLOIEMENT STANDARD DISPONIBLE"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "   • Tous les SKUs disponibles"
    echo "   • Architecture complète FSI Landing Zone possible"
    echo "   • Azure Firewall, Bastion, Load Balancer disponibles"
    echo ""
    log_info "💡 Pour déployer en mode Standard:"
    echo "   az deployment sub create \\"
    echo "     --location westeurope \\"
    echo "     --template-file main.bicep \\"
    echo "     --parameters isFreeTier=false env=prod"
    echo ""
fi

exit 0
