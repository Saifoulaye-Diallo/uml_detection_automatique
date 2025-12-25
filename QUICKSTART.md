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

## 4. Lancer les tests automatisés
```bash
# Tous les tests (19 tests)
pytest tests/test_complete.py -v

# Tests avec coverage
pytest tests/test_complete.py --cov=src/uml_core -v
```

## 5. Consulter les logs
```bash
# Logs du jour
cat logs/uml_grader_*.log

# Mode DEBUG (logs détaillés)
# Ajouter dans .env: DEBUG=true
```

---

**Nouvelles fonctionnalités:**
- ✅ Interface responsive (mobile + desktop)
- ✅ Rate limiting: 10 requêtes/minute
- ✅ Validation uploads: 10MB max, types MIME stricts
- ✅ Tests automatisés: 19 tests avec CI/CD
- ✅ Logging professionnel: console + fichiers avec rotation

---

Pour l'installation complète, voir [docs/INSTALLATION.md](docs/INSTALLATION.md)
