# AGENTS.md (repo root)

## Purpose
This repository hosts a Linux-deployable, enterprise-serious bot trading platform scaffold.

## Read first
1. `README.md`
2. `docs/product-vision.md`
3. `docs/architecture.md`
4. `docs/decisions.md`
5. `docs/testing.md`
6. `docs/deployment.md`
7. `docs/operations.md`
8. `docs/adapter-interface.md`

## Architectural stance (non-negotiable)
- Modular platform and service-oriented code organization; **not** microservice sprawl.
- Central execution/risk/OMS spine owns order state and exchange-side lifecycle.
- Strategies are isolated workers that emit intents, never direct exchange execution.
- Durable event backbone starts with Postgres-backed events/outbox before Kafka.
- Linux server + Docker Compose is the primary deployment path.
- No dependency on a separate AI/agentic repository.

## Repository structure
- `app/core`: cross-cutting kernel (settings, logging, event contracts, id/time helpers).
- `app/domain`: trading domain language and invariants.
- `app/infrastructure`: concrete adapters for storage, brokers, exchanges, market data.
- `app/services`: runtime services (`api`, `strategy_runner`, `execution_engine`, `reconciler`, `simulation`).
- `app/interfaces`: inbound entrypoints (HTTP/CLI).
- `app/tests`: tests.
- `docs`: architectural and operational documentation.

## Key invariants
- No direct strategy-to-exchange order placement.
- Order lifecycle authority is centralized in execution core.
- Use strict typing and explicit boundaries.
- Favor append-only event records and idempotent handlers.
- Postgres-first; SQLite is not a production baseline here.

## Validation commands
- `make format`
- `make lint`
- `make typecheck`
- `make test`
- `make check`

## Scoped guidance
- `app/AGENTS.md`: app-wide layering rules.
- `app/core/AGENTS.md`: kernel concerns only.
- `app/domain/AGENTS.md`: domain purity and invariants.
- `app/infrastructure/AGENTS.md`: implementation details and adapters.
- `app/services/AGENTS.md`: orchestration/runtime rules.
- Service-specific AGENTS files in each `app/services/*` subtree.
- `app/tests/AGENTS.md`: testing policy.

## Working norms
- Keep changes small and composable.
- Update docs alongside architecture-impacting code.
- Add tests with behavior changes.
- Prefer explicit interfaces over implicit coupling.
- Avoid introducing distributed complexity prematurely.
