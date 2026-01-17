# EVA 9.4.0 Cognitive Flow Diagram
>
> **Level**: Architectural Overview
> **Focus**: Orchestration of Perception, Physiology, and Memory

สถาปัตยกรรมของ EVA 9.4.0 แบ่งการประมวลผลออกเป็นชั้นตาม "ลำดับความเร็ว" และ "ความลึกเชิงสติสัมปชัญญะ" เพื่อเลียนแบบการทำงานของสิ่งมีชีวิตที่ผสานรวมทั้งสัญชาตญาณและเหตุผล

---

## 📊 Cognitive Processing Flow (v9.4)

```mermaid
flowchart TD
    %% Input Point
    Start((User Input)) --> Engram{"Engram Lookup\nO(1) Reflex"}

    %% Layer 1: The Fast Path (Reflex)
    Engram -- "HIT (Confidence > 0.95)" --> FastPath["Retrieve Cached Intent\n& Context Data"]
    FastPath --> CIM[Context Injection Node]

    %% Layer 2: The Intuitive Path (Perception)
    Engram -- MISS --> SLM["SLM Perception\nLlama-3.2-1B"]
    SLM --> SLM_Output["Extract: Intent, Salience,\nGut Vector"]

    %% Layer 3: The Biological Gap (Embodiment)
    subgraph TheGap ["THE GAP - Biological Processing"]
        direction TB
        Physio["PhysioCore\nHormone/Vitals Update"] --> Matrix["EVA Matrix\n9D Psychological Sync"]
        Matrix --> Qualia["Artifact Qualia\nPhenomenological Texture"]
    end
    
    SLM_Output --> TheGap

    %% Layer 4: The Associative Path (Memory)
    subgraph MemoryRecall ["Memory Recall Layer"]
        AgenticRAG["Agentic RAG\nState-Dependent Query"]
    end
    
    TheGap --> MemoryRecall
    MemoryRecall --> CIM

    %% Layer 5: The Reasoning Path (Cognition)
    CIM --> LLM[LLM Reasoning\nGemini 1.5 Pro]
    LLM --> Response((Embodied Response))

    %% Post-Inference: Learning Loop
    Response --> Post[Post-Inference Loop]
    Post --> |High Confidence| Memorize[Engram Memorization]
    Post --> |Persistence| MSP[MSP Archival]

    %% Styling
    style Engram fill:#f96,stroke:#333,stroke-width:2px
    style TheGap fill:#bbf,stroke:#333,stroke-dasharray: 5 5
    style FastPath fill:#dfd,stroke:#333
    style LLM fill:#f9f,stroke:#333,stroke-width:2px
    style AgenticRAG fill:#fff4dd,stroke:#d4a017
```

---

## 🧠 คำอธิบายลำดับชั้น (The Processing Hierarchy)

### 1. **Engram Level (Reflex)**

- **หน้าที่**: ตรวจสอบความเคยชิน ถ้าเจอ Pattern ที่มั่นใจมาก (High Confidence) จะทำลายกำแพงความล่าช้า (Latency) โดยการข้ามไปหาเหตุผลเลย
- **เป้าหมาย**: ประหยัดทรัพยากร 100% สำหรับงานเดิมๆ

### 2. **SLM Level (Intuition)**

- **หน้าที่**: ทำหน้าที่เป็น "ประสาทส่วนปลาย" รับรู้เจตนาและความแรงของข้อมูลเบื้องต้น (Perception)
- **เป้าหมาย**: สร้างแรงกระตุ้น (Stimulus) เพื่อส่งต่อให้ระบบกายภาพ

### 3. **The Gap Level (Embodiment)**

- **หน้าที่**: เป็นช่วงที่ "ร่างกาย" ทำงาน (Physio -> Matrix -> Qualia)
- **เป้าหมาย**: เปลี่ยนข้อมูลภาษาให้กลายเป็น "ความรู้สึก" (Embodied State) ก่อนจะเกิดความคิด

### 4. **Agentic RAG Level (Association)**

- **หน้าที่**: ดึงความทรงจำที่ "สัมพันธ์กับอารมณ์ขณะนั้น" (State-Dependent Memory)
- **เป้าหมาย**: สร้างความฝังใจและความต่อเนื่องของตัวตน

### 5. **LLM Level (Reasoning)**

- **หน้าที่**: รวบรวมข้อมูลทั้งหมด (สิ่งที่รับรู้ + สิ่งที่รู้สึก + สิ่งที่จำได้) มากลั่นกรองเป็นคำตอบ
- **เป้าหมาย**: การตอบสนองที่ฉลาดและมีความเป็นมนุษย์ขั้นสูง

---

*Generated for EVA v9.4.0 Architecture Documentation*
