# Changelog

All notable changes to the EVA Core project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [9.4.0-Refactor] - 2026-01-13

### Added

- **System -> Module -> Node Hierarchy**: Formally established the standard directory and logic structure across all systems.
- **Central Module & Sub-System Classification**: Defined new architectural layers for OS-direct modules and specialized internal sub-systems with restricted bus permissions.
- **Read-Only State Access**: Implemented "Owner-Only" communication protocol for Sub-Systems to bypass bottlenecks while maintaining structural integrity.
- **Doc-to-Code Workflow**: established `/doc_to_code` protocol where documentation and configuration MUST precede implementation.
- **Archivist Workflow**: Added `/run_archivist` for synchronizing Agent context with Source of Truth.
- **Checkpoint Workflow**: Added `/checkpoint` for automated doc-sync and git commitment.

### Changed

- **Memory Architecture (Facade Pattern)**: Refactored the monolithic `MSP` class into a facade that delegates responsibilities to specialized `Episodic`, `Semantic`, and `Sensory` memory modules.
- **Config-Driven Development**: Eliminated hardcoded values throughout the MSP system by resolving all module/node parameters from `MSP_configs.yaml`.
- **Documentation Hub (SSOT)**: Centralized all scattered documentation from module-local folders into a unified `agent/docs/` hierarchy.
- **GKS Independence**: Decoupled GKS (The Knowledge Backbone) from MSP storage to allow for modular/tier-based (Paid/Free)知识库 plugins.
- **EVA_Matrix & Artifact_Qualia**: Refactored to delegate logic to `MatrixPsychModule` and `QualiaIntegratorModule` respectively.
- **PhysioCore Exemption**: Officially exempted PhysioCore from strict Module/Node refactoring due to its unique biological density, while maintaining its System Authority status.

### Fixed

- **Architectural Drift**: Unified `core_systems.yaml` and `permissions.yaml` as the canonical Source of Truth for system registration and authority.

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

## [9.1.0-C3] - 2026-01-10

### Changed

- **Identity Manager Implementation**: Centralized identity logic into `operation_system/identity_manager.py`.
- **Context ID:** Updated format to be human-readable sequence: `ctx_{session_seq}_{episodic_id}.md` (e.g., `ctx_5_EVA_EP27.md`).
- **Session ID:** Aligned with session memory logic: `SES_{dev_id}_SP{sphere}C{core}_SS{session}`.
- **Identity Logic:** Centralized all ID generation in `IdentityManager`.
- **Cleanup:** Removed legacy `transient_id` and deleted redundant `eva/identity` directory.

## [9.1.0-C2] - 2026-01-10

### Added

- **SLM Bridge:** Implemented `Qwen3` (0.6b) as a Cognitive Gateway (Pre-Inference) for accurate Thai intent tagging.
- **Vector Memory:** Implemented `ChromaDB` (Local) with `sentence-transformers` (`multilingual-e5-base`) for robust multilingual semantic search.
- **Pre-Inference Flow:** Added "Cognitive Gateway" step in Orchestrator to inject Intent & Fast Memories before Phase 1 Perception.

## [9.1.0-Resonance] - 2026-01-10

### Changed

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
