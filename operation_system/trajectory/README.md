# Trajectory Manager

**Directory**: `operation_system/trajectory/`  
**Purpose**: Execution trace logging for debugging and decision analysis.  
**Version**: v9.4.3 (Core Infrastructure)

---

## 📋 Overview

The **Trajectory Manager** is EVA's "Black Box Recorder." It captures every significant event during a conversational turn, including LLM prompts/responses, tool calls, system errors, and internal decision points. This data is essential for auditing the organism's reasoning process and debugging complex multi-step flows.

---

## ⚙️ Core Functions

1. **Execution Tracing**: Logs the sequential steps of a turn (Start -> LLM -> Tool -> Result -> End).
2. **Decision Analysis**: Records why specific choices were made (Reasoning) and what alternatives were considered.
3. **Turn-Based Isolation**: Flushes data into individual `.jsonl` files per turn to prevent context bloat and ensure fast retrieval.
4. **Error Capture**: Provides detailed context for system failures within the execution path.

---

## 📂 Structure

- **`trajectory_manager.py`**: The core logging engine.
- **`__pycache__`**: Compiled Python bytecode.

---

## 📐 Governance

- **Output Standard**: Saves traces in JSONL (Line-delimited JSON) format for easy parsing and analysis.
- **Location**: Trajectories are written to the directory specified in `trajectory_config.yaml` (default: `operation_system/logs/trajectories/`).

---

*Recording the path of consciousness.*
