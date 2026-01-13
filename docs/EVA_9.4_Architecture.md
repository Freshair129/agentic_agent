# EVA v9.4.0 Architecture Guide (Resonance Refactored)

**Version:** 9.4.0
**Codename:** Resonance Refactored
**Root Directory:** `agent/`

---

## 🌟 Core Philosophy

EVA v9.4.0 introduces the **Consciousness-Implementation Separation** principle:

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
│   ├── episodic_memory/      # [MSP owned] ความจำเหตุการณ์ (Active story)
│   ├── semantic_memory/      # [GKS owned] ความจำความหมาย (Active concepts)
│   ├── sensory_memory/       # [AQI owned] ความจำการรับรู้ (Active sensation)
│   │
│   # === Capabilities (รู้ว่ามันทำอะไรได้ / Awareness of How) ===
│   # These are SHORTCUTS / REF FILES pointing to capabilities/ implementation
│   ├── tools/                # [SHORTCUTS] Interfaces to stateless tools (Read-Only)
│   │   ├── write_file.lnk    # → /capabilities/tools/filesystem/write_file.py
│   │   ├── search_web.lnk    # → /capabilities/tools/browser/search_web.py
│   │   └── ...
│   │
│   ├── skills/               # [SHORTCUTS] Interfaces to complex skills (Read-Only)
│   │   ├── emotional_analysis.lnk  # → /capabilities/skills/cognitive/analysis.py
│   │   └── ...
│   │
│   ├── services/             # [SHORTCUTS] Interfaces to external providers (Read-Only)
│   │   ├── agentic_rag.lnk   # → /capabilities/services/rag_engine/
│   │   └── ...
│   │
│   └── indexes/              # [Active Indices]
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
│       ├── rag_engine/       
│       ├── slm_core/         
│       └── vector_db/        
│
├── memory/                   # [STORAGE] Persistence Layer (MSP Custodian)
│   ├── session_memory/       # Archived sessions
│   ├── core_memory/          # Long-term identity
│   ├── sphere_memory/        # Structural knowledge
│   ├── user_profile/         # User data
│   ├── state_store/          # System snapshot storage
│   ├── context_store/        # Orchestrator context
│   ├── archival_memory/      # Deep freeze
│   │
│   # === GKS Knowledge Blocks (Read-Only Source) ===
│   ├── genesis_block/        
│   ├── master_block/         
│   ├── safety_block/         
│   │
│   └── indexes/              # Storage Indices
│
# === SYSTEMS (The Organs) ===
├── genesis_knowledge_system/ # [BRAIN] Strategic reasoning & knowledge
├── physio_core/              # [BODY] Biological simulation
├── eva_matrix/               # [MIND] Psychological state
├── artifact_qualia/          # [SENSE] Phenomenological experience
├── resonance_memory_system/  # [SUBCONSCIOUS] Automatic memory encoding
└── memory_n_soul_passport/   # [OS] Memory operating system
```

---

## 🔑 Key Principles

- **Separation of Concerns:** `consciousness` is for *being*, `capabilities` is for *doing*, `systems` is for *functioning*.
- **Safety by Design:** LLM cannot modify its own source code (Capabilities) directly from Consciousness.
- **Shortcuts:** The `tools/` and `skills/` in Consciousness act as API definitions or Symlinks to the actual code.
- **Memory Flow:**
  - Session Start: Load relevant blocks to `consciousness/memory`.
  - Session End: Flush `consciousness/memory` to `memory/session_memory` (via MSP).

---

## 🛠️ Migration Guide (from v9.3.x)

1. **Tools:** Move generic tools to `capabilities/tools/`.
2. **Services:** Move service engines to `capabilities/services/`.
3. **Skills:** Identify logic inside Systems that are actually skills (e.g., Code Gen) and move to `capabilities/skills/`.
4. **Systems:** Move core system engines (`physio_core`, `eva_matrix`) to root `agent/`.
5. **Memory:** Re-map MSP paths to the new `memory/` structure.

---
*Generated for EVA v9.4.0 Implementation*
