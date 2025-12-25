"""Pipeline de prétraitement d'images pour optimiser la reconnaissance UML.

Ce module implémente un pipeline OpenCV en 11 étapes pour transformer
une image de diagramme UML brute en une version optimisée pour la
reconnaissance par modèle vision (GPT-4o Vision).

Author: UML Vision Grader Pro
Version: 2.0
Date: 2025
"""

import cv2
import numpy as np


def preprocess_image(input_path: str, output_path: str) -> None:
    """Prétraite une image UML pour maximiser la reconnaissance par IA.

    Pipeline complet en 11 étapes :
    1. Redimensionnement intelligent (max 1536px)
    2. Conversion en niveaux de gris
    3. Denoising agressif (fastNlMeansDenoising)
    4. Sharpening (kernel 3x3)
    5. Amélioration du contraste (CLAHE)
    6. Binarisation adaptative (Gaussian)
    7. Morphologie (nettoyage des artefacts)
    8. Recadrage intelligent avec marges
    9. Upscaling si nécessaire (<800px)
    10. Inversion si fond sombre
    11. Export PNG compression maximale

    Args:
        input_path (str): Chemin vers l'image source (PNG/JPG)
        output_path (str): Chemin de sortie pour l'image traitée (PNG)

    Raises:
        ValueError: Si l'image source ne peut pas être lue

    Example:
        >>> preprocess_image('student.png', 'student_preprocessed.png')
    """
    # 1. Lecture
    img = cv2.imread(input_path)
    if img is None:
        raise ValueError(f"Cannot read image: {input_path}")

    # 2. Redimensionnement intelligent (max 1536px pour meilleure qualité)
    h, w = img.shape[:2]
    max_dim = 1536
    scale = min(max_dim / max(h, w), 1.0)
    if scale < 1.0:
        new_w, new_h = int(w * scale), int(h * scale)
        img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)

    # 3. Conversion en niveaux de gris
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 4. Denoising agressif pour éliminer le bruit de scan/photo
    denoised = cv2.fastNlMeansDenoising(
        gray, h=10, templateWindowSize=7, searchWindowSize=21)

    # 5. Sharpening pour améliorer la netteté du texte et des traits
    kernel_sharpen = np.array([[-1, -1, -1],
                               [-1, 9, -1],
                               [-1, -1, -1]])
    sharpened = cv2.filter2D(denoised, -1, kernel_sharpen)

    # 6. Amélioration du contraste via CLAHE (Contrast Limited Adaptive
    # Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    contrast_enhanced = clahe.apply(sharpened)

    # 7. Binarisation adaptative pour séparer texte/lignes du fond
    binarized = cv2.adaptiveThreshold(
        contrast_enhanced,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        blockSize=11,  # Bloc plus petit pour capturer les détails fins
        C=2  # Seuil ajusté pour meilleure séparation
    )

    # 8. Morphologie: nettoyer les petits artefacts tout en préservant les
    # traits UML
    kernel_clean = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    cleaned = cv2.morphologyEx(binarized, cv2.MORPH_CLOSE, kernel_clean)

    # 9. Crop automatique des marges blanches
    coords = cv2.findNonZero(255 - cleaned)
    if coords is not None:
        x, y, w_crop, h_crop = cv2.boundingRect(coords)
        # Ajouter une petite marge (5px) pour ne pas couper les bordures
        margin = 5
        x = max(0, x - margin)
        y = max(0, y - margin)
        w_crop = min(cleaned.shape[1] - x, w_crop + 2 * margin)
        h_crop = min(cleaned.shape[0] - y, h_crop + 2 * margin)
        cropped = cleaned[y:y + h_crop, x:x + w_crop]
    else:
        cropped = cleaned

    # 10. Upscaling léger si l'image finale est trop petite (< 800px)
    final_h, final_w = cropped.shape[:2]
    if max(final_h, final_w) < 800:
        upscale_factor = 800 / max(final_h, final_w)
        cropped = cv2.resize(
            cropped,
            None,
            fx=upscale_factor,
            fy=upscale_factor,
            interpolation=cv2.INTER_CUBIC)

    # 11. Sauvegarde en PNG haute qualité
    cv2.imwrite(output_path, cropped, [cv2.IMWRITE_PNG_COMPRESSION, 0])
