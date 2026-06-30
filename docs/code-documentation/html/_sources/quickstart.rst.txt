Quick Start
===========

Run a demo
----------

All demo scripts call :func:`src.agentic_layer.graph.validation_workflow.run_validation_workflow`
and make live HTTP requests to FHIR servers.

.. code-block:: bash

   make demo-loops           # HAPI feedback loops
   make demo-agent-trace     # Per-agent pipeline + human gate
   make demo-query-generator # Generate + validate a Patient query
   make demo-adk-cli         # Google ADK CLI scenarios
   make test                 # Full test suite (158 tests)

Generate a query then validate
------------------------------

.. code-block:: bash

   python3 scripts/demo_query_generator.py --intent "male patients" --run

Or pass ``query_generation`` to the workflow instead of ``query_url``:

.. code-block:: python

   from src.agentic_layer.graph.validation_workflow import run_validation_workflow

   run_validation_workflow({
       "query_generation": {
           "resource_type": "Patient",
           "criteria": {"gender": "male"},
           "count": 10,
       },
       "server_key": "hapi",
       "mode": "validate_and_execute",
   })

ADK entry point
---------------

.. code-block:: bash

   adk run fhir_validator_agent
   adk web --port 8080 fhir_validator_agent

The ADK package re-exports :data:`fhir_validator_agent.agent.root_agent`.

Build code documentation
------------------------

.. code-block:: bash

   make docs
   open doc/_build/html/index.html