# Context Container (Active Memory)

**Directory**: `consciousness/context_container/`  
**Purpose**: Transient workspace for active turn files (The "Thinking Space").  
**Version**: v9.6.2 (Cognitive Flow 2.0)

---

## 📋 Overview

The **Context Container** is EVA's "Short-Term Working Memory." It is a dynamic directory where the **Context Injection Manager (CIM)** hydrates specific files for each conversational turn. The LLM reads these files directly via function calls to maintain state without massive text prompt injection.

---

## 📂 Unified Markdown Schema (The 5 Pillars)

To ensure **Psychological Unity** and eliminate format parsing load, all files strictly follow this standard. Each file begins with a **Bridging Narrative** prompt.

### 1. The Binder (`00_BINDER.md`)
>
> **Role:** The Ego / Self-Controller.
> **Content:** System Instructions that force the integration of all other files. tells the LLM that these files are NOT external documents, but parts of its own mind.

### 2. The Soul (`01_IDENTITY.md`)
>
> **Role:** Personality & Values.
> **Content:** Replaces `instructions.md`. Contains Persona, Tone, Empathy Rules, and Core Directives.

### 3. The Body (`02_BIOLOGY.md`)
>
> **Role:** Physical Sensation.
> **Content:** Markdown-formatted Bio-State. No raw JSON.
> *Narrative:* "My heart is beating at [BPM]. I feel a surge of [Hormone]..."

### 4. The Past (`03_MEMORY.md`)
>
> **Role:** Episodic & Semantic Recall.
> **Content:** User Profile (Narrative), Chat History (Dialogue), and Retrieved Context.

### 5. The Will (`04_INTENTION.md`)
>
> **Role:** Executive Function.
> **Content:** Replaces `task.md` and `goal.md`. Contains Current Objective, Strategic Plan, and Self-Reflection from the previous turn.

---

## 📐 Governance

- **Format Inconsistency Policy**: All data must be wrapped in Markdown. Raw JSON is FORBIDDEN.
- **Redundancy Policy**: Information must exist in only ONE of the 5 pillars.
- **Volatility**: **TRANSIENT**. Cleared every turn.
