#!/usr/bin/env python3
"""
demo_adk_cli.py
Showcase the FHIR Query Validator via Google ADK CLI (`adk run`).

Runs scripted scenarios through the ADK graph workflow agent and prints
node-level events plus spec-aligned final_output. Also prints instructions
for interactive CLI mode.

Usage:
    python3 scripts/demo_adk_cli.py
    python3 scripts/demo_adk_cli.py --scenario valid
    python3 scripts/demo_adk_cli.py --interactive-hint-only

Requirements:
    pip install google-adk
    Run from repository root.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from typing import Any

from _demo_utils import adk_available, agent_dir, project_root, require_adk, summarize_final_output

AGENT_FOLDER = "fhir_validator_agent"

SCENARIOS: dict[str, dict[str, Any]] = {
    "valid": {
        "title": "Valid query — cache → validate → execute",
        "state": {
            "query_url": "Patient?gender=male",
            "server_key": "hapi",
            "user_id": "adk-cli-alice",
            "mode": "validate_and_execute",
        },
    },
    "invalid": {
        "title": "Invalid query — validation errors surfaced",
        "state": {
            "query_url": "Patient?not_a_real_param=true",
            "server_key": "hapi",
            "user_id": "adk-cli-bob",
            "mode": "validate_only",
        },
    },
    "learner": {
        "title": "Repeated invalid queries — learner escalation",
        "state": {
            "query_url": "Patient?not_a_real_param=true",
            "server_key": "hapi",
            "user_id": "adk-cli-carol",
            "mode": "validate_only",
        },
        "repeat": 3,
    },
}


def _parse_jsonl_events(stdout: str) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for line in stdout.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return events


def _extract_run_summary(events: list[dict[str, Any]]) -> dict[str, Any]:
    node_paths: list[str] = []
    final_output: dict[str, Any] = {}
    errors: list[str] = []

    for event in events:
        node_info = event.get("nodeInfo") or {}
        path = node_info.get("path")
        if path:
            node_paths.append(path)

        if event.get("errorMessage"):
            errors.append(f"{event.get('errorCode')}: {event.get('errorMessage')}")

        delta = (event.get("actions") or {}).get("stateDelta") or {}
        if delta.get("final_output"):
            final_output = delta["final_output"]

    return {
        "node_paths": node_paths,
        "final_output": final_output,
        "errors": errors,
    }


def run_adk_scenario(name: str, config: dict[str, Any]) -> None:
    repeat = config.get("repeat", 1)
    for attempt in range(1, repeat + 1):
        title = config["title"]
        if repeat > 1:
            title = f"{title} (attempt {attempt}/{repeat})"

        print("\n" + "=" * 78)
        print(f"ADK CLI SCENARIO: {name} — {title}")
        print("=" * 78)
        print(f"Agent      : {AGENT_FOLDER}")
        print(f"State      : {json.dumps(config['state'])}")
        print("-" * 78)

        cmd = [
            "adk",
            "run",
            AGENT_FOLDER,
            "--state",
            json.dumps(config["state"]),
            "--jsonl",
            "run",
        ]

        result = subprocess.run(
            cmd,
            cwd=project_root(),
            capture_output=True,
            text=True,
        )

        if result.returncode != 0 and not result.stdout.strip():
            print(result.stderr or "adk run failed")
            sys.exit(result.returncode)

        events = _parse_jsonl_events(result.stdout)
        summary = _extract_run_summary(events)

        if summary["node_paths"]:
            print("\n--- ADK GRAPH NODES ---")
            for path in summary["node_paths"]:
                print(f"  • {path}")

        if summary["errors"]:
            print("\n--- ADK ERRORS ---")
            for err in summary["errors"]:
                print(f"  • {err}")

        if summary["final_output"]:
            summarize_final_output(summary["final_output"])
        else:
            print("\nNo final_output found in ADK events (check stderr logs).")
            if result.stderr:
                print(result.stderr[-500:])

        print("=" * 78)


def print_interactive_instructions() -> None:
    print("\n" + "=" * 78)
    print("INTERACTIVE ADK CLI")
    print("=" * 78)
    print("Launch the agent in interactive mode:")
    print(f"  cd {project_root()}")
    print(f"  adk run {AGENT_FOLDER}")
    print()
    print("One-shot run with workflow state (JSON):")
    print(
        "  adk run fhir_validator_agent "
        '--state \'{"query_url":"Patient?gender=male","server_key":"hapi",'
        '"mode":"validate_and_execute","user_id":"you"}\' "run"'
    )
    print()
    print("Structured JSONL output (for tooling):")
    print(
        "  adk run fhir_validator_agent --jsonl --state '{...}' run"
    )
    print("=" * 78)


def main() -> None:
    parser = argparse.ArgumentParser(description="Google ADK CLI demo for FHIR Query Validator")
    parser.add_argument(
        "--scenario",
        choices=[*SCENARIOS.keys(), "all"],
        default="all",
        help="Which scripted scenario to run (default: all)",
    )
    parser.add_argument(
        "--interactive-hint-only",
        action="store_true",
        help="Skip scripted runs; only print interactive adk run instructions",
    )
    args = parser.parse_args()

    require_adk()
    if not agent_dir().exists():
        print(f"Agent folder not found: {agent_dir()}")
        sys.exit(1)

    print("FHIR Query Validator Factory — Google ADK CLI Demo")
    print(f"ADK CLI     : {'found' if adk_available() else 'missing'}")
    print(f"Agent entry : {agent_dir() / 'agent.py'}")

    if args.interactive_hint_only:
        print_interactive_instructions()
        return

    names = list(SCENARIOS) if args.scenario == "all" else [args.scenario]
    for name in names:
        run_adk_scenario(name, SCENARIOS[name])

    print_interactive_instructions()
    print("\nDemo complete.")


if __name__ == "__main__":
    main()