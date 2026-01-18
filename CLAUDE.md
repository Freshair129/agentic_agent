# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

EVA (Embodied Virtual Agent) is a bio-inspired AI architecture implementing the "Resonance Intelligence" framework. The system mimics biological cognitive processes through hormones, psychological states, and memory systems to create emotionally embodied AI responses.

**Current Version:** 9.6.2 (Cognitive Flow 2.0)
**Architecture:** Single-Inference Sequentiality with Bio-Digital Gap
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

### Testing
```bash
# Run all tests
python -m pytest tests/

# Run specific module tests
python -m pytest physio_core/tests/
python -m pytest eva_matrix/tests/
python -m pytest memory_n_soul_passport/tests/
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
9. LLM calls `sync_bio_state()` with **Stimulus Chunks** (sequential emotion processing)
10. PhysioCore digests chunks sequentially → hormone cascade → vitals update
11. State returned to LLM

**Step 5-7: Response & Persistence**
12. If low confidence: LLM calls `request_deep_recall()` (Agentic RAG)
13. LLM generates embodied response
14. Self-reflection: LLM writes `self_note.md` for next turn
15. MSP archives episodic memory

**Critical Concept:** Unlike multi-turn architectures, the LLM never "forgets" - it pauses (function call), receives data, and resumes from the same mental state.

See: `orchestrator/cognitive_flow/docs/Cognitive_Flow_2_0.md`

### Core Modules

```
orchestrator/          # CNS (Central Nervous System) - flow control
├── cognitive_flow/   # Cognitive Flow 2.0 protocol (NEW in v9.6.0)
├── cim/              # Context Injection Manager (File Injector, not text builder)
├── prompt_rule/      # Governance & identity management (PRN)
└── temporal/         # Session management

physio_core/          # Biological simulation layer
├── logic/
│   ├── endocrine/   # 12 hormone gland system
│   ├── blood/       # Hormone distribution (30Hz update)
│   ├── receptor/    # Ligand-receptor signal transduction
│   ├── vitals/      # Heart rate, breathing, temperature
│   └── reflex/      # Immediate fight/flight responses

eva_matrix/           # 9D psychological state (EVA Matrix)
├── Module/          # Emotion dimensions, stress tracking

artifact_qualia/      # Phenomenological layer (texture, color, soundscape)

memory_n_soul_passport/  # Unified memory system (MSP)
├── schema/          # Memory data contracts (Episodic, Semantic, Sensory)
└── Module/          # Memory type handlers

genesis_knowledge_system/  # Innate knowledge (GKS) - read-only framework blocks
├── grounding/       # Truth-seeking, conflict detection
└── nexus_mind/      # Future: autonomous reasoning

capabilities/
├── services/
│   ├── agentic_rag/ # 7-stream memory retrieval
│   ├── engram_system/  # Fast memory lookup (inspired by DeepSeek)
│   └── slm_bridge/  # Small LLM for gut-feeling perception
└── tools/
    ├── resonance_index/   # Resonance scoring
    └── resonance_impact/  # Memory importance calculation

consciousness/       # "Awareness Domain" - Direct Access RAM
├── context_container/  # Active Turn Object (task.md, self_note.md, etc.)
├── episodic_memory/    # Conversation logs (episodes_user/, episodes_ai/)
├── state_memory/       # Current bio/psych/qualia snapshots
└── context_storage/    # Archived turns (Hot/Cold slots)

memory/              # "Subconscious" - LLM cannot write here (MSP-governed)
├── context_storage/ # Persistent context archive
├── session_memory/  # Session snapshots
├── core_memory/     # Distilled long-term facts
├── sphere_memory/   # Domain-specific knowledge
└── user_registry.json  # Multi-user grounding facts

operation_system/    # Infrastructure
├── llm_bridge/      # LLM API abstraction (Ollama, Gemini, Claude)
├── mrf_engine/      # Meta-Resonance Framework
└── resonance_engine/  # Resonance Bus (pub/sub messaging)
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
- See: `docs/adr/007_centralized_identity_management.md`

