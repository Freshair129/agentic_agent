# ADR-015: GSD Governance Scope & Core System Exceptions

> **Status**: APPROVED  
> **Date**: 2026-01-18  
> **Context**: Clarification of GSD application scope and structural exceptions

---

## 1. Problem Statement

There was confusion about:

1. When to use **GSD (Get Shit Done)** vs **SOLID Structure**
2. Whether **Core Systems** (PhysioCore, MSP) must follow v9.4.3 structure standards
3. The meaning of "GSD" itself (Get Shit Done vs Goal-State Driven)

---

## 2. Decision

### 2.1 GSD Definition (Resolved)

**GSD = "Get Shit Done"** (from [Cars-10/get-shit-done-gemini](https://github.com/Cars-10/get-shit-done-gemini))

- **Philosophy**: Practical, anti-bureaucracy, focus on working code over structure
- **Not**: "Goal-State Driven" (this was a misinterpretation that appeared in some docs)

### 2.2 When to Use GSD

**✅ USE GSD for:**

- **Simple Components/Nodes** with 1-2 methods
- **Non-critical features** that don't impact core functionality
- **Speed-critical implementations** where SOLID overhead is unnecessary

**Example**: A utility node with only `format_timestamp()` doesn't need:

- Separate `ITimestampFormatter.py` interface
- Abstract base class inheritance
- Module/Node directory structure

**❌ DON'T USE GSD for:**

- Multi-implementation interfaces (when polymorphism is actually needed)
- Core business logic that changes frequently
- Public APIs exposed across Systems

### 2.3 Core System Exceptions (The Untouchables)

**PhysioCore** and **MSP** are **EXEMPT** from v9.4.3 structure standards.

#### Why?

1. **Stability Lock**: These are architectural foundations - changing structure risks cascade failures
2. **Performance Critical**: PhysioCore runs 30Hz loops - refactoring overhead is unacceptable
3. **Proven Stability**: Both systems are **Verified Stable** and **Verified Coupled** ✅

#### What This Means

| Aspect | Standard Systems | PhysioCore & MSP (Exceptions) |
| :--- | :--- | :--- |
| **Directory Structure** | Must follow v9.4.3 | Can deviate if needed |
| **Interface Contracts** | Encouraged | Optional (legacy OK) |
| **File Organization** | Module/Node hierarchy | Any structure that works |
| **Refactoring Priority** | Normal | **LOWEST** (only if broken) |

---

## 3. GSD vs SOLID Decision Matrix

| Hierarchy Level | Default Approach | GSD Allowed? | Reasoning |
| :--- | :--- | :--- | :--- |
| **System** (Organs) | ⚠️ **SOLID** | ❌ No | High-level contracts needed for decoupling |
| **Module** (Integrators) | ⚖️ **Hybrid** | ✅ Yes | Simple modules can be functional |
| **Node** (Logic) | ✅ **GSD** | ✅ Yes | Pure logic, no need for abstraction |
| **Component** (Utilities) | ✅ **GSD** | ✅ Yes | Single-purpose functions |

### Decision Algorithm

```text
START
 ↓
 Does this code have >2 implementations? → YES → Use SOLID
 ↓ NO
 Is this a Public API between Systems? → YES → Use SOLID
 ↓ NO
 Is this PhysioCore or MSP? → YES → **DO NOT TOUCH** (Structural Lock)
 ↓ NO
 Is implementation <50 lines AND <3 methods? → YES → **Use GSD**
 ↓ NO
 Use SOLID (play it safe)
```

---

## 4. Registry Consolidation (Related)

As part of this governance clarification, we consolidated:

- ❌ `operation_system/configs/permissions.yaml`
- ❌ `operation_system/configs/core_systems.yaml`

Into:

- ✅ `registry/eva_master_registry.yaml` (Single Source of Truth)

This aligns with the **"consolidation over scattering"** principle.

---

## 5. Documentation Updates Required

Files using **"Goal-State Driven"** terminology must be updated:

- [x] ADR-013: Already uses correct principles (just wrong label)
- [ ] `docs/03_Architecture/EVA_v9.4.3_Architecture.md` (line 115)
- [ ] `docs/00_Governance/CHANGELOG.md` (mentions GSD)
- [ ] Implementation plan artifacts (if still referenced)

**Action**: Either remove the expansion or use "GSD (Implementation Pattern)" without expansion.

---

## 6. Consequences

### Positive

- **Clarity**: Developers know exactly when to use GSD vs SOLID
- **Safety**: Core Systems protected from unnecessary refactoring
- **Speed**: Simple components can be built quickly without bureaucracy

### Negative

- **Judgment Required**: Engineers must evaluate complexity before choosing approach
- **Inconsistency Risk**: Mixed codebase with different styles

### Mitigation

- Use the Decision Algorithm (Section 3)
- When in doubt, ask: **"Would refactoring this break anything critical?"**

---

## 7. Related Documents

- [EVA Development Protocol](../../EVA%20Development%20Protocol.md) - GSD philosophy
- [ADR-013: GSD Node Implementation Pattern](./013_gsd_node_implementation_pattern.md)
- [ADR-011: Independent Component Versioning](./011_independent_component_versioning.md)
- [Master Registry](../../registry/eva_master_registry.yaml) - Consolidated permissions

---

**Enforcement**: This is a **governance decision**, not a coding standard.  
**Review**: Required when adding new Systems or changing existing Core Systems.
