import pytest
from src.agentic_layer.agents.query_validator import QueryValidatorAgent


def test_valid_query():
    validator = QueryValidatorAgent()
    result = validator.validate(
        query_url="Patient?gender=male",
        interpreted_capability={"supported_resources": {"Patient": {}}},
        user_id="test-user"
    )
    assert result["valid"] is True


def test_pattern_detection():
    validator = QueryValidatorAgent()
    user = "test-user-pattern"
    
    # Simulate multiple invalid queries
    for _ in range(3):
        result = validator.validate(
            query_url="Patient?invalid=true",
            interpreted_capability={},
            user_id=user
        )
    
    assert result.get("pattern_detected") is True
