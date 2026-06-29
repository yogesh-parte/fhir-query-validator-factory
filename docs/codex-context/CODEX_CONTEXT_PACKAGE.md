# Codex Context Package – fhir-query-validator-factory

This file can be used as a single context block when prompting Codex / Claude / Cursor.

---

## 1. Project Brief

This is a demonstration repository showing how to apply **Software Factory** principles when building agentic systems with Google ADK.

**Goal**: Build a generalized FHIR Query Validator that can:
- Dynamically validate any query against a CapabilityStatement
- Execute valid queries
- Detect repeated invalid patterns and respond with learning or human escalation

**Key Principles**:
- Planning is human-driven and highest leverage
- Use specialist agents with narrow responsibilities
- Design explicit feedback loops
- Maintain human oversight at critical points
- Follow Spec-Driven Development

**Tech Stack**: Google ADK + agents-cli (primary), Python

---

## 2. Architecture Summary

**Two Layers**:
1. **Human-Centric Planning Layer** (upstream, not automated)
2. **Agentic Orchestration Layer** (Google ADK Graph Workflow)

**Core Specialist Agents**:
- CacheAgent (hybrid TTL + ETag invalidation)
- CapabilityInterpreter Agent
- QueryValidator Agent (with pattern detection)
- QueryExecution Agent
- Rule Agent (escalation decisions)
- Search Learner Agent
- Human Intervention Gate

**Feedback Loops**:
- Cache invalidation
- Validation → Execution
- Pattern detection → Learning / Human escalation

**Multi-Server Support**:
- Public test servers via `server_key` (HAPI, Firely, Spark, WildFHIR)
- Authenticated servers via Bearer token or OAuth2

---

## 3. Key Specifications (Reference)

Please refer to the following files when implementing:

- `docs/spec/query-validation-spec.md`
- `docs/spec/cache-agent-spec.md`
- `docs/spec/query-execution-spec.md`
- `docs/spec/rule-and-learner-spec.md`
- `docs/spec/human-intervention-spec.md`
- `docs/configuration.md`

---

## 4. Current Phase Guidance

We are moving into **Phase 3 (Scaffolding + Core Agents)** followed by **Phase 4 (Loop Engineering)**.

Detailed plans are available in:
- `planning/phase-3-scaffolding-core-agents.md`
- `planning/phase-4-loop-engineering.md`

---

## 5. Implementation Rules

- Follow specs strictly (especially Acceptance Criteria)
- Prefer specialist agents over large monolithic agents
- Use ADK Graph Workflows
- Support configuration-driven server switching
- Add clear logging for agent decisions
- Keep human oversight points explicit

---

**End of Context Package**
