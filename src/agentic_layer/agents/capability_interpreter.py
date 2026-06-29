"""
CapabilityInterpreterAgent
Dynamically interprets CapabilityStatement to support generalized validation.
"""

from typing import Dict, Any, List


class CapabilityInterpreterAgent:
    """
    Specialist agent that extracts usable information from CapabilityStatement.
    """

    def interpret(self, capability_statement: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract supported resources, search parameters, modifiers, etc.
        """
        print("[CapabilityInterpreter] Interpreting CapabilityStatement...")

        supported = {}

        try:
            rest = capability_statement.get("rest", [])
            for rest_entry in rest:
                for resource in rest_entry.get("resource", []):
                    resource_type = resource.get("type")
                    if not resource_type:
                        continue

                    search_params = []
                    for param in resource.get("searchParam", []):
                        search_params.append({
                            "name": param.get("name"),
                            "type": param.get("type", "string")
                        })

                    supported[resource_type] = {
                        "search_params": search_params
                    }
        except Exception as e:
            print(f"[CapabilityInterpreter] Error interpreting CapabilityStatement: {e}")
            return {"supported_resources": {}}

        return {
            "supported_resources": supported,
            "software": capability_statement.get("software", {})
        }
