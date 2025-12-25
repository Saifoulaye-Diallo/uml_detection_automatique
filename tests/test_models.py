"""Test unitaire pour les modèles UML.

Ce module teste la sérialisation et désérialisation des modèles UML.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from uml_core.models import UMLAttribute, UMLOperation, UMLClass, UMLRelationship
from uml_core.logger import logger


def test_attribute_serialization():
    """Test de sérialisation/désérialisation d'un attribut."""
    attr = UMLAttribute(name="age", type="int")
    data = attr.to_dict()
    
    assert data == {"name": "age", "type": "int"}
    
    attr2 = UMLAttribute.from_dict(data)
    assert attr2.name == "age"
    assert attr2.type == "int"
    logger.info("[OK] test_attribute_serialization passed")


def test_operation_serialization():
    """Test de sérialisation/désérialisation d'une opération."""
    op = UMLOperation(
        name="setAge",
        parameters=[{"name": "newAge", "type": "int"}],
        return_type="void"
    )
    data = op.to_dict()
    
    assert data["name"] == "setAge"
    assert len(data["parameters"]) == 1
    assert data["return_type"] == "void"
    
    op2 = UMLOperation.from_dict(data)
    assert op2.name == "setAge"
    assert op2.return_type == "void"
    logger.info("[OK] test_operation_serialization passed")


def test_class_serialization():
    """Test de sérialisation/désérialisation d'une classe."""
    cls = UMLClass(
        name="Person",
        attributes=[UMLAttribute("name", "String")],
        operations=[UMLOperation("getName", [], "String")]
    )
    data = cls.to_dict()
    
    assert data["name"] == "Person"
    assert len(data["attributes"]) == 1
    assert len(data["operations"]) == 1
    
    cls2 = UMLClass.from_dict(data)
    assert cls2.name == "Person"
    assert len(cls2.attributes) == 1
    logger.info("[OK] test_class_serialization passed")


def test_relationship_serialization():
    """Test de sérialisation/désérialisation d'une relation."""
    rel = UMLRelationship(
        source="Student",
        target="Person",
        type="inheritance",
        source_multiplicity="",
        target_multiplicity=""
    )
    data = rel.to_dict()
    
    assert data["source"] == "Student"
    assert data["target"] == "Person"
    assert data["type"] == "inheritance"
    
    rel2 = UMLRelationship.from_dict(data)
    assert rel2.source == "Student"
    assert rel2.type == "inheritance"
    logger.info("[OK] test_relationship_serialization passed")


if __name__ == "__main__":
    test_attribute_serialization()
    test_operation_serialization()
    test_class_serialization()
    test_relationship_serialization()
    logger.info("\nTous les tests sont passés avec succès!")
