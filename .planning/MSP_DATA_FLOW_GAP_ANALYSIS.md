# MSP Data Flow & Schema Gap Analysis

**Analysis Date:** 2026-01-19
**EVA Version:** v9.6.2 (Cognitive Flow 2.0)
**Analyst:** Claude Code
**Purpose:** Verify MSP schema coverage for all system data flows

---

## Executive Summary

This audit examined each EVA system to verify whether MSP (Memory & Soul Passport) schemas adequately capture all data produced during the cognitive cycle. The analysis revealed **significant gaps** in data logging, particularly for:

1. **PhysioCore detailed state** (vitals, receptor signals)
2. **Input stimulus from LLM** to PhysioCore
3. **RMS texture and trauma flags**
4. **Artifact Qualia depth and texture**
5. **EVA Matrix reflex directives**

### Critical Finding

While MSP has schemas for capturing bio-cognitive state (`State_Storage_Schema.json`), **episodic memory snapshots** (`State_Snapshot_Schema.json`) only capture high-level emotional summaries, missing the rich physiological and phenomenological details that generated those emotions.

---

## System-by-System Analysis

### 1. PhysioCore (Biological Simulation)

**Contract (from eva_master_registry.yaml):**
- **Inputs**: `StimulusVector` from Orchestrator via BUS_PHYSICAL
- **Outputs**: `HormonePanel` + `VitalsData` to BUS_PHYSICAL

**Actual Data Produced** (from physio_core.py:264-285):
```python
physio_payload = {
    "autonomic": {
        "sympathetic": float,
        "parasympathetic": float
    },
    "blood": {
        "ESC_H01_ADRENALINE": float,
        "ESC_H02_CORTISOL": float,
        "ESC_N02_DOPAMINE": float,
        # ... ~20 hormones
    },
    "vitals": {
        "bpm": float,           # Heart rate
        "rpm": float,           # Respiration rate
        "vagus_tone": float     # Parasympathetic activation
    },
    "receptor_signals": {
        # Transduced hormone signals
    },
    "timestamp": ISO8601
}
```

#### MSP Schema Coverage

| Data Field | State_Storage_Schema | State_Snapshot_Schema | Episodic_Memory_Schema |
|------------|---------------------|----------------------|----------------------|
| blood (hormone panel) | ✅ Captured | ❌ **Missing** | ❌ **Missing** |
| autonomic (symp/para) | ✅ Captured | ❌ **Missing** | ❌ **Missing** |
| vitals (bpm, rpm, vagus) | ❌ **MISSING** | ❌ **Missing** | ❌ **Missing** |
| receptor_signals | ❌ **MISSING** | ❌ **Missing** | ❌ **Missing** |
| **Input: StimulusVector** | ❌ **MISSING** | ❌ **Missing** | ❌ **Missing** |

#### Gap Severity: **HIGH**

**Impact:**
- **Lost**: Detailed vitals tracking (heart rate, breathing, vagus tone)
- **Lost**: Receptor signal transduction data (how hormones become neural signals)
- **Lost**: Input stimulus from LLM (what triggered the physiological response)

**Why it matters:**
- Cannot reconstruct *why* hormones changed without stimulus logging
- Cannot track cardiovascular stress patterns without vitals
- Cannot debug PhysioCore → Matrix signal chain without receptor_signals

---

### 2. EVA Matrix (Psychological State Engine)

**Contract:**
- **Inputs**: `HormonePanel`, `VitalsData` from PhysioCore via BUS_PHYSICAL
- **Outputs**: `EmotionalState (9D)` to BUS_PSYCHOLOGICAL

**Actual Data Produced** (from eva_matrix.py:114-123):
```python
matrix_payload = {
    "matrix_state": {
        "axes_9d": {
            "stress": float,
            "warmth": float,
            "drive": float,
            "clarity": float,
            "joy": float,
            "stability": float,
            "orientation": float,
            "primary": str,
            "secondary": str
        },
        "emotion_label": str,
        "momentum": {
            "intensity": float
        }
    },
    "reflex_directives": {},  # Fast-path commands
    "timestamp": ISO8601
}
```

#### MSP Schema Coverage

| Data Field | State_Storage_Schema | State_Snapshot_Schema | Episodic_Memory_Schema |
|------------|---------------------|----------------------|----------------------|
| axes_9d (all 9 dimensions) | ✅ Captured | ✅ Captured (5 dims) | ✅ Captured (5 dims) |
| emotion_label | ✅ Captured | ✅ Captured | ✅ Captured |
| momentum | ✅ Captured | ❌ **Missing** | ❌ **Missing** |
| reflex_directives | ❌ **MISSING** | ❌ **Missing** | ❌ **Missing** |

