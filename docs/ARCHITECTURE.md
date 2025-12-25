# Documentation UML Vision Grader Pro

## Architecture du projet

### Structure des dossiers

```
Code UML/
├── src/                         # Code source principal
│   ├── uml_core/                # Moteur de base UML
│   │   ├── models.py            # Modèles de données UML
│   │   ├── vision_llm_client.py # Client GPT-4o Vision
│   │   ├── preprocess_image.py  # Pipeline OpenCV
│   │   ├── grader.py            # Système de notation
│   │   ├── serializer.py        # Sérialisation JSON
│   │   ├── logger.py            # Système de logging centralisé
│   │   └── env.py               # Configuration
│   │
│   └── webapp/                  # Application web
│       ├── app.py               # Backend FastAPI + rate limiting
│       ├── templates/           # Templates Jinja2
│       │   └── index.html       # Interface responsive
│       ├── static/              # Assets statiques
│       └── uploads/             # Fichiers temporaires
│
├── scripts/                     # Scripts utilitaires
│   ├── compare.py               # CLI de comparaison
│   └── test_openai.py           # Diagnostic API
│
├── tests/                       # Tests automatisés
│   ├── test_models.py           # Tests des modèles
│   └── test_complete.py         # Suite complète (19 tests)
│
├── .github/                     # CI/CD
│   └── workflows/
│       └── ci.yml               # GitHub Actions
│
├── logs/                        # Logs de l'application
│   └── uml_grader_*.log         # Logs quotidiens (rotation)
│
├── examples/                    # Fichiers d'exemple
│   ├── student.png              # Diagramme d'exemple
│   └── solution.json            # Référence d'exemple
│
├── docs/                        # Documentation
│   └── ARCHITECTURE.md          # Ce fichier
│
├── .env                         # Variables d'environnement (gitignored)
├── .env.example                 # Template de configuration
├── .gitignore                   # Fichiers ignorés par Git
├── requirements.txt             # Dépendances Python
└── README.md                    # Documentation principale
```

## Flux de données

### 1. Interface Web (FastAPI)

```
Utilisateur → Upload (image + JSON)
            ↓
    Validation (taille, type MIME)
            ↓
    Rate limiter (10 req/min/IP)
            ↓
    FastAPI endpoint /compare
            ↓
    Sauvegarde temporaire
            ↓
    Logging (logger.info)
            ↓
    extract_uml_json_from_image()
            ↓
    Réponse JSON avec diff + grading
```

### 2. CLI (compare.py)

```
Ligne de commande
        ↓
Parsing des arguments
        ↓
Lecture des fichiers
        ↓
extract_uml_json_from_image()
        ↓
Écriture diff.json
```

### 3. Pipeline de traitement d'image

```
Image brute (PNG/JPG)
        ↓
preprocess_image() - 11 étapes OpenCV
        ↓
Image optimisée (PNG)
        ↓
Encodage base64
        ↓
API OpenAI GPT-4o Vision
```

### 4. Extraction et comparaison

```
Image preprocessed + JSON référence
                ↓
        GPT-4o Vision API
                ↓
        Prompt 4 phases:
        1. Extraction UML
        2. Normalisation
        3. Comparaison
        4. Génération diff
                ↓
        JSON de différences
```

## Composants principaux

### uml_core.logger

**Système de logging centralisé:**
```python
get_logger(name: str) -> logging.Logger
set_debug_mode(enabled: bool)
```

**Fonctionnalités:**
- Dual handlers: Console (INFO) + Fichiers (DEBUG)
- Rotation quotidienne: `logs/uml_grader_YYYYMMDD.log`
- Mode DEBUG activable via `.env`
- Format: `[YYYY-MM-DD HH:MM:SS] [LEVEL] [module.function] Message`

**Utilisation:**
```python
from uml_core.logger import get_logger
logger = get_logger(__name__)
logger.info("Traitement démarré")
logger.error("Erreur lors de l'upload", exc_info=True)
```

### uml_core.models

**Classes principales:**
- `UMLClass`: Représentation d'une classe UML
- `UMLAttribute`: Attribut d'une classe
- `UMLOperation`: Méthode/opération
- `UMLRelationship`: Relation entre classes

**Méthodes:**
- `to_dict()`: Sérialisation en dictionnaire
- `from_dict()`: Désérialisation depuis dictionnaire

