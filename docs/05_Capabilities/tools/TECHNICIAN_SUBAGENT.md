# 🛠️ AuthDoc: Technician Subagent

> **Status**: DRAFT (v9.6.2 Backfill)
> **Governs**: `capabilities/tools/subagents/technician_subagent.py`

## 1. Overview
The Technician is a high-autonomy subagent designed for mass code modification, refactoring, and feature integration. It follows the [Integrate Feature Protocol](file:///e:/The%20Human%20Algorithm/T2/agent/docs/07_Protocols/INTEGRATE_FEATURE.md).

## 2. Core Responsibilities
- **Batch Refactoring**: Safely modifies multiple files across systems.
- **Dependency Resolution**: Updates `eva_master_registry.yaml` automatically when adding new components.
- **Deployment Prep**: Validates build status and runs local tests before finalizing changes.

## 3. Code Mapping
- `subagents/technician_subagent.py`: Execution engine for codebase modifications.
