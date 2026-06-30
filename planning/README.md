# Planning Roadmap – fhir-query-validator-factory

**Goal**: Demonstrate the Software Factory approach by building a generalized, agentic FHIR Query Validator with feedback loops.

**Last updated:** 2026-06-30

## Time Philosophy

We treat **planning, ideation, and human validation** as first-class, high-leverage activities. This folder contains detailed phase-by-phase planning artifacts.

## Phase Files

| Phase | Focus | File | Status |
|-------|-------|------|--------|
| 0 | Ideation & Problem Definition | `phase-0-ideation.md` | Completed |
| 1 | Requirements & Structured Planning | `phase-1-requirements-planning.md` | Completed |
| 2 | Architecture & Decision Making | `phase-2-architecture.md` | Completed |
| 3 | Scaffolding + Core Agents | `phase-3-scaffolding-core-agents.md` | Completed |
| 4 | Loop Engineering & Advanced Agents | `phase-4-loop-engineering.md` | Completed |
| 5 | Demo Parity, Security Hardening & Governance | `phase-5-demo-hardening-and-governance.md` | Completed |

## Summary of Planning Phases

- **Phase 0–2**: Vision, requirements, architecture, and key decisions
- **Phase 3**: Google ADK scaffolding; `CacheAgent`, `CapabilityInterpreter`, `QueryValidator`; configuration and initial workflow
- **Phase 4**: `QueryExecution`, pattern detection, `RuleAgent`, `SearchLearnerAgent`, `HumanInterventionGate`; full feedback loops in `workflow_engine.py`
- **Phase 5**: Demo parity (HAPI, mock.health, ADK CLI/Web, agent traceability); **148 tests**; OWASP + spec compliance reviews; opt-in production security hardening; CI Bandit/pip-audit

## Current state (2026-06-30)

| Layer | Status |
|-------|--------|
| Core specs (5 agent specs) | Acceptance criteria **closed** — see [README Spec vs Code Gap Review](../README.md#spec-vs-code-gap-review) |
| Implementation | Google ADK 2.0 graph + shared `execute_workflow()` engine |
| Demos | 6 CLI scripts + Makefile targets; ADK `adk run` / `adk web` via `fhir_validator_agent/` |
| Security | OWASP Pass 2 complete; hardening behind `FHIR_*` env flags — see [OWASP review](../docs/reviews/owasp-security-review.md) |
| Reviews | `docs/reviews/owasp-security-review.md`, `docs/reviews/spec-implementation-compliance-review.md` |

## Next Steps (post–Phase 5)

1. **Documentation parity** — align `docs/loop-engineering.md` and notebook with CLI demo coverage (mock.health, human gate)
2. **Reproducible deps** — add committed lockfile (`uv.lock` or `requirements.lock`)
3. **Optional production path** — deployment guide or automation for ADK Web behind API gateway with production `FHIR_*` flags enabled
4. **Knowledge bundle** — run OKF or equivalent to refresh `docs/knowledge-bundle.md` if publishing reference artifacts

## Review artifacts

| Review | Location |
|--------|----------|
| OWASP security (Pass 1 + Pass 2) | [docs/reviews/owasp-security-review.md](../docs/reviews/owasp-security-review.md) |
| Spec implementation compliance | [docs/reviews/spec-implementation-compliance-review.md](../docs/reviews/spec-implementation-compliance-review.md) |

All planning artefacts are designed to support **spec-driven development** and maintain strong alignment with Software Factory principles.