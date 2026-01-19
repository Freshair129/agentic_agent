# 🔍 AuthDoc: Resonance Integrity Subagent (RIS)

> **Status**: DRAFT (v9.6.2 Backfill)
> **Governs**: `capabilities/tools/subagents/ris_subagent.py`

## 1. Overview
The RIS (Resonance Integrity Subagent) is the system's internal auditor. It monitors the "Doc-to-Code" alignment and detects "Ghost Keys" (configuration items without implementation).

## 2. Core Responsibilities
- **Integrity Audits**: Scans the registry against the codebase to ensure 1:1 mapping.
- **Ghost Detection**: Identifies implemented systems that lack authoritative documentation or vice-versa.
- **Version Validation**: Ensures that all components adhere to the ADR-011 versioning standard.

## 3. Code Mapping
- `subagents/ris_subagent.py`: Auditor logic and reporting engine.
