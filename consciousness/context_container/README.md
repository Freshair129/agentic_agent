# Context Container (Active Memory)

**Directory**: `consciousness/context_container/`  
**Purpose**: Transient workspace for active turn files (The "Thinking Space").  
**Version**: v9.6.2 (Cognitive Flow 2.0)

---

## 📋 Overview

The **Context Container** is EVA's "Short-Term Working Memory." It is a dynamic directory where the **Context Injection Manager (CIM)** hydrates specific files for each conversational turn. The LLM reads these files directly via function calls to maintain state without massive text prompt injection.

---

## 📂 Standard Files

1. **`task.md`**: The objective for the current turn.
2. **`instructions.md`**: Persistent system directives and behavioral constraints.
3. **`self_note_epXX.md`**: Evaluation and reflections from the *previous* turn.
4. **`user_profile.md`**: Active grounding facts about the user.
5. **`goal.md`**: The long-term conversational goal.
6. **`context_summary_epXX.md`**: A summary of the immediate history.

---

## ⚙️ Lifecycle

1. **Phase 1 (Pre-Inference)**: CIM clears the container and injects fresh files.
2. **Phase 2 (Inference)**: LLM reads files from this directory to inform its response.
3. **Phase 3 (Post-Inference)**: MSP archives the container's contents into episodic memory.

---

## 📐 Governance

- **Volatility**: This directory is **TRANSIENT**. It is cleared at the start of every new turn.
- **Access**: Only the **Orchestrator**, **CIM**, and **MSP** are authorized to write to this directory.

---

*The focused lens of awareness.*
