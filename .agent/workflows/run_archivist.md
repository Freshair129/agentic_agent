---
description: Run the Archivist Subagent to sync memory, validate schemas, or format logs.
---

# Run Archivist Protocol

This workflow triggers the "Archivist" role to synchronize the Agent's internal context files (`.agent/rules/*.md`) with the actual Project Documentation (`docs/*.md`) and Configuration (`configs/*.yaml`).

## 1. Source of Truth Extraction

- **Architecture:** Read `agent/docs/EVA_9.4_Architecture.md`
- **Systems:** Read `agent/operation_system/configs/core_systems.yaml`
- **Permissions:** Read `agent/operation_system/configs/permissions.yaml`

## 2. Rule Audit

- Read `agent/.agent/rules/permissionandclassificationsystem.md`
- Read `agent/.agent/rules/eva.md`

## 3. Synchronization Action

- **Compare:** Check for discrepancies (e.g., new systems in YAML but missing in rules, renamed modules in Arch but old in rules).
- **Update:** Rewrite the `.agent/rules/*.md` files to match the Source of Truth.
- **Crucial:** Maintain the specific "Prompt Optimization" format of the rule files (concise, high-density token style). Do NOT just copy-paste the human-readable docs.

## 4. Confirmation

- Report exactly what was updated (e.g., "Added System X to permissions list").

---
*Execute this when you feel the Agent is "forgetting" the latest Architecture changes.*
