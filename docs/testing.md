# Testing Strategy

## Validation matrix
- Lint: `ruff check .` and `ruff format --check .`
- Type: `mypy app`
- Unit/component tests: `pytest -m "not integration"` with coverage gate (80% in CI)
- Integration tests: `pytest -m integration` with Postgres/Redis service containers
- Migration verification: `alembic upgrade head` on fresh Postgres
- Docker verification: build API/runner/reconciler images
- Security checks: `pip-audit` + Trivy filesystem scan

## Integration assumptions
- Integration tests expect a live Postgres DSN via `BTP_TEST_DATABASE_URL`.
- CI provisions Postgres/Redis service containers.

## Operational-hardening scenarios covered
- kill switch enforcement
- duplicate/idempotent intent handling
- restart recovery tagging for pending orders
- reconciliation mismatch detection
- replay query behavior with explicit recovery mode
- adapter health endpoint behavior
