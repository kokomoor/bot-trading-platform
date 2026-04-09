# Deployment

## Target
Single Linux server (Ubuntu/Debian) using Docker Compose.

## Prerequisites
- Docker Engine + Compose plugin
- Python 3.12 (for migration/admin scripts)
- `.env` configured from `.env.example`

## Bootstrap (Ubuntu/Debian)
1. Install Docker and Compose plugin.
2. Clone repo and copy environment file.
3. Run `scripts/deploy_linux.sh`.

## Standard deploy/update process
1. Pull latest code.
2. Run migrations: `alembic upgrade head`.
3. Rebuild/restart stack: `docker compose -f docker-compose.prod.yml up --build -d`.
4. Verify:
   - `/health`
   - `/ready`
   - `/admin/adapter-health`
   - `/admin/risk-config`

## Rollback process (practical baseline)
1. Keep previous image tags or previous git revision available.
2. Roll back code/image.
3. If required, apply `alembic downgrade -1` only when migration is known reversible.
4. Restart compose stack.

## Backup and recovery notes
- Postgres volume backup is required before production upgrades.
- At minimum, nightly `pg_dump` with retention policy.
- Restore rehearsal should be tested in staging.
- After restore/restart, run reconciler and inspect mismatch issues.
