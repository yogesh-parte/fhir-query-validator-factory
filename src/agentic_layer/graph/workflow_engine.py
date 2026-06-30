"""
Core validation workflow engine shared by ADK graph nodes and legacy runner.
"""

from __future__ import annotations

from typing import Any, Optional

import httpx

from ..agents import (
    CacheAgent,
    CapabilityInterpreterAgent,
    HumanInterventionGate,
    QueryExecutionAgent,
    QueryValidatorAgent,
    RuleAgent,
    SearchLearnerAgent,
)
from ..config.settings import DEFAULT_SERVERS, get_auth_headers, get_server_config
from ..exceptions import AuthenticationRequiredError, CapabilityFetchError, UnknownServerKeyError
from ..state.workflow_state import ValidationWorkflowState
from ..utils.audit_log import AuditLog

# Shared singletons preserve cross-request pattern history in demos/tests.
_audit_log = AuditLog()
cache_agent = CacheAgent()
interpreter = CapabilityInterpreterAgent()
validator = QueryValidatorAgent()
executor = QueryExecutionAgent()
rule_agent = RuleAgent(audit_log=_audit_log)
learner_agent = SearchLearnerAgent()
human_gate = HumanInterventionGate(audit_log=_audit_log)


def build_final_output(state: ValidationWorkflowState) -> dict[str, Any]:
    """Align final output with query-validation-spec JSON contract."""
    validation = state.validation_result or {}
    execution = state.execution_result or {}
    executed = bool(execution.get("executed")) and execution.get("status") == "success"

    return {
        "valid": validation.get("valid", False),
        "server_used": state.server_key,
        "errors": validation.get("errors", []),
        "warnings": validation.get("warnings", []),
        "executed": executed,
        "results": execution if executed else None,
        "pattern_detected": state.pattern_detected,
        "escalation": state.escalation_decision,
        "guidance": state.learner_guidance or None,
        "human_review_required": bool(state.human_review),
        "human_review": state.human_review or None,
    }


def execute_workflow(initial: dict[str, Any]) -> ValidationWorkflowState:
    """Run the full validation workflow synchronously."""
    state = ValidationWorkflowState.model_validate(initial)

    if state.user_id and human_gate.is_paused(state.user_id):
        state.workflow_error = f"User '{state.user_id}' is paused pending human review."
        state.final_output = {
            "valid": False,
            "server_used": state.server_key,
            "errors": [state.workflow_error],
            "warnings": [],
            "executed": False,
            "results": None,
        }
        return state

    try:
        server = get_server_config(state.server_key)
    except UnknownServerKeyError as exc:
        state.workflow_error = str(exc)
        state.validation_result = {
            "valid": False,
            "errors": [str(exc)],
            "warnings": [],
            "error_types": ["unknown_server"],
            "pattern_detected": False,
        }
        state.final_output = build_final_output(state)
        return state

    auth_headers = get_auth_headers(server, auth_token_override=state.auth_token)
    if server.requires_auth and not auth_headers:
        env_hint = DEFAULT_SERVERS.get(server.key, {}).get("auth_token_env")
        hint = (
            f" Set {env_hint} in .env.local (git-ignored) or pass auth_token at runtime."
            if env_hint
            else " Provide credentials via .env.local or auth_token at runtime."
        )
        message = (
            f"Authentication required for server '{server.key}' but no credentials were provided."
            + hint
        )
        state.workflow_error = message
        state.validation_result = {
            "valid": False,
            "errors": [message],
            "warnings": [],
            "error_types": ["authentication_required"],
            "pattern_detected": False,
        }
        state.final_output = build_final_output(state)
        return state

    print("\n=== [LOOP] Cache Invalidation Loop ===")
    try:
        state.capability_statement = cache_agent.get_capability_statement(
            state.server_key,
            auth_token=state.auth_token,
        )
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code in {401, 403}:
            raise AuthenticationRequiredError(str(exc)) from exc
        raise CapabilityFetchError(str(exc)) from exc
    except httpx.RequestError as exc:
        raise CapabilityFetchError(str(exc)) from exc

    state.interpreted_capability = interpreter.interpret(state.capability_statement)

    print("\n=== [LOOP] Validation + Pattern Detection ===")
    state.validation_result = validator.validate(
        query_url=state.query_url,
        interpreted_capability=state.interpreted_capability,
        user_id=state.user_id,
        server_key=state.server_key,
    )
    state.pattern_detected = state.validation_result.get("pattern_detected", False)

    if state.validation_result.get("valid") and state.mode == "validate_and_execute":
        print("\n=== [LOOP] Validation → Execution Loop ===")
        state.execution_result = executor.execute(
            query_url=state.query_url,
            server_key=state.server_key,
            auth_token=state.auth_token,
        )
    else:
        state.execution_result = {"executed": False}

    print("\n=== [LOOP] Pattern Detection → Learning / Human Escalation ===")
    if state.pattern_detected:
        decision, audit = rule_agent.decide_escalation(
            pattern_detected=True,
            validation_result=state.validation_result,
            user_id=state.user_id,
            server_key=state.server_key,
        )
        state.escalation_decision = decision
        state.escalation_audit = audit

        if decision == "learner":
            state.learner_guidance = learner_agent.provide_guidance(
                query_url=state.query_url,
                validation_result=state.validation_result,
                interpreted_capability=state.interpreted_capability,
            )
        elif decision == "human":
            state.human_review = human_gate.request_human_review({
                "query_url": state.query_url,
                "user_id": state.user_id,
                "server_key": state.server_key,
                "validation_result": state.validation_result,
            })
    else:
        state.escalation_decision = "none"

    state.final_output = build_final_output(state)
    return state