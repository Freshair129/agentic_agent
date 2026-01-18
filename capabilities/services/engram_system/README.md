# Engram System (Conditional Memory)

**Directory**: `capabilities/services/engram_system/`  
**Purpose**: Deterministic, O(1) matching for frequent interaction patterns.  
**Version**: v9.6.2 (Experimental / Rapid)

---

## 📋 Overview

The **Engram System** is a memory optimization layer inspired by the "Conditional Memory" concept. It provides a hash-based lookup for exact text matches, allowing EVA to bypass expensive Vector RAG or LLM reasoning for high-confidence, recurring interactions.

---

## ⚙️ Core Functions

1. **O(1) Lookup**: Rapidly identifies if a current input has a "perfect" or high-confidence match in the engram store.
2. **Conditional Memorization**: Automatically stores interactions that have an extremely high confidence score (threshold-governed), effectively "burning" them into structural memory.
3. **Pattern Recognition**: Helps in identifying conversational shortcuts and routine reflexes.

---

## 📂 Structure

- **`engram_engine.py`**: The core logic using deterministic SHA-256 hashing.
- **`configs/`**: Threhsold settings and storage paths.
- **`data/`**: JSON storage for the engram table (key: hash, value: response/metadata).

---

## 📐 Governance

- **System 1 Logic**: Engram is the first memory layer checked during the **CNS Pre-Processing** phase.
- **Confidence Lock**: Memories are only stored in the Engram if the cognitive confidence score exceeds `0.95`.

---

*Memory without the math.*
