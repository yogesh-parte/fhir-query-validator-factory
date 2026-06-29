import pytest

from src.agentic_layer.agents.query_validator import QueryValidatorAgent


PATIENT_CAPABILITY = {
    "supported_resources": {
        "Patient": {
            "search_params": [
                {"name": "gender", "type": "token", "modifiers": ["exact", "missing"], "comparators": []},
                {"name": "birthdate", "type": "date", "modifiers": ["missing"], "comparators": ["gt", "lt"]},
            ]
        }
    }
}


def test_valid_query():
    validator = QueryValidatorAgent()
    result = validator.validate(
        query_url="Patient?gender=male",
        interpreted_capability=PATIENT_CAPABILITY,
        user_id="test-user",
        server_key="hapi",
    )
    assert result["valid"] is True


def test_invalid_parameter():
    validator = QueryValidatorAgent()
    result = validator.validate(
        query_url="Patient?invalid=true",
        interpreted_capability=PATIENT_CAPABILITY,
        user_id="test-user",
        server_key="hapi",
    )
    assert result["valid"] is False
    assert "unknown_parameter" in result["error_types"]


def test_unsupported_modifier():
    validator = QueryValidatorAgent()
    result = validator.validate(
        query_url="Patient?gender:text=smith",
        interpreted_capability=PATIENT_CAPABILITY,
        user_id="test-user",
        server_key="hapi",
    )
    assert result["valid"] is False
    assert "unsupported_modifier" in result["error_types"]


def test_pattern_detection_per_user_and_server():
    validator = QueryValidatorAgent()
    user = "test-user-pattern"

    for _ in range(3):
        result = validator.validate(
            query_url="Patient?invalid=true",
            interpreted_capability=PATIENT_CAPABILITY,
            user_id=user,
            server_key="hapi",
        )

    assert result.get("pattern_detected") is True
    assert result["pattern_stats"]["invalid_count_10m"] >= 3