# 🧠 Orchestrator Module (EVA 8.2.0)
**Component ID:** `SYS-ORCH-8.2` | **Version:** `8.2.0` | **Role:** Central Decision Making & Flow Control

> [!NOTE]
> The Orchestrator is the "brain" of EVA, coordinating the entire dual-phase, one-inference cognitive loop. It acts as the conductor, ensuring seamless information flow between biological, psychological, and memory systems to generate embodied responses.

## 📋 Overview
The Orchestrator module is responsible for the overall execution flow of EVA's cognitive process. It implements the `Dual-Phase One-Inference` architecture, mediating between user input, internal biological/psychological states, memory retrieval, and LLM reasoning. Its primary engine is `orchestrator_engine.py`.

## ⚙️ Core Responsibilities
1.  **Dual-Phase Flow Management**: Orchestrates Phase 1 (Perception), `The Gap` (Embodied Processing), and Phase 2 (Reasoning) within a single LLM inference.
2.  **Module Coordination**: Initializes and manages instances of Physio Core, EVA Matrix, Artifact Qualia, CIN, Agentic RAG, and MSP, ensuring proper data exchange via the Resonance Bus.
3.  **Context Assembly**: Directs the Context Injection Node (CIN) to build rich, embodied prompts for the LLM.
4.  **Persistence**: Instructs MSP to archive turn-by-turn interactions and their associated internal states.

## 🔗 Key Sub-modules
*   **`cin/` (Context Injection Node)**: Handles the detailed construction of LLM prompts for both phases.
*   **`pmt/` (Prompt Rule Layer)**: Manages EVA's identity, behavioral constraints, and safety protocols.

## 📚 Documentation
For a deep dive into the `Dual-Phase One-Inference` architecture and the mechanics of `The Gap`, refer to:
*   [Dual-Phase Orchestration Details](docs/Dual_Phase_Orchestration_Details.md)

## 🗂️ Directory Structure (8.2.0 Standard)
```
orchestrator/
├── cin/                     # Context Injection Node
├── docs/                    # Conceptual Documentation
│   └── Dual_Phase_Orchestration_Details.md
│
├── pmt/                     # Prompt Rule Layer
├── orchestrator_engine.py     # Main Execution Loop
└── README.md                # This document
```

---

**Last Updated**: 2026-01-05 | **Status**: Production Ready ✅
