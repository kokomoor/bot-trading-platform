# app/services/strategy_runner/AGENTS.md

## Subtree purpose
Runtime host for isolated strategy processes/workers.

## Belongs here
- Strategy worker lifecycle management
- Intent emission pipelines
- Strategy sandboxing controls

## Does not belong here
- Direct order placement to exchanges
- Canonical order-state ownership

## Invariants
- Strategies emit intents only.
- Runner must be isolated and restart-safe.

## Testing expectations
- Worker lifecycle, crash recovery, and intent emission tests.

## Common mistakes
- Coupling strategy code to execution adapters.
- Hidden mutable shared state across strategy workers.

## Extension guidance
- Add pluggable strategy loading and clear isolation boundaries.
