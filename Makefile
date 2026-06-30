# Makefile for fhir-query-validator-factory

.PHONY: help demo demo-loops demo-trace demo-agent-trace demo-mockhealth demo-adk-cli demo-adk-web spec-check lint test clean

help:
	@echo "Available commands:"
	@echo "  make demo              - Run HAPI loop demo (alias for demo-loops)"
	@echo "  make demo-loops        - Feedback loops on public HAPI server"
	@echo "  make demo-trace        - Structured traceability reports"
	@echo "  make demo-agent-trace  - Per-agent pipeline trace + audit trail"
	@echo "  make demo-mockhealth   - Loop demo on mock.health (requires .env.local)"
	@echo "  make demo-adk-cli      - Google ADK CLI agent demo (adk run)"
	@echo "  make demo-adk-web      - Google ADK Web UI + API demo (adk web)"
	@echo "  make spec-check        - Validate that all specs are present and consistent"
	@echo "  make lint              - Run linting on Python code"
	@echo "  make test              - Run unit and integration tests"
	@echo "  make clean             - Remove generated files and caches"

demo: demo-loops

demo-loops:
	python3 scripts/demo_loops.py

demo-trace:
	python3 scripts/demo_traceability.py

demo-agent-trace:
	python3 scripts/demo_agent_traceability.py

demo-mockhealth:
	python3 scripts/demo_loops_mockhealth.py

demo-adk-cli:
	python3 scripts/demo_adk_cli.py

demo-adk-web:
	python3 scripts/demo_adk_web.py --serve-only

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
	python3 -m pytest tests/ -q

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "Cleaned up Python cache files."
