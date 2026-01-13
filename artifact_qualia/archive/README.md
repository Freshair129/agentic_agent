# Artifact Qualia (Phenomenological Experience Engine)
**Component ID:** `SYS-QUALIA-8.1` | **Version:** `8.2.0` | **Status:** GKS Standardized

## 📋 Overview
Artifact Qualia is the phenomenological "Sensation" layer of EVA. It transforms abstract psychological metrics (from EVA Matrix) and semantic impact (from RIM) into a subjective experience snapshot (Qualia), representing "what it is like" for the system in this moment.

**Version 8.2.0 Updates**:
- **System Wrapper (`artifact_qualia_engine.py`)**: Acts as the system authority with state persistence.
- **MSP State Bus Integration**: Automatically pulls psychological state from MSP and pushes qualia snapshots to the bus.
- **Persistence**: State is saved to `eva/consciousness/state_memory/artifact_qualia_state.json`.

## 🗂️ Directory Structure
- `configs/`: Standardized phenomenological mapping and principles.
- `contract/`: Upstream (Psyche/RIM) and Downstream (Orchestrator/MSP) definitions.
- `logic/`: Functional implementation (`Artifact_Qualia.py` and `artifact_qualia_engine.py`).
- `validation/`: JSON schemas for qualia snapshots and semantic input.

```
Artifact_Qualia/
├── README.md                          # This file
├── Artifact_Qualia.py                 # Core implementation
│
├── configs/                           # YAML specifications
│   ├── Artifact_Qualia_Spec_v8.1.yaml           # Comprehensive spec
│   ├── Artifact_Qualia_Input_Contract.yaml      # Input specification
│   ├── Artifact_Qualia_Output_Contract.yaml     # Output specification
│   └── Artifact_Qualia_Interface.yaml           # Interface specification
│
└── tests/                             # Unit tests (when implemented)
```

---

## Design Principles (from EVA 7.0)

### Core Principles

1. **"Qualia คือประสบการณ์ ไม่ใช่คำอธิบาย"**
   Qualia is experience, not explanation

2. **"ร่างกายส่งสัญญาณ ไม่ส่ง label"**
   Body sends signals, not labels

3. **"ทิศทางสำคัญกว่าค่าคงที่"**
   Direction matters more than absolute values

4. **"น้ำหนักเหตุการณ์แยกจากการแสดงออก"**
   Event weight is separate from expression

5. **"LLM ตีความเองจากสัญญาณ"**
   LLM interprets signals itself
