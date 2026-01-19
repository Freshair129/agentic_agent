## 2. Phase Execution Logic (`cim.py`)

The CIM executes the cognitive loop in three distinct, sequential phases:

### Phase 1: Perception & First Impression
- **Perception Bundle**: Gathers raw Input, current Body State (Bus), and Engram Cache.
- **SLM Candidate**: Llama-3.2-1B generates an "Intuition Candidate" (Intent + Emotion Signal) to bootstrap LLM perception.
- **Hydration**: CIM assembles the initial `context_container/` with rules and first impressions.

### Phase 2: Reasoning & Deep Recall
- **Trigger**: LLM calls `sync_biocognitive_state`.
- **RAG Injection**: CIM injects retrieved memory streams (Hept-Stream results from Agentic RAG) into the container.
- **Deep State**: The container is re-hydrated with a high-fidelity "Deep State" for final LLM reasoning.

### Phase 3: Reflection & Persistence
- **Self-Note**: Generates a post-interaction "Reflection" (`self_note_epXX.md`) to guide future turns.
- **Archival**: MSP moves the turn context from `consciousness/context_container` to persistent history, clearing the RAM for the next technical turn.

### 2.1 Atomic Node Roles: `CIM`
- **Node: `Phase1_Perception`**: Responsible for intent extraction and stimulus normalization.
- **Node: `Phase2_Reasoning`**: Multi-stage recall and deep memory injection.
- **Node: `Phase3_Reflection`**: Memory distillation and future-turn priming.

## 3. Global Context Budgets
- **Token Counter**: Uses `tiktoken` (cl100k_base) to enforce strict context budgets (History cap, Rule cap) before LLM injection.

## 4. Code Mapping
- `cim.py`: The master execution engine for all 3 phases.
- `cim_identity_loader.py`: Specialized loader for Persona and Soul configurations.
