FROM python:3.11.7-slim-bookworm

WORKDIR /app

# Installer les dépendances système
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copier les fichiers de requirements
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier l'application
COPY . .

# Créer un utilisateur non-root
RUN useradd -m -u 1000 wiki && \
    chown -R wiki:wiki /app

USER wiki

# Exposer le port
EXPOSE 8080

# Healthcheck
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8080/health', timeout=2)"

# Démarrer l'application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]