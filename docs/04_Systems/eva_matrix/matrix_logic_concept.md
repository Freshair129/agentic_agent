# EVA Matrix: Concept & Pseudocode

# Purpose: Documentation of the mental model and logical flow for the Psych-State Engine

> [!NOTE]
> **Status**: VERIFIED STABLE (v9.6.2 Audit Complete)
> **Coupling**: Fully verified with `PhysioCore` via `verify_matrix_coupling.py`.

## Mental Model

The EVA Matrix is not just a database of numbers; it is a **Fluid Dynamical System**.
Every input signal (hormones, user stimulus) acts as a "force" that pulls the current state (a point in 9D space) toward a new position.

## Dynamic Structure: 5+2+2 Model

- **Core Axes (5)**: Stress, Warmth, Drive, Clarity, Joy.
- **Modifiers (2)**: Arousal, Valence (Auto-calculated).
- **Control (2)**: Momentum, Stability.

## Pseudocode: Update Cycle

```python
def update_matrix(current_state, neural_inputs, delta_time):
    # 1. Calculate Stimulus Vector
    # Convert hormones (cortisol, adrenaline) into raw emotional forces.
    stimulus_force = calculate_biocognitive_force(neural_inputs)
    
    # 2. Apply Inertia
    # Emotions don't change instantly.
    target_state = current_state + (stimulus_force * momentum_coefficient)
    
    # 3. Validation & Coherence
    # Apply rules from validation/matrix_coherence_rules.yaml
    final_state = apply_coherence_filters(target_state)
    
    # 4. Persistence
    save_to_local_cache(final_state)
    return final_state
```

## Axis Descriptions (Verified)

- **Stress**: Linked to Cortisol (+), Adrenaline (+), and Noradrenaline (+).
- **Warmth**: Linked to Oxytocin (+) and Serotonin (+).
- **Stability**: Decreased significantly by Adrenaline surges; maintained by GABA. Inverse link to acute reflex intensity.
- **Joy**: Driven by Dopamine and Endorphin spikes.
