# EVA — Embodied Virtual Agent

> **Version:** 9.7.0 | **Epoch:** Reflex | **Language:** Python 3.13

EVA คือ AI architecture แบบ Bio-Inspired ที่จำลองกระบวนการคิดและอารมณ์ของสิ่งมีชีวิต โดยใช้ระบบฮอร์โมน, สภาวะจิตวิทยา 9 มิติ และหน่วยความจำหลายชั้น ก่อนตอบสนองต่อ input ทุกครั้ง

---

## สารบัญ

- [Quick Start](#quick-start)
- [Architecture Overview](#architecture-overview)
- [Core Systems](#core-systems)
- [Key Features](#key-features)
- [API Reference](#api-reference)
- [Storage Architecture](#storage-architecture)
- [Configuration](#configuration)
- [Testing](#testing)
- [Versioning](#versioning)

---

## Quick Start

### Development Server (FastAPI)
```bash
cd api
python run_server.py
# Server runs on http://0.0.0.0:8000
```

### Lightweight Version (EVA Lite)
```bash
cd api
python eva_lite.py
```

### Web UI (Vue.js/Vite)
```bash
cd webui
npm run dev
```

### Run Tests
```bash
python -m pytest tests/
python -m pytest physio_core/tests/
python -m pytest eva_matrix/tests/
python -m pytest memory_n_soul_passport/tests/
```

### Health Checks
```bash
python scripts/check_versions.py         # Registry ↔ code version alignment
python scripts/check_doc_alignment.py    # Documentation consistency
python scripts/audit_msp_coverage.py     # MSP schema field coverage
python scripts/verify_physio_loop.py     # PhysioCore spike/decay validation
python scripts/verify_matrix_coupling.py # Matrix coupling check
```

---

## Architecture Overview

### Cognitive Flow 2.0 — Single-Inference Sequentiality

EVA ใช้ **LLM session เดียว** ตลอดทั้ง turn โดยไม่ตัด context ผ่านกลไก pause-resume:

```
User Input
    ↓
CNS (Orchestrator) → CIM (Context Assembler)
    ↓
CIM checks Engram (O(1) cache) + Body State (Resonance Bus)
    ↓
SLM (Llama-3.2-1B) → gut-feeling / intent extraction (System 1)
    ↓
LLM receives: Input + Body + Engram + Intent + Memory
    ↓
LLM calls sync_biocognitive_state()  ← THE GAP (LLM pauses here)
    ↓
PhysioCore: hormone cascade (23 chemicals, 30Hz)
    ↓
EVA Matrix: 9D psychological state update
    ↓
RMS: memory encoding (color, intensity, trauma protection)
    ↓
Agentic RAG: 7-stream deep recall (if needed)
    ↓
LLM RESUMES in same session with updated bio/emotion state
    ↓
LLM generates embodied response + writes self_note.md
    ↓
LLM calls propose_episodic_memory() → MSP validates & archives
```

> **Critical:** LLM ใช้ Tool Calling เพื่อ **อัปเดต internal state ของตัวเอง** ไม่ใช่ดึงข้อมูลภายนอก

### 5 Constitutional Pillars (ไม่เปลี่ยนได้)

| Pillar | Description |
|--------|-------------|
| **Embodied Existentialism** | ทุก response ต้องผ่าน PhysioCore state interaction |
| **Single-Inference Sequentiality** | 1 LLM session ต่อ turn เสมอ (pause-resume pattern) |
| **State Dominance** | organism state ขับเคลื่อนพฤติกรรม ไม่ใช่ external events |
| **Identity Integrity** | Persona: สงบ, ฉลาด, ล้อเล่นอ่อนโยน (cat-like) |
| **Tiered Wisdom (8-8-8)** | ความรู้ synthesized ผ่าน Session → Core → Sphere memory tiers |

---

## Core Systems

### 1. PhysioCore v2.4.3 — ระบบจำลองชีววิทยา

จำลองระบบชีววิทยาด้วย **23 สาร** ที่อัปเดต 30 ครั้ง/วินาที:

**16 Hormones (ESC_H prefix):**
Adrenaline, Cortisol, Aldosterone, Oxytocin, Vasopressin, Testosterone, Estrogen, Progesterone, Insulin, Glucagon, Leptin, Ghrelin, Thyroxine, Melatonin, Growth Hormone, Prolactin

**7 Neurotransmitters (ESC_N prefix):**
Noradrenaline, Dopamine, Serotonin, Endorphin, GABA, Adenosine, Histamine

**Features:**
- HPA Axis (stress response)
- Circadian rhythms (Melatonin)
- Receptor sensitization / desensitization
- Exponential hormone decay กลับสู่ baseline
- Reflex integration (fight/flight)
- Blood distribution (30Hz update cycle)

Config: `physio_core/configs/PhysioCore_configs.yaml` + `physio_core/configs/hormone_spec_ml.yaml`

---

### 2. EVA Matrix v2.5.0 — สภาวะจิตวิทยา 9 มิติ

แปลง hormone levels เป็น psychological state:

| Axis Type | Axes |
|-----------|------|
| **5 Core Affective** | Stress, Warmth, Drive, Clarity, Joy |
| **2 Meta-Directional** | Affective Stability (GABA − Adrenaline), Social Orientation (Oxytocin − Cortisol) |
| **2 Categorical** | Primary emotion, Secondary emotion (fear, anger, joy, sadness, disgust, surprise, calm) |

มี **dynamic momentum & inertia** ให้อารมณ์มีความต่อเนื่องตามธรรมชาติ

Config: `eva_matrix/configs/EVA_Matrix_configs.yaml`

---

### 3. Memory & Soul Passport (MSP) v2.1.0 — Central Memory Engine

Engine หลักสำหรับจัดการ memory ทั้งระบบ (2,633 lines):

- **Episodic Memory:** บันทึกบทสนทนา (episodes/, episodic_log.jsonl)
- **Semantic Memory:** ระบบความเชื่อ (hypothesis → confirmed)
- **Sensory Memory:** Qualia records
- **20 JSON schemas** สำหรับ validate data integrity
- **Multi-user support** ด้วย Thai name fuzzy matching

**Constitutional Principle:** LLM propose memories ผ่าน `propose_episodic_memory()` → MSP validates and writes เท่านั้น

---

### 4. Resonance Memory System (RMS) v2.5.0 — State Encoding

แปลง psychological state เป็น "สี" เพื่อเข้ารหัสความทรงจำ:

```
9D Matrix → 5D color axes (stress, warmth, clarity, drive, calm) → hex color
```

| Feature | Detail |
|---------|--------|
| Trauma Protection | threat > 0.85 → dim colors ×0.55, reduce intensity ×0.50 |
| Encoding Levels | L0_trace → L1_light → L2_standard → L3_deep → L4_trauma |
| Temporal Smoothing | color α=0.65, intensity α=0.70 |

---

### 5. Orchestrator v1.3.0 — Central Nervous System (CNS)

- **MasterFlowEngine:** ควบคุม cognitive flow pipeline ทั้งหมด
- **CIM (Context Injection Module):** hydrate files เข้า `consciousness/context_container/`
- **Prompt Rule Node:** Persona governance และ identity management
- **Session Node:** Session lifecycle, timeout management

---

### 6. Operation System — Infrastructure

| Component | Description |
|-----------|-------------|
| **Resonance Bus** | Pub/Sub global event bus (6 channels) |
| **Identity Manager v2.4.0** | Centralized ID factory — ห้าม hardcode constants |
| **LLM Bridge** | Gemini API (primary) + Ollama (fallback) |
| **Trajectory Manager** | Execution tracing |
| **NexusMind** | Reasoning engine |

**6 Bus Channels:** `bus:physical`, `bus:psychological`, `bus:phenomenological`, `bus:knowledge`, `bus:cognitive`, `bus:temporal`

---

## Key Features

### 4-Layer Affective Reflex System ⚡

แสดง "ปฏิกิริยาทางร่างกาย" แบบ real-time ก่อน LLM ตอบเสร็จ โดย **ไม่ใช้ LLM ตัวที่สอง:**

| Layer | Speed | Mechanism | Output |
|-------|-------|-----------|--------|
| 1. Enum Reflex | <1ms | Pattern match → hormone spike | Expression: flinch/blush/gasp |
| 2. SLM Gut | <50ms | gut_vector → nearest neighbor | Thai utterance: "อืม...", "ห๊ะ!?" |
| 3. Stimulus Extract | <50ms | SLM reads LLM tool args | Context-aware utterance |
| 4. CoT Extract | <50ms | SLM reads LLM thinking tokens | Most accurate utterance (optional) |

**Progressive Refinement Example:**
```
50ms  → "อืม..."        (gut guess)
550ms → "สูญเสีย..."   (from stimulus)
2.5s  → "ฉันเข้าใจ..." (full response)
```

---

### Stimulus Chunking Protocol v2.0 🧩

ตัด input ซับซ้อนเป็น "chunks" แล้วประมวลผล **ตามลำดับ** เพื่อรักษา emotional journey:

```
Input: "ขอบคุณนะ น่ารักมาก... ถ้าทำแบบนี้แค่คนเดียวก็คงดี"

❌ ไม่มี chunking: warmth=0.5, stress=0.5 → อารมณ์เฉลี่ย (แบน)

✅ มี chunking:
  chunk 1 "ขอบคุณ น่ารัก" → oxytocin ↑ → WebSocket: "☺️"
  chunk 2 "แค่คนเดียวก็คงดี" → cortisol ↑ → WebSocket: "...เดี๋ยวนะ"
```

---

### 7-Stream Agentic RAG 🔍

ดึง memory ด้วย 7 stream แบ่งเป็น 2 ระยะ:

**Quick Recall (30%, ขนานกับ PhysioCore):**
| Stream | Weight | Description |
|--------|--------|-------------|
| Narrative | 20% | Episode chains, story continuity |
| Intuition | 5% | Semantic graph patterns |
| Reflection | 5% | Meta-cognitive insights |

**Deep Recall (70%, หลัง bio state พร้อม):**
| Stream | Weight | Description |
|--------|--------|-------------|
| **Emotion** | **35%** | **Cosine similarity บน physiological vectors (KEY)** |
| Salience | 15% | Memories ที่มี RI > 0.70 |
| Sensory | 10% | Qualia texture matching |
| Temporal | 10% | Exponential decay (halflife 30 วัน) |

**Final step:** Deduplicate → SLM cross-encoder re-rank top 5

---

### Thai Name Matching 🌏

3-layer Thai-aware name matching:

1. **Word Segmentation** (pythainlp): แยกคำ — ป้องกัน "แอน" match ใน "แอนนี่"
2. **Prefix Stripping** (recursive): "คุณพี่แอน" → "พี่แอน" → "แอน" (16 Thai honorifics)
3. **Fuzzy Matching**: tone normalization (กิฟ ≈ กิ๊ฟ), edit distance ≤ 1-2, transliteration (Gift → กิ๊ฟ)

**Short name guard:** ชื่อ ≤ 2 ตัวอักษร ต้อง exact match เท่านั้น

---

### Engram System 🧠

Fast memory cache ที่ได้แรงบันดาลใจจาก DeepSeek's Conditional Memory:
- O(1) lookup สำหรับ frequent patterns
- Hash-based scalable lookups
- CIM checks Engram ก่อน RAG queries เพื่อประสิทธิภาพ

---

## API Reference

### Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/chat` | POST | Chat with EVA → `{response, emotional_state}` |
| `/api/health` | GET | `{status, agent_version, active_sessions}` |
| `/api/mind/state` | GET | `{eva_matrix, physio, qualia, resonance_index}` |
| `/ws/chat/{client_id}` | WebSocket | Full duplex: thinking status + real-time state updates |

### Tool Calls (LLM → System)

| Tool | Description |
|------|-------------|
| `sync_biocognitive_state()` | Trigger Bio-Digital Gap — update PhysioCore + Matrix |
| `propose_episodic_memory()` | Request MSP to validate and archive memory |

---

## Storage Architecture

```
consciousness/          ← Direct Access RAM (LLM read/write)
├── context_container/  # Active turn: task.md, self_note.md, user_profile.md
├── episodic_memory/    # Buffer: episodes/, episodic_log.jsonl
├── state_memory/       # Bio/psych/qualia snapshots (JSON)
├── sensory_memory/     # Qualia records
└── indexes/            # Episode counters, salience maps

memory/                 ← Subconscious (MSP-governed, LLM read-only)
├── context_storage/    # Persistent archive (full/, step1-3/)
├── user_profile/       # User belief systems
├── user_registry.json  # Multi-user identity registry
└── vector_store/       # ChromaDB (chroma.sqlite3)
```

**Constitutional Principle:** LLM ไม่สามารถเขียน `memory/` โดยตรง — ต้องผ่าน MSP เท่านั้น

---

## Configuration

| Config | Path |
|--------|------|
| Master Registry (SSOT) | `registry/eva_master_registry.yaml` |
| System-wide | `orchestrator/configs/Orchestrator_configs.yaml` |
| Biology | `physio_core/configs/PhysioCore_configs.yaml` + `hormone_spec_ml.yaml` |
| Psychology | `eva_matrix/configs/EVA_Matrix_configs.yaml` |
| Memory | `memory_n_soul_passport/configs/MSP_configs.yaml` |
| RMS | `resonance_memory_system/configs/` |
| RAG | `capabilities/services/agentic_rag/configs/Agentic_RAG_configs.yaml` |
| Identity/Persona | `orchestrator/Module/CIM/Node/prompt_rule/assets/identity/` |

> **Never hardcode:** ใช้ `IdentityManager.SYSTEM_*` และ `IdentityManager.BUS_*` เสมอ

---

## Testing

```bash
# All tests
python -m pytest tests/

# Per-module tests
python -m pytest physio_core/tests/
python -m pytest eva_matrix/tests/
python -m pytest memory_n_soul_passport/tests/
```

---

## Versioning

**System-level:** `9.7.0` (Epoch: Reflex)

| Module | Version |
|--------|---------|
| PhysioCore | v2.4.3 |
| EVA Matrix | v2.5.0 |
| Orchestrator | v1.3.0 |
| MSP | v2.1.0 |
| RMS | v2.5.0 |
| IdentityManager | v2.4.0 |
| AgenticRAG | v1.1.0 |

**Standards:**
- [Semantic Versioning 2.0.0](https://semver.org)
- [Conventional Commits 1.0.0](https://conventionalcommits.org)
- [Keep a Changelog 1.1.0](https://keepachangelog.com)

**Commit format:** `<type>(<scope>): <description>`
```bash
feat(PhysioCore): add ghrelin hormone support    # → MINOR bump
fix(MSP): correct episodic schema validation     # → PATCH bump
feat(API)!: change response envelope format      # → MAJOR bump (breaking)
```

---

## Documentation

```
docs/
├── 00_Governance/    # Changelog, governance docs
├── 01_Philosophies/  # MEM_PHILOSOPHY_888, design principles
├── 02_Requirements/  # System requirements
├── 03_Architecture/  # System architecture, ERD, Gap Flow
├── 04_Systems/       # Per-system documentation
├── 05_Capabilities/  # Services & tools docs
├── 06_Orchestration/ # CIM, Cognitive Flow 2.0
├── 07_Protocols/     # DOC_TO_CODE, standards
├── 08_Knowledge_Graphs/ # GraphRAG docs
├── 10_References/    # RTI.md, reference material
├── 99_Archive/       # Legacy docs
└── adr/              # Architecture Decision Records (ADR-001 to ADR-017)
```

**Key documents:**
- `docs/06_Orchestration/cognitive_flow/Cognitive_Flow_2_0.md` — Current standard
- `docs/03_Architecture/EVA_System_Architecture.md` — System overview
- `docs/03_Architecture/EVA_Gap_Flow.md` — Bio-Digital Gap orchestration
- `.agent/rules/constitution.md` — 5 Pillars (immutable)
- `registry/eva_master_registry.yaml` — Master Registry (SSOT)

---

*EVA — where biology meets cognition.*
