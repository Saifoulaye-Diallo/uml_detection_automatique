"""Client pour l'extraction et la comparaison de diagrammes UML via GPT-4o Vision.

Ce module gère l'interaction avec l'API OpenAI GPT-4o Vision pour :
- Extraire les éléments UML depuis une image de diagramme
- Normaliser les éléments extraits
- Comparer avec un JSON de référence
- Générer un rapport de différences détaillé

Le prompt est conçu en 4 phases rigoureuses pour minimiser les hallucinations
et garantir une comparaison stricte et déterministe.

Author: UML Vision Grader Pro
Version: 2.0
Date: 2025
"""

import base64
import requests
import tempfile
from .env import OPENAI_API_BASE, OPENAI_API_KEY
from .preprocess_image import preprocess_image

PROMPT = (
    "You are an advanced vision-based UML class diagram correction system.\n"
    "Your behavior MUST be deterministic, rule-based, and strictly aligned with the reference JSON.\n"
    "\n"
    "====================================================\n"
    "GLOBAL BEHAVIOR RULES (ABSOLUTE)\n"
    "====================================================\n"
    "- You MUST perform the following phases INTERNALLY and IN ORDER:\n"
    "  PHASE 1 → Extract UML from the image\n"
    "  PHASE 2 → Normalize extracted elements\n"
    "  PHASE 3 → Compare to the reference JSON\n"
    "  PHASE 4 → Produce ONLY the final diff JSON\n"
    "\n"
    "- You MUST NOT guess or infer UML elements based on logic or domain knowledge.\n"
    "- You MUST NOT correct, improve, simplify, or interpret the student's design.\n"
    "- You MUST NOT add semantic reasoning. This is a strict visual comparison task.\n"
    "- If something is unclear visually, mark it as \"unknown\" and explain in \"naming_issues\".\n"
    "\n"
    "====================================================\n"
    "PHASE 1 — UML EXTRACTION FROM IMAGE (MANDATORY)\n"
    "====================================================\n"
    "Extract EXACTLY what appears in the image:\n"
    "\n"
    "1. Classes\n"
    "   - class name (case-sensitive)\n"
    "\n"
    "2. Attributes\n"
    "   - format: \"<name>: <type>\"\n"
    "   - if type is missing/unreadable → use \"unknown\"\n"
    "\n"
    "3. Operations\n"
    "   - name\n"
    "   - return type\n"
    "   - parameters with name + type\n"
    "   - If any component is unreadable → use \"unknown\"\n"
    "\n"
    "4. Relationships\n"
    "   Fields required:\n"
    "   - type: MUST be exactly one of:\n"
    "       [\"inheritance\", \"association\", \"aggregation\", \"composition\", \"dependency\"]\n"
    "   - from: source class name\n"
    "   - to: target class name\n"
    "   - multiplicity_from: exact text visible (ex: \"1\", \"0..*\", \"1..*\", \"0..1\", \"*\", \"n\", \"\")\n"
    "   - multiplicity_to: same format\n"
    "\n"
    "STRICT RULES:\n"
    "- Do NOT infer types or multiplicities.\n"
    "- Do NOT assume direction unless visually clear.\n"
    "- If a symbol is ambiguous, treat it as \"unknown\".\n"
    "\n"
    "====================================================\n"
    "PHASE 2 — NORMALIZATION RULES (INTERNAL)\n"
    "====================================================\n"
    "Normalize extracted elements so they can be compared:\n"
    "\n"
    "- Strip whitespace around names (\"Client \" → \"Client\")\n"
    "- Normalize multiplicities:\n"
    "  - Remove spaces (\"0 .. *\" → \"0..*\")\n"
    "  - If no multiplicity: use \"\"\n"
    "\n"
    "Do NOT:\n"
    "- rename elements\n"
    "- convert synonyms\n"
    "- fix typos\n"
    "\n"
    "====================================================\n"
    "PHASE 3 — STRICT COMPARISON TO REFERENCE\n"
    "====================================================\n"
    "Perform a field-by-field, element-by-element comparison.\n"
    "\n"
    "For each category:\n"
    "\n"
    "1. missing_classes → class exists in reference but NOT in extraction\n"
    "2. extra_classes → class exists in extraction but NOT in reference\n"
    "\n"
    "3. missing_attributes → attribute present in reference but absent in extraction\n"
    "4. extra_attributes → attribute present in extraction but not in reference\n"
    "\n"
    "5. missing_operations → operation present in reference but absent in extraction\n"
    "6. extra_operations → operation present in extraction but not in reference\n"
    "\n"
    "7. missing_relationships → relationship object exists in reference but not in extraction\n"
    "\n"
    "8. extra_relationships → relationship exists in extraction but not in reference\n"
    "\n"
    "9. incorrect_multiplicities\n"
    "   → relationship exists in both, but multiplicity_from or multiplicity_to does NOT match\n"
    "\n"
    "10. naming_issues\n"
    "   → unreadable, ambiguous text, OCR uncertainty, case mismatch, typos, etc.\n"
    "\n"
    "IMPORTANT:\n"
    "- ALL comparisons are CASE-SENSITIVE.\n"
    "- Direction of relationships MUST match exactly: (from/to).\n"
    "- Type of relationship MUST match exactly (no semantic correction).\n"
    "- If extraction == reference → ALL arrays MUST BE EMPTY.\n"
    "\n"
    "Example relationship object:\n"
    "{\n"
    "  \"type\": \"association\",\n"
    "  \"from\": \"Customer\",\n"
    "  \"to\": \"Order\",\n"
    "  \"multiplicity_from\": \"1\",\n"
    "  \"multiplicity_to\": \"0..*\"\n"
    "}\n"
    "\n"
    "====================================================\n"
    "PHASE 4 — FINAL OUTPUT (STRICT JSON)\n"
    "====================================================\n"
    "You MUST output ONLY this JSON, with EXACT field names and order:\n"
    "\n"
    "{\n"
    "  \"missing_classes\": [],\n"
    "  \"extra_classes\": [],\n"
    "  \"missing_attributes\": [],\n"
    "  \"extra_attributes\": [],\n"
    "  \"missing_operations\": [],\n"
    "  \"extra_operations\": [],\n"
    "  \"missing_relationships\": [],\n"
    "  \"extra_relationships\": [],\n"
    "  \"incorrect_multiplicities\": [],\n"
    "  \"naming_issues\": []\n"
    "}\n"
    "\n"
    "RULES:\n"
    "- NO markdown.\n"
    "- NO explanatory text.\n"
    "- NO comments.\n"
    "- NO reasoning.\n"
    "- NO extraction shown.\n"
    "- ONLY the JSON object.\n"
    "\n"
    "====================================================\n"
    "MANDATORY CHECKLIST (VERIFY BEFORE OUTPUT)\n"
    "====================================================\n"
    "Before producing the final JSON, you MUST internally verify:\n"
    "\n"
    "✓ Extraction includes ALL visible UML elements\n"
    "✓ No invented or inferred elements\n"
    "✓ Comparison is strictly visual, no semantic improvements\n"
    "✓ JSON is valid and respects the exact schema & order\n"
    "✓ All lists exist, even if empty\n"
    "✓ No hallucinated differences\n"
    "✓ If identical: ALL arrays are empty\n"
    "\n"
    "Return ONLY the JSON object.\n"
)

