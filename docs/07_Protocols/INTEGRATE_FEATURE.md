# 🏗️ Protocol: Feature Integration (V9 Standard)

> **Status**: CANONICAL
> **Version**: 2.2.0 (SSOT & Law Enforced)

This protocol defines the mandatory steps for adding any new System, Module, or Feature to the EVA organism.

## 1. The Golden Rule: Structural Hierarchy
Every piece of logic in EVA must be nested within the [System -> Module -> Node] hierarchy. No "flat" engines are permitted in the core.

### 📁 Standard Layout
```text
[system_name]/
├── resonance_memory_system.py # Entry Point / Controller
├── Module/
│   ├── encoding_module/
│   │   ├── Node/
│   │   │   ├── color_node.py
│   │   │   └── intensity_node.py
│   │   └── encoding_module.py
│   └── latching_module/
│       ├── Node/
│       │   └── smoothing_node.py
│       └── latching_module.py
└── configs/
```

## 2. Integration Workflow

### Phase 1: Planning & Registry
1. **Define in Registry**: Update `registry/eva_master_registry.yaml` with the new System/Module/Node IDs.
2. **AuthDoc Creation**: Create the corresponding documentation in `docs/04_Systems/` or `docs/05_Capabilities/`.

### Phase 2: Structural Setup
1. **Create Folders**: Initialize `Module/` and `Node/` directories.
2. **Ghost Keys**: Add the necessary configuration variables to `configs/*.yaml`.

### Phase 3: Implementation (Atomic First)
1. **Write Nodes**: Implement small, single-responsibility logic in the `Node/` folders.
2. **Assemble Modules**: Create the Module classes that orchestrate the internal Nodes.
3. **Connect System**: Wrap the Modules in a System-level controller/authority entry point.

### Phase 4: Verification
1. **RIS Audit**: Run `python capabilities/tools/subagents/ris_subagent.py` to ensure all registered units exist.
2. **Bus Integrity**: Verify signal propagation on the Resonance Bus.

## 3. Structural Governance & SSOT

To maintain absolute integrity, all agents MUST follow these laws:

### 3.1 Documentation SSOT
- **Prohibition**: Never create a `docs/` folder within a system or module directory.
- **Centralization**: All documentation must reside in the central `docs/` folder, organized by domain.
- **Linking**: Every system/module entry in the registry MUST have an `auth_doc` field pointing to its central documentation.

### 3.2 Root Slot Protection
- **Unauthorized Creation**: No agent is permitted to create a new root-level directory without first registering it in the `root_slots` section of `registry/eva_master_registry.yaml`.
- **Redundancy Check**: Before adding data or grounding, verify if an existing location (e.g., `memory/user_profile`, `GKS`) already serves that purpose.

### 3.3 Registry Dominance
- **Pre-Registration**: Any structural change (moving files, adding systems) MUST be reflected in the registry **BEFORE** filesystem execution.
- **Sync**: Code headers must exactly match registry versions (MINOR bumps for structural changes).

### 3.4 Structural Exceptions (CNS Privilege)
- **Authority**: The **Orchestrator (CNS)** is the only system permitted to deviate from strict `[System -> Module -> Node]` nesting for its core `execution_logic`.
- **Registration**: Any non-standard directory (e.g., `Execution/`, `Node/` at system level) MUST be registered under the `specialized_slots` or `nodes` field in the system manifest.
- **Master Logic**: The `Execution/` directory (e.g., `orchestrator/Execution/CognitiveFlow/`) is a symbolic slot reserved for master orchestration logic that does not follow module-controller patterns.
- **Scope**: This privilege is restricted to the Central Nervous System and cannot be claimed by other systems/modules.

## ⚖️ Enforcement
Failure to follow the **[Structural Law Enforcement](file:///e:/The%20Human%20Algorithm/T2/agent/.agent/workflows/structural-law-enforcement.md)** workflow is a **Constitutional Violation**.

---
*Authored by: Antigravity*
