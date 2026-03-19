# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

EVA (Embodied Virtual Agent) is a bio-inspired AI architecture implementing the "Resonance Intelligence" framework. The system mimics biological cognitive processes through hormones, psychological states, and memory systems to create emotionally embodied AI responses.

**Current Version:** 9.7.0 (Epoch: Reflex)
**Architecture:** Single-Inference Sequentiality with Bio-Digital Gap + 4-Layer Affective Reflex
**Language:** Python 3.13
**Core Pattern:** Schema-First ("Doc-to-Code" Protocol)
**Master Registry:** `registry/eva_master_registry.yaml` (SSOT for system topology)

## Running the System

### Development Server

```bash
# FastAPI server with auto-reload
cd api
python run_server.py
# Server runs on http://0.0.0.0:8000
```

### Lightweight Version

```bash
# EVA Lite (minimal bio-simulation)
cd api
python eva_lite.py
```

### Web UI

```bash
# Vue.js/Vite frontend (development)
cd webui
npm run dev
```

### Testing

```bash
# Run all tests
python -m pytest tests/

# Run specific module tests
python -m pytest physio_core/tests/
python -m pytest eva_matrix/tests/
python -m pytest memory_n_soul_passport/tests/
```

### Health Checks

```bash
python scripts/check_versions.py       # Registry ↔ code version alignment
python scripts/check_doc_alignment.py  # Documentation consistency
python scripts/audit_msp_coverage.py   # MSP schema field coverage
python scripts/verify_physio_loop.py   # PhysioCore spike/decay validation
python scripts/verify_matrix_coupling.py  # Matrix coupling check
```

## System Architecture

### Cognitive Flow 2.0 (Single-Inference Sequentiality)

EVA operates in a **single LLM session** with sequential function calling. The flow is:

**Step 0-2: Pre-Processing (CIM-Centric)**

1. User Input → CNS (Orchestrator) → CIM (Context Assembler)
2. CIM checks **Engram** (reflex cache for fast memory lookup - DeepSeek-inspired)
3. CIM bundles: Input + Engram Result + Body State (from Resonance Bus)
4. Bundle sent to **SLM** (Small LLM for gut-feeling/intent extraction)
5. SLM Intent → CNS routes to MSP/RAG for **Quick Recall**
6. Memory + Context → CIM finalizes injection

**Step 3: LLM Reasoning (System 2)**
7. LLM receives full context (Input + Body + Engram + Intent + Memory)
8. LLM performs **Confidence Check**: "Do I need deep recall?"

**Step 4: The Gap (Bio-Digital Sync)**
9. LLM calls `sync_biocognitive_state()` with **Stimulus Chunks** (sequential emotion processing)
10. PhysioCore digests chunks sequentially → hormone cascade → vitals update
11. State returned to LLM

**Step 5-7: Response & Persistence**
12. If low confidence: LLM triggers Deep Recall (Agentic RAG 7-stream)
13. LLM generates embodied response
14. Self-reflection: LLM writes `self_note.md` for next turn
15. LLM calls `propose_episodic_memory()` → MSP validates and archives

**Critical Concept:** Unlike multi-turn architectures, the LLM never "forgets" - it pauses (function call), receives data, and resumes from the same mental state.

See: `docs/06_Orchestration/cognitive_flow/Cognitive_Flow_2_0.md`

### Core Modules (Actual Directory Structure)

