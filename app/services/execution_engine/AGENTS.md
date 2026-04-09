# app/services/execution_engine/AGENTS.md

## Purpose
Central execution/risk spine for submit/cancel/replace workflows.

## Invariants
- Strategies emit intents; execution engine owns order state.
- Risk checks must run before adapter calls.
- Idempotency keys must prevent duplicate submit side effects.
- Kill switch blocks new intents.
- Startup recovery must detect and mark stuck pending orders.

## Extension guidance
- Keep event emission around every lifecycle transition.
- Extend recovery logic before adding asynchronous adapters.
