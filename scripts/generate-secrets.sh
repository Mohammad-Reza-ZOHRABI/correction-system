#!/bin/bash

# Script pour générer des secrets sécurisés
# Usage: ./scripts/generate-secrets.sh

set -e

echo "==================================="
echo "Générateur de Secrets Sécurisés"
echo "==================================="
echo ""

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Fonction pour générer un mot de passe
generate_password() {
    openssl rand -base64 32 | tr -d "=+/" | cut -c1-32
}

# Fonction pour générer une clé hexadécimale
generate_hex_key() {
    openssl rand -hex 32
}

echo -e "${YELLOW}Génération des secrets...${NC}"
echo ""

# PostgreSQL Password
POSTGRES_PASSWORD=$(generate_password)
echo -e "${GREEN}✓${NC} POSTGRES_PASSWORD généré"

# Dashboard Secret Key
DASHBOARD_SECRET_KEY=$(generate_hex_key)
echo -e "${GREEN}✓${NC} DASHBOARD_SECRET_KEY généré"

echo ""
echo "==================================="
echo "Secrets générés avec succès !"
echo "==================================="
echo ""

echo -e "${YELLOW}Copiez ces valeurs dans votre fichier .env :${NC}"
echo ""
echo "POSTGRES_PASSWORD=$POSTGRES_PASSWORD"
echo "DASHBOARD_SECRET_KEY=$DASHBOARD_SECRET_KEY"
echo ""

echo -e "${YELLOW}Secrets à générer manuellement depuis Gitea :${NC}"
echo ""
echo "1. RUNNER_TOKEN"
echo "   → Gitea > Site Admin > Actions > Runners > Create Runner"
echo ""
echo "2. GITEA_OAUTH_CLIENT_ID et GITEA_OAUTH_CLIENT_SECRET"
echo "   → Gitea > Settings > Applications > Create OAuth2 Application"
echo "   → Redirect URI: https://grades.zohrabi.cloud/auth/callback"
echo ""

echo -e "${RED}⚠️  IMPORTANT:${NC}"
echo "   - Ne partagez JAMAIS ces secrets"
echo "   - Ne les commitez JAMAIS dans git"
echo "   - Stockez-les dans un gestionnaire de mots de passe"
echo ""
