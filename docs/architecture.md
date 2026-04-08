# Architecture

## Overview
The platform follows a **modular monolith with service-oriented runtimes** approach:
- one repository
- clear bounded modules
- separately runnable service processes/containers where useful
- shared domain model and contracts

This avoids both monolithic tangling and premature microservice fragmentation.

## Core layers
- **Core**: shared settings, structured logging, common contracts/utilities.
- **Domain**: business language and invariants (orders, fills, positions, risk intents).
- **Infrastructure**: technical integrations (DB, cache, adapters, messaging implementation).
- **Services**: runtime orchestrators (`api`, `strategy_runner`, `execution_engine`, `reconciler`, `simulation`).
- **Interfaces**: inbound transport adapters (HTTP, CLI).

## Execution and risk spine
- Strategies produce **intents** (desired actions).
- Execution/risk core validates and authorizes transitions.
- Only execution core can own order lifecycle and external placement responsibility.

## Event backbone
- Durable DB-backed event/outbox pattern first.
- Event records are append-oriented and idempotent to replay safely.
- Kafka or external bus can be added later only when justified by scale/throughput constraints.

## Deployment model
- Primary target: Linux server + Docker Compose.
- Postgres and Redis as foundational infrastructure.
- Runtime services isolated by process/container.
