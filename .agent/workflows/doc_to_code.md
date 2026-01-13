---
description: Standard Protocol for implementing features ensuring Documentation and Config precede Code.
---

# Doc-to-Code Workflow

> **"Config is the Law. Code is the Enforcer."**

This workflow enforces the strict integrity protocol where Logic Parameters and Architecture must be defined in Documentation and Configuration BEFORE any Python code is written.

## 1. Phase 1: Legislation (The Blueprint)

- **Architecture:** Update `docs/EVA_9.4_Architecture.md` to reflect the new structure or logic flow.
- **Configuration:** Update `operation_system/configs/*.yaml` and *internal* module configs (e.g., `MSP_configs.yaml`) with new parameters, node classes, or feature flags.
  > [!IMPORTANT]
  > Configuration is not just about registry; it's about eliminating "Magic Strings" and Hardcoded Defaults in logic.
- *Outcome:* You have created "Ghost Keys" — configuration values that exist but are not yet used by code.

## 2. Phase 2: Execution (The Implementation)

- **Scaffold:** Create directories/files as defined in Architecture.
- **Implement:** Write the Python code.
- **Constraint:** All logic variables (timeouts, thresholds, paths) MUST be pulled from the `self.config` loaded validation. **NEVER Hardcode.**

## 3. Phase 3: Verification (The Audit)

- **Verify Config Binding:** Ensure the code successfully loads the new YAML keys without default fallbacks (referencing the YAML directly).
- **Verify Consistency:** specific implementation matches the description in `EVA_9.4_Architecture.md`.

## 4. Legislative Targets (SSOT Mapping)

Every change must be "legislated" in the following files before code execution:

| System Layer | Primary Configuration (Law) | Documentation (Intent) |
| :--- | :--- | :--- |
| **Arch Law** | [ARCH-LAW-001](docs/protocols/ARCHITECTURAL_STANDARDS.md) | `docs/protocols/ARCHITECTURAL_STANDARDS.md` |
| **OS / Bus** | `operation_system/configs/permissions.yaml` | `docs/EVA_9.4_Architecture.md` |
| **Identity** | `operation_system/configs/core_systems.yaml` | `docs/adr/007_centralized_identity.md` |
| **Memory (MSP)** | `memory_n_soul_passport/configs/MSP_configs.yaml` | `docs/systems/memory_n_soul_passport/MSP_CONCEPT.md` |
| **Bio (Physio)** | `physio_core/configs/PhysioCore_configs.yaml` | `docs/systems/physio_core/PhysioCore_Logic.md` |
| **Psyche (Matrix)** | `eva_matrix/configs/EVA_Matrix_configs.yaml` | `docs/systems/eva_matrix/matrix_logic_concept.md` |
| **Qualia (AQI)** | `artifact_qualia/configs/Artifact_Qualia_configs.yaml` | `docs/EVA_9.4_Architecture.md` |
| **Cognitive (CIM)**| `orchestrator/cim/configs/cim_configs.yaml` | `docs/orchestration/Dual_Phase_Orchestration.md` |
| **Prompt (PRN)** | `orchestrator/cim/prompt_rule/configs/PMT_configs.yaml`| `docs/adr/001_cim_prompt_transition.md` |
| **Knowledge (GKS)**| `genesis_knowledge_system/configs/GKS_configs.yaml` | `docs/systems/genesis_knowledge_system/GKS_Complete_Guide_V9.4.md` |
| **RAG** | `capabilities/services/rag_engine/configs/Agentic_RAG_configs.yaml` | `docs/capabilities/services/agentic_rag/Agentic_RAG_CONCEPT.md` |

---
*Run this workflow whenever adding new Systems, Modules, or major Logic flows.*
