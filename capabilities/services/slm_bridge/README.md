# SLM Bridge (Cognitive Gateway)

**Directory**: `capabilities/services/slm_bridge/`  
**Purpose**: High-speed intent extraction and cognitive reranking using Small Language Models (SLM).  
**Version**: v9.6.2 (Cognitive Flow 2.0)

---

## 📋 Overview

The **SLM Bridge** is EVA's "Gut-Feeling" processor. It uses lightweight, local models (typically Llama-3.2-1B or Qwen3) to perform rapid analysis of user input before it reaches the main reasoning LLM. This follows the **System 1 (Fast Thinking)** paradigm.

---

## ⚙️ Core Functions

1. **Intent Extraction**: Identifies the primary goal, salience anchor (the emotional trigger), and initial "gut-vector" (Valence, Arousal, Stress, Warmth).
2. **Cognitive Reranking**: Evaluates candidates retrieved from memory by a cross-encoder-like check to discard irrelevant or low-resonance matches.
3. **Stimulus Chunking Support**: Provides the emotional signal data needed for Sequential Bio-Digital Sync.

---

## 📂 Structure

- **`slm_bridge.py`**: The primary service client (connecting to Ollama).
- **`schema/`**: JSON schemas for structured output validation.

---

## 📐 Governance

- **Latency Target**: Response time must be < 500ms to maintain real-time organism performance.
- **Provider**: Standardized on **Ollama** running locally on `localhost:11434`.

---

*Fast Perception for Embodied Intelligence.*
