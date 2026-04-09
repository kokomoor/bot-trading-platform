# Testing Strategy

## Core test layers
- Unit tests: strategies, risk decisions, state transitions, replay queries.
- Service tests: execution end-to-end in simulation mode.
- API smoke tests: operator/admin endpoints and kill switch controls.
- Integration tests: repository behavior with real Postgres (`@pytest.mark.integration`).

## Commands
- `ruff check .`
- `mypy app`
- `pytest`
- Optional integration DB: set `BTP_TEST_DATABASE_URL`.

## Operational-hardening scenarios covered
- kill switch enforcement
- duplicate/idempotent intent handling
- reconciliation mismatch detection
- adapter health endpoint behavior
- replay query behavior
