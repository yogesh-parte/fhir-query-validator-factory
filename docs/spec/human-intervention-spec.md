# Spec: Human Intervention Gate

**Status:** Draft  
**Version:** 0.1  
**Last Updated:** 2026-06-28  
**Related Specs:** rule-and-learner-spec.md

## 1. Overview

The **Human Intervention Gate** defines when and how human oversight is required in the system. It acts as a safety and governance mechanism when automated agents detect situations that exceed their confidence or policy boundaries.

## 2. Goals

- Prevent automated systems from making high-risk decisions alone
- Provide clear escalation paths for repeated or suspicious user behavior
- Maintain auditability of human decisions
- Balance automation benefits with responsible AI practices

## 3. When Human Intervention is Triggered

The Rule Agent may escalate to the Human Intervention Gate in the following situations:

| Trigger Condition                        | Example | Recommended Action |
|------------------------------------------|---------|--------------------|
| Repeated invalid queries from same user  | 5+ failures in 15 minutes | Show learning content + optional human review |
| Potential misuse or abuse patterns       | Systematic probing of unsupported parameters | Human review required |
| High-severity validation failures        | Queries that could expose sensitive data | Immediate human notification |
| System confidence below threshold        | Ambiguous CapabilityStatement interpretation | Human validation of interpretation |
| Persistent failure to improve            | User ignores suggestions repeatedly | Temporary restriction + human review |

### Implementation mapping (current code)

The following triggers are **implemented** in `src/agentic_layer/agents/rule_agent.py` and `query_validator.py`:

| Trigger | Implemented | Notes |
|---------|-------------|-------|
| 5+ invalid queries in 15 minutes | Yes | `HUMAN_THRESHOLD` + `human_threshold_met` |
| High-severity validation failures | Yes | Chained params touching sensitive markers (`patient.`, `subject.`, `individual.`) bypass learner tier |
| Systematic probing / abuse heuristics | Partial | Pattern stats and error-type tracking; no dedicated abuse classifier |
| Low confidence / ambiguous CapabilityStatement | No | Future — requires confidence scoring on interpretation |
| Persistent failure to improve after learner | No | Future — requires learner outcome tracking |

When human escalation fires, `HumanInterventionGate` pauses the user, emits a demo notification (stdout), and exposes decision options documented in §5.

## 4. Human Intervention Workflow

1. **Detection**: Rule Agent identifies a condition requiring human review.
2. **Pause**: Automated processing for the affected user/session is paused.
3. **Notification**: Relevant humans (operators, reviewers) are notified via configured channel (email, dashboard, ticket).
4. **Review**: Human reviews context (query history, errors, user info).
5. **Decision**: Human chooses one of:
   - Approve continued automated assistance
   - Provide additional guidance / update rules
   - Temporarily restrict user
   - Escalate further (security/legal team)
6. **Resume / Action**: System resumes with the human decision applied.
7. **Logging**: All decisions and rationale are recorded.

## 5. Human Decision Options

- **Continue with monitoring**
- **Show enhanced learning content**
- **Temporarily block automated queries for user**
- **Update validation rules or glossary**
- **Mark as false positive / ignore pattern**
- **Escalate to security/compliance**

## 6. Observability & Audit

- Every human intervention must be logged with:
  - Timestamp
  - Triggering condition
  - Human reviewer
  - Decision made + rationale
- This supports compliance and continuous improvement of the Rule Agent.

## 7. Non-Functional Requirements

- Human review interface should be simple and fast
- Notifications should be reliable and timely
- All intervention data must be auditable

## 8. Acceptance Criteria

- [ ] Clear, documented conditions for triggering human review
- [ ] Defined decision options for humans
- [ ] All interventions are logged with context and rationale
- [ ] System can resume correctly after human decision
- [ ] Supports different severity levels of intervention
