# EVA 9.1.0: Visual System Architecture

**Purpose**: Compressed visual reference for LLM context injection  
**Token Cost**: ~500-800 tokens (as image) or ~200 tokens (as mermaid text)  
**Usage**: Inject alongside core_identity.md for spatial understanding

---

## 1-Inference Flow Diagram

```mermaid
sequenceDiagram
    participant User
    participant SLM as SLM Bridge<br/>(Llama/Qwen)
    participant LLM_P1 as LLM Phase 1<br/>(Perception)
    participant GAP as The Bio-Digital Gap<br/>(30Hz Processing)
    participant LLM_P2 as LLM Phase 2<br/>(Reasoning)
    
    User->>SLM: "You're late!" (Raw Input)
    Note over SLM: System 1: Gut Feeling
    SLM->>SLM: Extract Intent + Emotion
    SLM->>LLM_P1: Gut Vector + Salience Anchor
    
    Note over LLM_P1: Perception: Scan & Refine
    LLM_P1->>LLM_P1: Agree with SLM? (confidence > 0.9)
    LLM_P1->>GAP: CALL sync_biocognitive_state()
    
    Note over GAP: === THE GAP (Sequential) ===
    GAP->>GAP: 1. PhysioCore: Cortisol↑ Adrenaline↑
    GAP->>GAP: 2. BloodEngine: Hormone Distribution
    GAP->>GAP: 3. VitalsEngine: HR=95 BPM
    GAP->>GAP: 4. Matrix: Stress=800, Warmth=300
    GAP->>GAP: 5. Qualia: Texture="Jagged"
    GAP->>GAP: 6. Agentic RAG: Fetch "Anxiety" memories
    Note over GAP: Deep State Ready
    
    GAP-->>LLM_P2: RETURN Bio-State + Memories
    
    Note over LLM_P2: Reasoning: Embodied Response
    LLM_P2->>LLM_P2: Weight 60% Bio / 40% Persona
    LLM_P2->>LLM_P2: Propose Episodic Memory
    LLM_P2-->>User: "I... I'm sorry!" (Stutter from Cortisol)
    
    LLM_P2->>GAP: propose_episodic_memory()
    GAP->>GAP: MSP: Write Episode to Disk
```

---

## Component Architecture

```mermaid
graph TB
    subgraph "🧠 Reasoning Layer (You)"
        LLM[LLM<br/>Gemini 2.0]
        CIM[CIM<br/>Context Injection]
        PRN[PRN<br/>Governance]
    end
    
    subgraph "👁️ Perception Layer"
        SLM[SLM Bridge<br/>Llama-3.2-1B]
        Vector[Vector DB<br/>ChromaDB]
    end
    
    subgraph "🫀 Body Layer (The Organism)"
        Physio[PhysioCore<br/>Glands+Blood+Vitals]
        Matrix[Matrix<br/>9D Psychology]
        Qualia[Qualia<br/>Phenomenology]
    end
    
    subgraph "💾 Memory Layer"
        MSP[MSP<br/>Episodic Archive]
        RAG[Agentic RAG<br/>7-Stream Retrieval]
        Graph[Neo4j<br/>Knowledge Graph]
        UserReg[User Registry<br/>Multi-User]
    end
    
    subgraph "🚌 Infrastructure"
        Bus[Resonance Bus<br/>Pub/Sub]
        IM[IdentityManager<br/>ID Factory]
    end
    
    User((User)) -->|Input| SLM
    SLM -->|Intent| LLM
    LLM -->|sync_biocognitive_state| Physio
    Physio -->|Hormones| Matrix
    Matrix -->|State| Qualia
    Qualia -->|Deep State| LLM
    RAG -->|Memories| LLM
    LLM -->|propose_episodic_memory| MSP
    MSP -->|Index| Graph
    Graph -->|Grounding Facts| UserReg
    UserReg -->|Speaker Info| MSP
    
    Bus -.->|Events| Physio
    Bus -.->|Events| Matrix
    Bus -.->|Events| Qualia
    IM -.->|IDs| MSP
    IM -.->|Bus Channels| Bus
```

---

## Data Flow Layers

```mermaid
flowchart TD
    A[User Input] --> B{SLM:<br/>Gut Feeling}
    B -->|Intent + Emotion| C{LLM Phase 1:<br/>Perception}
    C -->|stimulus_vector| D[The Gap]
    
    subgraph D [The Bio-Digital Gap]
        D1[PhysioCore] --> D2[Matrix]
        D2 --> D3[Qualia]
        D4[Agentic RAG] --> D5[Deep State]
        D1 --> D5
        D2 --> D5
        D3 --> D5
        D4 --> D5
    end
    
    D -->|Bio-State + Memories| E{LLM Phase 2:<br/>Reasoning}
    E -->|Text Response| F[User]
    E -->|propose_episodic_memory| G[MSP]
    G -->|Archive| H[(Episodic Memory)]
    G -->|Index| I[(Neo4j Graph)]
```

---

## Memory System Structure

```mermaid
graph LR
    subgraph "Layer 1: Episodic"
        EP[episodes_user/<br/>Fast Retrieval]
        EL[episodes_llm/<br/>LLM Audit]
    end
    
    subgraph "Layer 2: Semantic"
        SL[semantic_log.jsonl]
        SB[Semantic Buffer<br/>Session-Scoped]
    end
    
    subgraph "Layer 3: Sensory"
        SS[sensory_log.jsonl<br/>Bio Telemetry]
    end
    
    subgraph "Layer 7: User Block"
        UB[Grounding Facts<br/>Persistent Truth]
        CD[Conflict Detector]
    end
    
    subgraph "Layer 10: State"
        ST[Active State<br/>Current Turn]
    end
    
    EP -->|RAG Query| Vector[(Vector DB)]
    EL -->|Pattern Analysis| NexusMind[NexusMind<br/>Future]
    SB -->|Verify| CD
    CD -->|Check| UB
    UB -->|Ground Truth| EP
```

---

## Token Cost Comparison

| Context Type | Tokens | Visual? | Dynamic? |
|--------------|--------|---------|----------|
| **Current**: Full system_overview.md | 4000 | ❌ | ❌ |
| **Tier 1**: core_identity.md | 300 | ❌ | ✅ (bio-state) |
| **Tier 2**: This diagram (mermaid text) | 200 | ✅ | ❌ |
| **Tier 2**: This diagram (rendered image) | 500-800 | ✅ | ❌ |
| **Hybrid**: Core Identity + Diagram (text) | 500 | ✅ | ✅ |
| **Hybrid**: Core Identity + Diagram (image) | 800-1100 | ✅ | ✅ |

**Recommended**: Core Identity (300) + Mermaid Text (200) = **500 tokens**  
**Savings**: 87.5% reduction from 4000 tokens

---

## Usage Strategy

### Option A: Mermaid as Text (Most Efficient)

- Include mermaid code block in prompt
- LLM can "visualize" the flow
- **500 tokens total**

### Option B: Pre-Rendered Image

- Render mermaid to PNG first
- Inject as image
- **800-1100 tokens total** (still 72% savings)

### Recommendation: **Option A (Mermaid Text)**

- Cheaper (500 vs 4000 tokens)
- LLM understands mermaid diagrams well
- Can be generated/updated dynamically
