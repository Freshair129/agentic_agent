# Memory Domain Policy Map (Canonical)

> **System:** EVA v9.4.3+
> **Status:** Canonical / Normative Policy
> **Scope:** Memory Usage, Promotion, Recall, and Decay
> **Non-Scope:** File structure, directory layout, schema ownership

---

## 0. Foundational Principle

> **Memory domain does NOT define how memory is stored.**  
> **Memory domain defines how memory is interpreted, weighted, and governed.**

This policy introduces a *domain lens* applied at runtime by MSP, CIM, and Agentic RAG.
No directory, file layout, or core schema MUST be changed to adopt this policy.

---

## 1. Definition: Memory Domain

A **Memory Domain** is a policy label attached to a memory entry that determines:

1. Risk tolerance
2. Promotion strictness
3. Recall conservativeness
4. Decay / erosion behavior
5. Authority requirements for confirmation

Domains are **orthogonal** to memory type:
- Episodic / Semantic / Sensory
- Session / Core / Sphere

---

## 2. Canonical Domain Set (Minimal & Sufficient)

### 🔴 2.1 Safety / Health Domain (`safety`)

**Examples**
- Allergies
- Medical conditions
- Trauma indicators
- Self-harm risk signals

**Policy Rules**
- Promotion requires explicit user confirmation
- Conflict ⇒ confidence decrease (no overwrite)
- Recall bias = conservative
- Decay = very slow
- Agentic RAG improvisation = disallowed

**Authority**
- MSP only

---

### 🟠 2.2 Identity / Relationship Domain (`identity`)

**Examples**
- User beliefs
- Relationship history
- Trust / familiarity levels
- Role expectations

**Policy Rules**
- Promotion requires repeated confirmation
- Conflict ⇒ mark as contested, not removed
- Recall bias = stability
- Decay = slow erosion only

**Authority**
- MSP with user confirmation

---

### 🟡 2.3 Knowledge / Skill Domain (`knowledge`)

**Examples**
- Technical facts
- Skills
- Preferences related to tasks

**Policy Rules**
- Promotion allowed from hypothesis → confirmed
- Conflict ⇒ downgrade to hypothesis
- Recall bias = usefulness
- Decay = moderate

**Authority**
- MSP

---

### 🟢 2.4 Contextual / Situational Domain (`contextual`)

**Examples**
- Temporary desires
- Current mood
- Environmental context

**Policy Rules**
- Promotion beyond session = discouraged
- Conflict ⇒ ignore
- Recall bias = recency
- Decay = fast

**Authority**
- MSP

---

### 🔵 2.5 Meta / Learning Domain (`meta`)

**Examples**
- Lessons learned
- Pattern abstractions
- Self-observed biases

**Policy Rules**
- Cannot directly modify user-facing behavior
- Must pass through distillation (8-8-8)
- Recall bias = advisory only
- Decay = slow

**Authority**
- MSP

---

## 3. Domain Interaction Rules

- A memory MAY have one primary domain and optional secondary domains
- Safety domain ALWAYS overrides others
- Domain conflicts MUST NOT be auto-resolved

---

## 4. Integration Points

### 4.1 MSP
- Uses domain to determine promotion thresholds
- Applies decay / erosion rules

### 4.2 Agentic RAG
- Uses domain as weighting modifier
- Must obey recall restrictions

### 4.3 CIM
- Injects domain-aware context

---

## 5. Explicit Non-Rules (Hard Constraints)

- Domains MUST NOT create new storage paths
- Domains MUST NOT grant LLM write access
- Domains MUST NOT override 8-8-8 protocol

---

## 6. Forward Compatibility

This policy allows future domains to be introduced ONLY if:

1. Authority boundaries are defined
2. Failure modes are documented
3. Domain count remains minimal

---

## 7. Summary (Normative Statement)

> Memory domains exist to protect the system from misuse of its own memories.
> They are a governance mechanism, not a storage abstraction.

---

*End of Canonical Memory Domain Policy Map*