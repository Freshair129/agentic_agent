# EVA v9.6.2 Full System Architecture Diagram 🛰️

**Date:** 2026-01-18
**Status:** ✅ **DATA-FLOW CENTRIC**
**Version:** 9.6.2
**Source:** `eva_master_registry.yaml` (Contracts & Topology)

---

This diagram visualizes the **Data Flow** of the organism, starting from **User Input**, passing through the **Bio-Digital Gap**, and resulting in an **Embodied Response**.

## 🌊 Unified Data Flow Architecture

```mermaid
graph TB
    %% ==========================================
    %% EXTERNAL LAYER
    %% ==========================================
    UserIn(["👤 User Input<br/>(Stimulus)"])
    UserOut(["💬 Final Response<br/>(Action)"])

    %% ==========================================
    %% ORCHESTRATION (The Gatekeeper)
    %% ==========================================
    subgraph CNS ["Step 9: ORCHESTRATION (Central Nervous System) [L0]"]
        Orch["Orchestrator<br/>(Main Loop)"]
        CIM["CIM<br/>(Context Injection)"]
    end

    %% ==========================================
    %% THE GAP (Bio-Digital Processing)
    %% ==========================================
    subgraph TheGap ["THE GAP: Real-Time Processing (No LLM)"]
        direction TB
        
        %% Step 3: Biology
        subgraph Body ["Step 3: BIOLOGY (Physiological Domain) [L0]"]
            PhysioCtrl["PhysioCore"]
            
            subgraph BioEngines ["Parallel Engines"]
                Endo["Endocrine (Hormones)"]
                Blood["Blood (Transport)"]
                ANS["ANS (Reflex)"]
                Vitals["Vitals (Heart/Lung)"]
            end
        end

        %% Step 4: Psychology
        subgraph Mind ["Step 4: PSYCHOLOGY (Matrix Domain) [L1]"]
            Matrix["EVA Matrix<br/>(9D Emotional State)"]
        end

        %% Step 5-8: Memory & Pheno
        subgraph Soul ["Step 5-8: MEMORY & SENSES [L1/L2]"]
            MSP["MSP Authority<br/>(Persistence)"]
            GKS["GKS (Knowledge)"]
            RMS["RMS (Resonance)"]
            AQI["Artifact Qualia<br/>(Phenomenology)"]
            
            subgraph MemoryStreams ["Memory Streams"]
                Epi["Episodic"]
                Sem["Semantic"]
            end
        end
    end

    %% ==========================================
    %% INFRASTRUCTURE & IDENTITY
    %% ==========================================
    subgraph Infra ["INFRASTRUCTURE"]
        ID["Step 1: Identity Manager"]
        Bus["Step 2: Resonance Bus"]
    end

    %% ==========================================
    %% DATA FLOW (Registry Contracts)
    %% ==========================================

    %% Input Flow
    UserIn ===> Orch
    Orch -->|Extract Stimulus| PhysioCtrl

    %% Biological Cascade
    PhysioCtrl -->|Drive| Endo
    PhysioCtrl -->|Drive| Blood
    PhysioCtrl -->|Drive| ANS
    PhysioCtrl -->|Drive| Vitals
    
    %% Bus Transport (Implicit)
    Endo -.->|HormonePanel| Bus
    Blood -.->|VitalsData| Bus
    ANS -.->|ReflexState| Bus
    Bus -.->|Global State| Matrix

    %% Psychological Drift
    Matrix -->|Emotional Shift| MSP
    Matrix -.->|9D State| Orch

    %% Memory & Senses
    MSP -->|Latch State| Epi
    MSP -->|Latch State| Sem
    MSP -->|Query Wisdom| GKS
    GKS -->|Filter| RMS
    RMS -->|Resonance| AQI
    AQI ===>|Qualia Texture| Orch

    %% Reasoning & Response
    Orch -->|Contextualize| CIM
    CIM -->|Generate| UserOut

    %% Output Loop
    UserOut -.->|Feedback| Orch

    %% ==========================================
    %% STYLING
    %% ==========================================
    classDef Input fill:#e1f5ff,stroke:#0066cc,stroke-width:2px;
    classDef Output fill:#e1f5ff,stroke:#0066cc,stroke-width:2px;
    classDef L0 fill:#ffcccc,stroke:#d93025,stroke-width:3px;
    classDef L1 fill:#fff2cc,stroke:#f1c232,stroke-width:2px;
    classDef L2 fill:#d9ead3,stroke:#6aa84f,stroke-width:1px;
    classDef InfraStyle fill:#eeeeee,stroke:#999999,stroke-width:1px,stroke-dasharray: 5 5;

    class UserIn Input;
    class UserOut Output;
    class Orch,CIM,PhysioCtrl,Endo,Blood,ANS,Vitals,Bus L0;
    class Matrix,MSP,Epi,Sem L1;
    class GKS,RMS,AQI L2;
    class ID,Bus InfraStyle;
```

---

## 🗺️ Flow Explanation

1. **User Input**: `User` enters text/signal.
2. **Orchestration**: `Orchestrator` receives input and extracts the `StimulusVector`.
3. **Biological Awakening**: `PhysioCore` processes the stimulus, triggering parallel changes in Hormones (`Endocrine`), Heart/Lungs (`Vitals`), and Nerves (`ANS`).
4. **Psychological Shift**: The biological changes travel via the `Resonance Bus` to the `EVA Matrix`, forcing the emotional state (9D) to drift.
5. **Memory Latching**: `MSP` latches this new state and simultaneously queries `Episodic` and `Semantic` memory.
6. **Resonance & Qualia**: The state passes through `GKS` (Knowledge check) and `RMS` (Resonance filter) to create a subjective "feeling" in `Artifact Qualia`.
7. **Embodied Response**: The `Orchestrator` receives the `Qualia` and uses `CIM` to generate a response that matches the biological state.
