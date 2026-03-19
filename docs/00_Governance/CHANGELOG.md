<!-- markdownlint-disable MD024 -->
# Changelog

All notable changes to the EVA Core project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

**LATEST:** v9.7.0 | Epoch: Reflex | 2026-03-20

---

## [v9.7.0-Reflex] - 2026-03-20

### Added

- **4-Layer Affective Reflex System**: Novel architecture for sub-LLM emotional reactions before full response.
  - **Layer 1 (Enum Reflex, <1ms):** Deterministic pattern match → hormone spike + expression (flinch/blush/gasp)
  - **Layer 2 (SLM Gut Utterance, <50ms):** gut_vector → nearest neighbor → short Thai utterance ("ห๊ะ!?", "อืม...")
  - **Layer 3 (Stimulus Extraction, <50ms during Gap):** SLM reads LLM tool arguments → context-aware utterance
  - **Layer 4 (CoT Extraction, optional):** SLM reads LLM thinking tokens → most accurate utterance
  - **No second LLM call** — Constitutional Pillar 2 preserved
  - **No existing AI system implements this combination** (verified via comprehensive market research)

- **Stimulus Chunking Protocol v2.0**: Sequential emotional processing with per-chunk reflex output.
  - Tool schema extension: `stimulus_chunks: [{text, vector, bio_impacts}, ...]`
  - Each chunk triggers separate PhysioCore.step() + reflex via WebSocket
  - Preserves emotional shifts (e.g., warmth→anxiety) instead of averaging
  - Thai cultural nuance handling ("ก็คงดี" = passive-aggressive, not literal "good")

- **Single-Inference Sequentiality Spec**: Formalized in `system_requirements.yaml` with full flow documentation.
  - 6-step pipeline: Start → Pause (Tool Call) → Gap Execution → Inject Context → Resume → Persist
  - Critical distinction documented: "EVA uses Tool Calling to UPDATE ITS OWN INTERNAL STATE, not to fetch external data"

- **System Specifications Created**:
  - `.agent/standards/system_requirements.yaml` — Full tech stack, 10 core systems, 7-stream RAG, API, storage, NFRs, boot sequence, cognitive flow, reflex system, stimulus chunking
  - `.agent/standards/id_standards.yaml` — All ID formats (System, Bus, Turn, Session, Episode, Memory, User, Hormone, Changelog), naming conventions, never-hardcode rules
  - `docs/00_Governance/CHANGELOG_SYSTEM.md` — Sliding window spec, severity levels, EVA-specific tags

- **Version Control Protocol**: Formalized in `.agent/workflows/version-control.md` based on international standards.
  - Semantic Versioning 2.0.0 (semver.org)
  - Conventional Commits 1.0.0 (conventionalcommits.org)
  - Keep a Changelog 1.1.0 (keepachangelog.com)
  - Pre-commit checklist, post-commit checklist, rollback protocol

### Changed

- **CLAUDE.md**: Complete rewrite — verified every path, class, function against actual codebase.
  - Fixed: 45% of directory paths were wrong (14/31)
  - Fixed: 35% of file paths were wrong (12/34)
  - Fixed: "12 hormones" → 23 chemicals (16 hormones + 7 neurotransmitters)
  - Fixed: `sync_bio_state()` → `sync_biocognitive_state()` (actual tool name)
  - Fixed: GKS marked as NOT YET IMPLEMENTED
  - Fixed: memory/ subdirectory structure (removed phantom dirs)
  - Added: 4-Layer Reflex System, Stimulus Chunking, Resonance Bus details, API endpoints, full config table

- **GEMINI.md**: Complete rewrite — moved to `docs/10_References/GEMINI.md` (root policy compliance).
  - Same corrections as CLAUDE.md + EVA-specific development conventions

- **Root Policy Enforcement**: Cleaned up root directory per `.agent/governance/root_policy.yaml`.
  - Moved 4 files out of root (GEMINI.md, CHANGELOG_SYSTEM.md, system_requirements.yaml, id_standards.yaml)
  - Deleted outdated workspace file (contained external project references)
  - Updated policy: removed temporary exemptions, commented out phantom directories

- **Version bump**: 9.6.2 → **9.7.0** (MINOR: new features, backward compatible). Epoch: "Resonance" → **"Reflex"**

