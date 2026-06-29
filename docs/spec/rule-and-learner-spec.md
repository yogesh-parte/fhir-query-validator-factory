# Spec: Rule Agent + Search Learner Agent

**Status:** Draft  
**Version:** 0.1  
**Last Updated:** 2026-06-28  
**Related Specs:** query-validation-spec.md

## 1. Overview

This specification covers two collaborating agents:

- **Rule Agent**: Monitors for repeated invalid query patterns from the same user and decides on escalation.
- **Search Learner Agent**: Educates the user and captures improvement opportunities when triggered.

Together they implement a **meta-feedback loop** for continuous improvement and responsible handling of user errors.

## 2. Goals

- Detect problematic usage patterns early
- Provide helpful guidance instead of repeated hard failures
- Protect system stability through human escalation when needed
- Capture data for long-term improvement of validation rules

## 3. Rule Agent Responsibilities

| Responsibility                    | Description |
|-----------------------------------|-----------|
| Pattern Detection                 | Track invalid queries per user over a time window |
| Threshold Evaluation              | Decide when repeated failures warrant escalation |
| Decision Making                   | Choose between activating Search Learner Agent or triggering Human Intervention |
| Logging & Observability           | Record pattern events for auditing and improvement |

### Pattern Detection Criteria (Example)
- Same user submits 3+ invalid queries within 10 minutes
- Repeated use of the same unsupported modifier or parameter
- High error rate on similar query structures

## 4. Search Learner Agent Responsibilities

| Responsibility                    | Description |
|-----------------------------------|-----------|
| Explain Errors                    | Provide user-friendly explanation of why queries are failing |
| Suggest Corrections               | Offer corrected query examples based on CapabilityStatement |
| Educational Response              | Help users learn valid query patterns |
| Pattern Logging                   | Record recurring issues for future rule or documentation improvements |

## 5. Human Intervention Gate

When the Rule Agent determines the situation requires human oversight (e.g., persistent misuse, potential abuse, or complex edge cases), it should:

- Pause automated processing for that user/session
- Create a ticket or notification for human review
- Allow human to either:
  - Approve continued automated assistance
  - Temporarily restrict the user
  - Update validation rules or guidance

## 6. Inputs to Rule Agent

- User ID / session identifier
- Recent invalid query history
- Error types and frequency

## 7. Outputs

- Decision: `activate_learner` | `trigger_human` | `continue_monitoring`
- Optional: Suggested learning content or human ticket details

## 8. Acceptance Criteria

- [ ] Correctly detects repeated invalid patterns per user
- [ ] Triggers appropriate escalation path (Learner vs Human)
- [ ] Search Learner Agent provides helpful, accurate suggestions
- [ ] Human intervention path is clearly defined and observable
- [ ] All decisions are logged with reasoning

## 9. Open Questions

- What is the exact threshold and time window for pattern detection?
- Should the learner agent update global validation rules over time, or only provide per-user suggestions?
