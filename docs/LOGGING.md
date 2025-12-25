# Documentation Logging - UML Vision Grader Pro

**Version** : 2.1  
**Module** : `src/uml_core/logger.py`  
**Status** : ✅ Production-ready

---

## Table des matières

1. [Vue d'ensemble](#vue-densemble)
2. [Configuration](#configuration)
3. [Utilisation](#utilisation)
4. [Niveaux de logs](#niveaux-de-logs)
5. [Rotation des fichiers](#rotation-des-fichiers)
6. [Mode DEBUG](#mode-debug)
7. [Exemples](#exemples)
8. [Dépannage](#dépannage)

---

## Vue d'ensemble

### Architecture

```
logger.py
    ↓
Dual handlers:
├── StreamHandler (Console) → Niveau INFO
└── FileHandler (Fichier)   → Niveau DEBUG
    ↓
logs/uml_grader_YYYYMMDD.log
```

### Fonctionnalités

- ✅ **Dual logging** : Console (INFO) + Fichiers (DEBUG)
- ✅ **Rotation quotidienne** : Un fichier par jour
- ✅ **Mode DEBUG** : Activable via `.env`
- ✅ **Format structuré** : Timestamp, niveau, module, fonction, message
- ✅ **Exception tracking** : Logs automatiques des erreurs avec traceback

---

## Configuration

### Structure du module

**Fichier** : `src/uml_core/logger.py`

```python
import logging
import os
from datetime import datetime

def get_logger(name: str) -> logging.Logger:
    """Obtient un logger configuré"""
    
def set_debug_mode(enabled: bool):
    """Active/désactive le mode DEBUG"""
```

### Variables d'environnement

**Fichier** : `.env`

```env
# Mode DEBUG (logs détaillés)
DEBUG=false  # true pour activer
```

### Format des logs

```
[YYYY-MM-DD HH:MM:SS] [LEVEL] [module.function] Message
```

**Exemple** :
```
[2025-12-25 14:32:15] [INFO] [app.compare_endpoint] Début de la comparaison
[2025-12-25 14:32:16] [DEBUG] [vision_llm_client.extract_uml] Envoi requête OpenAI
[2025-12-25 14:32:20] [ERROR] [app.compare_endpoint] Erreur upload: File too large
```

---

## Utilisation

### Import et initialisation

```python
from uml_core.logger import get_logger

# Créer un logger pour le module
logger = get_logger(__name__)
```

### Logging de base

```python
# Information importante
logger.info("Traitement démarré")

# Avertissement
logger.warning("Fichier volumineux, traitement long possible")

# Erreur
logger.error("Échec de l'upload")

# Erreur critique
logger.critical("API OpenAI inaccessible")
```

### Logging avec variables

```python
# Avec f-strings
username = "john_doe"
logger.info(f"Utilisateur connecté: {username}")

# Avec paramètres (recommandé)
logger.info("Utilisateur connecté: %s", username)

# Multiples variables
filename = "diagram.png"
size_mb = 2.5
logger.info("Fichier uploadé: %s (%.2f MB)", filename, size_mb)
```

### Logging d'exceptions

```python
try:
    result = process_image(image_path)
except Exception as e:
    # Logs automatiques du traceback
    logger.error("Erreur traitement image", exc_info=True)
    
    # Ou avec message personnalisé
    logger.exception("Erreur traitement image: %s", str(e))
```

### Logging conditionnel

```python
import os

# Mode DEBUG activé ?
if os.getenv('DEBUG', 'false').lower() == 'true':
    logger.debug("Détails de configuration: %s", config)
```

---

## Niveaux de logs

### Hiérarchie

| Niveau | Valeur | Usage | Console | Fichier |
|--------|--------|-------|---------|---------|
| DEBUG | 10 | Détails développement | ❌ | ✅ |
| INFO | 20 | Événements importants | ✅ | ✅ |
| WARNING | 30 | Avertissements | ✅ | ✅ |
| ERROR | 40 | Erreurs | ✅ | ✅ |
| CRITICAL | 50 | Erreurs critiques | ✅ | ✅ |

### Quand utiliser chaque niveau ?

#### DEBUG
- Détails techniques
- Variables intermédiaires
- État interne du programme
- Seulement visible en mode DEBUG

```python
logger.debug("Paramètres reçus: student=%s, reference=%s", student_path, ref_path)
logger.debug("Résultat preprocessing: taille=%dx%d", width, height)
```

#### INFO
- Événements importants
- Début/fin de processus
- Actions utilisateur
- Visible en production

```python
logger.info("Serveur démarré sur http://localhost:8000")
logger.info("Comparaison terminée avec succès")
logger.info("Utilisateur %s a uploadé un fichier", username)
```

#### WARNING
- Situations anormales mais gérables
- Comportements non optimaux
- Dépréciations

```python
logger.warning("Fichier volumineux (%.2f MB), traitement long", size_mb)
logger.warning("API OpenAI lente, retry en cours")
logger.warning("Fonction deprecated: utilisez new_function()")
```

#### ERROR
- Erreurs empêchant une opération
- Exceptions catchées
- Problèmes graves mais récupérables

```python
logger.error("Upload échoué: fichier trop volumineux (max 10MB)")
logger.error("API OpenAI inaccessible, code %d", status_code)
logger.error("Fichier JSON invalide", exc_info=True)
```

#### CRITICAL
- Erreurs fatales
- Application compromise
- Nécessite intervention immédiate

```python
logger.critical("OPENAI_API_KEY manquante, arrêt du serveur")
logger.critical("Disque plein, impossible d'écrire les logs")
logger.critical("Corruption de données détectée")
```

---

## Rotation des fichiers

### Stratégie

**Rotation quotidienne** : Un nouveau fichier chaque jour

```
logs/
├── uml_grader_20251220.log
├── uml_grader_20251221.log
├── uml_grader_20251222.log
├── uml_grader_20251223.log
├── uml_grader_20251224.log
└── uml_grader_20251225.log  (aujourd'hui)
```

### Format du nom

```
uml_grader_YYYYMMDD.log
```

**Exemples** :
- `uml_grader_20251225.log` → 25 décembre 2025
- `uml_grader_20260101.log` → 1er janvier 2026

### Nettoyage manuel

```powershell
# Supprimer les logs de plus de 30 jours (Windows)
Get-ChildItem logs\uml_grader_*.log | 
    Where-Object {$_.LastWriteTime -lt (Get-Date).AddDays(-30)} | 
    Remove-Item

# Linux/macOS
find logs/ -name "uml_grader_*.log" -mtime +30 -delete
```

### Automatisation (à ajouter)

```python
# À implémenter dans logger.py
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    'logs/uml_grader.log',
    maxBytes=10*1024*1024,  # 10MB
    backupCount=30  # Garder 30 fichiers
)
```

---

## Mode DEBUG

### Activation

**Méthode 1 : Variable d'environnement**

```env
# .env
DEBUG=true
```

**Méthode 2 : Code Python**

```python
from uml_core.logger import set_debug_mode

set_debug_mode(True)
```

**Méthode 3 : Ligne de commande**

```bash
# Windows PowerShell
$env:DEBUG="true"; python run_server.py

# Linux/macOS
DEBUG=true python run_server.py
```

### Différences

| Aspect | Mode NORMAL (DEBUG=false) | Mode DEBUG (DEBUG=true) |
|--------|---------------------------|-------------------------|
| Console | INFO, WARNING, ERROR | INFO, WARNING, ERROR |
| Fichiers | DEBUG, INFO, WARNING, ERROR | DEBUG, INFO, WARNING, ERROR |
| Détails | Basiques | Complets |
| Performance | Optimale | Légèrement réduite |
| Taille logs | Petite | Grande |

### Utilisation

```python
import os
from uml_core.logger import get_logger

logger = get_logger(__name__)

# Logs toujours visibles
logger.info("Application démarrée")

# Logs visibles uniquement en DEBUG
if os.getenv('DEBUG', 'false').lower() == 'true':
    logger.debug("Configuration: %s", config)
    logger.debug("Variables d'environnement: %s", os.environ)
```

---

## Exemples

### Exemple 1 : Module de comparaison

```python
# scripts/compare.py
from uml_core.logger import get_logger

logger = get_logger(__name__)

def compare_diagrams(student_path, reference_path):
    logger.info("Début comparaison: student=%s, reference=%s", 
                student_path, reference_path)
    
    try:
        # Lecture fichiers
        logger.debug("Lecture fichier étudiant")
        student_data = read_image(student_path)
        
        logger.debug("Lecture fichier référence")
        reference_data = read_json(reference_path)
        
        # Traitement
        logger.info("Envoi requête OpenAI")
        result = extract_uml_json_from_image(student_path, reference_data)
        
        logger.info("Comparaison terminée avec succès")
        return result
        
    except FileNotFoundError as e:
        logger.error("Fichier non trouvé: %s", str(e))
        raise
    except Exception as e:
        logger.error("Erreur comparaison", exc_info=True)
        raise
```

### Exemple 2 : API FastAPI

```python
# src/webapp/app.py
from uml_core.logger import get_logger
from fastapi import FastAPI, HTTPException

logger = get_logger(__name__)
app = FastAPI()

@app.post("/compare")
async def compare_endpoint(student: UploadFile, reference: UploadFile):
    logger.info("Requête /compare reçue: student=%s, reference=%s",
                student.filename, reference.filename)
    
    # Validation
    if student.size > 10 * 1024 * 1024:
        logger.warning("Fichier trop volumineux: %.2f MB", 
                      student.size / 1024 / 1024)
        raise HTTPException(400, "Fichier trop volumineux (max 10MB)")
    
    try:
        # Traitement
        logger.debug("Sauvegarde temporaire fichiers")
        student_path = save_temp_file(student)
        reference_path = save_temp_file(reference)
        
        logger.info("Lancement analyse")
        result = compare_diagrams(student_path, reference_path)
        
        logger.info("Analyse terminée avec succès")
        return result
        
    except Exception as e:
        logger.error("Erreur endpoint /compare", exc_info=True)
        raise HTTPException(500, "Erreur serveur")
```

### Exemple 3 : Prétraitement d'image

```python
# src/uml_core/preprocess_image.py
import cv2
from uml_core.logger import get_logger

logger = get_logger(__name__)

def preprocess_image(image_path):
    logger.info("Début prétraitement: %s", image_path)
    
    try:
        # Étape 1: Lecture
        logger.debug("Lecture image")
        img = cv2.imread(image_path)
        
        if img is None:
            logger.error("Impossible de lire l'image: %s", image_path)
            raise ValueError(f"Image invalide: {image_path}")
        
        # Étape 2: Redimensionnement
        h, w = img.shape[:2]
        logger.debug("Taille originale: %dx%d", w, h)
        
        if max(w, h) > 1536:
            logger.info("Redimensionnement nécessaire (max 1536px)")
            img = resize_image(img, 1536)
            logger.debug("Nouvelle taille: %dx%d", img.shape[1], img.shape[0])
        
        # Étape 3-11: Autres traitements
        logger.debug("Application pipeline OpenCV (11 étapes)")
        img = apply_pipeline(img)
        
        # Sauvegarde
        output_path = image_path.replace('.png', '_processed.png')
        cv2.imwrite(output_path, img)
        logger.info("Prétraitement terminé: %s", output_path)
        
        return output_path
        
    except Exception as e:
        logger.error("Erreur prétraitement", exc_info=True)
        raise
```

---

## Dépannage

### Logs non générés

**Problème** : Aucun fichier dans `logs/`

**Solutions** :

```bash
# Vérifier que le dossier existe
mkdir logs

# Vérifier les permissions (Linux/macOS)
chmod 755 logs/

# Vérifier le code
python -c "from uml_core.logger import get_logger; logger = get_logger('test'); logger.info('Test')"

# Vérifier les logs
cat logs/uml_grader_*.log
```

### Logs vides ou incomplets

**Problème** : Fichiers créés mais vides

**Solutions** :

```python
# Forcer le flush des buffers
import logging
logging.shutdown()

# Ou utiliser flush manuel
import sys
sys.stdout.flush()
sys.stderr.flush()
```

### Logs en double

**Problème** : Messages dupliqués

**Solutions** :

```python
# Éviter les handlers multiples
logger = get_logger(__name__)

# Ne PAS réinitialiser le logger
# ❌ logger = logging.getLogger(__name__)
# ❌ logger.addHandler(handler)
```

### Mode DEBUG ne fonctionne pas

**Problème** : `DEBUG=true` sans effet

**Solutions** :

```bash
# Vérifier la variable d'environnement
echo $env:DEBUG  # PowerShell
echo $DEBUG      # Linux/macOS

# Redémarrer le serveur après modification .env
python run_server.py

# Vérifier le code
python -c "import os; print(os.getenv('DEBUG', 'not set'))"
```

### Performances dégradées

**Problème** : Logs ralentissent l'application

**Solutions** :

```python
# Désactiver DEBUG en production
DEBUG=false

# Réduire la verbosité
logger.setLevel(logging.WARNING)

# Utiliser logging conditionnel
if logger.isEnabledFor(logging.DEBUG):
    logger.debug("Message coûteux: %s", expensive_operation())
```

---

## Bonnes pratiques

### 1. Utiliser des noms de logger appropriés

```python
# ✅ Bon: Utiliser __name__
logger = get_logger(__name__)

# ❌ Éviter: Noms génériques
logger = get_logger('app')
```

### 2. Ne pas logger de données sensibles

```python
# ❌ Éviter: Clés API, mots de passe
logger.info("API key: %s", api_key)

# ✅ Bon: Masquer les données sensibles
logger.info("API key: %s***", api_key[:8])
```

### 3. Utiliser le bon niveau de log

```python
# ❌ Éviter: Tout en ERROR
logger.error("Utilisateur connecté")

# ✅ Bon: Niveau approprié
logger.info("Utilisateur connecté")
```

### 4. Logger les exceptions avec traceback

```python
# ❌ Éviter: Perdre le traceback
except Exception as e:
    logger.error(str(e))

# ✅ Bon: Conserver le traceback
except Exception as e:
    logger.error("Erreur traitement", exc_info=True)
```

### 5. Utiliser des messages descriptifs

```python
# ❌ Éviter: Messages vagues
logger.error("Error")

# ✅ Bon: Messages explicites
logger.error("Échec upload fichier: taille %.2f MB dépasse limite 10MB", size_mb)
```

---

## Ressources

### Documentation Python logging
- [Documentation officielle](https://docs.python.org/3/library/logging.html)
- [Logging HOWTO](https://docs.python.org/3/howto/logging.html)
- [Logging Cookbook](https://docs.python.org/3/howto/logging-cookbook.html)

### Outils complémentaires
- **Loguru** : Alternative moderne à logging
- **structlog** : Logs structurés JSON
- **Sentry** : Monitoring erreurs en production
- **ELK Stack** : Elasticsearch + Logstash + Kibana

---

**Auteur** : GitHub Copilot  
**Date** : Décembre 2025  
**Version** : 2.1  
**Status** : ✅ Production-ready