### uml_core.vision_llm_client

**Fonction principale:**
```python
extract_uml_json_from_image(
    image_path: str,
    reference_json: Optional[str] = None
) -> dict
```

**Prompt en 4 phases:**
1. **PHASE 1** - Extraction brute depuis l'image
2. **PHASE 2** - Normalisation (casse, multiplicités, types)
3. **PHASE 3** - Comparaison avec référence
4. **PHASE 4** - Génération du diff JSON final

**Règles strictes:**
- Pas d'inférence logique
- Pas de correction automatique
- Comparaison visuelle stricte
- Marquage "unknown" si illisible

### uml_core.preprocess_image

**Pipeline OpenCV (11 étapes):**

1. **Redimensionnement** - Max 1536px (LANCZOS4)
2. **Grayscale** - Conversion niveaux de gris
3. **Denoising** - fastNlMeansDenoising (h=10)
4. **Sharpening** - Kernel 3x3 pour netteté
5. **CLAHE** - Amélioration contraste adaptatif
6. **Binarisation** - Adaptative Gaussian (blockSize=11)
7. **Morphologie** - Nettoyage artefacts (2x2)
8. **Crop** - Recadrage intelligent avec marges
9. **Upscale** - Si <800px, agrandissement
10. **Inversion** - Si fond sombre détecté
11. **Export** - PNG compression 0 (maximale)

### webapp.app

**Endpoints FastAPI:**

- `GET /` - Interface utilisateur HTML (responsive)
- `POST /compare` - Analyse et comparaison (avec rate limiting)

**Sécurité et validation:**
- **Rate limiting** : 10 requêtes/minute par IP (slowapi)
- **Validation uploads** : Max 10MB, types MIME stricts (image/png, image/jpeg, application/json)
- **Gestion erreurs** : HTTPException avec codes appropriés (400, 429, 500)

**Workflow /compare:**
1. Vérification rate limit (IP-based)
2. Réception fichiers (multipart/form-data)
3. Validation taille et type
4. Sauvegarde temporaire dans uploads/
5. Lecture JSON référence
6. Appel vision_llm_client
7. Logging (logger.info/error)
8. Nettoyage fichiers temporaires
9. Retour JSONResponse avec diff + grading

## Format des données

### JSON de référence

```json
{
  "classes": [
    {
      "name": "ClassName",
      "attributes": [
        {"name": "attr1", "type": "String"}
      ],
      "operations": [
        {
          "name": "method1",
          "parameters": [{"name": "param1", "type": "int"}],
          "return_type": "void"
        }
      ]
    }
  ],
  "relationships": [
    {
      "source": "ClassA",
      "target": "ClassB",
      "type": "association",
      "source_multiplicity": "1",
      "target_multiplicity": "0..*"
    }
  ]
}
```

### JSON de différences (output)

```json
{
  "diff": {
    "missing_classes": ["ClassX"],
    "extra_classes": ["ClassY"],
    "missing_attributes": [
      {"class": "Person", "attribute": "age: int"}
    ],
    "extra_attributes": [],
    "missing_operations": [
      {"class": "Person", "operation": "getName()"}
    ],
    "extra_operations": [],
    "missing_relationships": [
      {
        "source": "Student",
        "target": "Person",
        "type": "inheritance"
      }
    ],
    "extra_relationships": [],
    "incorrect_multiplicities": [
      {
        "relation": "Student -> Course",
        "expected": "1..*",
        "found": "0..*"
      }
    ],
    "naming_issues": [
      {
        "type": "class",
        "found": "person",
        "expected": "Person",
        "issue": "Casse incorrecte"
      }
    ]
  },
  "grading": {
    "score": 15.5,
    "max_score": 20.0,
    "percentage": 77.5,
    "grade": "B",
    "points_lost": 4.5,
    "feedback": "Bon travail, quelques éléments manquants",
    "error_breakdown": {
      "missing_class": 2.0,
      "missing_attribute": 0.5,
      "missing_operation": 0.5,
      "naming_issue": 0.2
    },
    "total_errors": 5
  }
}
```

## Variables d'environnement

### .env

```env
# OpenAI API Configuration
OPENAI_API_KEY=sk-proj-your-api-key-here
OPENAI_API_BASE=https://api.openai.com/v1

# Logging Configuration
DEBUG=false  # Activez 'true' pour logs détaillés
```

