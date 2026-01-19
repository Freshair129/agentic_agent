# PMT (Prompt Rule Layer)
**Component ID:** `SYS-PMT-8.2` | **Version:** `8.2.0` | **Role:** Behavioral Governance

> [!NOTE]
> **Resonance Bus Integration:** This module publishes to `bus:knowledge` and subscribes to `bus:physical` and `bus:psychological`.

## 📋 Overview
The Prompt Rule Layer (PMT) is the **Behavioral and Identity Governor** for EVA 8.2.0. It acts as the system's "conscience," ensuring that all generated responses align with EVA's core identity and behavioral rules.

It enforces the "40/60 Hierarchy of Truth," where 60% of the response is dictated by the raw physiological state and 40% by the defined persona and communication style.

## ⚙️ Core Functions
1.  **Identity Management**: Loads and provides the core `soul.md` and `persona.yaml` identity documents.
2.  **Rule Modulation**: Dynamically selects and activates behavioral rules based on the current physiological and psychological state received from the bus.
3.  **Governance Payload**: Publishes a "knowledge" payload containing the active identity block and behavioral directives for the Context Injection Node (CIN) to use in prompt construction.

## 🗂️ Directory Structure (8.2.0 Standard)
```
pmt/
├── configs/
│   ├── PMT_Interface.yaml
│   └── PMT_configs.yaml
│
├── contract/
│   └── PMT_Payload_Contract.yaml
│
├── schema/
│   └── PMT_Payload_Schema_v2.json
│
├── docs/
│   └── (Conceptual Docs)
│
├── tests/
│   └── (Unit and integration tests)
│
├── pmt_engine.py     # [ENGINE] Main engine
└── __init__.py
```

## 📡 The `bus:knowledge` Payload
The data broadcast by this module is validated by `PMT_Payload_Schema_v2.json` and contains:
-   **`identity_block`**: The core `soul.md` and `persona.yaml` content.
-   **`behavioral_directive`**: The set of active rules and constraints based on the current system state.
