# app/AGENTS.md

## Subtree purpose
Application source root. Defines layered architecture boundaries and runtime service composition.

## Belongs here
- Core/shared primitives
- Domain concepts and invariants
- Infrastructure implementations
- Service orchestration
- Inbound interface adapters

## Does not belong here
- Ad-hoc scripts (use `scripts/`)
- Architecture decisions without docs updates (use `docs/`)
- Experimental notebooks or research artifacts

## Invariants
- Respect layer boundaries: domain must not import infrastructure.
- Service packages orchestrate; they do not redefine domain truth.
- Strong typing and explicit interfaces are mandatory.

## Testing expectations
- New behavior requires tests under `app/tests`.
- Boundary-heavy changes should include integration tests.

## Common mistakes
- Leaking vendor-specific models into domain.
- Building service-local "mini domains" that conflict with shared invariants.

## Extension guidance
- Add new bounded modules under the correct layer.
- Document architectural impacts in `docs/decisions.md`.
