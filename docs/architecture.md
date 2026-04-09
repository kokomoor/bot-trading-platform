# Architecture

## Runtime path
Implemented simulation/paper flow:
- market feed -> strategy runner -> intent
- central risk check -> execution engine
- normalized adapter placement
- fill updates to orders/positions/balances
- durable event recording + operational replay
- reconciliation compares internal state to adapter truth

## Control boundaries
- Strategies never place orders directly.
- Execution engine is sole order lifecycle authority.
- Risk precedes placement.
- Reconciler emits mismatch events and issue records.

## Event/replay posture
- Postgres schema includes durable domain events/outbox fields.
- Replay tooling is read-oriented by default.
- Recovery replay mode is explicit and observable.

## CI/CD posture
- Separate CI jobs for lint, typecheck, unit tests, integration tests, migrations, docker builds, and security scans.
- Integration/migration jobs use service containers (Postgres/Redis) to validate real operational assumptions.
