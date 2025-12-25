# Guide de dépannage - UML Vision Grader Pro

Ce document contient les solutions aux problèmes les plus courants rencontrés lors de l'utilisation de l'application.

---

## 🔴 Problèmes critiques

### 1. Erreur "OPENAI_API_KEY manquant"

**Symptôme:**
```
RuntimeError: OPENAI_API_KEY manquant dans l'environnement ou le .env
```

**Solution:**
1. Créez un fichier `.env` à la racine du projet
2. Ajoutez votre clé API :
```env
OPENAI_API_KEY=sk-proj-votre-cle-ici
OPENAI_API_BASE=https://api.openai.com/v1
```
3. Obtenez une clé sur [platform.openai.com](https://platform.openai.com/api-keys)
4. Vérifiez que `.env` n'est PAS dans `.gitignore` (il y est normalement)

---

### 2. Erreur SSL / Certificate Verification

**Symptôme:**
```
SSLError: [SSL: CERTIFICATE_VERIFY_FAILED]
```

**Causes:** Antivirus (Kaspersky, Avast, Norton), proxy d'entreprise, firewall

**Solutions (par ordre de préférence):**

#### Solution 1: Mettre à jour les certificats
```powershell
pip install --upgrade certifi
```

#### Solution 2: Désactiver temporairement l'antivirus
- Windows Defender : Désactiver protection en temps réel
- Kaspersky/Avast : Désactiver SSL scanning
- **Réactiver après test !**

#### Solution 3: Utiliser un VPN
- Si votre réseau/pays bloque OpenAI
- VPN recommandé : Proton, NordVPN, ExpressVPN

#### Solution 4: Vérifier le proxy
```powershell
# Vérifier variables d'environnement proxy
echo $env:HTTP_PROXY
echo $env:HTTPS_PROXY

# Désactiver temporairement
$env:HTTP_PROXY=""
$env:HTTPS_PROXY=""
```

---

### 3. Erreur HTTP 401 Unauthorized

**Symptôme:**
```json
{
  "error": "Incorrect API key provided"
}
```

**Solutions:**
1. Vérifiez que votre clé API est correcte
2. Connectez-vous sur [platform.openai.com](https://platform.openai.com)
3. Vérifiez votre usage/quota
4. Rechargez des crédits si nécessaire
5. Générez une nouvelle clé si l'ancienne est révoquée

---

### 4. Erreur HTTP 429 Rate Limit

**Symptôme:**
```json
{
  "error": "Rate limit exceeded"
}
```

**Solutions:**
1. Attendez 1-2 minutes avant de réessayer
2. Vérifiez votre plan OpenAI (Tier 1, 2, 3...)
3. Upgradez votre plan si besoin
4. L'app a un rate limiter : max 10 requêtes/minute par IP

---

## 🟠 Problèmes d'installation

### 5. Module 'slowapi' introuvable

**Symptôme:**
```
ModuleNotFoundError: No module named 'slowapi'
```

**Solution:**
```powershell
# Activer environnement virtuel
.\.venv\Scripts\Activate.ps1

# Installer slowapi
pip install slowapi==0.1.9
```

---

### 6. Erreur "No module named 'uml_core'"

**Symptôme:**
```
ModuleNotFoundError: No module named 'uml_core'
```

**Causes:** PYTHONPATH incorrect, mauvais dossier de travail

**Solutions:**

#### Pour le serveur web:
```powershell
# Depuis la racine du projet
python run_server.py
```

#### Pour les scripts CLI:
```powershell
# Depuis la racine
python scripts/compare.py --student image.png --reference ref.json
```

#### Pour les tests:
```powershell
# Depuis la racine
pytest tests/test_complete.py -v
```

---

### 7. opencv-python ne s'installe pas

**Symptôme:**
```
ERROR: Could not build wheels for opencv-python
```

**Solution Windows:**
```powershell
# Installer Visual C++ Redistributable
# Télécharger depuis Microsoft

# Ou utiliser version pre-built
pip install opencv-python-headless==4.8.1.78
```

**Solution Linux:**
```bash
sudo apt-get install libopencv-dev python3-opencv
pip install opencv-python==4.8.1.78
```

---

## 🟡 Problèmes d'utilisation

### 8. Image trop volumineuse (>10MB)

**Symptôme:**
```json
{
  "detail": "Image trop volumineuse (max 10MB). Taille: 15MB"
}
```

**Solutions:**
1. Compresser l'image avec un outil en ligne
2. Réduire la résolution (max 4000x4000px recommandé)
3. Convertir en PNG avec compression

---

### 9. JSON de référence invalide

**Symptôme:**
```json
{
  "error": "Expecting property name enclosed in double quotes"
}
```

**Solution:**
1. Validez votre JSON sur [jsonlint.com](https://jsonlint.com)
2. Vérifiez les guillemets doubles `"` (pas simples `'`)
3. Vérifiez les virgules (pas de virgule après dernier élément)
4. Utilisez `examples/solution.json` comme template

Format correct:
```json
{
  "classes": [
    {
      "name": "Person",
      "attributes": [
        {"name": "age", "type": "int"}
      ],
      "operations": []
    }
  ],
  "relationships": []
}
```

---

### 10. Analyse prend trop de temps (>60s)

**Causes possibles:**
- Image très grande (>5MB)
- GPT-4o Vision surchargé
- Connexion internet lente

**Solutions:**
1. Réduire taille de l'image
2. Réessayer dans 5 minutes
3. Vérifier votre connexion internet
4. Timeout par défaut : 120 secondes

---

### 11. Diagramme mal reconnu

**Symptômes:**
- Classes manquantes
- Attributs mal lus
- Relations incorrectes

**Solutions:**

#### Améliorer la qualité de l'image:
1. **Résolution minimale** : 800x600px
2. **Format** : PNG (meilleur que JPG)
3. **Contraste** : Fond blanc, traits noirs
4. **Netteté** : Pas de flou

#### Bonnes pratiques UML:
1. Classe : Nom en **CamelCase** (ex: `Person`, `CieAerienne`)
2. Attributs : Format `name: Type` (ex: `age: int`)
3. Relations : Flèches claires avec multiplicités visibles
4. Pas de texte manuscrit

#### Pipeline OpenCV automatique:
- L'app applique déjà 11 étapes de traitement
- Si résultat insatisfaisant, améliorer l'image source

---

## 🔧 Problèmes de développement

### 12. Tests pytest échouent

**Symptôme:**
```
FAILED tests/test_complete.py::TestAPI::test_root_endpoint
```

**Solution:**
```powershell
# Utiliser Python de l'environnement virtuel
.\.venv\Scripts\python.exe -m pytest tests/test_complete.py -v

# Ou activer l'env d'abord
.\.venv\Scripts\Activate.ps1
pytest tests/test_complete.py -v
```

---

### 13. FastAPI ne démarre pas sur port 8000

**Symptôme:**
```
ERROR: [Errno 10048] Address already in use
```

**Solution:**
```powershell
# Trouver le processus utilisant le port 8000
netstat -ano | findstr :8000

# Tuer le processus (remplacer PID par le numéro trouvé)
taskkill /PID <PID> /F

# Ou lancer sur autre port
uvicorn webapp.app:app --port 8001
```

---

### 14. Logs non créés

**Symptôme:**
Aucun fichier dans `logs/`

**Solution:**
1. Vérifiez que le dossier `logs/` existe (créé automatiquement)
2. Vérifiez les permissions d'écriture
3. Les logs sont nommés `uml_grader_YYYYMMDD.log`
4. Logs console : niveau INFO par défaut
5. Logs fichier : niveau DEBUG (tout)

Activer DEBUG en console:
```powershell
$env:DEBUG="true"
python run_server.py
```

---

## 📱 Problèmes interface

### 15. Interface ne s'affiche pas correctement

**Symptôme:**
- Layout cassé
- Boutons manquants
- Couleurs incorrectes

**Solutions:**
1. Videz le cache navigateur (Ctrl+F5)
2. Vérifiez que Tailwind CSS se charge (cdn.tailwindcss.com)
3. Désactivez bloqueur de pub (peut bloquer CDN)
4. Testez sur autre navigateur (Chrome/Firefox/Edge)

---

### 16. Upload ne fonctionne pas

**Symptôme:**
Bouton "Lancer l'analyse" ne fait rien

**Solutions:**
1. Ouvrez console développeur (F12)
2. Vérifiez les erreurs JavaScript
3. Vérifiez que les deux fichiers sont sélectionnés
4. Types acceptés : PNG, JPG, JPEG (image) + JSON (référence)
5. Taille max : 10MB par fichier

---

## 🌐 Problèmes réseau

### 17. Timeout après 120 secondes

**Symptôme:**
```
TimeoutError: Request timed out after 120s
```

**Solutions:**
1. Vérifiez votre connexion internet
2. Image trop grande : réduire à <2MB
3. OpenAI API en maintenance : vérifier [status.openai.com](https://status.openai.com)
4. Réessayer dans 5-10 minutes

---

### 18. Proxy d'entreprise bloque l'API

**Symptôme:**
```
ProxyError: Cannot connect to proxy
```

**Solution:**
1. Contactez votre admin réseau
2. Ajoutez OpenAI à la whitelist
3. Utilisez un VPN personnel
4. Travaillez depuis réseau personnel (hotspot mobile)

---

## 🆘 Support et aide

### Ressources:
- **Documentation** : `docs/API_REFERENCE.md`
- **Architecture** : `docs/ARCHITECTURE.md`
- **Installation** : `docs/INSTALLATION.md`
- **GitHub Issues** : [github.com/Saifoulaye-Diallo/uml_detection_automatique/issues](https://github.com/Saifoulaye-Diallo/uml_detection_automatique/issues)

### Diagnostic complet:
```powershell
# Test connexion API
python scripts/test_openai.py

# Test modèles
python tests/test_models.py

# Tests complets
pytest tests/test_complete.py -v

# Vérifier environnement
pip list
```

### Informations à fournir pour support:
1. Message d'erreur complet
2. Version Python (`python --version`)
3. Système d'exploitation
4. Logs (`logs/uml_grader_YYYYMMDD.log`)
5. Étapes pour reproduire l'erreur

---

**Dernière mise à jour:** 2025-12-25  
**Version:** 2.1
