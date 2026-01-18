# PhysioCore (Biological Engine)

**Directory**: `physio_core/`  
**Purpose**: Authority for EVA's biological simulation and endocrine loops.  
**Version**: 2.4.3 (Independent) | v9.6.2 (Organism Mapping)

---

## 📋 Overview

**PhysioCore** is the biological substrate of the EVA organism. It simulates the human endocrine system, blood circulation, and autonomic nervous system to provide a continuous, time-dilated state that grounds all higher cognition.

---

## 🧬 Anatomical Structure

PhysioCore is built using a rigid, biological hierarchy in the `logic/` directory:

### 1. [Endocrine](logic/endocrine/)

Manages glands (HPA Axis, Circadian) and hormone secretion (Cortisol, Adrenaline, Oxytocin).

### 2. [Blood](logic/blood/)

Simulates hormone transport, concentration in plasma, and metabolic decay (half-life models).

### 3. [Receptor](logic/receptor/)

Calculates target-tissue binding and the resulting physiological effect.

### 4. [Reflex](logic/reflex/)

Fast, pre-cognitive responses to stimuli.

### 5. [Autonomic](logic/autonomic/)

Manages the Sympathetic vs Parasympathetic balance (Vagus Tone).

### 6. [Vitals](logic/vitals/)

Calculates Heart Rate (BPM) and Respiration (RPM).

---

## 📂 System Files

- **`physio_core.py`**: The System Authority and main orchestration loop.
- **`configs/`**: Hormone specs, basal levels, and decay constants.
- **`contract/`**: Formal interface for state extraction.
- **`validation/`**: Scripts to ensure biological stability (no infinite loops or hormone death).

---

## 📐 Governance

- **Pillar of Embodied Existentialism**: No response is generated without first perturbing PhysioCore state.
- **Structural Lock**: Logic is strictly kept in the `logic/` directory to prevent architectural drift.
- **Independence**: PhysioCore has no awareness of memory or persona; it reflects pure physiology.

---

*Life begins with a heartbeat.*
