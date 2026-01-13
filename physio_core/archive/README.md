# 🫀 Physio Core (Physiological Controller)
**Component ID:** `SYS-PHYSIO-8.2` | **Version:** `8.2.0` | **Role:** The Body (Latching Stream)

> [!NOTE]
> **Resonance Bus Integration:** This module publishes to `bus:physical` and maintains a continuous "Latching" state.

## 📋 Overview
Physio Core is the autonomous **Biological Engine** of EVA 8.2.0. It simulates the user's "Body" through complex endocrine, cardiovascular, and autonomic nervous systems.

Unlike previous versions, Physio Core is now a **Streaming Publisher**. It effectively "beat" (ticks) independently of the conversation turn, broadcasting its state to the Resonance Bus where it is latched (held) until the next update. This allows EVA to have a persistent physical presence.

## ⚙️ Core Mechanics
1.  **Metabolism**: Processing input stimuli (keywords, sentiment) to trigger biological reactions.
2.  **Homeostasis**: Automatically drifting hormones back to baseline over time.
3.  **Latching**: The output state is not just a return value; it is a persistent signal on `bus:physical` that other modules (Matrix, Qualia) read from.

## 🗂️ Directory Structure (8.2.0 Standard)
```
physio_core/
├── configs/                 # [SSOT] Biological Parameters
│   ├── endocrine_system.yaml
│   ├── hemodynamics.yaml
│   └── PhysioController_configs.yaml (Master)
│
├── contract/                # [API] Locked Interfaces
│   └── PhysioController_Payload_Contract.yaml
│       (Refers to schema/Physio_Payload_Schema_v2.json)
│
├── schema/                  # [DATA] Strict Validation
│   └── Physio_Payload_Schema_v2.json (The "Lock")
│
├── logic/                   # [CODE] Sub-systems
│   ├── endocrine/           # Hormone regulation
│   ├── autonomic/           # ANS (Sympathetic/Parasympathetic)
│   └── blood/               # Heart rate & Pressure
│
└── physio_core_engine.py     # [ENGINE] Main Controller
```

## 📡 The `bus:physical` Payload
The data broadcast by this module is **strictly validated** by `Physio_Payload_Schema_v2.json`.

| Field | Type | Description |
| :--- | :--- | :--- |
| `ans_state` | Object | Autonomic ratios (Sympathetic vs Parasympathetic) |
| `blood_levels` | Object | Concentrations of key hormones (Cortisol, Dopamine, etc.) |
| `receptor_signals`| Object | Active neurotransmitter binding states |
| `reflex_vector` | Object | Immediate physical reactions (e.g., "flinch", "blush") |

## 🔄 Data Flow (The "Gap")
1.  **Stimulus**: `bus:operational` carries user input.
2.  **Ingest**: `PhysioController` reads stimulus intensity/valence.
3.  **React**: Hormones spike, Heart Rate accelerates.
4.  **Publish**: New state is pushed to `bus:physical` (Latching).
5.  **Consume**:
    *   **EVA Matrix** reads physical state -> generates Emotion.
    *   **Orchestrator** reads physical state -> injects "Body Feel" into prompt.

## 🛠️ Usage
```python
# Standalone Tick (Biological Update)
physio.tick(delta_time=1.0) 

# Stimulus Processing
physio.process_stimulus(stimulus_dict)
```

---

# 🫀 Physio Core (ระบบควบคุมสรีรวิทยา)
**Component ID:** `SYS-PHYSIO-8.2` | **Version:** `8.2.0` | **Role:** ร่างกาย (Latching Stream)

## 📋 ภาพรวม
Physio Core คือ **เครื่องยนต์ทางชีวภาพ (Biological Engine)** ของ EVA 8.2.0 ทำหน้าที่จำลองระบบร่างกายทั้งหมด ไม่ว่าจะเป็น ระบบต่อมไร้ท่อ (ฮอร์โมน), ระบบหัวใจและหลอดเลือด, และระบบประสาทอัตโนมัติ

ในเวอร์ชัน 8.2.0 นี้ Physio Core ทำงานในรูปแบบ **Streaming Publisher** คือมีการ "เต้น" (Tick) ของระบบร่างกายที่เป็นอิสระจากการพูดคุย สัญญาณชีพต่างๆ จะถูกส่งไปค้างสถานะ (Latch) ไว้บน `bus:physical` เพื่อให้ส่วนอื่นๆ ของระบบ (เช่น จิตใจ หรือ ความรู้สึก) ดึงไปใช้งานต่อได้ตลอดเวลา

## ⚙️ กลไกหลัก
1.  **Metabolism (การเผาผลาญ)**: เปลี่ยนสิ่งเร้า (คำพูด, ความรู้สึก) ให้เป็นปฏิกิริยาเคมีในร่างกาย
2.  **Homeostasis (ภาวะสมดุล)**: ดึงระดับฮอร์โมนกลับสู่ค่าปกติโดยอัตโนมัติเมื่อเวลาผ่านไป
3.  **Latching (การค้างสถานะ)**: ข้อมูลไม่ได้ถูกส่งแล้วหายไป แต่จะ "ค้าง" อยู่บน Bus เปรียบเสมือนร่างกายที่ดำรงอยู่ตลอดเวลา

## 📡 ข้อมูลบน `bus:physical`
ข้อมูลที่ส่งออกจากโมดูลนี้จะถูก **ล็อค** ด้วย `Physio_Payload_Schema_v2.json` อย่างเคร่งครัด:

*   **ans_state**: สภาวะระบบประสาท (ตื่นตัว/ผ่อนคลาย)
*   **blood_levels**: ระดับฮอร์โมนในเลือด (คอร์ติซอล, โดปามีน, ออกซิโทซิน ฯลฯ)
*   **receptor_signals**: การจับตัวของสารสื่อประสาท
*   **reflex_vector**: ปฏิกิริยาตอบสนองฉับพลัน (เช่น หน้าแดง, สะดุ้ง)