```
orchestrator/                  # CNS (Central Nervous System) - flow control
├── Execution/
│   └── CognitiveFlow/        # MasterFlowEngine (run_turn pipeline)
├── Module/
│   └── CIM/                  # Context Injection Module (File Injector)
│       └── Node/
│           └── prompt_rule/  # Identity/persona governance (PRN)
│               └── assets/identity/  # Persona definitions (soul.md, etc.)
├── Node/                     # SessionNode (session lifecycle)
├── configs/                  # Orchestrator_configs.yaml
└── archive/                  # Deprecated dual-phase code

physio_core/                  # Biological simulation layer
├── logic/
│   ├── endocrine/           # 23 chemicals (16 hormones + 7 neurotransmitters)
│   ├── blood/               # Hormone distribution (30Hz update)
│   ├── receptor/            # Ligand-receptor signal transduction
│   ├── vitals/              # Heart rate, breathing, temperature
│   └── reflex/              # Immediate fight/flight responses
├── configs/
│   ├── PhysioCore_configs.yaml    # Unified config (NOT separate per subsystem)
│   └── hormone_spec_ml.yaml      # Full chemical database (23 entries)
└── tests/

eva_matrix/                   # 9D psychological state (EVA Matrix)
├── Module/                  # AxesComputation, ResonanceComputation nodes
├── configs/
│   └── EVA_Matrix_configs.yaml    # Single config file
└── schema/

artifact_qualia/              # Phenomenological layer (texture, color, soundscape)

resonance_memory_system/      # RMS - Affective memory encoding
├── Module/
│   ├── encoding_module/     # ColorGeneration, Intensity, TraumaProtection nodes
│   └── latching_module/     # Temporal smoothing
├── configs/
└── schema/

memory_n_soul_passport/       # Unified memory system (MSP) - 2,633 lines
├── Module/
│   ├── EpisodicMemory/      # JournalNode (file I/O)
│   ├── SemanticMemory/      # GroundingNode (belief revision)
│   └── SensoryMemory/       # QualiaStorageNode
├── schema/                  # 20 JSON schemas
├── contract/
└── configs/
    └── MSP_configs.yaml

operation_system/             # Infrastructure
├── identity_manager.py      # Centralized ID factory (ALL constants)
├── resonance_bus.py         # Pub/sub event bus (global singleton)
├── llm_bridge/              # LLM API (Gemini + Ollama)
│   └── schema/              # Tool schemas (sync_biocognitive_state, propose_episodic_memory)
├── nexus_mind/              # NexusMind reasoning engine
├── trajectory/              # TrajectoryManager (execution tracing)
├── rim/                     # Resonance Impact Measurement
└── configs/

capabilities/
├── services/
│   ├── agentic_rag/         # 7-stream memory retrieval (870 lines)
│   ├── engram_system/       # Fast memory lookup (DeepSeek-inspired)
│   ├── slm_bridge/          # Small LLM (Llama-3.2-1B) for System 1
│   ├── vector_bridge/       # ChromaDB integration (multilingual-e5-base)
│   └── graph_bridge/        # GraphRAG engine
└── tools/
    ├── resonance_index/     # RI scoring (4-layer: ER, IF, SR, CR)
    ├── resonance_impact/    # RIM calculation
    ├── subagents/           # RIS, Archivist, Technician
    ├── ui/                  # Debug web UI (Flask)
    ├── msp_monitor.py       # State completeness checker
    └── logger.py            # Thread-safe structured logging

contracts/                    # Interface definitions
├── systems/                 # IMSPassport, IPhysioSystem, IMatrixSystem, IResonanceBus
└── modules/                 # IMemoryStorage, IMemoryRetrieval, IKnowledgeAuthority, ICognitiveGateway

consciousness/               # "Awareness Domain" - Direct Access RAM
├── context_container/       # Active Turn Object (task.md, self_note.md, etc.)
├── data/                    # Runtime Workspace (Uploads, Outputs, Processing)
├── episodic_memory/         # Conversation logs
│   ├── episodes/            # Full episodes (JSON per episode)
│   ├── episodes_user/       # User-filtered variants
│   ├── episodes_ai/         # LLM-relevant variants
│   └── episodic_log.jsonl   # Fast append-only index
├── state_memory/            # Current bio/psych/qualia snapshots (JSON)
├── sensory_memory/          # Qualia records
├── indexes/                 # Salience maps, episode counters
├── services/                # Shortcuts to capabilities/services
└── tools/                   # Shortcuts to capabilities/tools

memory/                      # "Subconscious" - LLM cannot write here (MSP-governed)
├── context_storage/         # Persistent context archive (hot/cold slots)
│   ├── full_context/
│   ├── step1_perception/
│   ├── step2_processing/
│   └── step3_reasoning/
├── user_profile/            # User profiles
├── user_registry.json       # Multi-user identity registry
└── vector_store/            # ChromaDB persistent storage (chroma.sqlite3)

api/                         # External interface
├── chat_endpoint.py         # FastAPI + WebSocket (POST /api/chat, WS /ws/chat/{id})
├── eva_lite.py              # Lightweight EVA (5 hormones, 2D matrix, keyword RAG)
└── run_server.py            # Uvicorn launcher (port 8000)

webui/                       # Vue.js/Vite frontend
├── src/
│   ├── components/
│   └── services/
└── public/

tools/                       # Top-level system tools
└── technician/              # Registry auditor
```

