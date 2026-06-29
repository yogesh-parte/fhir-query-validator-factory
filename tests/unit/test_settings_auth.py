import pytest

from src.agentic_layer.config.settings import DEFAULT_SERVERS, get_server_config
from src.agentic_layer.exceptions import UnknownServerKeyError


def test_protected_server_registered_when_auth_enabled(monkeypatch):
    monkeypatch.setenv("FHIR_USE_AUTH", "true")
    monkeypatch.setenv("FHIR_SERVER_BASE", "https://fhir.example.com/R4")
    monkeypatch.delenv("FHIR_DEFAULT_SERVER_KEY", raising=False)

    if "protected" in DEFAULT_SERVERS:
        del DEFAULT_SERVERS["protected"]

    config = get_server_config("protected")

    assert config.key == "protected"
    assert config.requires_auth is True
    assert config.base_url == "https://fhir.example.com/R4"

    del DEFAULT_SERVERS["protected"]


def test_public_server_does_not_require_auth(monkeypatch):
    monkeypatch.setenv("FHIR_USE_AUTH", "false")
    config = get_server_config("hapi")
    assert config.requires_auth is False
    assert config.auth_token is None


def test_unknown_server_key_raises(monkeypatch):
    monkeypatch.setenv("FHIR_USE_AUTH", "false")
    with pytest.raises(UnknownServerKeyError):
        get_server_config("not-a-real-server")