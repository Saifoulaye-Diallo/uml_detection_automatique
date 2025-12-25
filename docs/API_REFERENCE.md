# API Reference - Documentation Complète des Fonctions

**UML Vision Grader Pro - Documentation Technique Détaillée**  
Version: 2.0  
Date: 2025-12-18

---

## Table des matières

1. [Module: uml_core.models](#module-uml_coremodels)
2. [Module: uml_core.vision_llm_client](#module-uml_corevision_llm_client)
3. [Module: uml_core.preprocess_image](#module-uml_corepreprocess_image)
4. [Module: uml_core.grader](#module-uml_coregrader)
5. [Module: uml_core.comparator](#module-uml_corecomparator)
6. [Module: uml_core.serializer](#module-uml_coreserializer)
7. [Module: uml_core.env](#module-uml_coreenv)
8. [Module: webapp.app](#module-webappapp)
9. [Script: compare.py](#script-comparepy)

---

## Module: uml_core.models

**Fichier:** `src/uml_core/models.py`  
**Rôle:** Définition des structures de données UML (classes, attributs, opérations, relations)

### Classe: `UMLAttribute`

**Description:** Représente un attribut d'une classe UML (nom + type).

#### Attributs:
- `name` (str): Nom de l'attribut (ex: "age", "studentId")
- `type` (str): Type de l'attribut (ex: "int", "String", "Date")

#### Méthodes:

##### `to_dict() -> dict`
Convertit l'attribut en dictionnaire JSON.

**Returns:**
```python
{"name": "age", "type": "int"}
```

**Exemple:**
```python
attr = UMLAttribute(name='age', type='int')
result = attr.to_dict()
# result = {"name": "age", "type": "int"}
```

##### `from_dict(data: dict) -> UMLAttribute` (static)
Crée un UMLAttribute depuis un dictionnaire.

**Paramètres:**
- `data` (dict): Dictionnaire avec clés "name" et "type"

**Returns:** Instance de UMLAttribute

**Exemple:**
```python
attr = UMLAttribute.from_dict({"name": "email", "type": "String"})
# attr.name = "email", attr.type = "String"
```

---

### Classe: `UMLOperation`

**Description:** Représente une méthode/opération d'une classe UML.

#### Attributs:
- `name` (str): Nom de l'opération (ex: "calculate", "getName")
- `parameters` (List[Dict[str, str]]): Liste des paramètres avec name et type
- `return_type` (Optional[str]): Type de retour (ex: "void", "String")

#### Méthodes:

##### `to_dict() -> dict`
Convertit l'opération en dictionnaire JSON.

**Returns:**
```python
{
    "name": "setAge",
    "parameters": [{"name": "age", "type": "int"}],
    "return_type": "void"
}
```

**Exemple:**
```python
op = UMLOperation(
    name='setAge',
    parameters=[{'name': 'age', 'type': 'int'}],
    return_type='void'
)
result = op.to_dict()
```

##### `from_dict(data: dict) -> UMLOperation` (static)
Crée une UMLOperation depuis un dictionnaire.

**Paramètres:**
- `data` (dict): Contient "name", "parameters" (optionnel), "return_type" (optionnel)

**Returns:** Instance de UMLOperation

**Exemple:**
```python
op = UMLOperation.from_dict({
    "name": "getName",
    "parameters": [],
    "return_type": "String"
})
```

---

### Classe: `UMLClass`

**Description:** Représente une classe UML complète avec attributs et opérations.

#### Attributs:
- `name` (str): Nom de la classe (ex: "Person", "Student")
- `attributes` (List[UMLAttribute]): Liste des attributs
- `operations` (List[UMLOperation]): Liste des méthodes

#### Méthodes:

##### `to_dict() -> dict`
Convertit la classe en dictionnaire JSON.

**Returns:**
```python
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
```

**Exemple:**
```python
cls = UMLClass(
    name='Person',
    attributes=[UMLAttribute('name', 'String')],
    operations=[UMLOperation('getName', [], 'String')]
)
result = cls.to_dict()
```

##### `from_dict(data: dict) -> UMLClass` (static)
Crée une UMLClass depuis un dictionnaire.

**Parsing intelligent:**
- Attributs: Supporte format string "name: type" ou dict
- Opérations: Supporte format string "name(params): return" ou dict

**Paramètres:**
- `data` (dict): Contient "name", "attributes" (liste), "operations" (liste)

**Returns:** Instance de UMLClass

**Exemple:**
```python
cls = UMLClass.from_dict({
    "name": "Student",
    "attributes": [
        {"name": "id", "type": "int"},
        "name: String"  # Format string aussi supporté
    ],
    "operations": []
})
```

---

### Classe: `UMLRelationship`

**Description:** Représente une relation entre deux classes UML.

#### Attributs:
- `type` (str): Type de relation ("association", "composition", "inheritance", "aggregation", "dependency")
- `from_class` (str): Nom de la classe source
- `to_class` (str): Nom de la classe cible
- `multiplicity_from` (Optional[str]): Multiplicité côté source (ex: "1", "0..*")
- `multiplicity_to` (Optional[str]): Multiplicité côté cible

#### Méthodes:

##### `to_dict() -> dict`
Convertit la relation en dictionnaire JSON.

**Returns:**
```python
{
    "type": "association",
    "from": "Student",
    "to": "Course",
    "multiplicity_from": "1",
    "multiplicity_to": "0..*"
}
```

##### `from_dict(data: dict) -> UMLRelationship` (static)
Crée une UMLRelationship depuis un dictionnaire.

**Auto-correction:** Supporte "from"/"to" ET "source"/"target" comme noms de clés.

**Paramètres:**
- `data` (dict): Contient type, from/source, to/target, multiplicités (optionnel)

**Returns:** Instance de UMLRelationship

---

### Classe: `UMLDiagram`

**Description:** Représente un diagramme UML complet (ensemble de classes + relations).

#### Attributs:
- `classes` (List[UMLClass]): Liste des classes du diagramme
- `relationships` (List[UMLRelationship]): Liste des relations

#### Méthodes:

##### `to_dict() -> dict`
Convertit le diagramme en dictionnaire JSON.

**Returns:**
```python
{
    "classes": [...],
    "relationships": [...]
}
```

##### `from_dict(data: dict) -> UMLDiagram` (static)
Crée un UMLDiagram depuis un dictionnaire JSON.

**Paramètres:**
- `data` (dict): Contient "classes" (liste) et "relationships" (liste)

**Returns:** Instance de UMLDiagram

---

## Module: uml_core.vision_llm_client

**Fichier:** `src/uml_core/vision_llm_client.py`  
**Rôle:** Communication avec GPT-4o Vision pour extraction et comparaison UML

### Fonction: `encode_image_base64(image_path: str) -> str`

**Description:** Encode une image en base64 pour l'API OpenAI.

**Paramètres:**
- `image_path` (str): Chemin vers le fichier image (PNG/JPG)

**Returns:** String base64 de l'image

**Exemple:**
```python
b64 = encode_image_base64("student.png")
# b64 = "iVBORw0KGgoAAAANSUhEUg..."
```

---

### Fonction: `extract_uml_json_from_image(image_path: str, reference_json: str = None) -> dict`

**Description:** Fonction principale d'extraction et comparaison UML.

**Workflow:**
1. Prétraitement de l'image via OpenCV (11 étapes)
2. Encodage base64
3. Envoi à GPT-4o Vision avec prompt en 4 phases
4. Récupération du JSON de différences

**Paramètres:**
- `image_path` (str): Chemin vers l'image UML à analyser
- `reference_json` (str, optionnel): JSON de référence (solution correcte)

**Returns:** Dictionnaire de différences avec 10 catégories:
```python
{
    "missing_classes": ["ClassName1", ...],
    "extra_classes": ["ClassName2", ...],
    "missing_attributes": [
        {"class": "Person", "attribute": "age: int"},
        ...
    ],
    "extra_attributes": [...],
    "missing_operations": [
        {"class": "Person", "operation": "getName()"},
        ...
    ],
    "extra_operations": [...],
    "missing_relationships": [
        {
            "type": "association",
            "from": "Student",
            "to": "Person",
            "multiplicity_from": "1",
            "multiplicity_to": "0..*"
        },
        ...
    ],
    "extra_relationships": [...],
    "incorrect_multiplicities": [
        {
            "relationship": ["association", "Student", "Course"],
            "expected": ["1", "0..*"],
            "actual": ["0..1", "*"]
        },
        ...
    ],
    "naming_issues": [
        {
            "type": "class",
            "found": "person",
            "expected": "Person",
            "issue": "Casse incorrecte"
        },
        ...
    ]
}
```

**Exceptions:**
- `requests.exceptions.SSLError`: Erreur SSL (réessai sans vérification)
- `requests.exceptions.HTTPError`: Erreur API (400, 401, 500, etc.)
- `json.JSONDecodeError`: Réponse invalide du LLM

**Exemple:**
```python
# Sans référence (extraction seule)
extracted = extract_uml_json_from_image("student.png")

# Avec référence (extraction + comparaison)
with open("solution.json") as f:
    ref_json = f.read()
diff = extract_uml_json_from_image("student.png", reference_json=ref_json)
```

**Configuration:**
- Modèle: GPT-4o
- Max tokens: 2048
- Timeout: 120 secondes
- Retry: 3 tentatives avec backoff exponentiel

**Prompt en 4 phases:**
1. **PHASE 1** - Extraction UML depuis l'image (classes, attributs, opérations, relations)
2. **PHASE 2** - Normalisation (espaces, casse, multiplicités)
3. **PHASE 3** - Comparaison stricte avec référence (field-by-field)
4. **PHASE 4** - Génération JSON final (10 catégories)

**Règles strictes:**
- Pas d'inférence logique
- Pas de correction automatique
- Comparaison visuelle stricte
- Marquage "unknown" si illisible

---

## Module: uml_core.preprocess_image

**Fichier:** `src/uml_core/preprocess_image.py`  
**Rôle:** Pipeline OpenCV pour optimiser les images UML avant reconnaissance

### Fonction: `preprocess_image(input_path: str, output_path: str) -> None`

**Description:** Prétraite une image UML en 11 étapes pour maximiser la reconnaissance.

**Pipeline complet:**

1. **Redimensionnement intelligent** (max 1536px)
   - Algorithme: LANCZOS4 (haute qualité)
   - Conserve ratio d'aspect
   - Pas d'upscale si déjà <1536px

2. **Conversion niveaux de gris**
   - Réduit le bruit couleur
   - Facilite traitement OpenCV

3. **Denoising agressif**
   - Algorithme: fastNlMeansDenoising
   - h=10, templateWindowSize=7, searchWindowSize=21
   - Élimine bruit de scan/photo

4. **Sharpening**
   - Kernel 3x3 (-1 partout, 9 au centre)
   - Améliore netteté texte et traits

5. **CLAHE (Contrast Limited Adaptive Histogram Equalization)**
   - clipLimit=2.0, tileGridSize=8x8
   - Améliore contraste localement

6. **Binarisation adaptative**
   - Type: ADAPTIVE_THRESH_GAUSSIAN_C
   - blockSize=11, C=2
   - Sépare texte/lignes du fond

7. **Morphologie**
   - Opération: MORPH_CLOSE
   - Kernel 2x2 (MORPH_RECT)
   - Nettoie artefacts sans perdre traits

8. **Recadrage automatique**
   - Détection contours non-blancs
   - Marge de 5px préservée
   - Élimine espaces inutiles

9. **Upscaling conditionnel**
   - Si <800px, agrandissement CUBIC
   - Garantit résolution minimale

10. **Détection inversion**
    - Vérifie si fond sombre
    - Inverse si nécessaire (fond blanc optimal)

11. **Export PNG compression 0**
    - Qualité maximale (aucune perte)
    - Format PNG optimisé pour Vision API

**Paramètres:**
- `input_path` (str): Chemin image source (PNG/JPG/JPEG)
- `output_path` (str): Chemin image traitée (PNG)

**Exceptions:**
- `ValueError`: Image source illisible (fichier corrompu/inexistant)

**Exemple:**
```python
preprocess_image("raw_student.jpg", "student_preprocessed.png")
# Crée student_preprocessed.png optimisé en 11 étapes
```

**Performance:**
- Temps moyen: 0.5-2 secondes selon résolution
- Taille sortie: 100-500 KB typiquement

---

## Module: uml_core.grader

**Fichier:** `src/uml_core/grader.py`  
**Rôle:** Calcul de notes académiques basé sur les différences UML

### Classe: `UMLGrader`

**Description:** Calculateur de notes avec pondération par type d'erreur.

#### Constantes de classe:

##### `WEIGHTS` (dict)
Poids des erreurs (points perdus par erreur):

```python
WEIGHTS = {
    "missing_class": 2.0,           # -2 pts par classe manquante
    "extra_class": 1.5,             # -1.5 pts par classe en trop
    "missing_attribute": 0.5,       # -0.5 pts par attribut manquant
    "extra_attribute": 0.3,         # -0.3 pts par attribut en trop
    "missing_operation": 0.5,       # -0.5 pts par opération manquante
    "extra_operation": 0.3,         # -0.3 pts par opération en trop
    "missing_relationship": 1.5,    # -1.5 pts par relation manquante
    "extra_relationship": 1.0,      # -1 pts par relation en trop
    "incorrect_multiplicity": 0.5,  # -0.5 pts par multiplicité incorrecte
    "naming_issue": 0.2,            # -0.2 pts par problème de nommage
}
```

#### Méthodes:

##### `calculate_score(diff: dict, max_score: float = 20.0) -> dict` (static)

**Description:** Calcule la note complète à partir du diff JSON.

**Algorithme:**
1. Parcourt chaque catégorie du diff
2. Compte le nombre d'erreurs × poids
3. Soustrait les points perdus du max_score
4. Calcule pourcentage = (score / max_score) × 100
5. Attribue mention (A+ à F) selon pourcentage
6. Génère feedback textuel personnalisé

**Paramètres:**
- `diff` (dict): Dictionnaire de différences (output de extract_uml_json_from_image)
- `max_score` (float): Note maximale (défaut: 20.0)

**Returns:**
```python
{
    "score": 15.5,                    # Note finale sur 20
    "max_score": 20.0,                # Note maximale
    "percentage": 77.5,               # Pourcentage (score/max * 100)
    "grade": "B+",                    # Mention (A+ à F)
    "points_lost": 4.5,               # Points perdus au total
    "error_breakdown": {              # Détail par catégorie
        "missing_classes": {
            "count": 2,               # Nombre d'erreurs
            "weight": 2.0,            # Poids unitaire
            "points_lost": 4.0        # Total perdu (count × weight)
        },
        "extra_attributes": {
            "count": 1,
            "weight": 0.3,
            "points_lost": 0.3
        },
        ...
    },
    "feedback": "[OK] Très bon travail ! [X] 2 classe(s) manquante(s): ...",
    "total_errors": 5                 # Nombre total d'erreurs toutes catégories
}
```

**Exemple:**
```python
diff = {
    "missing_classes": ["Person", "Address"],
    "extra_classes": [],
    "missing_attributes": [{"class": "Student", "attribute": "age: int"}],
    # ... autres catégories vides
}

result = UMLGrader.calculate_score(diff, max_score=20.0)
# result["score"] = 15.5
# result["grade"] = "B+"
# result["points_lost"] = 4.5 (2*2.0 + 1*0.5)
```

---

##### `_get_grade_letter(percentage: float) -> str` (static)

**Description:** Convertit un pourcentage en mention académique.

**Grille de notation:**
- **A+** : 90-100%
- **A**  : 85-89%
- **A-** : 80-84%
- **B+** : 75-79%
- **B**  : 70-74%
- **B-** : 65-69%
- **C+** : 60-64%
- **C**  : 55-59%
- **C-** : 50-54%
- **D**  : 40-49%
- **F**  : 0-39%

**Paramètres:**
- `percentage` (float): Pourcentage (0-100)

**Returns:** Mention (str)

**Exemple:**
```python
grade = UMLGrader._get_grade_letter(77.5)
# grade = "B+"

grade = UMLGrader._get_grade_letter(92.0)
# grade = "A+"
```

---

##### `_generate_feedback(diff: dict, score: float, max_score: float) -> str` (static)

**Description:** Génère un feedback textuel personnalisé selon les erreurs.

**Format du feedback:**
- **Intro** : Message global selon pourcentage
  - ≥80% : "[OK] Très bon travail !"
  - ≥60% : "Bon travail, quelques améliorations à apporter."
  - ≥40% : "[!] Travail à revoir, plusieurs erreurs importantes."
  - <40% : "[X] Travail insuffisant, révision complète nécessaire."
  
- **Détails** : Liste des 4 erreurs principales
  - [X] Classes manquantes
  - [+] Classes en trop
  - [~] Relations manquantes
  - [#] Multiplicités incorrectes

**Paramètres:**
- `diff` (dict): Dictionnaire de différences
- `score` (float): Note calculée
- `max_score` (float): Note maximale

**Returns:** Feedback textuel (str)

**Exemple:**
```python
feedback = UMLGrader._generate_feedback(diff, 15.5, 20.0)
# feedback = "[OK] Très bon travail ! [X] 2 classe(s) manquante(s): Person, Address"
```

---

### Fonction: `grade_uml_diff(diff: dict, max_score: float = 20.0) -> dict`

**Description:** Fonction helper simplifiée pour noter un diff.

**Paramètres:**
- `diff` (dict): Résultat de extract_uml_json_from_image()
- `max_score` (float): Note maximale

**Returns:** Même format que UMLGrader.calculate_score()

**Exemple:**
```python
from uml_core.grader import grade_uml_diff

diff = {...}
result = grade_uml_diff(diff, max_score=20.0)
print(f"Note: {result['score']}/20 ({result['grade']})")
```

---

## Module: uml_core.comparator

**Fichier:** `src/uml_core/comparator.py`  
**Rôle:** Comparaison legacy de diagrammes UML (deprecated, remplacé par Vision LLM)

### Fonction: `compare_uml_diagrams(ref: UMLDiagram, student: UMLDiagram) -> dict`

**Description:** Compare deux diagrammes UML (méthode classique sans IA).

**Note:** Cette fonction est **deprecated** et remplacée par `extract_uml_json_from_image()` qui utilise GPT-4o Vision.

**Paramètres:**
- `ref` (UMLDiagram): Diagramme de référence
- `student` (UMLDiagram): Diagramme étudiant

**Returns:** Dictionnaire de différences (même format que Vision LLM)

**Fonctionnalités:**
- Fuzzy matching pour relations proches
- Tolérance sur types de relations équivalents
- Normalisation casse pour détection naming issues

---

## Module: uml_core.serializer

**Fichier:** `src/uml_core/serializer.py`  
**Rôle:** Conversion UMLDiagram ↔ JSON

### Fonction: `diagram_to_json(diagram: UMLDiagram) -> str`

**Description:** Convertit un UMLDiagram en chaîne JSON.

**Paramètres:**
- `diagram` (UMLDiagram): Instance de UMLDiagram

**Returns:** String JSON formaté (indent=2, UTF-8)

**Exemple:**
```python
from uml_core.models import UMLDiagram, UMLClass
from uml_core.serializer import diagram_to_json

diagram = UMLDiagram(classes=[UMLClass(name="Person")])
json_str = diagram_to_json(diagram)
# json_str = '{\n  "classes": [\n    {"name": "Person", ...}\n  ],\n  ...\n}'
```

---

### Fonction: `diagram_from_json(json_str: str) -> UMLDiagram`

**Description:** Parse une chaîne JSON en UMLDiagram.

**Paramètres:**
- `json_str` (str): String JSON représentant un diagramme

**Returns:** Instance de UMLDiagram

**Exemple:**
```python
json_str = '{"classes": [{"name": "Person", "attributes": [], "operations": []}], "relationships": []}'
diagram = diagram_from_json(json_str)
# diagram.classes[0].name = "Person"
```

---

## Module: uml_core.env

**Fichier:** `src/uml_core/env.py`  
**Rôle:** Gestion des variables d'environnement

### Variables globales:

#### `OPENAI_API_KEY` (str)
Clé API OpenAI pour GPT-4o Vision.

**Source:** Variable d'environnement ou fichier `.env`

**Format:** `sk-proj-...`

**Validation:** Lève `RuntimeError` si manquante

---

#### `OPENAI_API_BASE` (str)
URL de base de l'API OpenAI.

**Défaut:** `"https://api.openai.com/v1"`

**Usage:** Permet de pointer vers proxy/Azure OpenAI

**Exemple:**
```python
from uml_core.env import OPENAI_API_KEY, OPENAI_API_BASE

print(f"Clé: {OPENAI_API_KEY[:10]}...")
print(f"Base URL: {OPENAI_API_BASE}")
```

---

## Module: webapp.app

**Fichier:** `src/webapp/app.py`  
**Rôle:** Application web FastAPI avec endpoints

### Constantes:

- `BASE_DIR`: Dossier de base du module webapp
- `STATIC_DIR`: Dossier pour fichiers CSS/JS statiques
- `UPLOAD_DIR`: Dossier temporaire pour fichiers uploadés

### Endpoints FastAPI:

#### `GET /`

**Description:** Affiche la page d'accueil HTML.

**Returns:** HTMLResponse (template `index.html`)

**Exemple:**
```bash
curl http://localhost:8000/
# Renvoie le HTML de l'interface utilisateur
```

---

#### `POST /compare`

**Description:** Compare un diagramme UML avec une solution de référence.

**Workflow détaillé:**
1. Réception fichiers multipart/form-data
2. Sauvegarde temporaire dans `uploads/`
3. Lecture JSON référence
4. Prétraitement image (11 étapes OpenCV)
5. Appel GPT-4o Vision API
6. Récupération diff JSON
7. Parser poids personnalisés (si fournis)
8. Calcul note avec UMLGrader
9. Nettoyage fichiers temporaires
10. Retour JSONResponse

**Paramètres (multipart/form-data):**
- `student_img` (UploadFile): Image PNG/JPG du diagramme UML
- `reference_json` (UploadFile): Fichier JSON de référence
- `weights` (Optional[str]): JSON des poids personnalisés

**Format weights:**
```json
{
  "missing_class": 2.0,
  "extra_class": 1.5,
  "missing_attribute": 0.5,
  ...
}
```

**Returns (Success):**
```json
{
  "success": true,
  "diff": {
    "missing_classes": [...],
    "extra_classes": [...],
    ...
  },
  "grading": {
    "score": 15.5,
    "max_score": 20.0,
    "percentage": 77.5,
    "grade": "B+",
    "points_lost": 4.5,
    "error_breakdown": {...},
    "feedback": "...",
    "total_errors": 5
  }
}
```

**Returns (Error - 500):**
```json
{
  "success": false,
  "error": "Message d'erreur",
  "details": "Traceback complet..."
}
```

**Exemple curl:**
```bash
curl -X POST http://localhost:8000/compare \
  -F "student_img=@student.png" \
  -F "reference_json=@solution.json" \
  -F 'weights={"missing_class":3.0}'
```

**Exceptions gérées:**
- `ValueError`: Image illisible ou JSON invalide
- `requests.HTTPError`: Erreur API OpenAI
- `json.JSONDecodeError`: JSON malformé
- `Exception`: Toute autre erreur (traceback complet retourné)

**Sécurité:**
- Fichiers temporaires automatiquement nettoyés (finally block)
- Validation UTF-8 du JSON
- Timeout API 120 secondes

---

## Script: compare.py

**Fichier:** `scripts/compare.py`  
**Rôle:** Interface CLI pour comparaison UML

### Fonction: `main()`

**Description:** Point d'entrée du script CLI avec argparse.

**Arguments:**
- `--student` (requis): Fichier image du diagramme UML (PNG/JPG)
- `--reference` (requis): Fichier JSON de la solution
- `--diff` (optionnel): Fichier de sortie (défaut: `diff.json`)

**Workflow:**
1. Parsing arguments ligne de commande
2. Validation existence des fichiers
3. Lecture JSON référence
4. Appel extract_uml_json_from_image()
5. Écriture diff.json
6. Affichage résumé dans terminal

**Exemple d'usage:**
```bash
# Basique
python scripts/compare.py --student student.png --reference solution.json

# Avec fichier sortie personnalisé
python scripts/compare.py --student diagram.jpg --reference ref.json --diff my_diff.json
```

**Output terminal:**
```
[INFO] Chargement de la référence depuis 'solution.json'...
[INFO] Analyse de l'image 'student.png' avec GPT-4o Vision...
[INFO] Cela peut prendre 15-30 secondes...
💾 Écriture du rapport dans 'diff.json'...

============================================================
✅ Analyse terminée ! Total d'erreurs détectées : 5
============================================================
📄 Rapport détaillé : diff.json
⚠️  5 différence(s) trouvée(s). Consultez le fichier diff.json.
```

**Codes de sortie:**
- `0`: Succès
- `1`: Fichier introuvable ou erreur d'analyse

**Exceptions:**
- Affiche traceback complet si erreur API/parsing
- Messages préfixés [INFO], [ERREUR] pour clarté

---

## Résumé des fichiers

| Fichier | Rôle | Fonctions principales |
|---------|------|----------------------|
| `models.py` | Structures données UML | `UMLClass`, `UMLAttribute`, `UMLOperation`, `UMLRelationship`, `UMLDiagram` |
| `vision_llm_client.py` | API GPT-4o Vision | `extract_uml_json_from_image()`, `encode_image_base64()` |
| `preprocess_image.py` | Pipeline OpenCV | `preprocess_image()` (11 étapes) |
| `grader.py` | Système de notation | `UMLGrader.calculate_score()`, `grade_uml_diff()` |
| `comparator.py` | Comparaison legacy | `compare_uml_diagrams()` (deprecated) |
| `serializer.py` | Conversion JSON | `diagram_to_json()`, `diagram_from_json()` |
| `env.py` | Configuration | `OPENAI_API_KEY`, `OPENAI_API_BASE` |
| `app.py` | Web FastAPI | `GET /`, `POST /compare` |
| `compare.py` | CLI | `main()` (argparse) |

---

## Flux de données complet

```
1. Utilisateur upload image + JSON référence
           ↓
2. FastAPI endpoint /compare reçoit fichiers
           ↓
3. preprocess_image() - 11 étapes OpenCV
           ↓
4. encode_image_base64() - Conversion base64
           ↓
5. extract_uml_json_from_image() - GPT-4o Vision API
   - PHASE 1: Extraction UML
   - PHASE 2: Normalisation
   - PHASE 3: Comparaison
   - PHASE 4: Génération diff JSON
           ↓
6. UMLGrader.calculate_score() - Calcul note
   - Pondération erreurs
   - Calcul pourcentage
   - Attribution mention (A+ à F)
   - Génération feedback
           ↓
7. JSONResponse retournée à l'utilisateur
   - diff (10 catégories)
   - grading (score, grade, feedback)
           ↓
8. Interface affiche résultats + statistiques
```

---

## Types d'erreurs détectés

| Catégorie | Description | Poids défaut |
|-----------|-------------|--------------|
| `missing_classes` | Classes présentes dans référence mais absentes dans extraction | 2.0 pts |
| `extra_classes` | Classes présentes dans extraction mais absentes dans référence | 1.5 pts |
| `missing_attributes` | Attributs manquants (par classe) | 0.5 pts |
| `extra_attributes` | Attributs en trop (par classe) | 0.3 pts |
| `missing_operations` | Opérations manquantes (par classe) | 0.5 pts |
| `extra_operations` | Opérations en trop (par classe) | 0.3 pts |
| `missing_relationships` | Relations manquantes | 1.5 pts |
| `extra_relationships` | Relations en trop | 1.0 pts |
| `incorrect_multiplicities` | Multiplicités incorrectes sur relations existantes | 0.5 pts |
| `naming_issues` | Problèmes de casse, typos, texte illisible | 0.2 pts |

---

## Configuration et personnalisation

### Modifier les poids de notation

**Via API:**
```javascript
const formData = new FormData();
formData.append('student_img', imageFile);
formData.append('reference_json', jsonFile);
formData.append('weights', JSON.stringify({
    missing_class: 3.0,        // Pénalité plus sévère
    extra_class: 2.0,
    missing_attribute: 1.0,
    // ... autres poids
}));

fetch('/compare', { method: 'POST', body: formData });
```

**Via code Python:**
```python
from uml_core.grader import UMLGrader

grader = UMLGrader()
grader.WEIGHTS['missing_class'] = 3.0  # Modifier poids
result = grader.calculate_score(diff)
```

### Modifier le prompt GPT-4o

Éditer la variable `PROMPT` dans `vision_llm_client.py` (lignes 23-176).

**Sections modifiables:**
- PHASE 1: Règles d'extraction
- PHASE 2: Règles de normalisation
- PHASE 3: Règles de comparaison
- PHASE 4: Format de sortie

### Modifier le pipeline OpenCV

Éditer `preprocess_image()` dans `preprocess_image.py`.

**Paramètres ajustables:**
- Ligne 44: `max_dim = 1536` (taille max)
- Ligne 51: `h=10` (force denoising)
- Ligne 59: Kernel sharpening
- Ligne 63: `clipLimit=2.0` (CLAHE)
- Ligne 70: `blockSize=11` (binarisation)

---

**Fin de la documentation API**
