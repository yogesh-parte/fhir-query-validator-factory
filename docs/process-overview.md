# Process Overview: Software Factory for Agentic Systems

This document provides a high-level view of the methodology followed in building the `fhir-query-validator-factory` demonstration.

## Mermaid Diagram: End-to-End Process

```mermaid
flowchart TD
    subgraph Human_Planning["Human-Centric Planning Layer"]
        P0[Phase 0: Ideation & Problem Definition]
        P1[Phase 1: Requirements & Structured Planning]
        P2[Phase 2: Architecture & Key Decisions<br/>+ ADRs + Specs]
        
        P0 --> P1
        P1 --> P2
    end

    subgraph Spec_Driven["Spec-Driven Development"]
        S1[Create Detailed Specifications<br/>docs/spec/]
        S2[Define Feedback Loops & Human Gates]
        
        P2 --> S1
        S1 --> S2
    end

    subgraph Implementation["Implementation Layer<br/>(Google ADK + Codex)"]
        I1[Phase 3: Scaffolding + Core Agents<br/>CacheAgent, Interpreter, Validator]
        I2[Phase 4: Loop Engineering<br/>Execution + Rule + Learner + Human Gate]
        
        S2 --> I1
        I1 --> I2
    end

    subgraph Observability["Traceability & Observability"]
        T1[Structured Logging]
        T2[Trace Reports<br/>demo_traceability.py]
        T3[Optional: Langfuse Integration]
        
        I2 --> T1
        T1 --> T2
        T2 --> T3
    end

    subgraph Knowledge["Knowledge Packaging"]
        K1[Generate OKF Knowledge Bundle<br/>using OKF skill]
        K2[Final Documentation & Demo Polish]
        
        T3 --> K1
        K1 --> K2
    end

    style Human_Planning fill:#e3f2fd,stroke:#1565c0
    style Spec_Driven fill:#fff3e0,stroke:#ef6c00
    style Implementation fill:#e8f5e9,stroke:#2e7d32
    style Observability fill:#f3e5f5,stroke:#7b1fa2
    style Knowledge fill:#e0f7fa,stroke:#00838f
```

## Process Summary

| Layer                        | Focus                              | Key Activities                              | Artifacts Produced                     |
|-----------------------------|------------------------------------|---------------------------------------------|----------------------------------------|
| **Human Planning**          | Upstream thinking                  | Ideation, Requirements, Architecture        | Planning files, ADRs, Specs            |
| **Spec-Driven Development** | Define behavior before code        | Write detailed agent specifications         | `docs/spec/*.md`                       |
| **Implementation**          | Build using ADK + Codex            | Develop specialist agents + workflow        | `src/agentic_layer/`                   |
| **Loop Engineering**        | Design feedback mechanisms         | Cache, Execution, Pattern → Learner/Human   | `docs/loop-engineering.md`             |
| **Observability**           | Make decisions visible             | Structured traces, optional Langfuse        | `scripts/demo_traceability.py`         |
| **Knowledge Packaging**     | Make knowledge reusable            | Generate OKF bundle                         | Structured knowledge documentation     |

## Core Principles Followed

- **Planning is the highest-leverage activity**
- **Spec-Driven Development** before implementation
- **Specialist Agents** over monolithic agents
- **Explicit Feedback Loops** (including meta-learning)
- **Human Oversight** at critical points
- **Traceability & Observability** by design
- **Knowledge as a first-class deliverable** (via OKF)

This process can be reused as a template for building other agentic systems in a disciplined, governable way.
