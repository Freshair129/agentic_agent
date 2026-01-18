# EVA v9.6.2 Full System Architecture Diagram 🛰️

**Date:** 2026-01-18
**Status:** ✅ **LOGICAL PIPELINE (AUDIT VIEW)**
**Version:** 9.6.2
**Role:** Life of a Request (Input to Output)

---

This diagram visualizes the **Logical Execution Path** of a single user interaction, detailing **Reflex (Fast)**, **Perception (Intent)**, **Embodiment (Gap)**, and **Reasoning (Slow)** layers. Designed for **Logic Auditing**.

## 🧠 Logical Pipeline: The Life of a Request

```mermaid
graph TD
    %% ==========================================
    %% 1. INPUT & REFLEX (STEP 0)
    %% ==========================================
    UserIn(["👤 User Input"]) --> EngramCheck
    
    subgraph Reflex ["Layer 1: REFLEX (Engram)"]
        EngramCheck{"Engram System<br/>(Cache Hit?)"}
        FastOut(["⚡ Fast Response<br/>(O(1) Return)"])
    end
    
    EngramCheck -- "YES" --> FastOut
    EngramCheck -- "NO" --> SLM

    %% ==========================================
    %% 2. PERCEPTION (STEP 1)
    %% ==========================================
    subgraph Perception ["Layer 2: PERCEPTION (SLM)"]
        SLM["SLM Bridge<br/>(Extract Intent & Sentiment)"]
        Stimulus["Stimulus Vector<br/>(Intent + Anchor)"]
    end
    
    SLM --> Stimulus

    %% ==========================================
    %% 3. EMBODIMENT & REASONING (STEP 2-3)
    %% ==========================================
    subgraph BodyMind ["Layer 3: REASONING & EMBODIMENT (One API Call)"]
        direction TB
        
        %% Phase 1
        Stimulus --> LLM_Start["LLM Start<br/>(Phase 1 Probe)"]
        
        %% Function Call
        LLM_Start --> FnCall{{"Fn: sync_bio_state()"}}
        
        %% The Gap
        subgraph Gap ["The Gap (Bio-Digital Sync)"]
            direction TB
            Physio["PhysioCore"]
            Matrix["EVA Matrix"]
            MemRetrieval["RAG & RMS"]
        end
        
        FnCall -->|Pause| Physio
        Physio --> Matrix
        Matrix --> MemRetrieval
        
        %% Phase 2
        MemRetrieval -->|Resume| LLM_Resume["LLM Resume<br/>(Phase 2 Reasoning)"]
    end

    %% ==========================================
    %% 4. PERSISTENCE & PREDICTION (STEP 4)
    %% ==========================================
    subgraph Phase3 ["Layer 4: PERSISTENCE & PREDICTION"]
        FinalOut(["💬 Final Response"])
        Prediction["🔮 Phase 3<br/>(Loopback & Sponge)"]
        MSP["MSP Authority<br/>(Archival)"]
    end

    LLM_Resume --> FinalOut
    FinalOut --> Prediction
    Prediction -->|Context| MSP
    
    %% Loopback
    Prediction -.->|Next Turn Context| EngramCheck

    %% ==========================================
    %% STYLING
    %% ==========================================
    classDef Node fill:#ffffff,stroke:#333333,stroke-width:2px;
    classDef Critical fill:#ffffff,stroke:#d93025,stroke-width:3px;
    classDef Logic fill:#ffffff,stroke:#16537e,stroke-width:3px;
    classDef Fast fill:#ffffff,stroke:#f1c232,stroke-width:3px;

    class UserIn,FastOut,FinalOut Node;
    class EngramCheck,EngramAction Fast;
    class SLM,Stimulus,LLM_Start,LLM_Resume,FnCall,Prediction Logic;
    class Physio,Matrix,MemRetrieval Critical;
    class MSP Node;
```

---

## 🔍 Logic Flow Explanation (Audit Checklist)

1. **Reflex Layer (Engram)**:
    * **Engram System**: ตรวจสอบ Cache ก่อนเข้าสู่ Perception
    * **Hit**: ตอบกลับทันที (O1 Fast Response)
    * **Miss**: ส่งต่อให้ SLM (Deep Process)

2. **Perception Layer (SLM)**:
    * **SLM Bridge**: แปลง Input เป็น `Stimulus Vector` (Intent/Sentiment)
    * **No Hallucination**: ใช้ Llama-3.2 1B เพื่อ Cross-check เจตนา

3. **Reasoning & Embodiment (The Gap)**:
    * **LLM Phase 1**: รับ Stimulus -> ตัดสินใจเรียก Tool `sync_bio_state`
    * **The Gap**:
        * **PhysioCore**: ร่างกายตอบสนอง (หัวใจ/ฮอร์โมน)
        * **Matrix**: อารมณ์เปลี่ยน (Drift)
        * **Retrieval**: ดึงความจำด้วย "อารมณ์" เป็น Key
    * **LLM Phase 2**: รับข้อมูล Embodied State ทั้งหมดแล้วตอบสนอง

4. **Prediction & Persistence**:
    * **Loopback**: ส่ง Context Family และ Self-Note กลับไปที่ CIM (Turn หน้า)
    * **MSP**: บันทึก Episode ลงฐานข้อมูลถาวร

---

> **Note**: Diagram นี้เน้น **Logic Flow** ตามที่ User ต้องการ (Input -> Reflex -> Perception -> Body -> Reasoning) ไม่ใช่ System Topology.
