"""Application web FastAPI pour UML Vision Grader Pro.

Interface web moderne pour la correction automatique de diagrammes UML de classes.
Permet de téléverser une image (PNG/JPG) et un JSON de référence, puis affiche
un rapport détaillé des différences avec statistiques visuelles.

Endpoints:
    GET  /          - Interface utilisateur (HTML)
    POST /compare   - Analyse et comparaison (retourne JSON)

Author: UML Vision Grader Pro
Version: 1.0
Date: 2025
"""

from fastapi import FastAPI, Request, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import shutil
import os
import traceback
import json
from typing import Optional
from uml_core.vision_llm_client import extract_uml_json_from_image
from uml_core.grader import grade_uml_diff
from uml_core.logger import logger

# Rate limiter pour éviter spam API
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="UML Vision Grader Pro",
    description="Correction automatique de diagrammes UML par IA",
    version="1.0"
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configuration des chemins relatifs
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Créer le dossier static s'il n'existe pas
STATIC_DIR = os.path.join(BASE_DIR, "static")
os.makedirs(STATIC_DIR, exist_ok=True)

# Monter static seulement si le dossier contient des fichiers
if os.path.exists(STATIC_DIR) and os.listdir(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Affiche la page d'accueil de l'application.
    
    Args:
        request (Request): Requête HTTP FastAPI
    
    Returns:
        HTMLResponse: Template Jinja2 de l'interface utilisateur
    """
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/compare", response_class=JSONResponse)
@limiter.limit("10/minute")  # Max 10 requêtes par minute par IP
async def compare(
    request: Request,  # Nécessaire pour rate limiter
    student_img: UploadFile = File(...), 
    reference_json: UploadFile = File(...),
    weights: Optional[str] = Form(None)
):
    """Compare un diagramme UML avec une solution de référence.
    
    Workflow:
    1. Validation des fichiers uploadés
    2. Sauvegarde temporaire des fichiers
    3. Lecture du JSON de référence
    4. Appel à GPT-4o Vision avec prétraitement OpenCV
    5. Génération du rapport de différences
    6. Calcul de la note avec poids personnalisés
    7. Nettoyage des fichiers temporaires
    
    Args:
        request (Request): Requête HTTP (pour rate limiter)
        student_img (UploadFile): Image du diagramme UML (PNG/JPG)
        reference_json (UploadFile): Solution de référence (JSON)
        weights (Optional[str]): JSON des poids personnalisés
    
    Returns:
        JSONResponse: {
            "success": bool,
            "diff": dict,
            "grading": dict
        }
    
    Raises:
        400: Fichier invalide (type ou taille)
        500: En cas d'erreur (API, parsing, etc.)
    """
    # Validation taille fichiers (max 10MB)
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
    
    # Validation image
    allowed_image_types = ["image/png", "image/jpeg", "image/jpg"]
    if student_img.content_type not in allowed_image_types:
        logger.warning(f"Type d'image invalide: {student_img.content_type}")
        raise HTTPException(
            status_code=400,
            detail=f"Type d'image invalide. Formats acceptés: PNG, JPG, JPEG"
        )
    
    # Lire la taille de l'image
    img_content = await student_img.read()
    if len(img_content) > MAX_FILE_SIZE:
        logger.warning(f"Image trop volumineuse: {len(img_content)} bytes")
        raise HTTPException(
            status_code=400,
            detail=f"Image trop volumineuse (max 10MB). Taille: {len(img_content) // 1024 // 1024}MB"
        )
    
    # Validation JSON
    if reference_json.content_type != "application/json":
        logger.warning(f"Type JSON invalide: {reference_json.content_type}")
        raise HTTPException(
            status_code=400,
            detail="Type de fichier invalide. Format attendu: JSON"
        )
    
    json_content = await reference_json.read()
    if len(json_content) > MAX_FILE_SIZE:
        logger.warning(f"JSON trop volumineux: {len(json_content)} bytes")
        raise HTTPException(
            status_code=400,
            detail=f"Fichier JSON trop volumineux (max 10MB)"
        )
    
    student_img_path = None
    ref_json_path = None
    
    try:
        logger.info(f"Nouvelle requête de comparaison: {student_img.filename}")
        
        # Sauvegarder l'image (déjà lue pour validation)
        student_img_path = os.path.join(UPLOAD_DIR, student_img.filename)
        with open(student_img_path, "wb") as f:
            f.write(img_content)
        
        # Sauvegarder le JSON (déjà lu pour validation)
        ref_json_path = os.path.join(UPLOAD_DIR, reference_json.filename)
        with open(ref_json_path, "wb") as f:
            f.write(json_content)
        
        # Lecture du JSON de référence
        with open(ref_json_path, encoding="utf-8") as f:
            ref_json_content = f.read()
        
        logger.info("Lancement de l'analyse GPT-4o Vision...")
        # Extraction et comparaison via LLM
        diff = extract_uml_json_from_image(student_img_path, reference_json=ref_json_content)
        logger.info("Analyse terminée avec succès")
        
        # Parser les poids personnalisés si fournis
        custom_weights = None
        if weights:
            try:
                custom_weights = json.loads(weights)
            except json.JSONDecodeError:
                pass  # Utiliser les poids par défaut si parsing échoue
        
        # Calcul de la note académique avec poids personnalisés
        if custom_weights:
            from uml_core.grader import UMLGrader
            # Créer une instance temporaire avec poids personnalisés
            grader = UMLGrader()
            grader.WEIGHTS = {
                "missing_class": custom_weights.get("missing_class", 2.0),
                "extra_class": custom_weights.get("extra_class", 1.5),
                "missing_attribute": custom_weights.get("missing_attribute", 0.5),
                "extra_attribute": custom_weights.get("extra_attribute", 0.3),
                "missing_operation": custom_weights.get("missing_operation", 0.5),
                "extra_operation": custom_weights.get("extra_operation", 0.3),
                "missing_relationship": custom_weights.get("missing_relationship", 1.5),
                "extra_relationship": custom_weights.get("extra_relationship", 1.0),
                "incorrect_multiplicity": custom_weights.get("incorrect_multiplicity", 0.5),
                "naming_issue": custom_weights.get("naming_issue", 0.2),
            }
            grading_result = grader.calculate_score(diff, max_score=20.0)
        else:
            grading_result = grade_uml_diff(diff, max_score=20.0)
        
        return JSONResponse(content={
            "success": True,
            "diff": diff,
            "grading": grading_result
        })
    
    except HTTPException:
        # Re-raise HTTPException (erreurs de validation)
        raise
    except Exception as e:
        error_details = {
            "error": str(e),
            "type": type(e).__name__,
            "traceback": traceback.format_exc()
        }
        logger.error(f"Erreur dans /compare: {error_details}")
        
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e), "details": error_details["traceback"]}
        )
    
    finally:
        # Nettoyage des fichiers temporaires
        if student_img_path and os.path.exists(student_img_path):
            os.remove(student_img_path)
        if ref_json_path and os.path.exists(ref_json_path):
            os.remove(ref_json_path)

