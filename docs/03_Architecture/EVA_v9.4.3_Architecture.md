# EVA v9.4.3 Architecture Guide (Resonance Refactored)

**Version:** 9.4.3
**Codename:** Resonance Refactored
**Root Directory:** `agent/`

---

## 🌟 Core Philosophy

EVA v9.4.3 introduces the **Consciousness-Implementation Separation** principle:

1. **Consciousness (Awareness):** The LLM operates here. It sees "Shortcuts" (Interfaces) to its capabilities and has R/W access to its Working Memory. It is "aware" of what it can do but cannot alter the underlying code during runtime.
2. **Capabilities (Implementation):** The actual Python code (Tools, Skills, Services) lives here, independent of the consciousness layer. This ensures stability and safety.
3. **Organism (Systems):** The biological and psychological systems (Physio, Matrix) run autonomously, providing the "feeling" of being alive.

---

## 📂 Full Directory Structure

```text
agent/
├── consciousness/            # [AWARENESS DOMAIN] สติสัมปชัญญะ - LLM Full R/W (Locked)
│   │
│   # === Memory (รู้ว่ามันมีอะไร / Awareness of What) ===
│   ├── episodic_memory/      # [MSP owned] ความจำเหตุการณ์ → move to memory/session_memory when session end
│   ├── semantic_memory/      # [EVA owned] ความจำความหมาย → MSP moves to session_memory (Candidate for GKS)
│   ├── sensory_memory/       # [EVA owned] ความจำการรับรู้ → MSP archives to Sensory Store
│   │
│   # === Capabilities (รู้ว่ามันทำอะไรได้ / Awareness of How) ===
│   ├── tools/                # [SHORTCUTS] Interfaces to stateless tools (Read-Only)
│   │   ├── write_file.lnk    # → /tools/filesystem/write_file.py
│   │   ├── read_file.lnk     # → /tools/filesystem/read_file.py
│   │   ├── search_web.lnk    # → /tools/browser/search_web.py
│   │   ├── run_command.lnk   # → /tools/terminal/run_command.py
│   │   └── ... (shortcuts to actual implementations)
│   │
│   ├── skills/               # [SHORTCUTS] Interfaces to complex skills (Read-Only)
│   │   ├── emotional_analysis.lnk     # → /eva/eva_matrix/logic/analysis.py
│   │   ├── memory_synthesis.lnk       # → /services/agentic_rag/synthesis.py
│   │   ├── code_generation.lnk        # → /tools/coding/generator.py
│   │   └── ... (shortcuts to skill modules)
│   │
│   ├── services/             # [SHORTCUTS] Interfaces to external providers (Read-Only)
│   │   ├── agentic_rag.lnk       # → /services/agentic_rag/
│   │   ├── slm_bridge.lnk        # → /services/slm_bridge/
│   │   ├── engram_system.lnk     # → /services/engram_system/
│   │   ├── vector_search.lnk     # → /services/vector_bridge/
│   │   └── ... (shortcuts to service inputs)
│   │
│   └── indexes/              
│
├── capabilities/             # [IMPLEMENTATION] Source code (Hidden/Locked from LLM)
│   ├── tools/                # Stateless atomic tools
│   │   ├── filesystem/       
│   │   ├── browser/          
│   │   ├── analysis/         
│   │   └── terminal/         
│   │
│   ├── skills/               # Complex skill modules
│   │   ├── cognitive/        
│   │   ├── creative/         
│   │   └── projection/       
│   │
│   └── services/             # Service wrappers
│       ├── engram_system/    # [NEW] Conditional Memory (O(1) Lookup)
│       ├── rag_engine/       
│       ├── slm_core/         
│       └── vector_db/        
│
├── memory/                   # [STORAGE] Subconscious Domain - LLM Read-only (via MSP)
│   ├── session_memory/       # [Working Memory] Raw snapshot of consciousness layers
│   ├── core_memory/          # [Short-term Memory] 8-Session Distillation
│   ├── sphere_memory/        # [Long-term Memory] 8-Core Distillation (Wisdom)
│   ├── user_profile/         # [User Modeling]
│   ├── state_store/          # [System State] PhysioCore, Matrix, RMS static state
│   ├── context_store/        # [Runtime Buffers] CIM dynamic context
│   ├── archival_memory/      # [Frozen] Immutable logs (MSP owned)
│   │
    │   # === GKS Blocks (moved from consciousness - read-only knowledge) ===
    ├── orchestrator/         # [SYSTEM] Main Orchestration Loop
    │   ├── cim/              # [MODULE] Context Injection
    │   ├── session_manager/  # [MODULE] Lifecycle & Grounding Handoff
    │   └── orchestrator.py
    │
    │   # === GKS Blocks (moved from consciousness - read-only knowledge) ===
│   ├── genesis_block/        # [read-only cache] Loaded from GKS stores
│   ├── master_block/         # [read-only cache] Core knowledge (DNA)
│   ├── safety_block/         # [read-only cache] Safety protocols
│   │
│   └── indexes/              # [memory indices]
│
├── genesis_knowledge_system/ # [SYSTEM] Source of truth for knowledge (Locked)
│   ├── configs/              # [configs]
│   ├── contracts/            # [contracts]
│   ├── logic/                # [logic]
│   ├── schemas/              # [schemas]
│   ├── nexus_mind/           # [MODULE] Strategic brain (reasoning & decision)
│   ├── archetypal_projection/# [MODULE] Framework projection (APM)
│   ├── meta_learning_loop/   # [MODULE] Pattern reinforcement (MLL)
│   ├── grounding/            # [NODE] User conflict detection
│   │   └── truth_seeker_node.py # [NEW] "Grilled Shrimp" Validation Logic
│   ├── Algorithm_how_Genesis_Block_store/ 
│   ├── concept_why_Genesis_Block_store/
│   ├── framework_genesis_Block_store/ 
│   ├── parameter_what_Genesis_Block_store/
│   ├── protocol_process_Genesis_Block_store/      
│   └── master_block_store/
│
├── physio_core/              # [SYSTEM] Biological simulation (Hormones + ANS) (Locked)
│   ├── configs/              # PhysioCore configs
│   ├── logic/
│   │   ├── endocrine/        # Hormone glands
│   │   ├── bloodstream/      # Circulation & transport
│   │   ├── vitals/           # Medical vitals (BPM, RPM, BP, Temp)
│   │   └── autonomous/       # ANS (Sympathetic/Parasympathetic)
│   └── physio_core.py        # Main engine
│
├── eva_matrix/               # [SYSTEM] Psychological state (9D axes) (Locked)
│   ├── configs/              # Matrix configs
│   ├── logic/
│   │   ├── core_axes/        # 5 Core: Arousal, Valence, Tension, Clarity, Warmth
│   │   └── meta_axes/        # 2 Meta: Stability, Coherence + 2 Categorical
│   └── eva_matrix.py         # Psychological engine
│
├── artifact_qualia/          # [SYSTEM] Phenomenological experience (AQI) (Locked)
│   ├── configs/              # AQI configs
│   ├── logic/
│   │   ├── intensity/        # Experience intensity
│   │   ├── tone/             # Emotional tone
│   │   ├── coherence/        # Narrative coherence
│   │   └── texture/          # Phenomenological texture
│   └── artifact_qualia.py    # Qualia engine
│
├── resonance_memory_system/  # [AUTOMATIC] สติไร้สำนึก - Memory encoding (LLM cannot control) (Locked)
│   ├── configs/              # RMS Configs
│   ├── contract/             # RMS Payload Contract (Locked)
│   ├── schema/               # RMS Payload Schema v2 (Locked)
│   ├── trauma_store/         # Trauma indexing
│   └── rms.py                # Encoding engine (Locked)
│
└── memory_n_soul_passport/   # [SYSTEM] MSP - Memory OS & Custodian (Locked)
    ├── configs/              # MSP configs
    ├── schema/               # Memory schemas
    ├── Module/               # [NEW] Delegated Logic Modules
    │   ├── EpisodicMemory/
    │   │   └── Node/
    │   │       └── JournalNode/
    │   ├── SemanticMemory/
    │   │   └── Node/
    │   │       └── GroundingNode/
    │   └── SensoryMemory/
    │       └── Node/
    │           └── QualiaStorageNode/
    └── memory_n_soul_passport_engine.py # Facade


├── operation_system/         # [SYSTEM] Core Identity & Bus Management (Locked)
        ├── configs/              # OS configs
        ├── identity_manager.py   # Global ID Factory
        ├── resonance_bus.py      # Communication Backbone
        └── rim/                  # [MODULE] Resonance Impact Model
            ├── configs/
            └── rim_engine.py
```

