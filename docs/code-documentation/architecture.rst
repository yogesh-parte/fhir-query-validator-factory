Architecture
============

High-level flow
---------------

.. code-block:: text

   Client / Demo / ADK
          │
          ▼
   validation_workflow.run_validation_workflow()
          │
          ▼
   workflow_engine.execute_workflow()
          │
          ├── CacheAgent ──► CapabilityStatement (TTL + ETag/304)
          ├── CapabilityInterpreterAgent
          ├── QueryValidatorAgent (+ pattern detection)
          ├── QueryExecutionAgent (if valid + mode allows)
          └── RuleAgent ──► SearchLearnerAgent | HumanInterventionGate

Optional upstream step: **QueryGeneratorAgent** populates ``query_url`` from
standard FHIR search parameters when ``query_generation`` is supplied.

Specialist agents
-----------------

.. list-table::
   :header-rows: 1
   :widths: 22 48 30

   * - Agent
     - Responsibility
     - Module
   * - CacheAgent
     - CapabilityStatement caching and invalidation
     - :mod:`src.agentic_layer.agents.cache_agent`
   * - CapabilityInterpreterAgent
     - Parse CapabilityStatement into validation index
     - :mod:`src.agentic_layer.agents.capability_interpreter`
   * - QueryValidatorAgent
     - Validate queries; track invalid patterns per user
     - :mod:`src.agentic_layer.agents.query_validator`
   * - QueryExecutionAgent
     - Execute validated FHIR search requests
     - :mod:`src.agentic_layer.agents.query_execution`
   * - RuleAgent
     - Decide learner vs human escalation
     - :mod:`src.agentic_layer.agents.rule_agent`
   * - SearchLearnerAgent
     - Suggest corrections from CapabilityStatement
     - :mod:`src.agentic_layer.agents.search_learner_agent`
   * - HumanInterventionGate
     - Pause, notify, review, resume
     - :mod:`src.agentic_layer.agents.human_gate`
   * - QueryGeneratorAgent
     - Build queries from FHIR standard search parameters
     - :mod:`src.agentic_layer.agents.query_generator_agent`

ADK graph wrapper
-----------------

The Google ADK ``Workflow`` in :mod:`src.agentic_layer.graph.validation_workflow`
is a thin graph over the shared engine:

.. code-block:: text

   START → initialize_workflow → run_validation_pipeline → finalize_output

Escalation (learner / human) runs inside
:func:`src.agentic_layer.graph.workflow_engine.execute_workflow`.

State model
-----------

:class:`src.agentic_layer.state.workflow_state.ValidationWorkflowState` is the
Pydantic model passed through ADK nodes and demo entry points.

Further reading
---------------

* ``docs/architecture.md`` — Mermaid diagrams and design narrative
* ``docs/loop-engineering.md`` — Feedback loop detail
* ``docs/traceability.md`` — Observability patterns