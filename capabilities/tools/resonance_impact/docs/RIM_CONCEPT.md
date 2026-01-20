# Resonance Impact Concept & Integration Guide

## Overview

The **Resonance Impact Model (RIM)** translates the abstract Resonance Index into actionable physiological and cognitive multipliers.

## Core Concept

### What is Impact?
RIM converts RI (0.0-1.0) into 3 categories:
1. **Low** - Minimal physiological response
2. **Medium** - Standard response
3. **High** - Amplified response (trauma/ecstasy)

## Impact Curves

### Thresholds
```
RI < 0.3  → Low Impact
0.3 ≤ RI < 0.8 → Medium Impact
RI ≥ 0.8  → High Impact
```

### Multipliers by Level

| Level | Hormone Release | Receptor Sensitivity | Emotional Weight |
|-------|----------------|---------------------|------------------|
| **Low** | 0.5x | 0.7x | 0.6x |
| **Medium** | 1.0x | 1.0x | 1.0x |
| **High** | 1.8x | 1.5x | 1.8x |

## Bus Integration

### Subscribe
- `bus:knowledge` (RI output)

### Publish
- `bus:physical` (RIM multipliers)

### Consumers
1. **PhysioController** - Applies multipliers to hormone secretion
2. **Receptor Engine** - Adjusts signal transduction sensitivity
3. **EVA Matrix** - Amplifies emotional state intensity

## Use Cases

### 1. Trauma Response (High RI + Negative)
```
High RI (0.95) + Fear/Anger
→ RIM: High Impact
→ Multipliers: 1.8x hormone, 1.5x receptor
→ Result: Intense stress response (cortisol spike)
```

### 2. Ecstatic Joy (High RI + Positive)
```
High RI (0.92) + Joy/Love
→ RIM: High Impact
→ Multipliers: 1.8x hormone, 1.5x receptor
→ Result: Intense pleasure response (dopamine/oxytocin surge)
```

### 3. Routine Experience (Low RI)
```
Low RI (0.2) + Neutral
→ RIM: Low Impact
→ Multipliers: 0.5x hormone, 0.7x receptor
→ Result: Minimal physiological change
```

## Impact Curve Details

RIM uses **non-linear curves** for realistic response:

```python
def calculate_multiplier(ri, curve_type):
    if ri < 0.3:
        return baseline * 0.5  # Dampened
    elif ri < 0.8:
        return baseline * 1.0  # Normal
    else:
        return baseline * (1.0 + (ri - 0.8) * 4.0)  # Amplified
```

## API

### `calculate_impact(resonance_index)`
Returns: `{ impact_level: "High", multipliers: {...} }`

## Configuration

See `configs/rim_config.yaml` for:
- Impact thresholds
- Multiplier curves
- Saturation limits

---

**Related Modules**:
- [RI](../../resonance_index/docs/RI_CONCEPT.md) - Index calculator
- [PhysioCore](../../physio_core/README.md) - Hormone system
