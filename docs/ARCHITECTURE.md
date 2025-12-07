# 📝 Documentation UML Vision Grader Pro

## Architecture du projet

### Structure des dossiers

```
Code UML/
├── src/                         # Code source principal
│   ├── uml_core/                # Moteur de base UML
│   │   ├── models.py            # Modèles de données UML
│   │   ├── vision_llm_client.py # Client GPT-4o Vision
│   │   ├── preprocess_image.py  # Pipeline OpenCV
│   │   ├── serializer.py        # Sérialisation JSON
│   │   ├── comparator.py        # Comparaison (legacy)
│   │   └── env.py               # Configuration
│   │
│   └── webapp/                  # Application web
│       ├── app.py               # Backend FastAPI
│       ├── templates/           # Templates Jinja2
│       │   └── index.html       # Interface utilisateur
│       ├── static/              # Assets statiques
│       └── uploads/             # Fichiers temporaires
│
├── scripts/                     # Scripts utilitaires
│   └── compare.py               # CLI de comparaison
│
├── tests/                       # Tests unitaires
│   └── (à venir)
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
    FastAPI endpoint /compare
            ↓
    Sauvegarde temporaire
            ↓
    extract_uml_json_from_image()
            ↓
    Réponse JSON avec diff
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

- `GET /` - Interface utilisateur HTML
- `POST /compare` - Analyse et comparaison

**Workflow /compare:**
1. Réception fichiers (multipart/form-data)
2. Sauvegarde temporaire dans uploads/
3. Lecture JSON référence
4. Appel vision_llm_client
5. Nettoyage fichiers temporaires
6. Retour JSONResponse

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
}
```

## Variables d'environnement

### .env

```env
# OpenAI API Configuration
OPENAI_API_KEY=sk-proj-your-api-key-here
OPENAI_API_BASE=https://api.openai.com/v1
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
```

## Commandes de développement

### Lancer l'application web
```bash
cd src
uvicorn webapp.app:app --reload --host 0.0.0.0 --port 8000
```

### Utiliser le CLI
```bash
python scripts/compare.py --student examples/student.png --reference examples/solution.json
```

### Installer les dépendances
```bash
pip install -r requirements.txt
```

## Extension future

### Tests à implémenter

```
tests/
├── test_models.py         # Tests des modèles UML
├── test_preprocess.py     # Tests du pipeline OpenCV
├── test_client.py         # Tests du client Vision
└── test_api.py            # Tests de l'API FastAPI
```

### Fonctionnalités à ajouter

1. **Export PDF** - Génération de rapports PDF
2. **Historique** - Base de données des analyses
3. **Multi-langues** - Support i18n
4. **Batch processing** - Analyse de plusieurs diagrammes
5. **API REST publique** - Endpoint pour intégration externe

---

**Version:** 2.0  
**Dernière mise à jour:** 2025-12-06
