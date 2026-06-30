Installation
============

Requirements
------------

* Python **3.11** or newer
* Network access for live FHIR demo scripts (public servers or mock.health)

Install dependencies
--------------------

**Option A — pip (recommended for docs build)**

.. code-block:: bash

   python3 -m venv .venv
   source .venv/bin/activate
   pip install -e ".[dev]"

**Option B — uv**

.. code-block:: bash

   uv venv && source .venv/bin/activate
   uv pip install -e ".[dev]"

Optional extras
---------------

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Extra
     - Purpose
   * - ``dev``
     - pytest, ruff, bandit, pip-audit, **sphinx**
   * - ``adk-cli``
     - Google agents CLI tooling
   * - ``observability``
     - Langfuse integration

Secrets and configuration
-------------------------

Copy the example environment file and add API keys locally (never commit
``.env.local``):

.. code-block:: bash

   cp .env.example .env.local

``python-dotenv`` loads ``.env.local`` at startup via
:mod:`src.agentic_layer.config.settings`.

See also: :doc:`security` and ``docs/configuration.md`` in the repository.