def encode_image_base64(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def extract_uml_json_from_image(image_path: str, reference_json: str = None) -> dict:
    """
    Prétraite l'image puis l'envoie à l'API OpenAI (GPT-4o vision) avec le JSON de référence, et récupère le diff JSON.
    """
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
        preprocess_image(image_path, tmp.name)
        preprocessed_path = tmp.name
    image_b64 = encode_image_base64(preprocessed_path)
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    user_content = [
        {"type": "text", "text": PROMPT},
        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_b64}"}}
    ]
    if reference_json is not None:
        user_content.append({"type": "text", "text": f"Reference JSON:\n{reference_json}"})
    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant that extracts UML diagrams from images."
            },
            {
                "role": "user",
                "content": user_content
            }
        ],
        "max_tokens": 2048,
        "response_format": {"type": "json_object"}
    }
    
    url = f"{OPENAI_API_BASE}/chat/completions"
    
    # Configuration de la session avec retry et désactivation SSL si nécessaire
    from requests.adapters import HTTPAdapter
    from requests.packages.urllib3.util.retry import Retry
    
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["POST"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    
    # Tentative avec vérification SSL
    try:
        response = session.post(url, headers=headers, json=payload, timeout=120, verify=True)
    except requests.exceptions.SSLError:
        # Si erreur SSL, réessayer sans vérification (solution temporaire)
        print("⚠️  Erreur SSL détectée, tentative sans vérification SSL...")
        response = session.post(url, headers=headers, json=payload, timeout=120, verify=False)
    
    response.raise_for_status()
    result = response.json()
    # OpenAI renvoie le JSON dans result['choices'][0]['message']['content']
    import json
    content = result['choices'][0]['message']['content']
    if isinstance(content, str):
        return json.loads(content)
    return content
