# Guide de Sécurité

## Variables d'environnement sensibles

Toutes les informations sensibles sont stockées dans le fichier `.env` qui **NE DOIT JAMAIS** être commité dans git.

### Vérifier que .env est ignoré

```bash
# Vérifier que .env est dans .gitignore
grep "^\.env$" .gitignore
```

## Génération des secrets

### 1. Mot de passe PostgreSQL

Générer un mot de passe fort :

```bash
openssl rand -base64 32
```

Puis mettre à jour `POSTGRES_PASSWORD` dans `.env`

### 2. Dashboard Secret Key

```bash
openssl rand -hex 32
```

Puis mettre à jour `DASHBOARD_SECRET_KEY` dans `.env`

### 3. Runner Token

1. Se connecter à Gitea
2. Aller dans : Site Administration → Actions → Runners
3. Cliquer sur "Create new Runner"
4. Copier le token généré
5. Mettre à jour `RUNNER_TOKEN` dans `.env`

### 4. OAuth Credentials

1. Se connecter à Gitea
2. Aller dans : Settings → Applications
3. Cliquer sur "Create OAuth2 Application"
4. Nom: "Grades Dashboard"
5. Redirect URI: `https://grades.zohrabi.cloud/auth/callback`
6. Copier Client ID et Client Secret
7. Mettre à jour `GITEA_OAUTH_CLIENT_ID` et `GITEA_OAUTH_CLIENT_SECRET` dans `.env`

## Bonnes pratiques

1. **Ne jamais commiter .env** dans git
2. **Utiliser des mots de passe forts** (minimum 32 caractères)
3. **Sauvegarder .env** de manière sécurisée (gestionnaire de mots de passe, coffre-fort)
4. **Changer régulièrement** les secrets (tous les 6 mois minimum)
5. **Limiter l'accès SSH** au serveur
6. **Activer le firewall** et n'ouvrir que les ports nécessaires (80, 443, 2222)

## Permissions des fichiers

```bash
# .env doit être accessible uniquement par le propriétaire
chmod 600 .env

# Vérifier les permissions
ls -la .env
# Doit afficher: -rw------- 1 user user ... .env
```

## Sauvegarde sécurisée

Pour sauvegarder votre configuration :

```bash
# Créer une archive chiffrée
tar czf - .env | openssl enc -aes-256-cbc -e -pbkdf2 > env-backup.tar.gz.enc

# Pour restaurer
openssl enc -aes-256-cbc -d -pbkdf2 -in env-backup.tar.gz.enc | tar xzf -
```

## Audit de sécurité

Commandes pour vérifier la sécurité :

```bash
# Vérifier qu'aucun mot de passe n'est en clair dans docker-compose.yml
grep -i "password" docker-compose.yml | grep -v "POSTGRES_PASSWORD"

# Lister les variables d'environnement utilisées
docker compose config | grep -E "PASSWORD|SECRET|TOKEN"
```
