# Guide de Test du Pipeline CI/CD

## Vue d'ensemble

Le pipeline CI/CD est configuré avec GitHub Actions et s'exécute automatiquement sur :
- **Push** sur les branches `main` ou `develop`
- **Pull Request** vers `main`

Le pipeline comporte 3 jobs parallèles :
1. **test** - Exécution des tests
2. **lint** - Vérification du formatage du code
3. **security** - Analyse de sécurité

---

## Méthode 1 : Test automatique (Push sur GitHub)

### Étape 1 : Créer une modification

```powershell
cd "c:\Users\Saifon\Documents\Code UML"

# Modifier un fichier (exemple)
echo "# Test pipeline" >> README.md
```

### Étape 2 : Commit et push

```powershell
git add README.md
git commit -m "test: vérification pipeline CI/CD"
git push origin main
```

### Étape 3 : Vérifier l'exécution

1. Aller sur GitHub : `https://github.com/Saifoulaye-Diallo/uml_detection_automatique`
2. Cliquer sur l'onglet **Actions**
3. Voir le workflow "CI/CD Pipeline" en cours d'exécution
4. Cliquer dessus pour voir les détails des 3 jobs

**Temps d'exécution** : ~3-5 minutes

---

## Méthode 2 : Test manuel local (Simulation)

### Test Job 1 : Tests automatiques

```powershell
cd "c:\Users\Saifon\Documents\Code UML"
.\.venv\Scripts\Activate.ps1

# Installer les dépendances (si nécessaire)
pip install -r requirements.txt

# Lancer les tests pytest
python -m pytest tests/test_complete.py -v --tb=short

# Lancer test_models
python tests/test_models.py

# Vérifier qualité code
pip install flake8
flake8 src/ --count --select=E9,F63,F7,F82 --show-source --statistics
```

**Résultat attendu** :
```
tests/test_complete.py::TestModels::test_uml_attribute_creation PASSED
...
================================= 19 passed in 11.21s =================================
```

---

### Test Job 2 : Linting

```powershell
# Installer les linters
pip install flake8 black isort

# Vérifier formatage avec black
black --check src/ tests/ scripts/

# Vérifier tri des imports
isort --check-only src/ tests/ scripts/

# Lint avec flake8
flake8 src/ tests/ scripts/ --count --statistics
```

**Résultat attendu** :
```
All done! ✨ 🍰 ✨
X files would be left unchanged.
```

---

### Test Job 3 : Sécurité

```powershell
# Installer outils sécurité
pip install safety bandit

# Vérifier vulnérabilités dépendances
safety check --json

# Analyser code avec bandit
bandit -r src/ -f json
```

**Résultat attendu** :
```
No known security vulnerabilities found.
```

---

## Méthode 3 : Test avec Pull Request

### Étape 1 : Créer une branche

```powershell
cd "c:\Users\Saifon\Documents\Code UML"

# Créer une branche de test
git checkout -b test/pipeline-validation

# Faire des modifications
echo "# Test PR" >> QUICKSTART.md

# Commit
git add QUICKSTART.md
git commit -m "test: validation pipeline via PR"

# Push la branche
git push origin test/pipeline-validation
```

### Étape 2 : Créer une Pull Request

1. Aller sur GitHub
2. Cliquer sur **Pull requests**
3. Cliquer sur **New pull request**
4. Sélectionner `test/pipeline-validation` → `main`
5. Cliquer sur **Create pull request**

### Étape 3 : Observer le pipeline

Le pipeline s'exécute automatiquement :
- Onglet **Checks** dans la PR
- Voir les 3 jobs : test, lint, security
- Attendre que tout soit vert

### Étape 4 : Merger ou fermer la PR

```powershell
# Option 1 : Merger via GitHub UI

# Option 2 : Supprimer la branche de test
git checkout main
git branch -D test/pipeline-validation
git push origin --delete test/pipeline-validation
```

---

## Méthode 4 : Déclencher manuellement (workflow_dispatch)

### Modifier .github/workflows/ci.yml

Ajouter `workflow_dispatch` :

```yaml
on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  workflow_dispatch:  # Permet déclenchement manuel
```

### Déclencher depuis GitHub

1. Onglet **Actions**
2. Sélectionner "CI/CD Pipeline"
3. Cliquer sur **Run workflow**
4. Choisir la branche
5. Cliquer sur **Run workflow**

---

## Vérifier les résultats du pipeline

### Sur GitHub Actions

1. **Onglet Actions** : `https://github.com/Saifoulaye-Diallo/uml_detection_automatique/actions`
2. Cliquer sur un workflow run
3. Voir les 3 jobs en parallèle :
   - **Tests automatiques** (job test)
   - **Linting** (job lint)
   - **Sécurité** (job security)

