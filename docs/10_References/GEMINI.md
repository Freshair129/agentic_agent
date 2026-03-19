# EVA v9.7.0 (Epoch: Reflex) - Gemini Development Context

This document provides a comprehensive overview of the EVA v9.7.0 project, its architecture, and development conventions. It is intended to be used as a primary context file for Gemini AI assistants working on this project.

## 1. Project Overview

EVA is a highly complex, modular AI agent framework designed to simulate a "digital organism." It features a sophisticated architecture that models biological, psychological, and cognitive processes.

### Core Concepts:

*   **Digital Organism:** EVA is structured as a collection of interconnected "organs" or systems, each with a specific function (e.g., physiology, psychology, memory).
*   **Registry-Centric Governance:** The entire system is defined and governed by `registry/eva_master_registry.yaml`. This master registry specifies all systems, their dependencies, communication channels, and the boot sequence.
*   **Cognitive Flow 2.0:** The agent's reasoning process follows a single-inference sequential cycle:
    1.  **Perception:** SLM (Llama 1B) extracts intent + Engram reflex check + CIM context injection
    2.  **The Gap:** PhysioCore hormone cascade + EVA Matrix 9D update + RMS encoding + 7-stream RAG retrieval
    3.  **Reasoning:** LLM generates embodied response + proposes episodic memory
    4.  **Persistence:** MSP validates + archives episode + autonomic prediction for next turn
*   **Resonance Bus:** A pub/sub messaging system (6 channels) that allows components to communicate without direct coupling.
*   **Single-Inference Sequentiality:** The entire flow happens in ONE LLM session via sequential function calling (`sync_biocognitive_state()` → Gap → `propose_episodic_memory()`). The LLM never loses context.

### Key Systems:

*   **Orchestrator (`orchestrator/`):** The "Central Nervous System" that directs cognitive flow via `MasterFlowEngine` at `orchestrator/Execution/CognitiveFlow/`.
*   **PhysioCore (`physio_core/`):** Simulates 23 chemicals (16 hormones + 7 neurotransmitters) with decay, basal secretion, and 30Hz blood distribution.
*   **EVA Matrix (`eva_matrix/`):** Computes 9D psychological state (stress, warmth, drive, clarity, joy, alertness, connection, groundedness, openness) from physiology.
*   **RMS (`resonance_memory_system/`):** Encodes psychological state into memory-storable format (color axes, intensity, trauma protection, encoding levels L0-L4).
*   **Artifact Qualia (`artifact_qualia/`):** Generates phenomenological sensory experience (texture, color, tone).
*   **MSP (`memory_n_soul_passport/`):** Central memory system (2,633 lines). Manages episodic, semantic, and sensory memory with schema validation. Sole writer to `memory/` (subconscious).
*   **Agentic RAG (`capabilities/services/agentic_rag/`):** 7-stream memory retrieval (emotion, narrative, salience, sensory, temporal, intuition, reflection) with 2-stage optimization.
*   **Operation System (`operation_system/`):** Infrastructure — IdentityManager, Resonance Bus, LLM Bridge (Gemini + Ollama), NexusMind, TrajectoryManager, RIM engine.
*   **Contracts (`contracts/`):** Interface definitions — `IMSPassport`, `IPhysioSystem`, `IMatrixSystem`, `IResonanceBus` (systems) + `IMemoryStorage`, `IMemoryRetrieval` (modules).
*   **API (`api/`):** FastAPI + WebSocket server. Also includes EVA Lite (lightweight 5-hormone, 2D matrix version).

### Key Innovations:

*   **4-Layer Affective Reflex System:** Immediate sub-LLM reactions before full response:
    - Layer 1: Enum Reflex (<1ms) → hormone spike + expression
    - Layer 2: SLM Gut Utterance (<50ms) → "ห๊ะ!?", "อืม..."
    - Layer 3: Stimulus Extraction (<50ms, during Gap) → context-aware utterance from LLM tool args
    - Layer 4: CoT Extraction (optional, during Gap) → most accurate utterance from thinking tokens
    - **No second LLM call** — uses Enum + SLM (already running) + LLM tool arguments
    - See: `.agent/standards/system_requirements.yaml` (reflex_system section)

*   **Stimulus Chunking v2.0:** LLM breaks complex input into sequential emotion chunks. Each chunk triggers separate PhysioCore step + per-chunk reflex via WebSocket. Preserves emotional shifts (e.g., warmth→anxiety) instead of averaging.
    - Tool call: `stimulus_chunks: [{text, vector, bio_impacts}, ...]`
    - PhysioCore already supports list input (`physio_core.py` line 177)
    - See: `.agent/standards/system_requirements.yaml` (stimulus_chunking section)

