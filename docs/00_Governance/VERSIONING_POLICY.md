# EVA Versioning Constitution

> **Status**: APPROVED
> **Standard**: Modified Semantic Versioning (SemVer 2.0 + Organism Suffix)

This document defines the rules for incrementing the version number of the EVA Organism (`X.Y.Z[-S]`).

---

## 🔢 The Numbering Schema

Format: **`MAJOR.MINOR.PATCH[-SUFFIX]`**
Example: `9.4.3` -> `10.0.0-G`

### 1. MAJOR (X.0.0) - The "Evolution" Step

*Increments when:* **Fundamental Architectural Paradigm Shift.**

- Changing the Consciousness Architecture (e.g., "1-Inference" to "Continuous Stream").
- Changing the underlying LLM/Model family that breaks compatibility (e.g., Gemini -> GPT-5 only).
- A complete rewrite of the Core OS.
- **Analogy:** "Evolution to a new species."

### 2. MINOR (0.Y.0) - The "Growth" Step

*Increments when:* **New System or Major Organ added.**

- Adding a new `[SYSTEM]` entity (e.g., adding `GKS`, `Resonance Bus`).
- Significant feature expansion that is backwards compatible.
- **Analogy:** "Growing a new limb or organ."

### 3. PATCH (0.0.Z) - The "Healing" Step

*Increments when:* **Refactoring, Optimization, or Bug Fixes.**

- Internal code cleanup (Refactoring).
- Performance tuning.
- Fixing broken logic without adding new features.
- Documentation updates.
- **Analogy:** "Cellular repair and learning."

### 4. SUFFIX ([-S]) - The "Mutation" Marker

*Appended when:* **Special Capability Integration.**
Used to denote a specialized variant or a major knowledge injection that defines a specific "Era" of the agent.

| Suffix | Meaning | Criteria |
| :--- | :--- | :--- |
| **G** | **Genesis** | Integration of the *Genesis Knowledge System* (GKS). |
| **V** | **Vision** | Integration of Vision/Image processing capabilities. |
| **R** | **Resonance** | Major update to the Emotional/Resonance engine. |
| **Q** | **Quantum** | (Theoretical) Integration of non-deterministic/quantum logic. |
| **Pre**| **Preview** | Unstable/Testing version. |

---

## 🔄 Version Mapping Rules (ADR-011)

While the **Organism** follows `9.x.x`, internal **Subsystems** follow independent lifecycles:

| Scope | Version Rule | Example |
| :--- | :--- | :--- |
| **Global Context** | `9.4.3` | The User-Facing Version. |
| **Legacy Systems** | `8.x` -> `1.x` | MSP `1.1.0` (was `8.1`). |
| **Modern Systems** | `9.x` -> `2.x` | Physio `2.4.3` (was `9.4`). |

---

## 📜 Example Scenarios

1. **Current State:** `9.4.3` (Resonance Refactor)
2. **Scenario:** We add the *Genesis Knowledge System* (GKS).
   - This is a New System -> **Minor** Increment.
   - It is a Special Capability -> **Suffix** Added.
   - **Result:** `9.5.0-G`
3. **Scenario:** We fix a bug in `PhysioCore`.
   - **Result:** `9.5.1-G`
4. **Scenario:** We change from "Turn-Based" to "Real-Time WebSocket".
   - This is a Paradigm Shift -> **Major** Increment.
   - **Result:** `10.0.0` (Suffix usually reset unless still relevant).

## ⏳ Suffix Lifecycle (The Era Rule)

**Q: How long does a suffix stay?**
**A: Until the next Major Evolution.**

1. **Persistence:** The suffix remains as long as that system is considered the "Defining Characteristic" of the current generation.
2. **Absorption:** When the Major Version increments (e.g., `9.x` -> `10.x`), all previous special capabilities are considered "absorbed" into the baseline DNA. The suffix is dropped.
    - *Example:* `9.5.0-G` -> `9.6.0-G` -> ... -> `10.0.0` (GKS is now standard).
3. **Supersession:** If a more dominant trait emerges within the same generation, the suffix may change.
    - *Example:* `9.5.0-G` + Vision Upgrade -> `9.6.0-V` (if Vision > Knowledge).