### Détails de chaque job

**Job test** :
```
✓ Checkout code
✓ Setup Python 3.12
✓ Install dependencies
✓ Run tests (19 passed)
✓ Test models
✓ Check code quality
```

**Job lint** :
```
✓ Checkout code
✓ Setup Python
✓ Install linters
✓ Check formatting with black
✓ Check import sorting
✓ Lint with flake8
```

**Job security** :
```
✓ Checkout code
✓ Setup Python
✓ Check for security vulnerabilities
```

---

## Résoudre les échecs

### Si le job "test" échoue

```powershell
# Lancer les tests localement pour débugger
pytest tests/test_complete.py -v -s

# Voir les erreurs détaillées
pytest tests/test_complete.py -v --tb=long
```

### Si le job "lint" échoue

```powershell
# Corriger automatiquement le formatage
black src/ tests/ scripts/

# Corriger le tri des imports
isort src/ tests/ scripts/

# Vérifier
flake8 src/ tests/ scripts/
```

### Si le job "security" échoue

```powershell
# Voir les vulnérabilités
safety check

# Mettre à jour les dépendances vulnérables
pip install --upgrade <package>
pip freeze > requirements.txt
```

---

## Statut du pipeline

### Badges GitHub Actions

Ajouter dans README.md :

```markdown
[![CI/CD Pipeline](https://github.com/Saifoulaye-Diallo/uml_detection_automatique/actions/workflows/ci.yml/badge.svg)](https://github.com/Saifoulaye-Diallo/uml_detection_automatique/actions/workflows/ci.yml)
```

### Voir l'historique

```powershell
# Via GitHub CLI (si installé)
gh run list --workflow=ci.yml

# Voir les détails d'un run
gh run view <run-id>
```

---

## Test complet du pipeline maintenant

### Script de test rapide

```powershell
cd "c:\Users\Saifon\Documents\Code UML"
.\.venv\Scripts\Activate.ps1

Write-Host "`n=== TEST PIPELINE CI/CD ===" -ForegroundColor Green

Write-Host "`n1. Tests pytest..." -ForegroundColor Cyan
python -m pytest tests/test_complete.py -v

Write-Host "`n2. Linting..." -ForegroundColor Cyan
pip install -q flake8 black isort
black --check src/ tests/ scripts/
isort --check-only src/ tests/ scripts/
flake8 src/ tests/ scripts/ --count --statistics

Write-Host "`n3. Sécurité..." -ForegroundColor Cyan
pip install -q safety bandit
safety check || Write-Host "Safety check completed" -ForegroundColor Yellow
bandit -r src/ -ll || Write-Host "Bandit scan completed" -ForegroundColor Yellow

Write-Host "`n=== PIPELINE TEST TERMINÉ ===" -ForegroundColor Green
```

### Exécuter le script

```powershell
cd "c:\Users\Saifon\Documents\Code UML"
.\.venv\Scripts\Activate.ps1

# Copier le script ci-dessus et l'exécuter
```

---

## Configuration avancée

### Ajouter des notifications

Modifier `.github/workflows/ci.yml` :

```yaml
- name: Send notification on failure
  if: failure()
  run: |
    echo "Pipeline failed! Check logs."
```

### Ajouter cache pour accélérer

```yaml
- name: Cache pip packages
  uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-
```

### Matrice de tests multi-versions

```yaml
strategy:
  matrix:
    python-version: ['3.10', '3.11', '3.12']
```

---

## Récapitulatif

**4 méthodes pour tester le pipeline :**

1. **Push automatique** - La plus simple
   ```powershell
   git add .
   git commit -m "test"
   git push origin main
   ```

2. **Tests locaux** - Pour débugger
   ```powershell
   pytest tests/test_complete.py -v
   flake8 src/
   ```

3. **Pull Request** - Pour tester avant merge
   ```powershell
   git checkout -b test-branch
   # modifications
   git push origin test-branch
   # Créer PR sur GitHub
   ```

4. **Manuel** - Via GitHub Actions UI
   - Actions → CI/CD Pipeline → Run workflow

**Temps d'exécution total** : ~3-5 minutes sur GitHub Actions

**Coût** : Gratuit (2000 minutes/mois pour comptes publics)

---

**Prochaines étapes recommandées :**

1. Tester maintenant avec un push de test
2. Vérifier les résultats sur GitHub Actions
3. Ajouter le badge dans README.md
4. Configurer les notifications si souhaité

---

**Auteur** : GitHub Copilot  
**Date** : 25 Décembre 2025  
**Version** : 1.0
< ! - -   T e s t   p i p e l i n e   C I / C D   -   2 0 2 5 - 1 2 - 2 5   1 3 : 0 2 : 5 3   - - >  
 