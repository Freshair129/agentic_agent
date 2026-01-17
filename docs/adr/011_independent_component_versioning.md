# ADR-011: Independent Component Versioning Standard

- **Status**: Accepted
- **Decided by**: USER, Antigravity
- **Date**: 2026-01-17

## 1. Context & Problem

As EVA matures into a multi-component organism, maintaining a single global version (e.g., 9.4.3) across all subsystems becomes brittle. Changes in the `PhysioCore` logic shouldn't necessarily force a version bump in `AgenticRAG`. We need a way to track the development life-cycle of each "organ" independently while preserving their relative historical context.

## 2. Decision: Decoupled Logic-Based Mapping

We will implement an **Independent Versioning System** where each component maintains its own version number in `core_systems.yaml`.

To prevent "version shock" (resetting everything to 1.0.0) while moving away from the global 9.x.x numbering, we have adopted a **Legacy-Based Mapping Rule**:

- **Mapping Rule**:
  - `8.x.x` versions are mapped to `1.x.x` (e.g., 8.2.0 -> 1.2.0)
  - `9.x.x` versions are mapped to `2.x.x` (e.g., 9.4.3 -> 2.4.3)
  - Other versions (e.g., RMS 6.2.0) remain as-is.

## 3. Implementation Details

- **Authoritative Source**: `operation_system/configs/core_systems.yaml` is the single source of truth for all component versions.
- **Header Synchronization**: Every core system Python file must include its independent version in the docstring and initialization prints.
- **Documentation Synchronization**: All system-level documentation (`docs/04_Systems/` etc.) must reference the independent version in metadata.

## 4. Consequences

- **Positive**: Components can now evolve at different speeds. Version numbers now reflect the *logical* maturity and history of the component rather than just the global system state.
- **Negative**: Increased overhead in manually syncing version strings across files (partially mitigated by the Orchestrator reading from central config in the future).
- **Nuance**: Version numbers no longer match the "EVA 9.4" global release tags, requiring a clear mapping in the `CHANGELOG.md`.
