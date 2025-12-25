# Dockerfile pour UML Vision Grader Pro
FROM python:3.12-slim

# Métadonnées
LABEL maintainer="Saifoulaye Diallo"
LABEL version="2.1.0"
LABEL description="UML Vision Grader Pro - Correction automatique de diagrammes UML"

# Variables d'environnement
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Installer les dépendances système pour OpenCV
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Répertoire de travail
WORKDIR /app

# Copier requirements et installer dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY src/ ./src/
COPY run_server.py .
COPY .env.example .env

# Créer les dossiers nécessaires
RUN mkdir -p logs uploads

# Exposer le port
EXPOSE 8000

# Commande de démarrage
CMD ["python", "run_server.py"]

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000', timeout=5)"
