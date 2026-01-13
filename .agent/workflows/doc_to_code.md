---
description: Standard Protocol for implementing features ensuring Documentation and Config precede Code.
---

# Doc-to-Code Workflow

> **"Config is the Law. Code is the Enforcer."**

This workflow enforces the strict integrity protocol where Logic Parameters and Architecture must be defined in Documentation and Configuration BEFORE any Python code is written.

## 1. Phase 1: Legislation (The Blueprint)

- **Architecture:** Update `docs/EVA_9.4_Architecture.md` to reflect the new structure or logic flow.
- **Configuration:** Update `operation_system/configs/*.yaml` (e.g., `core_systems.yaml`, `MSP_configs.yaml`) with new parameters, module paths, or feature flags.
- *Outcome:* You have created "Ghost Keys" — configuration values that exist but are not yet used by code.

## 2. Phase 2: Execution (The Implementation)

- **Scaffold:** Create directories/files as defined in Architecture.
- **Implement:** Write the Python code.
- **Constraint:** All logic variables (timeouts, thresholds, paths) MUST be pulled from the `self.config` loaded validation. **NEVER Hardcode.**

## 3. Phase 3: Verification (The Audit)

- **Verify Config Binding:** Ensure the code successfully loads the new YAML keys without default fallbacks (referencing the YAML directly).
- **Verify Consistency:** specific implementation matches the description in `EVA_9.4_Architecture.md`.

---
*Run this workflow whenever adding new Systems, Modules, or major Logic flows.*
