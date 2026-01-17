# ADR-017: Config Centralization & Standard Structure Enforcement

> **Status**: APPROVED  
> **Date**: 2026-01-18  
> **Context**: Reducing configuration chaos by centralizing configs and enforcing standard structure

---

## 1. Problem Statement

Configuration files are currently scattered across multiple systems:

- `system_name/configs/` (3-4 files per system)
- `operation_system/configs/` (global configs)
- `registry/` (topology)

**Pain Points**:

- Editing one feature requires touching 3-4 files
- Config drift between systems
- Unclear which config is authoritative
- Violates DRY (Don't Repeat Yourself)

---

## 2. Decision: Two-Tier Config Strategy

### 2.1 Centralized Global Configs

**Location**: `operation_system/configs/`

**What Goes Here**:

- `glossary.yaml` - Terminology (SSOT for acronyms)
- `system_defaults.yaml` - Default settings shared across systems
- `bus_channels.yaml` - Bus configuration
- `identity.yaml` - Persona definitions
- System-agnostic configurations

**Benefit**: One place to update cross-system settings

### 2.2 System-Specific Configs

**Location**: `system_name/configs/` (ONLY if truly system-specific)

**Allowed**:

- System-unique parameters (e.g., PhysioCore hormone thresholds)
- Module-specific settings
- Internal component configuration

**NOT Allowed**:

- Duplicate global settings
- Bus channel definitions (use global)
- Identity/persona configs (use global)

---

## 3. Standard Structure Enforcement

### 3.1 Exception List (Structural Freedom)

These systems are **EXEMPT** from v9.4.3 standard structure:

| System | Reason | Current Structure |
| :--- | :--- | :--- |
| **PhysioCore** | Verified Stable, Performance Critical (30Hz) | `logic/` directory |
| **MSP** | Legacy, Verified Stable | Custom structure |

**Reference**: ADR-015 (GSD Governance Scope)

### 3.2 Required Standard Structure (All Other Systems)

**Mandatory for**: EVA_Matrix, Orchestrator, RMS, GKS, Artifact_Qualia, AgenticRAG, etc.

**v9.4.3 Standard Structure**:

```text
system_name/
├── Module/              # Integration layer
│   └── ComponentX.py
├── Node/                # Pure logic
│   ├── LogicA.py
│   └── LogicB.py
├── configs/             # System-specific settings ONLY
│   └── system_config.yaml
├── schema/              # Data schemas
│   └── system_schema.json
└── system_name.py       # Main entry point
```

**Note**: Contracts are **centralized** at `agent/contracts/`, not in system directories.

**Benefits**:

- Predictable file locations
- Easier onboarding
- Automated tooling (Archivist, RIS)
- Consistent import paths
- SSOT for interfaces (agent/contracts/)

---

## 3.3 Contracts Centralization

**Location**: `agent/contracts/` (SSOT for all public interfaces)

**Structure**:

```text
agent/contracts/
├── systems/         # System-level interfaces (5 files)
│   ├── IPhysioSystem.py
│   ├── IMatrixSystem.py
│   ├── IMSPassport.py
│   ├── IOrchestrator.py
│   └── IResonanceBus.py
└── modules/         # Module-level interfaces (4 files)
    ├── ICognitiveGateway.py
    ├── IKnowledgeAuthority.py
    ├── IMemoryRetrieval.py
    └── IMemoryStorage.py
```

**Rules**:

1. **NO** `system_name/contracts/` directories (redundant)
2. **All** public interfaces MUST be in `agent/contracts/`
3. **Exception**: Internal contracts (used only within a system) can live in `system_name/internal/` if needed

**Benefits**:

- ✅ SSOT for all interfaces
- ✅ Prevents interface duplication
- ✅ Easier to find and update contracts
- ✅ Follows Dependency Inversion Principle (SOLID "D")

---

## 4. Config Migration Plan

### Phase 1: Audit Current Configs

```bash
# Find all config files
find agent/ -name "*.yaml" -path "*/configs/*"

# Categorize:
# - Global (move to operation_system/configs/)
# - System-specific (keep in system_name/configs/)
# - Duplicate (merge into global)
```

### Phase 2: Create Global Configs

**New Files** in `operation_system/configs/`:

1. **`system_defaults.yaml`** - Shared defaults

```yaml
defaults:
  bus:
    retry_count: 3
    timeout_ms: 5000
  logging:
    level: INFO
    format: json
```

1. **`bus_channels.yaml`** - Bus topology

```yaml
channels:
  BUS_PHYSICAL: {stream: hormones, subscribers: [EVA_Matrix]}
  BUS_PSYCHOLOGICAL: {stream: matrix_state, subscribers: [Artifact_Qualia]}
```

### Phase 3: Update Systems

For each non-exception system:

1. Remove duplicate global settings
2. Keep only system-unique configs
3. Update code to load from centralized configs
4. Update registry manifest

---

## 5. Implementation Rules

### Rule 1: Config Priority (Cascade)

```
1. system_name/configs/system_config.yaml  (highest priority)
2. operation_system/configs/system_defaults.yaml
3. Hard-coded fallbacks in code (lowest priority)
```

### Rule 2: Config Loading Pattern

```python
# Standard pattern for all systems
def load_config(system_name: str) -> dict:
    # 1. Load global defaults
    global_config = yaml.safe_load(
        Path("operation_system/configs/system_defaults.yaml").read_text()
    )
    
    # 2. Load system-specific (if exists)
    system_config_path = Path(f"{system_name}/configs/{system_name}_config.yaml")
    system_config = {}
    if system_config_path.exists():
        system_config = yaml.safe_load(system_config_path.read_text())
    
    # 3. Merge (system overrides global)
    return {**global_config, **system_config}
```

### Rule 3: No Config in Code

```python
# ❌ BAD - Hard-coded config
TIMEOUT = 5000

# ✅ GOOD - Loaded from config
config = load_config("orchestrator")
TIMEOUT = config.get("timeout_ms", 5000)  # Fallback only
```

---

## 6. Registry Enforcement

**Updated Registry Schema**:

```yaml
systems:
  - id: SystemName
    name: System_Name
    version: X.Y.Z
    
    # Structural compliance
    structure_standard: v9.4.3 | exception
    exception_reason: "Performance critical (ADR-015)" # If exception
    
    manifest:
      follows_standard: true | false
      folders:
        - system_name/Module  # Required if follows_standard=true
        - system_name/Node
      config_location: centralized | local | hybrid
```

**Validation**: Archivist will check structure compliance

---

## 7. Consequences

### Positive

- ✅ One-stop config editing
- ✅ Reduced config drift
- ✅ Clear SSOT for shared settings
- ✅ Predictable structure for non-exceptions

### Negative

- ⚠️ Migration effort for existing systems
- ⚠️ Two-tier complexity (global vs local)

### Mitigation

- Gradual migration (not breaking changes)
- Clear documentation of what goes where
- Automated validation (Archivist)

---

## 8. Related Documents

- [ADR-015: GSD Governance Scope](./015_gsd_governance_scope.md) - Exception criteria
- [Master Registry](../../registry/eva_master_registry.yaml) - SSOT for structure
- [Archivist Subagent](../../capabilities/tools/subagents/archivist_subagent.py) - Validation tool

---

**Enforcement**: Structure violations will be flagged by Archivist.  
**Review**: Quarterly review of exception list - systems must justify continued exemption.
