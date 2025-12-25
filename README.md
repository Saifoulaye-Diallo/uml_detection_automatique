# UML Vision Grader Pro

Système de correction automatique de diagrammes UML de classes utilisant GPT-4o Vision et OpenCV.

## Fonctionnalités

- **Analyse IA avancée** : Utilise GPT-4o Vision pour extraire et comparer les diagrammes UML
- **Prétraitement d'image optimisé** : Pipeline OpenCV en 11 étapes pour une reconnaissance maximale
- **Interface web moderne** : Application FastAPI avec design gradient et animations fluides
- **Comparaison rigoureuse** : Système de normalisation et détection de différences ultra-précis
- **Rapport détaillé** : Statistiques visuelles et export JSON des différences

## Prérequis

- Python 3.8+
- OpenAI API Key (GPT-4o Vision)
- Windows/Linux/macOS

## Installation

### 1. Cloner le projet
```bash
git clone https://github.com/Saifoulaye-Diallo/uml_detection_automatique.git
cd uml_detection_automatique
```

### 2. Créer l'environnement virtuel
```powershell
# Windows PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Linux/macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Installer les dépendances
```powershell
pip install -r requirements.txt
```

### 4. Configuration de l'API OpenAI
Créez un fichier `.env` à la racine du projet :
```env
OPENAI_API_KEY=sk-proj-votre-clé-api-ici
OPENAI_API_BASE=https://api.openai.com/v1
```

**Important** : Obtenez votre clé API sur [platform.openai.com](https://platform.openai.com/api-keys)

## 🎯 Utilisation

### Interface Web (Recommandé)

1. **Lancer le serveur** :
```powershell
python run_server.py
```

2. **Ouvrir l'interface** :
   - Le serveur démarre sur `http://localhost:8000`
   - L'interface s'ouvrira automatiquement dans votre navigateur

3. **Utiliser l'application** :
   - **Téléverser** le diagramme UML de l'étudiant (PNG/JPG)
   - **Téléverser** la solution de référence (JSON)
   - **Configurer** les pénalités de notation (optionnel)
   - **Lancer** l'analyse
   - **Consulter** le rapport détaillé avec note, statistiques et différences

### Interface Desktop
L'application utilise un layout desktop professionnel avec :
- **Panneau latéral gauche** : Upload des fichiers et configuration de notation
- **Zone principale** : Affichage des résultats, score et rapport JSON

### Ligne de commande

```powershell
python scripts/compare.py --student examples/student.png --reference examples/solution.json
```

Le fichier `diff.json` sera généré à la racine avec les différences.

## Structure du projet

```
uml_detection_automatique/
├── src/                         # Code source principal
│   ├── uml_core/                # Moteur de traitement UML
│   │   ├── models.py            # Modèles de données (UMLClass, UMLRelationship)
│   │   ├── vision_llm_client.py # Client GPT-4o Vision avec retry SSL
│   │   ├── preprocess_image.py  # Pipeline OpenCV (11 étapes)
│   │   ├── grader.py            # Système de notation académique
│   │   ├── serializer.py        # Sérialisation/désérialisation JSON
│   │   ├── comparator.py        # Comparaison avec fuzzy matching
│   │   └── env.py               # Variables d'environnement
│   │
│   └── webapp/                  # Application web FastAPI
│       ├── app.py               # API REST avec endpoint /compare
│       ├── templates/           # Templates Jinja2
│       │   └── index.html       # Interface desktop avec sidebar
│       ├── static/              # Assets statiques
│       └── uploads/             # Fichiers temporaires (gitignored)
│
├── scripts/                     # Scripts CLI
│   ├── compare.py               # Comparaison en ligne de commande
│   └── test_openai.py           # Diagnostic API OpenAI
│
├── tests/                       # Tests unitaires
│   └── test_models.py           # Tests des modèles UML
│
├── examples/                    # Exemples d'utilisation
│   ├── student.png              # Diagramme étudiant exemple
│   └── solution.json            # Solution de référence
│
├── docs/                        # Documentation technique
│   ├── ARCHITECTURE.md          # Architecture complète
│   ├── INSTALLATION.md          # Guide d'installation détaillé
│   ├── TROUBLESHOOTING.md       # Résolution de problèmes
│   └── PROMPT_OPTIMIZED.md      # Prompt engineering optimisé
│
├── run_server.py                # Script de démarrage serveur
├── requirements.txt             # Dépendances Python
├── .env.example                 # Template configuration
├── .gitignore                   # Fichiers exclus de Git
└── README.md                    # Ce fichier
```

## Architecture technique

### 1. Système de notation académique
```python
# Système de grading avec pénalités configurables
- Note sur 20 avec conversion en lettre (A+ à F)
- Pénalités personnalisables par type d'erreur
- Feedback détaillé pour l'étudiant
- Export JSON du rapport de notation
```

