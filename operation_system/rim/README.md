# RIM Engine (Resonance Impact)

**Directory**: `operation_system/rim/`  
**Purpose**: Calculating numerical impact of emotional signals and salience anchors.  
**Version**: v9.6.2 (Cognitive Flow 2.0)

---

## 📋 Overview

The **RIM Engine** is a precision utility responsible for translating qualitative emotional data into quantitative impact scores. It converts the "Gut-Vector" and "Emotional Signal" from the SLM Bridge into a normalized **Resonance Impact (RIM)** value used throughout the organism's memory and bio-systems.

---

## ⚙️ Core Functions

1. **Impact Calculation**: Maps specific emotions (e.g., affection, jealousy) to a base impact score.
2. **Anchor Multipliers**: Adjusts the impact based on the "Salience Anchor" length and characteristics (e.g., shorter, punchier phrases may have higher impact multipliers).
3. **Clamping & Normalization**: Ensures all scores reside within the `[-1.0, 1.0]` or `[0.0, 1.0]` range as defined by governance constraints.

---

## 📂 Structure

- **`rim_engine.py`**: The core calculator logic.
- **`configs/`**: YAML definitions for emotion-to-score mappings and anchor multipliers.

---

## 📐 Governance

- **Single Source of Truth**: The `RIM_configs.yaml` is the authoritative map for how feelings weigh on EVA's state.
- **Objective Measurement**: Provides the "Authoritative System Impact" used during **System-Propelled Hydration**.

---

*Measuring the ripples of interaction.*
