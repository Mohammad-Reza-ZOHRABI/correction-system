---
title: "Comment faire un Push"
description: "Guide complet pour soumettre votre projet via Git"
order: 2
category: "🚀 Démarrage"
---

# Comment faire un Push

Ce guide explique en détail comment soumettre votre projet sur Gitea avec Git.

## 📋 Prérequis

Avant de commencer, assurez-vous d'avoir :

- ✅ Git installé sur votre machine
- ✅ Votre compte Gitea créé
- ✅ Repository cloné localement

### Vérifier que Git est installé

```bash
git --version
# Résultat attendu : git version 2.x.x
```

Si Git n'est pas installé :

**Ubuntu/Debian :**
```bash
sudo apt update
sudo apt install git
```

**macOS :**
```bash
brew install git
```

**Windows :**
Téléchargez depuis : https://git-scm.com/download/win

## 🔧 Configuration initiale de Git

### Configurer votre identité

```bash
# Votre nom
git config --global user.name "Jean Dupont"

# Votre email
git config --global user.email "jean.dupont@students.zohrabi.cloud"

# Vérifier la configuration
git config --list
```

## 📥 Cloner votre repository

### Première fois : Clonage

```bash
# Remplacer par VOTRE nom d'utilisateur et groupe
git clone https://git.zohrabi.cloud/Groupe-A/jean.dupont-tds.git

# Entrer dans le dossier
cd jean.dupont-tds
```

Lors du clone, Git vous demandera :
- **Username** : `jean.dupont`
- **Password** : votre mot de passe Gitea

## 🏗️ Workflow complet de soumission

### Étape 1 : Créer/modifier vos fichiers

Créez votre projet dans le dossier cloné :

```bash
# Exemple : Créer les fichiers nécessaires
touch Dockerfile
touch docker-compose.yml
mkdir app
touch app/index.html
```

### Étape 2 : Vérifier l'état de Git

```bash
# Voir les fichiers modifiés
git status
```

Résultat :
```
On branch main
Untracked files:
  (use "git add <file>..." to include in what will be committed)
	Dockerfile
	docker-compose.yml
	app/

nothing added to commit but untracked files present
```

### Étape 3 : Ajouter les fichiers au staging

```bash
# Ajouter tous les fichiers
git add .

# OU ajouter des fichiers spécifiques
git add Dockerfile docker-compose.yml app/
```

Vérifier à nouveau :
```bash
git status
```

Résultat :
```
On branch main
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	new file:   Dockerfile
	new file:   docker-compose.yml
	new file:   app/index.html
```

### Étape 4 : Créer un commit

```bash
# Commit avec un message descriptif
git commit -m "TD1: Application web avec Nginx"
```

**Bonnes pratiques pour les messages de commit :**

✅ **BON** :
```bash
git commit -m "TD1: Application web avec Nginx et Docker Compose"
git commit -m "Ajout du healthcheck dans le Dockerfile"
git commit -m "Correction: Ports mal configurés dans compose.yml"
```

❌ **MAUVAIS** :
```bash
git commit -m "update"
git commit -m "fix"
git commit -m "test"
```

### Étape 5 : Push vers Gitea

```bash
# Push vers la branche main
git push origin main
```

Git vous demandera à nouveau vos identifiants Gitea.

## 🔄 Workflow de mise à jour

### Après la première soumission

Si vous modifiez vos fichiers après le premier push :

```bash
# 1. Vérifier les modifications
git status

# 2. Ajouter les modifications
git add .

# 3. Commit
git commit -m "TD1: Amélioration du Dockerfile"

# 4. Push
git push origin main
```

### Commandes utiles

```bash
# Voir l'historique des commits
git log

# Voir les différences avant de commit
git diff

# Annuler les modifications d'un fichier
git checkout -- Dockerfile

# Voir les branches
git branch

# Récupérer les dernières modifications depuis Gitea
git pull origin main
```

## 📊 Vérifier que le push a fonctionné

### Dans votre terminal

Après `git push`, vous devriez voir :

```
Enumerating objects: 5, done.
Counting objects: 100% (5/5), done.
Delta compression using up to 8 threads
Compressing objects: 100% (3/3), done.
Writing objects: 100% (3/3), 345 bytes | 345.00 KiB/s, done.
Total 3 (delta 2), reused 0 (delta 0), pack-reused 0
remote: . Processing 1 references
remote: Processed 1 references in total
To https://git.zohrabi.cloud/Groupe-A/jean.dupont-tds.git
   abc1234..def5678  main -> main
```

### Sur Gitea

1. Allez sur https://git.zohrabi.cloud
2. Ouvrez votre repository
3. Vérifiez que vos fichiers apparaissent
4. Allez dans l'onglet **"Actions"**
5. Vous devriez voir le workflow de correction en cours