### 2. Prétraitement d'image (OpenCV)
```python
# Pipeline optimisé en 11 étapes
1. Redimensionnement intelligent (max 1536px)
2. Conversion niveaux de gris
3. Denoising (fastNlMeansDenoising h=10)
4. Sharpening (kernel 3x3)
5. CLAHE (amélioration contraste)
6. Binarisation adaptative (Gaussian)
7. Morphologie (nettoyage artefacts)
8. Recadrage intelligent
9. Upscaling si nécessaire
10. Inversion automatique (fond sombre)
11. Export PNG optimisé
```

### 3. Extraction IA (GPT-4o Vision)
```python
# Prompt optimisé en 4 phases
PHASE 1 → Extraction depuis l'image
PHASE 2 → Normalisation (camelCase, visibilités)
PHASE 3 → Comparaison avec JSON référence
PHASE 4 → Génération rapport différences
```

### 4. Comparaison et grading
```python
# Détection de 10 types d'erreurs
- Classes manquantes/en trop
- Attributs manquants/en trop  
- Opérations manquantes/en trop
- Relations manquantes/en trop
- Multiplicités incorrectes
- Problèmes de nommage
```
### Structure du rapport de notation
```json
{
  "diff": {
    "missing_classes": ["Classe1"],
    "extra_classes": [],
    "missing_attributes": [{"class": "Person", "attribute": "email: String"}],
    ...
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
      ...
    },
    "total_errors": 5
  }
}
```

## Interface Web

### Fonctionnalités
- **Layout desktop** : Sidebar fixe + zone de résultats
- **Configuration notation** : 10 pénalités personnalisables
- **Affichage score** : Note/20, lettre (A+ à F), pourcentage
- **Statistiques** : 9 cartes colorées avec détails des erreurs
- **Export** : Copie et téléchargement du rapport JSON
- **États** : Welcome, Loading, Error, Results

### Technologies
- **Frontend** : Tailwind CSS 3.x, JavaScript async/await
- **Backend** : FastAPI + Jinja2
- **API** : OpenAI GPT-4o Vision (timeout 120s, retry SSL)

## Configuration

### Pénalités de notation (par défaut)
```python
missing_class = 2.0          # Classe manquante
extra_class = 1.5            # Classe en trop
missing_attribute = 0.5      # Attribut manquant
extra_attribute = 0.3        # Attribut en trop
missing_operation = 0.5      # Opération manquante
extra_operation = 0.3        # Opération en trop
missing_relationship = 1.5   # Relation manquante
extra_relationship = 1.0     # Relation en trop
incorrect_multiplicity = 0.5 # Multiplicité incorrecte
naming_issue = 0.2           # Problème de nommage
```

### Types de relations supportés
- `association` : Association simple
- `aggregation` : Agrégation (◇)
- `composition` : Composition (◆)
- `inheritance` : Héritage/Généralisation
- `realization` : Réalisation/Implémentation
- `dependency` : Dépendance

## Format JSON

### Structure du diagramme de référence
```json
{
  "classes": [
    {
      "name": "Person",
      "attributes": [
        {"name": "name", "type": "String"},
        {"name": "age", "type": "int"}
      ],
      "operations": [
        {
          "name": "getName",
          "parameters": [],
          "return_type": "String"
        }
      ]
    }
  ],
  "relationships": [
    {
      "source": "Student",
      "target": "Person",
      "type": "inheritance",
      "source_multiplicity": "",
      "target_multiplicity": ""
    }
  ]
}
```

## 🐛 Dépannage

### Erreur 401 API OpenAI
```bash
# Vérifier la clé API dans .env
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
```

### Erreur SSL UNEXPECTED_EOF_WHILE_READING
- Le système utilise un retry automatique avec `verify=False` en fallback
- Consultez `docs/TROUBLESHOOTING.md` pour plus de détails

### Image non reconnue
- **Format** : PNG ou JPG uniquement
- **Qualité** : 300 DPI minimum recommandé
- **Contraste** : Fond blanc, traits noirs épais
- **Taille** : Éviter les images trop petites (<800px)

### Installation OpenCV échouée
```powershell
# Alternative headless (sans interface graphique)
pip install opencv-python-headless
```

## Documentation complète

Pour plus de détails, consultez :
- **docs/ARCHITECTURE.md** : Architecture technique détaillée
- **docs/INSTALLATION.md** : Guide d'installation pas à pas
- **docs/TROUBLESHOOTING.md** : Résolution de problèmes courants
- **docs/PROMPT_OPTIMIZED.md** : Détails du prompt GPT-4o Vision

## Licence

Projet académique - Utilisation libre pour l'enseignement et la recherche.

## Auteur

**Saifoulaye Diallo**
- GitHub: [@Saifoulaye-Diallo](https://github.com/Saifoulaye-Diallo)
- Repository: [uml_detection_automatique](https://github.com/Saifoulaye-Diallo/uml_detection_automatique)

---

**UML Vision Grader Pro v2.0** • GPT-4o Vision × OpenCV × FastAPI • Décembre 2025