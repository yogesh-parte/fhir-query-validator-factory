# Loop Engineering Documentation

This document explains the explicit feedback loops implemented in the `fhir-query-validator-factory` demonstration.

## Overview

One of the core ideas of the **Software Factory** approach is **loop engineering** — deliberately designing feedback loops so the system can self-correct, learn, and escalate when necessary.

## Implemented Loops

### 1. Cache Invalidation Loop

**Agents Involved:** `CacheAgent`

**Description:**
- The `CacheAgent` fetches the `CapabilityStatement` and stores it with a timestamp.
- On subsequent requests, it checks if the cache is still valid (TTL-based).
- If expired, it refetches the statement.
- Future enhancement: Use ETag / `If-Modified-Since` for conditional requests (currently simulated).

**Goal:** Reduce unnecessary network calls while keeping data reasonably fresh.

---

### 2. Validation → Execution Loop

**Agents Involved:** `QueryValidatorAgent` → `QueryExecutionAgent`

**Description:**
- A query is only executed if it passes validation.
- This prevents wasteful or potentially harmful queries from reaching the FHIR server.

**Goal:** Ensure safety and efficiency by gating execution behind validation.

---

### 3. Pattern Detection → Learning / Human Escalation Loop (Meta Loop)

**Agents Involved:** 
- `QueryValidatorAgent` (pattern detection)
- `RuleAgent` (decision making)
- `SearchLearnerAgent` or `HumanInterventionGate`

**Description:**
This is the most important loop for demonstrating intelligent behavior:

1. `QueryValidatorAgent` tracks invalid queries per user.
2. If repeated invalid patterns are detected (e.g., 3+ failures in 5 minutes), it sets `pattern_detected = True`.
3. `RuleAgent` evaluates the situation and decides:
   - **"learner"** → Activate `SearchLearnerAgent` to educate the user.
   - **"human"** → Trigger `HumanInterventionGate` for review.
4. The system either helps the user improve or escalates to a human.

**Goal:** 
- Reduce repeated failures through guidance.
- Maintain responsible AI behavior via human oversight when automation is insufficient.
- Demonstrate self-improving / meta-feedback capabilities.

---

### Summary of Loop Engineering

| Loop Name                        | Type          | Agents Involved                     | Purpose                              | Intelligence Level |
|----------------------------------|---------------|-------------------------------------|--------------------------------------|--------------------|
| Cache Invalidation               | Operational   | CacheAgent                          | Performance & freshness              | Low                |
| Validation → Execution           | Safety        | QueryValidator + QueryExecution     | Prevent invalid execution            | Medium             |
| Pattern → Learner / Human        | Meta / Learning | QueryValidator + Rule + Learner/Human | Self-correction + responsible AI   | High               |

These loops are explicitly wired in `src/agentic_layer/graph/validation_workflow.py` and can be observed when running the demo.

---

This document serves as evidence of deliberate **loop engineering** in the Software Factory demonstration.