## 🚫 Problèmes courants et solutions

### Problème 1 : Authentification échoue

**Symptôme :**
```
remote: Invalid username or password.
fatal: Authentication failed
```

**Solutions :**

1. Vérifier votre nom d'utilisateur et mot de passe
2. Si vous avez changé votre mot de passe, utilisez le nouveau
3. Essayer de vous reconnecter sur https://git.zohrabi.cloud

### Problème 2 : Conflit de merge

**Symptôme :**
```
error: failed to push some refs to 'https://git.zohrabi.cloud/...'
hint: Updates were rejected because the remote contains work that you do not have locally.
```

**Solution :**
```bash
# Récupérer les modifications distantes
git pull origin main

# Résoudre les conflits si nécessaire
# Puis push à nouveau
git push origin main
```

### Problème 3 : Fichiers non suivis (untracked)

**Symptôme :**
Vos fichiers n'apparaissent pas après `git status`

**Solution :**
```bash
# Vérifier que vous êtes dans le bon dossier
pwd

# Lister tous les fichiers
ls -la

# Ajouter explicitement
git add Dockerfile docker-compose.yml
```

### Problème 4 : .gitignore bloque des fichiers

**Symptôme :**
Certains fichiers ne sont jamais ajoutés

**Solution :**

Créer/modifier `.gitignore` :
```bash
# Fichiers à ignorer
node_modules/
*.log
.env
.DS_Store

# Mais ne PAS ignorer les fichiers nécessaires :
# !Dockerfile
# !docker-compose.yml
```

## 🔐 Authentification SSH (Avancé)

Pour éviter de taper le mot de passe à chaque fois :

### Étape 1 : Générer une clé SSH

```bash
ssh-keygen -t ed25519 -C "jean.dupont@students.zohrabi.cloud"
# Appuyer sur Entrée pour tout accepter par défaut
```

### Étape 2 : Copier la clé publique

```bash
cat ~/.ssh/id_ed25519.pub
```

Copier tout le contenu affiché.

### Étape 3 : Ajouter la clé dans Gitea

1. Aller sur https://git.zohrabi.cloud
2. **Paramètres** → **Clés SSH/GPG**
3. **Ajouter une clé**
4. Coller la clé publique
5. Donner un nom (ex: "Mon PC")
6. Sauvegarder

### Étape 4 : Changer l'URL du remote

```bash
# Voir l'URL actuelle
git remote -v

# Changer pour SSH
git remote set-url origin git@git.zohrabi.cloud:Groupe-A/jean.dupont-tds.git

# Vérifier
git remote -v
```

Maintenant, `git push` ne demandera plus de mot de passe !

## 📝 Checklist avant chaque push

Avant de faire `git push`, vérifiez :

- [ ] ✅ Projet testé **localement**
- [ ] ✅ `docker compose up` fonctionne
- [ ] ✅ Pas de fichiers inutiles (node_modules, etc.)
- [ ] ✅ Pas de secrets/mots de passe en clair
- [ ] ✅ Fichiers requis présents (Dockerfile, docker-compose.yml)
- [ ] ✅ Message de commit descriptif
- [ ] ✅ `git status` vérifié

## 📚 Commandes Git essentielles (Résumé)

```bash
# Configuration initiale
git config --global user.name "Votre Nom"
git config --global user.email "votre@email.com"

# Cloner un repository
git clone https://git.zohrabi.cloud/Groupe-A/username-tds.git

# Vérifier l'état
git status

# Ajouter des fichiers
git add .                    # Tous les fichiers
git add Dockerfile          # Fichier spécifique

# Créer un commit
git commit -m "Message descriptif"

# Push vers Gitea
git push origin main

# Pull (récupérer les modifications)
git pull origin main

# Voir l'historique
git log

# Voir les différences
git diff

# Annuler des modifications
git checkout -- fichier
```

## 🎯 Exemple complet de A à Z

```bash
# 1. Clone (première fois seulement)
git clone https://git.zohrabi.cloud/Groupe-A/jean.dupont-tds.git
cd jean.dupont-tds

# 2. Créer votre projet
echo "FROM nginx:alpine" > Dockerfile
echo "version: '3.8'" > docker-compose.yml

# 3. Tester localement
docker compose up -d
docker compose ps
docker compose down

# 4. Ajouter au Git
git add .

# 5. Commit
git commit -m "TD1: Premier projet Docker"

# 6. Push
git push origin main

# 7. Vérifier sur Gitea
# Aller sur https://git.zohrabi.cloud > Votre repo > Actions
```

## 🆘 Besoin d'aide ?

- 📖 Consultez la [FAQ](/page/faq)
- 💡 Guide [Git officiel](https://git-scm.com/book/fr/v2)
- 📧 Contactez : admin@zohrabi.cloud

---

**Bon push ! 🚀**