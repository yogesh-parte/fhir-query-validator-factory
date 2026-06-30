# Spec Implementation Compliance Review

This file records **spec-vs-implementation compliance audits** in **reverse chronological order** (newest entry first). Each pass compares `docs/spec/*.md` and supporting `docs/*.md` against `src/agentic_layer/`, demos, tests, and configuration.

Also see: [README Spec vs Code Gap Review](../../README.md#spec-vs-code-gap-review) (implementation summary).

---

## Pass 2 — 2026-06-30 (second audit)

| Field | Value |
|-------|-------|
| **Review timestamp** | `2026-06-30T18:30:00+05:30` (IST) / `2026-06-30T13:00:00Z` (UTC) |
| **Reviewer** | `/review --local` compliance audit (read-only) |
| **Scope** | `docs/spec/*.md`, `docs/configuration.md`, `docs/loop-engineering.md`, `docs/architecture.md`, `docs/traceability.md`, `docs/public-test-servers.md`, `README.md` vs implementation |
| **Prior pass** | [Pass 1 below](#pass-1--2026-06-30-first-audit) |
| **Evidence** | `python3 -m pytest tests/ -q` → **41 passed**; live **mock.health** validate+execute OK with `MOCK_HEALTH_API_KEY` from `.env.local` |

### Executive summary

| Layer | Status | Notes |
|-------|--------|-------|
| **Implementation vs specs** | **Mostly compliant** | All five draft specs implemented; mock.health added since Pass 1 |
| **E2E demonstration** | **Partially compliant** | Notebook improved (firely switcher, human gate); **CLI scripts still HAPI-only**; mock.health live but **not in notebook/scripts** |
| **Documentation** | **Improved, inconsistent** | `public-test-servers.md`, mockhealth in spec v0.3/README; **`loop-engineering.md` and `planning/` stale**; **critical: live API key in tracked `.env.example`** |

**Verdict:** Implementation is **ahead of Pass 1**. mock.health (`server_key: mockhealth`) works end-to-end with `MOCK_HEALTH_API_KEY` in git-ignored `.env.local`. Demo parity remains the main gap: richest coverage is in [`examples/notebooks/demo_loops.ipynb`](../../examples/notebooks/demo_loops.ipynb); [`scripts/demo_loops.py`](../../scripts/demo_loops.py) unchanged.

### Delta since Pass 1

| Item | Pass 1 | Pass 2 |
|------|--------|--------|
| mock.health server | Not implemented | `mockhealth` in [`settings.py`](../../src/agentic_layer/config/settings.py); `auth_token_env: MOCK_HEALTH_API_KEY` |
| Secrets loading | Not noted | `python-dotenv` in [`pyproject.toml`](../../pyproject.toml); `.env.local` auto-loaded |
| `.gitignore` | Not detailed | Ignores `.env`, `.env.local`, `env.mockhealth` |
| `docs/public-test-servers.md` | Missing (S-04) | **Created** |
| query-validation-spec | v0.2 | **v0.3** — mockhealth acceptance criterion |
| README | Basic quick start | Env setup (uv/pip), mock.health snippet, 41 tests |
| Notebook | HAPI only | Scenarios 3–4: `hapi`+`firely`, human escalation, pause/resume |
| CLI demos | HAPI only | **Still HAPI only** |
| Tests | 38 passed | **41 passed** (+3 mockhealth in [`test_settings_auth.py`](../../tests/unit/test_settings_auth.py)) |
| Live mock.health | Not demonstrated | **Works** (validate_only + validate_and_execute, HTTP 200) |

### Per-spec acceptance criteria (summary)

All specs remain **Draft**. Full tables in Pass 1; key Pass 2 updates:

| Spec | Pass 2 status | Notable change |
|------|---------------|----------------|
| [query-validation-spec](../spec/query-validation-spec.md) | **Mostly Met** | mockhealth + `MOCK_HEALTH_API_KEY` criterion added and implemented |
| [cache-agent-spec](../spec/cache-agent-spec.md) | **Met** (partial hybrid) | mock.health auth-scoped cache keys exercised live |
| [query-execution-spec](../spec/query-execution-spec.md) | **Met** | mock.health execution confirmed live |
| [rule-and-learner-spec](../spec/rule-and-learner-spec.md) | **Met** | Human path demonstrated in notebook |
| [human-intervention-spec](../spec/human-intervention-spec.md) | **Partial** | Pause/resume in notebook; not all spec trigger rows coded |

### Cross-doc inconsistencies

| ID | Documents | Issue |
|----|-----------|-------|
| **X-01** | [`loop-engineering.md`](../loop-engineering.md) L19, L48 vs code | Still says ETag "simulated" and **5-minute** learner threshold; code uses real ETag/304 and **10m/15m** |
| **X-02** | [`README.md`](../../README.md) vs notebook | README claims notebook includes mock.health when key set; **notebook has no mock.health cell** |
| **X-03** | Notebook Scenario 3 markdown vs code | Markdown lists four public servers; code uses `PUBLIC_SERVERS = ["hapi", "firely"]` only |
| **X-04** | [`planning/phase-3`](../planning/phase-3-scaffolding-core-agents.md), [`phase-4`](../planning/phase-4-loop-engineering.md) | Status still **Planned** |
| **X-05** | [`.env.example`](../../.env.example) L36 vs security policy | **Uncommented live `MOCK_HEALTH_API_KEY` in tracked file** — contradicts configuration docs; **rotate key and replace with commented placeholder** |
| **X-06** | Pass 1 S-04 | **Resolved** — `public-test-servers.md` now exists |

### E2E demonstration matrix (Pass 2)

| Behavior | Code | `demo_loops.py` | `demo_traceability.py` | Notebook | README |
|----------|------|-----------------|------------------------|----------|--------|
| Cache + validate + execute | ✅ | ✅ HAPI | ✅ HAPI | ✅ | — |
| Learner escalation | ✅ | ✅ | ✅ | ✅ | — |
| Human escalation + pause/resume | ✅ | ❌ | ❌ | ✅ Scenario 4 | — |
| Multi-server public | ✅ | ❌ | ❌ | **Partial** (`hapi`, `firely`) | — |
| `validate_only` | ✅ | ❌ | ❌ | ✅ | — |
| **mock.health** authenticated | ✅ | ❌ | ❌ | ❌ | ✅ one-liner |
| Makefile demo/test | — | ❌ stubs | ❌ stubs | — | pytest documented |

### Test coverage

**41 passed** (`python3 -m pytest tests/ -q`, 2026-06-30).

Gaps: no live-network pytest for mockhealth/firely/spark/wildfhir; no integration test for auth-missing error message on mockhealth workflow path; Makefile `test` still a stub.

### Critical findings

| Sev | ID | Finding | File |
|-----|-----|---------|------|
| **bug** | C-01 | Live mock.health API key committed in `.env.example` (uncommented) | [`.env.example`](../../.env.example) |
| suggestion | C-02 | CLI demos lag notebook for human gate and multi-server | [`scripts/demo_loops.py`](../../scripts/demo_loops.py) |
| suggestion | C-03 | README overstates notebook mock.health coverage | [`README.md`](../../README.md) |

### Priority actions

1. **Rotate and remove** live key from `.env.example`; use commented placeholder only (C-01).
2. Add mock.health cell to notebook **or** correct README claim (X-02).
3. Update [`loop-engineering.md`](../loop-engineering.md) thresholds and ETag status (X-01).
4. Extend `demo_loops.py` with optional `mockhealth` + human-escalation scenarios.
5. Wire [`Makefile`](../../Makefile) `demo`/`test` to real commands.
6. Update `planning/` phase status to Complete (X-04).

### Live evidence (mock.health)

With `MOCK_HEALTH_API_KEY` in `.env.local` (not committed):

- `validate_only` `Patient?_count=1` → `valid: true`, `server_used: mockhealth`
- `validate_and_execute` → `executed: true`, HTTP 200, `bundle_type: searchset`, ~800–900ms

---

*End of Pass 2.*

---

## Pass 1 — 2026-06-30 (first audit)

| Field | Value |
|-------|-------|
| **Review timestamp** | `2026-06-30T04:12:00+05:30` (IST) / `2026-06-29T22:42:00Z` (UTC) |
| **Reviewer** | Automated compliance review (goal-driven analysis) |
| **Scope** | `docs/spec/*.md` vs `src/agentic_layer/`, `fhir_validator_agent/`, `scripts/`, `tests/`, `examples/`, `planning/`, supporting `docs/*.md` |
| **Evidence runs** | `demo_loops.py` (exit 0), `demo_traceability.py` (exit 0), `pytest` (38 passed) |
| **Related** | [README Spec vs Code Gap Review](../../README.md#spec-vs-code-gap-review) |

---

### Executive summary

The **implementation layer** (`src/agentic_layer/`) is substantially aligned with all five draft specifications: real HTTP via `httpx`, CapabilityStatement-driven validation, auth forwarding, hybrid cache invalidation, tiered escalation, and a human intervention gate are present and tested.

The **end-to-end demonstration layer** (`scripts/`, `examples/notebooks/`, `Makefile`) does **not yet exercise the full SPEC surface area**. Demos hard-code `server_key: "hapi"`, never show protected-server auth, never reach the human-escalation path, and do not switch across Firely/Spark/WildFHIR. Interactive ADK entry points exist but are not wired into demo scripts.

**Verdict:**

| Layer | Status | Notes |
|-------|--------|-------|
| Spec acceptance criteria (code) | **Mostly compliant** | 5/5 specs have implementing modules; minor gaps in production hardening |
| E2E demonstration as per SPEC | **Partially compliant** | Core happy path + learner loop demonstrated; multi-server, auth, human gate not demonstrated |
| Documentation consistency | **Needs updates** | Threshold mismatch in `loop-engineering.md`; missing `public-test-servers.md`; stale `planning/` status |

---

### Review methodology

1. Read all five specification files in [`docs/spec/`](../spec/) and supporting architecture/configuration/loop docs.
2. Traced each spec acceptance criterion to implementing modules under [`src/agentic_layer/`](../../src/agentic_layer/).
3. Ran live demos and test suite (see [Evidence: demo and test runs](#evidence-demo-and-test-runs-pass-1)).
4. Compared demo scripts and notebook against SPEC-required behaviors (multi-server, auth, escalation paths, output contract).
5. Identified SPEC and doc inconsistencies requiring updates (draft status, open questions, cross-doc threshold conflicts).

---

### Per-spec compliance

All specs are marked **Draft** with open questions. Compliance below reflects **current on-disk implementation** at Pass 1 time.

#### 1. [query-validation-spec.md](../spec/query-validation-spec.md)

| Acceptance criterion | Status | Implementation | Gap / note |
|---------------------|--------|----------------|------------|
| Supports switching between multiple public test servers via configuration | ✅ Met | [`settings.py`](../../src/agentic_layer/config/settings.py) — `hapi`, `firely`, `spark`, `wildfhir` in `DEFAULT_SERVERS` | Demos never switch servers; no integration test against live alternate servers |
| Can authenticate against protected servers using Bearer token or OAuth | ✅ Met | [`auth/provider.py`](../../src/agentic_layer/auth/provider.py), [`workflow_engine.py`](../../src/agentic_layer/graph/workflow_engine.py) | OAuth is client-credentials only; no demo scenario |
| Validates any parameter declared in the CapabilityStatement | ✅ Met | [`query_validator.py`](../../src/agentic_layer/agents/query_validator.py), [`capability_interpreter.py`](../../src/agentic_layer/agents/capability_interpreter.py), [`query_parser.py`](../../src/agentic_layer/utils/query_parser.py) | Modifiers derived from FHIR type tables, not server-declared modifier lists |
| Pattern detection and escalation work across different servers | ⚠️ Partial | Pattern history keyed by `user_id:server_key` in [`query_validator.py`](../../src/agentic_layer/agents/query_validator.py) | No test or demo proving cross-server isolation |
| Clear error messages when authentication fails | ✅ Met | [`workflow_engine.py`](../../src/agentic_layer/graph/workflow_engine.py); execution 401/403 in [`query_execution.py`](../../src/agentic_layer/agents/query_execution.py) | — |

**Output contract:** [`build_final_output()`](../../src/agentic_layer/graph/workflow_engine.py) returns the six spec fields plus demo extensions. Core contract satisfied.

---

#### 2. [cache-agent-spec.md](../spec/cache-agent-spec.md)

| Acceptance criterion | Status | Implementation | Gap / note |
|---------------------|--------|----------------|------------|
| Works with both public and authenticated servers | ✅ Met | [`cache_agent.py`](../../src/agentic_layer/agents/cache_agent.py) | — |
| Correctly implements hybrid invalidation | ✅ Met | TTL + ETag/`If-None-Match` + 304 | `Last-Modified` not implemented |
| Logs cache decisions | ✅ Met | stdout logging | No structured log sink |
| Respects authentication when fetching | ✅ Met | [`auth_cache_suffix()`](../../src/agentic_layer/auth/provider.py) | In-memory only |

---

#### 3. [query-execution-spec.md](../spec/query-execution-spec.md)

| Acceptance criterion | Status | Implementation | Gap / note |
|---------------------|--------|----------------|------------|
| Execute on public test servers | ✅ Met | Real `httpx` in [`query_execution.py`](../../src/agentic_layer/agents/query_execution.py) | Live demo HAPI only |
| Auth headers for protected | ✅ Met | `get_auth_headers()` forwarded | No live protected-server demo |
| Structured responses | ✅ Met | `status`, `error_type`, `elapsed_ms` | Bundle summary only |
| Log outcome + timing | ✅ Met | `print` + `elapsed_ms` | — |

---

#### 4. [rule-and-learner-spec.md](../spec/rule-and-learner-spec.md)

| Acceptance criterion | Status | Implementation | Gap / note |
|---------------------|--------|----------------|------------|
| Pattern detection | ✅ Met | 3/10m, 5/15m in [`query_validator.py`](../../src/agentic_layer/agents/query_validator.py) | — |
| Learner vs human escalation | ✅ Met | [`rule_agent.py`](../../src/agentic_layer/agents/rule_agent.py) | Demos only show learner |
| Learner suggestions | ✅ Met | [`search_learner_agent.py`](../../src/agentic_layer/agents/search_learner_agent.py) | Rule-based |
| Human path observable | ⚠️ Partial | [`human_gate.py`](../../src/agentic_layer/agents/human_gate.py) | Not in demo scripts |
| Audit logging | ✅ Met | [`audit_log.py`](../../src/agentic_layer/utils/audit_log.py) | — |

**ADK note:** Escalation runs inside [`workflow_engine.py`](../../src/agentic_layer/graph/workflow_engine.py); the ADK graph is a linear initialize → pipeline → finalize wrapper.

---

#### 5. [human-intervention-spec.md](../spec/human-intervention-spec.md)

| Acceptance criterion | Status | Implementation | Gap / note |
|---------------------|--------|----------------|------------|
| Documented triggers | ⚠️ Partial | 5+/15m, high-severity in code | Not all spec table rows coded |
| Decision options | ✅ Met | Six options in [`human_gate.py`](../../src/agentic_layer/agents/human_gate.py) | — |
| Logged interventions | ✅ Met | `AuditLog` | stdout notification only |
| Resume after decision | ✅ Met | `submit_review_decision()`, `is_paused()` | No demo |
| Severity levels | ✅ Met | `InterventionSeverity` enum | — |

---

### E2E demonstration assessment (Pass 1)

| Behavior | Demo script | Pass 1 status |
|----------|-------------|---------------|
| Cache invalidation | `demo_loops.py` | ✅ HAPI |
| Valid query + execute | demos | ✅ HAPI |
| Learner escalation | `demo_loops.py` | ✅ |
| Human escalation | — | ❌ |
| Multi-server | — | ❌ HAPI only |
| Protected server / auth | — | ❌ |
| `validate_only` | — | ❌ |

---

### Test coverage (Pass 1)

**38 passed** (`python3 -m pytest tests/ --tb=no -q`).

Gaps: no live-network tests; Makefile stubs; human pause not in integration tests.

---

### Gaps summary (Pass 1)

**Implementation (non-blocking):** in-memory cache, no Last-Modified, OAuth client-credentials with in-memory token reuse, stdout human notifications.

**E2E (blocking full showcase):** D-01 demos HAPI-only; D-02 no auth demo; D-03 no human path in scripts; D-05 Makefile stubs.

---

### SPEC updates required (Pass 1)

| ID | Document | Issue |
|----|----------|-------|
| S-01 | `loop-engineering.md` | 5-minute threshold; ETag "simulated" |
| S-02 | `rule-and-learner-spec.md` | Open threshold question |
| S-04 | `query-validation-spec.md` | Missing `public-test-servers.md` reference |
| S-05–S-06 | `planning/` | Status still Planned |
| S-07 | All specs | Draft status |

---

### Recommendations (Pass 1)

Wire Makefile; extend demos for firely + human escalation; add `@pytest.mark.live` tests; document `adk web`; extend notebook (subsequently done in Pass 2 for human gate and partial multi-server).

---

### Evidence: demo and test runs (Pass 1)

| Artifact | Result |
|----------|--------|
| `demo_loops.py` | Exit 0; learner on 3rd invalid attempt |
| `demo_traceability.py` | Exit 0 |
| `pytest` | 38 passed |

---

### Conclusion (Pass 1)

Core spec behavior implemented in code; demo/tooling layer lagged specs. Priority: update `loop-engineering.md`, extend demos, wire Makefile, resolve draft spec open questions.

---

*End of Pass 1.*