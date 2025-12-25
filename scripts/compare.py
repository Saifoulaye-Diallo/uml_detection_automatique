"""Script CLI pour comparer un diagramme UML image avec un JSON de référence.

Ce script en ligne de commande utilise GPT-4o Vision pour :
1. Extraire les éléments UML depuis l'image
2. Comparer avec le JSON de référence
3. Générer un fichier diff.json avec les différences

Usage:
    python compare_image.py --student student.png --reference solution.json
    python compare_image.py --student diagram.jpg --reference ref.json --diff output.json

Author: UML Vision Grader Pro
Version: 2.0
Date: 2025
"""

import sys
import os
import json
import argparse

# Ajouter le dossier src au PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from uml_core.vision_llm_client import extract_uml_json_from_image
from uml_core.logger import logger


def main():
    """Point d'entrée principal du script CLI."""
    parser = argparse.ArgumentParser(
        description="Compare un diagramme UML (image) à une solution de référence (JSON).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  python compare_image.py --student student.png --reference solution.json
  python compare_image.py --student diagram.jpg --reference ref.json --diff my_diff.json

Le fichier de sortie contiendra les différences détaillées :
  - Classes manquantes/en trop
  - Attributs manquants/en trop
  - Opérations manquantes/en trop
  - Relations manquantes/en trop
  - Multiplicités incorrectes
  - Problèmes de nommage
        """
    )
    parser.add_argument(
        '--student',
        required=True,
        help='Fichier image du diagramme UML de l\'étudiant (PNG/JPG)'
    )
    parser.add_argument(
        '--reference',
        required=True,
        help='Fichier JSON de la solution de référence'
    )
    parser.add_argument(
        '--diff',
        default='diff.json',
        help='Fichier de sortie pour les différences (défaut: diff.json)'
    )
    
    args = parser.parse_args()

    # Vérification de l'existence des fichiers
    if not os.path.exists(args.student):
        logger.error(f"Le fichier '{args.student}' n'existe pas.")
        sys.exit(1)
    
    if not os.path.exists(args.reference):
        logger.error(f"Le fichier '{args.reference}' n'existe pas.")
        sys.exit(1)

    logger.info(f"Chargement de la référence depuis '{args.reference}'...")
    with open(args.reference, encoding='utf-8') as f:
        ref_json = f.read()

    logger.info(f"Analyse de l'image '{args.student}' avec GPT-4o Vision...")
    logger.info("Cela peut prendre 15-30 secondes...")
    
    try:
        diff = extract_uml_json_from_image(args.student, reference_json=ref_json)
    except Exception as e:
        logger.error(f"Erreur lors de l'analyse : {e}")
        sys.exit(1)

    logger.info(f"Écriture du rapport dans '{args.diff}'...")
    with open(args.diff, 'w', encoding='utf-8') as f:
        json.dump(diff, f, indent=2, ensure_ascii=False)
    
    # Résumé des différences
    total_errors = sum([
        len(diff.get('missing_classes', [])),
        len(diff.get('extra_classes', [])),
        len(diff.get('missing_attributes', [])),
        len(diff.get('extra_attributes', [])),
        len(diff.get('missing_operations', [])),
        len(diff.get('extra_operations', [])),
        len(diff.get('missing_relationships', [])),
        len(diff.get('extra_relationships', [])),
        len(diff.get('incorrect_multiplicities', [])),
    ])
    
    logger.info("="*60)
    logger.info(f"Analyse terminée ! Total d'erreurs détectées : {total_errors}")
    logger.info("="*60)
    logger.info(f"Rapport détaillé : {args.diff}")
    
    if total_errors == 0:
        logger.info("Parfait ! Aucune différence détectée.")
    else:
        logger.warning(f"{total_errors} différence(s) trouvée(s). Consultez le fichier diff.json.")


if __name__ == "__main__":
    main()

