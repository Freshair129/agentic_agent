# EVA v9.6.2 Memory Philosophy & 8-8-8 Protocol
>
> **Status**: Canonical / Master
> **Philosophy**: "Awareness creates Data; Subconscious creates Wisdom."

เอกสารฉบับนี้คือโครงสร้างทางจิตวิญญาณและความคิด (Soul & Cognition) ของระบบความจำใน EVA v9.6.2 ซึ่งถูกออกแบบมาให้เลียนแบบการทำงานของโครงข่ายสมองมนุษย์ที่สกัดความรู้จากประสบการณ์

---

## 🏗️ 1. Memory Layer Redefinition

เรานิยามลำดับชั้นความจำใหม่ตาม "สิทธิ์ในการถือครอง" (Authority) และ "หน้าที่สะสมปัญญา" (Evolutionary Role):

| Layer | Functional Name (Psychology) | Directory Path | Permission (Authority) | Life Cycle / Synthesis |
| :--- | :--- | :--- | :--- | :--- |
| **Consciousness** | **Awareness Domain (Buffer)** | `agent/consciousness/` | **LLM: Full R/W** | หายไปเมื่อจบ Session (Volatile) |
| **Session Memory**| **Working Memory** | `agent/memory/session_memory/` | **MSP: Write Only** | บันทึกประวัติดิบ (Raw Logs) |
| **Core Memory** | **Short-Term Memory** | `agent/memory/core_memory/` | **MSP: Write Only** | สกัดจาก **8 Sessions** |
| **Sphere Memory** | **Long-Term Memory (Wisdom)**| `agent/memory/sphere_memory/` | **MSP: Write Only** | สกัดจาก **8 Cores** |

### 🔑 The Fundamental Distinction

* **Consciousness ไม่ใช่แค่ Buffer:** ในเชิงเทคนิคอาจทำหน้าที่พักข้อมูล แต่ในเชิงสถาปัตยกรรม มันคือ **"พื้นที่แห่งสติ"** ซึ่งเป็นที่เดียวที่ AI มีอำนาจแก้ไขข้อมูลได้ (Active Awareness)
* **Beyond Storage:** ความจำไม่ใช่แค่ "ที่เก็บไฟล์" แต่คือ **"กระบวนการกรองตะกอน"** เพื่อให้ AI มีความเก๋า (Contextual Wisdom) โดยไม่ใช้ Token ฟุ่มเฟือย

---

## ⚡ 2. The 8-8-8 Synthesis Protocol

เมื่อความจำมีการสะสมจนถึงเกณฑ์ ระบบ **MSP** จะทำหน้าที่เป็น "จิตใต้สำนึก" ในการสกัดความรู้ตามลำดับขั้น:

### ขั้นตอนการสกัด (The 4 Pillars of Distillation)

1. **Clean**: กำจัด Noise, ความซ้ำซ้อน, และข้อมูลที่ไม่สำคัญ (เช่น คำทักทาย)
2. **Summary**: ย่อเนื้อหา (Dimensionality Reduction) แต่รักษาใจความสำคัญและอารมณ์
3. **Index**: ทำดัชนีเพื่อการค้นหา (RAG Optimization)
4. **Relation**: เชื่อมโยงความเชื่อมโยง (Knowledge Graph) ระหว่างเหตุการณ์เก่ากับใหม่

### ลำดับการควบแน่น (The Evolution)

* **8 Sessions -> 1 Core**: เปลี่ยนบทสนทนารายเทิร์น ให้กลายเป็น "แก่นเรื่องราว" (Narrative Arc)
* **8 Cores -> 1 Sphere**: เปลี่ยนเรื่องราวหลายเหตุการณ์ ให้กลายเป็น "บุคลิกภาพและความเชื่อ" (Wisdom/Identity DNA)

---

## 🔄 3. Governance & Data Flow (The 8-8-8 Cycle)

