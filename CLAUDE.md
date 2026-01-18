# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

EVA (Embodied Virtual Agent) is a bio-inspired AI architecture implementing the "Resonance Intelligence" framework. The system mimics biological cognitive processes through hormones, psychological states, and memory systems to create emotionally embodied AI responses.

**Current Version:** 9.1.0 (Resonance Edition)
**Architecture:** Dual-Phase One-Inference with Bio-Digital Gap
**Language:** Python 3.13
**Core Pattern:** Schema-First ("Doc-to-Code" Protocol)

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

### One-Inference Flow
EVA uses a single LLM inference session with function calling:

1. **Phase 1 (Perception):** LLM receives user input → calls `sync_biocognitive_state()`
2. **The Gap (Bio-Digital Processing):** Local CPU executes PhysioCore → Matrix → Qualia → Memory RAG
3. **Phase 2 (Reasoning):** LLM receives bio-state → generates embodied response → calls `propose_episodic_memory()`

See: `docs/adr/004_one_inference_architecture.md`

### Core Modules

```
orchestrator/          # Central flow control, manages dual-phase loop
├── cim/              # Context Injection Manager (CIM) - builds LLM prompts
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

consciousness/       # Runtime state & episodic memory storage
├── episodic_memory/ # Conversation logs (episodes_user/, episodes_ai/)
├── state_memory/    # Current bio/psych/qualia snapshots
└── context_storage/ # Full-context prompts per turn

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
- See: `docs/07_Protocols/DOC_TO_CODE.md`

**2. Centralized Identity Management**
- All system IDs, bus channels, personas managed by `IdentityManager`
- Never hardcode IDs like `"bus:physical"` → use `IdentityManager.BUS_PHYSICAL`
- See: `docs/adr/007_centralized_identity_management.md`

**3. Memory Centralization**
- MSP = Single source of truth for all lived experience
- GKS = Read-only innate knowledge (frameworks, safety rules)
- See: `docs/adr/008_Memory_Architecture_Centralized_MSP.md`

## Key Concepts

### The Bio-Digital Gap
The sequential processing that happens between LLM perception and reasoning:
```
stimulus → hormone release → blood distribution → receptor activation →
psychological state → phenomenological qualia → memory retrieval → response
```

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

## Configuration Locations

- **System-wide:** `orchestrator/configs/orchestrator_configs.yaml`
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
- `consciousness/` = Runtime state (modified during execution)
- `genesis_knowledge_system/` = Read-only innate knowledge
- `docs/` = Documentation only
- `archive/` = Deprecated code (do not modify)

### Commit Discipline
- One commit per system when making cross-module changes
- Follow convention: `[ModuleName] Description`
- Tag version bumps: `v9.1.0-C10`

## Architecture Decision Records (ADRs)

Critical ADRs to understand:
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

**Memory not persisting:** MSP write policy in `MSP_Write_Policy.yaml`

**LLM context too large:** Reduce prompt size via CIM tier settings

### Logging
- Console logs use structured format: `[MODULE] [LEVEL] Message`
- PhysioCore logs hormone levels: `[PhysioCore] [INFO] Dopamine: 0.75`
- Bus events logged: `[ResonanceBus] [DEBUG] Published to bus:physical`

## Project Versioning

Semantic versioning: `MAJOR.MINOR.PATCH-BUILD`
- Example: `9.1.0-C10` = Version 9.1.0, Commit 10
- MAJOR = Architecture changes
- MINOR = New modules/features
- PATCH = Bug fixes
- BUILD = Sequential commit counter

## Special Files

- `.agent/workflows/` - Automated workflow scripts (archivist, doc_to_code)
- `.agent/rules/` - Agent behavior policies (eventpolicy, gapflow)
- `consciousness/indexes/memory_index.json` - Fast memory lookup index
- `memory/user_registry.json` - Multi-user grounding facts

## Notes on Multilingual Content

The codebase contains Thai language content in:
- `Conditional Memory.md` - DeepSeek Conditional Memory analysis
- `RTI.md` - Resonance Intelligence framework explanation
- Some docstrings and comments

This is intentional - EVA supports multilingual operation. Do not remove Thai content.
