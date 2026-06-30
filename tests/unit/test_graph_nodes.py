"""Unit tests for ADK graph workflow nodes."""

import asyncio
from unittest.mock import MagicMock, patch

import pytest

from src.agentic_layer.graph.nodes import (
    finalize_output,
    initialize_workflow,
    route_escalation,
    run_validation_pipeline,
)


async def _run_node(node, ctx, node_input=None):
    events = []
    async for event in node.run(ctx=ctx, node_input=node_input):
        events.append(event)
    return events


def _ctx(state: dict | None = None) -> MagicMock:
    ctx = MagicMock()
    ctx.state = dict(state or {})
    return ctx


@pytest.mark.parametrize(
    ("decision", "expected_route"),
    [
        ("human", "human"),
        ("learner", "learner"),
        ("none", "none"),
        (None, "none"),
    ],
)
def test_route_escalation_branches(decision, expected_route):
    ctx = _ctx({"escalation_decision": decision})

    events = asyncio.run(_run_node(route_escalation, ctx))

    assert events[0].actions.route == expected_route


def test_initialize_workflow_requires_query_url():
    ctx = _ctx({"server_key": "hapi"})

    asyncio.run(_run_node(initialize_workflow, ctx))

    assert ctx.state["workflow_error"] == "query_url is required"


def test_initialize_workflow_accepts_valid_request():
    ctx = _ctx({"query_url": "Patient?gender=male", "server_key": "hapi"})

    asyncio.run(_run_node(initialize_workflow, ctx))

    assert not ctx.state.get("workflow_error")


def test_run_validation_pipeline_skips_when_workflow_error_set():
    ctx = _ctx({
        "query_url": "Patient?gender=male",
        "workflow_error": "blocked",
    })

    with patch("src.agentic_layer.graph.nodes.execute_workflow") as mock_execute:
        asyncio.run(_run_node(run_validation_pipeline, ctx))
        mock_execute.assert_not_called()


@patch("src.agentic_layer.graph.nodes.execute_workflow")
def test_run_validation_pipeline_delegates_to_engine(mock_execute):
    mock_execute.return_value = MagicMock(
        model_dump=lambda: {
            "query_url": "Patient?gender=male",
            "server_key": "hapi",
            "validation_result": {"valid": True, "errors": [], "warnings": []},
            "execution_result": {"executed": False},
            "final_output": {"valid": True, "executed": False},
        }
    )
    ctx = _ctx({
        "query_url": "Patient?gender=male",
        "server_key": "hapi",
        "mode": "validate_only",
    })

    asyncio.run(_run_node(run_validation_pipeline, ctx))

    mock_execute.assert_called_once()
    assert ctx.state["final_output"]["valid"] is True


def test_finalize_output_builds_contract_when_missing():
    ctx = _ctx({
        "server_key": "hapi",
        "validation_result": {"valid": True, "errors": [], "warnings": []},
        "execution_result": {"executed": False},
    })

    asyncio.run(_run_node(finalize_output, ctx))

    assert ctx.state["final_output"]["valid"] is True
    assert ctx.state["final_output"]["server_used"] == "hapi"


def test_finalize_output_preserves_existing_payload():
    existing = {"valid": False, "errors": ["already set"], "executed": False}
    ctx = _ctx({"server_key": "hapi", "final_output": existing})

    asyncio.run(_run_node(finalize_output, ctx))

    assert ctx.state["final_output"] == existing