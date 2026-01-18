# EVA Operation System (OS)

**Directory**: `operation_system/`  
**Purpose**: Infrastructure, Identity, and Communication Bus.  
**Version**: v9.6.2 (Registry Refined)

---

## 📋 Overview

The **Operation System (OS)** layer provides the low-level infrastructure required for the EVA organism to function as a unified entity. It handles identity management (SSOT), inter-system communication (Resonance Bus), and resonance calculation.

---

## 🏗️ Core Systems

### 1. [Identity Manager](identity_manager.py)

The central authority for all identifiers.

- Manages **Bus Channels**, **System IDs**, **Session IDs**, and **Turn Indexes**.
- Defines the `PERSONA_MAP` (e.g., EVA vs LYRA).

### 2. [Resonance Bus](resonance_bus.py)

The "Heartbeat" of the organism.

- A high-performance signal-bus using a Publish/Subscribe model.
- Decouples systems (Physio, Matrix, Qualia) from direct method calls.
- Standard Channels: `BUS_PHYSICAL`, `BUS_PSYCHOLOGICAL`, `BUS_PHENOMENOLOGICAL`, `BUS_KNOWLEDGE`.

### 3. [RIM (Resonance Impact Engine)](rim/)

Calculates the numerical impact of stimuli on the organism's state.

---

## 📐 Governance

- **Root Authority**: The OS layer is the first thing to initialize and the last to shutdown.
- **Pillar of Decoupling**: All inter-system state propagation MUST occur via the Resonance Bus.
- **Registry Alignment**: All IDs used in the OS must match `registry/eva_master_registry.yaml`.

---

## 🛠️ Verification Tools

- `verify_resonance_loop.py`: Tests the integrity of signal propagation across the bus.
- `verify_retrieval.py`: Validates the interface between OS and Memory.

---

*Infrastructure is the silent substrate of life.*
