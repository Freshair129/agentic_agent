# Resonance Index (RI)
**Component ID:** `SYS-RI-8.2` | **Version:** `8.2.0-S1` | **Status:** Production

## 📋 Overview | ภาพรวม

The **Resonance Index** module calculates the cognitive resonance score, representing how well the current experience aligns with stored memories and values.

**Resonance Index** คำนวณคะแนนความสอดคล้องทางปัญญา วัดว่าประสบการณ์ปัจจุบันตรงกับความทรงจำและค่านิยมที่เก็บไว้แค่ไหน

---

## ⚙️ Core Functions | หน้าที่หลัก

1. **Cognitive Alignment** | **ความสอดคล้องทางปัญญา**: Compare current state with historical clusters
2. **Emotional Congruence** | **ความสอดคล้องทางอารมณ์**: Match emotional states with memory tags
3. **Memory Similarity** | **ความคล้ายคลึงความทรงจำ**: Measure overlap with existing episodes

**Output**: `resonance_index` (0.0 - 1.0)

---

## 🔗 Integration Flow | กระบวนการทำงาน

1. **Input**: Receives cognitive state from **EVA Matrix** and memory clusters from **RMS**
2. **Calculate**: Computes RI from similarity scores
3. **Output**: Publishes RI to **bus:knowledge** for RMS, RIM, CIN, Orchestrator

---

## 📂 Module Structure

```
resonance_index/
├── configs/
│   ├── RI_Interface.yaml      # Bus bindings
│   └── ri_config.yaml          # Runtime params
├── contract/
│   └── RI_Payload_Contract.yaml
├── schema/
│   └── RI_Payload_Schema_v2.json
├── docs/
│   ├── RI_CONCEPT.md           # Integration guide
│   └── RI_Spec.yaml            # Technical spec
├── tests/                      # Unit tests
├── archive/                    # Legacy files
└── resonance_index_engine.py   # Calculation engine
```

---

## 📊 Key Specifications

- **Latency**: <50ms
- **State**: Stateless (Calculates based on inputs)
- **Consumers**: RMS, RIM, CIN, Orchestrator

---

**Last Updated**: 2026-01-05 | **Status**: Tier 2 Module ✅
