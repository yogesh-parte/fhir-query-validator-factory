"""
Integration test for the full validation workflow.
"""

import pytest
from src.agentic_layer.graph.validation_workflow import run_validation_workflow


def test_full_workflow_with_valid_query():
    state = {
        "query_url": "Patient?gender=male",
        "server_key": "hapi",
        "user_id": "integration-test",
        "mode": "validate_and_execute"
    }
    
    result = run_validation_workflow(state)
    
    assert result["final_output"]["valid"] is True
    assert "execution" in result["final_output"]
