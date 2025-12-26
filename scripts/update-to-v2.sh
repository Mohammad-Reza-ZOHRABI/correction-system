#!/bin/bash
set -e

#######################################################
# Script de mise à jour vers v2.0.0
# - Système multilingue (EN/FR)
# - Limitation 5 tentatives par TD
# - Mise à jour email
#######################################################

echo "🚀 Mise à jour vers v2.0.0"
echo "=================================================="

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

PROJECT_DIR="/root/correction-system"

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# Vérifications préliminaires
check_prerequisites() {
    log_step "Vérifications préliminaires..."
    
    if [ ! -d "$PROJECT_DIR" ]; then
        log_error "Projet non trouvé dans $PROJECT_DIR"
        exit 1
    fi
    
    cd $PROJECT_DIR
    
    if ! docker compose ps > /dev/null 2>&1; then
        log_error "Docker Compose non disponible ou services non démarrés"
        exit 1
    fi
    
    log_info "✅ Prérequis OK"
}

# Backup avant modification
create_backup() {
    log_step "Création du backup..."
    
    BACKUP_DIR="/root/backups/pre-v2-$(date +%Y%m%d_%H%M%S)"
    mkdir -p $BACKUP_DIR
    
    # Backup PostgreSQL
    docker compose exec -T postgres pg_dumpall -U gitea | gzip > $BACKUP_DIR/postgres_backup.sql.gz
    
    # Backup fichiers de config
    cp -r grades-dashboard $BACKUP_DIR/
    cp docker-compose.yml $BACKUP_DIR/
    cp .env $BACKUP_DIR/
    
    log_info "✅ Backup créé dans $BACKUP_DIR"
}

# Mise à jour de la base de données
update_database() {
    log_step "Mise à jour de la base de données..."
    
    # Copier le nouveau script SQL
    cat > postgres/init/02-add-attempts-limit.sql << 'EOF'
-- Script copié depuis l'artifact
-- (Le contenu complet du fichier SQL)
EOF
    
    # Exécuter sur la base existante
    docker compose exec -T postgres psql -U gitea -d grades < postgres/init/02-add-attempts-limit.sql
    
    if [ $? -eq 0 ]; then
        log_info "✅ Base de données mise à jour"
    else
        log_error "Échec de la mise à jour de la base de données"
        log_warning "Consultez $BACKUP_DIR pour restauration"
        exit 1
    fi
}

# Ajouter le système i18n
setup_i18n() {
    log_step "Configuration du système multilingue..."
    
    # Créer le fichier de traductions
    cat > grades-dashboard/translations.json << 'EOF'
{
  "en": {
    "common": {
      "login": "Login",
      "logout": "Logout"
    }
  },
  "fr": {
    "common": {
      "login": "Connexion",
      "logout": "Déconnexion"
    }
  }
}
EOF
    
    log_info "✅ Fichier de traductions créé"
}

# Mettre à jour .env
update_env() {
    log_step "Mise à jour du fichier .env..."
    
    # Backup .env
    cp .env .env.backup
    
    # Mise à jour de l'email
    sed -i 's/LETSENCRYPT_EMAIL=.*/LETSENCRYPT_EMAIL=mohammad-reza.zohrabi@ext.devinci.fr/' .env
    
    # Ajouter la langue par défaut si elle n'existe pas
    if ! grep -q "DEFAULT_LANGUAGE" .env; then
        echo "" >> .env
        echo "# Default language (en or fr)" >> .env
        echo "DEFAULT_LANGUAGE=en" >> .env
    fi
    
    log_info "✅ Fichier .env mis à jour"
}

# Rebuild des services
rebuild_services() {
    log_step "Reconstruction des services..."
    
    # Rebuild le dashboard
    docker compose build grades-dashboard
    
    # Redémarrer tous les services
    docker compose down
    docker compose up -d
    
    log_info "✅ Services redémarrés"
}

