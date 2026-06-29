"""
RuleAgent
Evaluates pattern detection signals and decides escalation path.
"""

from typing import Dict, Any


class RuleAgent:
    """
    Decides whether to activate Search Learner or trigger Human Intervention.
    """

    def decide_escalation(self, pattern_detected: bool, validation_result: Dict[str, Any]) -> str:
        """
        Returns: 'learner', 'human', or 'none'
        """
        if not pattern_detected:
            return "none"

        # Simple rule: if pattern detected, prefer learner first
        print("[RuleAgent] Repeated invalid pattern detected. Deciding escalation...")

        # In a more advanced version, we could have more sophisticated rules
        return "learner"
