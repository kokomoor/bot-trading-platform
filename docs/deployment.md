# Deployment

## Primary target
- Linux server (systemd optional)
- Docker Engine + Docker Compose v2

## Baseline services
- `api`
- `strategy-runner`
- `reconciler`
- `postgres`
- `redis`

## Environment setup
1. Copy `.env.example` to `.env` and adjust secrets/hosts.
2. Provision storage for Postgres and Redis volumes.
3. Build and start: `docker compose -f docker-compose.prod.yml up --build -d`.

## Hardening checklist (future iterations)
- TLS termination via reverse proxy.
- Secret injection via vault/host secret manager.
- Backup/restore policy for Postgres volumes.
- Healthchecks and restart/backoff policy tuning.