### Removed

- **`consciousness/state_memory/matrix_state.json`**: Outdated state file (replaced by `eva_matrix_state.json` with different schema)
- **`.agent/rules/gapflow.md`**: v9.1 superseded by `docs/03_Architecture/EVA_Gap_Flow.md` (v9.6.2)
- **`orchestrator/orchestrator_3phase_backup.py`**: Moved to `orchestrator/archive/` (unreferenced v8.2 backup)

### Fixed

- **Codebase Analysis**: Created `vsoffice/docs/08-eva-codebase-analysis.md` — exhaustive function-by-function documentation of all ~75 files, ~8,000+ lines.

---

## [v9.6.3-ResonanceIntegrated] - 2026-01-19

### Added

- **Master Config System (SSOT)**: Created `registry/master_configs.yaml` to serve as the global "Common Law" for the organism.
  - **Offloaded Metadata**: Moved `organism_version` (v9.6.2) and `unified_paths` out of the registry to prevent version drift and simplify governance.
  - **Governance**: Integrated `IdentityManager` as the primary consumer and distributor of these constants.
- **CNS Execution Slot Formalization**: Established `orchestrator/Execution/` as a dedicated structural slot for master flow logic.
  - **Execution Node**: Implemented `MasterFlowEngine` to manage the multi-phase cognitive cycle (Perception, Gap, Reasoning, Persistence).
  - **Refactoring**: Decoupled `orchestrator.py` from execution mechanics, delegating all flow control to the new engine.

### Added (WebUI & MSP)

- **WebUI Portfolio Dashboard**: Launched a premium React-based dashboard at `agent/webui/`.
  - **Visualization**: Implemented real-time Radar Charts for 9D Matrix and animated Hormone/Vitals panels.
  - **Interaction**: Integrated a sleek Chat Interface with status indicators (Thinking/Ready).
  - **Stack**: Built with Vite 7, React 19, and TailwindCSS v4 with Glassmorphism aesthetics.
- **API Mind-State Extension**:
  - Added `GET /api/mind/state` endpoint for on-demand bio-cognitive snapshots.
  - Enhanced `/ws/chat` to push authoritative state updates during responses.
- **MSP Data Flow Gaps (Resolved)**:
  - **Validation**: Implemented `MSPSchemaValidator` to enforce strict JSON schema compliance during memory persistence.
  - **Monitoring**: Created `MSPDataMonitor` to detect and alert on missing bio-field telemetry.
  - **Schema Coverage**: Achieved 100% coverage across all 8 major output streams (Hormones, Vitals, Matrix, Qualia, etc.).

### Changed

- **Schema Standardization**: Refactored internal storage keys from CamelCase (e.g., `Resonance_index`) to standard `snake_case` (`resonance_index`) across MSP and Orchestrator.
- **Robust Retrieval**: Updated `EpisodicMemoryModule` to support dual-key reading, ensuring backward compatibility with legacy memory records.
- **Inner Organ Documentation**: Created/Updated READMEs for all 18 major root directories and 13 internal sub-modules...
- **Protocol Mirroring**: Synchronized critical rules from `.agent/rules/` to `docs/03_Architecture/` and `docs/07_Protocols/` (Gap Flow, Event Policy, Permissions).
- **Active Workspace**: Added a guide for the `consciousness/context_container/` transient area.
- **Consciousness Data Workspace**: Implemented `consciousness/data/` for transient runtime assets (Uploads, Outputs, Processing) with strict "must know" transience constraints.
- **Tooling Upgrades**: Enhanced `ris_subagent.py` to support v9.6.2 registry schema and corrected MSP manifest paths.

### Changed

- **Documentation Hub Index**: Updated the Master Index (`docs/00_Governance/INDEX.md`) with a comprehensive reading order and links to all primary system protocols.
- **Global Identity Alignment**: Synchronized `CLAUDE.md`, root READMEs, and API descriptions to reflect the final Cognitive Flow 2.0 and v9.6.2 standards.

## [v9.6.2-CognitiveFlow2.0] - 2026-01-18

### Added