---

## 🔑 Key Principles

- **Separation of Concerns:** `consciousness` is for *being*, `capabilities` is for *doing*, `systems` is for *functioning*.
- **Safety by Design:** LLM cannot modify its own source code (Capabilities) directly from Consciousness.
- **Shortcuts:** The `tools/` and `skills/` in Consciousness act as API definitions or Symlinks to the actual code.
- **Memory Flow:**
  - Session Start: Load relevant blocks to `consciousness/memory`.
  - Session End: Snapshot the entire `consciousness/` folder to `memory/session_memory` (via MSP).
หัวใจการออกแบบของเราตอนนี้คือ doc to code นะ เพราะฉะนั้นจะแก้อะไรแก้ไฟล์ yaml,md ก่อน

---

## 📡 Resonance Bus Architecture (v2.4.3)

The Central Nervous System of EVA v9.4.3 is the **Resonance Bus**, a decentralized, subscriber-based communication hub.

- **Role:** Replaces direct system-to-system method calls.
- **Pattern:** Publish/Subscribe (Decoupled).
- **Core Channels:**
  - `BUS_PHYSICAL` (PhysioCore -> Matrix)
  - `BUS_PSYCHOLOGICAL` (Matrix -> Qualia)
  - `BUS_PHENOMENOLOGICAL` (Qualia -> MSP)
