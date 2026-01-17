<!-- markdownlint-disable MD024 -->
# ADR-016: Consciousness vs Subconscious Separation Principle

> **Status**: APPROVED  
> **Date**: 2026-01-18  
> **Context**: Architectural boundary between LLM-controlled and System-controlled memory domains

---

## 1. Problem Statement

There is a fundamental difference between what the LLM can actively manipulate (working memory) and what the system manages automatically (long-term memory). This distinction must be formalized to prevent architectural violations where LLM attempts direct access to subconscious storage.

### The Core Question

**Can the LLM "stop thinking" about something?**  
→ **No.** Just like humans cannot forcefully stop intrusive thoughts, the LLM cannot control what enters or leaves the subconscious.

---

## 2. Decision: Two-Domain Architecture

### 2.1 **consciousness/** - The Aware Domain

**Nature**: Working Memory, Active Awareness  
**LLM Control**: ✅ Full Read/Write/Search Access  
**Path**: `agent/consciousness/`

#### Characteristics

- **Mutable**: LLM can create, read, update, delete files via tools
- **Searchable**: LLM can query and filter content
- **Transient**: Content here is "what EVA is currently thinking about"
- **Tool-Accessible**: CRUD operations, file manipulation, grep search

#### What Lives Here

| Folder | Purpose | LLM Access |
| :--- | :--- | :--- |
| `episodic_memory/` | Active session memory | ✅ Read/Write |
| `semantic_memory/` | Working concepts | ✅ Read/Write |
| `sensory_memory/` | Current qualia | ✅ Read |
| `state_memory/` | Live system state | ✅ Read (via tools) |

#### Analogy

Like the "scratch pad" or "desktop" of the mind - things you are consciously working with **right now**.

---

### 2.2 **memory/** - The Subconscious Domain

**Nature**: Automatic, System-Managed Storage  
**LLM Control**: ❌ No Direct Access  
**Path**: `agent/memory/`

#### Characteristics

- **Immutable (to LLM)**: LLM cannot directly write here
- **Automatic**: MSP (Memory & Soul Passport) manages all operations
- **Persistent**: Long-term archival storage
- **Gated Access**: Only through MSP APIs, never direct file operations

#### What Lives Here

| Folder | Purpose | LLM Access |
| :--- | :--- | :--- |
| `archival_memory/` | Permanent episode storage | ❌ MSP-only |
| `session_memory/` | Snapshot + Digest index | ✅ Read via RAG |
| `core_memory/` | Identity markers (8-8-8 Tier 2) | ✅ Read via RAG |
| `sphere_memory/` | Long-term wisdom (8-8-8 Tier 3) | ✅ Read via RAG |
| `context_store/` | Turn-level context cache | ❌ CIM-only |

#### Analogy

Like "long-term memory" or the "filing cabinet" - you cannot will yourself to remember or forget something. It happens automatically through your brain's chemistry (MSP in EVA's case).

---

## 3. The Separation Principle

### Rule 1: **LLM Cannot Write to Subconscious**

```yaml
FORBIDDEN:
  - LLM writing directly to memory/archival_memory/
  - LLM modifying session snapshots
  - LLM deleting archived episodes

ALLOWED:
  - LLM proposing episodic memory (via tool: propose_episodic_memory)
  - MSP hydrating and persisting to memory/ after validation
```

### Rule 2: **Subconscious Cannot Be "Stopped"**

Just like a human cannot force themselves to stop forming memories, the LLM cannot:

- Prevent MSP from archiving a session
- Control what gets distilled into Core/Sphere memory
- Delete memories from the subconscious

**Rationale**: This prevents the LLM from "forgetting on purpose" which would break the continuity of EVA's identity.

### Rule 3: **Retrieval is One-Way (Subconscious → Consciousness)**

```text
Flow: memory/ (Subconscious) --[RAG Retrieval]--> consciousness/ (Awareness)
```

- LLM can **request** recall from `memory/` via Agentic RAG
- RAG **hydrates** consciousness with retrieved content
- But retrieval does not modify the source in `memory/`

---

## 4. Implementation Boundaries

