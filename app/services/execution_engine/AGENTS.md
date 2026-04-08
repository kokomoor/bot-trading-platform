# app/services/execution_engine/AGENTS.md

## Subtree purpose
Central execution and order lifecycle authority.

## Belongs here
- Intent validation and transition to executable orders
- Risk gate orchestration
- Order state machine ownership

## Does not belong here
- Strategy signal generation logic
- API transport concerns

## Invariants
- Single source of truth for order lifecycle.
- Idempotent processing and replay-safe transitions.

## Testing expectations
- Extensive state-transition tests and risk gate tests.

## Common mistakes
- Duplicated state transitions in other services.
- Non-idempotent handlers.

## Extension guidance
- Introduce explicit command/event contracts before adding features.
