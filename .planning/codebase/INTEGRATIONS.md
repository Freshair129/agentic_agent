# External Integrations

**Analysis Date:** 2026-01-18

## APIs & External Services

**LLM Provider:**
- Google Gemini AI - Primary LLM for Cognitive Flow
  - SDK/Client: `google-generativeai`
  - Model: `gemini-2.0-flash-lite-preview-02-05`
  - Auth: `GOOGLE_API_KEY` (env var)
  - Implementation: `operation_system/llm_bridge/llm_bridge.py`
  - Features: Function calling, conversation history, safety settings

## Data Storage

**Databases:**
- ChromaDB (Vector Database)
  - Connection: Local persistent storage
  - Client: `chromadb.PersistentClient`
  - Path: Configured in bridge
  - Usage: Semantic memory, episodic retrieval
  - Implementation: `capabilities/services/vector_bridge/chroma_bridge.py`

**File Storage:**
- Local filesystem only
  - Consciousness state: `consciousness/` (runtime RAM)
  - Long-term memory: `memory/` (MSP-governed)
  - Context storage: `consciousness/context_storage/`
  - Indexes: `consciousness/indexes/memory_index.json`

**Caching:**
- Engram System - Fast memory lookup (O(1) hash-based)
  - Location: `capabilities/services/engram_system/`
  - Purpose: DeepSeek-inspired conditional memory cache
  - Storage: Local

## Authentication & Identity

**Auth Provider:**
- Custom (No external auth detected)
  - Implementation: IdentityManager system
  - Boot sequence: Position 1 (Security First)
  - Registry: `registry/eva_master_registry.yaml`

## Monitoring & Observability

**Error Tracking:**
- None (no external service detected)

**Logs:**
- Console-based structured logging
  - Format: `[MODULE] [LEVEL] Message`
  - Custom logger: `capabilities/tools/logger.py`
  - Examples: `[PhysioCore] [INFO] Dopamine: 0.75`

## CI/CD & Deployment

**Hosting:**
- Not configured (local development only)

**CI Pipeline:**
- None detected
  - No `.github/workflows/` found
  - No CI config files

## Environment Configuration

**Required env vars:**
- `GOOGLE_API_KEY` - Gemini AI access (critical)

**Optional env vars:**
- Additional LLM keys (Ollama, Claude) may be supported in llm_bridge

**Secrets location:**
- `.env` file in project root (not committed)

## Webhooks & Callbacks

**Incoming:**
- None detected

**Outgoing:**
- None detected

## Internal Event Bus

**Resonance Bus:**
- Internal pub/sub messaging system
- Not an external integration, but critical for module communication
- Channels: `BUS_PHYSICAL`, `BUS_PSYCHOLOGICAL`, etc.
- Implementation: `operation_system/resonance_engine/`

---

*Integration audit: 2026-01-18*
