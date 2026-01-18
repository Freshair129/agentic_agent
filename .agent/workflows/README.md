# .agent/workflows — Development Process Definitions

**Directory**: `.agent/workflows/`  
**Purpose**: Reusable development workflows and protocols  
**Status**: Active (Maintained continuously)

---

## 📋 Overview

This directory contains **workflow definitions** — step-by-step protocols for common development activities. Think of them as "recipes" that ensure consistency and quality across the project.

### Key Principle

> **"Don't reinvent the wheel. Follow the workflow."**

Workflows ensure:

- Consistent processes
- Reduced errors
- Knowledge transfer
- Automated compatibility (via special directives)

---

## 📚 Workflow Catalog

| Workflow | Purpose | Complexity | Turbo |
|----------|---------|------------|-------|
| `/checkpoint` | Create project snapshot | Medium | ✅ turbo-all |
| `/doc_to_code` | Documentation-first development | High | ⚠️ Selective |
| `/integrate_feature` | Add new features or components | High | ⚠️ Selective |
| `/autonomous-refactor` | Complex system refactors | Very High | ❌ Manual |
| `/run_archivist` | Run Archivist Subagent | Low | ✅ turbo-all |
| `/version-control` | Version checking & validation | Medium | ⚠️ Selective |

---

## 🎯 Workflow Details

### `/checkpoint` — Project Snapshot

**File**: `checkpoint.md` (1.3 KB)  
**Purpose**: Create a stable checkpoint of the project state

**When to Use:**

- After completing major features
- Before starting risky refactors
- Weekly/bi-weekly for large projects
- Before version bump

**Key Steps:**

1. Update documentation (CHANGELOG, INDEX)
2. Run Archivist (sync rules)
3. Verify codebase snapshot
4. Git commit with clear message

**Turbo**: ✅ All steps auto-run

---

### `/doc_to_code` — Documentation-First Development

**File**: `doc_to_code.md` (3.2 KB)  
**Purpose**: Ensure documentation and config precede code implementation

**When to Use:**

- Adding new features
- Changing architecture
- Modifying APIs

**Key Steps:**

