FROM python:3.11.7-slim-bookworm

WORKDIR /app

# Installation des dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copie des requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie de l'application
COPY . .

# Création du dossier logs et création d'un utilisateur non-root
RUN mkdir -p /app/logs && \
    useradd -m -u 1000 grades && \
    chown -R grades:grades /app

# Variables d'environnement par défaut
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Passage à l'utilisateur non-root
USER grades

# Exposition du port
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

# Démarrage de l'application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]