### Critical Design Patterns

**1. Schema-First Development (Doc-to-Code Protocol)**

- All features start as YAML config definitions
- Code implements what's defined in config
- "Ghost Keys" = unimplemented config → your job ticket
- Master Registry (`registry/eva_master_registry.yaml`) defines system topology
- See: `docs/07_Protocols/DOC_TO_CODE.md`

**2. Centralized Identity Management**

- All system IDs, bus channels, personas managed by `IdentityManager`
- Never hardcode IDs like `"bus:physical"` → use `IdentityManager.BUS_PHYSICAL`
- 12 SYSTEM_* constants, 6 BUS_* channels, PERSONA_MAP
- See: `docs/adr/007_centralized_identity_management.md`

**3. Memory Architecture (Consciousness vs Subconscious)**

- **Consciousness** (`consciousness/`) = Direct Access RAM (LLM can read/write)
  - Context Container, Episodic Buffer, State Memory, Sensory Memory
- **Subconscious** (`memory/`) = MSP-governed permanent storage (LLM cannot write)
  - Context Storage, User Profile, User Registry, Vector Store
- Constitutional Principle: LLM proposes memories via `propose_episodic_memory()`, MSP validates and writes
- See: `docs/adr/008_Memory_Architecture_Centralized_MSP.md`, `docs/03_Architecture/EVA_System_Storage_ERD.md`

**4. CIM as File Injector (v9.6.0)**

- CIM no longer generates text prompts
- Instead, it **copies files** into `consciousness/context_container/` (hydration)
- LLM reads files directly via function calls
- Located at: `orchestrator/Module/CIM/`
- See: `docs/03_Architecture/EVA_System_Storage_ERD.md`

**5. Resonance Bus (Signal-First Architecture)**

- All systems communicate via pub/sub, never direct method calls
- 4 primary channels: `bus:physical`, `bus:psychological`, `bus:phenomenological`, `bus:knowledge`
- 2 additional channels: `bus:cognitive` (GKS/NexusMind), `bus:temporal` (Temporal Engine)
- MSP acts as "Subconscious Listener" latching state from all channels
- Global singleton: `from operation_system.resonance_bus import bus`

## Key Concepts

### The Bio-Digital Gap

Sequential biological processing during `sync_biocognitive_state()`:

```
LLM generates Stimulus Chunks → PhysioCore sequential digestion →
hormone release → blood distribution (30Hz) → receptor activation →
psychological state (EVA Matrix 9D) → phenomenological qualia →
RMS encoding (color, intensity, trauma) → state snapshot
```

**Stimulus Chunking v2.0:** LLM breaks complex input into emotional "chunks" processed sequentially to preserve the emotional journey. Each chunk triggers a per-chunk reflex via WebSocket.

- Chunk 1: "I love you" → Dopamine spike → WebSocket: "☺️"
- Chunk 2: "...but I'm leaving" → Cortisol shock → WebSocket: "...เดี๋ยวนะ"

This prevents emotional averaging and shows real-time emotional shifts.

### Resonance Intelligence (RTI)

Multi-level resonance scoring system:

- **L1:** Basic sentiment (0.0-1.0)
- **L2:** Emotional depth (warmth, playfulness, nostalgia)
- **L3:** Relational resonance (empathy flow, shared qualia)
- **L4:** Resonant Dynamic Memory (qualia recall, hormone memory, dream links)
- **L5:** Transcendental Intelligence (meta-cognition, paradox resolution)

See: `docs/10_References/RTI.md`

### Hormone System

23 chemicals modeled (16 hormones + 7 neurotransmitters):

**Hormones (ESC_H prefix):** Adrenaline, Cortisol, Aldosterone, Oxytocin, Vasopressin, Testosterone, Estrogen, Progesterone, Insulin, Glucagon, Leptin, Ghrelin, Thyroxine, Melatonin, Growth Hormone, Prolactin

