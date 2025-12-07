# 🚀 Démarrage rapide

Trois façons de lancer l'application :

## 1. Script Python simplifié (Recommandé)
```bash
python run_server.py
```
Puis ouvrir http://localhost:8000

## 2. Uvicorn directement
```bash
cd src
uvicorn webapp.app:app --reload --host 0.0.0.0 --port 8000
```

## 3. CLI pour traitement par lot
```bash
python scripts/compare.py --student examples/student.png --reference examples/solution.json
```

---

Pour l'installation complète, voir [docs/INSTALLATION.md](docs/INSTALLATION.md)
