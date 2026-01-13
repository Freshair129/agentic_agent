# MSP Authority & Boundary Specification
Version: 1.0.0  
Applies to: EVA Memory Architecture ≥ 4.0.0  
Status: Canonical / Non-Overrideable

---

## 1. Purpose

This document defines the **authority, responsibility, and hard boundaries**
of the **MSP (Memory OS / Memory & Soul Passport)** within the EVA architecture.

The goal is to:
- Prevent ownership ambiguity
- Eliminate temporal paradoxes
- Ensure auditability and identity continuity
- Enforce strict separation between *memory ownership* and *memory management*

This is a **system-level contract**, not an implementation detail.

---

## 2. Core Principle (Non-Negotiable)

> **EVA owns memory.  
> MSP manages memory.  
> MSP never owns EVA’s lived experience.**

---

## 3. Entity Definitions

### 3.1 EVA (Cognitive Entity)
- A continuous identity
- Possesses lived experience
- Owns mutable memory
- Experiences time forward-only

### 3.2 MSP (Memory OS)
- Stateless system component
- Has no identity, no memory, no past
- Acts only as a custodian, validator, and archivist
- Replaceable without loss of EVA identity

---

## 4. Memory Domains & Ownership

| Domain | Path | Owner | Mutability | Authority |
|------|------|-------|------------|-----------|
| Live Consciousness | `eva/consciousness/` | EVA | Mutable | EVA |
| Session Snapshots | `eva/consciousness/session_*` | EVA | Frozen | EVA |
| Archival Memory | `/archival_memory/` | MSP | Immutable | MSP |

**Ownership is absolute and must never be inferred implicitly.**

---

## 5. MSP Authority (What MSP May Do)

MSP is authorized to:

1. Observe memory events emitted from EVA subsystems
2. Validate memory payloads against declared schemas
3. Normalize and scrub non-serializable artifacts
4. Persist validated data to appropriate memory domains
5. Freeze completed memory states at defined lifecycle boundaries
6. Archive frozen memory into immutable cold storage
7. Generate indexes, checksums, and provenance metadata
8. Provide read-only access to archival memory for audit or replay

MSP **never interprets** memory content.

---

## 6. MSP Prohibitions (Hard Boundary)

MSP **must never**:

- ❌ Write directly into `eva/consciousness/`
- ❌ Modify or rewrite any archived memory
- ❌ Reinterpret historical memory using current persona logic
- ❌ Generate new memory content
- ❌ Act as an identity-bearing entity
- ❌ Perform reverse data flow from archive to live memory
- ❌ Be treated as a persona, agent, or narrator

Violation of any prohibition constitutes a **system-level fault**.

---

## 7. Memory Flow Directionality

Memory flows strictly forward in time:
LIVE (EVA-owned)
↓ freeze
SNAPSHOT (immutable)
↓ archive
ARCHIVAL (MSP-owned)


Reverse flow is prohibited under all circumstances.

---

## 8. Freeze vs Archive (Semantic Separation)

### Freeze
- Converts mutable memory to immutable state
- Ownership remains with EVA
- Triggered by session end or lifecycle thresholds

### Archive
- Transfers frozen memory into MSP custody
- Applies compression, consolidation, and indexing
- Final state: immutable, auditable, replayable

Freeze ≠ Archive  
Archive is irreversible.

---

## 9. MSP and Persona Interaction

- MSP is persona-agnostic
- Persona identity is contextual and external to MSP
- MSP does not branch, fork, or merge personas
- Persona evolution must never alter archived memory

Persona changes affect **interpretation**, not **evidence**

---

## 10. Audit & Replay Guarantees

All archival memory must include:
- Schema version
- Checksum (content integrity)
- Provenance (source, timestamp, lifecycle stage)

Replay operations must:
- Use historical schema and context
- Never apply current persona cognition
- Preserve original temporal ordering

---

## 11. Failure Handling

In the event of:
- Crash
- Partial write
- Interrupted archive

MSP must:
- Abort safely
- Preserve last valid immutable state
- Never attempt heuristic recovery that alters content

---

## 12. Replaceability Requirement

MSP **must be replaceable** without:
- Loss of EVA identity
- Modification of archival memory
- Reinterpretation of historical data

If MSP cannot be replaced safely, the architecture is considered invalid.

---

## 13. Final Invariant

> **MSP is not a mind.  
> MSP does not remember.  
> MSP ensures that what EVA remembers can never be lost or rewritten.**

---

End of Specification


