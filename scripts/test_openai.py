"""Script de test pour diagnostiquer les problèmes de connexion à l'API OpenAI.

Usage:
    python scripts/test_openai.py
"""

from uml_core.logger import logger
import sys
import os

sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), '..', 'src')
)


def test_connection():
    """Test de connexion à l'API OpenAI."""
    logger.info("Test de connexion à l'API OpenAI...\n")

    # 1. Vérifier les variables d'environnement
    logger.info("1. Vérification des variables d'environnement...")
    try:
        from uml_core.env import OPENAI_API_KEY, OPENAI_API_BASE
        logger.info(
            f"   [OK] OPENAI_API_KEY: {OPENAI_API_KEY[:20]}..."
            f"{OPENAI_API_KEY[-10:]}"
        )
        logger.info(f"   [OK] OPENAI_API_BASE: {OPENAI_API_BASE}")
    except Exception as e:
        logger.error(f"   Erreur: {e}")
        return

    # 2. Test de connexion simple
    logger.info("\n2. Test de connexion HTTPS basique...")
    import requests
    try:
        response = requests.get(
            "https://api.openai.com", timeout=10, verify=True
        )
        logger.info(
            f"   [OK] Connexion réussie (code {response.status_code})"
        )
    except requests.exceptions.SSLError as e:
        logger.error(f"   Erreur SSL: {e}")
        logger.warning("   Essayez avec verify=False...")
        try:
            response = requests.get(
                "https://api.openai.com", timeout=10, verify=False
            )
            logger.warning(
                f"   Connexion réussie SANS vérification SSL "
                f"(code {response.status_code})"
            )
            logger.info(
                "   Votre antivirus/proxy bloque probablement les "
                "certificats SSL"
            )
        except Exception as e2:
            logger.error(f"   Erreur persistante: {e2}")
    except Exception as e:
        logger.error(f"   Erreur: {e}")

    # 3. Test de l'API OpenAI
    logger.info("\n3. Test de l'API OpenAI (modèle simple)...")
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
        urllib3.disable_warnings(
            urllib3.exceptions.InsecureRequestWarning
        )

        response = requests.post(
            f"{OPENAI_API_BASE}/chat/completions",
            headers=headers,
            json=payload,
            timeout=30,
            verify=False  # Désactiver temporairement pour le test
        )
        response.raise_for_status()
        result = response.json()
        logger.info(
            f"   [OK] API fonctionnelle: "
            f"{result['choices'][0]['message']['content']}"
        )
    except requests.exceptions.HTTPError as e:
        logger.error(
            f"   Erreur HTTP {e.response.status_code}: "
            f"{e.response.text}"
        )
    except Exception as e:
        logger.error(f"   Erreur: {e}")

    # 4. Recommandations
    logger.info("\n" + "=" * 60)
    logger.info("RECOMMANDATIONS:")
    logger.info("=" * 60)
    logger.info("Si vous avez des erreurs SSL:")
    logger.info(
        "  1. Désactivez temporairement votre antivirus "
        "(Kaspersky, Avast, etc.)"
    )
    logger.info("  2. Vérifiez votre proxy/firewall d'entreprise")
    logger.info("  3. Utilisez un VPN si votre réseau bloque OpenAI")
    logger.info(
        "  4. Mettez à jour Python: pip install --upgrade certifi"
    )
    logger.info("\nSi l'API répond avec erreur 401:")
    logger.info("  - Vérifiez votre clé API dans .env")
    logger.info("  - Rechargez des crédits sur platform.openai.com")
    logger.info("\nSi l'API répond avec erreur 429:")
    logger.info("  - Vous avez dépassé votre quota/limite de taux")
    logger.info(
        "  - Attendez quelques minutes ou upgradez votre plan"
    )


if __name__ == "__main__":
    test_connection()
