Demo Scripts
============

All scripts live under ``scripts/``. Shared helpers are in ``_demo_utils.py``.

.. list-table::
   :header-rows: 1
   :widths: 28 52 20

   * - Script
     - Purpose
     - Auth
   * - ``demo_loops.py``
     - HAPI cache → validate → execute → learner escalation
     - No
   * - ``demo_traceability.py``
     - Compact trace reports
     - No
   * - ``demo_agent_traceability.py``
     - Per-agent pipeline, audit trail, human pause/resume
     - mock.health only
   * - ``demo_loops_mockhealth.py``
     - Loops on authenticated mock.health sandbox
     - Yes
   * - ``demo_query_generator.py``
     - Generate queries from standard FHIR search params
     - No
   * - ``demo_adk_cli.py``
     - ``adk run`` scenarios and JSONL events
     - No
   * - ``demo_adk_web.py``
     - ``adk web`` UI + ``/run`` API demo
     - No

Makefile targets
----------------

.. code-block:: bash

   make demo-loops
   make demo-trace
   make demo-agent-trace
   make demo-mockhealth
   make demo-query-generator
   make demo-adk-cli
   make demo-adk-web

Singleton reset
---------------

Demos call :func:`src.agentic_layer.graph.workflow_engine.reset_singletons` between
scenarios so pattern history does not leak across runs.