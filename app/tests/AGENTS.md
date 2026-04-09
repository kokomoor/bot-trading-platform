# app/tests/AGENTS.md

## Purpose
Validate correctness, recovery behavior, and operations safety.

## Required expectations
- Unit tests remain fast and deterministic.
- Integration tests use live Postgres/Redis service assumptions.
- Reconciliation, replay, idempotency, and kill-switch paths require coverage.

## CI assumptions
- Integration tests run with `BTP_TEST_DATABASE_URL` configured.
- Migration checks run against fresh Postgres in CI service containers.

## Validation commands
- `pytest -m "not integration"`
- `pytest -m integration`
- `ruff check .`
- `mypy app`
