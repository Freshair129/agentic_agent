# 🧠 MSP (Memory & Soul Passport)

**Component ID**: `SYS-MSP` | **Version**: v9.6.2 (Cognitive Flow 2.0) | **Role**: The Auditor & Archive

---

## 📋 Overview

**Memory & Soul Passport (MSP)** is the operating system for EVA's memory. It ensures that every moment of existence — biological, psychological, or cognitive — is validated, hashed, and stored according to the **8-8-8 Distillation Protocol**.

In **v9.6.2**, MSP acts as the "Subconscious Observer," listening to the Resonance Bus and capturing state snapshots automatically (Latching).

---

## ⚙️ Core Responsibilities

1. **Subconscious Latching**: Automatically captures state from `physio_core` and `eva_matrix` via the Bus.
2. **Episodic Persistence**: Validates and writes "Episodes" (Turns) to `memory/archival_memory`.
3. **8-8-8 Distillation**: Manages the promotion of memory from **Session** (Tier 1) to **Core** (Tier 2) and **Sphere** (Tier 3).
4. **Epistemic Integrity**: Assigns confidence levels (`Hypothesis`, `Confirmed`) to memory fragments.
5. **Registry Management**: Maintains the authoritative `user_registry.json`.

---

## 🗂️ The Memory Stack (8-8-8 Protocol)

| Tier | Duration | Purpose | Location |
| :--- | :--- | :--- | :--- |
| **Tier 1 (Session)** | Turn/Session | Active interaction | `consciousness/episodic_memory` |
| **Tier 2 (Core)** | Cross-Session | Stable world model | `memory/core_memory` |
| **Tier 3 (Sphere)** | Eternal | Global bias / Wisdom | `memory/sphere_memory` |

---

## 📂 Structure

- **`memory_n_soul_passport_engine.py`**: The primary logic engine.
- **`Module/`**: Specialized modules for validation and distillation.
- **`configs/`**: Write policies and schema mappings.
- **`contract/`**: Formal interfaces for the memory proposal tool.
- **`schema/`**: JSON Schemas (V2) for all memory objects.

---

## 📐 Interaction Flow (v9.6.2)

1. **Observation**: MSP listens to Resonance Bus pulses.
2. **Snapshot**: Captures biological/psychological state into a "Latching Node."
3. **Proposal**: Receives Turn Metadata from the LLM via the `propose_episodic_memory` tool.
4. **Hydration**: System "hydrates" the proposal with authoritative bio-data.
5. **Final Commit**: Signed and written to long-term storage.

---

## ⚖️ Governance

- **Single Writer Rule**: MSP is the **only** component with write access to the `memory/` directory.
- **Passive Persistence**: Latching occurs without explicit LLM instructions to ensure biological continuity.

---

*Verified Memory. Unified Identity.*