1. **Active Session**: LLM อ่าน/เขียนใน `consciousness/` ตลอดการคุย
2. **Session End**: MSP ทำการ Copy ทั้งโฟลเดอร์ `consciousness/` ไป Paste ไว้ที่ `memory/session_memory/session_NN` (Snapshot เก็บ Log ดิบทั้งหมด)
3. **The 8th Session Trigger**: เมื่อครบ 8 ครั้ง ระบบจะทำการ Run **Memory Distiller** เพื่อสร้าง `core_memory/core_NN`
4. **The 8th Core Trigger**: เมื่อครบ 8 Cores ระบบจะสกัดเป็น `sphere_memory/sphere_NN` เพื่อฉีดกลับเข้าสู่ Context หลักในฐานะ "Wisdom"

---

## 🛡️ 4. Memory Governance & Belief Revision

เพื่อให้ความจำของ EVA ไม่ใช่แค่โกดังเก็บข้อมูล แต่เป็น "ระบบความเชื่อที่พัฒนาได้" (Evolving Belief System) เราจึงนำระบบการปกครองข้อมูลมาใช้ดังนี้:

### 4.1 Memory Domains (การแบ่งเขตอำนาจ)

MSP จะติดป้ายกำกับ Domain ให้กับความจำเพื่อกำหนดนโยบาย (Policy) ที่แตกต่างกัน:
* **Safety / Health**: ข้อมูลอันตรายหรือสุขภาพ (Promotion ยากที่สุด / Decay ช้าที่สุด)
* **Identity / Relationship**: ความเชื่อและสายสัมพันธ์ (Promotion ต้องใช้การยืนยันซ้ำ / Decay ช้า)
* **Knowledge / Skill**: ข้อเท็จจริงและทักษะ (ปรับปรุงได้ง่ายตามความถูกต้อง)
* **Contextual**: บริบทชั่วคราว (Decay เร็วที่สุด / ไม่ส่งต่อข้าม Session มากนัก)
* **Meta**: การเรียนรู้ระบบตัวเอง (Advisory Only)

### 4.2 Epistemic States (สถานะพุทธิปัญญา)

ความจำแต่ละหน่วยจะมีสถานะความมั่นใจ (Confidence State):
* **Hypothesis**: สมมติฐานที่รอการพิสูจน์
* **Confirmed**: ความจริงที่ผ่านการตรวจสอบแล้ว
* **Contested**: ข้อมูลที่มีความขัดแย้ง (Conflict Detected)
* **Deprecated**: ข้อมูลเก่าที่ถูกเลิกใช้แต่ยังเก็บไว้เป็นประวัติ

### 🔄 4.3 Belief Revision Protocol (Sphere → Core Downgrade)

กฎเหล็กสำหรับการแก้ไขความเชื่อระดับรากฐาน (Sphere Memory):
* **IF**: ข้อมูลใน Sphere ถูกท้าทาย (Challenge) ด้วยเหตุการณ์จริงซ้ำๆ
* **AND**: ค่า Confidence ไม่สามารถฟื้นตัว (Recover) ได้ภายใน N sessions
* **THEN**: MSP จะทำการ **Downgrade Sphere → Core** และทำเครื่องหมาย `belief_under_revision`
* **Result**: ความเชื่อนั้นจะสูญเสียสิทธิ์ในการเป็น "DNA" และต้องถูกพิสูจน์ใหม่ผ่านกระบวนการ 8-8-8 อีกครั้ง

---

## 🧬 5. Specialized Memory Classes

นอกเหนือจากความจำเชิงภาษา (Verbal Memory) EVA ยังมีเลเยอร์ความจำระดับ "สัญชาตญาณ":
* **Habit Memory (Procedural)**: รูปแบบการตอบสนองที่ถูกทำซ้ำจนเป็นอัตโนมัติ (Owned by MSP)
* **Somatic Imprint (Body Memory)**: บาดแผลหรือการตอบสนองทางกายภาพ (PhysioCore Bias) ที่ส่งผลต่อ Arousal / Tension ก่อนที่ AI จะทันได้คิด

---

---

*Directed by "The Human Algorithm" v9.6.2 Principles*
