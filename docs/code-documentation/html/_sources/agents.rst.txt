Agents
======

This page summarizes each specialist agent. See :doc:`api/index` for full
autodoc signatures.

CacheAgent
----------

Fetches and caches ``CapabilityStatement`` resources with hybrid invalidation:

* TTL-based expiry (default 7 days)
* Conditional requests with ``ETag`` / ``304 Not Modified``
* Auth-scoped cache keys via :func:`src.agentic_layer.auth.provider.auth_cache_suffix`
* Admin invalidation via ``FHIR_CACHE_INVALIDATE`` env vars

CapabilityInterpreterAgent
--------------------------

Transforms a raw CapabilityStatement JSON document into a lookup structure:

* Supported resource types
* Search parameter names, types, modifiers, comparators

QueryValidatorAgent
-------------------

Validates a ``query_url`` against the interpreted capability:

* Resource type support
* Parameter names, modifiers, comparators, chained parameters
* Pattern detection keyed by ``user_id`` + ``server_key``

QueryExecutionAgent
-------------------

Executes validated queries using :mod:`src.agentic_layer.utils.url_safety`:

* Rejects absolute ``query_url`` values
* ``follow_redirects=False`` on outbound HTTP
* Forwards Bearer / OAuth headers from :func:`src.agentic_layer.config.settings.get_auth_headers`

RuleAgent
---------

When pattern detection fires, decides ``learner``, ``human``, or ``none`` and
writes an audit record via :class:`src.agentic_layer.utils.audit_log.AuditLog`.

SearchLearnerAgent
------------------

Produces user-facing guidance and example queries using CapabilityStatement
metadata and validation errors.

HumanInterventionGate
---------------------

Implements pause → notify → review → resume:

* Classifies severity (low / medium / high / critical)
* Stores pending reviews in memory
* :meth:`~src.agentic_layer.agents.human_gate.HumanInterventionGate.submit_review_decision`
  supports optional operator auth (see :doc:`security`)

QueryGeneratorAgent
-------------------

See :doc:`query_generator`.