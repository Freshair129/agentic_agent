# Vector Bridge (Semantic Memory)

**Directory**: `capabilities/services/vector_bridge/`  
**Purpose**: Local vector storage and semantic retrieval interface.  
**Version**: v9.6.2 (Cognitive Flow 2.0)

---

## 📋 Overview

The **Vector Bridge** provides the interface between EVA and her high-dimensional semantic memory. It utilizes **ChromaDB** for local storage and the **multilingual-e5-base** model to handle embeddings, ensuring excellent support for the Thai language.

---

## ⚙️ Core Functions

1. **Local Embedding Generation**: Uses `sentence-transformers` to generate 768-dimensional vectors offline.
2. **Semantic Search**: Performs "Cosine Similarity" search to find conceptually related memories based on user queries.
3. **Metadata Grounding**: Stores and retrieves JSON metadata alongside documents to provide context (Episode ID, Timestamp, Sentiment).

---

## 📂 Structure

- **`chroma_bridge.py`**: The primary implementation using ChromaDB's persistent client.
- **`__pycache__`**: Compiled Python bytecode.

---

## 📐 Governance

- **Model Standard**: Authorized to use `intfloat/multilingual-e5-base` to ensure cross-lingual resonance.
- **Persistence**: Storage is directed to `memory/vector_store/` (The Subconscious Domain).

---

*Connecting concepts through high-dimensional space.*
