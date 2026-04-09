# app/core/AGENTS.md

## Subtree purpose
Shared platform kernel used by every runtime service.

## Belongs here
- Typed configuration (`pydantic-settings`) and environment-aware helpers.
- Logging setup (`structlog`) and correlation-id context helpers.
- Observability primitives (Prometheus metric registry/helpers, health/readiness models).
- Deterministic ID helpers.
- Clock abstractions used by execution/reconciliation/simulation logic.

## Does not belong here
- Trading domain entities/state transitions.
- SQLAlchemy models or adapter implementations.
- Service-specific orchestration.

## Invariants
- `BTP_` environment variable prefix is mandatory for runtime settings.
- No hidden side effects at import time except immutable constants.
- Core APIs must stay strongly typed and deterministic.
- App code should log via `app.core.logging` wrappers, not direct stdlib logger usage.

## Testing expectations
- Validate settings parsing/validation paths and env prefix behavior.
- Validate ID and clock determinism/invariants.
- Validate metrics registration and health/readiness helpers.

## Common mistakes
- Putting broker/exchange semantics in core.
- Adding weakly typed dict-based config surfaces.
- Emitting plain prints instead of structured logs.

## Extension guidance
- Add narrow modules with explicit responsibility.
- Keep public API stable and update tests + docs with each new core contract.
