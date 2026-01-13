# 🧠 Agentic RAG (Retrieval-Augmented Generation)
**Component ID:** `SYS-ARAG-8.2` | **Version:** `8.2.0` | **Role:** Memory Retrieval Service

> [!NOTE]
> **Resonance Bus Integration:** This module subscribes to `bus:operational` for retrieval requests and publishes memory matches back to `bus:operational`.

## 📋 Overview
The **Agentic RAG** module is EVA 8.2.0's advanced memory retrieval service. It specializes in **7-dimensional affective memory retrieval** across various memory streams, with a critical focus on physio-congruent recall. Unlike traditional RAG systems, Agentic RAG prioritizes memories that emotionally and physiologically align with EVA's current internal state.

It acts as the system's "Hippocampus Retrieval," actively searching for relevant past experiences and knowledge to enrich the LLM's cognitive process during Phase 2 of the Orchestration.

## ⚙️ Core Functions
1.  **Hept-Stream Retrieval**: Performs vector searches across 7 specialized memory streams (Emotion, Narrative, Salience, Sensory, Temporal, Intuition, Reflection).
2.  **Affective Matching**: Utilizes physiological state (ANS, hormones) to find emotionally congruent memories.
3.  **Temporal Decay**: Applies exponential temporal decay to prioritize recent and relevant memories.
4.  **Context Enrichment**: Provides retrieved memory matches to the CIN for deep context injection into the LLM prompt.

## 🔗 Hept-Stream Breakdown
Agentic RAG queries the following distinct memory streams:

| Stream        | Method                               | Purpose                                     | Criticality |
| :------------ | :----------------------------------- | :------------------------------------------ | :---------- |
| **Emotion**   | Physio-congruent matching (ANS + hormones) | Heart of embodied memory - felt-sense matching. | **CRITICAL**|
| **Narrative** | Sequential episode chains (links)    | Storyline continuity.                       | High        |
| **Salience**  | High RI (Resonance Intelligence) score ranking | High-impact event retrieval.                | Medium      |
| **Sensory**   | Qualia texture matching (5D vectors) | Experiential texture matching.              | Medium      |
| **Temporal**  | Exponential decay (30d half-life)    | Recency and chronological flow.             | Medium      |
| **Intuition** | Semantic graph pattern recognition   | Concept relationship matching.              | Low         |
| **Reflection**| Meta-cognitive pattern matching      | Self-awareness and past insights.           | Low         |

## 🗂️ Directory Structure (8.2.0 Standard)
```
agentic_rag/
├── configs/                 # [SSOT] Master Configuration
│   ├── Agentic_RAG_Interface.yaml # Bus bindings
│   └── Agentic_RAG_configs.yaml   # Runtime logic & Stream weights
│
├── contract/                # [API] Locked Interfaces
│   └── Agentic_RAG_Payload_Contract.yaml
│
├── schema/                  # [DATA] Strict Validation
│   └── Agentic_RAG_Payload_Schema_v2.json
│
├── docs/                    # [DOCS] Conceptual & Technical Documentation
│   └── Agentic_RAG_CONCEPT.md
│
├── tests/                   # [TESTS] Unit and integration tests
│
└── agentic_rag_engine.py    # [ENGINE] Main retrieval engine
```

## 🛠️ Usage
Agentic RAG is primarily called by the **CIN** during Phase 2 of the orchestration.

```python
from agentic_rag.agentic_rag_engine import AgenticRAG

# Initialize Agentic RAG (requires MSP client)
rag = AgenticRAG(msp_client=my_msp_client_instance)

# Perform a retrieval based on current context
query_context = {
    "tags": ["stress", "deadline"],
    "ans_state": {"sympathetic": 0.75, "parasympathetic": 0.25},
    "blood_levels": {"cortisol": 0.8, "adrenaline": 0.6},
    "context_id": "ctx_..."
}
memory_matches = rag.retrieve(query_context)

for match in memory_matches:
    print(f"Stream: {match.stream_source}, Content: {match.content}, Score: {match.score}")
```

---

## 📚 Documentation
- **Technical Specifications**: Refer to `configs/Agentic_RAG_configs.yaml` for detailed stream weights and infrastructure settings.
- **Conceptual Overview**: See `docs/Agentic_RAG_CONCEPT.md` for a deeper dive into the affective retrieval principles.

---

**Last Updated**: 2026-01-05 | **Status**: Production Ready ✅
