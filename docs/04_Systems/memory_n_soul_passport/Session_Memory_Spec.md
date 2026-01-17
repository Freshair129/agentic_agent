# Session Memory Specification (v9.4.3)
>
> **Status**: Canonical / Final
> **Version**: 9.4.3
> **Philosophy**: "Data needs a Snapshot; Search needs a Map."

เอกสารฉบับนี้กำหนดมาตรฐานการจัดเก็บความจำราย Session สำหรับ EVA v9.4.3 โดยเปลี่ยนจากเพียงการทำสรุปเนื้อหา มาเป็นการทำ **"Snapshot & Master Index"** เพื่อความสมบูรณ์ของข้อมูลและประสิทธิภาพในการสืบค้น (Retrieval Optimization)

---

## 🏗️ 1. The Dual-Role Architecture

ในเวอร์ชัน 9.4.3 ระบบ **Session Memory** ทำหน้าที่สองอย่างควบคู่กัน:

1. **The Raw Snapshot (Body)**: การ Copy ทั้งโฟลเดอร์ `agent/consciousness/` ไปเก็บไว้ทั้งหมด (Episodic, Semantic, Sensory, State) เพื่อให้ข้อมูลในขณะเกิดเหตุไม่สูญหาย
2. **The Session Digest (Map/Index)**: ไฟล์ Markdown สรุปใจความสำคัญที่ทำหน้าที่เป็น **"ดัชนีและตัวจุดชนวนการค้นหา" (Search Trigger)** เพื่อให้ LLM หรือ Agentic RAG สแกนไฟล์นี้เพียงไฟล์เดียวแทนการกวาดข้อมูลดิบทั้งหมด

---

## 📂 2. Storage Structure

### Path Mapping

- **Source**: `agent/consciousness/`
- **Destination**: `agent/memory/session_memory/{session_id}/`

### Folder Contents

```text
session_memory/{session_id}/
├── snapshot/               # Raw copy of the entire consciousness folder
│   ├── episodic/
│   ├── semantic/
│   └── ... 
└── {session_id}_DIGEST.md  # The Master Index & Summary (Search Trigger)
```

---

## 📝 3. Digest Specification (The Search Trigger)

ไฟล์สรุปต้องประกอบด้วยหัวข้อมาตรฐานเพื่อให้ระบบ RAG สามารถประมวลผลได้รวดเร็ว:

### 3.1 Naming Convention

`SES{n}_{DevID}_SP{x}C{y}_DIGEST.md`

### 3.2 Structure & Metadata

```markdown
# Session Digest: {session_id}
> **Status**: {session_status} | **Objective**: {session_objective}
> **Motto**: "{session_motto}"

## � Manifest (Index of Snapshot)
- **Episodes**: EVA_EP{start} - EVA_EP{end}
- **Vitals Snapshot**: [Link to snapshot/state/...]
- **Sensory Logs**: {count} entries captured

## 🧠 Semantic Summary (The RAG Trigger)
หมวดหมู่นี้ใช้สำหรับการ "สแกนเร็ว" โดยไม่ต้องอ่าน Log ทั้งหมด:
- **Core Intent**: วัตถุประสงค์หลักที่ผู้ใช้ต้องการในครั้งนี้
- **Key Outcomes**: ความสำเร็จหรือข้อมูลสำคัญที่สกัดได้
- **Emotional Arc**: สรุปสภาวะอารมณ์รวมของ Session (H9 Compression)

## ⚡ Knowledge Triggers
รายการคำสำคัญหรือเหตุการณ์ที่ควรใช้ RAG ดึงข้อมูลดิบใน Snapshot มาอ่านเพิ่ม:
- [Topic A]: {Summary} -> Trigger reference: [EP_NN]
- [Topic B]: {Summary} -> Trigger reference: [EP_MM]

## 🔄 8-8-8 Synthesis Readiness
- [ ] Cleaned
- [ ] Summarized
- [ ] Indexed
- [ ] Relational Map Created
```

---

## ⚡ 4. Retrieval Strategy

เพื่อป้องกันการ "กวาดหา" (Sweep Search) ที่สิ้นเปลือง Token:

1. **RAG Scan**: Agentic RAG จะสแกนเฉพาะไฟล์ `*_DIGEST.md` ทั้งหมดใน `session_memory/`
2. **Trigger Hit**: เมื่อพบ Digest ที่ตรงกับ Context ปัจจุบัน ระบบจะใช้ **Trigger reference** เป็น "กุญแจ" เข้าไปเปิดไฟล์เจาะจงในโฟลเดอร์ `snapshot/`
3. **Deep Recall**: LLM จะได้รับเฉพาะส่วนของความจำดิบที่มีความสำคัญผ่านการชี้เป้าของ Digest

---

## 🔄 5. Lifecycle & 8-8-8 Handover

- **Trigger**: เมื่อ Session จบลง (Command/Timeout) -> MSP รัน `snapshot()` และ `generate_digest()`
- **Consolidation**: เมื่อสะสมครบ 8 Sessions -> ระบบจะใช้ Digest ทั้ง 8 เป็นวัตถุดิบหลักในการสร้าง **Core Memory**

---

<!-- markdownlint-disable-next-line MD036 -->
**Directed by "The Human Algorithm" v9.4.3 Principles**
