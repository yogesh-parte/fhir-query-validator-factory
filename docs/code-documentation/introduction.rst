Introduction
============

The **fhir-query-validator-factory** project demonstrates how to apply **Software
Factory** principles when building agentic AI systems with Google ADK.

Goals
-----

* Validate FHIR search queries against a server's **CapabilityStatement**
* Optionally **execute** valid queries against live FHIR servers
* Detect **repeated invalid patterns** and escalate to learner or human review
* Provide **traceability** via structured audit logs and demo scripts
* Support **multi-server** configuration including authenticated sandboxes (mock.health)

Core principles
---------------

* **Spec-driven development** — behavior defined in ``docs/spec/`` before code
* **Specialist agents** — narrow responsibilities per agent module
* **Explicit feedback loops** — cache, validation, execution, escalation
* **Human oversight** — pause / review / resume via HumanInterventionGate
* **Observable decisions** — stdout tracing and audit records

Technology stack
----------------

* Python 3.11+
* Google ADK 2.0 (``Workflow`` graph)
* ``httpx`` for FHIR HTTP I/O
* ``authlib`` for OAuth2 client credentials
* ``pydantic`` for workflow state

Repository layout
-----------------

.. code-block:: text

   src/agentic_layer/     Core agents, workflow engine, auth, utilities
   fhir_validator_agent/  ADK entry point (root_agent)
   scripts/               Demonstration CLI scripts
   tests/                 Unit, integration, regression suites
   docs/                  Specifications and user guides (Markdown)
   doc/                   This Sphinx code documentation
   planning/              Phase 0–5 roadmap artifacts