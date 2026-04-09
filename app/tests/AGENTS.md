# app/tests/AGENTS.md

## Purpose
Validate correctness, recovery behavior, and operational safeguards.

## Invariants
- Cover risk rejection/approval paths.
- Cover idempotency and restart-safety scenarios.
- Cover reconciliation mismatch detection and replay querying.
- Keep integration tests Postgres-backed when persistence behavior matters.

## Extension guidance
- Add focused tests for every new lifecycle transition.
- Prefer deterministic simulation fixtures for operational workflows.
