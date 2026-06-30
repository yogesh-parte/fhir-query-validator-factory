Security
========

This project is a **demonstration** system. Security controls are implemented as
**opt-in production flags** so local demos and tests keep default behavior.

Hardening controls
------------------

.. list-table::
   :header-rows: 1
   :widths: 35 35 30

   * - Control
     - Module / location
     - Enable with
   * - Safe URL joining + no redirects
     - :mod:`src.agentic_layer.utils.url_safety`
     - Always on
   * - Human-gate operator auth
     - :mod:`src.agentic_layer.auth.operator`
     - ``FHIR_HUMAN_GATE_REQUIRE_AUTH=true``
   * - Per-request workflow isolation
     - :class:`src.agentic_layer.graph.workflow_engine.WorkflowAgents`
     - ``FHIR_WORKFLOW_ISOLATE_STATE=true``
   * - Server-side user identity
     - :mod:`src.agentic_layer.auth.identity`
     - ``FHIR_TRUST_CLIENT_USER_ID=false``
   * - Log redaction
     - :mod:`src.agentic_layer.utils.logging_safe`
     - ``FHIR_VERBOSE_LOGGING=false``

Production environment example (``.env.local``):

.. code-block:: ini

   FHIR_WORKFLOW_ISOLATE_STATE=true
   FHIR_TRUST_CLIENT_USER_ID=false
   FHIR_HUMAN_GATE_REQUIRE_AUTH=true
   FHIR_HUMAN_GATE_OPERATOR_TOKEN=change-me
   FHIR_VERBOSE_LOGGING=false

ADK Web threat model
--------------------

See the module docstring in ``fhir_validator_agent/agent.py`` for networked
exposure risks and recommended gateway controls.

Automated scanning
------------------

.. code-block:: bash

   make security   # bandit -ll + pip-audit .

CI workflow: ``.github/workflows/security.yml``.

Review artifacts
----------------

* ``docs/reviews/owasp-security-review.md`` — OWASP Pass 1 and Pass 2
* ``docs/reviews/spec-implementation-compliance-review.md`` — Spec compliance