# Codebase Concerns

**Analysis Date:** 2026-01-18

## Tech Debt

**CIM (Context Injection Manager):**
- Issue: Monolithic file (2698 lines) - largest in codebase
- Files: `orchestrator/cim/cim.py`
- Impact: Difficult to maintain, test, and reason about
- Fix approach: Modularize into sub-components (context assembly, file injection, hydration)
- ADR Note: ADR-008 mentions "MSP logic becomes complex (3000+ lines), requiring future internal modularization" - same issue here

**MSP Engine:**
- Issue: Monolithic engine (2453 lines)
- Files: `memory_n_soul_passport/memory_n_soul_passport_engine.py`
- Impact: Hard to modify memory types without touching massive file
- Fix approach: Split into memory type handlers (Episodic, Semantic, Sensory, State)
- Note: Already documented in ADR-008 as "requiring future internal modularization"

**Archive Directories:**
- Issue: Multiple `/archive/` directories with deprecated code
- Files: `artifact_qualia/archive/`, `orchestrator/archive/`, `memory_n_soul_passport/archive/`, etc.
- Impact: Confusing for new developers, bloats codebase
- Fix approach: Move to single `/archive/` root directory or remove entirely

**3-Phase Backup File:**
- Issue: Old architecture backup file (729 lines) still in codebase
- Files: `orchestrator/orchestrator_3phase_backup.py`
- Impact: Confusion about which is current (v9.6.2 uses Cognitive Flow 2.0)
- Fix approach: Move to `/archive/` or delete (git history preserves it)

## Known Bugs

**Placeholder Tests:**
- Symptoms: Tests pass even when initialization fails
- Files: All `{module}/tests/test_{module}_init.py`
- Trigger: Run any module test without proper dependencies
- Workaround: Tests use `pass` in except blocks to avoid failing
- Fix: Implement proper mocking and remove error tolerance

## Incomplete Features

**Graph RAG Integration:**
- Issue: Graph RAG not fully integrated with vector store
- Files: `capabilities/services/graph_bridge/graph_rag_engine.py:24,128`
- TODO: "Integrate actual ChromaVectorBridge here"
- Impact: Hybrid search (graph + vector) not functional
- Fix: Complete ChromaDB integration

**MRF Engine (Meta-Resonance Framework):**
- Issue: Multiple unimplemented TODO features
- Files: `operation_system/mrf_engine/mrf_engine.py:129,137,165,173,181`
- Missing:
  - Literal parsing (line 129)
  - Emotion detection (line 137)
  - Relational analysis (line 165)
  - Narrative positioning (line 173)
  - Paradox detection (line 181)
- Impact: MRF not fully operational (stub implementation)
- Fix: Implement each TODO based on MRF specification

**Resonance Engine Integration:**
- Issue: Not integrated with MSP and ArtifactQualia
- Files: `operation_system/resonance_engine/resonance_engine.py:160,161`
- Missing:
  - MSP memory recall integration
  - ArtifactQualia phenomenology integration
- Impact: Resonance scoring incomplete
- Fix: Wire up MSP query and Qualia retrieval

**Session Manager Analysis:**
- Issue: LLM analysis generation not connected
- Files: `orchestrator/session_manager/session_manager.py:129,136`
- Missing: `_generate_analysis()` LLM call
- Impact: Session digests lack LLM-generated insights
- Fix: Connect to LLMBridge

**GKS Deep Search:**
- Issue: Deep search not implemented
- Files: `genesis_knowledge_system/gks_loader.py:78`
- Impact: Limited knowledge retrieval capabilities
- Fix: Implement semantic search in GKS blocks

## Security Considerations

**API Key Storage:**
- Risk: `.env` file contains sensitive keys
- Files: `.env` (not committed, but risk if accidentally committed)
- Current mitigation: `.gitignore` prevents commit
- Recommendations: Use secret management service (AWS Secrets Manager, etc.)

**Safety Settings Disabled:**
- Risk: Gemini safety filters set to BLOCK_NONE
- Files: `operation_system/llm_bridge/llm_bridge.py:51-56`
- Current mitigation: Intentional for chatbot flexibility
- Recommendations: Re-enable for production, use custom content filtering

**No Input Validation:**
- Risk: No validation on external API inputs
- Files: `api/chat_endpoint.py` (if exists)
- Current mitigation: Pydantic schemas (partial)
- Recommendations: Add input sanitization and rate limiting

