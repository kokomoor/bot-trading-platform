# app/infrastructure/repositories/AGENTS.md

## Purpose
DB-backed repository implementations for domain aggregates and durable event/outbox storage.

## Rules
- Repositories persist domain state and envelopes; they do not implement business policy.
- Keep query filters explicit and index-aligned.
- Idempotency checks must be deterministic and transaction-safe.
- Event writes must be durable before publication attempts.

## Common mistakes
- Mixing API request schemas into repository interfaces.
- Emitting side effects (network calls) from repository methods.
