from src.agentic_layer.agents.human_gate import HumanInterventionGate


def test_human_gate_pause_notify_and_resume():
    gate = HumanInterventionGate()
    review = gate.request_human_review({
        "query_url": "Patient?bad=true",
        "user_id": "user-paused",
        "server_key": "hapi",
        "validation_result": {
            "pattern_stats": {"human_threshold_met": True},
            "high_severity": False,
        },
    })

    assert review["paused"] is True
    assert review["severity"] in {"high", "medium", "critical"}
    assert gate.is_paused("user-paused")

    resolved = gate.submit_review_decision(
        review["review_id"],
        reviewer="operator-1",
        decision="continue_monitoring",
        rationale="Benign learning pattern.",
    )
    assert resolved["resumed"] is True
    assert not gate.is_paused("user-paused")