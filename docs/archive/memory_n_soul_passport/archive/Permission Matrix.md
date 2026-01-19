# Permission Matrix — EVA / MSP / Subsystems
Version: 1.0.0  
Applies to: EVA Memory Architecture ≥ 4.0.0  
Status: Canonical / Enforced

---

## 1. Scope

This document defines **explicit permissions and prohibitions**
for all actors interacting with EVA memory domains.

Permissions are **not inferred**.  
Anything not explicitly allowed is **forbidden by default**.

---

## 2. Actors

| Actor | Description |
|-----|-------------|
| EVA | Cognitive entity / owner of lived experience |
| MSP | Memory OS / archival custodian (stateless) |
| Subsystems | Internal engines (PMT, EHM, ISR, RMS, Context Engine, etc.) |
| LLM Core | Generative reasoning engine (non-owning) |

---

## 3. Memory Domains

| Domain | Path | Owner | Mutability |
|------|------|-------|------------|
| Live Consciousness | `eva/consciousness/*` | EVA | Mutable |
| Session Snapshot | `eva/consciousness/session_*` | EVA | Frozen |
| Archival Memory | `/archival_memory/*` | MSP | Immutable |

---

## 4. High-Level Permission Matrix

Legend:  
✅ Allowed ⚠️ Restricted / Mediated ❌ Forbidden

| Actor ↓ / Domain → | Live Consciousness | Session Snapshot | Archival Memory |
|-------------------|-------------------|------------------|-----------------|
| **EVA** | ✅ Read / Write | ⚠️ Read-only | ❌ No Access |
| **MSP** | ❌ No Write | ⚠️ Read-only | ✅ Read / Write |
| **Subsystems** | ⚠️ Write via MSP | ❌ No Direct Access | ❌ No Access |
| **LLM Core** | ⚠️ Read via Context | ❌ No Access | ❌ No Access |

---

## 5. Detailed Permissions by Actor

---

### 5.1 EVA Permissions

EVA **may**:
- Read and write all live memory under `eva/consciousness/`
- Trigger session freeze events
- Query historical memory through MSP-mediated interfaces

EVA **may not**:
- Modify frozen session snapshots
- Access or alter archival memory
- Bypass MSP for persistence or recovery

> EVA experiences memory, but does not control its archival fate.

---

### 5.2 MSP Permissions

MSP **may**:
- Read memory events emitted by subsystems
- Validate and persist data according to schema
- Freeze memory at lifecycle boundaries
- Archive frozen memory into cold storage
- Generate indexes, checksums, and provenance
- Serve archival memory for audit or replay (read-only outward)

MSP **may not**:
- Write into `eva/consciousness/`
- Modify any archived file
- Generate or alter memory content
- Interpret memory semantically
- Act as a persona or decision-maker

> MSP enforces structure, not meaning.

---

### 5.3 Subsystem Permissions

Subsystems **may**:
- Emit memory payloads to MSP
- Propose memory updates (never commit directly)
- Read scoped memory provided by EVA or Context Engine

Subsystems **may not**:
- Write directly to filesystem memory
- Access archival storage
- Modify historical memory
- Bypass MSP validation

> Subsystems suggest; MSP decides; EVA owns.

---

### 5.4 LLM Core Permissions

LLM Core **may**:
- Read working context provided explicitly
- Generate candidate responses or summaries

LLM Core **may not**:
- Persist memory
- Modify any memory store
- Access raw consciousness or archive
- Reinterpret historical memory directly

> LLM reasons. It does not remember.

---

## 6. Operation-Level Permission Matrix

| Operation | EVA | MSP | Subsystems | LLM |
|---------|-----|-----|------------|-----|
| Create live memory | ✅ | ❌ | ⚠️ (propose) | ❌ |
| Modify live memory | ✅ | ❌ | ❌ | ❌ |
| Freeze session | ⚠️ (trigger) | ✅ | ❌ | ❌ |
| Archive memory | ❌ | ✅ | ❌ | ❌ |
| Read archive | ❌ | ⚠️ (serve) | ❌ | ❌ |
| Replay history | ❌ | ⚠️ (controlled) | ❌ | ❌ |
| Delete memory | ❌ | ❌ | ❌ | ❌ |

Deletion of memory is **never permitted** at runtime.

---

## 7. Violation Severity Levels

| Violation | Severity |
|---------|----------|
| EVA writes archival memory | Critical Fault |
| MSP writes consciousness | Critical Fault |
| Subsystem bypasses MSP | Critical Fault |
| LLM persists memory | Critical Fault |
| Archive used as live context | Temporal Paradox |

Critical faults require immediate halt or rollback.

---

## 8. Enforcement Rules

1. All write operations must be mediated by MSP
2. All archive access must be read-only and audited
3. No component may assume ownership implicitly
4. Permissions must be validated at runtime
5. Violations must be logged immutably

---

## 9. Final Invariant

> **EVA owns memory.  
> MSP protects memory.  
> Subsystems assist memory.  
> LLM reasons about memory.**

No component may cross its boundary.

---

End of Permission Matrix