- **Storage ERD**: Renamed `v9.4.3_SYSTEM_STORAGE_ERD.md` to `EVA_System_Storage_ERD.md` and updated for v9.6.2 (Context Container, Active/History Slots, CIM Injection).
- **Stimulus Protocol**: Restored and upgraded `STIMULUS_CHUNKING_PROTOCOL.md` to **v2.0**, aligning with LLM-driven generation in Cognitive Flow 2.0.
- **Verification Tools**: Created `scripts/check_doc_alignment.py` for automated version verification across the Documentation Hub.

### Changed

- **Architecture Documentation (SSOT)**:
  - Upgraded `EVA_System_Architecture.md` to **v9.6.2**.
  - Merged "Logical Execution Pipeline" from Audit View into Section 7.
  - Consolidated all conflicting architecture files into a single SSOT.
- **Cognitive Flow Protocol**:
  - Established **Cognitive Flow 2.0** as the Master Protocol.
  - Defined **"Single-Inference Sequentiality"** rule (Pause-Resume Pattern).
  - Clarified CIM's role as **"File Injector"** (Container Hydration) vs Text Assembler.
  - Corrected Diagram Logic: Explicitly assigned `Stimulus` generation to **LLM**, removing it from SLM/Perception layer.
- **Documentation Hub**:
  - Upgraded `README.md` and `INDEX.md` to **v9.6.2**.
  - Updated `RULES_ALIGNMENT_AUDIT.md` to **v9.6.2**.
- **Registry**:
  - Registered `Cognitive_Flow_2_0`, `Memory_Philosophy_888`, and `Memory_Interface_Protocol` as formal Master Protocols.
  - Linked documentation for `CIM` (06_Orchestration) and `NexusMind`.
  - Registered `NexusMind` as a Central Module and integrated it into the **Boot Flow** (Step 6: Reasoning & Knowledge).
  - **Enhanced root_slots** with `logical_type` classification (organ, infra, memory, knowledge, governance).
- **Directory Structure Optimization** (Multi-Model Consensus):
  - **Phase 1 (Root Cleanup)**: Moved 7 loose files from root to appropriate locations:
  - **[PHASE 45] SE Refactor**: "PMT" (Prompt Moral Triage) renamed to **"PRN" (Prompt Rule Node)** across all filenames, code, and contracts.
  - **[PHASE 45] Logic Fix**: Fixed `comp_map` bug in Orchestrator resonance report.
  - **[PHASE 44] PRN Cleanup**: Centralized contracts to `agent/contracts/` and moved legacy code to `docs/99_Archive/`.
  - **[PHASE 43] Asset Classification**: `prompt_rule/configs/` renamed to `assets/`.
  - **Phase 2 (Registry Enhancement)**: Added semantic `type` field to all root_slots for logical organization without physical restructuring.
  - **Phase 3 (Enforcement)**: Created `.agent/governance/root_policy.yaml` whitelist to prevent future root pollution.
  - **Result**: Root directory reduced to 5 essential files. Flat anatomy preserved per Embodied Organism philosophy.

## [9.6.0-ResonanceRefined] - 2026-01-18

### Added

- **Registry as SSOT**: Elevated `eva_master_registry.yaml` to be the absolute Source of Truth for all versions, permissions, and runtime sequences.
- **Runtime Execution Graph**: Added `execution_graph` to the Registry to autogenerate boot sequences.
- **Criticality Levels**: Defined L0-L3 criticality for all systems to manage failure tolerance.
- **Phase 3 Protocol**: Formalized `Phase_3_Loopback` (The Sponge) as a `cognitive_loop` protocol in CIM.

### Changed

- **Architecture Diagram**: Updated `FULL_SYSTEM_ARCHITECTURE_v9.6.2.md` to strictly follow logic: Input -> Engram -> SLM -> Gap -> Output.
- **Version Control**: Enforced clear semantic versioning guidelines (Skipped v9.5.x as internal refactor).

## [9.4.3-ResonanceRefactored] - 2026-01-17

### Added

- **Resonance Bus Architecture**: Implemented a decentralized communication hub using a subscriber-based pattern.
  - **Decoupling**: Removed direct dependencies between `PhysioCore`, `EVAMatrix`, and `ArtifactQualia`.
  - **IResonanceBus**: Formally defined the interface for stable messaging across components.
  - **Passive Persistence**: MSP now functions as a "Subconscious Listener," automatically latching state snapshots from the bus.
  - **ADR-012**: Documented the "Resonance Bus State Decoupling" architecture.
