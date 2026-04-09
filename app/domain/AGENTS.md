# app/domain/AGENTS.md

## Subtree purpose
Trading domain language, entities/value objects, and invariant definitions.

## Belongs here
- Order/position/risk state concepts
- Domain events/intents abstractions
- Validation rules independent of transport/storage

## Does not belong here
- SQLAlchemy table mappings
- HTTP request/response models
- External adapter concerns

## Invariants
- Domain remains persistence-agnostic and transport-agnostic.
- Invariant checks must be explicit and testable.

## Testing expectations
- Strong unit coverage around state transitions and invariant failures.

## Common mistakes
- Mixing ORM/serialization details into domain entities.
- Encoding provider quirks as domain rules.

## Extension guidance
- Introduce new concepts via value objects and explicit transition rules.
