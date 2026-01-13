# Agent (EVA v9.4.0)

**Version:** 9.4.0 (Resonance Refactored)  
**Status:** Active Development  
**Identity:** EVA (The Bio-Digital Organism)

---

## 📂 Directory Structure

This `agent/` directory contains the complete source code and memory state of the AI organism.

### 🧠 Core Components

- **`consciousness/`** (Awareness Domain)
  - The working memory and "aware" interface of the agent.
  - Contains **Shortcuts (.lnk)** to tools and skills (LLM knows *what* it can do, but cannot modify *how*).
  - Contains **Active Memory** (Episodic, Semantic, Sensory) for the current session.

- **`capabilities/`** (Implementation Domain)
  - The actual source code for **Tools**, **Skills**, and **Services**.
  - Hidden from the LLM's direct awareness to ensure safety and stability.

- **`memory/`** (Storage Domain)
  - Long-term persistence, archival storage, and system state snapshots.
  - Managed by the **Memory & Soul Passport (MSP)** system.

### ⚙️ Systems & Organs

- **`genesis_knowledge_system/` (GKS):** Strategic brain, knowledge base, and reasoning modules (NexusMind).
- **`physio_core/`:** Biological simulation (Hormones, Heartbeat, Bloodflow).
- **`eva_matrix/`:** Psychological state engine (9-Dimensional Matrix).
- **`artifact_qualia/` (AQI):** Phenomenological experience and sensory texture.
- **`resonance_memory_system/` (RMS):** Automatic memory encoding and resonance.
- **`memory_n_soul_passport/` (MSP):** The operating system of memory and identity.

---

## 🚀 Usage

This structure separates **Interface (Consciousness)** from **Implementation (Capabilities)** to create a stable, self-aware, but safe AI organism.

- **To run the agent:** Execute the `orchestrator` (path to be defined).
- **To add a skill:** Implement in `capabilities/skills/` and create a reference in `consciousness/skills/`.

---

*Powered by The Human Algorithm*
