# Architecture

## Operational slice now implemented
The platform supports an end-to-end simulation/paper path:
- market feed -> strategy runner -> intent emission
- central risk engine -> execution engine
- normalized adapter placement (simulation adapter)
- fills update positions/balances
- events recorded for operator visibility and replay

## Control boundaries
- Strategies never call venue adapters directly.
- Execution engine is the only order-state authority.
- Risk engine gates intents before placement.
- Reconciler compares internal state against adapter truth.

## Event and replay posture
- Durable event schema exists in Postgres (`domain_events` + outbox semantics).
- In-memory operational replay tooling supports safe read-mode by default.
- Recovery-mode replay is explicit and operator-invoked.
