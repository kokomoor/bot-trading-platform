# Operations

## Normal workflow
1. Start infrastructure and services (`api`, `strategy-runner`, `reconciler`).
2. Verify `/health`, `/ready`, and `/metrics`.
3. Confirm adapter health via `/admin/adapter-health`.
4. Confirm kill switch is disabled for normal flow.

## Incident workflow
1. Enable kill switch (`POST /admin/kill-switch/true`) to block new intents.
2. Inspect recent events (`/admin/events`) and order timelines (`/admin/orders/{id}/timeline`).
3. Run reconciler and inspect mismatches (`/admin/reconciliation/issues`).
4. Use replay query endpoint in read-only mode first.
5. Only use replay recovery mode with explicit operator decision.

## Reconciliation workflow
- Trigger on-demand reconciler (`btp-cli run-reconciler-once`) or periodic service run.
- Reconciler compares internal orders/positions/balances with adapter truth.
- Mismatches are stored and emitted as `reconciliation.mismatch_detected` events.

## Replay workflow
- Default replay is read-only inspection (`/admin/events/replay`).
- Recovery mode (`recovery_mode=true`) is explicit and marks replayed events.
- Use aggregate/account filters to keep blast radius small.
