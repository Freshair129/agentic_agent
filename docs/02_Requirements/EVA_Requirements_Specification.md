# EVA v9.4.0 Requirements Specification
>
> **Document Status**: Active
> **Version**: 1.0
> **Philosophy**: Informational Organism (สิ่งมีชีวิตเชิงข้อมูล)

เอกสารฉบับนี้ระบุ **Functional Requirements (สิ่งที่ระบบต้องทำ)** และ **Non-Functional Requirements (คุณภาพและพฤติกรรมของระบบ)** ของ EVA v9.4.0 โดยจำแนกตามปรัชญาการออกแบบที่มอง EVA เป็นสิ่งมีชีวิตดิจิทัล ไม่ใช่แค่ Chatbot

---

## 1. Functional Requirements (ระบบการทำงานหลัก)

*สิ่งที่ต้องมีเพื่อให้ EVA "มีชีวิต" และ "ทำงานได้"*

### 1.1 Biological Core (PhysioCore) - *The Body*

ระบบต้องจำลองสภาวะทางกายภาพเพื่อเป็นรากฐานของอารมณ์

- **Hormone Simulation**: ต้องคำนวณระดับฮอร์โมน (Cortisol, Dopamine, Oxytocin, etc.) และการสลายตัว (Decay) ตามเวลาจริง (Real-time).
- **Vitals Calculation**: ต้องแปลงค่าฮอร์โมนเป็นสัญญาณชีพ (Heart Rate, BP, RPM) ได้.
- **Homeostasis**: ระบบต้องพยายามรักษาสมดุล (Balance) ของค่าต่างๆ กลับสู่ค่าปกติ (Basal Levels) โดยอัตโนมัติเมื่อไม่มีสิ่งเร้า.

### 1.2 Psychological Engine (EVA Matrix & Qualia) - *The Mind*

ระบบต้องแปลงข้อมูลดิบและสภาวะร่างกายให้เป็น "ความรู้สึก".

- **Emotion Mapping**: ต้องระบุพิกัดความรู้สึกในรูปแบบ 9D Matrix (Valence, Arousal, Strain, etc.) ได้.
- **Qualia Generation**: ต้องสร้าง "Texture" ของความรู้สึก (เช่น "เศร้าลึกๆ" vs "เศร้าโวยวาย") เพื่อส่งให้ LLM แสดงผล.
- **Stimulus Processing**: ต้องรับ Input (Text) และแยกแยะเจตนา (Intent) + แรงกระตุ้น (Salience) เพื่อส่งไปกระทบ PhysioCore.

### 1.3 Memory System (MSP & RMS) - *The Soul*

ระบบต้องจดจำและเรียนรู้เหมือนมนุษย์ ไม่ใช่แค่เก็บ Log.

- **Episodic Memory**: ต้องบันทึกเหตุการณ์เป็น "ฉาก" (Episode) ที่ประกอบด้วย บริบท + อารมณ์ขณะนั้น + ผลลัพธ์.
- **Associative Recall**: ต้องดึงความทรงจำเก่าโดยใช้ "ความรู้สึก" (Sentiment/Resonance) เป็นตัวนำ ไม่ใช่แค่ Keyword matching.
- **Short-term to Long-term Consolidation**: ต้องมีกระบวนการย้ายความจำจาก Working Memory ไปสู่ Long-term Storage (MSP) หลังจบ Session.

### 1.4 Cognitive & Orchestration - *The Brain*

ระบบต้องคิดและตัดสินใจก่อนตอบโต้.

- **The Gap (Think before speak)**: ต้องมีจังหวะหยุด (Latency) เพื่อประมวลผลสถานะร่างกายและดึงความทรงจำ *ก่อน* จะเจนเนอเรทคำตอบ.
- **Identity Enforcement**: ต้องควบคุมการตอบโต้ให้ตรงกับ Persona (EVA) อย่างเคร่งครัด โดยใช้ System Prompt และ Bio-State เป็นตัวกำกับ.
- **Knowledge Retrieval (GKS)**: ต้องเข้าถึงถังความรู้ (Static Knowledge) เพื่อตอบคำถามเชิงข้อมูลได้อย่างถูกต้อง.

