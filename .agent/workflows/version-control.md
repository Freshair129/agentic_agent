---
description: Check and validate system/module versions against registry (SSOT)
---

# Version Control Workflow

This workflow ensures that all system and module versions in code match the registry (Single Source of Truth).

## Step 1: Understand Version Mapping (ADR-011)

EVA uses **independent component versioning** where internal system versions follow their own lifecycle:

- **Mapping Rule:** `8.x.x` organism version → `1.x.x` system version
- **Mapping Rule:** `9.x.x` organism version → `2.x.x` system version
- **Example:** EVA 9.4.3 → PhysioCore 2.4.3, MSP 1.1.0 (legacy)

**See:** [VERSIONING_POLICY.md](file:///e:/The%20Human%20Algorithm/T2/agent/docs/00_Governance/VERSIONING_POLICY.md)

---

## Step 2: Check Registry (SSOT)

The **authoritative** version source is:

```
File: registry/eva_master_registry.yaml
```

Each system entry has a `version` field:

```yaml
- id: PhysioCore
  name: Physiological_Core
  version: 2.4.3  # Current SSOT
```

---

## Step 3: Verify Code Headers

Check that the version in Python file headers matches the registry.

### Example Locations

```
physio_core/physio_core.py
eva_matrix/eva_matrix.py
memory_n_soul_passport/memory_n_soul_passport_engine.py
orchestrator/orchestrator.py
```

### Expected Header Format

```python
"""
System: PhysioCore
Version: 2.4.3  # MUST match registry
"""
```

---

## Step 4: Update Mismatched Versions

If you find a version mismatch:

### Option A: Code is Outdated

1. Update the code header to match registry
2. Commit: `[Version] Sync PhysioCore to v2.4.3 per registry`

### Option B: Registry is Outdated

1. Update `registry/eva_master_registry.yaml`
2. Document reason in commit message
3. Update related ADRs if this is a MAJOR/MINOR change
4. Commit: `[Registry] Bump PhysioCore to v2.5.0 (added new module)`

---

## Step 5: Automated Check (Optional)

Create a verification script:

```python
# scripts/check_versions.py
import yaml
import re
from pathlib import Path

def check_system_versions():
    # Load registry
    registry = yaml.safe_load(Path("registry/eva_master_registry.yaml").read_text())
    
    errors = []
    for system in registry['systems']:
        system_id = system['id']
        expected_version = system['version']
        
        # Find corresponding Python file
        file_path = find_system_file(system_id)
        if not file_path:
            continue
            
        # Extract version from header
        code_version = extract_version_from_code(file_path)
        
        if code_version != expected_version:
            errors.append(f"{system_id}: Registry={expected_version}, Code={code_version}")
    
    if errors:
        print("❌ Version Mismatches Found:")
        for error in errors:
            print(f"  - {error}")
        return False
    else:
        print("✅ All versions match registry (SSOT)")
        return True
```

Run before commits:

```bash
python scripts/check_versions.py
```

---

## Step 6: Version Increment Rules

When to bump versions (per VERSIONING_POLICY.md):

### MAJOR (X.0.0)

- Breaking API changes
- Architectural paradigm shift
- **Example:** PhysioCore 2.x → 3.0.0 (switch from 30Hz to continuous stream)

### MINOR (0.Y.0)

- New module added
- New feature (backwards compatible)
- **Example:** PhysioCore 2.4.x → 2.5.0 (add new hormone)

### PATCH (0.0.Z)

- Bug fixes
- Performance improvements
- **Example:** PhysioCore 2.4.3 → 2.4.4 (fix reflex calculation)

---

## Step 7: Documentation Updates Required

When bumping a system version, also update:

1. **Registry** (`registry/eva_master_registry.yaml`)
2. **Code Header** (system's main Python file)
3. **CHANGELOG** (`docs/00_Governance/CHANGELOG.md`)
4. **ADR** (if architectural change)

---

## Common Scenarios

### Scenario 1: Adding a New System

1. Decide initial version (usually `2.0.0` for new v9 systems)
2. Add to registry with `version` field
3. Add version header to code
4. Update `root_slots` if needed

### Scenario 2: Refactoring Existing System

1. Determine version impact (MAJOR/MINOR/PATCH)
2. Update registry version first (SSOT)
3. Update code header
4. Document in CHANGELOG

### Scenario 3: Pre-Commit Validation

```bash
# Run before git commit
python scripts/check_versions.py

# If pass:
git add .
git commit -m "[...] message"

# If fail:
# Fix mismatches, then retry
```

---

## Emergency: Version Conflict Resolution

If registry and code disagree:

1. **Trust the Registry** (SSOT principle)
2. Check git history to see which was updated last
3. If registry is newer → Update code
4. If code is newer → Likely forgot to update registry → Update registry + CHANGELOG
5. Create ADR if this represents a significant change

---

**Enforcement**: Version mismatches are detected during code review.  
**Tool**: Consider adding `check_versions.py` to pre-commit hooks.