#### Gap Severity: **MEDIUM**

**Impact:**
- **Lost**: Reflex directives (fast-path emotional responses)
- **Lost**: Momentum in episodic snapshots (rate of emotional change)

**Why it matters:**
- Reflex directives represent immediate, pre-cognitive responses that bypass deliberation
- Momentum is critical for understanding emotional trajectories over time

---

### 3. RMS (Resonance Memory System)

**Contract:**
- **Subscribes to**: BUS_ALL (monitors all channels)
- **Outputs**: Memory encoding metadata

**Actual Data Produced** (from rms.py:158-172):
```python
rms_output = {
    "matrix_snapshot": dict,      # Copy of EVA state
    "Resonance_index": float,     # RI total score
    "memory_encoding_level": str, # L0_trace | L1_light | L2_standard | L3_deep | L4_trauma
    "memory_color": str,          # Hex color (#RRGGBB)
    "resonance_texture": {        # 5D color axes
        "stress": float,
        "warmth": float,
        "clarity": float,
        "drive": float,
        "calm": float
    },
    "qualia": {
        "intensity": float
    },
    "reflex": {
        "threat_level": float
    },
    "trauma_flag": bool,
    "timestamp": ISO8601
}
```

#### MSP Schema Coverage

| Data Field | State_Storage_Schema | State_Snapshot_Schema | Episodic_Memory_Schema |
|------------|---------------------|----------------------|----------------------|
| Resonance_index | N/A | ✅ Captured | ✅ Captured |
| memory_encoding_level | N/A | ✅ Captured | ✅ Captured |
| memory_color | N/A | ✅ Captured | ✅ Captured |
| resonance_texture (5D) | ❌ **MISSING** | ❌ **Missing** | ❌ **Missing** |
| qualia.intensity | N/A | ✅ Captured | ✅ Captured |
| reflex.threat_level | N/A | ✅ Captured | ✅ Captured |
| trauma_flag | ❌ **MISSING** | ❌ **Missing** | ❌ **Missing** |

#### Gap Severity: **MEDIUM**

**Impact:**
- **Lost**: 5D resonance texture (detailed color composition)
- **Lost**: Trauma flag (critical for memory protection)

**Why it matters:**
- Resonance texture provides nuanced emotional coloring beyond simple intensity
- Trauma flag is essential for trauma-informed memory processing (ADR compliance)

---

### 4. Artifact Qualia (Phenomenology Engine)

**Contract:**
- **Publishes to**: BUS_PHENOMENOLOGICAL
- **Inputs**: Psychological state from EVA Matrix

**Actual Data Produced** (from artifact_qualia.py:127-147):
```python
qualia_snapshot = {
    "intensity": float,      # Overall phenomenal intensity
    "tone": str,             # Qualitative feel (warm, sharp, soft, etc.)
    "coherence": float,      # How unified the experience feels
    "depth": float,          # Existential depth/meaningfulness
    "texture": {             # Multi-dimensional feel
        "grain": float,
        "flow": float,
        "weight": float,
        # ... additional texture dimensions
    },
    "timestamp": ISO8601
}
```

#### MSP Schema Coverage

| Data Field | State_Storage_Schema | State_Snapshot_Schema | Episodic_Memory_Schema |
|------------|---------------------|----------------------|----------------------|
| intensity | ✅ Captured | ✅ Captured | ✅ Captured |
| tone | ✅ Captured | ❌ **Missing** | ❌ **Missing** |
| coherence | ✅ Captured | ❌ **Missing** | ❌ **Missing** |
| depth | ❌ **MISSING** | ❌ **Missing** | ❌ **Missing** |
| texture (detailed) | ❌ **MISSING** | ❌ **Missing** | ❌ **Missing** |

#### Gap Severity: **MEDIUM-HIGH**

**Impact:**
- **Lost**: Phenomenological depth (existential significance)
- **Lost**: Qualitative tone and detailed texture
- **Partial**: State_Storage has tone/coherence, but episodic memory doesn't

**Why it matters:**
- Qualia depth represents the "weight" of experiences (philosophical consciousness)
- Texture provides rich phenomenological detail beyond numeric intensity
- Tone describes the *feel* of experience (warm vs cold, sharp vs soft)

---

## Schema-Level Findings

### State_Storage_Schema.json (Real-Time State)

