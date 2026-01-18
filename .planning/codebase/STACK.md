# Technology Stack

**Analysis Date:** 2026-01-18

## Languages

**Primary:**
- Python 3.13.7 - All core systems and modules

**Secondary:**
- YAML - Configuration and contracts
- JSON - Data schemas and runtime state
- Markdown - Documentation

## Runtime

**Environment:**
- Python 3.13.7

**Package Manager:**
- pip (Python package installer)
- Lockfile: No requirements.txt in root (module-specific in `api/requirements.txt`)

## Frameworks

**Core:**
- FastAPI - Web API framework (`api/` layer)
- Uvicorn - ASGI server
- Pydantic - Data validation and schemas

**AI/LLM:**
- Google Generative AI SDK - Gemini integration (`operation_system/llm_bridge/`)
- Function calling support for Cognitive Flow 2.0

**Vector/Memory:**
- ChromaDB - Vector database for semantic memory (`capabilities/services/vector_bridge/`)

**Build/Dev:**
- python-dotenv - Environment variable management
- No formal build tool (interpreted Python)

## Key Dependencies

**Critical:**
- `fastapi` - Core API framework for web endpoints
- `google-generativeai` - LLM integration (Gemini 2.0 Flash)
- `chromadb` - Persistent vector storage for episodic/semantic memory
- `pydantic` - Schema validation (critical for contracts between modules)
- `uvicorn` - ASGI server for FastAPI

**Infrastructure:**
- `websockets` - Real-time communication (if used)
- `python-dotenv` - Env var loading for API keys

## Configuration

**Environment:**
- `.env` file for API keys (GOOGLE_API_KEY required)
- YAML-based module configurations (`{module}/configs/`)
- Master registry: `registry/eva_master_registry.yaml` (v9.6.2 SSOT)

**Build:**
- No build configuration (Python interpreted)
- Module-specific configs in `{module}/configs/*.yaml`

## Platform Requirements

**Development:**
- Python 3.13+
- Google Gemini API key
- ChromaDB storage directory

**Production:**
- Same as development
- No containerization detected (no Dockerfile found)
- Deployment target: Not specified

## Architecture Versioning

**System Version:** 9.6.2 (Cognitive Flow 2.0)
**Module Versions:**
- PhysioCore: v2.4.3 (Verified Stable)
- EVA_Matrix: v2.0.0
- GKS: v2.0.0
- IdentityManager: v2.4.0

---

*Stack analysis: 2026-01-18*
