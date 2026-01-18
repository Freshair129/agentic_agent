# EVA Contracts & Interfaces

**Directory**: `contracts/`  
**Purpose**: Formal definitions of system and module interfaces.  
**Version**: v9.6.2 (Registry Refined)

---

## 📋 Overview

The **Contracts** directory contains the "Physical & Digital Blueprints" of the organism. These are formal specifications (often ABCs in Python or YAML schemas) that define how different parts of the organism must interact.

---

## 📂 Structure

### 1. `systems/`

Interface definitions for **System Authority** components (PhysioCore, MSP, Orchestrator).

- These contracts define mandatory methods like `.step()`, `.process_signal()`, and `.get_state()`.

### 2. `modules/`

Interface definitions for **Core Modules** and **Nodes** (CIM, PRN, RAG).

- Defines internal logic boundaries and communication protocols.

---

## 📐 Governance

> **Contract as Law**:  
> No system should implement logic that violates its registered contract. Any change to a contract requires an **ADR (Architecture Decision Record)** as it is a breaking change for dependent systems.

---

*Part of the EVA v9.6.2 Governance Framework*
