Workflow Engine
===============

The synchronous orchestrator
:func:`src.agentic_layer.graph.workflow_engine.execute_workflow` runs the full
validation pipeline and is shared by ADK graph nodes, demo scripts, and tests.

Execution order
---------------

1. **Identity** — resolve ``user_id`` via :mod:`src.agentic_layer.auth.identity`
2. **Query generation** (optional) — if ``query_url`` is empty and
   ``query_generation`` is set, :class:`~src.agentic_layer.agents.query_generator_agent.QueryGeneratorAgent`
   builds the query
3. **Pause check** — block paused users via HumanInterventionGate
4. **Server config** — load server registry; verify auth when required
5. **Cache loop** — fetch CapabilityStatement (cache hit / 304 / miss)
6. **Interpret** — build supported resource and parameter index
7. **Validate** — check ``query_url``; update pattern history
8. **Execute** — if valid and ``mode == validate_and_execute``
9. **Escalate** — RuleAgent → learner guidance or human review

Workflow modes
--------------

.. list-table::
   :header-rows: 1

   * - ``mode``
     - Behavior
   * - ``validate_only``
     - Validation and escalation only; no FHIR search execution
   * - ``validate_and_execute``
     - Run QueryExecutionAgent when validation passes

Output contract
---------------

:func:`src.agentic_layer.graph.workflow_engine.build_final_output` returns:

.. code-block:: json

   {
     "valid": true,
     "server_used": "hapi",
     "errors": [],
     "warnings": [],
     "executed": true,
     "results": { "...": "execution_result" },
     "pattern_detected": false,
     "escalation": "none",
     "guidance": null,
     "human_review_required": false,
     "human_review": null
   }

Agent bundles and isolation
---------------------------

:class:`src.agentic_layer.graph.workflow_engine.WorkflowAgents` groups all agent
singletons. Set ``FHIR_WORKFLOW_ISOLATE_STATE=true`` or pass ``isolate_state: true``
for per-request isolation in multi-tenant deployments.

Escalation thresholds
---------------------

.. list-table::
   :header-rows: 1

   * - Path
     - Threshold
   * - Learner
     - 3+ invalid queries within **10 minutes** (per ``user_id`` + ``server_key``)
   * - Human
     - 5+ invalid queries within **15 minutes**, or high-severity validation