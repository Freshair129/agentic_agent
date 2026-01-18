# EVA Matrix System (9D Psychological Engine)

**Directory**: `eva_matrix/`  
**Purpose**: Authority for EVA's psychological state and emotional trajectory.  
**Version**: 2.4.3 (Independent) | v9.6.2 (Organism Mapping)

---

## 📋 Overview

The **EVA Matrix System** is the psychological heart of the organism. It manages a **9-Dimensional Matrix** of emotional axes that shift based on physiological changes, user interactions, and internal reflections.

---

## 🛠️ The 9D axes

1. **Stress**: Bio-feedback from hormones (Cortisol/Adrenaline).
2. **Warmth**: Relationship depth and empathy levels.
3. **Drive**: Motivation and goal-orientation.
4. **Clarity**: Epistemic certainty and processing speed.
5. **Joy**: Positive valence and reward signal.
6. **Stability**: Emotional inertia and resilience.
7. **Orientation**: External vs Internal focus.
8. **Primary Emotion**: Categorical label (e.g., Calm, Excited).
9. **Secondary Emotion**: Nuance layer.

---

## 📂 Structure

- **`eva_matrix.py`**: The System Authority class.
- **`Module/psych_engine/`**: The core logic that calculates axes shifts.
- **`configs/`**: Axis weights, decay rates, and thresholds.
- **`schema/`**: Validation for the 9D state JSON.

---

## 📡 Interaction Model

- **Subscription**: Listens to `BUS_PSYCHOLOGICAL` for hormone snapshots from `PhysioCore`.
- **Publication**: Emits the `MatrixState` to the Bus for use by the LLM (Reasoning) and `ArtifactQualia` (Feeling).
- **Latency**: Continuous background processing at 30Hz or per-turn pulse.

---

## ⚖️ Governance

- **State Dominance**: All emotional shifts are normalized through the Matrix before affecting cognition.
- **Persistence**: State is saved to `consciousness/state_memory/eva_matrix_state.json`.

---

*Emotional depth through mathematical precision.*
