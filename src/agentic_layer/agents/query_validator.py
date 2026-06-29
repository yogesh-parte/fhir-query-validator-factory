"""
QueryValidatorAgent
Validates FHIR search queries against interpreted CapabilityStatement.
Includes basic pattern detection for repeated invalid queries.
"""

from typing import Dict, Any, List, Optional
from collections import defaultdict
import time


class QueryValidatorAgent:
    """
    Validates queries and tracks repeated invalid patterns per user.
    """

    def __init__(self):
        # Simple in-memory pattern tracker: user_id -> list of (timestamp, error_type)
        self._pattern_history: Dict[str, List[tuple]] = defaultdict(list)

    def validate(
        self,
        query_url: str,
        interpreted_capability: Dict[str, Any],
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Validate the query and detect patterns if user_id is provided.
        """
        print(f"[QueryValidator] Validating query: {query_url}")

        errors = []
        warnings = []

        # Very simplified validation logic (for demonstration)
        # In real version this would deeply analyze the interpreted_capability

        if "Patient?gender" in query_url or "Observation?" in query_url:
            is_valid = True
        else:
            is_valid = False
            errors.append("Query uses unsupported parameters or structure (demo logic)")

        result = {
            "valid": is_valid,
            "errors": errors,
            "warnings": warnings,
            "query_url": query_url
        }

        # Pattern detection
        if user_id and not is_valid:
            self._record_invalid_query(user_id, "unsupported_parameter")
            pattern_detected = self._check_for_pattern(user_id)
            result["pattern_detected"] = pattern_detected
        else:
            result["pattern_detected"] = False

        return result

    def _record_invalid_query(self, user_id: str, error_type: str):
        now = time.time()
        self._pattern_history[user_id].append((now, error_type))
        # Keep only last 10 entries
        self._pattern_history[user_id] = self._pattern_history[user_id][-10:]

    def _check_for_pattern(self, user_id: str) -> bool:
        """Simple pattern detection: 3+ invalid queries in last 5 minutes."""
        history = self._pattern_history.get(user_id, [])
        if len(history) < 3:
            return False

        recent = [t for t, _ in history if time.time() - t < 300]  # 5 minutes
        return len(recent) >= 3
