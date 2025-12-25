"""Module de logging centralisé pour UML Vision Grader Pro.

Fournit un logger configuré avec différents niveaux (DEBUG, INFO, WARNING, ERROR).
Remplace les appels print() pour un logging professionnel.

Usage:
    from uml_core.logger import logger
    
    logger.info("Message d'information")
    logger.warning("Message d'avertissement")
    logger.error("Message d'erreur")
    logger.debug("Message de debug (visible uniquement si DEBUG=true)")
"""

import logging
import sys
import os
from datetime import datetime

# Créer le dossier logs s'il n'existe pas
LOG_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

# Configuration du logger
logger = logging.getLogger('uml_grader')
logger.setLevel(logging.DEBUG)

# Format des logs
formatter = logging.Formatter(
    '[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Handler console (stdout)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)  # Par défaut INFO en console
console_handler.setFormatter(formatter)

# Handler fichier (logs complets)
log_file = os.path.join(LOG_DIR, f'uml_grader_{datetime.now().strftime("%Y%m%d")}.log')
file_handler = logging.FileHandler(log_file, encoding='utf-8')
file_handler.setLevel(logging.DEBUG)  # Tout dans le fichier
file_handler.setFormatter(formatter)

# Ajouter les handlers
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Empêcher la propagation aux loggers parents
logger.propagate = False


def set_debug_mode(enabled: bool = True):
    """Active ou désactive le mode debug en console.
    
    Args:
        enabled (bool): True pour afficher les logs DEBUG en console
    """
    if enabled:
        console_handler.setLevel(logging.DEBUG)
        logger.info("Mode DEBUG activé")
    else:
        console_handler.setLevel(logging.INFO)
        logger.info("Mode DEBUG désactivé")


# Vérifier variable d'environnement pour activer DEBUG
if os.environ.get('DEBUG', '').lower() in ('true', '1', 'yes'):
    set_debug_mode(True)
