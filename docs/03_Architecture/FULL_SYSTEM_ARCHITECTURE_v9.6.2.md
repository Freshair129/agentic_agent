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
    %% 1. INPUT LAYER
    %% ==========================================
    UserIn(["👤 User Input"]) --> OrchStart
    
    subgraph CNS ["Step 0: ORCHESTRATION GATEWAY"]
        OrchStart{"Orchestrator<br/>Receive Input"}
    end

    %% ==========================================
    %% 2. REFLEX LAYER (O1 - Fast Recall)
    %% ==========================================
    subgraph Reflex ["Layer 1: REFLEX (Fast Recall)"]
        EngramCheck{"Engram System<br/>(Cache Hit?)"}
        EngramAction["⚡ Reflex Action<br/>(O(1) Response)"]
    end

    OrchStart --> EngramCheck
    EngramCheck -- "YES (Confident)" --> EngramAction
    EngramAction --> FinalOut

    %% ==========================================
    %% 3. PERCEPTION LAYER (P1 - Intent)
    %% ==========================================
    subgraph Perception ["Layer 2: PERCEPTION (Intent & Signal)"]
        SLM["SLM Bridge<br/>(Small Language Model)"]
        ExtractIntent["🔍 Extract Intent<br/>& Sentiment"]
    end

    EngramCheck -- "NO (Deep Process)" --> SLM
    SLM --> ExtractIntent

    %% ==========================================
    %% 4. THE GAP (Bio-Digital Bridge)
    %% ==========================================
    subgraph Gap ["Layer 3: THE GAP (Embodiment)"]
        direction TB
        Stimulus["Stimulus Injection"]
        
        subgraph Body ["Biological State"]
            Physio["PhysioCore<br/>(Hormones/Vitals)"]
        end
        
        subgraph Mind ["Psychological State"]
            Matrix["EVA Matrix<br/>(Emotion Drift)"]
        end

        subgraph Memory ["Subjective Memory"]
            RAG["Agentic RAG<br/>(7-Stream Recall)"]
            Qualia["Artifact Qualia<br/>(Texture)"]
        end
    end

    ExtractIntent --> Stimulus
    Stimulus --> Physio
    Physio --> Matrix
    Matrix --> RAG
    RAG --> Qualia

    %% ==========================================
    %% 5. REASONING LAYER (P2 - Synthesis)
    %% ==========================================
    subgraph Reason ["Layer 4: REASONING (Synthesis)"]
        CIM["CIM Injector<br/>(Context Assembly)"]
        LLM["LLM Core<br/>(Gemini/Ollama)"]
    end

    Qualia --> CIM
    CIM --> LLM

    %% ==========================================
    %% 6. OUTPUT & PERSISTENCE
    %% ==========================================
    subgraph Save ["Layer 5: PERSISTENCE"]
        MSP["MSP Authority<br/>(Save Episode)"]
    end

    LLM --> FinalOut(["💬 Final Response"])
    FinalOut --> MSP

    %% ==========================================
    %% STYLING (High Contrast)
    %% ==========================================
    classDef Node fill:#ffffff,stroke:#333333,stroke-width:2px;
    classDef Critical fill:#ffffff,stroke:#d93025,stroke-width:3px;
    classDef Logic fill:#ffffff,stroke:#16537e,stroke-width:3px;
    classDef Fast fill:#ffffff,stroke:#f1c232,stroke-width:3px;

    class UserIn,FinalOut Node;
    class OrchStart,EngramCheck,EngramAction Fast;
    class SLM,ExtractIntent,Stimulus,CIM,LLM Logic;
    class Physio,Matrix,RAG,Qualia Critical;
    class MSP Node;
```

---

## 🔍 Logic Flow Explanation (Audit Checklist)

1. **Reflex Check (Fast Recall)**:
    * **Is it in Engram?**: ระบบตรวจสอบ Cache (Engram) ก่อนทันที
    * **Yes**: ตอบกลับทันที (O1) จบ Process ไม่ต้องปลุกระบบร่างกาย
    * **No**: ส่งต่อเข้ากระบวนการเต็มรูปแบบ

2. **Perception (Intent)**:
    * **SLM Analysis**: ใช้ Model เล็ก (SLM) วิเคราะห์ **Intent** และ **Sentiment** เพื่อสร้าง `StimulusVector` ที่แม่นยำ

3. **The Gap (Embodiment)**:
    * **Physio Reaction**: ร่างกายตอบสนองต่อ Stimulus (หัวใจเต้น, ฮอร์โมนหลั่ง)
    * **Matrix Drift**: อารมณ์ (9D) เปลี่ยนตามสรีระ
    * **Memory Context**: ดึงความจำโดยใช้ *อารมณ์ปัจจุบัน* เป็นตัวล่อ (State-Dependent Retrieval)

4. **Reasoning**:
    * **CIM Assembly**: รวบรวม "ความรู้สึก" + "ความจำ" + "เจตนา" ส่งให้ LLM
    * **Generation**: LLM สร้างคำตอบภายใต้สภาวะร่างกายนั้น

5. **Persistence**:
    * บันทึกเหตุการณ์ลง MSP เพื่อเป็นความจำในอนาคต

---

> **Note**: Diagram นี้เน้น **Logic Flow** ตามที่ User ต้องการ (Input -> Reflex -> Perception -> Body -> Reasoning) ไม่ใช่ System Topology.
