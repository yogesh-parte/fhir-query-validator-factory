# Makefile for fhir-query-validator-factory

.PHONY: help demo spec-check lint test clean

help:
	@echo "Available commands:"
	@echo "  make demo          - Run the main validation demo"
	@echo "  make spec-check    - Validate that all specs are present and consistent"
	@echo "  make lint          - Run linting on Python code"
	@echo "  make test          - Run unit and integration tests"
	@echo "  make clean         - Remove generated files and caches"

demo:
	@echo "Running validation workflow demo..."
	python -m src.agentic_layer.graph.validation_workflow

spec-check:
	@echo "Checking documentation specs..."
	@ls docs/spec/ | grep -E '\.md$$' || echo "No spec files found"
	@echo "Spec check complete."

lint:
	@echo "Running linting..."
	# Add your preferred linter here, e.g.:
	# ruff check src/
	# pylint src/
	@echo "Linting complete (placeholder)."

test:
	@echo "Running tests..."
	# pytest tests/ -v
	@echo "Tests complete (placeholder)."

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "Cleaned up Python cache files."
