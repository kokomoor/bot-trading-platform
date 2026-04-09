# app/infrastructure/AGENTS.md

## Subtree purpose
Concrete technical implementations for persistence and external integrations.

## Belongs here
- Async SQLAlchemy engine/session wiring.
- DB metadata/base organization and migration integration.
- Redis and provider adapter implementations.
- Transaction helper patterns and persistence boundaries.

## Does not belong here
- Domain rule ownership.
- API handler code and request models.
- Service command orchestration.

## Invariants
- Postgres-first defaults (`postgresql+asyncpg`) for primary persistence.
- No synchronous SQLAlchemy session patterns in app code.
- Naming conventions on metadata must remain stable for migrations.
- Infrastructure translates to/from domain contracts, without redefining domain logic.

## Testing expectations
- Unit tests for engine/session wiring and transaction helpers.
- Integration tests should prefer real Postgres-backed workflows (no SQLite default path).

## Common mistakes
- Leaking provider payload shapes beyond infrastructure boundaries.
- Coupling adapters directly to interface layer.

## Extension guidance
- Keep adapter implementations isolated per provider.
- Add migrations when introducing persistence-bearing models.
