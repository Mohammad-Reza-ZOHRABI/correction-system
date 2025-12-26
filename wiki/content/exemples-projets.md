---
title: "Exemples de Projets"
description: "Exemples concrets de projets Docker pour vous inspirer"
order: 3
category: "📚 Ressources"
---

# Exemples de Projets

Voici des exemples de projets containerisés pour vous guider dans vos TDs.

## 🌐 Projet 1 : Site Web Statique avec Nginx

### Description
Un site web HTML/CSS simple servi par Nginx.

### Structure
```
td1-site-web/
├── Dockerfile
├── docker-compose.yml
├── app/
│   ├── index.html
│   ├── style.css
│   └── assets/
│       └── logo.png
└── README.md
```

### Dockerfile
```dockerfile
FROM nginx:alpine

# Copier les fichiers du site
COPY app/ /usr/share/nginx/html/

# Exposer le port 80
EXPOSE 80

# Nginx en mode foreground
CMD ["nginx", "-g", "daemon off;"]
```

### docker-compose.yml
```yaml
version: '3.8'

services:
  web:
    build: .
    container_name: mon-site-web
    ports:
      - "8080:80"
    networks:
      - frontend
    restart: unless-stopped

networks:
  frontend:
    driver: bridge
```

### app/index.html
```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mon Site Web Docker</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <h1>🐳 Mon Premier Site avec Docker</h1>
    </header>
    <main>
        <p>Ce site est servi par un conteneur Docker avec Nginx!</p>
    </main>
</body>
</html>
```

### Commandes
```bash
# Build et démarrer
docker compose up -d

# Voir les logs
docker compose logs -f

# Accéder au site
curl http://localhost:8080
# ou ouvrir dans un navigateur

# Arrêter
docker compose down
```

---

## 🐍 Projet 2 : API Python avec Flask

### Description
Une API REST simple avec Flask et base de données PostgreSQL.

### Structure
```
td2-api-flask/
├── Dockerfile
├── docker-compose.yml
├── app/
│   ├── app.py
│   └── requirements.txt
└── README.md
```

### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Installer les dépendances
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code
COPY app/ .

# Exposer le port
EXPOSE 5000

# Lancer l'application
CMD ["python", "app.py"]
```

### docker-compose.yml
```yaml
version: '3.8'

services:
  api:
    build: .
    container_name: flask-api
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/mydb
    depends_on:
      - db
    networks:
      - backend
    restart: unless-stopped

  db:
    image: postgres:15-alpine
    container_name: postgres-db
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=mydb
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - backend
    restart: unless-stopped

networks:
  backend:
    driver: bridge

volumes:
  postgres_data:
```

### app/requirements.txt
```
Flask==3.0.0
psycopg2-binary==2.9.9
```

### app/app.py
```python
from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "message": "API Flask avec Docker",
        "version": "1.0",
        "database": os.getenv("DATABASE_URL", "Not configured")
    })

@app.route('/health')
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

### Commandes
```bash
# Build et démarrer
docker compose up -d

# Tester l'API
curl http://localhost:5000
curl http://localhost:5000/health

# Voir les logs
docker compose logs -f api

# Arrêter
docker compose down -v  # -v pour supprimer les volumes
```

---

## ⚛️ Projet 3 : Application React Multi-Stage

### Description
Application React avec build optimisé multi-stage.

### Structure
```
td3-react-app/
├── Dockerfile
├── docker-compose.yml
├── src/
│   ├── App.js
│   ├── index.js
│   └── ...
├── public/
│   └── index.html
├── package.json
└── README.md
```

### Dockerfile (Multi-stage)
```dockerfile
# Stage 1: Build
FROM node:18-alpine AS build

WORKDIR /app

# Copier package.json et installer les dépendances
COPY package*.json ./
RUN npm ci --only=production

# Copier le code source et builder
COPY . .
RUN npm run build

# Stage 2: Production
FROM nginx:alpine

# Copier les fichiers buildés depuis le stage précédent
COPY --from=build /app/build /usr/share/nginx/html

# Copier la config nginx personnalisée (optionnel)
# COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### docker-compose.yml
```yaml
version: '3.8'

services:
  app:
    build: .
    container_name: react-app
    ports:
      - "3000:80"
    networks:
      - frontend
    restart: unless-stopped

networks:
  frontend:
    driver: bridge
```

### Avantages du Multi-stage
- ✅ Image finale très légère (seulement Nginx + fichiers statiques)
- ✅ Pas de Node.js dans l'image de production
- ✅ Sécurité renforcée
- ✅ Déploiement plus rapide

---

## 🔧 Projet 4 : Stack Complète (Frontend + Backend + DB)

### Description
Application complète avec React (frontend), Node.js (backend), et MongoDB.

### docker-compose.yml
```yaml
version: '3.8'

services:
  frontend:
    build: ./frontend
    container_name: react-frontend
    ports:
      - "3000:80"
    depends_on:
      - backend
    networks:
      - app-network
    restart: unless-stopped

  backend:
    build: ./backend
    container_name: nodejs-backend
    ports:
      - "5000:5000"
    environment:
      - MONGODB_URI=mongodb://mongo:27017/myapp
      - NODE_ENV=production
    depends_on:
      - mongo
    networks:
      - app-network
    restart: unless-stopped

  mongo:
    image: mongo:7-jammy
    container_name: mongodb
    volumes:
      - mongo_data:/data/db
    networks:
      - app-network
    restart: unless-stopped

networks:
  app-network:
    driver: bridge

volumes:
  mongo_data:
```

---

## 💡 Bonnes Pratiques Observées

### 1. Images de Base
- ✅ Utiliser des variantes **alpine** (plus légères)
- ✅ Spécifier une **version précise** (pas `latest`)
- ✅ Images officielles privilégiées

### 2. Sécurité
- ✅ Pas de secrets en dur dans les fichiers
- ✅ Utiliser des variables d'environnement
- ✅ Ne pas exposer de ports inutiles

### 3. Performance
- ✅ Multi-stage builds pour réduire la taille
- ✅ Cache des layers Docker optimisé
- ✅ `.dockerignore` pour exclure les fichiers inutiles

### 4. Maintenance
- ✅ README.md documenté
- ✅ Logs accessibles
- ✅ Healthchecks configurés

---

## 📝 .dockerignore Exemple

Créez un fichier `.dockerignore` à la racine :

```
node_modules/
npm-debug.log
.git
.gitignore
README.md
.env
.vscode/
.idea/
*.md
.DS_Store
```

---

## 🚀 Pour Aller Plus Loin

### Ajouter des Healthchecks

```yaml
services:
  api:
    build: .
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 3s
      retries: 3
      start_period: 10s
```

### Limiter les Ressources

```yaml
services:
  api:
    build: .
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
```

---

## 📚 Ressources Supplémentaires

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- [Dockerfile Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)

---

**Besoin d'aide ?** Consultez la [FAQ](/page/faq) ou contactez **Reza@zohrabi.fr**