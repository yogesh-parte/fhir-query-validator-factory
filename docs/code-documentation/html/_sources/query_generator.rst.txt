Query Generator
===============

:class:`src.agentic_layer.agents.query_generator_agent.QueryGeneratorAgent`
builds FHIR REST search query strings from **standard R4 search parameters**
documented on `build.fhir.org <https://build.fhir.org/resourcelist.html>`_.

Data source
-----------

Standard parameters are bundled in:

.. code-block:: text

   src/agentic_layer/data/fhir_standard_search_params.json

Each resource entry includes:

* ``resource_page`` — e.g. https://build.fhir.org/patient.html
* ``search_page`` — e.g. https://build.fhir.org/patient-search.html
* ``search_params`` — name, FHIR type, documentation, optional comparators

Supported resource types (bundled)
----------------------------------

Patient, Observation, Condition, Encounter, MedicationRequest,
DiagnosticReport, Organization, Practitioner.

API overview
------------

.. code-block:: python

   from src.agentic_layer.agents.query_generator_agent import QueryGeneratorAgent

   agent = QueryGeneratorAgent()

   # List resources
   agent.list_resources()

   # Describe standard parameters
   agent.describe_resource("Observation")

   # Generate from criteria
   agent.generate("Patient", {"gender": "male"}, count=10)
   # → Patient?gender=male&_count=10

   # Date comparator
   agent.generate("Observation", {
       "status": "final",
       "date": {"comparator": "ge", "value": "2024-01-01"},
   })

   # Built-in intent templates
   agent.generate_from_intent("Patient", "male patients")

Workflow integration
--------------------

Pass ``query_generation`` instead of ``query_url``:

.. code-block:: python

   {
     "query_generation": {
       "resource_type": "Patient",
       "criteria": {"gender": "male"},
       "count": 10
     }
   }

Or with intent:

.. code-block:: python

   {"query_generation": {"resource_type": "Patient", "intent": "male patients"}}

The engine stores the result in ``generated_query`` and sets ``query_url`` before
validation runs.

Demo
----

.. code-block:: bash

   make demo-query-generator
   python3 scripts/demo_query_generator.py --describe --resource Patient