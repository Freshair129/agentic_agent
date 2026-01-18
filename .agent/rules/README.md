# .agent/rules — Constitutional Documents

**Directory**: `.agent/rules/`  
**Purpose**: Immutable philosophical and architectural principles governing EVA  
**Status**: Core (Established v9.0.0+)

---

## 📜 Overview

This directory contains **EVA's Constitution** — the foundational documents that define:

- What EVA **is** (identity, philosophy)
- How EVA **works** (architecture, patterns)
- What EVA **must never violate** (invariants, constraints)

### Sacred Principle

> **"Code may change. Rules do not."**

These documents are **immutable by default**. Changes require:

1. Architectural Decision Record (ADR)
2. Multi-stakeholder review
3. Version bump with deprecation notice

---

## 📚 Rule Hierarchy

### Tier 1: Foundation (IMMUTABLE)

#### `constitution.md`

**The 5 Pillars of EVA**

1. Embodied Existentialism
2. Single-Inference Sequentiality  
3. State Dominance
4. Identity Integrity
5. Tiered Wisdom (8-8-8)

**Status**: 🔒 **IMMUTABLE**  
**Version**: Foundation  
**Last Updated**: v9.0.0

#### `eva.md`

**The Vision & Philosophy**

- วิสัยทัศน์ (The Vision)
- Think Different philosophy
- "Craftsman, Artist, Engineer" identity
- Directory structure principles
- Memory & Soul Passport system

**Status**: 🔒 **IMMUTABLE**  
**Version**: Foundation  
**Last Updated**: v9.4.0

---

### Tier 2: Architecture (STABLE)

#### `eventpolicy.md`

**Event vs State Governance**

- EVA is NOT event-driven
- State-dominant organism principle
- Event ownership rules
- Bus architecture policy

**Status**: 🟡 **STABLE** (updates rare)  
**Version**: v9.1.0  
**Last Updated**: 2026-01-XX

#### `resonancestandard.md`

**Technical Patterns**

- Pillar of Decoupling (Signal-First)
- Pillar of Passive Persistence
- Pillar of GSD Node Excellence
- Pillar of Legacy Mapping

**Status**: 🟡 **STABLE**  
**Version**: v9.4.3+  
**Last Updated**: 2026-01-XX

#### `permissionandclassificationsystem.md`

**Authority & Access Rules**

- System classifications
- Root slot permissions
- Memory ownership maps
- Violation protocols

**Status**: 🟢 **EVOLVING**  
**Version**: v9.6.0 → v9.6.2 (needs update)  
**Last Updated**: 2026-01-XX

---

### Tier 3: Operational (EVOLVING)

#### `gapflow.md`

**Bio-Digital Gap Flow**

- 1-Inference architecture
- Perception → Gap → Reasoning
- Hydration & Persistence
- Context Safety

**Status**: 🟢 **EVOLVING**  
**Version**: v9.1.0 → v9.6.2 (needs review vs Cognitive Flow 2.0)  
**Last Updated**: 2026-01-XX

#### `memorygovernance.md`

**Memory & Belief Revision**

- 8-8-8 Tiered Hierarchy
- Belief Revision Protocol
- Epistemic Integrity

**Status**: 🟢 **EVOLVING**  
**Version**: v9.4.3 → v9.6.2 (needs update)  
**Last Updated**: 2026-01-XX

---

### Tier 4: Reference (UTILITY)

#### `glossary.md`

**Term Definitions**

- Key concepts
- Technical terminology
- Acronyms

**Status**: ⚪ **UTILITY** (frequent updates OK)  
**Version**: Unknown (needs version)  
**Last Updated**: Unknown

**⚠️ Note**: May duplicate `operation_system/configs/glossary.yaml` — needs deduplication check

#### `versioning.md`

**Version Mapping**

- Legacy version mapping (8.x.x → 1.x.x)
- Subsystem versioning
- ADR-011 reference

**Status**: ⚪ **UTILITY**  
**Version**: Unknown (needs version)  
**Last Updated**: Unknown

**⚠️ Note**: May duplicate `docs/00_Governance/VERSIONING_POLICY.md` — needs deduplication check

---

## 🎯 Rule Status Legend

| Icon | Status | Meaning | Update Policy |
|------|--------|---------|---------------|
| 🔒 | **IMMUTABLE** | Foundation principles | Requires ADR + major version bump |
| 🟡 | **STABLE** | Rarely changes | Requires ADR + minor version bump |
| 🟢 | **EVOLVING** | May update with system | Requires review + patch version bump |
| ⚪ | **UTILITY** | Frequently updated | Standard review process |

---

## 📐 Update Policy

### For IMMUTABLE Rules (🔒)

1. **Propose ADR** (Architecture Decision Record)
2. **Multi-Model Review** (minimum 3 AI models + human)
3. **Impact Analysis** (What breaks?)
4. **Migration Plan** (How to transition?)
5. **Major Version Bump** (e.g., v9 → v10)

### For STABLE Rules (🟡)

1. **Document Reason** (Why change?)
2. **Review** (1-2 models + human)
3. **Test Impact** (Run full test suite)
4. **Minor Version Bump** (e.g., v9.6 → v9.7)

### For EVOLVING Rules (🟢)

1. **Standard Review** (human + automated checks)
2. **Patch Version Bump** (e.g., v9.6.2 → v9.6.3)

### For UTILITY Rules (⚪)

1. **Direct Update** (after review)
2. **No version bump required** (unless major content change)

---

## ⚠️ Known Issues (Audit Findings)

### Version Inconsistencies

- `gapflow.md`: v9.1.0 → Should be v9.6.2 (Cognitive Flow 2.0)
- `memorygovernance.md`: v9.4.3 → Should be v9.6.2
- `permissionandclassificationsystem.md`: v9.6.0 → Should be v9.6.2
- `glossary.md`: No version → Needs version header
- `versioning.md`: No version → Needs version header

### Potential Duplications

- `glossary.md` vs `operation_system/configs/glossary.yaml`
- `versioning.md` vs `docs/00_Governance/VERSIONING_POLICY.md`

**Action Required**: Phase 2 & 3 of Documentation Audit

---

## 🔗 Related Documentation

| Location | Purpose | Relationship |
|----------|---------|--------------|
| `.agent/governance/` | Enforcement policies | Rules → Policies (enforcement) |
| `docs/00_Governance/` | Project governance | Rules → Docs (elaboration) |
| `docs/01_Philosophies/` | Philosophical depth | Rules → Philosophy (foundation) |
| `registry/eva_master_registry.yaml` | System authority | Rules → Registry (implementation) |

---

## 📖 How to Reference Rules

In code comments or documentation:

```python
# Compliant with .agent/rules/eventpolicy.md (State Dominance)
# Violates .agent/rules/resonancestandard.md (Should use Bus, not direct call)
```

In ADRs:

```markdown
## Architectural Constraints

This decision must respect:
- `.agent/rules/constitution.md` (Pillar 2: Single-Inference Sequentiality)
- `.agent/rules/resonancestandard.md` (Pillar 1: Signal-First Decoupling)
```

---

## 🏁 Status

**Total Rules**: 9 documents  
**Immutable**: 2 (constitution, eva)  
**Stable**: 2 (eventpolicy, resonancestandard)  
**Evolving**: 3 (gapflow, memorygovernance, permissions)  
**Utility**: 2 (glossary, versioning)

**Last Audit**: 2026-01-19  
**Next Audit**: After Phase 2 (Version Update)

---

*These rules form the DNA of EVA. Treat them with reverence.*
