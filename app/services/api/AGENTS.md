# app/services/api/AGENTS.md

## Purpose
Operator/admin HTTP surface.

## Invariants
- API reads/writes orchestration state but does not implement trading policy.
- Expose operational controls (kill switch) and visibility endpoints.
- Health/ready/metrics endpoints must remain lightweight.

## Extension guidance
- Add auth/token controls before internet exposure.
- Keep endpoint contracts stable and typed.
