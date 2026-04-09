# app/services/strategy_runner/AGENTS.md

## Purpose
Isolated strategy runtime that consumes market data and emits intents.

## Invariants
- Never call venue adapters directly from strategies.
- Every intent includes strategy/deployment/account metadata and idempotency key.
- Strategy loops must be replayable with deterministic feed inputs.

## Extension guidance
- Add new strategies via the strategy protocol.
- Keep market-data ingestion and intent emission separate from execution.
