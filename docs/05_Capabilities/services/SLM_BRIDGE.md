# 🌉 AuthDoc: SLM Bridge Service

> **Status**: DRAFT (v9.6.2 Backfill)
> **Governs**: `capabilities/services/slm_bridge/`

## 1. Overview
The SLM Bridge provides a standardized interface for Small Language Models (e.g., Llama-3.2-1B, Qwen). Its primary role in EVA 9.6.2 is **Phase 1 Perception Delegation**.

## 2. Core Responsibilities
- **Stimulus Normalization**: Converts raw input into a normalized `StimulusVector`.
- **Intent Extraction**: Rapid identification of user goal and emotional valence.
- **Salience Anchoring**: Highlighting the specific tokens that triggered the biological reaction.

## 3. Code Mapping
- `slm_bridge/qwen_bridge.py`: Specialized implementation for Qwen-based intent extraction.
- `slm_bridge/slm_interface.py`: Abstract base class for all SLM implementations.
