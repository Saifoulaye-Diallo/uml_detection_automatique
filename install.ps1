# Script d'installation automatique pour UML Vision Grader Pro
# Usage: .\install.ps1

Write-Host "`n=== INSTALLATION UML VISION GRADER PRO ===" -ForegroundColor Cyan

# 1. Vérifier Python
Write-Host "`n[1/6] Vérification de Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  Python détecté: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  ERREUR: Python non installé" -ForegroundColor Red
    Write-Host "  Téléchargez Python sur https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# 2. Créer environnement virtuel
Write-Host "`n[2/6] Création de l'environnement virtuel..." -ForegroundColor Yellow
if (Test-Path ".venv") {
    Write-Host "  .venv existe déjà" -ForegroundColor Gray
} else {
    python -m venv .venv
    Write-Host "  Environnement créé: .venv" -ForegroundColor Green
}

# 3. Activer l'environnement
Write-Host "`n[3/6] Activation de l'environnement..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1
Write-Host "  Environnement activé" -ForegroundColor Green

# 4. Installer dépendances
Write-Host "`n[4/6] Installation des dépendances..." -ForegroundColor Yellow
pip install --upgrade pip | Out-Null
pip install -r requirements.txt
Write-Host "  Dépendances installées" -ForegroundColor Green

# 5. Installer en mode développement
Write-Host "`n[5/6] Installation du package en mode développement..." -ForegroundColor Yellow
pip install -e .
Write-Host "  Package installé" -ForegroundColor Green

# 6. Configuration .env
Write-Host "`n[6/6] Configuration de l'environnement..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "  .env existe déjà" -ForegroundColor Gray
} else {
    Copy-Item ".env.example" ".env"
    Write-Host "  Fichier .env créé depuis .env.example" -ForegroundColor Green
    Write-Host "  N'oubliez pas d'ajouter votre clé OpenAI API!" -ForegroundColor Yellow
}

# Résumé
Write-Host "`n=== INSTALLATION TERMINÉE ===" -ForegroundColor Green
Write-Host "`nProchaines étapes:" -ForegroundColor Cyan
Write-Host "  1. Éditez .env et ajoutez votre OPENAI_API_KEY" -ForegroundColor White
Write-Host "  2. Lancez le serveur: python run_server.py" -ForegroundColor White
Write-Host "  3. Ouvrez http://localhost:8000" -ForegroundColor White
Write-Host "`nTests: pytest tests/test_complete.py -v" -ForegroundColor Gray
Write-Host "Documentation: voir docs/README.md`n" -ForegroundColor Gray
