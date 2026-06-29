"""
demo_loops.py
Demonstration script showing the feedback loops in action.
"""

import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agentic_layer.graph.validation_workflow import run_validation_workflow


def run_scenario(name: str, query_url: str, user_id: str, mode: str = "validate_and_execute"):
    print("\n" + "="*70)
    print(f"SCENARIO: {name}")
    print("="*70)
    print(f"Query     : {query_url}")
    print(f"User      : {user_id}")
    print(f"Mode      : {mode}")
    print("-"*70)

    initial_state = {
        "query_url": query_url,
        "server_key": "hapi",
        "user_id": user_id,
        "mode": mode
    }

    result = run_validation_workflow(initial_state)

    print("\n--- FINAL OUTPUT ---")
    print(f"Valid                 : {result['final_output']['valid']}")
    print(f"Pattern Detected      : {result['final_output']['pattern_detected']}")
    print(f"Escalation            : {result['final_output']['escalation']}")
    print(f"Execution Performed   : {result['final_output']['execution'].get('executed')}")
    print(f"Human Review Required : {result['final_output']['human_review_required']}")

    if result.get("learner_guidance"):
        print(f"\nLearner Guidance: {result['learner_guidance']['message']}")
        print(f"Suggestion       : {result['learner_guidance']['suggestion']}")

    print("="*70 + "\n")


if __name__ == "__main__":
    print("FHIR Query Validator Factory - Loop Engineering Demo\n")

    # Scenario 1: Normal valid query (no loops triggered)
    run_scenario(
        name="Normal Valid Query",
        query_url="Patient?gender=male",
        user_id="user-alice"
    )

    # Scenario 2: Invalid query (triggers learner after repeated failures)
    run_scenario(
        name="Repeated Invalid Queries (Triggers Learner)",
        query_url="Patient?invalid_param=true",
        user_id="user-bob"
    )

    # Run same invalid query again to trigger pattern
    run_scenario(
        name="Repeated Invalid Queries #2",
        query_url="Patient?invalid_param=true",
        user_id="user-bob"
    )

    # Run again to trigger pattern detection
    run_scenario(
        name="Repeated Invalid Queries #3 (Pattern Detected)",
        query_url="Patient?invalid_param=true",
        user_id="user-bob"
    )

    print("\nDemo completed. Check the loop messages above to see feedback in action.")
