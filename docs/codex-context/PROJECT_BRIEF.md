# Project Brief: fhir-query-validator-factory

## Overview
This is a **demonstration repository** that shows how to apply **Software Factory** principles when building agentic systems using Google ADK.

The goal is to evolve from a traditional limited FHIR Query Validator into a **generalized, intelligent system** that can:
- Dynamically validate any query against a server’s CapabilityStatement
- Execute valid queries
- Detect repeated user errors and respond intelligently (via learning or human escalation)

## Core Philosophy
- **Planning is the highest-leverage activity** (human-driven)
- Use **specialist agents** with narrow responsibilities instead of monolithic agents
- Design **explicit feedback loops** (cache, execution, learning, human escalation)
- Maintain strong **human oversight** at critical points
- Follow **Spec-Driven Development**

## Technology Stack
- **Orchestration**: Google Agent Development Kit (ADK) + `agents-cli`
- **Primary Path**: Google ADK (Enterprise)
- **Lighter Path**: Direct Gemini API
- **Language**: Python

## Key Architectural Decisions
- Dual-path strategy (Enterprise ADK vs Lighter Gemini)
- Specialist agents orchestrated via ADK Graph Workflows
- Configuration-driven multi-server support (public + authenticated)
- Clear separation between Human Planning Layer and Agentic Execution Layer

## Current Status
- Phases 0–2 completed (Vision, Requirements, Architecture)
- Detailed plans available for Phase 3 (Core Agents) and Phase 4 (Loop Engineering)
- Comprehensive specifications exist in `docs/spec/`

## Important Principles for Implementation
1. Every agent must be implemented according to its specification in `docs/spec/`
2. Maintain modularity — one agent = one clear responsibility
3. All feedback loops and human gates must be explicit
4. Configuration and server switching must be clean and well-documented
5. Observability (logging of agent decisions) is important for the demonstration
