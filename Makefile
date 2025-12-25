# Makefile pour UML Vision Grader Pro
# Usage: make <command>

.PHONY: help install install-dev test test-cov lint format clean run docker-build docker-run

# Aide par défaut
help:
	@echo "Commandes disponibles:"
	@echo "  make install       - Installer les dépendances"
	@echo "  make install-dev   - Installer dépendances + outils dev"
	@echo "  make test          - Lancer les tests"
	@echo "  make test-cov      - Tests avec coverage"
	@echo "  make lint          - Vérifier la qualité du code"
	@echo "  make format        - Formatter le code (black + isort)"
	@echo "  make run           - Lancer le serveur"
	@echo "  make docker-build  - Construire l'image Docker"
	@echo "  make docker-run    - Lancer avec Docker Compose"
	@echo "  make clean         - Nettoyer les fichiers temporaires"

# Installation
install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt -r requirements-dev.txt
	pip install -e .

# Tests
test:
	pytest tests/test_complete.py -v

test-cov:
	pytest tests/test_complete.py --cov=src/uml_core --cov-report=html --cov-report=term -v

# Qualité du code
lint:
	flake8 src/ tests/ --max-line-length=120 --exclude=__pycache__,.venv
	pylint src/uml_core src/webapp --disable=C0111,R0903

format:
	black src/ tests/ --line-length=120
	isort src/ tests/ --profile=black

# Serveur
run:
	python run_server.py

# Docker
docker-build:
	docker build -t uml-grader-pro:latest .

docker-run:
	docker-compose up -d

docker-stop:
	docker-compose down

docker-logs:
	docker-compose logs -f uml-grader

# Nettoyage
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache .coverage htmlcov/ dist/ build/