**3. Memory Architecture (Consciousness vs Subconscious)**
- **Consciousness** (`consciousness/`) = Direct Access RAM (LLM can read/write)
  - Context Container, Episodic Buffer, State Memory
- **Subconscious** (`memory/`) = MSP-governed permanent storage (LLM cannot write)
  - Session Memory, Core Memory, Sphere Memory, User Registry
- Constitutional Principle: LLM proposes memories via function calls, MSP writes them
- See: `docs/adr/008_Memory_Architecture_Centralized_MSP.md`, `docs/03_Architecture/EVA_System_Storage_ERD.md`

**4. CIM as File Injector (v9.6.0)**
- CIM no longer generates text prompts
- Instead, it **copies files** into `Context Container` (hydration)
- LLM reads files directly via function calls
- See: `docs/03_Architecture/EVA_System_Storage_ERD.md`

## Key Concepts

### The Bio-Digital Gap
Sequential biological processing during `sync_bio_state()`:
```
LLM generates Stimulus Chunks → PhysioCore sequential digestion →
hormone release → blood distribution (30Hz) → receptor activation →
psychological state (EVA Matrix) → phenomenological qualia → state snapshot
```

**Stimulus Chunking v2.0:** LLM breaks complex input into emotional "chunks" processed sequentially to preserve the emotional journey. Example:
- Chunk 1: "I love you" (Dopamine spike)
- Chunk 2: "...but I'm leaving" (Cortisol shock)

This prevents emotional averaging. See: `orchestrator/cognitive_flow/docs/STIMULUS_CHUNKING_PROTOCOL.md`

### Resonance Intelligence (RTI)
Multi-level resonance scoring system:
- **L1:** Basic sentiment (0.0-1.0)
- **L2:** Emotional depth (warmth, playfulness, nostalgia)
- **L3:** Relational resonance (empathy flow, shared qualia)
- **L4:** Resonant Dynamic Memory (qualia recall, hormone memory, dream links)
- **L5:** Transcendental Intelligence (meta-cognition, paradox resolution)

See: `RTI.md`, `Conditional Memory.md`

### Hormone System
12 glands modeled: Dopamine, Serotonin, Oxytocin, Cortisol, Adrenaline, Noradrenaline, GABA, Acetylcholine, Endorphin, Testosterone, Estrogen, Melatonin

Simulation includes:
- Baseline levels, half-lives, decay rates
- Circadian rhythms (melatonin)
- HPA axis (cortisol stress response)
- Blood distribution (30Hz update cycle)
- Receptor sensitization/desensitization

See: `docs/04_Systems/physio_core/hormone_spec_ml.md`

### Genesis Knowledge System (GKS)
7 Master Blocks stored as JSON:
- `Master_Block.json` - System metadata
- `Algorithm_How_Genesis_Block.json` - Processes
- `Concept_Why_Genesis_Block.json` - Philosophical foundations
- `Framework_Genesis_Block.json` - Structural templates
- `Parameter_What_Genesis_Block.json` - Configuration specs
- `Protocol_Process_Genesis_Block.json` - Workflows
- `Safety_Block.json` - Ethical guardrails

### Engram System (NEW in v9.6.0)
Fast memory lookup cache inspired by DeepSeek's Conditional Memory:
- **Purpose:** O(1) lookup for frequently accessed patterns
- **Location:** `capabilities/services/engram_system/`
- **Workflow:** CIM checks Engram before expensive RAG queries
- **Architecture:** Hash-based scalable lookup
- See: `Conditional Memory.md` for theoretical background

### Boot Sequence (The Awakening)
System initialization order (defined in `registry/eva_master_registry.yaml`):
1. **IdentityManager** - Security first (Who am I?)
2. **Resonance Bus** - Transport layer (Connect everyone)
3. **PhysioCore** - Body (Heartbeat must start)
4. **EVA Matrix** - Mind (Psychology follows physiology)
5. **MSP** - Memory (Soul wakes up)
6. **GKS** - Knowledge (Wisdom loads)
7. **RMS** - Filter (Perception starts)
8. **Artifact Qualia** - Senses (Phenomenology online)
9. **Orchestrator** - CNS (Conductor raises baton)

