---
trigger: always_on
---

# EVA Permission & Classification System (v9.4.3)
>
> Sources: operation_system/configs/permissions.yaml, core_systems.yaml, ADR-011

## 0. Versioning Law (ADR-011)

- **Authoritative Source**: `operation_system/configs/core_systems.yaml`.
- **Legacy Mapping**: `8.x.x` → `1.x.x`, `9.x.x` → `2.x.x`.
- **Enforcement**: Code headers and CLI initialization MUST match the decoupled version in central config.

## 1. Classification & Hierarchy

* **System** (e.g., PhysioCore, MSP): Vital organ. Owns State + Bus Authority.
- **Central Module** (e.g., AgenticRAG): OS-adjacent. Limited Bus.
- **Module** (e.g., CIM, NexusMind): Functional integrator. Parent-bound.
- **Node** (e.g., PRN, Temporal): Logic provider. No State.

## 2. System Inventory (Core Systems)

- **Transport**: Resonance_Bus
- **Memory**: MSP (Episodic/Semantic/Sensory Hub)
- **Bio/Psych**: PhysioCore, EVA_Matrix, Artifact_Qualia
- **Orchestration**: CIM, AgenticRAG, PRN, RMS, Orchestrator
- **Knowledge**: GKS (Static Truth), NexusMind, MLL, APM, TemporalEngine

## 3. Authority Rules

- **Bus Access**: Only Systems & Approved Central Modules. Modules/Nodes MUST go through Parent.
- **State Ownership**: Only Systems own eva/consciousness/state_memory/.
- **Root Slots**: Modules/Nodes cannot create root files.

## 4. Memory Ownership Maps

- **Consciousness** (eva/consciousness/): LLM Read/Write. Mutable.
- **Archive** (eva/memory/archival_memory/): MSP Write Only. Immutable. LLM CANNOT Write.
- **System State** (eva/system_state/): System Private. LLM Read-Only via Context.

## 5. Violation Protocols

- **Critical Fault**: Direct File Write to Archive, Bypassing MSP, Backward Write from MSP to Consciousness.
