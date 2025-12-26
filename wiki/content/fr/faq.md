---
title: "FAQ - Questions Fréquentes"
description: "Réponses aux questions les plus courantes"
order: 10
category: "❓ Aide"
---

# FAQ - Questions Fréquentes

## 🔐 Authentification et Accès

### Je n'ai pas reçu mes identifiants

Vérifiez votre dossier spam. Si vous ne trouvez toujours pas l'email, contactez votre enseignant à **Reza@zohrabi.fr**.

### J'ai oublié mon mot de passe

Actuellement, vous devez contacter votre enseignant pour réinitialiser votre mot de passe. Envoyez un email à **Reza@zohrabi.fr** avec votre nom d'utilisateur.

### Mon compte est bloqué

Après 3 tentatives de connexion échouées, votre compte peut être temporairement bloqué. Attendez 15 minutes ou contactez votre enseignant.

## 📦 Git et Repository

### Comment cloner mon repository?

```bash
git clone https://git.zohrabi.cloud/VotreGroupe/votre.nom-tds.git
```

Remplacez `VotreGroupe` et `votre.nom` par vos informations.

### Je ne peux pas push vers mon repository

Vérifiez que :
- Vous êtes bien authentifié (username/password corrects)
- Vous avez les droits d'écriture sur le repository
- Vous êtes sur la bonne branche (`main` ou `master`)

```bash
git remote -v  # Vérifier l'URL
git branch     # Vérifier la branche
```

### Erreur : "fatal: unable to access"

Cette erreur signifie généralement un problème de connexion. Vérifiez :
- Votre connexion internet
- L'URL du repository est correcte
- Vos identifiants sont corrects

## 🐳 Docker et Conteneurs

### Docker Compose ne démarre pas

Vérifiez :
1. La syntaxe de votre `docker-compose.yml`
2. Les ports ne sont pas déjà utilisés
3. Les images sont correctement spécifiées

```bash
# Vérifier la syntaxe
docker compose config

# Voir les logs d'erreur
docker compose logs
```

### Erreur : "port is already allocated"

Un autre service utilise déjà ce port. Solutions :
- Changez le port dans `docker-compose.yml`
- Arrêtez le service qui utilise le port
- Utilisez `docker ps` pour voir les conteneurs actifs

### Comment nettoyer Docker?

```bash
# Arrêter tous les conteneurs
docker compose down

# Supprimer les images non utilisées
docker image prune -a

# Supprimer tous les volumes (ATTENTION : perte de données)
docker volume prune
```

## ✅ Correction Automatique

### La correction ne se déclenche pas

Vérifiez que :
- Vous avez bien fait `git push`
- Le fichier `.gitea/workflows/correction.yml` existe
- Vous n'avez pas modifié le workflow

Allez dans **Actions** sur Gitea pour voir si le workflow s'est lancé.

### Ma note est 0/100

Causes possibles :
- Le build Docker a échoué
- Le `docker-compose.yml` est invalide
- Les services requis ne démarrent pas
- Les tests ne passent pas

Consultez le rapport détaillé dans l'email pour comprendre l'erreur.

### Je n'ai pas reçu l'email avec ma note

Vérifiez :
- Votre dossier spam
- Que la correction s'est bien terminée (onglet Actions)
- Votre adresse email dans Gitea (Paramètres > Profil)

Si le problème persiste après 30 minutes, contactez votre enseignant.

### Puis-je soumettre plusieurs fois?

Oui ! Vous pouvez push autant de fois que nécessaire. La **meilleure note** sera conservée pour l'évaluation finale.

## 📝 Bonnes Pratiques

### Quelle structure de projet utiliser?

Structure minimale :
```
mon-projet/
├── Dockerfile
├── docker-compose.yml
├── app/
│   └── (vos fichiers)
└── README.md
```

### Quelles images Docker utiliser?

Privilégiez les **images officielles** :
- `nginx:alpine`
- `node:18-alpine`
- `python:3.11-slim`
- `postgres:15-alpine`

Toujours spécifier une **version/tag** (pas `latest`).

### Comment documenter mon projet?

Créez un `README.md` avec :
- Titre du projet
- Description
- Technologies utilisées
- Instructions de build et run
- Auteur

## 🔍 Debugging

### Où voir les logs de mon conteneur?

```bash
# Logs en temps réel
docker compose logs -f

# Logs d'un service spécifique
docker compose logs -f web

# Dernières 100 lignes
docker compose logs --tail=100
```

### Comment entrer dans un conteneur?

```bash
# Pour un conteneur en cours d'exécution
docker compose exec web sh

# Ou avec bash si disponible
docker compose exec web bash
```

### Mon application ne répond pas

Vérifiez :
1. Le conteneur est bien démarré : `docker compose ps`
2. Les logs : `docker compose logs`
3. Le port mapping est correct
4. Le pare-feu autorise le port

## 📊 Notes et Évaluation

### Comment est calculée ma note?

La note est basée sur :
- Build Docker réussi (20%)
- Services démarrent correctement (30%)
- Tests fonctionnels (40%)
- Bonnes pratiques (10%)

### Puis-je contester ma note?

Oui. Envoyez un email à **Reza@zohrabi.fr** avec :
- Votre nom d'utilisateur
- Le commit concerné
- Une explication détaillée

### Où consulter mes notes?

Allez sur **https://grades.zohrabi.cloud** et connectez-vous avec vos identifiants Gitea.

## 🆘 Support

### Je n'arrive pas à résoudre mon problème

1. Consultez cette FAQ
2. Vérifiez la documentation sur [zohrabi.cloud](https://zohrabi.cloud)
3. Contactez votre enseignant : **Reza@zohrabi.fr**

### Les services sont-ils disponibles 24/7?

Oui, tous les services (Gitea, Dashboard, Correction) sont disponibles 24h/24 et 7j/7.

En cas d'indisponibilité, un message sera affiché sur la page d'accueil.

---

**Une question non listée ?** Contactez **Reza@zohrabi.fr**