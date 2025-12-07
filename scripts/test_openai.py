"""Script de test pour diagnostiquer les problèmes de connexion à l'API OpenAI.

Usage:
    python scripts/test_openai.py
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_connection():
    """Test de connexion à l'API OpenAI."""
    print("🔍 Test de connexion à l'API OpenAI...\n")
    
    # 1. Vérifier les variables d'environnement
    print("1️⃣ Vérification des variables d'environnement...")
    try:
        from uml_core.env import OPENAI_API_KEY, OPENAI_API_BASE
        print(f"   ✅ OPENAI_API_KEY: {OPENAI_API_KEY[:20]}...{OPENAI_API_KEY[-10:]}")
        print(f"   ✅ OPENAI_API_BASE: {OPENAI_API_BASE}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return
    
    # 2. Test de connexion simple
    print("\n2️⃣ Test de connexion HTTPS basique...")
    import requests
    try:
        response = requests.get("https://api.openai.com", timeout=10, verify=True)
        print(f"   ✅ Connexion réussie (code {response.status_code})")
    except requests.exceptions.SSLError as e:
        print(f"   ❌ Erreur SSL: {e}")
        print("   💡 Essayez avec verify=False...")
        try:
            response = requests.get("https://api.openai.com", timeout=10, verify=False)
            print(f"   ⚠️  Connexion réussie SANS vérification SSL (code {response.status_code})")
            print("   📝 Votre antivirus/proxy bloque probablement les certificats SSL")
        except Exception as e2:
            print(f"   ❌ Erreur persistante: {e2}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # 3. Test de l'API OpenAI
    print("\n3️⃣ Test de l'API OpenAI (modèle simple)...")
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": "Say 'Hello'"}],
        "max_tokens": 10
    }
    
    try:
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        response = requests.post(
            f"{OPENAI_API_BASE}/chat/completions",
            headers=headers,
            json=payload,
            timeout=30,
            verify=False  # Désactiver temporairement pour le test
        )
        response.raise_for_status()
        result = response.json()
        print(f"   ✅ API fonctionnelle: {result['choices'][0]['message']['content']}")
    except requests.exceptions.HTTPError as e:
        print(f"   ❌ Erreur HTTP {e.response.status_code}: {e.response.text}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # 4. Recommandations
    print("\n" + "="*60)
    print("📋 RECOMMANDATIONS:")
    print("="*60)
    print("Si vous avez des erreurs SSL:")
    print("  1. Désactivez temporairement votre antivirus (Kaspersky, Avast, etc.)")
    print("  2. Vérifiez votre proxy/firewall d'entreprise")
    print("  3. Utilisez un VPN si votre réseau bloque OpenAI")
    print("  4. Mettez à jour Python: pip install --upgrade certifi")
    print("\nSi l'API répond avec erreur 401:")
    print("  - Vérifiez votre clé API dans .env")
    print("  - Rechargez des crédits sur platform.openai.com")
    print("\nSi l'API répond avec erreur 429:")
    print("  - Vous avez dépassé votre quota/limite de taux")
    print("  - Attendez quelques minutes ou upgradez votre plan")


if __name__ == "__main__":
    test_connection()
