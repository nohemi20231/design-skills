---
name: software-architecture
description: Use when designing or reviewing system structure: layering, module and service boundaries, microservices, data ownership, integration patterns, and architecture decisions (ADRs).
---

# Software Architecture

This skill covers structure above the class level. For code-level quality, use the `clean-code` skill. For judging whether a design is good at any level (economics of change, minimalism, cohesion and coupling, non-functional requirements), use the `software-design` skill. Read and update the living diagram with the `architecture-diagram` skill.

## How to approach
1. **Clarify the drivers first.** Establish the following, and ask about any that are unknown and would change the answer:
   - functional scope
   - quality attributes: scalability, availability, latency, consistency, security, maintainability, and cost
   - constraints: team size and skills, deadlines, and existing systems
2. **Propose the simplest architecture that meets the drivers.** For significant decisions, present two or three options with their trade-offs.
3. **Record significant decisions as ADRs.**
4. **Define how success is verified**, using metrics and fitness functions such as ArchUnit rules, latency SLOs, and deploy frequency.

## Core principles
- **Dependency rule**: source dependencies point inward toward domain policy. The domain has no framework imports.
- **Separation of concerns**: high cohesion within modules, low coupling between them.
- **Explicit boundaries and contracts**: each module hides its internals behind a published interface.
- **Decompose by volatility**: isolate what is likely to change. Don't abstract everything.
- **Trade-offs**: every choice gives something up. Name what you give up.
- **Reversibility**: prefer decisions that are cheap to undo, and delay irreversible ones until the last responsible moment.
- **Conway's law**: align boundaries with team ownership.

## Structural styles
- **Layered** (controller, service, repository): fine for CRUD. Watch for leaking layers and anemic domains.
- **Hexagonal / clean architecture**: a domain core, ports (interfaces) defined by the core, and adapters for web, persistence, and messaging.
- **Package by feature over package by layer.**
- **Modular monolith**: the default for new products and small teams. Enforce module boundaries with tooling.
- **Microservices**: use only when independent deployability, independent scaling, or team autonomy justifies the operational cost.

## Domain-driven design
- Bounded contexts each have their own ubiquitous language.
- Map how contexts relate: upstream and downstream, anti-corruption layer, shared kernel.
- An aggregate is a consistency boundary. Keep aggregates small and reference other aggregates by ID.
- Use domain events for reactions across aggregates and contexts.

## Microservices checklist
- **Boundaries**:
  - Draw boundaries along bounded contexts and business capabilities, not technical layers.
  - Splitting by database table or noun is a smell.
- **Data**:
  - Each service owns its database.
  - No shared tables and no cross-service joins.
- **Communication**:
  - Use synchronous calls (REST or gRPC) for queries that need an immediate answer.
  - Use asynchronous events for propagating changes and decoupling services.
  - Avoid long chains of synchronous calls.
- **Consistency**:
  - Eventual consistency is the default.
  - Use sagas for multi-service workflows, choosing choreography or orchestration deliberately.
  - Use a transactional outbox for reliable event publishing.
  - Make consumers idempotent.
- **Resilience**:
  - Set a timeout on every remote call.
  - Retry with backoff and jitter, and only for idempotent operations.
  - Use circuit breakers, bulkheads, and fallbacks.
- **APIs**:
  - Version APIs and make changes backward-compatible by default.
  - Use consumer-driven contract tests.
- **Observability**:
  - Structured logs with correlation and trace IDs.
  - RED and USE metrics.
  - Distributed tracing.
  - Health and readiness probes.
- **Security**:
  - Authenticate at the edge and authorize in each service.
  - Give services their own identity for service-to-service calls (mTLS or JWT).
  - Keep secrets in a secrets manager.
- **Delivery**:
  - Each service has an independent pipeline.
  - Configuration is externalized.
  - Deploys have zero downtime.
- **Smells**:
  - Distributed monolith: services must deploy together.
  - Chatty services.
  - Shared libraries that carry domain models.
  - Shared database.
  - Nanoservices.

## Cross-cutting concerns
Handle each consistently across the system, through a platform library, gateway, or sidecar:
- caching
- configuration
- logging
- auth
- rate limiting
- feature flags

## Architecture decision record template
Store ADRs in `docs/adr/NNNN-title.md`:
- **Title**
- **Status**: proposed, accepted, or superseded
- **Context**: forces and constraints
- **Decision**
- **Alternatives considered**
- **Consequences**: positive and negative

## Output formats
- **For a design**, give these in order:
  1. the drivers
  2. the options and their trade-offs
  3. a recommendation
  4. a C4 context or container diagram in Mermaid
  5. risks and open questions
  6. ADRs for the key decisions
- **For a review**, order findings by impact: data integrity and correctness, then reliability, then scalability, then maintainability. For each finding, give:
  - the principle it violates
  - the consequence
  - the recommended change
  - the cost of making the change

## Spring Boot notes
- Enforce module boundaries with Spring Modulith or ArchUnit.
- Use Spring Cloud Gateway at the edge.
- Use Resilience4j for timeouts, retries, and circuit breakers.
- Use Micrometer with OpenTelemetry for metrics and tracing.
- Use Spring Cloud Stream or Spring Kafka for events, with an outbox table for reliable publishing.
