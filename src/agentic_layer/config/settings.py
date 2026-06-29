"""
Configuration loader for fhir-query-validator-factory.
Supports multiple servers via server_key and basic authentication.
"""

import os
from dataclasses import dataclass
from typing import Optional, Dict

from ..auth.provider import AuthProvider, build_auth_provider, resolve_auth_headers
from ..exceptions import UnknownServerKeyError

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


_auth_provider_cache: Optional[AuthProvider] = None


def get_settings() -> dict:
    """Load settings from environment variables."""
    return {
        "default_server_key": os.getenv("FHIR_DEFAULT_SERVER_KEY", "hapi"),
        "server_base": os.getenv("FHIR_SERVER_BASE"),
        "use_auth": os.getenv("FHIR_USE_AUTH", "false").lower() == "true",
        "auth_type": os.getenv("FHIR_AUTH_TYPE", "bearer"),
        "auth_token": os.getenv("FHIR_AUTH_TOKEN"),
        "oauth_client_id": os.getenv("OAUTH_CLIENT_ID"),
        "oauth_client_secret": os.getenv("OAUTH_CLIENT_SECRET"),
        "oauth_token_url": os.getenv("OAUTH_TOKEN_URL"),
        "oauth_scope": os.getenv("OAUTH_SCOPE"),
    }


def _ensure_protected_server(settings: dict) -> None:
    """Register a protected server when FHIR_USE_AUTH is enabled."""
    if not settings.get("use_auth"):
        return

    base_url = settings.get("server_base")
    if not base_url:
        return

    DEFAULT_SERVERS["protected"] = {
        "name": "Protected FHIR Server",
        "base_url": base_url.rstrip("/"),
        "requires_auth": True,
    }


def get_auth_provider() -> Optional[AuthProvider]:
    """Return a cached auth provider built from current settings."""
    global _auth_provider_cache
    settings = get_settings()
    if not settings.get("use_auth"):
        _auth_provider_cache = None
        return None
    if _auth_provider_cache is None:
        _auth_provider_cache = build_auth_provider(settings)
    return _auth_provider_cache


def get_auth_headers(
    server: ServerConfig,
    auth_token_override: Optional[str] = None,
) -> dict[str, str]:
    """Resolve Authorization headers for a server request."""
    settings = get_settings()
    return resolve_auth_headers(
        requires_auth=server.requires_auth,
        settings=settings,
        auth_token_override=auth_token_override,
        provider=get_auth_provider(),
    )


def get_server_config(server_key: Optional[str] = None) -> ServerConfig:
    """
    Get server configuration by key.
    Raises UnknownServerKeyError when an explicit unknown key is provided.
    """
    settings = get_settings()
    _ensure_protected_server(settings)

    key = server_key or settings["default_server_key"]
    if settings.get("use_auth") and key not in DEFAULT_SERVERS and settings.get("server_base"):
        key = "protected"

    if server_key and server_key not in DEFAULT_SERVERS:
        raise UnknownServerKeyError(
            f"Unknown server_key '{server_key}'. "
            f"Registered keys: {', '.join(sorted(DEFAULT_SERVERS.keys()))}"
        )

    if key not in DEFAULT_SERVERS:
        raise UnknownServerKeyError(
            f"Default server_key '{key}' is not registered. "
            f"Registered keys: {', '.join(sorted(DEFAULT_SERVERS.keys()))}"
        )

    server_info = DEFAULT_SERVERS[key]
    requires_auth = server_info.get("requires_auth", False) or (
        settings.get("use_auth", False) and key == "protected"
    )
    return ServerConfig(
        key=key,
        name=server_info["name"],
        base_url=server_info["base_url"],
        requires_auth=requires_auth,
        auth_token=settings.get("auth_token") if requires_auth else None,
    )