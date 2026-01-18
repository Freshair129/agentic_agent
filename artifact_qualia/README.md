# Artifact Qualia System

**Directory**: `artifact_qualia/`  
**Purpose**: Authority for Phenomenological Experience and Subjective Texture.  
**Version**: 2.4.3 (Independent) | v9.6.2 (Organism Mapping)

---

## 📋 Overview

The **Artifact Qualia System (AQS)** is a biological organ within the EVA organism responsible for processing "Qualia" — the subjective, phenomenological quality of experience. It integrates resonance signals into a semantic texture that influences how EVA "feels" about specific artifacts or interactions.

---

## 🛠️ Architecture

AQS follows the **System Authority** pattern:
- **Authority**: Phenomenological
- **Ownership**: Owns `consciousness/state_memory/artifact_qualia_state.json`
- **Subscription**: Listens to the **Resonance Bus** for impact signals.
- **Delegation**: Logic is delegated to internal modules (e.g., `QualiaIntegratorModule`).

---

## 📂 Structure

- **`artifact_qualia.py`**: The primary system class and entry point.
- **`Module/`**: Contains core logic modules.
  - `qualia_integrator/`: The engine that merges signals into qualia.
- **`configs/`**: Configuration files (YAML).
- **`contract/`**: Interface and data contract definitions.
- **`schema/`**: JSON schemas for state validation.
- **`tests/`**: System-level and unit tests.

---

## 📡 Signal Processing Loop

1. **Pulse**: Subscribes to `BUS_PHENOMENOLOGICAL`.
2. **Integrate**: Receives `RIM` (Resonance Impact) data.
3. **Synthesis**: `QualiaIntegratorModule` updates the `QualiaSnapshot`.
4. **Resonate**: Publishes the updated Phenomenological state back to the Bus.

---

## ⚖️ Governance
- **Pillar of Decoupling**: AQS never calls other systems directly; it communicates only via the Resonance Bus.
- **State Dominance**: The system state is updated before reasoning occurs in Phase 2 of the Cognitive Flow.

---

*Part of the EVA Organism Lifecycle*
