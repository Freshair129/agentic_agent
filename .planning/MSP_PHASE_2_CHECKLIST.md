# MSP Logging Implementation Checklist - Phase 2

**Goal:** Ensure new schema fields are populated by system components.

## Task 2.1: Hook System Outputs

### Step 2.1.1: Verify PhysioCore Output

**File:** `physio_core/physio_core.py`
**Action:** Audit `get_state()` or `step()` output
**Check:** Ensure `vitals` (bpm, rpm, vagus_tone) are present in the returned dictionary.

**Validation:**
```python
# Inspect PhysioCore.py manually or run:
python -c "from physio_core.physio_core import PhysioCore; print('Auditing PhysioCore output structure...')"
```

### Step 2.1.2: Hook EVA Matrix Reflex Directives

**File:** `eva_matrix/eva_matrix.py`
**Action:** Update `step()` or `process()` to log `reflex_directives` to MSP.
**Change:**
```python
if self.msp:
    self.msp.set_active_state("reflex_directives", result.get("reflex_directives", {}))
```

### Step 2.1.3: Hook RMS Resonance Texture

**File:** `resonance_memory_system/rms.py`
**Action:** Ensure `process_resonance()` output includes `resonance_texture` and `trauma_flag`.
**Note:** These might already be in the returned object, we just need to confirm MSP reads them later.

### Step 2.1.4: Hook Artifact Qualia

**File:** `artifact_qualia/artifact_qualia.py`
**Action:** Ensure `last_qualia` output includes `depth` and `texture`.

---

## Task 2.2: Update MSP Write Logic

### Step 2.2.1: Update write_episodic_memory()

**File:** `memory_n_soul_passport/memory_n_soul_passport_engine.py`
**Action:** Modify `write_episodic_memory` to construct a full `state_snapshot` using active states from all systems.

**Code Update:**
```python
    # Build state snapshot from active state
    state_snapshot = {
        "EVA_matrix": {
            **self.active_state.get("matrix_state", {}).get("axes_9d", {}),
            "emotion_label": self.active_state.get("matrix_state", {}).get("emotion_label", "Neutral"),
            "momentum": self.active_state.get("matrix_state", {}).get("momentum", {})  # NEW
        },
        "Resonance_index": self.active_state.get("resonance_index", 0.0),
        "memory_encoding_level": self.active_state.get("memory_encoding_level", "L1_light"),
        "memory_color": self.active_state.get("memory_color", "#808080"),
        "qualia": {
            "intensity": self.active_state.get("qualia_state", {}).get("intensity", 0.3),
            "tone": self.active_state.get("qualia_state", {}).get("tone"),  # NEW
            "coherence": self.active_state.get("qualia_state", {}).get("coherence"),  # NEW
            "depth": self.active_state.get("qualia_state", {}).get("depth"),  # NEW
            "texture": self.active_state.get("qualia_state", {}).get("texture", {})  # NEW
        },
        "resonance_texture": self.active_state.get("resonance_texture", {}),  # NEW
        "trauma_flag": self.active_state.get("trauma_flag", False),  # NEW
        "reflex_directives": self.active_state.get("reflex_directives", {}),  # NEW
        "reflex": {
            "threat_level": self.active_state.get("threat_level", 0.0)
        }
    }
```

---

## Phase 2 Verification

**File:** `tests/test_msp_phase2.py`
**Action:** Create integration test simulating full data flow.
