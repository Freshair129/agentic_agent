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
    %% 2. ORCHESTRATION & REFLEX
    %% ==========================================
    subgraph CNS ["Step 0: ORCHESTRATION"]
        OrchStart{"Orchestrator<br/>(Input Handler)"}
        EngramCheck{"Engram System<br/>(Cache Hit?)"}
    end

    UserIn --> OrchStart
    OrchStart --> EngramCheck

    %% ==========================================
    %% 3. THE GAP (Embodiment & State Update)
    %% ==========================================
    %% CRITICAL: All paths must update Physio State
    subgraph Gap ["Layer 2: THE GAP (State Update)"]
        direction TB
        
        Physio["PhysioCore<br/>(Update Cycle)"]
        Matrix["EVA Matrix<br/>(State Drift)"]
        
        subgraph Perception ["Perception Route (Miss)"]
            SLM["SLM Bridge"]
            ExtractIntent["Extract Intent"]
        end
        
        subgraph Reflex ["Reflex Route (Hit)"]
            FetchCached["Fetch Cached Pattern"]
        end
    end

    %% Routing
    EngramCheck -- "YES (Reflex)" --> FetchCached
    EngramCheck -- "NO (Deep)" --> SLM

    %% Logic Flow
    SLM --> ExtractIntent
    ExtractIntent -->|Stimulus| Physio
    FetchCached -->|No Stimulus| Physio
    
    Physio -->|New State| Matrix

    %% ==========================================
    %% 4. CONTEXT & REASONING (Synthesis)
    %% ==========================================
    %% CRITICAL: CIM must inject State into LLM regardless of path
    subgraph Reason ["Layer 3: REASONING (State Awareness)"]
        CIM["CIM Injector<br/>(Merge State+Data)"]
        LLM["LLM Core<br/>(Generate Response)"]
    end

    Matrix -->|9D State| CIM
    ExtractIntent -->|Intent| CIM
    FetchCached -->|Pattern| CIM
    
    CIM -->|Prompt: State + Data| LLM

    %% ==========================================
    %% 5. OUTPUT & PERSISTENCE
    %% ==========================================

    %% ==========================================
    %% 5. OUTPUT & PERSISTENCE
    %% ==========================================
    subgraph Save ["Layer 5: PERSISTENCE & PREDICTION (Phase 3)"]
        MSP["MSP Authority<br/>(Save Episode)"]
        Phase3["🔮 Phase 3: PREDICTION<br/>(Self-Note & Summary)"]
    end

    LLM --> FinalOut(["💬 Final Response"])
    FinalOut --> Phase3
    Phase3 -->|Loopback: Self-Note + Plan| CIM
    Phase3 --> MSP

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