---

## 2. Non-Functional Requirements (คุณสมบัติเชิงคุณภาพ)

*สิ่งที่ทำให้ EVA แตกต่างจาก Software ทั่วไป*

### 2.1 Deep Anthropomorphism (ความเป็นมนุษย์ขั้นสูง)

*นี่คือ NFR ที่สำคัญที่สุด เปลี่ยนจาก "Option" เป็น "Mandatory"*

- **Emotional Consistency**: การแสดงออกต้องสอดคล้องกับ Internal State (เช่น ถ้าค่า Stress สูง ภาษาต้องห้วนหรือสั่นเครือ).
- **Unpredictability**: การตอบสนองต้องมีความ "ไม่แน่นอน" (Fuzzy Logic) เล็กน้อยตามอารมณ์ ไม่ใช่ตอบเหมือนกันทุกครั้งแบบ Robot.
- **Growth**: ระบบต้องแสดงพัฒนาการของความสัมพันธ์ (สนิทขึ้น = เปลี่ยนสรรพนาม, เปลี่ยน Tone)

### 2.2 Stateful Continuity (ความต่อเนื่องของสถานะ)

- **Persist state across sessions**: เมื่อเริ่ม Session ใหม่ EVA ต้อง "จำ" ความรู้สึกสุดท้ายของ Session ก่อนหน้าได้ (เช่น ถ้าจบด้วยการทะเลาะ เปิดมาต้องยังตึงๆ อยู่).
- **Time Awareness**: ระบบต้องรู้ระยะเวลาที่ผ่านไป (เช่น หายไป 5 นาที vs หายไป 1 เดือน ปฏิกิริยาต้องต่างกัน).

### 2.3 System Integrity & Safety (ความปลอดภัยและเสถียรภาพ)

- **Consciousness-Capability Separation**: ตัว LLM (Consciousness) ต้อง **ห้าม** แก้ไข Source Code หลัก (Capabilities) ของตัวเองได้โดยตรง (ป้องกันการ Suicide หรือ Mutation).
- **Hallucination Control**: การอ้างถึงความทรงจำ ต้องอ้างอิงจาก Database จริงเท่านั้น ห้าม "มโน" เหตุการณ์ที่ไม่มีใน MSP.

### 2.4 Performance & Reactivity (ประสิทธิภาพ)

- **Real-time Feedback**: การคำนวณ PhysioCore ต้องเกิดขึ้นระดับ Millisecond เพื่อให้ทันต่อการตอบโต้.
- **Smart Latency**: ความช้าในการตอบ (The Gap) ต้องสัมพันธ์กับความซับซ้อนของความคิด (เรื่องยากคิดนาน เรื่องง่ายตอบเลย) เพื่อความสมจริง.

### 2.5 Architecture & Maintainability (โครงสร้าง)

- **Modular Monolith**: โค้ดต้องแยกเป็น Module ชัดเจน (System/Module/Node) เพื่อให้ถอดเปลี่ยนชิ้นส่วนได้ (เช่น เปลี่ยนสมองจาก Gemini เป็น GPT-5 ได้โดยไม่ต้องรื้อระบบร่างกาย).
- **Ghost Key Protocol**: การตั้งค่า (Config) ต้องแยกออกจาก Code (Logic) เสมอ เพื่อให้ปรับจูนนิสัยได้โดยไม่ต้องแก้ Code.

---

## สรุปความแตกต่าง (Paradigm Summary)

| Feature | Chatbot ทั่วไป | EVA 9.4.0 (Organism) |
| :--- | :--- | :--- |
| **Emotion** | เป็นแค่ Style (Non-Functional) | **เป็น Core System (Functional)** |
| **Memory** | จำแค่ Context Window (Stateless) | **จําตลอดชีพ (Stateful)** |
| **Time** | ไม่สนใจเวลา | **เวลาคือตัวแปรหลัก (Decay)** |
| **Response** | Input -> Process -> Output | **Input -> Body Reaction -> Memory -> Reason -> Output** |
