# Graph Bridge (Knowledge Connection)

**Directory**: `capabilities/services/graph_bridge/`  
**Purpose**: Knowledge Graph integration (Neo4j) for Bio-Resonance and Trauma recall.  
**Version**: v9.6.2 (Cognitive Flow 2.0 Ready)

---

## 📋 Overview

The **Graph Bridge** is the "Relational Engine" of EVA's memory. While the Vector Bridge finds *similarity in content*, the Graph Bridge finds *similarity in experience*. It uses **Neo4j** to map episodes to biological states, psychological qualia, and foundational concepts (GKS).

---

## ⚙️ Core Functions

1. **Bio-Resonance Retrieval**: Finds memories where EVA had similar physiological profiles (e.g., "Find episodes where I felt this stressed").
2. **Trauma Recall**: Identifies high-impact or traumatic episodes that require immediate safety gating or defensive posturing.
3. **Knowledge Grounding**: Links episodic experiences to static Genesis Blocks in the Knowledge System.
4. **Affective Context**: Provides the "Affective" layer for Hybrid RAG.

---

## 📂 Structure

- **`graph_rag_engine.py`**: The main logic for hybrid search (Vector + Graph).
- **`graph_client.py`**: Low-level Neo4j driver and Cypher query builder.

---

## ⚖️ Governance

- **Memory Domain**: The Graph acts as the "Social & Emotional Ledger" of the organism.
- **Provider Standard**: Requires a local **Neo4j** instance (default: `bolt://localhost:7687`).

---

*Connecting the dots of existence.*
