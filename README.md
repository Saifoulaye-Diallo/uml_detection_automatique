# 🎓 UML Vision Grader Pro

Système de correction automatique de diagrammes UML de classes utilisant GPT-4o Vision et OpenCV.

## 🌟 Fonctionnalités

- **Analyse IA avancée** : Utilise GPT-4o Vision pour extraire et comparer les diagrammes UML
- **Prétraitement d'image optimisé** : Pipeline OpenCV en 11 étapes pour une reconnaissance maximale
- **Interface web moderne** : Application FastAPI avec design gradient et animations fluides
- **Comparaison rigoureuse** : Système de normalisation et détection de différences ultra-précis
- **Rapport détaillé** : Statistiques visuelles et export JSON des différences

## 📋 Prérequis

- Python 3.8+
- OpenAI API Key (GPT-4o Vision)
- Windows/Linux/macOS

## 🚀 Installation

### 1. Cloner le projet
```bash
git clone <repository-url>
cd "Code UML"
```

### 2. Créer l'environnement virtuel
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # Windows PowerShell
# ou
source .venv/bin/activate  # Linux/macOS
```

### 3. Installer les dépendances
```powershell
pip install -r requirements.txt
```

### 4. Configuration
Créez un fichier `.env` à la racine :
```env
OPENAI_API_KEY=sk-proj-votre-clé-api-ici
OPENAI_API_BASE=https://api.openai.com/v1
```

## 🎯 Utilisation

### Interface Web (Recommandé)

1. **Lancer le serveur** :
```powershell
cd src
uvicorn webapp.app:app --reload --host 0.0.0.0 --port 8000
```

2. **Ouvrir le navigateur** :
```
http://localhost:8000
```

3. **Téléverser les fichiers** :
   - Diagramme UML de l'étudiant (PNG/JPG)
   - Solution de référence (JSON)

4. **Analyser** et consulter le rapport détaillé

### Ligne de commande

```powershell
python scripts/compare.py --student examples/student.png --reference examples/solution.json
```

Le fichier `diff.json` sera généré à la racine avec les différences.

## 📂 Structure du projet

```
Code UML/
├── src/                         # Code source principal
│   ├── uml_core/                # Moteur de base UML
│   │   ├── models.py            # Modèles de données UML
│   │   ├── vision_llm_client.py # Client GPT-4o Vision
│   │   ├── preprocess_image.py  # Pipeline OpenCV (11 étapes)
│   │   ├── serializer.py        # Sérialisation/désérialisation JSON
│   │   ├── comparator.py        # Comparaison avec fuzzy matching
│   │   └── env.py               # Gestion des variables d'environnement
│   │
│   └── webapp/                  # Application web
│       ├── app.py               # Backend FastAPI avec endpoints async
│       ├── templates/           # Templates Jinja2
│       │   └── index.html       # Interface utilisateur moderne
│       ├── static/              # Assets statiques (CSS, JS, images)
│       └── uploads/             # Dossier temporaire pour fichiers uploadés
│
├── scripts/                     # Scripts utilitaires
│   └── compare.py               # CLI pour comparaison image + JSON
│
├── tests/                       # Tests unitaires
│   ├── __init__.py
│   └── test_models.py           # Tests des modèles UML
│
├── examples/                    # Fichiers d'exemple
│   ├── student.png              # Diagramme d'exemple
│   └── solution.json            # Référence d'exemple
│
├── docs/                        # Documentation détaillée
│   ├── ARCHITECTURE.md          # Architecture technique
│   └── INSTALLATION.md          # Guide d'installation
│
├── .env                         # Variables d'environnement (gitignored)
├── .env.example                 # Template de configuration
├── .gitignore                   # Fichiers ignorés par Git
├── requirements.txt             # Dépendances Python
└── README.md                    # Documentation principale (ce fichier)
```

## 🧠 Architecture technique

### 1. Prétraitement d'image (OpenCV)
```python
# Pipeline en 11 étapes pour optimiser la reconnaissance
1. Redimensionnement intelligent (max 1536px)
2. Conversion en niveaux de gris
3. Denoising agressif (fastNlMeansDenoising)
4. Sharpening (kernel 3x3)
5. Amélioration du contraste (CLAHE)
6. Binarisation adaptative (Gaussian, blockSize=11)
7. Morphologie (nettoyage artefacts)
8. Recadrage intelligent (marges préservées)
9. Upscaling si trop petite (<800px)
10. Inversion si nécessaire (fond sombre)
11. Export PNG compression maximale (0)
```

### 2. Extraction et comparaison (GPT-4o Vision)
```python
# Prompt en 4 phases rigoureuses
PHASE 1 → Extraction brute depuis l'image
PHASE 2 → Normalisation des éléments
PHASE 3 → Comparaison avec le JSON de référence
PHASE 4 → Génération du diff JSON final
```

### 3. Modèles UML
- **UMLClass** : Nom, attributs, opérations
- **UMLAttribute** : Nom, type
- **UMLOperation** : Nom, paramètres, type de retour
- **UMLRelationship** : Source, cible, type, multiplicités

### 4. Différences détectées
```json
{
  "missing_classes": ["Classe absente"],
  "extra_classes": ["Classe en trop"],
  "missing_attributes": [{"class": "X", "attribute": "attr"}],
  "extra_attributes": [...],
  "missing_operations": [...],
  "extra_operations": [...],
  "missing_relationships": [...],
  "extra_relationships": [...],
  "incorrect_multiplicities": [{"relation": "...", "expected": "1..*", "found": "0..*"}],
  "naming_issues": [{"type": "class", "found": "person", "expected": "Person"}]
}
```

## 🎨 Interface Web

### Caractéristiques UI
- **Design moderne** : Gradient animé bleu/violet/rose avec glassmorphism
- **Animations fluides** : Float, pulse, gradient, bounce
- **Feedback visuel** : Loading spinner, prévisualisations de fichiers, toasts
- **Statistiques visuelles** : 9 cartes colorées avec icônes SVG uniques
- **Terminal de code** : Affichage JSON avec scrollbar personnalisée
- **Responsive** : Compatible mobile/tablette/desktop
- **Score adaptatif** : Couleurs vert/jaune/orange/rouge selon les erreurs

### Technologies
- **Frontend** : Tailwind CSS 3.x, Vanilla JavaScript (async/await)
- **Backend** : FastAPI (Python 3.12), Jinja2 Templates
- **APIs** : OpenAI GPT-4o Vision, OpenCV 4.x

## 🔧 Configuration avancée

### Formats de multiplicité supportés
```
"1", "0..*", "1..*", "0..1", "*", "n", "" (vide)
```

### Types de relations UML
```
- association
- aggregation (◇)
- composition (◆)
- inheritance (extends/généralisation)
- realization (implements/réalisation)
- dependency (dépendance)
```

### Paramètres de prétraitement
```python
# Dans preprocess_image.py
MAX_DIM = 1536          # Résolution maximale
DENOISE_H = 10          # Force du denoising
CLAHE_CLIP_LIMIT = 2.0  # Limite de contraste
ADAPTIVE_BLOCK_SIZE = 11 # Taille de bloc binarisation
```

## 📊 Exemples

### Format JSON de référence
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

### Erreur 400 API
- Vérifier la clé API dans `.env`
- Confirmer le modèle : `gpt-4o` (pas `gpt-5`)

### Image non reconnue
- Vérifier le format : PNG/JPG supportés
- Améliorer la qualité : scanner haute résolution (300 DPI minimum)
- Contraste : fond blanc, traits noirs épais

### Installation OpenCV échouée
```powershell
pip install opencv-python-headless
```

## 📝 Licence

MIT License - Libre d'utilisation pour l'enseignement et la recherche.

## 🤝 Contribution

Les contributions sont bienvenues ! Créez une issue ou un pull request.

## 📞 Support

Pour toute question technique : ouvrir une issue sur GitHub.

---

**UML Vision Grader Pro v2.0** • Propulsé par GPT-4o Vision, OpenCV & FastAPI • 2025

FIN