**Neurotransmitters (ESC_N prefix):** Noradrenaline, Dopamine, Serotonin, Endorphin, GABA, Adenosine, Histamine

Simulation includes:

- Baseline levels, half-lives, exponential decay rates
- Circadian rhythms (melatonin)
- HPA axis (cortisol stress response)
- Blood distribution (30Hz update cycle)
- Receptor sensitization/desensitization
- Basal secretion (return to baseline)

Config: `physio_core/configs/PhysioCore_configs.yaml` + `physio_core/configs/hormone_spec_ml.yaml`

### Genesis Knowledge System (GKS)

**Status: NOT YET IMPLEMENTED** — GKS is defined in the master registry and IdentityManager (`SYSTEM_GKS = "GKS"`) but the `genesis_knowledge_system/` directory does not exist. Documentation exists at `docs/04_Systems/genesis_knowledge_system/`. The NexusMind component lives at `operation_system/nexus_mind/`.

### 7-Stream Agentic RAG

7-dimensional memory retrieval with 2-stage optimization:

**Quick Recall (30% weight, parallel with PhysioCore):**
- Narrative Stream (20%): Episode chains, story continuity
- Intuition Stream (5%): Semantic graph patterns
- Reflection Stream (5%): Meta-cognitive insights

**Deep Recall (70% weight, after bio state ready):**
- Emotion Stream (35%): **KEY** — cosine similarity on physio vectors (hormone matching)
- Salience Stream (15%): High-RI memories (impact > 0.70)
- Sensory Stream (10%): Qualia texture matching
- Temporal Stream (10%): Exponential decay (halflife 30 days)

**Merge:** Deduplicate → SLM cross-encoder re-rank top 5 → final ranked list

Location: `capabilities/services/agentic_rag/agentic_rag_engine.py` (870 lines)

### 4-Layer Affective Reflex System

EVA displays immediate body reactions and short utterances BEFORE the full LLM response. No second LLM is used — reflexes are sub-LLM mechanisms.

**Layers (fastest to most accurate):**

| Layer | Speed | Mechanism | Output |
|-------|-------|-----------|--------|
| 1. Enum Reflex | < 1ms | Pattern match → hormone spike | PhysioCore update + expression (flinch/blush/gasp) |
| 2. SLM Gut Utterance | < 50ms | gut_vector → nearest neighbor | Short Thai utterance ("ห๊ะ!?", "อืม...") |
| 3. Stimulus Extraction | < 50ms (Gap) | SLM reads LLM stimulus_chunks | Context-aware utterance (replaces Layer 2) |
| 4. CoT Extraction | < 50ms (Gap) | SLM reads LLM thinking tokens | Most accurate utterance (optional bonus) |

**Progressive Refinement:** Utterances upgrade as better data arrives:
```
50ms:   "อืม..."       ← gut guess
550ms:  "สูญเสีย..."   ← from stimulus (replaces gut)
2500ms: "ฉันเข้าใจ..." ← full LLM response
```

**Constitutional note:** No second LLM call — Pillar 2 preserved. Reflex uses Enum + SLM (already running) + LLM tool arguments.

See: `.agent/standards/system_requirements.yaml` (reflex_system section)

### Stimulus Chunking Protocol v2.0

Complex emotional input is broken into sequential "chunks" by the LLM. Each chunk is processed separately by PhysioCore during the Gap, preserving emotional shifts.

```
Input: "ขอบคุณนะ น่ารักมาก... ถ้าทำแบบนี้แค่คนเดียวก็คงดี"

Without chunking: warmth=0.5, stress=0.5 (averaged → flat)
With chunking:    chunk1(warmth=0.8) → chunk2(stress=0.7) → SHIFT preserved
```

**Tool call supports both:**
- `stimulus_vector` (single, backward compatible)
- `stimulus_chunks` (list, new — each chunk triggers separate reflex + PhysioCore step)

PhysioCore already supports list input (`physio_core.py` line 177). Each chunk fires a per-chunk reflex via WebSocket, so users see the emotional shift in real-time.

