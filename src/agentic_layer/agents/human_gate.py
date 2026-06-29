"""
HumanInterventionGate
Handles escalation to human review when needed.
"""

from typing import Dict, Any


class HumanInterventionGate:
    """
    Simulates human intervention for critical or persistent issues.
    In a real system, this would trigger notifications/tickets.
    """

    def request_human_review(self, context: Dict[str, Any]) -> Dict[str, Any]:
        print("[HumanInterventionGate] Human review requested.")
        print(f"   Context: Repeated invalid queries or high-risk pattern detected.")

        return {
            "status": "human_review_required",
            "message": "This case has been escalated for human review.",
            "context": context
        }
