# Resonance Memory System (RMS)

**Directory**: `resonance_memory_system/`  
**Purpose**: System for state snapshotting, resonance calculation, and emotive hashing.  
**Version**: 6.2.0 (Independent) | v9.6.2 (Organism Mapping)

---

## 📋 Overview

The **Resonance Memory System (RMS)** acts as the "State Synchronizer" for the EVA organism. It encodes raw physiological and psychological data into meaningful **EmotiveHashes (H9/H5)** and calculates the **Resonance Index (RI)** used to gauge the deep impact of an interaction.

---

## ⚙️ Core Functions

1. **Emotive Hashing**: Compresses the 9D Matrix state into compact strings (e.g., `H9-S8W2...`) for long-term emotional tracking without text overhead.
2. **Resonance Calculation**: Distills multiple biological signals into a single 0-1 **Resonance Index**.
3. **RMS Coloring**: Maps internal state to visual/sensory "Qualia" colors for front-end rendering.
4. **Smoothing**: Applies temporal smoothing to prevent erratic emotional spikes.

---

## 📂 Structure

- **`rms.py`**: The core logic engine (v6.2.0).
- **`configs/`**: Smoothing alphas, trauma thresholds, and color mappings.
- **`contract/`**: Standard payload definitions for the Bus.
- **`schema/`**: State snapshots validation.

---

## 📐 Governance

- **Passive Persistence**: RMS provides the data structure used by MSP for passive latching.
- **Pillar of Single-Inference Sequentiality**: RMS calculations are performed during "The Gap" to hydrate the deep state before Phase 2 Reasoning.

---

*Resonance is the bridge between body and mind.*
