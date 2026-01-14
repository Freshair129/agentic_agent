---
description: Standard protocol for adding new features or components. Ensures strict adherence to file structure, documentation, and system registration.
---

# Feature Integration Protocol

Use this workflow whenever you are adding a **new component, system, or major feature** to EVA.
Trigger: `/integrate_feature`

## 1. Plan & Document (Pre-Code)

Before writing logic, you must define the "Soul" of the feature.

1. **Concept Document**: Create `docs/systems/[domain]/[Feature_Name]_Concept.md`.
    - Define Purpose, Architecture, and Integration points.
2. **Implementation Plan**: Create/Update `implementation_plan.md` in the artifact folder.
3. **ADR Check**: If this is a major architectural decision, create a new ADR in `agent/docs/adr/`.

## 2. Structural Setup

Follow the [System -> Module -> Node] hierarchy.

1. **Create Directory**: `agent/capabilities/services/[feature_name]/` (or appropriate parent).
2. **Config First**: Create `configs/[feature]_config.yaml`. **NO HARDCODED MAGIC NUMBERS**.
3. **Main File**: Create `[feature]_engine.py` (or similar).

## 3. System Registration (CRITICAL)

You **MUST** registers the new component in `core_systems.yaml`.

1. **Open**: `agent/operation_system/configs/core_systems.yaml`.
2. **Add Entry**:

    ```yaml
    - id: [FeatureID]
      name: [Feature_Name]
      version: [X.X.X]
      role: [system_module/core_system]
      domain: [domain]
      description: "[Short description]"
      main_files:
        - path: [relative/path/to/engine.py]
        - path: [relative/path/to/config.yaml]
      id_registry: "IdentityManager.SYSTEM_[ID]"
    ```

    > **Note**: If `id_registry` constant doesn't exist, start by adding it to `IdentityManager` (if strictly necessary) or use a standard pattern.

3. **Permissions Update**:
    - **Open**: `agent/operation_system/configs/permissions.yaml`.
    - **Add Entry**: Classify your new component under `classification_criteria`.
    - **Bus Authority**: Define if it has Bus rights.

## 4. Implementation & Integration

1. **Write Code**: Implement the logic in `.py` files.
2. **Integrate**: Connect to `Orchestrator` or parent system.
3. **Verify**: Create a test script in `agent/tests/test_[feature].py`.

## 5. Finalize Documentation

1. **Changelog**: Update `agent/docs/CHANGELOG.md` under `### Added`.
2. **Task Update**: Mark steps as complete in `task.md`.