### NOT YET IMPLEMENTED:

*   **GKS (Genesis Knowledge System):** Referenced in registry and IdentityManager (`SYSTEM_GKS`) but `genesis_knowledge_system/` directory does not exist. Documentation only at `docs/04_Systems/genesis_knowledge_system/`.
*   **memory/ subdirectories:** `session_memory/`, `core_memory/`, `sphere_memory/` are defined in MSP config but directories not yet created.

### Technology Stack:

*   **Language:** Python 3.13
*   **API Framework:** FastAPI + Uvicorn
*   **Vector DB:** ChromaDB (SQLite-backed) with `intfloat/multilingual-e5-base` embeddings
*   **SLM:** Llama-3.2-1B via SLM Bridge (System 1 / gut-feeling)
*   **LLM:** Gemini API (System 2 / reasoning) + Ollama (local alternative)
*   **Schema Validation:** JSON Schema (20 schemas in `memory_n_soul_passport/schema/`)
*   **Frontend:** Vue.js/Vite (`webui/`) for debug UI

## 2. Building and Running

### Prerequisites:

```bash
pip install -r api/requirements.txt
```

### Running the Server:

```bash
# FastAPI server (port 8000)
python api/run_server.py

# EVA Lite (lightweight version)
python api/eva_lite.py

# Direct orchestrator
python orchestrator/orchestrator.py
```

### Web UI:

```bash
cd webui
npm install
npm run dev
```

### Health Checks:

```bash
python scripts/check_versions.py        # Registry ↔ code version alignment
python scripts/check_doc_alignment.py   # Documentation consistency
python scripts/audit_msp_coverage.py    # MSP schema field coverage
python scripts/verify_physio_loop.py    # PhysioCore spike/decay validation
python scripts/verify_matrix_coupling.py # Matrix coupling check
```

### API Endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/ws/chat/{session_id}` | WebSocket | Real-time stateful interaction |
| `/api/chat` | POST | Stateless request-response |
| `/api/health` | GET | System status |
| `/api/mind/state` | GET | Full bio/psych/qualia state |

## 3. Actual Directory Structure

```
agentic_agent/
├── orchestrator/                  # CNS - flow control
│   ├── Execution/CognitiveFlow/  # MasterFlowEngine
│   ├── Module/CIM/              # Context Injection Module
│   │   └── Node/prompt_rule/    # Identity/persona (PRN)
│   │       └── assets/identity/ # Persona files (soul.md, etc.)
│   ├── Node/                    # SessionNode
│   └── configs/                 # Orchestrator_configs.yaml
│
├── physio_core/                  # 23 chemicals simulation
│   ├── logic/                   # endocrine/, blood/, receptor/, vitals/, reflex/
│   └── configs/                 # PhysioCore_configs.yaml + hormone_spec_ml.yaml
│
├── eva_matrix/                   # 9D psychological state
│   ├── Module/                  # AxesComputation, ResonanceComputation
│   └── configs/                 # EVA_Matrix_configs.yaml
│
├── artifact_qualia/              # Phenomenological layer
├── resonance_memory_system/      # RMS - affective memory encoding
│   └── Module/                  # encoding_module/, latching_module/
│
├── memory_n_soul_passport/       # MSP - central memory (2,633 lines)
│   ├── Module/                  # EpisodicMemory/, SemanticMemory/, SensoryMemory/
│   ├── schema/                  # 20 JSON schemas
│   └── configs/                 # MSP_configs.yaml
│
├── operation_system/             # Infrastructure
│   ├── identity_manager.py      # ALL system IDs, bus channels, personas
│   ├── resonance_bus.py         # Pub/sub event bus (singleton)
│   ├── llm_bridge/              # Gemini + Ollama bridges
│   ├── nexus_mind/              # NexusMind engine
│   ├── trajectory/              # Execution tracing
│   └── rim/                     # Resonance Impact Measurement
│
├── capabilities/
│   ├── services/
│   │   ├── agentic_rag/         # 7-stream RAG (870 lines)
│   │   ├── engram_system/       # O(1) reflex cache
│   │   ├── slm_bridge/          # Llama 1B (System 1)
│   │   ├── vector_bridge/       # ChromaDB
│   │   └── graph_bridge/        # GraphRAG
│   └── tools/
│       ├── resonance_index/     # RI scoring (4-layer)
│       ├── resonance_impact/    # RIM calculation
│       ├── subagents/           # RIS, Archivist, Technician
│       ├── ui/                  # Flask debug UI
│       ├── msp_monitor.py
│       └── logger.py
│
├── contracts/                    # Interface definitions
│   ├── systems/                 # IMSPassport, IPhysioSystem, IMatrixSystem, IResonanceBus
│   └── modules/                 # IMemoryStorage, IMemoryRetrieval, etc.
│
├── consciousness/                # Awareness Domain (LLM read/write)
│   ├── context_container/       # Active turn workspace
│   ├── episodic_memory/         # episodes/, episodes_user/, episodes_ai/, episodic_log.jsonl
│   ├── state_memory/            # Bio/psych/qualia snapshots (JSON)
│   ├── sensory_memory/          # Qualia records
│   ├── indexes/                 # Episode counters, salience maps
│   ├── data/                    # Transient scratchpad
│   ├── services/                # Symlinks to capabilities/services
│   └── tools/                   # Symlinks to capabilities/tools
│
├── memory/                       # Subconscious (MSP-only write, LLM cannot write)
│   ├── context_storage/         # Persistent context (full/, step1-3/)
│   ├── user_profile/
│   ├── user_registry.json
│   └── vector_store/            # ChromaDB (chroma.sqlite3)
│
├── api/                          # FastAPI + WebSocket + EVA Lite
├── webui/                        # Vue.js/Vite frontend
├── tools/technician/             # Registry auditor
├── tests/                        # 11 test files
├── scripts/                      # 5 audit/verification scripts
├── registry/                     # eva_master_registry.yaml (SSOT)
├── docs/                         # Full documentation tree
├── .agent/                       # Rules, governance, tasks, workflows
└── .planning/                    # MSP implementation checklists
```

