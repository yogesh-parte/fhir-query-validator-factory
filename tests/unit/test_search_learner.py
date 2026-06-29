from src.agentic_layer.agents.search_learner_agent import SearchLearnerAgent


def test_search_learner_uses_capability_statement():
    agent = SearchLearnerAgent()
    guidance = agent.provide_guidance(
        query_url="Patient?invalid_param=true",
        validation_result={
            "errors": ["Search parameter 'invalid_param' is not supported for Patient."],
            "error_types": ["unknown_parameter"],
        },
        interpreted_capability={
            "supported_resources": {
                "Patient": {
                    "search_params": [
                        {"name": "gender", "type": "token"},
                        {"name": "birthdate", "type": "date"},
                    ]
                }
            }
        },
    )
    assert "gender" in guidance["supported_parameters"]
    assert "Patient?gender=example" == guidance["example"]