# app/services/api/AGENTS.md

## Subtree purpose
HTTP-facing API service runtime.

## Belongs here
- FastAPI app bootstrap
- Router registration and dependency wiring
- Read-only/admin endpoints as they evolve

## Does not belong here
- Core execution logic
- Direct adapter SDK calls in route handlers

## Invariants
- API delegates business workflows to application/domain services.
- Keep handlers thin and typed.

## Testing expectations
- Endpoint contract tests and startup/shutdown tests.

## Common mistakes
- Fat route handlers with business logic.
- Inconsistent API error mapping.

## Extension guidance
- Add versioned routes and clear DTO boundaries.
