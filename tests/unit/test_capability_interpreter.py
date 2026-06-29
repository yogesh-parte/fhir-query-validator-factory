from src.agentic_layer.agents.capability_interpreter import CapabilityInterpreterAgent


def test_interpreter_extracts_modifiers_and_comparators():
    capability = {
        "resourceType": "CapabilityStatement",
        "rest": [{
            "resource": [{
                "type": "Patient",
                "searchParam": [
                    {"name": "gender", "type": "token"},
                    {"name": "birthdate", "type": "date"},
                ],
            }],
        }],
    }
    agent = CapabilityInterpreterAgent()
    result = agent.interpret(capability)
    patient = result["supported_resources"]["Patient"]
    gender = next(p for p in patient["search_params"] if p["name"] == "gender")
    birthdate = next(p for p in patient["search_params"] if p["name"] == "birthdate")
    assert "exact" in gender["modifiers"]
    assert "gt" in birthdate["comparators"]