## Performance Bottlenecks

**PhysioCore 30Hz Loop:**
- Problem: 30Hz update cycle could be CPU-intensive
- Files: `physio_core/physio_core.py`, `physio_core/logic/blood/BloodEngine.py`
- Cause: Continuous hormone simulation
- Note: Marked as "Performance Critical" in ADR-015 (Verified Stable)
- Improvement path: Already optimized - further optimization requires profiling

**MSP Memory Writes:**
- Problem: 2453-line engine handles all memory types
- Files: `memory_n_soul_passport/memory_n_soul_passport_engine.py`
- Cause: Monolithic design
- Improvement path: Split into handlers, consider async writes

**ChromaDB Queries:**
- Problem: Vector similarity search can be slow on large datasets
- Files: `capabilities/services/vector_bridge/chroma_bridge.py`
- Cause: In-memory vector comparisons
- Improvement path: Index optimization, limit query scope

## Fragile Areas

**Cognitive Flow State Machine:**
- Files: `orchestrator/orchestrator.py` (930 lines)
- Why fragile: Complex state management for Cognitive Flow 2.0
- Safe modification: Follow ADR-004 (one-inference architecture)
- Test coverage: Minimal (only init test)

**Module Boot Sequence:**
- Files: `registry/eva_master_registry.yaml` runtime_sequence
- Why fragile: Strict 9-stage boot order, dependencies must load in sequence
- Safe modification: Never change boot order without full system test
- Test coverage: None detected

**Context Container Files:**
- Files: `consciousness/context_container/*`
- Why fragile: Files injected/read by CIM and LLM - schema must match
- Safe modification: Update schema definitions before changing files
- Test coverage: None detected

## Scaling Limits

**Single LLM Session:**
- Current capacity: Cognitive Flow 2.0 uses one continuous session
- Limit: Context window size (Gemini 2.0 Flash limit)
- Scaling path: Implement context summarization or session splitting

**Local File Storage:**
- Current capacity: All memory stored locally (consciousness/, memory/)
- Limit: Disk space on single machine
- Scaling path: Cloud storage (S3), database (PostgreSQL for structured memory)

**No Horizontal Scaling:**
- Current capacity: Single-instance only
- Limit: One user at a time
- Scaling path: Multi-instance with session management, load balancer

## Dependencies at Risk

**Google Gemini API:**
- Risk: Single LLM provider dependency
- Impact: System non-functional if Gemini unavailable
- Migration plan: LLMBridge supports multiple providers (Ollama, Claude) - implement fallback

**ChromaDB:**
- Risk: Embedded database, no cloud sync
- Impact: Data loss if local storage fails
- Migration plan: Support for cloud vector DBs (Pinecone, Weaviate)

## Missing Critical Features

**No CI/CD:**
- Problem: No automated testing or deployment
- Blocks: Reliable production releases
- Fix: Set up GitHub Actions for test automation

**No Monitoring:**
- Problem: No error tracking, no performance monitoring
- Blocks: Production troubleshooting
- Fix: Add Sentry (errors), Prometheus (metrics)

**No Multi-User Support:**
- Problem: System designed for single user
- Blocks: Production deployment
- Fix: Add user session management, separate memory spaces

**No Rate Limiting:**
- Problem: API can be overwhelmed
- Blocks: Production stability
- Fix: Add rate limiting middleware

## Test Coverage Gaps

**Integration Tests:**
- What's not tested: Full Cognitive Flow 2.0 end-to-end
- Files: All modules (only unit tests exist)
- Risk: Cognitive Flow state transitions could break unnoticed
- Priority: High

**Memory Persistence:**
- What's not tested: MSP write/read cycles
- Files: `memory_n_soul_passport/memory_n_soul_passport_engine.py`
- Risk: Data corruption or loss
- Priority: High

**Hormone Simulation:**
- What's not tested: PhysioCore state transitions over time
- Files: `physio_core/physio_core.py`
- Risk: Incorrect emotional modeling
- Priority: Medium

**Context Injection:**
- What's not tested: CIM file injection and LLM reading
- Files: `orchestrator/cim/cim.py`
- Risk: Context loading failures
- Priority: High

---

*Concerns audit: 2026-01-18*
