# EVA Capabilities

**Directory**: `capabilities/`  
**Purpose**: Skill, Tool, and Service implementation domain.  
**Version**: v9.6.2 (Cognitive Flow 2.0)

---

## 📋 Overview

The **Capabilities Domain** contains the implementation of all external-facing functions, internal utility services, and agentic tools. It is partitioned into three primary categories to maintain separation of concerns.

---

## 📂 Categories

### 1. [Services](file:///e:/The%20Human%20Algorithm/T2/agent/capabilities/services/)

Long-running or complex infrastructure-level services.

- **`agentic_rag`**: Intelligent retrieval and memory hydration.
- **`slm_bridge`**: Interface for the Cognitive Gateway (Llama-3.2-1B).
- **`vector_bridge`**: Vector database integration.

### 2. [Tools](file:///e:/The%20Human%20Algorithm/T2/agent/capabilities/tools/)

Atomic, functional units accessible by the LLM via `tool_use`.

- **`sync_biocognitive_state`**: Mandatory Phase 1 tool for Bio-Sync.
- **`propose_episodic_memory`**: Mandatory Phase 2 tool for persistence.
- **`logger`**: Standardized system logging.

### 3. [Skills](file:///e:/The%20Human%20Algorithm/T2/agent/capabilities/skills/)

Complex, multi-step behaviors or specialized logic (e.g., Code Analysis, Research).

---

## 📐 Implementation Protocol

All capabilities must adhere to the **Resonance Standard**:

1. **Type Hinting**: 100% type safety.
2. **Configuration**: parameters stored in `configs/*.yaml`.
3. **Registration**: Must be registered in `registry/eva_master_registry.yaml` if they are system-level.

---

## 🔗 Governance

> **Interface vs Implementation**:  
> The `consciousness/` domain contains the interfaces/shortcuts to these capabilities. The `capabilities/` directory is hidden from the LLM's direct file-system awareness by default to ensure organism integrity.

---

*EVA v9.6.2 Capability Architecture*
