<!-- markdownlint-disable MD024 -->
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

```text
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

```text
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

---

## Step 8: Log Version Changes (MANDATORY)

**EVERY version change MUST be logged** in `registry/version_log.yaml`

### Required Information

```yaml
- timestamp: 2026-01-18T14:30:00+07:00  # Use current datetime
  system_id: PhysioCore                  # From registry
  version_from: 2.4.3
  version_to: 2.5.0
  change_type: MINOR                     # MAJOR | MINOR | PATCH
  reason: "Added new hormone: Ghrelin"   # WHY this change
  changed_by: USER + Antigravity         # Who approved
  files_affected:
    - registry/eva_master_registry.yaml
    - physio_core/physio_core.py
    - physio_core/modules/endocrine_engine.py
  rollback_command: >
    1. Update registry: PhysioCore version 2.5.0 -> 2.4.3
    2. Update code: physio_core.py line 2
    3. Remove Ghrelin module
    4. git revert [commit_hash]
  git_commit: "[PhysioCore] v2.5.0: Added Ghrelin hormone support"
  approved: true
```

### How to Log

1. **Open** `registry/version_log.yaml`
2. **Add new entry** at TOP of `changes:` list (newest first)
3. **Fill all fields** - no field should be empty
4. **Save** and commit with the same message as `git_commit` field

### Rollback Procedure

To roll back to a previous version:

```bash
# 1. Find the change entry in version_log.yaml
# 2. Follow the rollback_command instructions
# 3. Remove the change entry from version_log.yaml
# 4. Commit with: [Rollback] System X.Y.Z -> A.B.C
```

**Example Rollback**:

```yaml
# Entry to roll back:
- timestamp: 2026-01-18T14:30:00+07:00
  system_id: PhysioCore
  version_from: 2.4.3
  version_to: 2.5.0
  rollback_command: >
    1. Update registry: PhysioCore version 2.5.0 -> 2.4.3
    2. Update code: physio_core.py line 2
    3. Remove Ghrelin module
    4. git revert abc123

# Execute rollback:
$ # Step 1: Update registry
$ # Step 2: Update code header
$ # Step 3: Delete module file
$ git add .
$ git commit -m "[Rollback] PhysioCore 2.5.0 -> 2.4.3 (removed Ghrelin)"
$ # Step 4: Remove this entry from version_log.yaml
```

---

## Step 9: Audit Trail

### View Full Version History

```bash
# All changes to a specific system
grep -A 10 "system_id: PhysioCore" registry/version_log.yaml

# Changes within date range
grep "2026-01" registry/version_log.yaml

# Approved vs Pending changes
grep "approved: false" registry/version_log.yaml
```

### Compliance Report

```python
# scripts/version_audit.py
import yaml
from datetime import datetime

log = yaml.safe_load(open("registry/version_log.yaml"))

print("Version Change Audit Report")
print(f"Baseline Date: {log['baseline_date']}")
print(f"Total Changes: {len(log['changes'])}")

for change in log['changes']:
    print(f"\n{change['timestamp']}: {change['system_id']}")
    print(f"  {change['version_from']} → {change['version_to']}")
    print(f"  Reason: {change['reason']}")
    print(f"  Approved: {change['approved']}")
```

---

## Common Scenarios

### Scenario 1: Adding a New System

1. Decide initial version (usually `2.0.0` for new v9 systems)
2. Add to registry with `version` field
3. Add version header to code
4. Update `root_slots` if needed
5. **Log the change** in `version_log.yaml`:

```yaml
- timestamp: [now]
  system_id: NewSystem
  version_from: null  # New system
  version_to: 2.0.0
  change_type: MAJOR
  reason: "Initial implementation of NewSystem"
  changed_by: [Your Name]
  files_affected: [...]
  rollback_command: >
    Delete all NewSystem files and remove from registry
  git_commit: "[NewSystem] v2.0.0: Initial implementation"
  approved: true
```

---

---

## International Standards Compliance

EVA version control follows these internationally recognized standards:

### 1. Semantic Versioning 2.0.0 (semver.org)

```
MAJOR.MINOR.PATCH

MAJOR: Breaking changes, incompatible API changes
MINOR: New features, backwards compatible
PATCH: Bug fixes, backwards compatible

Pre-release: 9.7.0-alpha.1, 9.7.0-beta.2, 9.7.0-rc.1
Build metadata: 9.7.0+build.123
```

