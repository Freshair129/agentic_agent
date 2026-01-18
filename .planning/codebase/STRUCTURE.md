# Codebase Structure

**Analysis Date:** 2026-01-18

## Directory Layout

```
agent/
├── .agent/                # Agent workflows and rules
├── .planning/             # GSD project management (new)
├── api/                   # FastAPI web layer
├── artifact_qualia/       # Phenomenological layer
├── capabilities/          # Services, skills, tools
│   ├── services/         # Agentic RAG, Engram, SLM, Vector/Graph bridges
│   ├── skills/           # Reusable capabilities
│   └── tools/            # Utilities (logger, resonance scoring)
├── consciousness/         # Working memory (LLM read/write)
│   ├── context_container/    # Active turn files
│   ├── episodic_memory/      # Recent conversation logs
│   ├── state_memory/         # Bio/psych/qualia snapshots
│   └── context_storage/      # Archived turns (hot/cold)
├── contracts/             # Cross-module data contracts
├── docs/                  # Documentation (ADRs, architecture, protocols)
├── eva_matrix/            # 9D psychological state
├── genesis_knowledge_system/  # Read-only knowledge blocks
├── memory/                # Permanent storage (MSP-governed)
├── memory_n_soul_passport/    # MSP engine
├── operation_system/      # Infrastructure (LLM, Bus, MRF)
├── orchestrator/          # CNS control
│   ├── cognitive_flow/   # Cognitive Flow 2.0 protocols
│   ├── cim/              # Context Injection Manager
│   └── prompt_rule/      # Identity & governance
├── physio_core/           # Biological simulation
├── registry/              # Master registry (SSOT)
├── resonance_memory_system/  # RMS (filter layer)
├── scripts/               # Verification utilities
├── tests/                 # Root-level tests
└── tools/                 # Subagents (RIS auditor, etc.)
```

## Directory Purposes