**Purpose:** Active bio-cognitive metrics (Layer 08) - runtime working memory

**Coverage:**
- ✅ PhysioCore: blood, autonomic (partial)
- ✅ EVA Matrix: axes_9d, emotion_label, momentum
- ✅ Artifact Qualia: intensity, tone, coherence

**Gaps:**
- ❌ PhysioCore vitals (bpm, rpm, vagus_tone)
- ❌ PhysioCore receptor_signals
- ❌ Artifact Qualia depth and texture

**Verdict:** Good for real-time state, but missing critical physiological telemetry.

---

### State_Snapshot_Schema.json (Episodic Memory Snapshots)

**Purpose:** Bio-cognitive state within episodic memory episodes

**Coverage:**
- ✅ EVA_matrix (5 core dimensions only)
- ✅ Resonance_index
- ✅ memory_encoding_level
- ✅ memory_color
- ✅ qualia.intensity
- ✅ reflex.threat_level

**Gaps:**
- ❌ PhysioCore state (blood, autonomic, vitals) - **CRITICAL**
- ❌ EVA Matrix momentum
- ❌ RMS resonance_texture
- ❌ RMS trauma_flag
- ❌ Artifact Qualia tone, coherence, depth, texture

**Verdict:** Only captures *emotional output*, not the *biological/phenomenological process* that created it.

---

### Episodic_Memory_Schema_v2.json (Long-Term Memory)

**Purpose:** Full episodic memory structure with turns and context

**Coverage:**
- ✅ References State_Snapshot_Schema (inherits its gaps)
- ✅ User turns with affective_inference
- ✅ LLM turns with epistemic_mode

**Gaps:**
- ❌ Same gaps as State_Snapshot_Schema
- ❌ No dedicated "stimulus" field for LLM→PhysioCore input

**Verdict:** Good for conversation structure, poor for bio-cognitive transparency.

---

## Critical Missing Data

### 1. Input Stimulus Logging (HIGHEST PRIORITY)

**What's missing:**
- LLM→PhysioCore stimulus vector (what triggered the biological response)

**Current state:**
- PhysioCore receives `eva_stimuli` dict with stimulus mappings
- These are applied via `stimulus_map` (physio_core.py:206-211)
- **NOT logged anywhere in MSP**

**Impact:**
- Cannot debug "Why did EVA get stressed?" questions
- Cannot trace emotional reactions back to conversational triggers
- Breaks causal chain: User Input → Stimulus → Hormones → Emotions

**Recommendation:**
Create `Stimulus_Input_Schema.json` or add to episodic turns:
```json
{
  "llm_stimulus_output": {
    "eva_stimuli": {
      "threat": 0.7,
      "novelty": 0.3,
      "social_warmth": 0.5
    },
    "timestamp": "ISO8601"
  }
}
```

---

### 2. PhysioCore Vitals Tracking

**What's missing:**
- bpm (heart rate)
- rpm (respiration rate)
- vagus_tone (parasympathetic activation)

**Current state:**
- Calculated by VitalsEngine (physio_core/logic/vitals/VitalsEngine.py)
- Published to MSP via `set_active_state("physio_state")`
- But `State_Storage_Schema.physio_state` doesn't include vitals field

**Impact:**
- Cannot track cardiovascular stress patterns
- Cannot correlate breathing rate with anxiety
- Cannot monitor vagal brake function (trauma recovery)

**Recommendation:**
Update `State_Storage_Schema.json`:
```json
{
  "physio_state": {
    "blood": {...},
    "autonomic": {...},
    "vitals": {
      "bpm": {"type": "number"},
      "rpm": {"type": "number"},
      "vagus_tone": {"type": "number"}
    }
  }
}
```

---

### 3. Phenomenological Texture Loss

**What's missing:**
- Artifact Qualia depth, tone, coherence, texture (in episodic snapshots)
- RMS resonance_texture (5D color axes)

**Current state:**
- Generated by systems but only `intensity` captured in episodic memory

**Impact:**
- Memories lose phenomenological richness
- Cannot distinguish between "sharp anxiety" vs "dull dread"
- Cannot retrieve memories by qualitative feel

**Recommendation:**
Expand `State_Snapshot_Schema.qualia`:
```json
{
  "qualia": {
    "intensity": {"type": "number"},
    "tone": {"type": "string"},
    "coherence": {"type": "number"},
    "depth": {"type": "number"},
    "texture": {"type": "object"}
  }
}
```

---

### 4. Reflex & Fast-Path Data

