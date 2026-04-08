# bot-trading-platform

Enterprise-grade (but pragmatic) trading infrastructure scaffold for Linux server deployment.

## Scope of this initial scaffold
This repository currently provides:
- foundational architecture and repository conventions
- strict Python tooling baseline (ruff, mypy, pytest, coverage)
- Docker/Compose skeleton for core runtime services
- documentation for product, architecture, operations, deployment, and adapter contracts
- placeholder packages and entrypoints to support incremental implementation

It intentionally does **not** yet implement full trading logic, execution internals, adapter integrations, or reconciliation workflows.

## Core principles
- Modular, service-oriented codebase without microservice sprawl.
- Central risk/OMS/execution spine owns order state and exchange lifecycle.
- Isolated strategy runners emit intents rather than executing orders directly.
- Durable event backbone starts with Postgres-backed outbox/event records.
- Postgres-first persistence strategy.
- Linux + Docker Compose as first deployment target.

## Quick start
```bash
cp .env.example .env
make install
make check
make up
```

## Repository map
- `app/` — platform source code organized by layer and runtime service
- `docs/` — architecture and operating documentation
- `docker/` — service Dockerfiles
- `scripts/` — helper scripts for local/dev workflows
- `alembic/` — migration scaffolding
- `.github/workflows/` — CI baseline

## Validation
```bash
make format
make lint
make typecheck
make test
make check
```

## Current runtime scaffold
`docker-compose.yml` includes initial services:
- `api`
- `strategy-runner`
- `reconciler`
- `postgres`
- `redis`

## Next implementation steps (future work)
- define durable event contracts and outbox patterns
- implement execution engine and order state machine
- define adapter plugin interfaces and first concrete adapters
- implement reconciliation and operational runbooks in depth
