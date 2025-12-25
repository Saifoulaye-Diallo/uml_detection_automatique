# Guide de déploiement Docker

## Lancement rapide

### Avec Docker Compose (recommandé)

```bash
# 1. Configurer la clé API
echo "OPENAI_API_KEY=sk-proj-votre-clé" > .env

# 2. Lancer le stack
docker-compose up -d

# 3. Vérifier les logs
docker-compose logs -f uml-grader

# 4. Accéder à l'interface
# http://localhost:8000
```

### Avec Docker seul

```bash
# Build
docker build -t uml-grader-pro:latest .

# Run
docker run -d \
  --name uml-grader \
  -p 8000:8000 \
  -e OPENAI_API_KEY=sk-proj-votre-clé \
  -v $(pwd)/logs:/app/logs \
  uml-grader-pro:latest

# Logs
docker logs -f uml-grader
```

## Commandes utiles

```bash
# Arrêter
docker-compose down

# Redémarrer
docker-compose restart

# Rebuild
docker-compose up -d --build

# Entrer dans le container
docker exec -it uml-grader-pro bash

# Voir les ressources
docker stats uml-grader-pro
```

## Variables d'environnement

| Variable | Défaut | Description |
|----------|--------|-------------|
| `OPENAI_API_KEY` | - | Clé API OpenAI (obligatoire) |
| `OPENAI_API_BASE` | `https://api.openai.com/v1` | URL de base API |
| `DEBUG` | `false` | Mode debug (logs détaillés) |

## Production

Pour un déploiement production, ajoutez :

```yaml
# docker-compose.prod.yml
services:
  uml-grader:
    restart: always
    environment:
      - DEBUG=false
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
```

Puis lancez :
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```
