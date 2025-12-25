"""Modèles de données pour les diagrammes UML de classes.

Ce module définit les structures de données pour représenter les éléments
d'un diagramme UML de classes : attributs, opérations, classes et relations.

Author: UML Vision Grader Pro
Version: 1.0
Date: 2025
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict


@dataclass
class UMLAttribute:
    """Représente un attribut d'une classe UML.

    Attributes:
        name (str): Nom de l'attribut (ex: 'age', 'studentId')
        type (str): Type de l'attribut (ex: 'int', 'String', 'Date')

    Example:
        >>> attr = UMLAttribute(name='age', type='int')
        >>> attr.to_dict()
        {'name': 'age', 'type': 'int'}
    """
    name: str
    type: str

    def to_dict(self):
        return {"name": self.name, "type": self.type}

    @staticmethod
    def from_dict(data):
        return UMLAttribute(name=data["name"], type=data["type"])


@dataclass
class UMLOperation:
    """Représente une opération (méthode) d'une classe UML.

    Attributes:
        name (str): Nom de l'opération
        parameters (List[Dict[str, str]]): Paramètres avec name et type
        return_type (Optional[str]): Type de retour de l'opération

    Example:
        >>> op = UMLOperation(
        ...     name='setAge',
        ...     parameters=[{'name': 'age', 'type': 'int'}],
        ...     return_type='void'
        ... )
    """
    name: str
    parameters: List[Dict[str, str]] = field(default_factory=list)
    return_type: Optional[str] = None

    def to_dict(self):
        return {
            "name": self.name,
            "parameters": self.parameters,
            "return_type": self.return_type,
        }

    @staticmethod
    def from_dict(data):
        return UMLOperation(
            name=data["name"],
            parameters=data.get("parameters", []),
            return_type=data.get("return_type"),
        )


@dataclass
class UMLClass:
    """Représente une classe UML complète.

    Attributes:
        name (str): Nom de la classe (ex: 'Person', 'Student')
        attributes (List[UMLAttribute]): Liste des attributs de la classe
        operations (List[UMLOperation]): Liste des opérations/méthodes

    Example:
        >>> cls = UMLClass(
        ...     name='Person',
        ...     attributes=[UMLAttribute('name', 'String')],
        ...     operations=[UMLOperation('getName', [], 'String')]
        ... )
    """
    name: str
    attributes: List[UMLAttribute] = field(default_factory=list)
    operations: List[UMLOperation] = field(default_factory=list)

    def to_dict(self):
        return {
            "name": self.name,
            "attributes": [a.to_dict() for a in self.attributes],
            "operations": [o.to_dict() for o in self.operations],
        }

    @staticmethod
    def from_dict(data):
        def parse_attribute(a):
            if isinstance(a, dict):
                return UMLAttribute.from_dict(a)
            elif isinstance(a, str):
                # Format attendu : "name: type"
                if ':' in a:
                    name, type_ = a.split(':', 1)
                    return UMLAttribute(name=name.strip(), type=type_.strip())
                else:
                    return UMLAttribute(name=a.strip(), type="?")
            else:
                raise ValueError(f"Attribut inattendu: {a}")

        def parse_operation(o):
            if isinstance(o, dict):
                return UMLOperation.from_dict(o)
            elif isinstance(o, str):
                # Format attendu : "name(params) : return_type"
                import re
                m = re.match(r"(\w+)\(([^)]*)\)\s*:\s*(\w+)", o)
                if m:
                    name, params, return_type = m.groups()
                    param_list = []
                    if params.strip():
                        for p in params.split(','):
                            if ':' in p:
                                pname, ptype = p.split(':', 1)
                                param_list.append(
                                    {
                                        "name": pname.strip(),
                                        "type": ptype.strip()
                                    }
                                )
                            else:
                                param_list.append(
                                    {"name": p.strip(), "type": "?"})
                    return UMLOperation(
                        name=name.strip(),
                        parameters=param_list,
                        return_type=return_type.strip())
                else:
                    return UMLOperation(name=o.strip())
            else:
                raise ValueError(f"Opération inattendue: {o}")

        return UMLClass(
            name=data["name"], attributes=[
                parse_attribute(a) for a in data.get(
                    "attributes", [])], operations=[
                parse_operation(o) for o in data.get(
                    "operations", [])], )


@dataclass
class UMLRelationship:
    type: str  # association, composition, inheritance, etc.
    from_class: str
    to_class: str
    multiplicity_from: Optional[str] = None
    multiplicity_to: Optional[str] = None

    def to_dict(self):
        return {
            "type": self.type,
            "from": self.from_class,
            "to": self.to_class,
            "multiplicity_from": self.multiplicity_from,
            "multiplicity_to": self.multiplicity_to,
        }

    @staticmethod
    def from_dict(data):
        # Supporte 'from'/'to' ou 'source'/'target' (auto-fix LLM)
        from_class = data.get("from") or data.get("source")
        to_class = data.get("to") or data.get("target")
        multiplicity_from = data.get(
            "multiplicity_from") or data.get("multiplicitySource")
        multiplicity_to = data.get(
            "multiplicity_to") or data.get("multiplicityTarget")
        return UMLRelationship(
            type=data["type"],
            from_class=from_class,
            to_class=to_class,
            multiplicity_from=multiplicity_from,
            multiplicity_to=multiplicity_to,
        )


@dataclass
class UMLDiagram:
    classes: List[UMLClass] = field(default_factory=list)
    relationships: List[UMLRelationship] = field(default_factory=list)

    def to_dict(self):
        return {
            "classes": [c.to_dict() for c in self.classes],
            "relationships": [r.to_dict() for r in self.relationships],
        }

    @staticmethod
    def from_dict(data):
        return UMLDiagram(
            classes=[
                UMLClass.from_dict(c) for c in data.get(
                    "classes", [])], relationships=[
                UMLRelationship.from_dict(r) for r in data.get(
                    "relationships", [])], )
