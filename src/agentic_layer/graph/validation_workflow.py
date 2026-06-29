"""
validation_workflow.py
Google ADK graph workflow for FHIR query validation with loop engineering.
"""

from __future__ import annotations

from typing import Any, Literal, Optional, TypedDict

from google.adk import Workflow

from ..state.workflow_state import ValidationWorkflowState
from .nodes import finalize_output, initialize_workflow, run_validation_pipeline
from .workflow_engine import execute_workflow


class ValidationState(TypedDict, total=False):
    """Legacy TypedDict kept for backward-compatible demo scripts and tests."""

    query_url: str
    server_key: Optional[str]
    user_id: Optional[str]
    auth_token: Optional[str]
    mode: Literal["validate_only", "validate_and_execute"]

    capability_statement: dict[str, Any]
    interpreted_capability: dict[str, Any]
    validation_result: dict[str, Any]
    execution_result: dict[str, Any]

    pattern_detected: bool
    escalation_decision: Optional[str]
    learner_guidance: dict[str, Any]
    human_review: dict[str, Any]

    final_output: dict[str, Any]


# ADK 2.0 graph workflow — runnable via `adk run` / `adk web` / agents-cli.
root_agent = Workflow(
    name="fhir_query_validator",
    description=(
        "Validates FHIR search queries against CapabilityStatement, executes valid "
        "queries, detects error patterns, and escalates to learner or human agents."
    ),
    state_schema=ValidationWorkflowState,
    edges=[
        ("START", initialize_workflow, run_validation_pipeline, finalize_output),
    ],
)


def run_validation_workflow(state: ValidationState) -> ValidationState:
    """
    Synchronous workflow entry point for demos, scripts, and tests.
    Delegates to the shared workflow engine used by ADK graph nodes.
    """
    result = execute_workflow(dict(state))
    return result.model_dump()  # type: ignore[return-value]