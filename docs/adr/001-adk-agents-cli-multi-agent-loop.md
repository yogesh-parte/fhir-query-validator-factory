# ADR-001: Adopting Google ADK + agents-cli as the Core Agentic Platform with Multi-Agent Loop Design

**Status:** Proposed  
**Date:** 2026-06-28  

## Context
The original fhirqueryvalidator implements a focused but limited rule-based FHIR search query validator. We want to evolve it into a more general system that can validate any query parameter declared in a CapabilityStatement, execute valid queries, and intelligently handle repeated user errors through learning and human escalation.

## Decision
We will use **Google Agent Development Kit (ADK)** as the primary orchestration framework, supported by the official `agents-cli` tool.

Key elements:
- ADK Graph Workflows for orchestrating specialist agents
- `agents-cli` for scaffolding, development, and deployment
- Specialist agents: CacheAgent, CapabilityInterpreter, QueryValidator, QueryExecution, Rule Agent, Search Learner Agent
- Explicit human-in-the-loop gates
- Dual paths: Enterprise (ADK) and Lighter (direct Gemini API)

## Consequences

**Positive:**
- Strong alignment with Software Factory principles
- Rapid development via agents-cli
- Good support for multi-agent collaboration and feedback loops
- Credible enterprise positioning

**Negative:**
- Introduces dependency on Google ecosystem (mitigated by dual-path design)
- Slightly higher complexity for very simple use cases

## Alignment with Software Factory
This decision directly supports planning-first approach, specialist agents, explicit feedback loops, and meaningful human oversight.
