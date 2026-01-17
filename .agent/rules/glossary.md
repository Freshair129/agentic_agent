# EVA Terminology & Acronym Policy

> **Status**: MANDATORY  
> **Scope**: All Agents (Human, AI, Subagents)  
> **Source of Truth**: `operation_system/configs/glossary.yaml`

---

## Rule: **NO GUESSING ACRONYMS**

### The Problem

Agents frequently **invent meanings** for acronyms instead of checking the official glossary:

- **Example**: GSD was interpreted as "Goal-State Driven" when it actually means "Get Shit Done"
- **Impact**: Documentation inconsistency, confusion in handovers, architectural drift

---

## Mandatory Protocol

### 1. **BEFORE** Using or Expanding an Acronym

**ALWAYS** check the glossary first:

```bash
File: operation_system/configs/glossary.yaml
Location: E:\The Human Algorithm\T2\agent\operation_system\configs\glossary.yaml
```

### 2. **IF** Acronym Not Found

**DO NOT GUESS**. Instead:

1. **Ask the user**: "I don't see `[ACRONYM]` in the glossary. What does it stand for?"
2. **Propose addition**: After confirmation, update `glossary.yaml` with the correct definition
3. **Commit change**: Use git to track glossary updates

### 3. **WHEN** Writing Documentation

- **First mention**: Use full form with acronym in parentheses
  - Example: `Memory & Soul Passport (MSP)`
- **Subsequent mentions**: Use acronym only
- **Link to glossary** if explaining a complex term

---

## Enforcement

### For AI Agents

- **Before expanding** any 2-4 letter acronym → Check glossary
- **If uncertain** → Use the full name from glossary, not guessed expansion
- **Update glossary** when introducing new terms (via pull request or user confirmation)

### For Documentation

All ADRs, Architecture docs, and READMEs **MUST** use terminology consistent with `glossary.yaml`.

**Violation**: Using non-standard expansions without glossary update → Requires correction

---

## Common Violations (Caught Examples)

| Acronym | ❌ Incorrect | ✅ Correct (Glossary) |
| :--- | :--- | :--- |
| **GSD** | Goal-State Driven | Get Shit Done |
| **CIN** | (deprecated) | **CIM** (Context Injection Module) |
| **BDC** | (deprecated) | **PhysioCore** (Physiological Core) |
| **RI** | Response Index | **Resonance Index** |

---

## Glossary Update Process

### When to Update

- New system/component introduced
- Acronym meaning changes (with ADR justification)
- Deprecated term needs removal

### How to Update

1. **Edit**: `operation_system/configs/glossary.yaml`
2. **Format**: Follow existing YAML structure
3. **Commit**: `[Glossary] Added/Updated definition for [TERM]`
4. **Reference**: Link to ADR if this is a policy change

### Example Entry

```yaml
- term: GSD
  full_name: Get Shit Done
  meaning: "Development philosophy focused on working code over bureaucracy. See ADR-015 for usage scope."
  references:
    - adr: docs/adr/015_gsd_governance_scope.md
    - source: https://github.com/Cars-10/get-shit-done-gemini
```

---

## Integration Points

The glossary is referenced in:

- **Master Registry**: `registry/eva_master_registry.yaml` (system names)
- **ADRs**: Should cite glossary when introducing new terms
- **Architecture Docs**: Should link to glossary for technical terms

---

## Penalty for Violations

**First Offense**: Gentle reminder to check glossary  
**Repeated Offense**: All documentation by that agent must be reviewed before merge  
**Systemic Issue**: Add glossary check to pre-commit hooks

---

**Summary**: When you see an acronym, **CHECK** `glossary.yaml` first. **DON'T GUESS**.
