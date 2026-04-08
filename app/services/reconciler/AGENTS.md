# app/services/reconciler/AGENTS.md

## Subtree purpose
Detect and resolve divergence between internal state and external venues.

## Belongs here
- Periodic reconciliation workflows
- Mismatch detection and remediation triggers
- Reconciliation metrics/logging

## Does not belong here
- Primary order placement orchestration
- Strategy alpha logic

## Invariants
- Reconciliation must be safe to rerun.
- Side effects must be controlled and auditable.

## Testing expectations
- Deterministic mismatch scenarios and replay tests.

## Common mistakes
- Silent auto-corrections without audit trail.
- Non-deterministic reconciliation outcomes.

## Extension guidance
- Expand mismatch taxonomy and remediation policies incrementally.