- **Passive Persistence:** The MSP Engine acts as a "Subconscious Listener," automatically latching state snapshots from the bus to maintain system continuity.
- **Reference:** `docs/adr/012_resonance_bus_state_decoupling.md`

## 🏷️ Independent Versioning Standard (ADR-011)

EVA v9.4.3 adopts a decoupled versioning strategy to allow subsystems to evolve independently while maintaining historical context.

- **Global Context:** v9.4.3 (The Orchestrator/Integration Layer)
- **Subsystem Logic:**
  - Legacy `8.x.x` → `1.x.x` (e.g., MSP v1.1.0)
  - Legacy `9.x.x` → `2.x.x` (e.g., PhysioCore v2.4.3)
- **System of Record:** `core_systems.yaml`

---

## Structural Hierarchy

## 🏗️ The Hierarchy (ลำดับชั้นโครงสร้าง)

1. **System (ระบบหลัก/อวัยวะ)**: หน่วยอิสระที่มี State ของตัวเอง (Owns Slots in MSP) เป็นโครงสร้างพื้นฐานของสิ่งมีชีวิต
2. **Central Module (โมดูลกลาง)**: หน่วยประมวลผลอิสระที่ขึ้นตรงกับ OS (OS-Direct) ไม่ขึ้นกับระบบใดระบบหนึ่ง มีความซับซ้อนกว่า Node สามารถสร้าง Slot บน Root และมี Node ของตัวเองได้ ถูกเรียกใช้จากหลายระบบ/โมดูล
3. **Module (โมดูลเชิงหน้าที่)**: ผู้ประสานงานภายใน System (Internal Integrator)
4. **Node (โหนดตรรกะ)**: ผู้กำหนดกฎเกณฑ์หรือตรรกะการตัดสินใจ (Decision/Policy Provider)
5. **Component (ส่วนประกอบย่อย)**: หน่วยประมวลผล Pure Logic ฐานราก

เพราะฉะนั้น ทุกระบบต้องเป็นเจ้าของโมดูลใดโมดูลหนึ่งเสมอ และทุกโมดูลต้องเป็นเจ้าของ node ใด้ node นึงเสมอ

### 💡 Core Rationale: Why System vs Service?

การเลือกระหว่าง **System** และ **Service** อิงจากปรัชญา **"Informational Organism"**:

| คุณสมบัติ | System (Core Organism) | Service (Extended Skill) |
| :--- | :--- | :--- |
| **บทบาท** | เป็นอวัยวะภายใน (Vital Organ) | เป็นทักษะเสริม (Extended Skill) |
| **ความถี่การทำงาน** | Continuous Loop (ตลอดเวลา) | On-demand (เมื่อเรียกใช้) |
| **State Ownership** | เจ้าของสัญญาณชีพ (Vital Signals) | เจ้าของข้อมูลอ้างอิง (Reference Data) |
| **Impact** | ขาดแล้ว "ตาย" หรือเสียตัวตน | ขาดแล้ว "เรียนรู้ช้า" หรือพูดได้จำกัด |

**ตัวอย่างเหตุผลที่ PhysioCore เป็น System:**

- กายภาพเป็น "หัวใจ" ของการแปรผันอารมณ์ ซึ่งต้องเปลี่ยนก่อนจะเกิดความคิด (Physiology First)
- PhysioCore ผลิตสัญญาณชีพวิ่งใน Resonance Bus ตลอดเวลา ไม่ใช่แค่บริการที่ถูกเรียกใช้เป็นครั้งคราว

### 📂 Directory Mapping for System

```text
[System]/
├── configs/                # System-wide SSOT
├── Module/
│   ├── [module]/           # Functional Integrator
│   │   ├── Node/   
│   │   │   └── [Node]/           # Logic Provider
│   │   │       ├── Component/    # Specialized Logic Unit
│   │   │       │   └── logic.py
│   │   │       └── [node]_node.py
│   │   └── [module].py
└── [system]_engine.py

> [!IMPORTANT]
> **PhysioCore Exemption**: The `PhysioCore` system is EXEMPT from the strict `Module/Node` hierarchy.
> It retains its unique `logic/[subsystem]_engine` structure (e.g., `logic/endocrine`, `logic/blood`) due to the complex, tightly coupled nature of biological simulation.
> **DO NOT REFACTOR** PhysioCore into the standard Module/Node pattern.

## 🛠️ Migration Guide (from v9.3.x)

1. **Tools:** Move generic tools to `capabilities/tools/`.
2. **Services:** Move service engines to `capabilities/services/`.
3. **Skills:** Identify logic inside Systems that are actually skills (e.g., Code Gen) and move to `capabilities/skills/`.
4. **Systems:** Move core system engines (`physio_core`, `eva_matrix`) to root `agent/`.
5. **Memory:** Re-map MSP paths to the new `memory/` structure.

## 🧠 Memory Architecture (v9.4.3)

> [!IMPORTANT]
> **Philosophy:** "Active Consciousness (LLM) creates experience in the Awareness Domain; Subconscious (MSP) distills Wisdom via the 8-8-8 Protocol."
> **Full Guide:** See [MEM_PHILOSOPHY_888.md](file:///e:/The%20Human%20Algorithm/T2/agent/docs/01_Philosophies/MEM_PHILOSOPHY_888.md)

### 1. Memory Layers (Redefined)
- **Consciousness (Buffer)**: The "Awareness Domain" where the LLM lives and has full R/W authority.
- **Session (Working Memory)**: คลังความจำเหตุการณ์ (Raw Snapshots) ที่เก็บโฟลเดอร์ `consciousness/` ทั้งหมดหลังจากจบ Session
- **Core (Short-Term)**: 8-session distillation (Clean, Summary, Index, Relation).
- **Sphere (Long-Term)**: 8-core / 64-session wisdom (Identity DNA).
- **Governance Overlay**: ความจำทั้งหมดถูกควบคุมด้วย **Memory Domains** และ **Epistemic States**
- **Belief Revision**: รองรับการ Downgrade Sphere -> Core เมื่อเกิดความขัดแย้งซ้ำๆ (Belief Erosion)
- **Intuition Layer**: ระบบความจำพิเศษแบบ Habit และ Somatic Imprint

### 2. MSP (Memory & Soul Passport) - **The Subconscious Governor**
- **Role:** Central authority for persistence and the 8-8-8 synthesis engine.
- **Independence:** Decouples active consciousness (Active State) from long-term storage data structures.

---
*Generated for EVA v9.4.3 Implementation*

