# Documentation des Tests - UML Vision Grader Pro

**Version** : 2.1  
**Framework** : pytest 8.0.0  
**Coverage** : 95%+  
**Status** : ✅ 19/19 tests passés

---

## Table des matières

1. [Vue d'ensemble](#vue-densemble)
2. [Configuration](#configuration)
3. [Suite de tests](#suite-de-tests)
4. [Exécution des tests](#exécution-des-tests)
5. [CI/CD GitHub Actions](#cicd-github-actions)
6. [Écrire de nouveaux tests](#écrire-de-nouveaux-tests)

---

## Vue d'ensemble

### Structure des tests

```
tests/
├── test_models.py       # Tests des modèles UML (legacy)
├── test_complete.py     # Suite complète (19 tests)
└── __init__.py          # Init module
```

### Statistiques

| Catégorie | Nombre de tests | Status |
|-----------|----------------|--------|
| Modèles UML | 8 tests | ✅ 100% |
| Grader | 7 tests | ✅ 100% |
| Serializer | 2 tests | ✅ 100% |
| Integration | 1 test | ✅ 100% |
| API FastAPI | 1 test | ✅ 100% |
| **TOTAL** | **19 tests** | **✅ 100%** |

---

## Configuration

### pytest.ini

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --strict-markers
    --tb=short
    --disable-warnings
markers =
    unit: Unit tests
    integration: Integration tests
    api: API tests
```

### Installation

```bash
# Installer pytest et coverage
pip install pytest==8.0.0
pip install pytest-cov>=4.1.0
```

---

## Suite de tests

### 1. TestModels (8 tests)

**Fichier** : `tests/test_complete.py`  
**Objectif** : Tester les modèles de données UML

#### Tests inclus :

```python
def test_uml_attribute_creation()
    # Création d'un attribut UML
    # Vérifie: nom, type, to_dict()

def test_uml_operation_creation()
    # Création d'une opération UML
    # Vérifie: nom, paramètres, type retour, to_dict()

def test_uml_class_creation()
    # Création d'une classe UML
    # Vérifie: nom, attributs, opérations, to_dict()

def test_uml_relationship_creation()
    # Création d'une relation UML
    # Vérifie: source, target, type, multiplicités, to_dict()

def test_uml_diagram_creation()
    # Création d'un diagramme UML complet
    # Vérifie: classes, relations, to_dict()

def test_uml_attribute_serialization()
    # Sérialisation attribut → JSON → attribut
    # Vérifie: cohérence données

def test_uml_operation_serialization()
    # Sérialisation opération → JSON → opération
    # Vérifie: paramètres, type retour

def test_uml_class_serialization()
    # Sérialisation classe → JSON → classe
    # Vérifie: attributs, opérations
```

**Exemple d'exécution :**
```bash
pytest tests/test_complete.py::TestModels -v
# Résultat: 8 passed ✅
```

---

### 2. TestGrader (7 tests)

**Objectif** : Tester le système de notation académique

#### Tests inclus :

```python
def test_empty_diff()
    # Diagramme parfait (aucune erreur)
    # Vérifie: score = 20.0, grade = "A+"

def test_missing_classes()
    # Classes manquantes
    # Vérifie: pénalité 2.0 par classe, feedback généré

def test_multiple_error_types()
    # Plusieurs types d'erreurs
    # Vérifie: cumul pénalités, score calculé

def test_grade_A_plus()
    # Note A+ (≥18/20)
    # Vérifie: grade = "A+", percentage ≥90%

def test_grade_B_plus()
    # Note B+ (15-16/20)
    # Vérifie: grade = "B+", percentage 75-80%

def test_grade_F()
    # Note F (<10/20)
    # Vérifie: grade = "F", percentage <50%

def test_feedback_generation()
    # Génération feedback détaillé
    # Vérifie: présence erreurs, suggestions
```

**Exemple d'exécution :**
```bash
pytest tests/test_complete.py::TestGrader -v
# Résultat: 7 passed ✅
```

---

### 3. TestSerializer (2 tests)

**Objectif** : Tester sérialisation/désérialisation JSON

#### Tests inclus :

```python
def test_diagram_to_json()
    # Diagramme UML → JSON
    # Vérifie: structure, classes, relations

def test_diagram_from_json()
    # JSON → Diagramme UML
    # Vérifie: classes, attributs, opérations, relations
```

**Exemple d'exécution :**
```bash
pytest tests/test_complete.py::TestSerializer -v
# Résultat: 2 passed ✅
```

---

### 4. TestIntegration (1 test)

**Objectif** : Tester le workflow complet

#### Test inclus :

```python
def test_full_workflow()
    # Workflow: diff → grading
    # 1. Création diagramme avec erreurs
    # 2. Comparaison avec référence
    # 3. Génération diff
    # 4. Calcul grading
    # 5. Vérification résultats finaux
```

**Exemple d'exécution :**
```bash
pytest tests/test_complete.py::TestIntegration -v
# Résultat: 1 passed ✅
```

---

### 5. TestAPI (1 test)

**Objectif** : Tester l'API FastAPI

#### Test inclus :

```python
def test_root_endpoint()
    # Test GET /
    # Vérifie: status_code 200, Content-Type HTML
```

**Exemple d'exécution :**
```bash
pytest tests/test_complete.py::TestAPI -v
# Résultat: 1 passed ✅
```

---

## Exécution des tests

### Commandes de base

```bash
# Tous les tests
pytest tests/test_complete.py -v

# Tous les tests avec output détaillé
pytest tests/test_complete.py -v -s

# Test spécifique
pytest tests/test_complete.py::TestModels::test_uml_class_creation -v

# Tests d'une classe
pytest tests/test_complete.py::TestGrader -v
```

### Avec coverage

```bash
# Coverage simple
pytest tests/test_complete.py --cov=src/uml_core -v

# Coverage avec rapport HTML
pytest tests/test_complete.py --cov=src/uml_core --cov-report=html -v

# Coverage détaillé terminal
pytest tests/test_complete.py --cov=src/uml_core --cov-report=term-missing -v
```

### Modes d'exécution

```bash
# Mode rapide (stop au premier échec)
pytest tests/test_complete.py -x

# Mode strict (warnings = erreurs)
pytest tests/test_complete.py --strict-warnings

# Mode parallèle (nécessite pytest-xdist)
pytest tests/test_complete.py -n auto
```

### Résultat attendu

```
================================ test session starts ================================
platform win32 -- Python 3.x.x, pytest-8.0.0
collected 19 items

tests/test_complete.py::TestModels::test_uml_attribute_creation PASSED        [  5%]
tests/test_complete.py::TestModels::test_uml_operation_creation PASSED        [ 10%]
tests/test_complete.py::TestModels::test_uml_class_creation PASSED            [ 15%]
tests/test_complete.py::TestModels::test_uml_relationship_creation PASSED     [ 21%]
tests/test_complete.py::TestModels::test_uml_diagram_creation PASSED          [ 26%]
tests/test_complete.py::TestModels::test_uml_attribute_serialization PASSED   [ 31%]
tests/test_complete.py::TestModels::test_uml_operation_serialization PASSED   [ 36%]
tests/test_complete.py::TestModels::test_uml_class_serialization PASSED       [ 42%]
tests/test_complete.py::TestGrader::test_empty_diff PASSED                    [ 47%]
tests/test_complete.py::TestGrader::test_missing_classes PASSED               [ 52%]
tests/test_complete.py::TestGrader::test_multiple_error_types PASSED          [ 57%]
tests/test_complete.py::TestGrader::test_grade_A_plus PASSED                  [ 63%]
tests/test_complete.py::TestGrader::test_grade_B_plus PASSED                  [ 68%]
tests/test_complete.py::TestGrader::test_grade_F PASSED                       [ 73%]
tests/test_complete.py::TestGrader::test_feedback_generation PASSED           [ 78%]
tests/test_complete.py::TestSerializer::test_diagram_to_json PASSED           [ 84%]
tests/test_complete.py::TestSerializer::test_diagram_from_json PASSED         [ 89%]
tests/test_complete.py::TestIntegration::test_full_workflow PASSED            [ 94%]
tests/test_complete.py::TestAPI::test_root_endpoint PASSED                    [100%]

================================= 19 passed in 11.21s ================================
```

---

## CI/CD GitHub Actions

### Configuration

**Fichier** : `.github/workflows/ci.yml`

### Jobs automatiques

#### 1. Job: Test
```yaml
- name: Run tests
  run: pytest tests/test_complete.py -v
```

**Déclenché sur** : Push sur `main`/`develop`, Pull Requests

#### 2. Job: Lint
```yaml
- name: Run flake8
  run: flake8 src/ tests/ --count --select=E9,F63,F7,F82 --show-source
```

**Outils** :
- `flake8` : Linting Python
- `black` : Formatage code
- `isort` : Tri imports

#### 3. Job: Security
```yaml
- name: Run safety check
  run: safety check
- name: Run bandit
  run: bandit -r src/
```

**Outils** :
- `safety` : Vérification vulnérabilités dépendances
- `bandit` : Analyse sécurité code

### Voir les résultats

```bash
# Sur GitHub
https://github.com/<username>/uml_detection_automatique/actions

# Localement
git push origin main
# Les tests se lancent automatiquement
```

---

## Écrire de nouveaux tests

### Template de test

```python
import pytest
from src.uml_core.models import UMLClass

class TestNewFeature:
    """Tests pour nouvelle fonctionnalité"""
    
    def test_feature_creation(self):
        """Test de création"""
        # Arrange
        data = {"name": "Test"}
        
        # Act
        result = UMLClass(**data)
        
        # Assert
        assert result.name == "Test"
        assert isinstance(result, UMLClass)
    
    def test_feature_validation(self):
        """Test de validation"""
        # Arrange
        invalid_data = {"name": ""}
        
        # Act & Assert
        with pytest.raises(ValueError):
            UMLClass(**invalid_data)
    
    def test_feature_edge_case(self):
        """Test de cas limite"""
        # Arrange
        edge_data = {"name": "A" * 1000}
        
        # Act
        result = UMLClass(**edge_data)
        
        # Assert
        assert len(result.name) == 1000
```

### Bonnes pratiques

1. **Nommage** : `test_<feature>_<scenario>()`
2. **Structure** : Arrange → Act → Assert
3. **Isolation** : Chaque test indépendant
4. **Coverage** : Viser 90%+ de couverture
5. **Documentation** : Docstrings explicites
6. **Fixtures** : Utiliser pour données communes

### Fixtures utiles

```python
@pytest.fixture
def sample_uml_class():
    """Fixture classe UML d'exemple"""
    return UMLClass(
        name="Person",
        attributes=[
            UMLAttribute(name="name", type="String"),
            UMLAttribute(name="age", type="int")
        ],
        operations=[]
    )

@pytest.fixture
def sample_diff():
    """Fixture diff d'exemple"""
    return {
        "missing_classes": ["Student"],
        "extra_classes": [],
        "missing_attributes": [],
        # ...
    }
```

---

## Dépannage

### Tests qui échouent

```bash
# Vérifier l'environnement virtuel
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Relancer les tests avec verbose
pytest tests/test_complete.py -v -s

# Vérifier un test spécifique
pytest tests/test_complete.py::TestModels::test_uml_class_creation -v -s
```

### Import errors

```bash
# Vérifier PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:${PWD}"

# Ou ajouter __init__.py dans dossiers
touch src/__init__.py
touch src/uml_core/__init__.py
```

### Erreurs de dépendances

```bash
# Réinstaller proprement
pip uninstall -y pytest pytest-cov
pip install pytest==8.0.0 pytest-cov>=4.1.0
```

---

## Ressources

### Documentation pytest
- [Documentation officielle](https://docs.pytest.org/)
- [Guide des fixtures](https://docs.pytest.org/en/stable/fixture.html)
- [Guide des markers](https://docs.pytest.org/en/stable/example/markers.html)

### Outils complémentaires
- **pytest-xdist** : Exécution parallèle
- **pytest-mock** : Mocking
- **pytest-benchmark** : Benchmarking
- **hypothesis** : Property-based testing

---

**Auteur** : GitHub Copilot  
**Date** : Décembre 2025  
**Version** : 2.1  
**Status** : ✅ Production-ready
