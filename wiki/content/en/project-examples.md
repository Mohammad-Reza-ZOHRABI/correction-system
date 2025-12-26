---
title: "Project Examples"
description: "Concrete examples of Docker projects to inspire you"
order: 3
category: "📚 Resources"
---

# Project Examples

Here are examples of containerized projects to guide you in your assignments.

## 🌐 Project 1: Static Website with Nginx

### Description
A simple HTML/CSS website served by Nginx.

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

# Copy website files
COPY app/ /usr/share/nginx/html/

# Expose port 80
EXPOSE 80

# Nginx in foreground mode
CMD ["nginx", "-g", "daemon off;"]
```

### docker-compose.yml
```yaml
version: '3.8'

services:
  web:
    build: .
    container_name: my-website
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
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Docker Website</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <h1>🐳 My First Website with Docker</h1>
    </header>
    <main>
        <p>This website is served by a Docker container with Nginx!</p>
    </main>
</body>
</html>
```

### Commands
```bash
# Build and start
docker compose up -d

# See logs
docker compose logs -f

# Access the website
curl http://localhost:8080
# or open in a browser

# Stop
docker compose down
```

---

## 🐍 Project 2: Python API with Flask

### Description
A simple REST API with Flask and PostgreSQL database.

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

# Install dependencies
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy code
COPY app/ .

# Expose port
EXPOSE 5000

# Launch application
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
        "message": "Flask API with Docker",
        "version": "1.0",
        "database": os.getenv("DATABASE_URL", "Not configured")
    })

@app.route('/health')
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

### Commands
```bash
# Build and start
docker compose up -d

# Test the API
curl http://localhost:5000
curl http://localhost:5000/health

# See logs
docker compose logs -f api

# Stop
docker compose down -v  # -v to remove volumes
```

---

## ⚛️ Project 3: React Application Multi-Stage

### Description
React application with optimized multi-stage build.

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

# Copy package.json and install dependencies
COPY package*.json ./
RUN npm ci --only=production

# Copy source code and build
COPY . .
RUN npm run build

# Stage 2: Production
FROM nginx:alpine

# Copy built files from previous stage
COPY --from=build /app/build /usr/share/nginx/html

# Copy custom nginx config (optional)
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

### Multi-stage Build Advantages
- ✅ Final image very lightweight (only Nginx + static files)
- ✅ No Node.js in production image
- ✅ Enhanced security
- ✅ Faster deployment

---

## 🔧 Project 4: Complete Stack (Frontend + Backend + DB)

### Description
Complete application with React (frontend), Node.js (backend), and MongoDB.

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

## 💡 Observed Best Practices

### 1. Base Images
- ✅ Use **alpine** variants (lighter)
- ✅ Specify a **precise version** (not `latest`)
- ✅ Prefer official images

### 2. Security
- ✅ No hardcoded secrets in files
- ✅ Use environment variables
- ✅ Don't expose unnecessary ports

### 3. Performance
- ✅ Multi-stage builds to reduce size
- ✅ Optimized Docker layer cache
- ✅ `.dockerignore` to exclude unnecessary files

### 4. Maintenance
- ✅ Documented README.md
- ✅ Accessible logs
- ✅ Configured healthchecks

---

## 📝 .dockerignore Example

Create a `.dockerignore` file at the root:

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

## 🚀 Going Further

### Add Healthchecks

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

### Limit Resources

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

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- [Dockerfile Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)

---

**Need help?** Check the [FAQ](/page/faq) or contact **Reza@zohrabi.fr**