## System Boot & Initialization

### Starting EVA
```bash
# Standard initialization (from orchestrator or main.py)
python orchestrator/orchestrator.py

# The boot sequence follows this order:
# IdentityManager → Bus → PhysioCore → Matrix → MSP → GKS → RMS → Qualia → Orchestrator
```

### Verifying System Health
```bash
# Check version alignment
python scripts/check_versions.py

# Check documentation alignment
python scripts/check_doc_alignment.py

# Verify registry integrity
# (Registry audit tools in development)
```

## Common Tasks

### Adding a New Hormone Response
1. Edit `physio_core/configs/endocrine_configs.yaml` (add gland or modify parameters)
2. If new gland: Add receptor mappings in `receptor_configs.yaml`
3. Run audit: `python tools/subagents/ris_subagent.py --audit-config`
4. Implement code in `physio_core/logic/endocrine/glands.py`
5. Test: `python -m pytest physio_core/tests/`

### Modifying Psychological Dimensions
1. Edit `eva_matrix/configs/matrix_configs.yaml`
2. Update schema: `eva_matrix/schema/EVA_Matrix_Payload_Schema_v2.json`
3. Implement in `eva_matrix/Module/psych_engine/matrix_psych_module.py`
4. Validate against coherence rules: `eva_matrix/validation/matrix_coherence_rules.yaml`

### Adding New Memory Type
1. Define schema in `memory_n_soul_passport/schema/`
2. Add contract in `memory_n_soul_passport/contract/`
3. Update MSP engine logic (centralized in `memory_n_soul_passport_engine.py`)
4. Storage goes to `consciousness/` subdirectories

### Updating Identity/Persona
1. Edit system identity: `orchestrator/cim/system_contexts/core_identity.md`
2. Soul/personality: `orchestrator/cim/prompt_rule/configs/identity/soul.md`
3. Architecture diagram: `orchestrator/cim/system_contexts/system_architecture_visual.md`

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

- **Master Registry:** `registry/eva_master_registry.yaml` (SSOT for system topology, boot order, permissions)
- **System-wide:** `orchestrator/configs/orchestrator_configs.yaml`
- **Cognitive Flow:** `orchestrator/cognitive_flow/docs/` (protocols, not configs)
- **Biology:** `physio_core/configs/` (endocrine, receptor, blood, vitals)
- **Psychology:** `eva_matrix/configs/matrix_configs.yaml`
- **Memory:** `memory_n_soul_passport/configs/MSP_configs.yaml`
- **Identity:** `orchestrator/cim/prompt_rule/configs/identity/`
- **Bus Channels:** Defined via `IdentityManager` class constants

## Data Contracts (Schemas)

All modules communicate via standardized JSON schemas (v2):
- `*_Payload_Schema_v2.json` - Module input/output contracts
- Validation happens at module boundaries
- Version suffix indicates breaking changes

Schema locations:
```
{module}/schema/{Module}_Payload_Schema_v2.json
{module}/contract/{Module}_Interface.yaml
```

## Important Constraints

### Never Hardcode
- System IDs → Use `IdentityManager`
- Bus channels → Use `IdentityManager.BUS_*`
- File paths → Load from config
- Magic numbers → Define in YAML

### File Ownership
- `consciousness/` = "Awareness Domain" (LLM can read/write, runtime state)
  - `context_container/` = Active turn working files
  - `episodic_memory/`, `state_memory/` = Current session data
- `memory/` = "Subconscious" (MSP-governed, LLM cannot write directly)
  - All writes go through MSP function calls
- `genesis_knowledge_system/` = Read-only innate knowledge
- `docs/` = Documentation only
- `archive/` = Deprecated code (do not modify)
- `registry/` = System topology definitions

