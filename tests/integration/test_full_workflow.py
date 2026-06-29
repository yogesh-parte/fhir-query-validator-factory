"""
Integration tests for the full validation workflow.
"""

from unittest.mock import MagicMock, patch

import pytest

from src.agentic_layer.exceptions import UnknownServerKeyError
from src.agentic_layer.graph.validation_workflow import run_validation_workflow


CAPABILITY = {
    "resourceType": "CapabilityStatement",
    "rest": [{
        "resource": [{
            "type": "Patient",
            "searchParam": [{"name": "gender", "type": "token"}],
        }],
    }],
}


def _mock_response(status_code: int, json_data: dict | None = None):
    response = MagicMock()
    response.status_code = status_code
    response.json.return_value = json_data or {}
    response.headers = {"ETag": 'W/"etag-1"'}
    response.raise_for_status = MagicMock()
    return response


@patch("src.agentic_layer.graph.workflow_engine.executor.execute")
@patch("src.agentic_layer.graph.workflow_engine.cache_agent.get_capability_statement")
def test_full_workflow_with_valid_query(mock_get_capability, mock_execute):
    mock_get_capability.return_value = CAPABILITY
    mock_execute.return_value = {
        "executed": True,
        "status": "success",
        "http_status": 200,
        "elapsed_ms": 12.5,
        "bundle_type": "searchset",
        "total": 2,
        "resource_type": "Bundle",
    }

    state = {
        "query_url": "Patient?gender=male",
        "server_key": "hapi",
        "user_id": "integration-test",
        "mode": "validate_and_execute",
    }

    result = run_validation_workflow(state)

    output = result["final_output"]
    assert output["valid"] is True
    assert output["server_used"] == "hapi"
    assert output["executed"] is True
    assert output["results"]["total"] == 2


@patch("src.agentic_layer.agents.cache_agent.httpx.Client")
def test_full_workflow_human_escalation(mock_cache_client):
    cache_http = MagicMock()
    cache_http.__enter__.return_value = cache_http
    cache_http.get.return_value = _mock_response(200, CAPABILITY)
    mock_cache_client.return_value = cache_http

    user = "integration-human-user"
    for _ in range(5):
        result = run_validation_workflow({
            "query_url": "Patient?invalid_param=true",
            "server_key": "hapi",
            "user_id": user,
            "mode": "validate_only",
        })

    assert result["final_output"]["valid"] is False
    assert result["final_output"]["escalation"] == "human"
    assert result["final_output"]["human_review_required"] is True


def test_unknown_server_key_returns_error():
    result = run_validation_workflow({
        "query_url": "Patient?gender=male",
        "server_key": "does-not-exist",
        "mode": "validate_only",
    })
    assert result["final_output"]["valid"] is False
    assert "Unknown server_key" in result["final_output"]["errors"][0]