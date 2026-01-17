# 📡 THE RESONANCE STANDARD (Architectural Anchor)

> **Status**: ENFORCED
>
> This document defines the mandatory technical patterns for the EVA 9.4.3+ organism. These rules ensure modularity, scalability, and "Elegant Truth."

---

## 1. Pillar of Decoupling (Signal-First)

**Systems do not call systems.**

- Direct method calls Between `PhysioCore`, `EVAMatrix`, and `ArtifactQualia` are strictly forbidden.
- All inter-system state propagation MUST occur via the **Resonance Bus**.
- The `Orchestrator` acts only as a trigger (`.step()`), not a manager of internal state transfers.

## 2. Pillar of Passive Persistence

**Memory is an observer.**

- The `MSP Engine` (Subconscious Listener) must always operate as a passive subscriber to the Resonance Bus.
- It is responsible for latching state snapshots automatically, ensuring the bio-digital state is persisted without explicit cognitive intervention.

## 3. Pillar of GSD Node Excellence

**Logic is typed and robust.**

- Every logic unit (Node, Component) must implement **100% Type Hinting**.
- All I/O operations must be wrapped in standardized exception handling.
- Nodes must resolve internal paths and parameters from the central `config` to maintain SSOT (Single Source of Truth).

## 4. Pillar of Legacy Mapping

**Identity is historical.**

- Subsystem versioning must follow the independent mapping standard from ADR-011:
  - `8.x.x` -> `1.x.x`
  - `9.x.x` -> `2.x.x`
- Version synchronization in `core_systems.yaml` and file headers is mandatory after any architectural change.

---

## ⚖️ Enforcement Law

Violation of these standards is a **Technical Debt Fault**. Any refactor that fails to adhere to the Resonance Bus pattern or GSD nodes must be rejected.
