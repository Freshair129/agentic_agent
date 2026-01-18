# EVA Registry (Single Source of Truth)

**Directory**: `registry/`  
**Purpose**: Centralized governance, versioning, and system registration.  
**Version**: v9.6.2 (Registry-Centric Governance)

---

## 📋 Overview

The **Registry** is the "DNA" of the EVA organism. It defines the authoritative state of every system, module, and protocol. If a system is not registered here, it does not officially exist in the eyes of the Orchestrator.

---

## 📂 Notable Files

### 1. [EVA Master Registry](eva_master_registry.yaml)

The most critical file in the project. It defines:

- **Root Slots**: Authorized folders and files.
- **System Inventory**: Registration of all Organs (Physio, Matrix, MSP).
- **Core Modules**: Implementation details for CIM, PRN, etc.
- **Bus Bindings**: Who publishes/subscribes to what.
- **Global Policies**: Versioning and Cognitive Flow definitions.

### 2. [Version Log](version_log.yaml)

A historical record of version bumps, feature injections, and development eras.

---

## 📐 Governance

- **Registry-Centricity**: Systems must resolve their ports, paths, and IDs from the Registry at runtime.
- **Immutability**: Changes to the registry during runtime are forbidden except through specific hot-reload protocols.
- **Audit**: Every `git commit` should ideally verify that the registry matches the physical file structure.

---

*The DNA of the Organism.*
