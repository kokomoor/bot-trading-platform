# app/infrastructure/AGENTS.md

## Subtree purpose
Concrete persistence and integration implementations.

## Belongs here
- SQLAlchemy schema/models and migrations.
- Repository implementations.
- Durable event store/outbox persistence.

## Does not belong here
- Core domain policy and transition rules.
- API request/response models.

## Invariants
- Postgres-first async persistence only.
- Domain events are persisted durably before publication.
- Idempotency keys are enforced at storage boundary.

## Common mistakes
- Publishing events before DB commit.
- Encoding business decisions inside repository query methods.

## Testing expectations
- Persistence tests should use real Postgres when integration testing.
- Replay and outbox query behavior must be validated.

## Extension guidance
- Keep repositories narrowly focused and typed.
- Add indexes with every new high-cardinality query path.
