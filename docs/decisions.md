# Architectural Decisions

## ADR-001: Modular monolith + service-oriented runtimes
**Decision:** Keep one coherent codebase with explicit modules and selective process isolation.

**Why:** Minimizes coordination overhead while preserving runtime boundaries for critical workloads.

## ADR-002: Postgres-first persistence
**Decision:** Use Postgres as primary durable store from day one.

**Why:** Better transactional semantics, concurrency handling, and operational profile for trading workloads than SQLite.

## ADR-003: Durable outbox/event backbone before Kafka
**Decision:** Implement DB-backed event/outbox persistence before introducing a dedicated event broker.

**Why:** Ensures reliable event durability and replay with lower operational overhead at current stage.

## ADR-004: Strategy isolation
**Decision:** Run strategies in isolated processes/containers.

**Why:** Fault containment, independent scaling, and safer multi-strategy operation.

## ADR-005: Centralized execution ownership
**Decision:** Strategies emit intents only; execution core owns order state and placement authority.

**Why:** Prevents fragmented order state and inconsistent risk controls.

## ADR-006: Docker Compose first deployment
**Decision:** Optimize for Linux + Docker Compose; avoid Kubernetes-first assumptions.

**Why:** Pragmatic operations footprint for initial production targets.
