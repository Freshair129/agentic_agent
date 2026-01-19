# 🗃️ AuthDoc: Archivist Subagent

> **Status**: DRAFT (v9.6.2 Backfill)
> **Governs**: `capabilities/tools/subagents/archivist_subagent.py`

## 1. Overview
The Archivist is a specialized subagent responsible for system maintenance, memory synchronization, and ensuring that the physical file structure remains aligned with the [Master Registry](file:///e:/The%20Human%20Algorithm/T2/agent/registry/eva_master_registry.yaml).

## 2. Core Responsibilities
- **Log Rotation**: Manages `.jsonl` files in `consciousness/` and `memory/` archives.
- **Rule Synchronization**: Updates local system rules based on global governance updates.
- **Health Checks**: Validates schema integrity for Episodic and Semantic memory buffers.

## 3. Code Mapping
- `subagents/archivist_subagent.py`: Principal agent logic.
