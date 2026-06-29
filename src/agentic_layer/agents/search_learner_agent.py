"""
SearchLearnerAgent
Provides helpful explanations and suggestions when repeated invalid queries are detected.
"""

from typing import Dict, Any


class SearchLearnerAgent:
    """
    Educates the user and suggests improvements.
    """

    def provide_guidance(self, query_url: str, validation_result: Dict[str, Any]) -> Dict[str, Any]:
        print("[SearchLearnerAgent] Providing guidance for repeated invalid queries...")

        return {
            "message": "It looks like you're having trouble with this query pattern.",
            "suggestion": "Try using supported search parameters from the server's CapabilityStatement.",
            "example": "Patient?gender=male&_count=10",
            "query_url": query_url
        }