**api/**
- Purpose: External API layer (FastAPI endpoints)
- Contains: `run_server.py`, `eva_lite.py`, `chat_endpoint.py`
- Key files: `api/requirements.txt` (FastAPI, Uvicorn, Pydantic)

**orchestrator/**
- Purpose: Central Nervous System - main flow control
- Contains: Cognitive Flow 2.0, CIM (context injector), Prompt Rule (identity)
- Key files: `orchestrator/orchestrator.py` (main entry), `cognitive_flow/docs/Cognitive_Flow_2_0.md`

**physio_core/**
- Purpose: Biological simulation (12 hormones, vitals, reflexes)
- Contains: `logic/` (endocrine, blood, receptor, vitals, reflex)
- Key files: `physio_core/physio_core.py` (304 lines), `configs/endocrine_configs.yaml`
- Note: **Structural Exception** - uses `logic/` instead of `Module/Node` (performance critical)

**eva_matrix/**
- Purpose: Psychological state computation
- Contains: `Module/psych_engine/`
- Key files: `eva_matrix/eva_matrix.py` (152 lines), `configs/matrix_configs.yaml`

**memory_n_soul_passport/**
- Purpose: Unified memory system (largest module)
- Contains: MSP Engine, schema definitions
- Key files: `memory_n_soul_passport_engine.py` (2453 lines!), `configs/MSP_configs.yaml`

**artifact_qualia/**
- Purpose: Phenomenological layer (texture, color, soundscape)
- Contains: `Module/qualia_integrator/`
- Key files: `artifact_qualia/artifact_qualia.py`

**genesis_knowledge_system/**
- Purpose: Innate knowledge (read-only)
- Contains: 7 Master JSON Blocks, grounding logic
- Key files: `Master_Block.json`, `Algorithm_How_Genesis_Block.json`, etc.

**consciousness/**
- Purpose: Working memory (Direct Access RAM for LLM)
- Contains: Context Container, episodic buffer, state snapshots
- Key files: `context_container/task.md`, `context_container/self_note_epXX.md`

**memory/**
- Purpose: Permanent storage (Subconscious - LLM cannot write)
- Contains: Long-term episodic, core memory, sphere memory
- Key files: `user_registry.json`

**capabilities/**
- Purpose: Reusable services and tools
- Contains: Agentic RAG, Engram system, SLM bridge, Vector/Graph bridges
- Key files: `services/agentic_rag/agentic_rag_engine.py`, `services/engram_system/engram_engine.py`

**operation_system/**
- Purpose: Infrastructure layer
- Contains: LLM Bridge, Resonance Bus, MRF Engine
- Key files: `llm_bridge/llm_bridge.py`, `resonance_engine/`

**registry/**
- Purpose: Single source of truth for system topology
- Contains: Master registry (v9.6.2)
- Key files: `eva_master_registry.yaml`

**docs/**
- Purpose: Documentation
- Contains: ADRs, architecture diagrams, protocols, philosophies
- Key files: `00_Governance/INDEX_v9.6.2.md`, `03_Architecture/EVA_System_Architecture.md`

**contracts/**
- Purpose: Data contracts between modules
- Contains: Module contracts, system contracts
- Key files: `{module}/{Module}_Interface.yaml`

## Key File Locations

**Entry Points:**
- `api/run_server.py`: FastAPI server launcher
- `api/eva_lite.py`: Lightweight bio-simulation test
- `orchestrator/orchestrator.py`: Main orchestrator

**Configuration:**
- `registry/eva_master_registry.yaml`: SSOT for system topology
- `{module}/configs/`: Module-specific YAML configs
- `.env`: API keys (not committed)

**Core Logic:**
- `physio_core/physio_core.py`: PhysioCore main class (304 lines)
- `eva_matrix/eva_matrix.py`: EVA Matrix main class (152 lines)
- `memory_n_soul_passport/memory_n_soul_passport_engine.py`: MSP engine (2453 lines)
- `operation_system/llm_bridge/llm_bridge.py`: Gemini integration

**Testing:**
- `{module}/tests/test_{module}_init.py`: Module initialization tests
- `tests/`: Root-level integration tests
- Test framework: pytest

## Naming Conventions

**Files:**
- Snake_case: `physio_core.py`, `eva_matrix.py`
- Config files: `{Module}_configs.yaml`
- Schemas: `{Module}_Payload_Schema_v2.json`
- Tests: `test_{module}_init.py`

**Directories:**
- Snake_case: `physio_core/`, `eva_matrix/`, `memory_n_soul_passport/`
- Module structure: `{module}/Module/` or `{module}/logic/` (PhysioCore exception)
- Configs: `{module}/configs/`
- Schemas: `{module}/schema/`

## Where to Add New Code

**New Module:**
- Primary code: Create `{module}/` in root
- Structure: `{module}/Module/` (or `logic/` if performance-critical)
- Config: `{module}/configs/{Module}_configs.yaml`
- Schema: `{module}/schema/{Module}_Payload_Schema_v2.json`
- Contract: `{module}/contract/{Module}_Interface.yaml`
- Tests: `{module}/tests/test_{module}_init.py`
- Register: Add to `registry/eva_master_registry.yaml`

**New Service/Tool:**
- Implementation: `capabilities/services/{service_name}/`
- Tools: `capabilities/tools/{tool_name}/`

**New Memory Type:**
- Schema: `memory_n_soul_passport/schema/`
- Handler: Update `memory_n_soul_passport_engine.py`
- Storage: `consciousness/` (working) or `memory/` (permanent)

**Utilities:**
- Shared helpers: `capabilities/tools/`
- Logger: Use `capabilities/tools/logger.py`

## Special Directories

**consciousness/**
- Purpose: Working memory (active turn state)
- Generated: Yes (runtime)
- Committed: No (runtime state only)

**memory/**
- Purpose: Permanent memory storage
- Generated: Yes (by MSP)
- Committed: Depends (user data, typically no)

**.planning/**
- Purpose: GSD project management
- Generated: Yes (by GSD)
- Committed: Yes (planning artifacts)

**archive/**
- Purpose: Deprecated code (do not modify)
- Generated: No
- Committed: Yes (historical reference)

**docs/docs.rar**
- Purpose: Compressed documentation backup
- Generated: Yes
- Committed: Yes
- Size: 216KB

---

*Structure analysis: 2026-01-18*
