# app/services/reconciler/AGENTS.md

## Purpose
Operational truth-check service for orders, positions, and balances.

## Invariants
- Reconciliation compares internal state with adapter-reported truth.
- Every mismatch must be recorded and event-emitted.
- Reconciliation should be safe to rerun and idempotent in behavior.

## Extension guidance
- Add severity rules carefully (high/medium/low semantics).
- Keep reconciliation side effects explicit and auditable.
