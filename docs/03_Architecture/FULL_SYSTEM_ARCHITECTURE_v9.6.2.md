# EVA v9.6.2 Full System Architecture Diagram 🛰️

**Date:** 2026-01-18
**Status:** ✅ **REGISTRY-DRIVEN** (Source: `eva_master_registry.yaml`)
**Version:** 9.6.2

---

This diagram represents the **Authoritative Architecture** of the EVA Organism, derived directly from the **Master Registry**. It visualizes the **Runtime Execution Flow** (Boot Order) and **Data Contracts** (Data Flow).

## 🧬 Registry-Driven Topology

```mermaid
graph TB
    %% ==========================================
    %% 1. RUNTIME SEQUENCE (Top-Down Boot Boot)
    %% ==========================================

    %% Step 1: Identity
    subgraph Step1_Security ["1. Security & Identity"]
        ID["Identity Manager<br/>(System ID Provider)"]
    end

    %% Step 2: Transport
    subgraph Step2_Transport ["2. Transport Layer"]
        Bus["Resonance Bus<br/>(Pub/Sub Infrastructure)"]
    end

    %% Step 3: Biology (Parallel Group)
    subgraph Step3_Body ["3. Biological Domain (PhysioCore) [L0]"]
        direction TB
        PhysioCtrl["PhysioCore<br/>(Controller)"]
        
        subgraph PhysioModules ["Parallel Engines (Async)"]
            Endo["Endocrine Engine<br/>(Hormones)"]
            Blood["Blood Engine<br/>(Transport)"]
            ANS["ANS Engine<br/>(Reflex)"]
            Vitals["Vitals Engine<br/>(Heart/Lung)"]
        end
    end

    %% Step 4: Psychology
    subgraph Step4_Mind ["4. Psychological Domain (Matrix) [L1]"]
        Matrix["EVA Matrix<br/>(9D Emotional State)"]
    end

    %% Step 5: Memory (Parallel Group)
    subgraph Step5_Soul ["5. Memory Domain (MSP) [L1]"]
        direction TB
        MSPCtrl["MSP Authority<br/>(Persistence Layer)"]
        
        subgraph MemModules ["Parallel Streams (Async)"]
            Episodic["Episodic Memory"]
            Semantic["Semantic Memory"]
        end
    end

    %% Step 6-8: Cognition & Senses
    subgraph Step678_Cognition ["6-8. Knowledge & Senses [L2]"]
        GKS["GKS (Knowledge)"]
        RMS["RMS (Resonance Filter)"]
        AQI["Artifact Qualia (Senses)"]
    end

    %% Step 9: Orchestration
    subgraph Step9_CNS ["9. Central Nervous System [L0]"]
        Orch["Orchestrator<br/>(Main Loop 30Hz)"]
        CIM["CIM<br/>(Context Injection)"]
    end

    %% ==========================================
    %% DATA FLOW CONTRACTS (From Registry)
    %% ==========================================

    %% 1. Init Flow
    ID -->|Auth| Bus
    Bus -->|Connect| PhysioCtrl
    Bus -->|Connect| Matrix
    Bus -->|Connect| MSPCtrl
    Bus -->|Connect| Orch

    %% 2. User Input Flow
    User((User)) -->|Input| Orch
    Orch -->|StimulusVector| PhysioCtrl

    %% 3. Biological Flow (Physio Contracts)
    PhysioCtrl -->|Drive| Endo
    PhysioCtrl -->|Drive| Blood
    PhysioCtrl -->|Drive| ANS
    PhysioCtrl -->|Drive| Vitals
    
    Endo -->|HormonePanel| Bus
    Blood -->|VitalsData| Bus
    ANS -->|ReflexState| Bus

    %% 4. Psychological Flow (Matrix Contracts)
    Bus -->|HormonePanel| Matrix
    Matrix -->|EmotionalState 9D| Bus
    Matrix -->|EmotionalState 9D| Orch

    %% 5. Memory Flow (MSP Contracts)
    Matrix -->|State Latch| MSPCtrl
    Orch -->|Context Query| MSPCtrl
    MSPCtrl -->|Retrieve| Episodic
    MSPCtrl -->|Retrieve| Semantic
    
    %% 6. Resonance & Phenomenology
    MSPCtrl -->|Context| GKS
    GKS -->|Wisdom| RMS
    RMS -->|Resonance| AQI
    AQI -->|Qualia| Orch

    %% 7. Output Flow
    Orch -->|Response| User

    %% ==========================================
    %% STYLING
    %% ==========================================
    classDef L0 fill:#ffcccc,stroke:#d93025,stroke-width:3px;    %% Critical (Red)
    classDef L1 fill:#fff2cc,stroke:#f1c232,stroke-width:2px;    %% Essential (Yellow)
    classDef L2 fill:#d9ead3,stroke:#6aa84f,stroke-width:1px;    %% Functional (Green)
    classDef Infra fill:#eeeeee,stroke:#999999,stroke-width:1px; %% Infra (Grey)

    class PhysioCtrl,Orch,Bus,Endo,Blood,ANS,Vitals,CIM L0;
    class Matrix,MSPCtrl,Episodic,Semantic L1;
    class GKS,RMS,AQI L2;
    class ID Infra;
```

---

## 🏗️ System Criticality & Roles

| System | Criticality | Role | Boot Step |
| :--- | :--- | :--- | :--- |
| **PhysioCore** | 🔴 **L0 (CRITICAL)** | System Authority | Step 3 |
| **Orchestrator** | 🔴 **L0 (CRITICAL)** | System Authority | Step 9 |
| **Resonance_Bus** | 🔴 **L0 (CRITICAL)** | Transport | Step 2 |
| **EVA_Matrix** | 🟡 **L1 (ESSENTIAL)** | Core System | Step 4 |
| **MSP** | 🟡 **L1 (ESSENTIAL)** | Core System | Step 5 |
| **GKS** | 🟢 **L2 (FUNCTIONAL)** | Knowledge | Step 6 |
| **Artifact_Qualia** | 🟢 **L2 (FUNCTIONAL)** | Core System | Step 8 |

> **Note**: This diagram is **Auto-Generated** conceptually from the `eva_master_registry.yaml`. Any changes to architecture should be made in the Registry first.
