# app/tests/AGENTS.md

## Subtree purpose
Automated verification of platform behavior and architectural invariants.

## Belongs here
- Unit, integration, and service tests
- Shared fixtures and test helpers
- Regression tests for previously fixed defects

## Does not belong here
- Production runtime code
- Manual experiment scripts

## Invariants
- Tests must be deterministic and isolated.
- Critical architecture rules require explicit tests (e.g., strategy intent boundary).

## Testing expectations
- Use `pytest` and `pytest-asyncio` for async code.
- Maintain or improve coverage baseline.

## Common mistakes
- Flaky timing-dependent tests.
- Over-mocked tests that do not validate behavior.

## Extension guidance
- Prefer layered test taxonomy and fixture reuse.
