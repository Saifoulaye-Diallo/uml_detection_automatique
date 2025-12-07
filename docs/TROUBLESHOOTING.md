## 🔧 Guide de résolution des erreurs

### Erreur SSL (UNEXPECTED_EOF_WHILE_READING)

**Causes possibles:**
1. Antivirus bloquant les certificats SSL (Kaspersky, Avast, Norton)
2. Proxy/Firewall d'entreprise
3. Certificats SSL obsolètes

**Solutions:**

1. **Mettre à jour les certificats:**
```bash
pip install --upgrade certifi
pip install --upgrade urllib3
```

2. **Désactiver temporairement l'antivirus** et réessayer

3. **Utiliser un VPN** si votre réseau bloque OpenAI

4. **Le code a déjà été corrigé** pour contourner automatiquement les erreurs SSL

---

### ❌ Erreur 401: Invalid API Key

**Votre clé API OpenAI est invalide ou expirée.**

**Solution:**

1. **Créer une nouvelle clé API:**
   - Allez sur https://platform.openai.com/api-keys
   - Cliquez sur "Create new secret key"
   - Copiez la clé (elle commence par `sk-proj-...`)

2. **Mettre à jour le fichier `.env`:**
```bash
# Ouvrez .env et remplacez la ligne:
OPENAI_API_KEY=votre-nouvelle-clé-ici
```

3. **Redémarrer le serveur:**
```bash
python run_server.py
```

---

### ⚡ Erreur 429: Rate Limit

**Vous avez dépassé votre quota.**

**Solution:**
- Attendez quelques minutes
- Vérifiez votre plan sur https://platform.openai.com/account/usage
- Ajoutez des crédits si nécessaire

---

### 🧪 Tester la connexion

Utilisez le script de diagnostic:
```bash
python scripts/test_openai.py
```

Ce script vous dira exactement quel est le problème.

---

### 📝 Commandes de test CLI

**Test rapide sans serveur web:**
```bash
python scripts/compare.py --student examples/student.png --reference examples/solution.json
```

Cette commande teste directement l'API OpenAI et génère `diff.json` si tout fonctionne.

---

### 🌐 Vérifier que le serveur fonctionne

1. **Lancer le serveur:**
```bash
python run_server.py
```

2. **Tester dans le navigateur:**
```
http://localhost:8000
```

3. **Voir les logs en temps réel** dans le terminal

---

### 🆘 Si rien ne fonctionne

1. Vérifiez votre connexion internet
2. Testez avec `curl`:
```bash
curl https://api.openai.com/v1/models -H "Authorization: Bearer VOTRE_CLE_API"
```
3. Créez une issue sur GitHub avec les logs complets