### Commit Discipline
- One commit per system when making cross-module changes
- Follow convention: `[ModuleName] Description`
- Tag version bumps: `v9.1.0-C10`

## Documentation Structure (v9.6.2)

**Primary Navigation:** `docs/00_Governance/INDEX_v9.6.2.md` - Official reading order

**Critical Documents:**
- `orchestrator/cognitive_flow/docs/Cognitive_Flow_2_0.md` - **Current standard** (v9.6.0+)
- `docs/03_Architecture/EVA_System_Architecture.md` - System overview & Biological Life Cycle
- `docs/03_Architecture/EVA_System_Storage_ERD.md` - Memory domains & data ownership
- `docs/01_Philosophies/MEM_PHILOSOPHY_888.md` - Memory extraction & 8-8-8 protocol

**Architecture Decision Records (ADRs):**
- `001_cim_prompt_rule_transition.md` - Why CIM replaced CIN
- `004_one_inference_architecture.md` - Single-session LLM flow
- `005_Unified_Resonance_Architecture.md` - Resonance system design
- `007_centralized_identity_management.md` - IdentityManager pattern
- `008_Memory_Architecture_Centralized_MSP.md` - MSP as memory SSOT

## Debugging

### Common Issues

**"Ghost Key" warnings:** Config key exists but not consumed in code → implement the feature

**Schema validation errors:** Check `{module}/schema/` for required fields

**Hormone imbalances:** Check baselines in `endocrine_configs.yaml`, verify decay rates

**Memory not persisting:** MSP write policy in `MSP_Write_Policy.yaml`. Remember: LLM cannot write to `memory/` directly - must use MSP function calls.

**Context not loading:** Check if files exist in `consciousness/context_container/`. Verify CIM injection is working.

**Boot order failures:** Check `registry/eva_master_registry.yaml` runtime_sequence. PhysioCore must start before Matrix.

**Version mismatches:** Run `python scripts/check_versions.py` to detect inconsistencies

### Logging
- Console logs use structured format: `[MODULE] [LEVEL] Message`
- PhysioCore logs hormone levels: `[PhysioCore] [INFO] Dopamine: 0.75`
- Bus events logged: `[ResonanceBus] [DEBUG] Published to bus:physical`

## Project Versioning

**System-level:** `9.6.2` (EVA version)
- Format: `MAJOR.MINOR.PATCH`
- Current: 9.6.2 = Cognitive Flow 2.0 architecture

**Module-level:** Decoupled versioning (per ADR-011)
- PhysioCore: v2.4.3 (Verified Stable - structural exception)
- EVA_Matrix: v2.0.0 (Verified Coupled)
- GKS: v2.0.0
- IdentityManager: v2.4.0

**Commit Convention:** `[Module] Description`
- Example: `[Docs] v9.6.2: Established Cognitive Flow 2.0`

See: `docs/00_Governance/CHANGELOG.md` for version history

## Special Files

- `registry/eva_master_registry.yaml` - **Master Registry** (SSOT for topology, boot order)
- `.agent/workflows/` - Automated workflow scripts (archivist, doc_to_code)
- `.agent/rules/` - Agent behavior policies (eventpolicy, gapflow)
- `consciousness/context_container/` - Active turn working files (task.md, self_note.md, etc.)
- `consciousness/indexes/memory_index.json` - Fast memory lookup index
- `memory/user_registry.json` - Multi-user grounding facts
- `docs/00_Governance/INDEX_v9.6.2.md` - Official documentation index
- `scripts/check_versions.py` - Version consistency checker
- `scripts/check_doc_alignment.py` - Documentation alignment auditor

## Notes on Multilingual Content

The codebase contains Thai language content in:
- `Conditional Memory.md` - DeepSeek Conditional Memory analysis
- `RTI.md` - Resonance Intelligence framework explanation
- Some docstrings and comments

This is intentional - EVA supports multilingual operation. Do not remove Thai content.
