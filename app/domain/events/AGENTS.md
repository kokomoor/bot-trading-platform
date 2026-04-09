# app/domain/events/AGENTS.md

## Purpose
Domain-level durable event envelope contracts and serialization behavior.

## Invariants
- Envelope fields are stable and replay-safe.
- Event payload/metadata must remain JSON-serializable.
- Correlation and causation identifiers are required for audit tracing.

## Boundaries
- No DB access logic here (belongs in infrastructure repositories).
- No transport/broker client code here.
