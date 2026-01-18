# LLM Bridge (Thinking Layer)

**Directory**: `operation_system/llm_bridge/`  
**Purpose**: Abstraction layer for LLM interactions and function calling.  
**Version**: v9.6.2 (Cognitive Flow 2.0)

---

## 📋 Overview

The **LLM Bridge** is the "Thinking Pipeline" of EVA. It abstracts the complexities of different LLM APIs (Ollama, Gemini, Claude) into a unified interface. It is the primary enforcer of the **Single-Inference Sequentiality** and the **Bio-Digital Gap** protocols.

---

## ⚙️ Core Functions

1. **Dual-Phase Inference**: Manages the transition from Perception (Phase 1) to Reasoning (Phase 2) within a single chat session.
2. **Unified Tool Interface**: Standardizes function calling mechanics (`sync_biocognitive_state`, `propose_episodic_memory`).
3. **Session Recovery**: Implements safety fallbacks for session corruption or "Malformed Function Call" errors to ensure conversational continuity.
4. **Clean Serialization**: Ensures complex system objects are safely serialized for LLM consumption.

---

## 📂 Structure

- **`llm_bridge.py`**: The primary Gemini/Google AI implementation.
- **`ollama_bridge.py`**: Local model support (Llama/Qwen) for air-gapped or testing modes.
- **`schema/`**: JSON schemas for function call validation.

---

## 📐 Governance

- **Protocol Enforcement**: Must implement Sequential Function Calling as defined in ADR-004.
- **Safety**: Disables default safety filters in `BLOCK_NONE` mode to allow for full simulate biological and psychological range.

---

*The architecture of thought.*