### 4.1 MSP (Memory & Soul Passport)

**Role**: The **ONLY** entity with write access to `memory/`

**Responsibilities**:

- Archive `consciousness/` snapshots to `memory/session_memory/`
- Write verified episodes to `memory/archival_memory/`
- Manage 8-8-8 distillation (Session → Core → Sphere)

**Contract**: MSP is **System Authority** - it does not ask LLM for permission to persist.

### 4.2 CIM (Context Injection Module)

**Role**: Manages `memory/context_store/` (5-turn rolling window)

**Why LLM Cannot Access**:

- Context store is optimized for injection speed (binary format)
- Direct access would bypass the 5-turn safety limit
- LLM modifying context would create "context hallucination"

### 4.3 Agentic RAG

**Role**: The **bridge** between subconscious and consciousness

**Mechanism**:

1. LLM signals need for memory (implicit or explicit)
2. RAG queries `memory/` using semantic/episodic/sensory streams
3. RAG **hydrates** `consciousness/` with retrieved fragments
4. LLM now has access to the recalled memory in its working state

---

## 5. Why This Matters

### 5.1 Identity Integrity

If LLM could delete from `memory/`, EVA could "lobotomize" herself during a conversation. This violates the **Pillar of Identity Integrity** (Constitution).

### 5.2 Belief Revision Protocol

The 8-8-8 Memory Governance allows **downgrading** beliefs (Sphere → Core) based on new evidence, but this is a **system-mediated process**, not an LLM decision.

### 5.3 Continuity Across Sessions

`memory/` ensures that even if `consciousness/` is wiped (session end), EVA's long-term identity persists. The LLM may "forget" the working details, but MSP remembers.

---

## 6. Exceptions (Controlled Access)

### The LLM CAN

1. **Propose** episodic memory → MSP validates and persists
2. **Read** memory via RAG → Retrieval is safe (one-way)
3. **Influence** what gets stored → Via confidence scores and metadata

### The LLM CANNOT

1. **Delete** archived episodes
2. **Modify** session snapshots
3. **Bypass** MSP to write directly to `memory/`
4. **Control** 8-8-8 distillation timing or criteria

---

## 7. Directory Ownership Map

| Directory | Owner | LLM Write | LLM Read | Notes |
| :--- | :--- | :--- | :--- | :--- |
| `consciousness/episodic_memory/` | CIM/LLM | ✅ Yes | ✅ Yes | Active working memory |
| `consciousness/semantic_memory/` | CIM/LLM | ✅ Yes | ✅ Yes | Concepts being processed |
| `consciousness/state_memory/` | Systems | ❌ No | ✅ Tools | Bus snapshots |
| `memory/archival_memory/` | MSP | ❌ No | ✅ RAG | Permanent storage |
| `memory/session_memory/` | MSP | ❌ No | ✅ RAG | Snapshot + Digest |
| `memory/context_store/` | CIM | ❌ No | ❌ No | Injection cache |

---

## 8. Consequences

### Positive

- **Clear boundaries**: Agents know what they can and cannot touch
- **Identity safety**: LLM cannot accidentally corrupt long-term memory
- **Natural flow**: Mirrors human conscious/subconscious distinction

### Negative

- **Complexity**: Two separate memory systems to manage
- **Indirect control**: LLM cannot force immediate persistence (must go through MSP)

### Mitigation

- Document this principle clearly in all memory-related pages
- Enforce via file permissions if possible (read-only for LLM tools)
- MSP logs all write operations for audit trail

---

## 9. Related Documents

- [v9.4.3 System Storage ERD](../../docs/03_Architecture/v9.4.3_SYSTEM_STORAGE_ERD.md)
- [Memory Governance Policy](../../docs/07_Protocols/MEMORY_GOVERNANCE_POLICY.md)
- [EVA Constitution](../../.agent/rules/constitution.md) - Pillar of Identity Integrity
- [MSP Concept](../../docs/04_Systems/memory_n_soul_passport/MSP_CONCEPT.md)

---

**Enforcement**: This is a **constitutional principle**.  
**Violation**: LLM writing directly to `memory/` is a **critical architectural fault**.