# Vérifier le déploiement
verify_deployment() {
    log_step "Vérification du déploiement..."
    
    # Attendre que les services démarrent
    sleep 10
    
    # Vérifier PostgreSQL
    if docker compose exec -T postgres pg_isready -U gitea > /dev/null 2>&1; then
        log_info "✅ PostgreSQL : OK"
    else
        log_error "❌ PostgreSQL : KO"
        return 1
    fi
    
    # Vérifier le dashboard
    if curl -sf http://localhost:8000/health > /dev/null 2>&1; then
        log_info "✅ Dashboard : OK"
    else
        log_warning "⚠️  Dashboard : Vérifier les logs"
    fi
    
    # Vérifier la fonction de limitation
    FUNCTION_EXISTS=$(docker compose exec -T postgres psql -U gitea -d grades -t -c "
        SELECT EXISTS(
            SELECT 1 FROM pg_proc WHERE proname = 'check_attempts_limit'
        );
    " | xargs)
    
    if [ "$FUNCTION_EXISTS" = "t" ]; then
        log_info "✅ Fonction de limitation des tentatives : Installée"
    else
        log_error "❌ Fonction de limitation : Non trouvée"
        return 1
    fi
    
    return 0
}

# Afficher les instructions post-installation
show_next_steps() {
    echo ""
    echo "=============================================="
    echo "✅ Mise à jour vers v2.0.0 terminée !"
    echo "=============================================="
    echo ""
    echo "📋 Changements appliqués :"
    echo ""
    echo "1. 🌍 Système multilingue (EN/FR)"
    echo "   - Langue par défaut : Anglais"
    echo "   - Changement de langue : Header du dashboard"
    echo ""
    echo "2. 🔢 Limitation à 5 tentatives par TD"
    echo "   - Fonction de vérification automatique"
    echo "   - Compteur dans les rapports"
    echo "   - Blocage après 5 tentatives"
    echo ""
    echo "3. 📧 Email mis à jour"
    echo "   - Nouveau : mohammad-reza.zohrabi@ext.devinci.fr"
    echo ""
    echo "⚠️  ACTIONS REQUISES :"
    echo ""
    echo "1. Mettre à jour les workflows dans TOUS les repositories étudiants"
    echo "   Script disponible : scripts/update_all_workflows.py"
    echo ""
    echo "2. Informer les étudiants des nouvelles limitations"
    echo "   - 5 tentatives maximum par TD"
    echo "   - Tester localement avant de push"
    echo ""
    echo "3. Vérifier les traductions"
    echo "   - EN : https://grades.zohrabi.cloud/set-language/en"
    echo "   - FR : https://grades.zohrabi.cloud/set-language/fr"
    echo ""
    echo "📊 Statistiques des tentatives actuelles :"
    echo ""
    
    # Afficher les étudiants ayant déjà 5+ tentatives
    docker compose exec -T postgres psql -U gitea -d grades -c "
        SELECT 
            s.prenom || ' ' || s.nom as etudiant,
            a.code as td,
            COUNT(sub.id) as tentatives
        FROM students s
        CROSS JOIN assignments a
        LEFT JOIN submissions sub ON s.id = sub.student_id AND a.id = sub.assignment_id
        GROUP BY s.id, s.prenom, s.nom, a.id, a.code
        HAVING COUNT(sub.id) >= 5
        ORDER BY COUNT(sub.id) DESC
        LIMIT 10;
    "
    
    echo ""
    echo "📁 Backup sauvegardé dans : $BACKUP_DIR"
    echo ""
    echo "🔄 Pour annuler cette mise à jour :"
    echo "   scripts/rollback-v2.sh"
    echo ""
    echo "📧 Support : mohammad-reza.zohrabi@ext.devinci.fr"
    echo ""
}

# Programme principal
main() {
    echo ""
    log_info "Démarrage de la mise à jour..."
    echo ""
    
    # Confirmation
    read -p "Cette mise à jour va modifier la base de données. Continuer ? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_warning "Mise à jour annulée"
        exit 0
    fi
    
    # Exécution
    check_prerequisites
    create_backup
    update_database
    setup_i18n
    update_env
    rebuild_services
    
    if verify_deployment; then
        show_next_steps
    else
        log_error "Erreur lors de la vérification"
        log_warning "Les services sont démarrés mais des problèmes ont été détectés"
        log_info "Consultez les logs : docker compose logs"
    fi
}

# Exécution
main "$@"