**EVA applies to:** Organism version + all system versions independently.

### 2. Conventional Commits 1.0.0 (conventionalcommits.org)

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Types:**

| Type | Description | Version Impact |
|------|-------------|---------------|
| `feat` | New feature | MINOR bump |
| `fix` | Bug fix | PATCH bump |
| `refactor` | Code restructuring (no behavior change) | No bump |
| `docs` | Documentation only | No bump |
| `style` | Formatting, missing semicolons | No bump |
| `test` | Adding or correcting tests | No bump |
| `chore` | Maintenance, tooling | No bump |
| `perf` | Performance improvement | PATCH bump |
| `ci` | CI/CD changes | No bump |
| `build` | Build system changes | No bump |
| `revert` | Revert previous commit | Depends on reverted commit |

**Breaking changes:** Add `!` after type or add `BREAKING CHANGE:` in footer → MAJOR bump.

**EVA-specific format:**

```bash
# Standard
feat(PhysioCore): add ghrelin hormone support
fix(MSP): correct episodic schema validation
refactor(Orchestrator): modularize CIM into Node hierarchy
docs(CLAUDE.md): sync with actual codebase

# Breaking change
feat(API)!: change /api/chat response envelope format

BREAKING CHANGE: response.text renamed to response.content

# Multi-system
feat(EVA): v9.7.0 Epoch Reflex — 4-Layer Affective Reflex System
```

### 3. Keep a Changelog 1.1.0 (keepachangelog.com)

```markdown
## [version] - YYYY-MM-DD

### Added       — new features
### Changed     — changes to existing features
### Deprecated  — features that will be removed
### Removed     — removed features
### Fixed       — bug fixes
### Security    — vulnerability fixes
```

**EVA applies to:** `docs/00_Governance/CHANGELOG.md`
**Extension:** EVA uses sliding window format (5 recent entries full, older as index).

### 4. Git Tags (for releases)

```bash
# Tag format
git tag -a v9.7.0 -m "Epoch Reflex: 4-Layer Affective Reflex System"

# Push tags
git push origin v9.7.0

# List tags
git tag -l "v9.*"
```

---

## Pre-Commit Checklist (MANDATORY)

Before every commit, verify:

```
□ 1. Code compiles/runs without errors
□ 2. Version numbers match:
     □ registry/eva_master_registry.yaml
     □ registry/master_configs.yaml
     □ Code file headers
     Run: python scripts/check_versions.py
□ 3. CHANGELOG updated (docs/00_Governance/CHANGELOG.md)
□ 4. version_log.yaml entry added (if version changed)
□ 5. Commit message follows Conventional Commits format
□ 6. No root policy violations (only CLAUDE.md + .gitignore at root)
     Run: ls *.md *.yaml *.json (should show only CLAUDE.md)
□ 7. No hardcoded IDs (use IdentityManager constants)
□ 8. Schema validation passes (if MSP data changed)
```

## Post-Commit Checklist

After committing:

```
□ 1. changelog/CL-YYYYMMDD-NNN.md created (if significant change)
□ 2. CLAUDE.md updated (if paths, features, or architecture changed)
□ 3. Git tag created (if version bumped)
□ 4. Notify partner agents (Gemini) of changes
```

## Rollback Protocol

```bash
# 1. Identify the bad commit
git log --oneline -10

# 2. Check version_log.yaml for rollback instructions
cat registry/version_log.yaml | grep -A 15 "version_to: X.Y.Z"

# 3. Execute rollback (prefer revert over reset)
git revert <commit-hash>

# 4. Update version_log.yaml (remove or mark as rolled back)

# 5. Update CHANGELOG.md

# 6. Commit rollback
git commit -m "revert(System): rollback X.Y.Z → A.B.C — reason"
```

---

**Enforcement**: Version mismatches are detected during code review and pre-commit checks.
**Tool**: `scripts/check_versions.py` should be added to pre-commit hooks.
**Audit**: All version changes logged in `registry/version_log.yaml` for compliance and rollback.
**Standards**: Semantic Versioning 2.0.0, Conventional Commits 1.0.0, Keep a Changelog 1.1.0.
