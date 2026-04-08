# app/services/simulation/AGENTS.md

## Subtree purpose
Simulation runtime for dry-run and paper execution pathways.

## Belongs here
- Simulated fills/execution behavior
- Deterministic replay scenarios
- Sandboxed strategy/service integration testing support

## Does not belong here
- Production adapter implementations
- Live account mutation logic

## Invariants
- Simulation behavior should be reproducible under fixed seeds/inputs.
- Contract compatibility with live execution interfaces.

## Testing expectations
- Reproducibility and contract parity tests.

## Common mistakes
- Diverging simulation contracts from production execution contracts.
- Embedding production secrets/config usage.

## Extension guidance
- Add scenario fixtures and time-control abstractions.
