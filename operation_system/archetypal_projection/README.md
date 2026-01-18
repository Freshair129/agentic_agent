# Archetypal Projection Module (APM)

**Directory**: `operation_system/archetypal_projection/`  
**Purpose**: Projecting contextual "lenses" (Frameworks) from GKS onto the active persona.  
**Version**: v9.3.1GE (Expansion Core)

---

## 📋 Overview

The **Archetypal Projection Module (APM)** is EVA's "Perspective Engine." It analyzes the current user input and emotional context to select appropriate "Lenses" from the **Genesis Knowledge System (GKS) Frameworks**. These lenses provide the LLM with consistent philosophical or structural frameworks (e.g., viewing a conflict through a "Relational Growth" lens vs. a "Safety First" lens).

---

## ⚙️ Core Functions

1. **Contextual Analysis**: Scans input and tags to identify relevant GKS Frameworks.
2. **Archetypal Injection**: Generates projection strings that are injected into the LLM's prompt to "prime" its perspective.
3. **Framework Mapping**: Maps dynamic interaction patterns to static, authoritative GKS blocks.

---

## 📂 Structure

- **`apm_engine.py`**: The logic for identifying and projecting archetypes based on GKS triggers.
- **`__init__.py`**: Module initialization.

---

## 📐 Governance

- **System Authority**: Operates as a central module serving both the **Resonance Engine** and **NexusMind**.
- **Data-Driven**: Projections must be based on frameworks explicitly defined in `GKS_Framework_Genesis_Block.json`.

---

*Seeing the world through many eyes.*
