# Operations

## Normal workflow
1. Start services (`api`, `strategy-runner`, `reconciler`, `postgres`, `redis`).
2. Verify `/health`, `/ready`, and `/metrics`.
3. Verify adapter status via `/admin/adapter-health`.
4. Ensure kill switch state is expected.

## Incident workflow
1. Engage kill switch: `POST /admin/kill-switch/true`.
2. Inspect recent events (`/admin/events`) and order timelines.
3. Run reconciler (`btp-cli run-reconciler-once`) and inspect `/admin/reconciliation/issues`.
4. Use replay query in read-only mode first.
5. Only use replay recovery mode with explicit operator change ticket/runbook approval.

## Replay workflow
- Query: `GET /admin/events/replay?...`
- CLI: `btp-cli replay-events --limit 100`
- Recovery mode requires explicit opt-in (`--recovery-mode` or `recovery_mode=true`).

## Restart safety expectations
- Startup recovery marks pending orders as `stuck_pending` for operator attention.
- Duplicate intents are idempotent by idempotency key.
- Reconciliation should run after restart to detect state drift.

## Backup/recovery baseline
- Perform regular Postgres backups (e.g., nightly `pg_dump`).
- Test restore procedure periodically.
- After recovery: run migration check, then reconciler.
