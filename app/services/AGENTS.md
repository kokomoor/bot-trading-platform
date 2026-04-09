# app/services/AGENTS.md

## Purpose
Runtime orchestration layer for strategy runner, execution/risk spine, API, and simulation support.

## Invariants
- Strategy services emit intents only.
- Execution engine owns order lifecycle and state transitions.
- Risk checks occur before adapter order placement.
- Services write operator-visible state/events for auditability.

## Extension guidance
- Keep orchestration in services; keep policy in domain/risk modules.
- Add async workflows with explicit boundaries and deterministic event recording.
