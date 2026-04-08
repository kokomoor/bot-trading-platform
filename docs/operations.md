# Operations

## Observability baseline
- Structured logs via `structlog`.
- Metrics exposure via `prometheus-client`.
- Service-level startup/shutdown logs required.

## Operational concerns
- Reconciliation loop for state divergence detection.
- Idempotent event handling and replay safety.
- Clear incident triage around execution and adapter boundaries.

## Runbook skeleton
- Verify service health and dependencies (Postgres/Redis).
- Check lag/backlog in event processing.
- Inspect reconciler mismatch counters and recent logs.
- Trigger controlled restart of isolated strategy workers when needed.
