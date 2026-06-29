"""
QueryExecutionAgent
Executes validated FHIR search queries.
"""

from typing import Dict, Any, Optional
from ..config.settings import get_server_config


class QueryExecutionAgent:
    """
    Executes FHIR queries after successful validation.
    """

    def execute(
        self,
        query_url: str,
        server_key: Optional[str] = None,
        auth_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Execute the query against the FHIR server.
        """
        server = get_server_config(server_key)
        print(f"[QueryExecution] Executing query on {server.name}: {query_url}")

        # Simulated execution
        if "Patient?" in query_url:
            result = {
                "executed": True,
                "status": "success",
                "total": 42,
                "bundle_type": "searchset"
            }
        else:
            result = {
                "executed": True,
                "status": "error",
                "error_type": "not_supported_in_demo",
                "message": "This query pattern is not simulated in the demo"
            }

        return result
