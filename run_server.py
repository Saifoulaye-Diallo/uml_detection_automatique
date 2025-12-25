"""Point d'entrée pour lancer le serveur web FastAPI.

Usage:
    python run_server.py
    
Ou avec uvicorn directement depuis src/:
    cd src
    uvicorn webapp.app:app --reload --host 0.0.0.0 --port 8000
"""

import sys
import os

# Ajouter src au path pour le logger
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
from uml_core.logger import logger

# Changer le répertoire de travail vers src/
src_dir = os.path.join(os.path.dirname(__file__), 'src')
os.chdir(src_dir)

if __name__ == "__main__":
    import uvicorn
    
    logger.info("Démarrage de UML Vision Grader Pro...")
    logger.info(f"Répertoire de travail: {os.getcwd()}")
    logger.info("URL: http://localhost:8000")
    logger.info("Documentation API: http://localhost:8000/docs")
    logger.info("-" * 60)
    
    uvicorn.run(
        "webapp.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
