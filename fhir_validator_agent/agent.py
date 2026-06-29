"""
ADK / agents-cli entry point for the FHIR Query Validator Factory.

Run with:
  adk web --port 8080          # from repo root (parent of this package)
  adk run fhir_validator_agent
  agents-cli playground        # when scaffolded via agents-cli
"""

from src.agentic_layer.graph.validation_workflow import root_agent

__all__ = ["root_agent"]