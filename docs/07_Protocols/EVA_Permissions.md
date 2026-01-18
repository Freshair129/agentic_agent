---
trigger: always_on
---

# EVA Permission & Classification System (v9.6.0)
>
> Sources: registry/eva_master_registry.yaml, ADR-011

## 0. Versioning Law (ADR-011)

- **Authoritative Source**: `registry/eva_master_registry.yaml`.
- **Legacy Mapping**: `8.x.x` → `1.x.x`, `9.x.x` → `2.x.x`.
- **Global Strategy**: v9.6.0 (Resonance Refined).
- **Enforcement**: Code headers, CLI initialization, and Subagent Manifests MUST match the registry.

## 1. Classification & Hierarchy

- **System Authority** (e.g., PhysioCore, Orchestrator, RMS): Owns state and has broad bus rights.
- **Core System** (e.g., EVA_Matrix, MSP, Artifact_Qualia): Essential for organism function; state-driven.
- **Central Module** (e.g., Resonance_Bus, Identity_Manager, AgenticRAG): Infrastructure-level services; often stateless or root-presence false.

## 2. System Inventory (Master Registry)

- **Transport**: Resonance_Bus (Central Module)
- **Memory**: MSP (Core System - Episodic/Semantic/Sensory), User_Registry (Logic Module)
- **Bio/Psych**: PhysioCore (System Authority), EVA_Matrix (Core System)
- **Phenomenology**: Artifact_Qualia (Core System)
- **Orchestration**: Orchestrator (System Authority), CIM (Core System), RMS (System Authority)
- **Epistemology**: GKS (Knowledge Authority), AgenticRAG (Central Module)

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