## Dépendances principales

```
fastapi>=0.104.0          # Framework web async
uvicorn>=0.24.0           # Serveur ASGI
jinja2>=3.1.0             # Templates HTML
python-multipart>=0.0.6   # Upload de fichiers
opencv-python>=4.8.0      # Traitement d'image
numpy>=1.24.0             # Calculs numériques
requests>=2.31.0          # HTTP client
python-dotenv>=1.0.0      # Variables d'environnement
openai==1.54.0            # Client OpenAI GPT-4o Vision (mise à jour 2025)
slowapi==0.1.9            # Rate limiting (nouveau)
pytest==8.0.0             # Tests automatisés (nouveau)
pytest-cov>=4.1.0         # Coverage des tests (nouveau)
```

**Nouvelles dépendances (2025):**
- `slowapi` : Rate limiting basé sur IP
- `pytest` : Framework de tests unitaires
- `pytest-cov` : Mesure de couverture de code

## Commandes de développement

### Lancer l'application web
```bash
# Méthode 1 : Script simplifié
python run_server.py

# Méthode 2 : Uvicorn direct
cd src
uvicorn webapp.app:app --reload --host 0.0.0.0 --port 8000
```

### Utiliser le CLI
```bash
python scripts/compare.py --student examples/student.png --reference examples/solution.json
```

### Lancer les tests automatisés
```bash
# Tous les tests (19 tests)
pytest tests/test_complete.py -v

# Tests avec coverage
pytest tests/test_complete.py --cov=src/uml_core -v

# Test spécifique
pytest tests/test_complete.py::TestModels::test_uml_class_creation -v
```

### Consulter les logs
```bash
# Logs du jour
cat logs/uml_grader_*.log

# Activer mode DEBUG
# Dans .env: DEBUG=true
```

### Installer les dépendances
```bash
pip install -r requirements.txt
```

## Tests automatisés

### Suite de tests (test_complete.py)

**19 tests couvrant:**
- **TestModels (8 tests)** : UMLClass, UMLAttribute, UMLOperation, UMLRelationship, UMLDiagram
- **TestGrader (7 tests)** : Système de notation, calcul de notes, mentions, feedback
- **TestSerializer (2 tests)** : Sérialisation/désérialisation JSON
- **TestIntegration (1 test)** : Workflow complet diff → grading
- **TestAPI (1 test)** : Endpoint FastAPI root

**Exécution:**
```bash
pytest tests/test_complete.py -v
# Résultat attendu: 19 passed
```

**CI/CD GitHub Actions:**
- Pipeline automatique sur push/PR
- Jobs: test, lint (flake8, black, isort), security (safety, bandit)
- Configuration: `.github/workflows/ci.yml`

## Système de sécurité

### Rate limiting
- **Limite** : 10 requêtes par minute par IP
- **Bibliothèque** : slowapi
- **Gestion** : Exception handler pour erreurs 429

### Validation uploads
- **Taille max** : 10MB par fichier
- **Types MIME** : image/png, image/jpeg, application/json
- **Vérification** : Lecture contenu avant traitement
- **Erreurs** : HTTPException(400) avec messages explicites

### Logging
- **Console** : Niveau INFO (événements importants)
- **Fichiers** : Niveau DEBUG (détails complets)
- **Rotation** : Quotidienne automatique
- **Format** : `[YYYY-MM-DD HH:MM:SS] [LEVEL] [module.function] Message`

## Extension future

### Fonctionnalités à ajouter

1. **Export PDF** - Génération de rapports PDF
2. **Historique** - Base de données des analyses
3. **Multi-langues** - Support i18n
4. **Batch processing** - Analyse de plusieurs diagrammes
5. **API REST publique** - Endpoint pour intégration externe
6. **Cache résultats** - Hash image → JSON pour éviter re-traitement
7. **Monitoring** - Sentry/DataDog pour production
8. **Tests E2E** - Playwright/Selenium pour interface web

---

**Version** : 1.0  
**Dernière mise à jour** : Décembre 2025  
**Note qualité** : 9.7/10 (voir OPTIMISATIONS.md)

**Version:** 1.0  
**Dernière mise à jour:** 2025-12-06
