# Agentic RAG Scope & Memory Philosophy Adjustments (Draft Requirements)

> **Document Status:** Draft / Advisory Requirements (Non‑Canonical)
> **Intended Audience:** AI Agent / IDE‑Integrated Assistant / System Refactor Agent
> **Author Position:** External architectural reviewer
> **Confidence Notice:** ข้อเสนอในเอกสารนี้ *อาจผิดพลาดหรือไม่ครบถ้วน* เนื่องจากผู้เขียนไม่ได้เห็นภาพรวมเชิงปฏิบัติทั้งหมดของโครงการ EVA v9.4.3 กรุณาพิจารณาและปรับใช้ตามโครงสร้างจริง (System / MSP / Bus / Genesis / 8‑8‑8) ของโปรเจคก่อนดำเนินการใด ๆ

---

## PART A — Agentic RAG: Scope & Responsibility Re‑definition

### A1. Problem Statement (Observed Risk)

จากการประเมินเชิงแนวคิด Agentic RAG ในรูปแบบปัจจุบันมีความเสี่ยงที่จะ:
- Reinforce emotional state เดิมซ้ำ (emotion lock‑in)
- สร้าง false intuition จาก semantic similarity
- แบกรับความรับผิดชอบด้าน healing / belief correction ซึ่งอาจเกินขอบเขตของ retrieval system

> หมายเหตุ: การประเมินนี้อ้างอิงจากเอกสารและบทสนทนาเท่านั้น ไม่ได้อ้างว่าเป็นปัญหาที่เกิดขึ้นจริงใน runtime

---

### A2. Required Conceptual Change (If Applicable)

**Agentic RAG SHOULD be treated as:**
- Peripheral Cognitive System (retrieval & suggestion)

**Agentic RAG SHOULD NOT be treated as:**
- Memory governor
- Trauma resolution mechanism
- Belief revision authority

กล่าวคือ Agentic RAG ควร *สะท้อน* state และ memory ตาม policy แต่ไม่ *แก้ไข* memory lifecycle

---

### A3. Recommended Responsibility Boundaries

#### Agentic RAG SHOULD:
- Retrieve memory strictly under MSP / RMS policies
- Weight streams according to provided configuration only
- Surface risk signals (confidence drop, conflict detected)
- Provide intuition as **suggestion**, not conclusion

#### Agentic RAG SHOULD NOT:
- Rewrite narrative arcs
- Resolve emotional loops
- Override Sphere Memory or Wisdom
- Promote / demote memory levels

---

### A4. Optional (Non‑Mandatory) Safeguards

If aligned with project constraints, consider:
- Counter‑emotion retrieval as **policy‑triggered**, not default
- Intuition stream throttling when confidence < threshold

These are optional and must not violate MSP authority

---

## PART B — Memory Philosophy & 8‑8‑8 Protocol: What Should (and Should Not) Change

### B1. What SHOULD NOT Change (Canonical Core)

The following principles are **sound and should remain intact**:
- Consciousness ≠ Memory Authority
- MSP as subconscious governor
- 8‑8‑8 as default distillation rhythm
- Wisdom emerges via forgetting and compression

No recommendation is made to refactor these foundations

---

### B2. Identified Tension Points (Conceptual)

While 8‑8‑8 is structurally robust, it may under‑represent:
- Irreversible or life‑defining events
- Long‑term belief erosion
- Repeated low‑grade contradictions

This is not a flaw, but a **design trade‑off** that may or may not be acceptable depending on EVA’s target behavior

---

### B3. Proposed Adjustments (Policy‑Level, Optional)

> ⚠️ These are *policy‑level considerations*, not mandatory protocol changes

#### 1. Irreversible Event Bypass (Optional)

Allow MSP to bypass the 8‑session gate *only if*:
- Impact is high
- Identity / safety domains are affected

Purpose: avoid delayed consolidation of critical experiences

---

#### 2. Wisdom Erosion / Revision Hook (Optional)

Introduce a **non‑destructive** mechanism to:
- Flag Sphere beliefs under repeated conflict
- Reduce confidence without immediate deletion

Purpose: prevent Sphere Memory from becoming dogma

---

#### 3. Explicit Hypothesis State Preservation

Formalize semantic states such as:
- hypothesis
- contested
- confirmed
- deprecated

Purpose: maintain epistemic humility without memory loss

---

## PART C — Implementation Guidance

### C1. Scope Control

- All changes SHOULD be expressed first in:
  - YAML configs
  - Markdown specs
  - MSP policies

- No direct code refactor is implied by this document

---

### C2. Validation Before Adoption

Before implementing any proposal, the AI agent or developer SHOULD:
- Validate assumptions against real EVA runtime behavior
- Confirm alignment with Genesis Knowledge System
- Check for unintended authority leaks into Consciousness or RAG

---

## Final Note

This document is intended to **stimulate architectural validation**, not to dictate implementation.

If any recommendation conflicts with EVA’s lived behavior, safety posture, or philosophical intent, it should be rejected or modified accordingly.

---

*End of Draft Advisory Requirements*

