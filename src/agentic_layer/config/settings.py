"""
Configuration loader for fhir-query-validator-factory.
Supports multiple servers via server_key and basic authentication.
"""

import os
from dataclasses import dataclass
from typing import Optional, Dict

# Default public test servers (from original repo + configuration.md)
DEFAULT_SERVERS: Dict[str, dict] = {
    "hapi": {
        "name": "HAPI FHIR",
        "base_url": "https://hapi.fhir.org/baseR4",
        "requires_auth": False,
    },
    "firely": {
        "name": "Firely",
        "base_url": "https://server.fire.ly/R4",
        "requires_auth": False,
    },
    "spark": {
        "name": "Spark",
        "base_url": "https://spark.fhir.org/r4",
        "requires_auth": False,
    },
    "wildfhir": {
        "name": "WildFHIR",
        "base_url": "https://wildfhir4.wildfhir.org/r4",
        "requires_auth": False,
    },
}


@dataclass
class ServerConfig:
    key: str
    name: str
    base_url: str
    requires_auth: bool = False
    auth_token: Optional[str] = None


def get_settings() -> dict:
    """Load settings from environment variables."""
    return {
        "default_server_key": os.getenv("FHIR_DEFAULT_SERVER_KEY", "hapi"),
        "use_auth": os.getenv("FHIR_USE_AUTH", "false").lower() == "true",
        "auth_type": os.getenv("FHIR_AUTH_TYPE", "bearer"),
        "auth_token": os.getenv("FHIR_AUTH_TOKEN"),
        "oauth_client_id": os.getenv("OAUTH_CLIENT_ID"),
        "oauth_client_secret": os.getenv("OAUTH_CLIENT_SECRET"),
        "oauth_token_url": os.getenv("OAUTH_TOKEN_URL"),
    }


def get_server_config(server_key: Optional[str] = None) -> ServerConfig:
    """
    Get server configuration by key.
    Falls back to default server if key is not provided or unknown.
    """
    settings = get_settings()
    key = server_key or settings["default_server_key"]

    if key in DEFAULT_SERVERS:
        server_info = DEFAULT_SERVERS[key]
        return ServerConfig(
            key=key,
            name=server_info["name"],
            base_url=server_info["base_url"],
            requires_auth=server_info.get("requires_auth", False),
            auth_token=settings.get("auth_token") if server_info.get("requires_auth") else None,
        )
    else:
        # Fallback to default
        default_key = settings["default_server_key"]
        server_info = DEFAULT_SERVERS.get(default_key, DEFAULT_SERVERS["hapi"])
        return ServerConfig(
            key=default_key,
            name=server_info["name"],
            base_url=server_info["base_url"],
            requires_auth=False,
        )
