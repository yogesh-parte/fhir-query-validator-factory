"""Shared helpers for demo scripts."""

from __future__ import annotations

import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


def add_project_root_to_path() -> Path:
    root = Path(__file__).resolve().parent.parent
    root_str = str(root)
    if root_str not in sys.path:
        sys.path.insert(0, root_str)
    return root


def mockhealth_api_key() -> str | None:
    return os.getenv("MOCK_HEALTH_API_KEY")


def require_mockhealth_key() -> str:
    key = mockhealth_api_key()
    if key:
        return key
    print(
        "mock.health requires MOCK_HEALTH_API_KEY.\n"
        "  1. Copy .env.example to .env.local\n"
        "  2. Add your key from https://mock.health/docs\n"
        "  3. Re-run this script"
    )
    sys.exit(1)


def reset_workflow_singletons() -> None:
    from src.agentic_layer.graph import workflow_engine

    workflow_engine.cache_agent._cache.clear()
    workflow_engine.validator._pattern_history.clear()
    workflow_engine.human_gate._paused_users.clear()
    workflow_engine.human_gate._pending_reviews.clear()


def print_scenario_header(name: str, *, query_url: str, server_key: str, user_id: str, mode: str) -> None:
    print("\n" + "=" * 78)
    print(f"SCENARIO: {name}")
    print("=" * 78)
    print(f"Query      : {query_url}")
    print(f"Server     : {server_key}")
    print(f"User       : {user_id}")
    print(f"Mode       : {mode}")
    print("-" * 78)


def project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def agent_dir() -> Path:
    return project_root() / "fhir_validator_agent"


def adk_available() -> bool:
    import shutil

    return shutil.which("adk") is not None


def require_adk() -> None:
    if adk_available():
        return
    print(
        "Google ADK CLI not found. Install with:\n"
        "  pip install google-adk\n"
        "  # or: pip install -e '.[adk-cli]'"
    )
    sys.exit(1)


def summarize_final_output(final: dict[str, Any]) -> None:
    print("\n--- FINAL OUTPUT ---")
    print(f"Valid                 : {final.get('valid')}")
    print(f"Server Used           : {final.get('server_used')}")
    print(f"Pattern Detected      : {final.get('pattern_detected')}")
    print(f"Escalation            : {final.get('escalation')}")
    print(f"Execution Performed   : {final.get('executed')}")
    print(f"Human Review Required : {final.get('human_review_required')}")
    if final.get("errors"):
        print(f"Errors                : {final.get('errors')}")
    if final.get("results"):
        print(f"Results               : {final.get('results')}")