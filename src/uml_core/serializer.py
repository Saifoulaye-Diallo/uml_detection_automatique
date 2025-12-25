# JSON serialization/deserialization for UMLDiagram
import json
from .models import UMLDiagram


def diagram_to_json(diagram: UMLDiagram) -> str:
    return json.dumps(diagram.to_dict(), indent=2, ensure_ascii=False)


def diagram_from_json(json_str: str) -> UMLDiagram:
    data = json.loads(json_str)
    return UMLDiagram.from_dict(data)
