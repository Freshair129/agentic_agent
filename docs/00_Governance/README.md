# EVA v9.6.2 Documentation Hub (SSOT)

Welcome to the centralized documentation hub for **EVA v9.6.2 (Cognitive Flow 2.0)**. According to the **Doc-to-Code Protocol**, all architectural decisions and logic parameters must be defined here before implementation.

## 📂 Hierarchy Overview

- **[Architecture Standards](protocols/ARCHITECTURAL_STANDARDS.md)**: The LEGO manual of composition.
- **[System Architecture](03_Architecture/EVA_System_Architecture.md)**: The Master Blueprint (SSOT).
- **[Requirements](02_Requirements/EVA_Requirements_Specification.md)**: The Functional Spec.

### 🧠 [Orchestration](orchestrator/) (Cognitive Flow)

- **[Cognitive Flow 2.0](orchestrator/cognitive_flow/docs/Cognitive_Flow_2_0.md)**: Single-Inference Sequentiality.
- **[Stimulus Chunking v2.0](orchestrator/cognitive_flow/docs/STIMULUS_CHUNKING_PROTOCOL.md)**: LLM-Driven Emotion Pipeline.

### 🫀 Systems & Organs

- **[PhysioCore](systems/physio_core/)**: Body, Vitals, and Hormones.
- **[EVAMatrix](systems/eva_matrix/)**: 9D Psychological State.
- **[Artifact Qualia](systems/artifact_qualia/)**: Subjective Texture & Feeling.
- **[MSP (Memory)](systems/memory_n_soul_passport/)**: Identity and Persistence Layer.
- **[GKS (Knowledge)](systems/genesis_knowledge_system/)**: Static Wisdom and Master Blocks.

### 🛠️ [Capabilities](capabilities/) (Skills)

- **[Services](capabilities/services/)**: RAG, SLM Bridge, Vector DB.
- **[Tools](capabilities/tools/)**: Resonance Impact (RIM), Resonance Index (RI).

### 📜 [Protocols](protocols/) & [ADR](adr/) (Laws & Decisions)

- **[Doc-to-Code](protocols/DOC_TO_CODE.md)**: The integrity protocol.
- **[Version Control](00_Governance/VERSIONING_POLICY.md)**: Independent Component Versioning.
- **[Architecture ADRs](adr/)**: Historical record of design decisions.

---
> **Rule:** Never update code without checking if the corresponding document in this hub reflects the change.