See: `.agent/standards/system_requirements.yaml` (stimulus_chunking section)

### Engram System (v9.6.0)

Fast memory lookup cache inspired by DeepSeek's Conditional Memory:

- **Purpose:** O(1) lookup for frequently accessed patterns
- **Location:** `capabilities/services/engram_system/`
- **Workflow:** CIM checks Engram before expensive RAG queries
- **Architecture:** Hash-based scalable lookup
- See: `docs/99_Archive/Conditional Memory.md` for theoretical background

### RMS Memory Encoding

Resonance Memory System encodes psychological state for storage:

1. **ColorGeneration:** 9D matrix → 5D color axes (stress, warmth, clarity, drive, calm) → hex color
2. **IntensityCalculation:** base arousal + impact boost + trend modifier
3. **TraumaProtection:** IF threat > 0.85 → dim colors (×0.55), reduce intensity (×0.50)
4. **LatchingModule:** Temporal smoothing (color α=0.65, intensity α=0.70)

**Encoding Levels:** L0_trace (<0.40) → L1_light (<0.65) → L2_standard (<0.85) → L3_deep (≥0.85) → L4_trauma (≥0.85 + threat)

### Boot Sequence (The Awakening)

System initialization order (defined in `registry/eva_master_registry.yaml`):

1. **IdentityManager** - Security first (Who am I?)
2. **Resonance Bus** - Transport layer (Connect everyone)
3. **PhysioCore** - Body (Heartbeat must start) [parallel]
4. **EVA Matrix** - Mind (Psychology follows physiology)
5. **MSP** - Memory (Soul wakes up) [parallel]
6. **GKS** - Knowledge (Wisdom loads) [NOT IMPLEMENTED]
7. **RMS** - Filter (Perception starts)
8. **Artifact Qualia** - Senses (Phenomenology online)
9. **Orchestrator** - CNS (Conductor raises baton)

## Common Tasks

### Adding a New Hormone Response

1. Edit `physio_core/configs/PhysioCore_configs.yaml` (add gland or modify parameters)
2. Add chemical spec in `physio_core/configs/hormone_spec_ml.yaml`
3. Run audit: `python capabilities/tools/subagents/ris_subagent.py --audit-config`
4. Implement code in `physio_core/logic/endocrine/`
5. Test: `python -m pytest physio_core/tests/`

### Modifying Psychological Dimensions

1. Edit `eva_matrix/configs/EVA_Matrix_configs.yaml`
2. Update schema: `eva_matrix/schema/EVA_Matrix_Payload_Schema_v2.json`
3. Implement in `eva_matrix/Module/`

### Adding New Memory Type

1. Define schema in `memory_n_soul_passport/schema/`
2. Add contract in `memory_n_soul_passport/contract/`
3. Update MSP engine logic (centralized in `memory_n_soul_passport_engine.py`)
4. Storage goes to `consciousness/` subdirectories

### Updating Identity/Persona

1. Edit persona assets: `orchestrator/Module/CIM/Node/prompt_rule/assets/identity/`
2. Config: `orchestrator/Module/CIM/Node/prompt_rule/` directory

### Working with Context Container

The Context Container is the "active working memory" for each turn:

1. **Location:** `consciousness/context_container/`
2. **Files injected by CIM:**
   - `task.md` - Current turn objective
   - `self_note_epXX.md` - Self-reflection from previous turn
   - `user_profile.md` - User grounding facts
   - `context_summary_epXX.md` - Turn summary
   - `goal.md`, `instructions.md` - Persistent directives
3. **LLM reads these directly** via function calls (no text prompts)
4. **MSP archives** container contents after turn completion

## Configuration Locations

| Config | Path |
|--------|------|
| Master Registry (SSOT) | `registry/eva_master_registry.yaml` |
| System-wide | `orchestrator/configs/Orchestrator_configs.yaml` |
| Cognitive Flow | `docs/06_Orchestration/cognitive_flow/` |
| Biology | `physio_core/configs/PhysioCore_configs.yaml` + `hormone_spec_ml.yaml` |
| Psychology | `eva_matrix/configs/EVA_Matrix_configs.yaml` |
| Memory | `memory_n_soul_passport/configs/MSP_configs.yaml` |
| RMS | `resonance_memory_system/configs/` |
| RAG | `capabilities/services/agentic_rag/configs/Agentic_RAG_configs.yaml` |
| Identity/Persona | `orchestrator/Module/CIM/Node/prompt_rule/assets/identity/` |
| Bus Channels | `IdentityManager` class constants (code, not config) |

