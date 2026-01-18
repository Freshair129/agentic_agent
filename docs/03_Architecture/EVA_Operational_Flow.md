# EVA v9.6.2 Operational Flow (Authoritative)
>
> **Status**: Canonical / Final
> **Version**: 9.6.2 (Registry Refined)
> **Role**: Source of Truth for Runtime Orchestration (Synced with Registry)
> **Companion**: See [Cognitive Flow 2.0](file:///e:/The%20Human%20Algorithm/T2/agent/orchestrator/cognitive_flow/docs/Cognitive_Flow_2_0.md) for logic sequence.

เอกสารฉบับนี้แสดง **Runtime Execution Flow** ที่ถูกกำหนดใน `eva_master_registry.yaml` ซึ่งเป็นจุดอ้างอิงเดียว (SSOT) สำหรับการ Boot และ Execution ของระบบ

---

## 📊 Unified Execution Graph (Registry-Driven)

แผนผังนี้แสดง **Boot Order** (Awakening Sequence) และ **Parallel Execution Groups** ตามที่กำหนดใน Registry:

```mermaid
sequenceDiagram
    participant ID as Identity (Step 1)
    participant Bus as Resonance Bus (Step 2)
    participant Physio as Physio + Modules (Step 3 Async)
    participant Matrix as Matrix (Step 4)
    participant MSP as MSP + Modules (Step 5 Async)
    participant GKS as GKS (Step 6)
    participant RMS as RMS (Step 7)
    participant AQI as Qualia (Step 8)
    participant Orch as Orchestrator (Step 9)

    Note over ID: 1. ACCESS GRANTED
    ID->>Bus: Initialize
    
    Note over Bus: 2. TRANSPORT READY
    Bus->>Physio: System Start
    
    par Step 3: BIOLOGICAL AWAKENING (Parallel)
        Physio->>Physio: Heartbeat Start
        Physio->>Bus: Hormones (Endocrine)
        Physio->>Bus: Circulation (Blood)
        Physio->>Bus: Reflex (ANS)
    end
    
    Physio->>Matrix: State Update
    
    Note over Matrix: 4. PSYCHOLOGICAL BIRTH
    Matrix->>MSP: Latch State
    
    par Step 5: MEMORY RESTORATION (Parallel)
        MSP->>MSP: Load Index
        MSP->>Bus: Load Episodic Stream
        MSP->>Bus: Load Semantic Concepts
    end
    
    MSP->>GKS: Request Wisdom
    Note over GKS: 6. KNOWLEDGE LOAD
    
    GKS->>RMS: Configure Filters
    Note over RMS: 7. RESONANCE READY
    
    RMS->>AQI: Open Senses
    Note over AQI: 8. PHENOMENOLOGY ONLINE
    
    AQI->>Orch: SYSTEM READY
    Note over Orch: 9. ORCHESTRATION LOOP START
    Orch->>Orch: Main Loop (30Hz)
```

---

## 🛠️ Runtime Hook Mapping (Configuration Source)

**[IMPORTANT]**: หากต้องการแก้ไขลำดับการทำงาน ให้ไปที่ `registry/eva_master_registry.yaml` หมวด **5. RUNTIME EXECUTION FLOW**.

| Step | System | Mode | Entry Point (Runtime Hook) | Config Source |
| :--- | :--- | :--- | :--- | :--- |
| **1** | Identity_Manager | `serial` | `operation_system.identity_manager` | Registry (`#5`) |
| **2** | Resonance_Bus | `serial` | `operation_system.resonance_bus` | Registry (`#5`) |
| **3** | **PhysioCore Group** | `parallel` | `physio_core.physio_core` (Controller) | Registry (Mod Rules) |
| **4** | EVA_Matrix | `serial` | `eva_matrix.eva_matrix` | Registry (`#5`) |
| **5** | **MSP Group** | `parallel` | `memory_n_soul_passport.engine` | Registry (Mod Rules) |
| **6** | GKS | `serial` | `genesis_knowledge_system.gks_interface` | Registry (`#5`) |
| **7** | RMS | `serial` | `resonance_memory_system.rms` | Registry (`#5`) |
| **8** | Artifact_Qualia | `serial` | `artifact_qualia.artifact_qualia` | Registry (`#5`) |
| **9** | **Orchestrator** | `loop_start` | `orchestrator.orchestrator` | Registry (`#5`) |

## 🔑 Terminology Enforcement (v9.4.3)

* **CIM (Context Injection Module)**: *[REPLACES CIN]* หน่วยงานจัดเตรียม Context ให้ LLM
* **The Gap**: ช่วงเวลาประมวลผลระบบสรีรวิทยาและจิตวิทยาข้าม Token
* **State-Dependent Memory**: การดึงความจำที่เน้นความสอดคล้องกับอารมณ์ความรู้สึกปัจจุบัน
* **Hydrate**: (State) การกู้คืนสภาวะความจำเก่าลงสู่ Consciousness โดย MSP/RAG
* **Contextualize**: (Process) การปรับปรุงบริบทของเทิร์นปัจจุบันด้วยข้อมูลจากความจำถาวร
* **Engram**: หน่วยความจำรีเฟล็กซ์ที่ทำงานระดับ O(1)

---

<!-- markdownlint-disable-next-line MD036 -->
**Created for EVA v9.4.3 Implementation**
