# Consciousness Domain (Awareness Domain) Structure

- **Status**: Canonical / EVA v9.4.3
- **Role**: Active Awareness, Working Memory, and Interface Layer.
- **Location**: `/agent/consciousness/`

---

## 1. Core Architecture

Consciousness ใน EVA คือ "Awareness Domain" ซึ่งแยกออกจาก "Implementation Domain" (Capabilities) อย่างเด็ดขาด เพื่อความเสถียรและความปลอดภัยของระบบ

### 📂 Directory Structure Overview

| Directory | Purpose | 8-8-8 Tier |
|:---|:---|:---:|
| **`context_storage/`** | เก็บประวัติ Context ของแต่ละ Turn (Step 1-3) ในรูปแบบ Markdown | Session (Tier 1) |
| **`episodic_memory/`** | ที่พักข้อมูล Episode ที่กำลัง Active ใน Session ปัจจุบัน (ก่อนส่งเข้า MSP Archive) | Session (Tier 1) |
| **`indexes/`** | เก็บ Salience Maps, Session Manifests และ Epistemic Markers | Session (Tier 1) |
| **`state_memory/`** | เก็บ Snapshot ล่าสุดของ Bio/Psych/Qualia State (Authoritative Snapshot) | Aware Layer |
| **`semantic_memory/`** | Interface ตัวกลางสำหรับสืบค้นความจำเชิงความหมาย (Working Vector Buffer) | Aware Layer |
| **`sensory_memory/`** | Interface สำหรับ Sensory Stream ข้อมูลดิบก่อนการสกัดเป็น Qualia | Aware Layer |
| **`tools/`** | **Shortcuts (.lnk)** ไปยังเครื่องมือหลักของระบบ (e.g. `sync_biocognitive_state`) | Interface |
| **`skills/`** | **Shortcuts (.lnk)** ไปยังฟังก์ชันเสริมที่ LLM สามารถเรียกใช้ได้ | Interface |
| **`services/`** | **Shortcuts (.lnk)** ไปยัง OS Services (e.g. VectorDB, Archivist) | Interface |

---

## 2. Key Principles

### 2.1 Separation of Concerns

- `/consciousness/` จะบรรจุเพียง **Interface** และ **Active State** เท่านั้น
- Logic และการประมวลผล (Code) ทั้งหมดต้องอยู่ใน `/capabilities/`

### 2.2 Short-Term Persistence (Tier 1)

- ข้อมูลใน `/consciousness/` จะมีความคงทนเพียงชั่วคราว (Ephemeral)
- ข้อมูลที่สำคัญจะได้รับการ "บีบอัด" และ "ย้าย" เข้าสู่ `/memory/archival_memory/` ผ่านทาง **MSP Engine** เมื่อจบ Turn หรือ Session

### 2.3 The Aware Interface

- LLM มีสิทธิ์ในการอ่าน (Read) และเขียน (Write) ในพื้นที่นี้เพื่อรักษาความต่อเนื่องของความคิดและความรู้สึกในระหว่างการสนทนา
- ไฟล์ในพื้นที่นี้ถูกออกแบบมาให้อยู่ในรูปแบบที่ LLM เข้าถึงได้ง่าย (Markdown, JSON)
