Testing
=======

Test layout
-----------

.. code-block:: text

   tests/unit/           Per-module unit tests
   tests/integration/    Full workflow with mocked HTTP
   tests/regression/     Spec regression fixtures

Run tests
---------

.. code-block:: bash

   make test
   python3 -m pytest tests/ -q
   python3 -m pytest tests/unit/test_query_generator.py -v

Coverage
--------

The unit suite achieves ~99% coverage on ``src/agentic_layer``. Integration tests
exercise human-gate pause/resume, learner escalation, and auth paths.

Security tests
--------------

:mod:`tests.unit.test_security_hardening` covers URL safety, operator auth,
workflow isolation, and identity resolution.

CI
--

* ``make test`` — full pytest suite (158 tests)
* ``make security`` — Bandit + pip-audit
* ``.github/workflows/security.yml`` — security on push/PR