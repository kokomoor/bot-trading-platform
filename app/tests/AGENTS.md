# app/tests/AGENTS.md

## Subtree purpose
Automated verification of platform behavior, architecture invariants, and core infrastructure contracts.

## Belongs here
- Unit tests for pure core helpers (config/logging/ids/time/metrics).
- Persistence wiring tests for async engine/session setup.
- Service-level tests for health/readiness behavior and boundary contracts.

## Does not belong here
- Production runtime implementations.
- Manual-only scripts or notebooks.

## Invariants
- Tests must be deterministic and isolated.
- Core tests should not require network calls.
- Postgres-backed patterns are default for DB integration tests; SQLite is not the baseline.

## Testing expectations
- Use strict typing in tests.
- Keep `ruff`, `mypy`, and `pytest` green in CI.
- Add regression tests for every bugfix impacting platform guarantees.

## Common mistakes
- Over-mocking persistence boundaries.
- Relying on time-dependent nondeterministic assertions.

## Extension guidance
- Add fixture modules for shared infra setup.
- Separate pure unit tests from DB integration tests with explicit markers.
