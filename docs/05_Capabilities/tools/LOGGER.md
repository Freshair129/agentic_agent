# 📝 AuthDoc: Logger Utility

> **Status**: DRAFT (v9.6.2 Backfill)
> **Governs**: `capabilities/tools/logger.py`

## 1. Overview
The Logger utility provides a standardized, thread-safe interface for printing and recording system events. It ensures that logs from parallel systems (e.g., PhysioCore's 30Hz loop vs. Orchestrator) do not interleave.

## 2. Core Responsibilities
- **Safe Printing**: Replaces standard `print()` with `safe_print()` to prevent stream corruption.
- **Log Formatting**: Applies consistent timestamps and system tags to all outputs.
- **Stream Redirection**: Handles redirection of stdout/stderr for subagent execution logs.

## 3. Code Mapping
- `tools/logger.py`: Principal logging implementation.
