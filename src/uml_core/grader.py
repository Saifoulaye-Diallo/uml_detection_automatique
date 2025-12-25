"""Module de notation pour les diagrammes UML.

Calcule un score académique basé sur les différences détectées,
avec pondération par type d'erreur et calcul de note sur 20.
"""

from typing import Dict, List


class UMLGrader:
    """Calculateur de notes pour diagrammes UML."""
    
    # Poids des erreurs (points perdus par erreur)
    WEIGHTS = {
        "missing_class": 2.0,           # Classe manquante = -2 pts
        "extra_class": 1.5,             # Classe en trop = -1.5 pts
        "missing_attribute": 0.5,       # Attribut manquant = -0.5 pts
        "extra_attribute": 0.3,         # Attribut en trop = -0.3 pts
        "missing_operation": 0.5,       # Opération manquante = -0.5 pts
        "extra_operation": 0.3,         # Opération en trop = -0.3 pts
        "missing_relationship": 1.5,    # Relation manquante = -1.5 pts
        "extra_relationship": 1.0,      # Relation en trop = -1 pts
        "incorrect_multiplicity": 0.5,  # Multiplicité incorrecte = -0.5 pts
        "naming_issue": 0.2,            # Problème de nommage = -0.2 pts
    }
    
    @staticmethod
    def calculate_score(diff: Dict, max_score: float = 20.0) -> Dict:
        """Calcule la note et les détails à partir du diff JSON.
        
        Args:
            diff (Dict): Dictionnaire des différences (output du LLM)
            max_score (float): Note maximale (défaut: 20.0)
        
        Returns:
            Dict: {
                "score": 15.5,
                "max_score": 20.0,
                "percentage": 77.5,
                "grade": "B+",
                "points_lost": 4.5,
                "error_breakdown": {...},
                "feedback": "..."
            }
        """
        points_lost = 0.0
        error_breakdown = {}
        
        # Calcul des points perdus par catégorie
        for key, weight in UMLGrader.WEIGHTS.items():
            # Convertir le nom de la clé (missing_class → missing_classes)
            diff_key = key + "es" if not key.endswith("y") else key.replace("y", "ies")
            if diff_key == "missing_class":
                diff_key = "missing_classes"
            elif diff_key == "extra_class":
                diff_key = "extra_classes"
            elif diff_key == "incorrect_multiplicity":
                diff_key = "incorrect_multiplicities"
            elif diff_key == "naming_issue":
                diff_key = "naming_issues"
            
            count = len(diff.get(diff_key, []))
            category_loss = count * weight
            points_lost += category_loss
            
            if count > 0:
                error_breakdown[diff_key] = {
                    "count": count,
                    "weight": weight,
                    "points_lost": round(category_loss, 2)
                }
        
        # Limiter la perte à max_score (ne pas descendre en dessous de 0)
        points_lost = min(points_lost, max_score)
        
        # Calcul du score final
        score = max(0, max_score - points_lost)
        percentage = (score / max_score) * 100
        
        # Détermination de la mention
        grade = UMLGrader._get_grade_letter(percentage)
        
        # Feedback textuel
        feedback = UMLGrader._generate_feedback(diff, score, max_score)
        
        return {
            "score": round(score, 2),
            "max_score": max_score,
            "percentage": round(percentage, 1),
            "grade": grade,
            "points_lost": round(points_lost, 2),
            "error_breakdown": error_breakdown,
            "feedback": feedback,
            "total_errors": sum(len(v) for v in diff.values() if isinstance(v, list))
        }
    
    @staticmethod
    def _get_grade_letter(percentage: float) -> str:
        """Convertit un pourcentage en mention."""
        if percentage >= 90:
            return "A+"
        elif percentage >= 85:
            return "A"
        elif percentage >= 80:
            return "A-"
        elif percentage >= 75:
            return "B+"
        elif percentage >= 70:
            return "B"
        elif percentage >= 65:
            return "B-"
        elif percentage >= 60:
            return "C+"
        elif percentage >= 55:
            return "C"
        elif percentage >= 50:
            return "C-"
        elif percentage >= 40:
            return "D"
        else:
            return "F"
    
    @staticmethod
    def _generate_feedback(diff: Dict, score: float, max_score: float) -> str:
        """Génère un feedback textuel personnalisé."""
        total_errors = sum(len(v) for v in diff.values() if isinstance(v, list))
        
        if total_errors == 0:
            return "🎉 Parfait ! Diagramme UML totalement conforme à la solution."
        
        feedback_parts = []
        
        # Feedback par catégorie
        if diff.get("missing_classes"):
            feedback_parts.append(
                f"[X] {len(diff['missing_classes'])} classe(s) manquante(s): "
                f"{', '.join(diff['missing_classes'][:3])}"
            )
        
        if diff.get("extra_classes"):
            feedback_parts.append(
                f"[+] {len(diff['extra_classes'])} classe(s) en trop: "
                f"{', '.join(diff['extra_classes'][:3])}"
            )
        
        if diff.get("missing_relationships"):
            feedback_parts.append(
                f"[~] {len(diff['missing_relationships'])} relation(s) manquante(s)"
            )
        
        if diff.get("incorrect_multiplicities"):
            feedback_parts.append(
                f"[#] {len(diff['incorrect_multiplicities'])} multiplicité(s) incorrecte(s)"
            )
        
        # Message global
        percentage = (score / max_score) * 100
        if percentage >= 80:
            intro = "[OK] Très bon travail !"
        elif percentage >= 60:
            intro = "Bon travail, quelques améliorations à apporter."
        elif percentage >= 40:
            intro = "[!] Travail à revoir, plusieurs erreurs importantes."
        else:
            intro = "[X] Travail insuffisant, révision complète nécessaire."
        
        return intro + " " + " ".join(feedback_parts[:4])


# Fonction utilitaire pour l'API
def grade_uml_diff(diff: Dict, max_score: float = 20.0) -> Dict:
    """Fonction helper pour noter un diff JSON.
    
    Args:
        diff (Dict): Résultat de extract_uml_json_from_image()
        max_score (float): Note maximale
    
    Returns:
        Dict: Résultat de notation complet
    """
    return UMLGrader.calculate_score(diff, max_score)