## Data Contracts (Schemas)

All modules communicate via standardized JSON schemas (v2):

- `*_Payload_Schema_v2.json` - Module input/output contracts
- Validation happens at module boundaries via `MSPSchemaValidator`
- 20 JSON schemas in `memory_n_soul_passport/schema/`

Schema locations:

```
{module}/schema/{Module}_Payload_Schema_v2.json
{module}/contract/{Module}_Interface.yaml
```

## Important Constraints

### Never Hardcode

- System IDs → Use `IdentityManager.SYSTEM_*`
- Bus channels → Use `IdentityManager.BUS_*`
- File paths → Load from config YAML
- Magic numbers → Define in YAML

### File Ownership

| Domain | Path | LLM Access | Write Authority |
|--------|------|-----------|-----------------|
| Consciousness | `consciousness/` | Read + Write | LLM direct |
| Subconscious | `memory/` | Read only (via RAG) | MSP only |
| Docs | `docs/` | Read only | Manual |
| Registry | `registry/` | Read only | Manual |
| Contracts | `contracts/` | Read only | Manual |

### Commit Discipline

- One commit per system when making cross-module changes
- Follow convention: `[ModuleName] Description`
- Tag version bumps: `v9.1.0-C10`

## Documentation Structure (v9.6.2)

```
docs/
├── 00_Governance/     # Changelog, governance docs
├── 01_Philosophies/   # MEM_PHILOSOPHY_888, design principles
├── 02_Requirements/   # System requirements
├── 03_Architecture/   # System architecture, ERD, Gap Flow
├── 04_Systems/        # Per-system documentation
├── 05_Capabilities/   # Services & tools docs
├── 06_Orchestration/  # CIM, Cognitive Flow 2.0 docs
├── 07_Protocols/      # DOC_TO_CODE, standards
├── 08_Knowledge_Graphs/ # GraphRAG docs
├── 10_References/     # RTI.md, reference material
├── 99_Archive/        # Legacy docs, Conditional Memory
├── adr/               # Architecture Decision Records
└── archive/           # Archived docs
```

**Critical Documents:**

- `docs/06_Orchestration/cognitive_flow/Cognitive_Flow_2_0.md` - **Current standard**
- `docs/03_Architecture/EVA_System_Architecture.md` - System overview
- `docs/03_Architecture/EVA_System_Storage_ERD.md` - Memory domains & data ownership
- `docs/03_Architecture/EVA_Gap_Flow.md` - Bio-Digital Gap orchestration
- `docs/01_Philosophies/MEM_PHILOSOPHY_888.md` - Memory 8-8-8 protocol

**Architecture Decision Records:**

