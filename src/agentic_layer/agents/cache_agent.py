"""
CacheAgent
Handles fetching and caching of CapabilityStatement with hybrid invalidation.
"""

import time
from typing import Optional, Dict, Any
from ..config.settings import get_server_config


class CacheAgent:
    """
    Specialist agent responsible for CapabilityStatement caching.
    Supports TTL-based and simulated conditional (ETag) invalidation.
    """

    def __init__(self, ttl_seconds: int = 7 * 24 * 3600):  # Default 7 days
        self.ttl_seconds = ttl_seconds
        self._cache: Dict[str, Dict[str, Any]] = {}  # server_key -> {data, timestamp, etag}

    def get_capability_statement(self, server_key: Optional[str] = None) -> Dict[str, Any]:
        """
        Get CapabilityStatement. Uses cache if valid, otherwise fetches.
        """
        server = get_server_config(server_key)
        key = server.key

        now = time.time()

        # Check cache
        if key in self._cache:
            cached = self._cache[key]
            age = now - cached["timestamp"]

            if age < self.ttl_seconds:
                # Simulate conditional request (in real version we would use ETag)
                print(f"[CacheAgent] Cache HIT for '{key}' (age: {int(age)}s)")
                return cached["data"]
            else:
                print(f"[CacheAgent] Cache EXPIRED for '{key}' (age: {int(age)}s)")

        # Fetch fresh (simulated)
        print(f"[CacheAgent] Fetching CapabilityStatement for '{key}' from {server.base_url}")
        capability_statement = self._fetch_from_server(server)

        # Store in cache
        self._cache[key] = {
            "data": capability_statement,
            "timestamp": now,
            "etag": f'W/"{int(now)}"'  # Simulated ETag
        }

        return capability_statement

    def _fetch_from_server(self, server) -> Dict[str, Any]:
        """Simulate fetching CapabilityStatement from FHIR server."""
        # In a real implementation, this would make an HTTP request
        return {
            "resourceType": "CapabilityStatement",
            "status": "active",
            "software": {"name": server.name},
            "rest": [
                {
                    "mode": "server",
                    "resource": [
                        {"type": "Patient", "searchParam": [{"name": "gender"}, {"name": "birthdate"}]},
                        {"type": "Observation", "searchParam": [{"name": "code"}, {"name": "date"}]}
                    ]
                }
            ]
        }

    def invalidate(self, server_key: str):
        """Force invalidation of cache for a server."""
        if server_key in self._cache:
            del self._cache[server_key]
            print(f"[CacheAgent] Cache invalidated for '{server_key}'")
