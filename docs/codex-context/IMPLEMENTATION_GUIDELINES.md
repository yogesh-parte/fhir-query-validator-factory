# Implementation Guidelines for Codex

## General Rules

1. **Follow Specifications Strictly**
   - Every agent must be implemented according to its spec in `docs/spec/`
   - Pay special attention to the **Acceptance Criteria** section in each spec

2. **Specialist Agent Philosophy**
   - Keep agents focused and narrow in responsibility
   - Avoid putting too much logic in one agent

3. **Use Google ADK Patterns**
   - Prefer ADK Graph Workflows and tools where appropriate
   - Follow ADK conventions for state management and node structure

4. **Configuration First**
   - All server-specific behavior should be driven by configuration (`docs/configuration.md`)
   - Support `server_key` for switching between servers

5. **Observability**
   - Add clear logging for key decisions made by each agent
   - Log cache hits/misses, validation results, escalation decisions, etc.

6. **Error Handling**
   - Return structured errors
   - Distinguish between validation errors, execution errors, and system errors

## Recommended Prompting Pattern

When asking Codex to implement something, use this structure:

```
You are implementing [Agent Name] for the fhir-query-validator-factory project.

Project Context:
[Reference PROJECT_BRIEF.md]

Relevant Specifications:
- [Paste or reference the spec file]

Architecture Overview:
[Reference docs/architecture.md or key parts]

Requirements:
- Follow the Acceptance Criteria in the spec
- Use Google ADK patterns
- Support both public and authenticated servers where applicable
- Add clear logging for decisions

Please implement [specific component] following the above.
```

## File Organization

- Place new agents in: `src/agentic_layer/agents/`
- Place graph workflows in: `src/agentic_layer/graph/`
- Place configuration logic in: `src/agentic_layer/config/`
- Keep implementation aligned with the planning in `planning/phase-3-*.md` and `planning/phase-4-*.md`

## Review Checklist (Human)

Before accepting generated code, verify:
- [ ] Aligns with the relevant spec
- [ ] Follows specialist agent principle (not bloated)
- [ ] Handles public + authenticated servers
- [ ] Has reasonable logging/observability
- [ ] Is consistent with existing code style and structure
