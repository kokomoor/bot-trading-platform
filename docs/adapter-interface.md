# Adapter Interface Principles

## Goal
Define stable contracts for integrating brokers, exchanges, and market-data providers without leaking provider-specific quirks into core domain logic.

## Adapter categories
- Execution adapters (order placement/cancel/status)
- Market data adapters (stream/snapshot)
- Account/portfolio adapters (balances, positions)

## Design constraints
- Domain-facing interfaces live in core/domain boundary.
- Provider-specific models stay in infrastructure implementations.
- All adapter operations should be idempotent where possible.
- Include correlation IDs and request IDs for traceability.

## Reliability expectations
- Explicit timeout/retry policies.
- Circuit-breaker/backoff hooks.
- Deterministic error taxonomy mapped to domain-level failure reasons.