**What's missing:**
- EVA Matrix reflex_directives
- RMS trauma_flag

**Current state:**
- Generated but not persisted in episodic memory

**Impact:**
- Cannot track pre-cognitive emotional responses
- Cannot audit trauma protection triggers
- Lose visibility into ANS reflex pathways

**Recommendation:**
Add to `State_Snapshot_Schema.json`:
```json
{
  "reflex_directives": {"type": "object"},
  "trauma_flag": {"type": "boolean"}
}
```

---

## Data Flow Compliance Matrix

| System | Produces Data | MSP Schema Exists | Schema Complete | Episodic Captured | **Status** |
|--------|---------------|-------------------|-----------------|-------------------|------------|
| PhysioCore | Hormones, Autonomic, Vitals, Receptors | ✅ State_Storage | ⚠️ Partial (no vitals) | ❌ Not in State_Snapshot | **GAP** |
| EVA Matrix | 9D Emotions, Momentum, Reflex | ✅ State_Storage | ⚠️ Partial (no reflex) | ⚠️ Partial (no momentum) | **GAP** |
| RMS | RI, Encoding Level, Color, Texture | ✅ State_Snapshot | ⚠️ Partial (no texture) | ⚠️ Partial (no texture) | **GAP** |
| Artifact Qualia | Intensity, Tone, Coherence, Depth, Texture | ✅ State_Storage | ⚠️ Partial (no depth/texture) | ❌ Only intensity | **GAP** |
| **Orchestrator** | **Stimulus to PhysioCore** | ❌ **NO SCHEMA** | ❌ **MISSING** | ❌ **MISSING** | **CRITICAL** |

---

## Recommendations

### Immediate Actions (Phase 1)

1. **Create Stimulus Logging Schema**
   - Add to `Episodic_Memory_Schema_v2.json` under `turn_llm`:
     ```json
     "stimulus_output": {
       "eva_stimuli": {"type": "object"},
       "timestamp": {"type": "string"}
     }
     ```

2. **Expand State_Storage_Schema**
   - Add `vitals` field to `physio_state`
   - Add `depth` and `texture` to `qualia_state`

3. **Expand State_Snapshot_Schema**
   - Add full `qualia` structure (tone, coherence, depth, texture)
   - Add `resonance_texture` from RMS
   - Add `trauma_flag` from RMS
   - Add `reflex_directives` from EVA Matrix

### Medium-Term Actions (Phase 2)

4. **Implement Logging Hooks**
   - Hook Orchestrator's `process_turn()` to log stimulus output
   - Hook PhysioCore's `step()` to log vitals
   - Hook RMS's `process()` to log full texture and trauma flag

5. **Create Schema Migration Tool**
   - Tool to backfill missing fields in existing episodic memories
   - Default values for unavailable historical data

6. **Add Validation Layer**
   - Schema validators for all MSP write operations
   - Log warnings when data is dropped due to schema gaps

### Long-Term Actions (Phase 3)

7. **Implement Data Lineage Tracking**
   - Track data flow: User Input → Stimulus → Hormones → Emotions → Qualia
   - Enable "Explain this emotion" queries with full causal chain

8. **Create Data Observatory Dashboard**
   - Real-time visualization of data flow gaps
   - Alerts when critical data is not being captured

9. **Audit Tool Development**
   - Automated schema coverage checker (like this report, but continuous)
   - Integration with CI/CD to prevent schema regressions

---

## Conclusion

MSP's current schema design captures **high-level emotional summaries** well, but **loses rich biological and phenomenological details** in episodic memory. The critical gap is **input stimulus logging** (LLM → PhysioCore), without which the entire causal chain is broken.

**Impact Assessment:**
- **HIGH**: Cannot debug emotional responses without stimulus logging
- **HIGH**: Vitals data loss prevents cardiovascular/stress tracking
- **MEDIUM**: Phenomenological texture loss reduces memory richness
- **MEDIUM**: Reflex/trauma flag loss hinders ANS/trauma analysis

**Next Steps:**
1. Implement stimulus logging immediately (Priority 1)
2. Expand State_Snapshot_Schema with missing fields (Priority 1)
3. Create migration path for existing memories (Priority 2)
4. Build continuous monitoring for schema compliance (Priority 3)

---

**Report Generated:** 2026-01-19
**Audit Tool:** Claude Code Manual Analysis
**Files Analyzed:** 15 schemas, 4 system codebases, eva_master_registry.yaml
**Total Gaps Identified:** 18 missing fields across 4 systems