- **SOLID Memory Delegation**: Refactored the MSP engine into a pure facade with specialized modules.
  - **Modules**: Created `EpisodicMemoryModule`, `SemanticMemoryModule`, and `SensoryMemoryModule`.
  - **Interfaces**: Implemented `IMemoryRetrieval` and `IMemoryStorage` contracts for all modules.
  - **Nodes**: Finalized `JournalNode`, `GroundingNode`, and `QualiaStorageNode` with robust logic and 100% type hinting.
  - **ADR-013**: Documented the "GSD Node Implementation Pattern".
- **GSD Implementation**: Enforced Goal-State Driven standards across new components, focusing on type safety and error resilience.
- **Technician Subagent**: Implemented `technician_subagent.py` for token-optimized, large-scale file modifications via `task_order.yaml`.
- **System Codification**: Formalized core laws into `.agent/rules/resonancestandard.md` and workflows into `.agent/workflows/`.

### Verified

- **Physio-Psych Coupling**: Completed functional audit of the `PhysioCore` <-> `EVAMatrix` link.
  - **Reactivity**: Confirmed that biological stimuli ('threat') correctly trigger hormonal spikes and subsequent psychological axis shifts (Stress/Stability).
  - **Feedback Loop**: Validated the autonomic resonance loop (Hormones -> BPM/RPM response).
  - **Homeostasis**: Verified state decay toward baseline for both biological and psychological state variables.

### Fixed

- **AutonomicResponseEngine**: Corrected config key from `weights` to `hormone_weights` to align with SSL (System Specification Law).
- **ReceptorUnit**: Resolved `max_density` vs `bmax` attribute collision, fixing a 100x signal amplification error.
- **FastReflexEngine**: Updated schema to use `inventory_pct` from `EndocrineGland` reports, restoring reflex functionality.
- **PhysioCore**: Fixed unit mismatch in Baseline Clamp logic (pg vs pg/mL) and resolved `core_vals` NameError in bus broadcast.

### Changed

- **Orchestrator Refine**: Simplified `Orchestrator._execute_the_gap` to act as a trigger, relying on the Resonance Bus for signal propagation.
- **Component Versioning**: Synchronized all file headers and documentation with the independent versioning system (e.g., PhysioCore v2.4.3, MSP v1.1.0).
- **Consolidated State**: Merged all "Locked" state files into the `consciousness/state_memory/` root for unified governance.

## [9.4.3-MemoryProtocolRefactor] - 2026-01-17

### Added

- **8-8-8 Memory Synthesis Protocol**: Implemented a tiered distillation architecture for long-term wisdom.
  - **Philosophy**: Redefined Consciousness as the Awareness Domain (Functional Buffer), while Session, Core, and Sphere represent the tiered distillation hierarchy.
  - **Session Memory Spec**: Refined the storage architecture to use a **"Snapshot + Digest Index"** pattern, ensuring full data integrity while optimizing RAG retrieval speed.
  - **Concept**: `docs/01_Philosophies/MEM_PHILOSOPHY_888.md`
  - **Spec**: `docs/04_Systems/memory_n_soul_passport/Session_Memory_Spec.md`
- **Documentation Master Index**: Created a unified entry point and reading order.
  - **Index**: `docs/00_Governance/INDEX.md`
- **ADR-010**: Documented the "8-8-8 Memory Protocol and Documentation Reorganization" decision.
- **Independent Component Versioning**: Implemented a decoupled versioning strategy to allow subsystems to evolve independently.
  - **Standard**: Applied a legacy-based mapping rule (8->1, 9->2) to preserve historical context while shifting away from global v9.x numbering.
  - **Artifacts**: Updated `core_systems.yaml`, all core system headers, and documentation headers.
  - **ADR-011**: Documented the "Independent Component Versioning Standard" decision.

### Changed

- **Documentation Reorganization**: Numbered all major documentation folders into a logical hierarchy (00_Governance → 09_Archive) to improve navigability and RAG performance.
  - **Governance**: Moved CHANGELOG, README, and INDEX to `docs/00_Governance/`.
  - **Philosophies**: Created `docs/01_Philosophies/` for core principles.
  - **Requirements**: Moved specs to `docs/02_Requirements/`.
  - **Architecture**: Consolidated all architectural diagrams and flows into `docs/03_Architecture/`.
