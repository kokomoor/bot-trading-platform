# AGENTS.md (repo root)

## Purpose
Linux-deployable, operator-first trading platform with central execution/risk authority.

## Architectural stance
- Modular monolith with service-oriented runtimes.
- Strategies emit intents only.
- Execution/risk spine owns order lifecycle.
- Postgres-first durable event/outbox model; no Kafka-first design.

## Required validation commands (before merge)
- `make lint`
- `make typecheck`
- `make test`
- `make integration-test` (requires Postgres test DSN)
- `make migrate`
- `make docker-build`

## CI expectations
- CI must run separate jobs for lint, typecheck, unit tests, integration tests, migration verification, docker builds, and security scans.
- Integration and migration jobs assume Postgres/Redis service containers.

## Working norms
- Keep changes typed and boundary-respecting.
- Prefer operational correctness over feature glitter.
- Update docs and AGENTS guidance with architectural/operational changes.
