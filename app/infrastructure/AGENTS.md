# app/infrastructure/AGENTS.md

## Subtree purpose
Concrete technical implementations for persistence, messaging, and external providers.

## Belongs here
- Repository implementations
- Database wiring and migrations integration
- Redis/cache integrations
- Broker/exchange/data-provider adapter implementations

## Does not belong here
- Domain rule ownership
- API route orchestration logic

## Invariants
- Infrastructure translates to/from domain contracts; it does not redefine them.
- Failures should map to well-defined error types.

## Testing expectations
- Integration tests with realistic infra dependencies or test containers.
- Idempotency and retry behavior tests for adapter code.

## Common mistakes
- Leaking vendor payloads beyond this layer.
- Tight coupling between one adapter and unrelated services.

## Extension guidance
- Add adapters behind stable interfaces and keep provider specifics isolated.
