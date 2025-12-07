# Guide d'installation rapide

## Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Clé API OpenAI (GPT-4o Vision)

## Installation en 5 étapes

### 1. Cloner le projet
```bash
git clone <repository-url>
cd "Code UML"
```

### 2. Créer l'environnement virtuel
**Windows PowerShell:**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux/macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Configurer les variables d'environnement
Créez un fichier `.env` à la racine du projet:
```env
OPENAI_API_KEY=sk-proj-votre-clé-api-ici
OPENAI_API_BASE=https://api.openai.com/v1
```

### 5. Lancer l'application

**Interface web:**
```bash
cd src
uvicorn webapp.app:app --reload --host 0.0.0.0 --port 8000
```
Puis ouvrir http://localhost:8000

**Ligne de commande:**
```bash
python scripts/compare.py --student examples/student.png --reference examples/solution.json
```

## Vérification de l'installation

Testez avec les fichiers d'exemple:
```bash
python scripts/compare.py --student examples/student.png --reference examples/solution.json
```

Si tout fonctionne, un fichier `diff.json` sera créé à la racine.

## Dépannage

### Erreur "OPENAI_API_KEY manquant"
- Vérifiez que le fichier `.env` existe à la racine
- Vérifiez que la clé API est correcte
- Redémarrez le terminal après avoir créé le `.env`

### Erreur OpenCV
```bash
pip uninstall opencv-python
pip install opencv-python-headless
```

### Erreur port 8000 déjà utilisé
Changez le port:
```bash
uvicorn webapp.app:app --reload --port 8080
```

## Structure après installation

```
Code UML/
├── .venv/                 # Environnement virtuel (créé)
├── src/                   # Code source
├── scripts/               # Scripts CLI
├── examples/              # Fichiers d'exemple
├── .env                   # Configuration (à créer)
└── requirements.txt       # Dépendances
```

---

Pour plus de détails, consultez [README.md](../README.md) et [docs/ARCHITECTURE.md](ARCHITECTURE.md).
