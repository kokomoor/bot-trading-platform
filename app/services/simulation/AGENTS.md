# app/services/simulation/AGENTS.md

## Purpose
Simulation feed and paper-trading runtime support.

## Invariants
- Simulated fills should drive the same execution state updates as live adapters.
- Feed generation must be deterministic for tests.

## Extension guidance
- Add replay feeds and scenario fixtures for regression testing.
- Keep interfaces compatible with future real market data adapters.
