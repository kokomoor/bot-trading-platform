# app/domain/AGENTS.md

## Subtree purpose
Pure trading domain language, invariants, and transition rules.

## Belongs here
- Domain entities/value objects.
- Order intent and order lifecycle semantics.
- Domain event envelopes and serialization contracts.
- Risk and reconciliation concepts.

## Does not belong here
- SQLAlchemy models.
- API transport DTOs.
- External API payload mappings.

## Invariants
- Strategies emit intents only; they never place orders directly.
- Order lifecycle transitions are validated by domain state rules.
- Domain event envelopes must remain stable, typed, and replay-friendly.

## Common mistakes
- Mixing database row structures into domain objects.
- Skipping transition validation and mutating order status ad hoc.
- Coupling domain events to queue/broker implementation details.

## Testing expectations
- Unit tests must cover valid/invalid order transitions.
- Event serialization/deserialization must be round-trip safe.

## Extension guidance
- Add domain modules per bounded context (accounts/orders/risk/etc.).
- Keep domain side-effect free.
