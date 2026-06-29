"""
validation_workflow.py
Main ADK-style graph workflow demonstrating loop engineering.
"""

from typing import TypedDict, Optional, Literal, Any, Dict
from ..agents import (
    CacheAgent,
    CapabilityInterpreterAgent,
    QueryValidatorAgent,
    QueryExecutionAgent,
    RuleAgent,
    SearchLearnerAgent,
    HumanInterventionGate
)


class ValidationState(TypedDict, total=False):
    query_url: str
    server_key: Optional[str]
    user_id: Optional[str]
    mode: Literal["validate_only", "validate_and_execute"]

    capability_statement: Dict[str, Any]
    interpreted_capability: Dict[str, Any]
    validation_result: Dict[str, Any]
    execution_result: Dict[str, Any]

    pattern_detected: bool
    escalation_decision: Optional[str]  # 'learner' | 'human' | 'none'
    learner_guidance: Dict[str, Any]
    human_review: Dict[str, Any]

    final_output: Dict[str, Any]


# Initialize agents (singletons for demo)
cache_agent = CacheAgent()
interpreter = CapabilityInterpreterAgent()
validator = QueryValidatorAgent()
executor = QueryExecutionAgent()
rule_agent = RuleAgent()
learner_agent = SearchLearnerAgent()
human_gate = HumanInterventionGate()


def run_validation_workflow(state: ValidationState) -> ValidationState:
    """
    Main workflow demonstrating multiple feedback loops.
    """

    # === Step 1: Cache Loop ===
    print("\n=== [LOOP] Cache Invalidation Loop ===")
    state["capability_statement"] = cache_agent.get_capability_statement(state.get("server_key"))

    # === Step 2: Interpretation ===
    state["interpreted_capability"] = interpreter.interpret(state["capability_statement"])

    # === Step 3: Validation + Pattern Detection ===
    print("\n=== [LOOP] Validation + Pattern Detection ===")
    state["validation_result"] = validator.validate(
        query_url=state["query_url"],
        interpreted_capability=state["interpreted_capability"],
        user_id=state.get("user_id")
    )
    state["pattern_detected"] = state["validation_result"].get("pattern_detected", False)

    # === Step 4: Execution Loop (only if valid) ===
    if state["validation_result"].get("valid") and state.get("mode") == "validate_and_execute":
        print("\n=== [LOOP] Validation → Execution Loop ===")
        state["execution_result"] = executor.execute(
            query_url=state["query_url"],
            server_key=state.get("server_key")
        )
    else:
        state["execution_result"] = {"executed": False}

    # === Step 5: Rule Agent + Meta Feedback Loop ===
    print("\n=== [LOOP] Pattern Detection → Learning / Human Escalation ===")
    if state["pattern_detected"]:
        state["escalation_decision"] = rule_agent.decide_escalation(
            pattern_detected=True,
            validation_result=state["validation_result"]
        )

        if state["escalation_decision"] == "learner":
            state["learner_guidance"] = learner_agent.provide_guidance(
                query_url=state["query_url"],
                validation_result=state["validation_result"]
            )
        elif state["escalation_decision"] == "human":
            state["human_review"] = human_gate.request_human_review({
                "query_url": state["query_url"],
                "user_id": state.get("user_id"),
                "validation_result": state["validation_result"]
            })
    else:
        state["escalation_decision"] = "none"

    # Final output
    state["final_output"] = {
        "valid": state["validation_result"].get("valid"),
        "pattern_detected": state["pattern_detected"],
        "escalation": state.get("escalation_decision"),
        "execution": state.get("execution_result"),
        "guidance": state.get("learner_guidance"),
        "human_review_required": state.get("human_review") is not None
    }

    return state
