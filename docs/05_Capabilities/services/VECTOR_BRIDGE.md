# 🗄️ AuthDoc: Vector Bridge Service

> **Status**: DRAFT (v9.6.2 Backfill)
> **Governs**: `capabilities/services/vector_bridge/`

## 1. Overview
The Vector Bridge is the storage abstraction for high-dimensional embedding data. It manages the connection to ChromaDB and handles the persistence of memory vectors.

## 2. Core Responsibilities
- **Embedding Generation**: Interface for `sentence-transformers` to convert text → vector.
- **Vector Search**: Performs cosine similarity search for the [Agentic RAG](file:///e:/The%20Human%20Algorithm/T2/agent/docs/05_Capabilities/services/agentic_rag/Agentic_RAG_CONCEPT.md) system.
- **Collection Management**: Handles namespacing for Episodic, Semantic, and Sensory streams.

## 3. Code Mapping
- `vector_bridge/chroma_client.py`: Wrapper for local ChromaDB instance.
- `vector_bridge/embedding_engine.py`: High-performance embedding service.
