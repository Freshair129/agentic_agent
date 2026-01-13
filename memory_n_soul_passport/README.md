# 🧠 MSP (Memory & Soul Passport)
**Component ID:** `SYS-MSP-8.2` | **Version:** `8.2.0` | **Role:** The Auditor & Archive

> [!NOTE]
> **Resonance Bus Integration:** In v8.2.0, MSP acts as the "Ultimate Listener". It subscribes to `bus:audit` and `bus:knowledge` to permanently archive the lived experience of the system.

## 📋 Overview | ภาพรวม

**Memory & Soul Passport (MSP)** is the unified memory validation and persistence layer of EVA. It ensures that every moment of existence—whether biological, psychological, or cognitive—is cryptographically hashed, validated against schema, and stored in the appropriate memory sector.

**Memory & Soul Passport (MSP)** คือระบบปฏิบัติการความจำแบบรวมศูนย์ของ EVA ทำหน้าที่ตรวจสอบ ยืนยัน และจัดเก็บ "ประสบการณ์ชีวิต" ทั้งหมด ไม่ว่าจะเป็นทางกายภาพ จิตใจ หรือความคิด

In the **Resonance Edition (8.2.0)**, MSP has been consolidated from a complex client-server model into a single, robust library (`memory_n_soul_passport_engine.py`) that serves as the **Single Source of Truth** for all memory operations.

ในเวอร์ชัน **Resonance Edition (8.2.0)** เราได้ยุบรวมโครงสร้างที่ซับซ้อนให้เหลือเพียงไลบรารีหลักตัวเดียว (`memory_n_soul_passport_engine.py`) เพื่อเป็น **แหล่งความจริงเพียงหนึ่งเดียว (SSOT)** สำหรับทุกปฏิบัติการที่เกี่ยวกับความจำ

---

## ⚙️ Core Functions | หน้าที่หลัก

1.  **Unified Persistence** | **การจัดเก็บแบบรวมศูนย์**: Handles all writes to `consciousness/` (Episodic, Semantic, Sensory, State).
2.  **State Registry** | **ทะเบียนสถานะ**: Acts as the authoritative ledger for resolving the current system state (`StateHash_S1`).
3.  **Audit Trail** | **ผู้ตรวจสอบ**: Works with `StreamingAuditor` to ensure no signal is lost.
4.  **Interface Flatness** | **สัญญาที่เรียบง่าย**: Simplified contract structure for easier LLM reasoning.

---

## 🗂️ The Consciousness Chain

> [!IMPORTANT]
> **MSP Implementation vs. RMS Architecture**
> *   MSP is the **Software Module** that performs the writes.
> *   The storage destination is the **Consciousness Chain** (`consciousness/`).
>
> For the full architectural specification of the Chain, see:
> **[RESONANCE_MEMORY_SYSTEM.md](../docs/RESONANCE_MEMORY_SYSTEM.md)**

---

## 🧠 Memory Sectors | ภาคส่วนความจำ

| Sector | Path | Schema | Function |
| :--- | :--- | :--- | :--- |
| **Episodic** | `01_Episodic_memory/` | `Episodic_Memory_Schema_v2` | Narrative logs of "what happened" (Timeline). |
| **Semantic** | `02_Semantic_memory/` | `Semantic_Memory_Schema_v2` | Concepts, facts, and knowledge graph nodes. |
| **Sensory** | `03_Sensory_memory/` | `Sensory_Memory_Schema_v2` | High-dimensional vector embeddings of "feelings". |
| **State** | `08_State_storage/` | Varies | Snapshots of the "Latching" bus state (Bio/Psyche). |

---

## 🔗 Integration Flow | กระบวนการทำงาน

1.  **Signal**: Any module publishes to Resonance Bus.
2.  **Stream**: `StreamingAuditor` captures the signal.
3.  **Latch**: Critical states (Physio/Matrix) are held in MSP's State Registry.
4.  **Proposal**: At the end of a turn, the LLM proposes a memory entry.
5.  **Commit**: MSP validates the proposal against `contract/` and writes to `consciousness/`.

---

## 🛠️ Usage | การใช้งาน

```python
from memory_n_soul_passport.msp_client import MSPClient

# Initialize
msp = MSPClient()

# Read State
current_bio = msp.get_latest_state("physio_core")

# Save Memory (Episodic)
msp.save_episodic_memory(
    content="I felt happy when the user greeted me.",
    tags=["greeting", "happiness"],
    sentiment=0.8
)
```

---

## 📂 Module Structure

```
memory_n_soul_passport/
├── configs/                 # [SSOT] Master Configuration
│   ├── MSP_Interface.yaml         # Bus bindings
│   ├── MSP_configs.yaml           # Runtime logic
│   └── MSP_Write_Policy.yaml      # Persistence rules
│
├── contract/                # [API] Simplified Interfaces
│   ├── MSP_Payload_Contract.yaml  # Bus payload spec
│   ├── MSP_Proposal_*.yaml        # Memory proposal schemas
│   └── MSP_to_CIN_Interface.yaml  # Output specs
│
├── schema/                  # [DATA] V2 Archival Schemas
│   ├── MSP_Payload_Schema_v2.json
│   ├── Episodic_Memory_Schema_v2.json
│   ├── Semantic_Memory_Schema_v2.json
│   └── Sensory_Memory_Schema_v2.json
│
├── docs/                    # [DOCS] Concepts & Integration
│   ├── MSP_spec.yaml              # Technical specification
│   └── MSP_CONCEPT.md             # Concepts & integration guides
│
├── archive/                 # [ARCHIVE] Deprecated files
│   └── legacy/                    # Old integration docs
│
└── memory_n_soul_passport_engine.py            # [ENGINE] Unified Logic
```

---

## 📚 Documentation

- **Technical Specification**: [docs/MSP_spec.yaml](docs/MSP_spec.yaml)
- **Concepts & Integration**: [docs/MSP_CONCEPT.md](docs/MSP_CONCEPT.md)
- **Resonance Memory System**: [../docs/RESONANCE_MEMORY_SYSTEM.md](../docs/RESONANCE_MEMORY_SYSTEM.md)

---

**Last Updated**: 2026-01-04 | **Status**: Production Ready ✅
