---
title: "Premiers Pas"
description: "Guide de démarrage rapide pour commencer avec le système"
order: 1
category: "🚀 Démarrage"
---

# Premiers Pas

Bienvenue dans le système de correction automatique ! Ce guide vous explique comment démarrer rapidement.

## 📧 1. Réception de votre compte

Vous recevrez un email contenant :

- **Nom d'utilisateur** : `prenom.nom`
- **Mot de passe temporaire** : À changer à la première connexion
- **Lien Gitea** : https://git.zohrabi.cloud
- **Votre groupe** : Groupe-A, Groupe-B, etc.

## 🔑 2. Première connexion

### Étape 1 : Accéder à Gitea

1. Ouvrez votre navigateur
2. Allez sur : **https://git.zohrabi.cloud**
3. Cliquez sur **"Se connecter"** en haut à droite

### Étape 2 : Connexion

1. **Nom d'utilisateur** : Celui reçu par email
2. **Mot de passe** : Le mot de passe temporaire
3. Cliquez sur **"Se connecter"**

### Étape 3 : Changer le mot de passe

⚠️ **Important** : Vous devrez changer votre mot de passe lors de la première connexion.

1. Choisissez un mot de passe fort (min. 8 caractères)
2. Confirmez le nouveau mot de passe
3. Validez

## 📁 3. Accéder à votre repository

Après connexion, vous verrez :

- **Organisations** : Votre groupe (ex: Groupe-A)
- **Repositories** : Votre repository personnel (ex: `jean.dupont-tds`)

### Cliquer sur votre repository

Vous verrez la structure de base :
```
README.md
.gitea/
  └── workflows/
      └── correction.yml
```

Le fichier `correction.yml` contient le workflow de correction automatique (ne pas le modifier).

## 💻 4. Cloner votre repository

### Option A : HTTPS (Recommandé pour débuter)

```bash
# Remplacer par votre nom d'utilisateur
git clone https://git.zohrabi.cloud/Groupe-A/jean.dupont-tds.git

cd jean.dupont-tds
```

Lors du clone, Git vous demandera :
- **Username** : votre nom d'utilisateur Gitea
- **Password** : votre mot de passe Gitea

### Option B : SSH (Avancé)

**Prérequis** : Avoir configuré une clé SSH dans Gitea

1. Générer une clé SSH (si vous n'en avez pas) :
   ```bash
   ssh-keygen -t ed25519 -C "votre.email@example.com"
   ```

2. Copier la clé publique :
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```

3. Dans Gitea : **Paramètres → Clés SSH/GPG → Ajouter une clé**

4. Cloner avec SSH :
   ```bash
   git clone git@git.zohrabi.cloud:Groupe-A/jean.dupont-tds.git
   ```

## 🏗️ 5. Créer votre premier projet

### Structure minimale requise

Votre projet doit contenir **au minimum** :

```
mon-projet/
├── Dockerfile              # Obligatoire
├── docker-compose.yml      # Obligatoire
├── app/                    # Vos fichiers d'application
│   └── index.html
└── README.md              # Recommandé
```

### Exemple : Application web simple

**Dockerfile** :
```dockerfile
FROM nginx:alpine
COPY app/ /usr/share/nginx/html/
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**docker-compose.yml** :
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "80:80"
    networks:
      - frontend

networks:
  frontend:
```

**app/index.html** :
```html
<!DOCTYPE html>
<html>
<head>
    <title>Mon Projet TD1</title>
</head>
<body>
    <h1>Hello Docker !</h1>
    <p>Mon premier projet containerisé</p>
</body>
</html>
```

## 📤 6. Soumettre votre projet

### Vérifier que tout fonctionne localement

**Avant de push**, testez en local :

```bash
# Build
docker compose build

# Démarrer
docker compose up -d

# Tester
curl http://localhost
# OU ouvrir http://localhost dans un navigateur

# Vérifier les logs
docker compose logs

# Arrêter
docker compose down
```

### Git : Add, Commit, Push

Une fois que tout fonctionne :

```bash
# Ajouter tous les fichiers
git add .

# Commit avec un message descriptif
git commit -m "TD1: Application web avec Nginx"

# Push vers Gitea
git push origin main
```

## ✅ 7. Correction automatique

### Déclenchement

Dès que vous faites `git push`, la correction automatique se lance :

1. **Gitea Actions** détecte le push
2. Le **workflow de correction** démarre
3. Tests et évaluation de votre projet
4. **Email envoyé** avec votre note

### Suivre la correction en temps réel

1. Aller sur Gitea
2. Ouvrir votre repository
3. Cliquer sur l'onglet **"Actions"**
4. Voir le workflow en cours

Vous verrez :
- ✅ **Running** : Correction en cours
- ✅ **Success** : Correction terminée avec succès
- ❌ **Failure** : Erreur détectée

### Consulter le rapport

Vous recevrez un **email** contenant :

- 📊 **Votre note** sur 100
- 📋 **Rapport détaillé** en HTML
- ✅ **Points obtenus** par critère
- 📝 **Logs** de la correction
- 💡 **Conseils** d'amélioration

## 🔄 8. Itérer et améliorer

Vous pouvez soumettre **plusieurs fois** :

- La **meilleure note** est conservée
- Chaque push déclenche une nouvelle correction
- Consultez les logs pour comprendre les erreurs

```bash
# Modifier vos fichiers
nano Dockerfile

# Tester localement
docker compose up -d

# Si OK, push à nouveau
git add .
git commit -m "TD1: Amélioration du Dockerfile"
git push origin main
```

## 📌 Points importants

### ✅ À FAIRE

- ✅ Tester **localement** avant de push
- ✅ Utiliser des **images officielles**
- ✅ Respecter la **structure requise**
- ✅ Documenter avec un **README.md**
- ✅ Messages de commit **descriptifs**

### ❌ À ÉVITER

- ❌ Push sans test local
- ❌ Images sans tag spécifique
- ❌ Mots de passe en clair
- ❌ Fichiers inutiles (node_modules, etc.)

## 🆘 Besoin d'aide ?

- 📖 Consultez la [FAQ](/page/faq)
- 💡 Voir les [Exemples de projets](/page/exemples-projets)
- 📧 Contactez : admin@zohrabi.cloud

---

**Prêt à commencer ? Bon courage ! 🚀**