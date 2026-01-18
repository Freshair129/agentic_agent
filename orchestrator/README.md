# 🧠 Orchestrator (The Nervous System)

**Component ID**: `SYS-ORCH` | **Version**: v9.6.2 (Cognitive Flow 2.0) | **Role**: CNS, Flow Control & Context Assembler

---

## 📋 Overview

The **Orchestrator** is the "Central Nervous System" of EVA. It coordinates the **Cognitive Flow 2.0** — a single-inference sequential process that simulates the transition from reflex (Perception) to processing (The Gap) to reasoning (Phase 2).

In **v9.6.2**, the Orchestrator has shifted from managing "Prompt Strings" to managing "File Containers" (The Context Injector Node).

---

## ⚙️ Core Responsibilities

1. **Flow Orchestration**: Executes the 3-phase loop (Perception -> Gap -> Reasoning).
2. **Context Assembly (CIM)**: Manages the `consciousness/context_container` by injecting and purging files turn-by-turn.
3. **Biological Synchronization**: Triggers the `sync_biocognitive_state` tool call.
4. **Resonance Management**: Monitors the Bus to determine when the "Deep State" is ready for Phase 2.
5. **Session Management**: Tracks `ConversationID` and `TurnIndex` via the OS Identity Manager.

---

## 🌀 Cognitive Flow 2.0

1. **Phase 1 (Perception)**: Initial reflex using SLM signals and immediate vitals.
2. **The Gap**: Wait for Physio-decay and Deep RAG recall.
3. **Phase 2 (Reasoning)**: LLM consumes the "Hydrated" context container.
4. **Phase 3 (Prediction)**: Post-turn prediction of future intent to prime next turn.

---

## 📂 Structure

- **`orchestrator.py`**: The main system class.
- **`cognitive_flow/`**: Rules and diagrams for the 2.0 flow protocol.
- **`cim/` (Context Injector Node)**: The engine that manipulates the `context_container/`.
- **`configs/`**: Runtime hooks and system sequence definitions.
- **`temporal/`**: Handles time-dilated biological processing.

---

## 📐 Interaction Pattern

The Orchestrator interacts with the LLM using a **Recursive Function Call** pattern:

- LLM calls `sync_biocognitive_state()` → Orchestrator executes Gap logic → Returns results → LLM continues.

---

## ⚖️ Governance

- **State Dominance**: The Orchestrator ensures no reasoning happens without fresh biological state.
- **Registry Authority**: The order of system execution is defined in `registry/eva_master_registry.yaml`.

---

*Orchestration is the art of synchronization.*
