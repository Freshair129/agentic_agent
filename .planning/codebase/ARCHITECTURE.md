# Architecture

**Analysis Date:** 2026-01-18

## Pattern Overview

**Overall:** Bio-Driven Embodied Cognition with Event-Driven Architecture

**Key Characteristics:**
- Single-Inference Sequentiality (Cognitive Flow 2.0) - LLM pauses but never forgets
- Biological simulation mimics human cognition (hormones → psychology → phenomenology)
- Event-driven communication via Resonance Bus (pub/sub)
- Strict module contracts with schema validation (JSON Schema v2)
- 9-stage boot sequence ("The Awakening")

## Layers

**1. Infrastructure Layer:**
- Purpose: Core services and communication
- Location: `operation_system/`
- Contains: LLM Bridge, Resonance Bus (pub/sub), MRF Engine
- Depends on: External APIs (Gemini)
- Used by: All higher layers

**2. Biological Layer (PhysioCore):**
- Purpose: Simulate human physiology (12 hormones, vitals, reflexes)
- Location: `physio_core/`
- Contains: Endocrine Engine, Blood Engine (30Hz), Receptor Engine, Vitals, Reflex
- Depends on: Resonance Bus
- Used by: EVA Matrix (psychology)
- Critical: Runs at 30Hz, performance-optimized

**3. Psychological Layer (EVA Matrix):**
- Purpose: 9D psychological state from biological signals
- Location: `eva_matrix/`
- Contains: Matrix Psych Module, emotion dimensions, stress tracking
- Depends on: PhysioCore (hormone panels)
- Used by: Orchestrator, Qualia
- Output: Psychological state vector

**4. Phenomenological Layer (Artifact Qualia):**
- Purpose: Sensory/perceptual layer (texture, color, soundscape)
- Location: `artifact_qualia/`
- Contains: Qualia Integrator
- Depends on: EVA Matrix
- Used by: Memory systems

**5. Memory Layer (MSP):**
- Purpose: Unified memory management (Episodic, Semantic, Sensory)
- Location: `memory_n_soul_passport/`
- Contains: MSP Engine (2453 lines - largest module)
- Depends on: ChromaDB, Qualia, Matrix
- Used by: Orchestrator (memory retrieval)
- Storage: `consciousness/` (working) + `memory/` (permanent)

**6. Knowledge Layer (GKS):**
- Purpose: Read-only innate knowledge (frameworks, safety)
- Location: `genesis_knowledge_system/`
- Contains: 7 Master Blocks (JSON), Grounding, Nexus Mind
- Depends on: None (foundational)
- Used by: All reasoning systems

**7. Orchestration Layer (CNS):**
- Purpose: Central nervous system - coordinates all modules
- Location: `orchestrator/`
- Contains: Cognitive Flow 2.0 protocol, CIM (Context Injector), Prompt Rule (identity)
- Depends on: All layers
- Used by: External API calls

**8. API Layer:**
- Purpose: External interface (web, chat)
- Location: `api/`
- Contains: FastAPI endpoints, EVA Lite, chat endpoint
- Depends on: Orchestrator
- Used by: External clients

## Data Flow

**Cognitive Flow 2.0 (Single-Inference Sequentiality):**

1. **User Input** → CNS (Orchestrator) → CIM (Context Assembler)
2. **CIM checks Engram** (fast O(1) lookup)
3. **CIM bundles** Input + Engram + Body State (from Bus)
4. **SLM processes** bundle → Intent/Signal
5. **CNS routes** to MSP/RAG for Quick Recall
6. **Memory + Context** → CIM finalizes injection → **Context Container**
7. **LLM Reasoning** (Gemini) reads Context Container
8. **Confidence Check**: LLM decides if deep recall needed
9. **LLM calls** `sync_bio_state()` with **Stimulus Chunks**
10. **PhysioCore digests chunks** sequentially → hormone cascade
11. **Hormone Panel** → Blood (30Hz) → Receptors → Vitals
12. **EVA Matrix** reads hormones → 9D psych state
13. **Artifact Qualia** reads psych → phenomenology
14. **State snapshot** → returned to LLM
15. **LLM generates response** (embodied with bio-state)
16. **Self-reflection**: LLM writes `self_note.md` for next turn
17. **MSP archives** episode to long-term memory

**State Management:**
- Working memory: `consciousness/context_container/` (active turn files)
- State snapshots: `consciousness/state_memory/`
- Permanent memory: `memory/` (MSP-governed, LLM cannot write)

## Key Abstractions

**Context Container:**
- Purpose: Active turn working memory (files injected by CIM)
- Examples: `consciousness/context_container/task.md`, `self_note_epXX.md`
- Pattern: File-based, not text prompts

**Stimulus Chunks:**
- Purpose: Sequential emotional processing (preserves emotional journey)
- Examples: "I love you" (chunk 1) → "but I'm leaving" (chunk 2)
- Pattern: List of valence/arousal/intensity objects

**Resonance Bus:**
- Purpose: Pub/sub event system for module communication
- Examples: `BUS_PHYSICAL`, `BUS_PSYCHOLOGICAL`
- Pattern: Channel-based messaging

**Schema Contracts:**
- Purpose: Strict data validation between modules
- Examples: `{module}/schema/*_Payload_Schema_v2.json`
- Pattern: JSON Schema validation at boundaries

## Entry Points

**API Server:**
- Location: `api/run_server.py`
- Triggers: HTTP requests
- Responsibilities: Launch FastAPI + Uvicorn on port 8000

**EVA Lite:**
- Location: `api/eva_lite.py`
- Triggers: Direct execution
- Responsibilities: Minimal bio-simulation for testing

**Orchestrator:**
- Location: `orchestrator/orchestrator.py`
- Triggers: Boot sequence (9 stages)
- Responsibilities: Initialize all modules, manage Cognitive Flow

## Error Handling

**Strategy:** Structured logging + graceful degradation

**Patterns:**
- Try/except with logging: `[MODULE] [ERROR] {message}`
- Safety settings in LLM calls (block harmful content)
- Schema validation failures logged and rejected

## Cross-Cutting Concerns

**Logging:** Custom logger (`capabilities/tools/logger.py`) with `[MODULE] [LEVEL]` format

**Validation:** JSON Schema validation at all module boundaries (v2 schemas)

**Authentication:** IdentityManager system (boot position 1) - custom, no external auth

**Configuration:** YAML-based with master registry (`registry/eva_master_registry.yaml`)

**Versioning:** Decoupled system (9.6.2) vs module versions (PhysioCore 2.4.3, etc.)

---

*Architecture analysis: 2026-01-18*
