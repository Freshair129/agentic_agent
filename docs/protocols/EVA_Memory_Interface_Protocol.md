# Protocol: Memory System Interface (v9.4.3)

This protocol defines the strict architectural boundaries between the **Memory & Soul Passport (MSP)** core engine and its specialized functional modules (Episodic, Semantic, Sensory).

## 0. Overview

Adhering to the **SOLID** principle of Interface Segregation, the memory system is decoupled into three primary contracts:

1. **IMSPassport**: The external system facade.
2. **IMemoryRetrieval**: Specialized retrieval logic (Agentic RAG).
3. **IMemoryStorage**: Persistent write operations.

## 1. IMSPassport (System Facade)

Located at: `agent/contracts/systems/IMSPassport.py`

| Method | Role |
| :--- | :--- |
| `set_active_state` | Broadcasts live telemetry (Bio/Psyche) |
| `get_active_state` | Synchronous retrieval of last known snapshot |
| `latch_state` | Latches bus data for MSP retention |
| `log_episodic_event` | Single-entry point for lifecycle logging |
| `query_memories` | Generic query interface for high-level reasoning |

## 2. IMemoryRetrieval (Retrieval Module)

Located at: `agent/contracts/modules/IMemoryRetrieval.py`

| Method | Role |
| :--- | :--- |
| `retrieve_by_tags` | Semantic/Tag-based lookup |
| `retrieve_by_resonance` | Salience-driven recall (RI Filter) |
| `retrieve_by_state_similarity` | Embodied recall (Physio/Qualia match) |

## 3. IMemoryStorage (Persistence Module)

Located at: `agent/contracts/modules/IMemoryStorage.py`

| Method | Role |
| :--- | :--- |
| `store_episode` | JSON/JSONL persistence logic |
| `update_semantic_node` | Incremental knowledge reinforcement |
| `archive_session` | Session-to-Archive promotion (Irreversible) |

## 4. Implementation Law

- All new memory modules **MUST** implement the respective `I-Prefix` ABC.
- The `MSP` class must serve as a **Pure Facade**, delegating calls to implementations that satisfy these contracts.
