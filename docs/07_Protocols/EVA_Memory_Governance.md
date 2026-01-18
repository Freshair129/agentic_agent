# Memory Governance Policy (v9.4.3)
>
> **Status**: Canonical / Normative Policy
> **Scope**: Memory Promotion, Decay, and Conflict Resolution

เอกสารฉบับนี้กำหนดกฎเกณฑ์ที่ MSP (Memory & Soul Passport) ใช้ในการกำกับดูแลความจำของ EVA เพื่อให้มั่นใจในความปลอดภัย (Safety) และความเสถียรของตัวตน (Identity Stability)

---

## 1. Domain-Based Policy Table

| Domain | Promotion Threshold | Decay Rate | Conflict Handling | Authority |
| :--- | :--- | :--- | :--- | :--- |
| **Safety** | User Confirmation Only | Very Slow | No Overwrite (Flag Conflict) | MSP Only |
| **Identity** | High Frequency (8+ Hits) | Slow | Mark as `Contested` | User + MSP |
| **Knowledge** | Moderate (3+ Hits) | Moderate | Auto-Update (Latest Truth) | MSP |
| **Contextual** | Session Only | Fast | Ignore / Drop | MSP |
| **Meta** | Distillation Only | Slow | Review Needed | MSP |

---

## 2. Epistemic Transition Logic

การเปลี่ยนสถานะพุทธิปัญญา (Confidence Level) ถูกควบคุมโดย MSP ตาม Logic ดังนี้:

### 2.1 Confirmation Loop

- ข้อมูลใหม่จะเริ่มต้นที่ `Hypothesis`
- เมื่อมีการบันทึกซ้ำใน Core Memory และไม่มีความขัดแย้ง จะถูกโปรโมทเป็น `Confirmed`
- เฉพาะข้อมูล `Confirmed` เท่านั้นที่มีสิทธิ์ถูกสกัดเป็น Sphere Memory (Wisdom)

### 2.2 Conflict Resolution (Belief Revision)

- เมื่อข้อมูลใหม่ขัดแย้งกับข้อมูลเดิมในฐานข้อมูล:
    1. ลดค่า Confidence ของข้อมูลเดิม
    2. ทำเครื่องหมายข้อมูลใหม่เป็น `Contested`
    3. หากความขัดแย้งเกิดขึ้นซ้ำในข้อมูลระดับ Sphere: **Execute Sphere → Core Downgrade**

---

## 3. Storage Constraints

- **Single Writer Rule**: เฉพาะ MSP เท่านั้นที่มีสิทธิ์เขียนหรือแก้ไขข้อมูลในหมวด `memory/` (LTM)
- **No Direct LLM Write**: LLM ไม่สามารถสั่งแก้ไขความจำในอดีตได้โดยตรง (ต้องผ่านการสรุปและโปรโมทตามรอบ 8-8-8 หรือผ่านคำสั่งยืนยันจากผู้ใช้ตาม Policy)
- **Domain Traceability**: ข้อมูลทุกหน่วยใน LTM ต้องระบุ Domain และ Epistemic State

---
*Created for EVA v9.4.3 Governance*
