# Configuration du Système

## Structure des fichiers

```
correction-system/
├── .env                    # ⚠️ SECRETS - Ne JAMAIS commiter
├── .env.example            # Template pour .env
├── docker-compose.yml      # Configuration propre (sans secrets)
├── .gitignore             # Liste des fichiers à ignorer
├── SECURITY.md            # Guide de sécurité
└── CONFIGURATION.md       # Ce fichier
```

## Variables d'environnement

Toutes les informations sensibles sont maintenant dans `.env` :

### PostgreSQL
- `POSTGRES_USER` : Utilisateur de la base de données
- `POSTGRES_PASSWORD` : Mot de passe PostgreSQL
- `POSTGRES_DB` : Nom de la base de données

### Gitea
- `GITEA_DOMAIN` : Domaine principal de Gitea
- `GITEA_ROOT_URL` : URL complète de Gitea

### Runner Gitea Actions
- `RUNNER_TOKEN` : Token d'enregistrement du runner

### OAuth Dashboard
- `GITEA_OAUTH_CLIENT_ID` : ID client OAuth
- `GITEA_OAUTH_CLIENT_SECRET` : Secret OAuth

### Dashboard Grades
- `DASHBOARD_SECRET_KEY` : Clé secrète pour les sessions
- `ALLOWED_TEAM` : Équipe autorisée à accéder

### Domaines
- `DOMAIN_GITEA` : git.zohrabi.cloud
- `DOMAIN_GRADES` : grades.zohrabi.cloud
- `DOMAIN_MAIL` : mail.zohrabi.cloud

### Email
- `LETSENCRYPT_EMAIL` : Email pour Let's Encrypt
- `MAILER_FROM` : Adresse d'envoi des emails

### Général
- `TZ` : Fuseau horaire
- `DEFAULT_LANGUAGE` : Langue par défaut

## Avantages de cette configuration

### ✅ Sécurité
- Aucun mot de passe en clair dans `docker-compose.yml`
- Fichier `.env` ignoré par git
- Facile de changer les secrets sans modifier le code

### ✅ Flexibilité
- Changement de domaine facile (une seule variable)
- Configuration par environnement (dev/staging/prod)
- Réutilisable pour d'autres projets

### ✅ Maintenabilité
- Configuration centralisée
- Documentation claire
- Facile à auditer

## Déploiement

### 1. Première installation

```bash
# Copier l'exemple
cp .env.example .env

# Éditer et remplir les secrets
nano .env

# Générer les secrets nécessaires
openssl rand -base64 32  # Pour POSTGRES_PASSWORD
openssl rand -hex 32     # Pour DASHBOARD_SECRET_KEY

# Démarrer les services
docker compose up -d
```

### 2. Mise à jour

```bash
# Récupérer les dernières modifications
git pull

# Redémarrer les services
docker compose up -d
```

### 3. Vérification

```bash
# Voir l'état des services
docker compose ps

# Voir les logs
docker compose logs -f

# Vérifier la configuration
docker compose config
```

## DNS Configuration

Ajouter ces enregistrements DNS (Type A) :

```
git.zohrabi.cloud      → 46.202.168.96
grades.zohrabi.cloud   → 46.202.168.96
mail.zohrabi.cloud     → 46.202.168.96
```

## Ports utilisés

- `80` : HTTP (redirection vers HTTPS)
- `443` : HTTPS (Traefik)
- `2222` : SSH Git (Gitea)

## Sauvegarde

### Fichiers à sauvegarder

```bash
# Configuration
.env

# Données
postgres/data/
gitea/data/
traefik/acme/acme.json
```

### Script de sauvegarde

```bash
#!/bin/bash
BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

# Sauvegarder .env (chiffré)
tar czf - .env | openssl enc -aes-256-cbc -e -pbkdf2 > "$BACKUP_DIR/env.tar.gz.enc"

# Sauvegarder PostgreSQL
docker compose exec -T postgres pg_dumpall -U gitea | gzip > "$BACKUP_DIR/postgres.sql.gz"

# Sauvegarder les données Gitea
tar czf "$BACKUP_DIR/gitea-data.tar.gz" gitea/data/

echo "Sauvegarde créée dans $BACKUP_DIR"
```

## Dépannage

### Services ne démarrent pas

```bash
# Vérifier les logs
docker compose logs

# Vérifier la configuration
docker compose config

# Recréer les conteneurs
docker compose down
docker compose up -d
```

### Erreurs de certificat SSL

```bash
# Vérifier les logs Traefik
docker compose logs traefik

# Vérifier que les DNS pointent vers le serveur
dig git.zohrabi.cloud +short
```

### Problème de connexion PostgreSQL

```bash
# Vérifier que PostgreSQL est démarré
docker compose ps postgres

# Se connecter à PostgreSQL
docker compose exec postgres psql -U gitea
```

## Support

Pour plus d'informations :
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Gitea Documentation](https://docs.gitea.io/)
- [Traefik Documentation](https://doc.traefik.io/traefik/)