- **Architecture Sync**: Updated `EVA_v9.4.3_Architecture.md` and `v9.4.3_SYSTEM_STORAGE_ERD.md` to align with the 8-8-8 nomenclature and the new "Snapshot + Digest" Session Memory model.
  - **Terminology Correction**: Refined the Agentic RAG model with a logical distinction: **"Hydrate"** for State (ERD) and **"Contextualize"** for Process (Flow).
- **Memory Governance & Belief Revision**:
  - Integrated **Memory Domains** (Safety, Identity, etc.) and **Epistemic States** into the 8-8-8 philosophy.
  - Implemented the **Belief Revision Protocol** (Sphere → Core downgrade logic).
  - Formalized specialized memory classes: **Habit** and **Somatic Imprint**.
  - New Policy: `docs/07_Protocols/MEMORY_GOVERNANCE_POLICY.md`.

## [9.4.3-ArchitectureConsolidation] - 2026-01-15

### Added

- **Trajectory System**: Implemented execution trace logger for capturing LLM reasoning, tool calls, and decision points.
  - **Engine**: `operation_system/trajectory/trajectory_manager.py`
  - **Config**: `operation_system/configs/trajectory_config.yaml`
  - **Concept**: `docs/systems/trajectory/Trajectory_Concept.md`
- **4-Layer Resonance Architecture**: Unified RTI, MRF, and APM into cohesive `ResonanceEngine`.
  - **Engine**: `operation_system/resonance_engine/resonance_engine.py`
  - **Config**: `operation_system/resonance_engine/configs/resonance_config.yaml`
  - **Concept**: `docs/systems/resonance_engine/Resonance_Engine_Concept.md`
- **MRF Engine**: Migrated Metacognitive Re-contextualization Framework to OS as Central Module.
  - **Location**: `operation_system/mrf_engine/`
  - **7-Layer Processor** for deep interpretation (Literal → Transcendental)
- **Umbrella Engine**: Created toggle-based safety layer with EMP (Exposure Management Protocol).
  - **Location**: `operation_system/umbrella/`
  - **Features**: State-based protection, graceful degradation, Prime Directive integration.
- **Verification Suite**: Created `tests/test_resonance_engine.py` and `tests/simulate_resonance_comparison.py` for automated and comparative validation.
- **ADR-005**: Formally documented the "Unified 4-Layer Resonance Architecture" decision.
- **Orchestrator V9.4**: Fully integrated the 4-Layer Resonance pipeline into the main processing loop.

### Changed

- **NexusMind**: Relocated from `genesis_knowledge_system/nexus_mind/` to `operation_system/nexus_mind/`
  - **Reason**: Functions as Thinking Mode Controller (Infrastructure), not just Knowledge
  - **Updated Role**: `central_module` (cognitive mode switcher)
- **APM (Archetypal Projection Module)**: Relocated from GKS to `operation_system/archetypal_projection/`
  - **Reason**: Cross-system usage as Central Module
  - **Updated Role**: `central_module` (independent, callable by multiple systems)
- **Architecture Cleanup**:
  - Disabled `TemporalEngine` (requires major refactor)
  - Removed APM and NexusMind from GKS `owned_modules`
  - All Central Modules now consolidated in `operation_system/`

### Updated

- **core_systems.yaml**: Registered Trajectory, Resonance Engine, MRF Engine, Umbrella Engine
- **permissions.yaml**: Added TrajectoryManager to System examples
- **EVA_9.4_Architecture.md**: Updated directory mappings for relocated modules

## [9.4.3-SystemRefactor] - 2026-01-15

### Added

- **Engram System (Conditional Memory)**: Implemented O(1) Scalable Lookup Cache to bypass heavy inference for frequent high-confidence interactions.
  - **Engine**: `capabilities/services/engram_system/engram_engine.py`
  - **Concept**: `docs/systems/memory/Engram_Concept.md`
