# Studio Automation System Makefile

.PHONY: help install test clean lint format run-tests setup dev-install

# Default target
help:
	@echo "Studio Automation System - Available Commands:"
	@echo ""
	@echo "  install     - Install production dependencies"
	@echo "  dev-install - Install development dependencies" 
	@echo "  test        - Run test suite"
	@echo "  lint        - Run code linting"
	@echo "  format      - Format code with black"
	@echo "  clean       - Clean up temporary files"
	@echo "  setup       - Initial project setup"
	@echo "  status      - Check studio status"
	@echo "  start-yoga  - Start yoga class session"
	@echo "  stop        - Stop current session"
	@echo ""

# Installation targets
install:
	pip install -r requirements.txt

dev-install: install
	pip install pytest pytest-cov black flake8

setup: dev-install
	@echo "Creating necessary directories..."
	mkdir -p recordings exports temp backups logs
	@echo "Setup complete!"
	@echo "Edit config/studio_config.yaml to match your equipment"

# Development targets
test:
	python -m pytest tests/ -v

test-coverage:
	python -m pytest tests/ --cov=src --cov-report=html --cov-report=term

lint:
	flake8 src/ scripts/ tests/ --max-line-length=100

format:
	black src/ scripts/ tests/ --line-length=100

# Cleaning
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/

# Studio operations
status:
	python scripts/studio_status.py

start-yoga:
	python scripts/start_session.py yoga_class

start-meditation:
	python scripts/start_session.py meditation

start-workshop:
	python scripts/start_session.py workshop

stop:
	python scripts/stop_session.py

# Development workflow
check: lint test
	@echo "All checks passed!"

# Docker targets (optional)
docker-build:
	docker build -t studio-automation .

docker-run:
	docker run -it --rm \
		-v $(PWD)/recordings:/app/recordings \
		-v $(PWD)/config:/app/config \
		studio-automation

# Quick development setup
dev-setup: dev-install
	@echo "Running initial tests..."
	python -m pytest tests/ -v
	@echo "Development environment ready!"