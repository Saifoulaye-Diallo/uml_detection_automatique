"""Configuration et gestion des variables d'environnement.

Ce module charge les variables d'environnement depuis le fichier .env
et expose les clés API nécessaires pour l'application.

Variables d'environnement requises:
    OPENAI_API_KEY: Clé API OpenAI pour GPT-4o Vision
    OPENAI_API_BASE: URL de base de l'API OpenAI (optionnel)

Author: UML Vision Grader Pro
Version: 2.0
Date: 2025
"""

from dotenv import load_dotenv
import os
import logging

# Charger le .env depuis la racine du projet (2 niveaux au-dessus de ce fichier)
env_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path=env_path, override=True)

logger = logging.getLogger('uml_grader.env')

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_API_BASE = os.environ.get(
    "OPENAI_API_BASE",
    "https://api.openai.com/v1")

if not OPENAI_API_KEY:
    raise RuntimeError(
        "OPENAI_API_KEY manquant dans l'environnement ou le .env\n"
        "Créez un fichier .env à la racine avec : OPENAI_API_KEY=sk-proj-..."
    )

# Log de confirmation en mode DEBUG
if os.environ.get("DEBUG") == "true":
    logger.debug(f"Clé API chargée: {OPENAI_API_KEY[:15]}...{OPENAI_API_KEY[-10:]}")
    logger.debug(f"API Base: {OPENAI_API_BASE}")
