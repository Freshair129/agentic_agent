---
description: Protocol for enforcing Registry-Centric Governance and Single Source of Truth (SSOT).
---

# ⚖️ Workflow: Structural Law Enforcement (SSOT)

This workflow MUST be executed before any operation that involves creating new directories, moving core assets, or adding documentation. It ensures the organism remains compliant with the `eva_master_registry.yaml` (The Law).

## 1. Pre-Execution Audit (The Law Check)
Before creating any file or folder:
1.  **Check Root Slots**: Verify if the target root directory is in the `root_slots` whitelist in `registry/eva_master_registry.yaml`.
2.  **Search for Redundancy**: Use `grep_search` or `find_by_name` to check if a similar concept, documentation, or grounding file already exists (e.g., check `memory/user_profile` before adding user data).
3.  **Validate Registry Scope**: Ensure the new component belongs to an existing `system` or `module`. If not, it MUST be registered in the registry FIRST.

## 2. Documentation Governance (SSOT)
- **NO LOCAL DOCS**: Never create a `docs/` folder inside a system or module directory.
- **CENTRAL ONLY**: All documentation must reside in the central `docs/` repository.
- **AUTH_DOC LINKING**: Every new system/module MUST have its `auth_doc` field in the registry pointing to a file in the central `docs/` folder.

## 3. Grounding & Memory Governance
- **GROUNDING HOME**: User-specific grounding belongs in `memory/user_profile/` or `GKS` blocks. Never create a root-level `data/` or `grounding/` folder.
- **MSP AUTHORITY**: Only the MSP system has the right to manage archival persistence.

## 4. Automated Verification
// turbo
1.  Run the Resonance Integrity Subagent (RIS) after any structural change:
    ```powershell
    python tools/subagents/ris_subagent.py --audit structure
    ```
2.  Any "Unauthorized Slot" or "Ghost File" detected by RIS must be resolved immediately by deleting the offender or registering it.

**FAILURE TO FOLLOW THIS WORKFLOW IS A CONSTITUTIONAL VIOLATION.**
