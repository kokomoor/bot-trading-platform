# Testing Strategy

## Test layers
- Unit tests: domain logic and invariants.
- Integration tests: DB/repository/event-outbox behavior.
- Service tests: runtime boundaries and orchestration behavior.

## Tooling
- `pytest`, `pytest-asyncio`, `pytest-cov`
- strict static analysis with `mypy`
- linting/format with `ruff`

## Quality gates
- Lint must pass.
- Type checks must pass.
- Tests must pass.
- Coverage is tracked and enforced with baseline threshold.

## Principles
- Tests should validate behaviors and invariants, not implementation trivia.
- Strategy intent flow and execution ownership boundaries must be explicitly tested.
