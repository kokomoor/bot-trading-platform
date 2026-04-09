# Deployment

## Services
- `api`: operator/admin HTTP and health/readiness/metrics
- `strategy-runner`: strategy loop and intent generation
- `reconciler`: state truth checks against adapter views
- `postgres`, `redis`: persistence and coordination dependencies

## Startup checklist
1. Apply migrations: `alembic upgrade head`
2. Start stack: `docker compose up --build -d`
3. Validate `/health` and `/ready`
4. Verify `/admin/adapter-health`

## Safe restart expectations
- Execution startup performs pending-order recovery tagging.
- Duplicate intent IDs are handled idempotently.
- Kill switch state is checked before accepting new intents.
- Reconciliation should be run after restart to detect drift.