- **Feature Integration Workflow**: Standardized protocol `integrate_feature.md` for adding new components with strict documentation and registration enforcement.
- **RIM Refactor**: Standardized Resonance Impact Model into `operation_system/rim/` with dedicated config separation.
- **Glossary Updates**: Added GKS and Engram definitions to `glossary.yaml`.
- **Truth Seeked Node**: Implemented `genesis_knowledge_system/grounding/truth_seeker_node.py` ("The Judge") to validate candidate facts against User Block, specifically detecting conflicts (e.g., Shrimp vs Allergy) using the "Grilled Shrimp" logic.
- **Session Manager Module**: Implemented `orchestrator/session_manager/session_manager.py` ("The Boss") to decouple lifecycle management (/start, /stop, timeout) from the main Orchestrator loop.

### Changed

- **Permissions & Registration**: Updated `core_systems.yaml` and `permissions.yaml` to include Engram and RIM, ensuring full architectural consistency.
- **Orchestrator Logic**: Refactored `orchestrator.py` to delegate session control to `SessionManager`, significantly cleaning up the main inference loop.
- **MSP Architecture**: Clarified `end_session` role as purely Storage/Archival, leveraging the new `SessionManager` to handle the validation business logic before/after storage.
- **Documentation**: Updated `EVA_9.4_Architecture.md` to reflect the new `Grounding` Node and `SessionManager` Module structure.

## [9.2.0-C8] - 2026-01-11

### Added

- **Phase 10: Pure Decay Metabolism**: Refactored `BloodEngine` for pure exponential decay (zero-decay) and `EndocrineGland` for Basal Secretion and Physiological Noise (+/- 10% Jitter).
- **Phase 11: Bidirectional Vitals (Vagus Feedback)**:
  - Created `VitalsEngine` (Backend HR/RR, RSA, Vagus Tone calculation).
  - Integrated bidirectional feedback in `PhysioCore`: Respiration (RPM) modulates **Vagus Tone**, which inhibits stress hormone (Adrenaline/Cortisol) production.
  - Heart Rate (BPM) now drives dynamic blood flow (Active Clearance).
- **Living Sandbox UI**:
  - `server.py` (FastAPI) implementation with 30Hz background physiological loop.
  - `run_sandbox_ui.bat` shortcut for ease of use.

## [9.1.0-Resonance] - 2026-01-10

### Added

- **SLM Bridge:** Implemented `Qwen3` (0.6b) as a Cognitive Gateway (Pre-Inference) for accurate Thai intent tagging.
- **Vector Memory:** Implemented `ChromaDB` (Local) with `sentence-transformers` (`multilingual-e5-base`) for robust multilingual semantic search.
- **Pre-Inference Flow:** Added "Cognitive Gateway" step in Orchestrator to inject Intent & Fast Memories before Phase 1 Perception.

### Changed

- **Identity Manager Implementation**: Centralized identity logic into `operation_system/identity_manager.py`.
- **Context ID:** Updated format to be human-readable sequence: `ctx_{session_seq}_{episodic_id}.md` (e.g., `ctx_5_EVA_EP27.md`).
- **Session ID:** Aligned with session memory logic: `SES_{dev_id}_SP{sphere}C{core}_SS{session}`.
- **Identity Logic:** Centralized all ID generation in `IdentityManager`.
- **Cleanup:** Removed legacy `transient_id` and deleted redundant `eva/identity` directory.
- **Architectural Pivot:** Moved from "3-Phase / Multi-Turn" to **"1-Inference / Single-Session"** architecture.
  - Reduced LLM calls from 3 to 1 per turn (plus 1 continuation).
  - Consolidated context injection into "Pre-Inference".
  - Refactored "The Gap" to be a synchronous function call within the same session.
- **Orchestrator:** Renamed processing stages to Step 1 (Perception/Pre-Infer), Step 2 (Gap), Step 3 (Reasoning/Post-Infer).
- **Gemini Bridge:** Implemented robust fallback mechanism for Function Responses (Text Injection Fallback) to resolve `IndexError`.

### Fixed

- **LLM Hang:** Resolved Orchestrator hanging at RAG step by fixing nonexistent method calls.
- **Protocol Mismatch:** Fixed Gemini SDK crash by handling empty candidates during function calling.

### Removed

- **Phase 3 Prediction:** Removed standalone Prediction Phase to simplify the cognitive loop.
- **Split Context Logs:** Stopped generating `context_phase2.json` and `context_phase3.json`; merged all reasoning data into Episodic Memory.
