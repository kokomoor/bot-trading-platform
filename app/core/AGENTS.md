# app/core/AGENTS.md

## Subtree purpose
Cross-cutting kernel concerns used by multiple modules.

## Belongs here
- Settings/config primitives
- Structured logging bootstrap
- Shared identifiers/time abstractions
- Domain-agnostic contracts/helpers

## Does not belong here
- Trading domain rules
- Broker/exchange-specific integration logic
- Service orchestration workflows

## Invariants
- Keep dependencies minimal and stable.
- No infrastructure-specific coupling.

## Testing expectations
- Deterministic unit tests for utilities and config parsing.

## Common mistakes
- Turning core into a generic dumping ground.
- Introducing business logic in shared utility code.

## Extension guidance
- Add focused modules with explicit usage boundaries.
