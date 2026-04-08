# app/services/AGENTS.md

## Subtree purpose
Runtime process orchestration and application service entrypoints.

## Belongs here
- Service bootstrap
- Wiring dependencies and runtime loops
- Coordination between domain and infrastructure

## Does not belong here
- Core domain invariant definitions
- Provider API payload definitions

## Invariants
- Services orchestrate; domain decides business validity.
- Preserve central execution/risk authority model.

## Testing expectations
- Service-level tests for startup, shutdown, wiring, and process contracts.

## Common mistakes
- Embedding heavy business logic directly in service startup files.
- Allowing strategy services to bypass execution spine.

## Extension guidance
- Keep each service package focused on one runtime responsibility.
