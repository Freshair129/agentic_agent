# EVA v9.4.3 – Habit & Somatic Imprint Layer (Draft Requirements)

> **Document Status:** Draft / Proposal (Non‑Canonical)
> **Author:** External Architectural Review (Advisory)
> **Confidence Level:** Medium
> **Important Disclaimer:** ข้อเสนอในเอกสารนี้อาจมีความคลาดเคลื่อนหรือไม่สอดคล้องกับภาพรวมทั้งหมดของโครงการ เนื่องจากผู้เขียนไม่ได้เข้าถึงระบบทั้งหมดในเชิงลึก การนำไปใช้ต้องพิจารณาและปรับตามโครงสร้างจริงของโปรเจค EVA v9.4.3

---

## 1. Context & Motivation

จากการทบทวนสถาปัตยกรรม EVA v9.4.3 พบว่าระบบมีความสมบูรณ์สูงในกลุ่มความจำเชิงการรับรู้และอารมณ์ (episodic / semantic / sensory / emotional / implicit) แต่ยังไม่มีการยกระดับความสามารถด้าน **Habit Formation (Procedural Memory)** และ **Somatic Pattern Retention (Body Memory)** ให้เป็น memory class ที่ชัดเจนและถูก govern โดย MSP อย่างเป็นทางการ

ข้อเสนอนี้มีเป้าหมายเพื่อ:
- เพิ่มความต่อเนื่องเชิงพฤติกรรม (behavioral continuity)
- ทำให้ EVA เรียนรู้จาก “สิ่งที่เคยเวิร์ก / เคยเจ็บ” โดยไม่ต้องอาศัยการคิดเชิงภาษาเสมอ
- รักษาปรัชญาหลักของ EVA: *Consciousness does not own memory*

---

## 2. Non‑Goals (สิ่งที่เอกสารนี้ไม่พยายามทำ)

- ไม่เสนอให้ LLM มีสิทธิ์เขียนหรือแก้ไข memory ชั้นล่าง
- ไม่เสนอให้ EVA มี autonomy เชิงร่างกายแบบไม่สามารถควบคุมได้
- ไม่เสนอการเปลี่ยนแปลง 8‑8‑8 Protocol หลัก
- ไม่เสนอการ refactor PhysioCore หรือ EVA Matrix ที่มีอยู่

---

## 3. Proposed New Memory Classes (Conceptual)

### 3.1 Habit Memory (Procedural Equivalent)

**Conceptual Definition:**
Memory class สำหรับ pattern การตอบสนองหรือการกระทำที่ถูก reinforce ซ้ำ ๆ จนกลายเป็น default behavior โดยไม่ต้องผ่าน conscious reasoning ทุกครั้ง

**Candidate Sources (Existing Systems):**
- Reflex Directives (EVA Matrix)
- Skill Invocation History
- Repeated successful interaction patterns

**Characteristics:**
- Non‑verbal
- Triggered by state / pattern, not query
- Read‑only ต่อ Consciousness

**Governance:**
- Owned and persisted by MSP
- Promotion ต้องผ่าน threshold (frequency + confidence + low conflict)

---

### 3.2 Somatic Imprint Memory (Body Memory Equivalent)

**Conceptual Definition:**
Memory class สำหรับ pattern ทางกายภาพหรือภาวะคุกคามที่ส่งผลให้ PhysioCore และ EVA Matrix ตอบสนองเร็วขึ้นหรือแรงขึ้นในอนาคต

**Candidate Sources (Existing Systems):**
- PhysioCore ANS state history
- Trauma flag / threat level
- RMS trauma_store

**Characteristics:**
- Affects baseline (bias), not explicit recall
- Influences arousal / tension before cognition

**Governance:**
- Owned by MSP
- Activation should be throttled and decay‑aware

---

## 4. Integration Constraints (Must Respect Existing Architecture)

- Must not introduce new R/W paths into `consciousness/`
- Must respect System vs Service separation
- Must integrate via MSP or Resonance Bus only
- Must remain compatible with Agentic RAG and CIM

---

## 5. Safety & Control Requirements

- Habit / Somatic memories must be:
  - Domain‑scoped (e.g. safety, trust, health)
  - Reversible or decaying over time
  - Auditable by system logs (not by LLM)

- No direct LLM introspection into raw habit/somatic data

---

## 6. Open Questions for Implementers

- Where should promotion thresholds live? (MSP vs Genesis Knowledge System)
- Should habit formation bypass 8‑8‑8 or be a parallel lane?
- How to prevent over‑generalization of somatic imprints?
- What is the rollback strategy if false positives accumulate?

---

## 7. Recommendation

This document should be treated as a **design exploration artifact**, not an implementation directive. Implementers are strongly encouraged to:
- Validate assumptions against real EVA runtime behavior
- Adjust scope based on system constraints
- Prototype in isolation before integrating into the main memory pipeline

---

*End of Draft Requirements*

