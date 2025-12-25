"""Configuration pytest pour les tests.

Ce fichier configure le PYTHONPATH avant la collection des tests.
"""

import sys
import os

# Ajouter src/ au PYTHONPATH avant la collection des tests
src_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', 'src')
)
if src_path not in sys.path:
    sys.path.insert(0, src_path)