1. Update docs/*.md first
2. Update configs/*.yaml
3. Run RIS (Subagent) to see "Ghost Keys" (missing implementations)
4. Implement code to satisfy docs/configs
5. Verify via RIS (ghosts disappear)

**Turbo**: ⚠️ Selective (manual review required)

---

### `/integrate_feature` — Feature Integration Protocol

**File**: `integrate_feature.md` (2.5 KB)  
**Purpose**: Add new features while maintaining system integrity

**When to Use:**

- Adding new systems/modules
- Integrating external libraries
- Creating new capabilities

**Key Steps:**

1. Check file structure compliance
2. Create documentation first
3. Register in `eva_master_registry.yaml`
4. Implement code
5. Test and verify

**Turbo**: ⚠️ Selective

---

### `/autonomous-refactor` — Complex Refactor Protocol

**File**: `autonomous-refactor.md` (1.7 KB)  
**Purpose**: Guide high-autonomy refactoring operations

**When to Use:**

- Multi-file refactors
- Architecture changes
- Breaking changes

**Key Steps:**

1. Create detailed plan
2. Get approval
3. Execute incrementally
4. Test at each step
5. Document changes

**Turbo**: ❌ Manual approval required at each phase

---

### `/run_archivist` — Archivist Subagent

**File**: `run_archivist.md` (1.3 KB)  
**Purpose**: Run the Archivist Subagent to sync memory and validate schemas

**When to Use:**

- Before checkpoints
- After rule changes
- Weekly maintenance

**Key Steps:**

1. Run with appropriate flags (`--sync-rules`, `--validate`, `--format-logs`)
2. Review output
3. Fix any violations

**Turbo**: ✅ Safe to auto-run

---

### `/version-control` — Version Validation

**File**: `version-control.md` (8.9 KB) ⚠️ **Largest**  
**Purpose**: Check and validate system/module versions against registry

**When to Use:**

- After version bumps
- Before releases
- During audits

**Key Steps:**

1. Check versions in code headers
2. Compare with `eva_master_registry.yaml`
3. Validate consistency
4. Update mismatches

**Turbo**: ⚠️ Selective

**⚠️ Note**: This file is 3-5x larger than others. May need review for possible splitting.

---

## 🚀 Turbo Mode Explained

Workflows support special directives for automation:

### `// turbo` (Single Step)

```markdown
// turbo
- Run this specific command
```

**Meaning**: This ONE step is safe to auto-run (AI can set `SafeToAutoRun: true`)

### `// turbo-all` (Entire Workflow)

```markdown
// turbo-all
# Workflow Title
```

**Meaning**: EVERY `run_command` step in this workflow is safe to auto-run

### No Directive (Manual)

```markdown
- Review this carefully
```

**Meaning**: Requires manual user approval

---

## 📐 Workflow Format

### Standard Structure

```markdown
---
description: <Short title>
---

# <Workflow Name>

## Purpose
<What this workflow achieves>

## When to Use
<Scenarios for this workflow>

## Steps

1. <Step 1>
   // turbo (if safe to auto-run)
   ```bash
   command here
   ```

1. <Step 2>
   <Description>

## Validation

<How to verify success>
```

---

## 🛠️ How to Use Workflows

### For Developers

**Via Slash Command:**

```
/checkpoint
/doc_to_code
/integrate_feature
```

AI agents will:

1. Read the workflow file
2. Execute steps in order
3. Auto-run turbo steps
4. Pause for manual steps

### For AI Agents

1. **Detect** slash command (e.g., `/checkpoint`)
2. **Read** `workflows/<command-name>.md`
3. **Parse** steps and turbo directives
4. **Execute** with appropriate `SafeToAutoRun` flags
5. **Report** progress and completion

---

## 📊 Workflow Metrics

| Metric | Value |
|--------|-------|
| **Total Workflows** | 6 |
| **Fully Automated** | 2 (checkpoint, run_archivist) |
| **Semi-Automated** | 3 (doc_to_code, integrate_feature, version-control) |
| **Manual** | 1 (autonomous-refactor) |
| **Avg Size** | ~2.5 KB |
| **Largest** | version-control.md (8.9 KB) |

---

## 🔧 Creating New Workflows

### When to Create a Workflow

✅ **Create When:**

- Repeating the same multi-step process 3+ times
- Process has clear steps and validation
- Knowledge transfer is important

❌ **Don't Create When:**

- One-off task
- Too simple (1-2 steps)
- Highly variable (no consistent pattern)

### Template

```markdown
---
description: <Your workflow title>
---

# <Workflow Full Name>

## Purpose
<What problem this solves>

## When to Use
- Scenario 1
- Scenario 2

## Prerequisites
- Requirement 1
- Requirement 2

## Steps

1. **<Step Name>**
   <Description>
   // turbo (if safe)
   ```bash
   command
   ```

## Validation

- [ ] Check 1
- [ ] Check 2

## Troubleshooting

**Issue**: <Common problem>
**Solution**: <How to fix>

```

---

## ⚠️ Workflow Maintenance

### Review Schedule
- **Monthly**: Check for outdated steps
- **After Major Changes**: Update affected workflows
- **Before Release**: Validate all workflows

### Update Process
1. Identify outdated workflow
2. Update steps
3. Test manually
4. Add "last_updated" comment
5. Commit with `[Workflow Update]` prefix

---

## 🏁 Status

**Total Workflows**: 6  
**Last Updated**: 2026-01-19  
**Coverage**: Core development processes ✅

**Planned Additions:**
- Workflow for creating new workflows (meta!)
- Testing workflow
- Release workflow
- Hotfix workflow

---

## 🔗 Related Documentation

- **Tasks**: `.agent/tasks/` — What to do
- **Workflows**: `.agent/workflows/` — How to do it
- **Rules**: `.agent/rules/` — What must be true
- **Governance**: `.agent/governance/` — What is enforced

---

*Workflows make excellence repeatable.*
