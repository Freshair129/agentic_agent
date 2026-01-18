# .agent/governance — Policy Enforcement Framework

**Directory**: `.agent/governance/`  
**Purpose**: Central repository for governance policies that enforce EVA's architectural integrity  
**Status**: Active (Created v9.6.2)

---

## 📋 Overview

This directory contains **enforcement policies** that protect EVA's architecture from degradation. Unlike `.agent/rules/` (which contains immutable philosophical principles), governance policies are **actionable enforcement mechanisms**.

### Key Principle

> **"Rules define what we believe. Policies enforce what we do."**

---

## 📁 Current Policies

### 1. `root_policy.yaml`

**Purpose**: Whitelist-based root directory protection  
**Created**: 2026-01-19 (Phase 3 of Structure Optimization)  
**Status**: ✅ Active

**What it does:**

- Defines allowed files at root level
- Defines allowed directories at root level
- Provides cleanup destinations for violations
- Enables pre-commit hook enforcement

**Enforces:**

- Flat Anatomy (Embodied Organism principle)
- Prevention of "Root Pollution"
- Registry-centric organization

**Usage:**

```bash
# Manual check
python scripts/check_root_policy.py

# Pre-commit hook (requires Python 3)
# Automatically runs on git commit
```

---

## 🎯 Governance Philosophy

### What Belongs Here

✅ **Enforcement mechanisms** (whitelists, blacklists, validators)  
✅ **Automated policies** (pre-commit hooks, CI checks)  
✅ **Operational guidelines** (commit standards, branch policies)

### What Does NOT Belong Here

❌ **Philosophical principles** → Go to `.agent/rules/`  
❌ **Documentation standards** → Go to `docs/00_Governance/`  
❌ **Code conventions** → Go to individual system configs

---

## 📐 Policy Types

| Type | Purpose | Examples |
|------|---------|----------|
| **Structural** | File/folder organization | `root_policy.yaml` |
| **Versioning** | Version consistency | (Future: `version_policy.yaml`) |
| **Quality** | Code/doc quality gates | (Future: `lint_policy.yaml`) |
| **Security** | Access control | (Future: `permission_policy.yaml`) |

---

## 🔄 Policy Lifecycle

1. **Proposal**: Policy idea emerges from pain point
2. **Design**: YAML schema created
3. **Implementation**: Enforcement script written
4. **Activation**: Added to CI/CD pipeline
5. **Maintenance**: Updated as architecture evolves

---

## 🚀 Future Policies (Planned)

### `commit_policy.yaml`

- Standardize commit message format
- Enforce conventional commits
- Require issue/ticket references

### `documentation_policy.yaml`

- Require README in every top-level directory
- Enforce markdown lint standards
- Mandate version headers in docs

### `registry_sync_policy.yaml`

- Ensure `eva_master_registry.yaml` stays in sync with reality
- Validate root_slots against actual directories
- Check version consistency

---

## 📖 Related Documentation

- **Rules** (Immutable Principles): `.agent/rules/`
- **Workflows** (Development Processes): `.agent/workflows/`
- **Global Governance**: `docs/00_Governance/`
- **Registry** (System Authority): `registry/eva_master_registry.yaml`

---

## 🛠️ How to Add a New Policy

1. **Create YAML file** in this directory
2. **Follow schema**:

   ```yaml
   # policy_name.yaml
   version: 1.0.0
   created: YYYY-MM-DD
   description: What this policy enforces
   
   rules:
     - rule_1
     - rule_2
   
   enforcement:
     pre_commit_hook: true/false
     ci_check: true/false
   ```

3. **Create enforcement script** in `scripts/` if needed
4. **Update this README** to list the new policy
5. **Test** before committing

---

## ⚖️ Enforcement Hierarchy

```
Constitution (.agent/rules/constitution.md)
    ↓
Resonance Standard (.agent/rules/resonancestandard.md)
    ↓
Registry (registry/eva_master_registry.yaml)
    ↓
Governance Policies (THIS DIRECTORY)
    ↓
Individual System Configs
```

**Policies must never contradict rules or standards above them.**

---

## 🏁 Status

**Version**: 1.0.0  
**Last Updated**: 2026-01-19  
**Policies Count**: 1 (root_policy.yaml)  
**Planned**: 3 (commit, documentation, registry_sync)

---

*Maintained as part of EVA v9.6.2 architectural governance*