## 4. Development Conventions

*   **Schema-First (Doc-to-Code):** All features start as YAML config → code implements config → "Ghost Keys" = unimplemented config = your job ticket. See: `docs/07_Protocols/DOC_TO_CODE.md`
*   **Centralized Identity:** Never hardcode IDs. Use `IdentityManager.BUS_PHYSICAL`, `IdentityManager.SYSTEM_MSP`, etc. See: `docs/adr/007_centralized_identity_management.md`
*   **Consciousness vs Subconscious:** `consciousness/` = LLM can read/write. `memory/` = MSP-only write, LLM reads via RAG. See: `docs/adr/008_Memory_Architecture_Centralized_MSP.md`
*   **Signal-First Architecture:** Systems communicate via Resonance Bus pub/sub, never direct method calls.
*   **Logging:** `from capabilities.tools.logger import safe_print` then `print = safe_print`. Format: `[MODULE] [LEVEL] Message`
*   **Config files:** Unified per system (e.g., `PhysioCore_configs.yaml` not separate endocrine/receptor/blood configs).
*   **Module hierarchy:** System → Module → Node → Component (see `docs/03_Architecture/EVA_System_Architecture.md`)

### Code Style:

*   Object-oriented with extensive type hints
*   `snake_case` for functions/variables, `PascalCase` for classes
*   Constants: `UPPER_SNAKE_CASE`
*   Config files: `{Module}_configs.yaml`
*   Schemas: `{Module}_Payload_Schema_v2.json`

### Key ADRs:

| ADR | Decision |
|-----|----------|
| `001` | CIM replaced CIN (file injection, not text building) |
| `002` | 2-stage RAG retrieval (quick ‖ physio, then deep) |
| `004` | Single-inference architecture (1 LLM session) |
| `005` | Unified Resonance Architecture |
| `006` | Hybrid GraphRAG integration |
| `007` | Centralized IdentityManager |
| `008` | MSP as memory SSOT |

## 5. Resonance Bus Channels

| Channel | Direction | Purpose |
|---------|-----------|---------|
| `bus:physical` | PhysioCore → Matrix | Hormone/vital state |
| `bus:psychological` | Matrix → Qualia | 9D psychological state |
| `bus:phenomenological` | Qualia → MSP | Sensory texture |
| `bus:knowledge` | RAG ↔ MSP | Memory retrieval signals |
| `bus:cognitive` | GKS/NexusMind | NOT YET ACTIVE |
| `bus:temporal` | Temporal Engine | NOT YET ACTIVE |

## 6. Critical Documents

| Document | Path |
|----------|------|
| Cognitive Flow 2.0 | `docs/06_Orchestration/cognitive_flow/Cognitive_Flow_2_0.md` |
| System Architecture | `docs/03_Architecture/EVA_System_Architecture.md` |
| Storage ERD | `docs/03_Architecture/EVA_System_Storage_ERD.md` |
| Gap Flow | `docs/03_Architecture/EVA_Gap_Flow.md` |
| Memory 8-8-8 | `docs/01_Philosophies/MEM_PHILOSOPHY_888.md` |
| DOC_TO_CODE | `docs/07_Protocols/DOC_TO_CODE.md` |
| Master Registry | `registry/eva_master_registry.yaml` |
