# app/services/execution_engine/AGENTS.md

## Purpose
Central execution/risk spine.

## Invariants
- All intents flow through risk evaluation first.
- Execution engine updates order/position/balance state and emits durable events.
- Kill switch blocks new intents immediately.

## Extension guidance
- Keep adapter integrations normalized.
- Extend workflows (cancel/replace) with explicit event emissions.
