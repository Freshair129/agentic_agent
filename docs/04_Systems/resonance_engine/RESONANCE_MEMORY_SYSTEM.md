# 📡 AuthDoc: Resonance Memory System (RMS)

> **Status**: OPERATIONAL (v9.6.2 Backfill)
> **Governs**: `resonance_memory_system/`

## 1. Core Concept: Lived Experience as Hash
In EVA 9.1.0, memory is not just text storage. It is the cryptographic proof of **Lived Experience**.
Every memory entry must satisfy the **Resonance Equation**:
`Memory = (Stimulus + Physio_State + Matrix_State + Qualia) * Time`

## 2. Architecture Layers / Components

### 2.1 Layer 1: The Latching Stream (Short-Term / Working Memory)
*   **Location**: `Resonance Bus (Active State)`
*   **Role**: Provides immediate context for the next cognitive cycle.
*   **Persistence**: Holds state between ticks (Living Presence), not persisted to disk in this layer.

### 2.2 Layer 2: The Audit Log (Sensory Buffer)
*   **Location**: `consciousness/audit_logs/audit_log.jsonl`
*   **Role**: "Flight Recorder" / Black Box.
*   **Persistence**: Append-only log of every bus signal.

### 2.3 Layer 3: The Crystal Archives (Long-Term Memory)
*   **Location**: `e:\The Human Algorithm\T2\agent\consciousness`
*   **Role**: Permanent storage of validated memories via [MSP](file:///e:/The%20Human%20Algorithm/T2/agent/docs/04_Systems/memory_n_soul_passport/msp_overview.md).

## 3. Modular Implementation (V9 Hierarchy)

### 3.1 Resonance Encoding Module (`Resonance_Encoding_Module`)

#### Node: `ColorGenerationNode`
- **Role**: Maps the 9D Psychological Matrix axes to the 5D RMS Color axes (Stress, Warmth, Clarity, Drive, Calm).
- **RGB Calculation**: Merges axes into a HEX color based on a weighted blend of Intensity and Clarity.

#### Node: `IntensityCalculationNode`
- **Role**: Quantifies the overall "impact" of an interaction.
- **Core Math**: `final_intensity = ((arousal * 0.6 + stress * 0.4) + impact_boost) * trend_mod`.

#### Node: `TraumaProtectionNode`
- **Role**: Filters and dims memory encoding during high-threat events to prevent "system shock".
- **Trigger**: `reflex_state.threat_level > 0.85`.

### 3.2 Latching Module (`Latching_Module`)

#### Node: `TemporalSmoothingNode`
- **Role**: Recursive smoothing of affective signals (EMA).

#### Node: `OutputPackagingNode`
- **Role**: Formats the final state snapshot for the MSP archival process.

## 4. Key Metrics
*   **RIM (Resonance Impact Model)**: Calculates the *Immediate Impact* of an event.
    *   **Low**: < 0.3 (Routine, may be discarded).
    *   **Medium**: 0.3 - 0.8 (Standard episodic).
    *   **High**: > 0.8 (Traumatic/Ecstatic, high priority).
*   **RI (Resonance Index)**: Global "Vibe Score" (0.0 - 1.0) merging Bio+Psych+Context.

## 5. Directory Structure
```
resonance_memory_system/
├── configs/                # RMS Configs
├── contract/               # Interface Contracts
├── schema/                 # Validation Schemas
└── Module/                 # V9 Logic Folders
    ├── encoding_module/
    └── latching_module/
```
