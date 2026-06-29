# Planning Roadmap – fhir-query-validator-factory

**Goal**: Demonstrate the Software Factory approach by building a generalized, agentic FHIR Query Validator with feedback loops.

## Time Philosophy
We treat **planning, ideation, and human validation** as first-class, high-leverage activities. This folder contains detailed phase-by-phase planning artifacts.

## Phase Files

| Phase | Focus                                      | File                                           | Status    |
|-------|--------------------------------------------|------------------------------------------------|-----------|
| 0     | Ideation & Problem Definition              | `phase-0-ideation.md`                          | Completed |
| 1     | Requirements & Structured Planning         | `phase-1-requirements-planning.md`             | Completed |
| 2     | Architecture & Decision Making             | `phase-2-architecture.md`                      | Completed |
| 3     | Scaffolding + Core Agents                  | `phase-3-scaffolding-core-agents.md`           | Detailed Planning |
| 4     | Loop Engineering & Advanced Agents         | `phase-4-loop-engineering.md`                  | Detailed Planning |
| 5     | Documentation & Final Demonstration        | *(To be created)*                              | Planned   |

## Summary of Planning Phases

- **Phase 0–2**: Completed (Vision, Requirements, Architecture & Key Decisions)
- **Phase 3**: Detailed plan for bootstrapping with `agents-cli` and implementing core agents (`CacheAgent`, `CapabilityInterpreter`, basic `QueryValidator`)
- **Phase 4**: Detailed plan for completing the system with execution, pattern detection, Rule Agent, Learner Agent, and Human Gate

## Next Steps
Begin implementation of **Phase 3** using the detailed plan in `phase-3-scaffolding-core-agents.md`, following the architecture and specifications from Phase 2.

All planning artefacts are designed to support **spec-driven development** and maintain strong alignment with Software Factory principles.