- `docs/adr/001_cim_prompt_rule_transition.md` - Why CIM replaced CIN
- `docs/adr/002_two_stage_rag_retrieval.md` - 2-stage RAG optimization
- `docs/adr/004_one_inference_architecture.md` - Single-session LLM flow
- `docs/adr/005_Unified_Resonance_Architecture.md` - Resonance system design
- `docs/adr/006_hybrid_graph_rag.md` - GraphRAG integration
- `docs/adr/007_centralized_identity_management.md` - IdentityManager pattern
- `docs/adr/008_Memory_Architecture_Centralized_MSP.md` - MSP as memory SSOT

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/chat` | POST | Chat with EVA → `{response, emotional_state}` |
| `/api/health` | GET | `{status, agent_version, active_sessions}` |
| `/api/mind/state` | GET | `{eva_matrix, physio, qualia, resonance_index}` |
| `/ws/chat/{client_id}` | WebSocket | Full duplex: thinking status + state updates |

## Debugging

### Common Issues

**"Ghost Key" warnings:** Config key exists but not consumed in code → implement the feature

**Schema validation errors:** Check `memory_n_soul_passport/schema/` for required fields

**Hormone imbalances:** Check baselines in `physio_core/configs/PhysioCore_configs.yaml`, verify decay rates in `hormone_spec_ml.yaml`

**Memory not persisting:** Check MSP write policy. LLM cannot write to `memory/` directly - must use `propose_episodic_memory()` tool.

**Context not loading:** Check if files exist in `consciousness/context_container/`. Verify CIM injection at `orchestrator/Module/CIM/`.

**Boot order failures:** Check `registry/eva_master_registry.yaml` runtime_sequence. PhysioCore must start before Matrix.

**Version mismatches:** Run `python scripts/check_versions.py`

### Logging

- Console logs use structured format: `[MODULE] [LEVEL] Message`
- Custom logger: `from capabilities.tools.logger import safe_print`
- Pattern: override `print = safe_print` per module

## Project Versioning

**System-level:** `9.7.0` Epoch: Reflex

**Module-level:** Decoupled versioning (per ADR-011)

- PhysioCore: v2.4.3
- EVA_Matrix: v2.5.0
- Orchestrator: v1.3.0
- MSP: v2.1.0
- RMS: v2.5.0
- IdentityManager: v2.4.0
- AgenticRAG: v1.1.0

### Version Control Standards (International)

| Standard | Version | What It Governs |
|----------|---------|-----------------|
| **Semantic Versioning** | 2.0.0 (semver.org) | MAJOR.MINOR.PATCH numbering |
| **Conventional Commits** | 1.0.0 (conventionalcommits.org) | Commit message format |
| **Keep a Changelog** | 1.1.0 (keepachangelog.com) | CHANGELOG format |

**Commit format:** `<type>(<scope>): <description>`

```bash
feat(PhysioCore): add ghrelin hormone support       # → MINOR bump
fix(MSP): correct episodic schema validation         # → PATCH bump
feat(API)!: change response envelope format          # → MAJOR bump (breaking)
docs(CLAUDE.md): sync with actual codebase           # → No bump
```

**Pre-commit:** `python scripts/check_versions.py` (verify registry ↔ code alignment)

**Full protocol:** `.agent/workflows/version-control.md`

See: `docs/00_Governance/CHANGELOG.md`, `registry/version_log.yaml`

## Special Files

| File | Purpose |
|------|---------|
| `registry/eva_master_registry.yaml` | Master Registry (SSOT for topology, boot order) |
| `registry/master_configs.yaml` | Global config (organism version, developer ID) |
| `.agent/rules/constitution.md` | 5 Pillars (immutable) |
| `.agent/rules/gapflow.md` | Bio-Digital Gap rules |
| `.agent/rules/memorygovernance.md` | 8-8-8 Memory governance |
| `.agent/workflows/` | Automated workflows (archivist, doc_to_code, etc.) |
| `.planning/` | Implementation checklists, gap analyses, Gemini handoff |
| `docs/10_References/GEMINI.md` | Instructions for Gemini LLM partner |
| `consciousness/context_container/` | Active turn working files |
| `consciousness/indexes/` | Memory index, episode counters |
| `memory/user_registry.json` | Multi-user identity facts |
| `memory/vector_store/chroma.sqlite3` | ChromaDB persistent storage |

## System Specifications

| Document | Path | Purpose |
|----------|------|---------|
| System Requirements | `.agent/standards/system_requirements.yaml` | Full tech stack, core systems, API, storage, NFRs, boot sequence |
| ID Standards | `.agent/standards/id_standards.yaml` | All ID formats, naming conventions, never-hardcode rules |
| Changelog System | `docs/00_Governance/CHANGELOG_SYSTEM.md` | Sliding window changelog spec, severity levels, tags |
| Master Registry | `registry/eva_master_registry.yaml` | SSOT for topology, boot order, permissions |
| Master Configs | `registry/master_configs.yaml` | Global constants (organism_version, developer_id) |

## Notes on Multilingual Content

The codebase contains Thai language content in:

- `docs/99_Archive/Conditional Memory.md` - DeepSeek analysis
- `docs/10_References/RTI.md` - Resonance Intelligence framework
- `.agent/rules/eva.md` - Vision document
- Some docstrings and comments

This is intentional - EVA supports multilingual operation. Do not remove Thai content.
