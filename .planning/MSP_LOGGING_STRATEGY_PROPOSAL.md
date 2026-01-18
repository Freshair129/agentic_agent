# MSP Logging & Tracking Strategy Proposal

**Date:** 2026-01-19
**Version:** 1.0
**Status:** Proposed (Pending Implementation)
**Related:** MSP_DATA_FLOW_GAP_ANALYSIS.md

---

## Executive Summary

This proposal outlines a phased implementation strategy to address the 18 data logging gaps identified in the MSP Data Flow Gap Analysis. The strategy prioritizes:

1. **Stimulus logging** (breaks causal chain if missing)
2. **Schema expansion** (capture missing fields)
3. **Validation enforcement** (prevent future data loss)
4. **Monitoring infrastructure** (continuous gap detection)

**Timeline:** 3 phases over ~4-6 weeks
**Risk Level:** LOW (additive changes, backward compatible)
**Breaking Changes:** None (schema expansion only)

---

## Phase 1: Critical Gaps (Week 1-2)

**Goal:** Fix data loss that breaks core functionality

### 1.1 Stimulus Input Logging

**Problem:** LLM→PhysioCore stimulus vector not logged anywhere.

**Solution:** Create dedicated schema and hook Orchestrator output.

#### Implementation Steps

**Step 1.1.1: Create Schema**

Create `memory_n_soul_passport/schema/Stimulus_Output_Schema.json`:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Stimulus_Output_Schema",
  "description": "Schema for LLM-generated stimulus vectors sent to PhysioCore",
  "type": "object",
  "required": [
    "turn_id",
    "eva_stimuli",
    "timestamp"
  ],
  "properties": {
    "turn_id": {
      "type": "string",
      "description": "Reference to LLM turn that generated this stimulus"
    },
    "eva_stimuli": {
      "type": "object",
      "description": "Stimulus vector mapping (stimulus_id -> intensity)",
      "additionalProperties": {
        "type": "number",
        "minimum": -1.0,
        "maximum": 1.0
      },
      "examples": [
        {
          "threat": 0.7,
          "novelty": 0.3,
          "social_warmth": 0.5,
          "cognitive_load": 0.6
        }
      ]
    },
    "stimulus_context": {
      "type": "object",
      "description": "Optional contextual metadata",
      "properties": {
        "reasoning": {
          "type": "string",
          "description": "Why LLM generated these stimuli"
        },
        "confidence": {
          "type": "number",
          "description": "LLM confidence in stimulus assessment"
        }
      }
    },
    "timestamp": {
      "type": "string",
      "format": "date-time"
    }
  }
}
```

**Step 1.1.2: Update Episodic Memory Schema**

Modify `memory_n_soul_passport/schema/Episodic_Memory_Schema_v2.json`:

```json
{
  "turn_llm": {
    "type": "object",
    "properties": {
      // ... existing fields ...
      "stimulus_output": {
        "$ref": "Stimulus_Output_Schema.json#"
      }
    }
  }
}
```

**Step 1.1.3: Hook Orchestrator**

In `orchestrator/orchestrator.py`, after LLM generates stimulus:

```python
def process_turn(self, user_input: str):
    # ... existing LLM call ...

    # Extract stimulus from LLM response (function calling)
    eva_stimuli = self._extract_eva_stimuli(llm_response)

    # NEW: Log stimulus to MSP BEFORE sending to PhysioCore
    if self.msp and eva_stimuli:
        stimulus_data = {
            "turn_id": self.current_turn_id,
            "eva_stimuli": eva_stimuli,
            "stimulus_context": {
                "reasoning": llm_response.get("stimulus_reasoning"),
                "confidence": llm_response.get("confidence", 0.5)
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        self.msp.log_stimulus_output(stimulus_data)  # NEW METHOD

    # Send to PhysioCore
    if self.physio:
        self.physio.step(eva_stimuli=eva_stimuli, dt=0.033)
```

**Step 1.1.4: Add MSP Method**

In `memory_n_soul_passport/memory_n_soul_passport_engine.py`:

```python
def log_stimulus_output(self, stimulus_data: Dict[str, Any]):
    """
    Log LLM-generated stimulus vectors for causal chain tracking.
    """
    # Validate against schema
    self._validate_schema(stimulus_data, "Stimulus_Output_Schema.json")

    # Store in active turn buffer
    if not hasattr(self, '_current_turn_stimulus'):
        self._current_turn_stimulus = []
    self._current_turn_stimulus.append(stimulus_data)

    # Will be written to episodic memory during turn finalization
```

**Files Modified:**
- ✅ `memory_n_soul_passport/schema/Stimulus_Output_Schema.json` (NEW)
- ✅ `memory_n_soul_passport/schema/Episodic_Memory_Schema_v2.json` (UPDATE)
- ✅ `orchestrator/orchestrator.py` (UPDATE)
- ✅ `memory_n_soul_passport/memory_n_soul_passport_engine.py` (UPDATE)

---

### 1.2 Expand State_Storage_Schema (Vitals)

**Problem:** PhysioCore vitals (bpm, rpm, vagus_tone) not captured in real-time state.

**Solution:** Add `vitals` field to `physio_state`.

#### Implementation Steps

**Step 1.2.1: Update Schema**

Modify `memory_n_soul_passport/schema/State_Storage_Schema.json`:

```json
{
  "physio_state": {
    "type": "object",
    "properties": {
      "blood": { /* existing */ },
      "autonomic": { /* existing */ },
      "vitals": {
        "type": "object",
        "description": "Cardiovascular and respiratory vitals",
        "properties": {
          "bpm": {
            "type": "number",
            "description": "Heart rate (beats per minute)",
            "minimum": 40,
            "maximum": 200
          },
          "rpm": {
            "type": "number",
            "description": "Respiration rate (breaths per minute)",
            "minimum": 8,
            "maximum": 40
          },
          "vagus_tone": {
            "type": "number",
            "description": "Parasympathetic activation (0-1)",
            "minimum": 0.0,
            "maximum": 1.0
          }
        },
        "required": ["bpm", "rpm", "vagus_tone"]
      },
      "receptor_signals": {
        "type": "object",
        "description": "Transduced hormone → neural signals",
        "additionalProperties": {
          "type": "object",
          "additionalProperties": {
            "type": "number"
          }
        }
      }
    },
    "required": ["blood", "autonomic", "vitals"]
  }
}
```

**Step 1.2.2: Update PhysioCore Output**

In `physio_core/physio_core.py`, modify payload:

```python
# Current (line 264)
physio_payload = {
    "autonomic": ans_state,
    "blood": blood_levels,
    "vitals": vitals_state,  # Already exists!
    "receptor_signals": receptor_signals,
    "timestamp": datetime.now().isoformat()
}
```

**Good news:** PhysioCore already sends vitals! MSP just needs to store them.

**Step 1.2.3: Update MSP Write**

In `memory_n_soul_passport_engine.py`, ensure vitals are written:

```python
def set_active_state(self, key: str, value: Any):
    # ... existing code ...

    # Ensure vitals are included when physio_state is set
    if key == "physio_state" and "vitals" in value:
        # Validate vitals schema
        self._validate_vitals(value["vitals"])

    self.active_state[key] = value
```

**Files Modified:**
- ✅ `memory_n_soul_passport/schema/State_Storage_Schema.json` (UPDATE)
- ✅ `memory_n_soul_passport/memory_n_soul_passport_engine.py` (UPDATE)

---

### 1.3 Expand State_Snapshot_Schema (Core Fields)

**Problem:** Episodic memory snapshots missing critical fields.

**Solution:** Add missing fields from all systems.

#### Implementation Steps

**Step 1.3.1: Update Schema**

Modify `memory_n_soul_passport/schema/State_Snapshot_Schema.json`:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "EVA-State-Snapshot-Schema",
  "description": "EXPANDED: Now includes full bio-cognitive state",
  "type": "object",
  "required": [
    "EVA_matrix",
    "Resonance_index",
    "memory_encoding_level",
    "memory_color",
    "qualia"
  ],
  "properties": {
    "EVA_matrix": {
      /* existing 9D structure */
      "properties": {
        // ADD momentum
        "momentum": {
          "type": "object",
          "properties": {
            "intensity": {"type": "number"}
          }
        }
      }
    },
    "Resonance_index": { /* existing */ },
    "memory_encoding_level": { /* existing */ },
    "memory_color": { /* existing */ },

    // EXPAND qualia
    "qualia": {
      "type": "object",
      "required": ["intensity"],
      "properties": {
        "intensity": {"type": "number"},
        "tone": {
          "type": "string",
          "description": "Qualitative feel (warm, sharp, soft, heavy, etc.)"
        },
        "coherence": {
          "type": "number",
          "description": "Unity of experience (0-1)"
        },
        "depth": {
          "type": "number",
          "description": "Existential significance (0-1)"
        },
        "texture": {
          "type": "object",
          "description": "Multi-dimensional phenomenological texture",
          "additionalProperties": {"type": "number"}
        }
      }
    },

    // ADD resonance_texture
    "resonance_texture": {
      "type": "object",
      "description": "5D RMS color axes (detailed emotional coloring)",
      "properties": {
        "stress": {"type": "number"},
        "warmth": {"type": "number"},
        "clarity": {"type": "number"},
        "drive": {"type": "number"},
        "calm": {"type": "number"}
      }
    },

    // ADD trauma_flag
    "trauma_flag": {
      "type": "boolean",
      "description": "Whether trauma protection was triggered"
    },

    // ADD reflex_directives
    "reflex_directives": {
      "type": "object",
      "description": "Fast-path emotional commands from EVA Matrix",
      "additionalProperties": true
    },

    "reflex": { /* existing threat_level */ },
    "threat_level": { /* existing */ }
  }
}
```

**Files Modified:**
- ✅ `memory_n_soul_passport/schema/State_Snapshot_Schema.json` (UPDATE)

---

## Phase 2: Data Pipeline Integration (Week 3-4)

**Goal:** Ensure new schema fields are actually populated.

### 2.1 Hook All Systems

Update each system to pass full data to MSP:

#### PhysioCore
```python
# Already done - just ensure vitals are passed
```

#### EVA Matrix
```python
# eva_matrix/eva_matrix.py (line 104)
if self.msp:
    self.msp.set_active_state("matrix_state", {
        "axes_9d": self.axes_9d,
        "emotion_label": self.emotion_label,
        "momentum": self.momentum,  # Already here
        "timestamp": datetime.now(timezone.utc).isoformat()
    })
    # ADD: Log reflex directives separately
    self.msp.set_active_state("reflex_directives", result.get("reflex_directives", {}))
```

#### RMS
```python
# resonance_memory_system/rms.py (line 158)
# Already returns full structure - just ensure MSP stores it
# In MSP, when writing episodic memory, include:
# - resonance_texture
# - trauma_flag
```

#### Artifact Qualia
```python
# artifact_qualia/artifact_qualia.py (line 127)
result_dict = {
    "intensity": float(self.last_qualia.intensity),
    "tone": str(self.last_qualia.tone),            # Already here
    "coherence": float(self.last_qualia.coherence), # Already here
    "depth": float(self.last_qualia.depth),        # Already here
    "texture": {k: float(v) for k, v in self.last_qualia.texture.items()},  # Already here
    "timestamp": datetime.now(timezone.utc).isoformat()
}
# All fields already exist - just ensure MSP writes them to episodic memory
```

### 2.2 Update MSP Write Logic

In `memory_n_soul_passport_engine.py`, update `write_episodic_memory()`:

```python
def write_episodic_memory(self, episode_data: Dict[str, Any]):
    """Write episode with FULL state snapshot"""

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

    # Validate against updated schema
    self._validate_schema(state_snapshot, "State_Snapshot_Schema.json")

    # Write to episodic memory
    episode_data["state_snapshot"] = state_snapshot
    self._write_to_disk(episode_data)
```

**Files Modified:**
- ✅ `memory_n_soul_passport/memory_n_soul_passport_engine.py` (UPDATE)

---

## Phase 3: Validation & Monitoring (Week 5-6)

**Goal:** Prevent future data loss and monitor compliance.

### 3.1 Schema Validation Enforcement

**Step 3.1.1: Create Validator**

Create `memory_n_soul_passport/schema_validator.py`:

```python
import json
from pathlib import Path
from jsonschema import validate, ValidationError
from typing import Dict, Any

class MSPSchemaValidator:
    """Validates MSP data against JSON schemas"""

    def __init__(self, schema_dir: Path):
        self.schema_dir = schema_dir
        self.schemas = {}
        self._load_schemas()

    def _load_schemas(self):
        """Load all JSON schemas"""
        for schema_file in self.schema_dir.glob("*.json"):
            schema_name = schema_file.stem
            with open(schema_file, 'r', encoding='utf-8') as f:
                self.schemas[schema_name] = json.load(f)

    def validate(self, data: Dict[str, Any], schema_name: str) -> bool:
        """
        Validate data against schema.
        Returns True if valid, raises ValidationError if invalid.
        """
        if schema_name not in self.schemas:
            raise ValueError(f"Schema {schema_name} not found")

        try:
            validate(instance=data, schema=self.schemas[schema_name])
            return True
        except ValidationError as e:
            # Log detailed error
            print(f"[MSP Validator] Schema violation in {schema_name}:")
            print(f"  Path: {' -> '.join(str(p) for p in e.path)}")
            print(f"  Message: {e.message}")
            raise

    def validate_with_warnings(self, data: Dict[str, Any], schema_name: str) -> Dict[str, Any]:
        """
        Validate and return gaps (missing optional fields).
        """
        gaps = {"missing_fields": [], "type_mismatches": []}

        # ... implementation for soft validation ...

        return gaps
```

**Step 3.1.2: Integrate Validator**

In `memory_n_soul_passport_engine.py`:

```python
from .schema_validator import MSPSchemaValidator

class MSP:
    def __init__(self, ...):
        # ... existing init ...

        # NEW: Schema validator
        schema_dir = Path(__file__).parent / "schema"
        self.validator = MSPSchemaValidator(schema_dir)

        # Enable strict validation (set to False for graceful degradation)
        self.strict_validation = True

    def set_active_state(self, key: str, value: Any):
        # Validate before storing
        if self.strict_validation:
            if key == "physio_state":
                self.validator.validate(value, "State_Storage_Schema")
            elif key == "matrix_state":
                # Validate against schema subset
                pass

        self.active_state[key] = value
```

### 3.2 Data Gap Monitoring

**Step 3.2.1: Create Monitor**

Create `capabilities/tools/msp_monitor.py`:

```python
from typing import Dict, List, Any
from datetime import datetime

class MSPDataMonitor:
    """Monitors MSP data flow for gaps"""

    def __init__(self):
        self.gap_log = []

    def check_state_completeness(self, state: Dict[str, Any]) -> Dict[str, List[str]]:
        """
        Check if state has all expected fields.
        Returns dict of missing fields by category.
        """
        gaps = {
            "physio": [],
            "matrix": [],
            "qualia": [],
            "rms": []
        }

        # Check PhysioCore
        if "physio_state" in state:
            physio = state["physio_state"]
            if "vitals" not in physio:
                gaps["physio"].append("vitals")
            if "receptor_signals" not in physio:
                gaps["physio"].append("receptor_signals")

        # Check EVA Matrix
        if "matrix_state" in state:
            matrix = state["matrix_state"]
            if "momentum" not in matrix:
                gaps["matrix"].append("momentum")

        # Check Artifact Qualia
        if "qualia_state" in state:
            qualia = state["qualia_state"]
            if "depth" not in qualia:
                gaps["qualia"].append("depth")
            if "texture" not in qualia:
                gaps["qualia"].append("texture")

        # Log gaps
        if any(gaps.values()):
            self.gap_log.append({
                "timestamp": datetime.now().isoformat(),
                "gaps": gaps
            })

        return gaps

    def get_gap_report(self) -> Dict[str, Any]:
        """Generate gap statistics"""
        if not self.gap_log:
            return {"status": "healthy", "gaps": 0}

        # Count gap occurrences
        gap_counts = {}
        for log_entry in self.gap_log:
            for category, fields in log_entry["gaps"].items():
                for field in fields:
                    key = f"{category}.{field}"
                    gap_counts[key] = gap_counts.get(key, 0) + 1

        return {
            "status": "gaps_detected",
            "total_checks": len(self.gap_log),
            "gap_counts": gap_counts,
            "most_common_gap": max(gap_counts.items(), key=lambda x: x[1]) if gap_counts else None
        }
```

**Step 3.2.2: Add Monitor to MSP**

```python
from capabilities.tools.msp_monitor import MSPDataMonitor

class MSP:
    def __init__(self, ...):
        # ... existing init ...
        self.monitor = MSPDataMonitor()

    def write_episodic_memory(self, episode_data: Dict[str, Any]):
        # Check for gaps before writing
        gaps = self.monitor.check_state_completeness(self.active_state)

        if gaps and any(gaps.values()):
            print(f"[MSP Monitor] ⚠️ Writing episode with missing fields: {gaps}")

        # ... existing write logic ...
```

### 3.3 Continuous Auditing

**Step 3.3.1: Create Audit Script**

Create `scripts/audit_msp_coverage.py`:

```python
#!/usr/bin/env python3
"""
MSP Schema Coverage Audit Script
Checks if all system outputs are captured in MSP schemas.
"""

import yaml
import json
from pathlib import Path

def audit_system_contracts():
    """Check eva_master_registry.yaml contracts against MSP schemas"""

    registry_path = Path("registry/eva_master_registry.yaml")
    schema_dir = Path("memory_n_soul_passport/schema")

    # Load registry
    with open(registry_path, 'r', encoding='utf-8') as f:
        registry = yaml.safe_load(f)

    # Load schemas
    state_storage = json.load(open(schema_dir / "State_Storage_Schema.json"))
    state_snapshot = json.load(open(schema_dir / "State_Snapshot_Schema.json"))

    # Check each system
    for system in registry.get("systems", []):
        system_id = system.get("id")
        contracts = system.get("contracts", {})
        outputs = contracts.get("outputs", [])

        print(f"\n[System] {system_id}")
        for output in outputs:
            data_type = output.get("data")
            print(f"  Output: {data_type}")

            # Check if covered by schemas
            # ... implementation ...

    print("\n[Audit Complete]")

if __name__ == "__main__":
    audit_system_contracts()
```

**Step 3.3.2: Add to Pre-commit Hook**

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# Run MSP audit before commits

echo "Running MSP schema audit..."
python scripts/audit_msp_coverage.py

if [ $? -ne 0 ]; then
    echo "❌ MSP audit failed. Fix schema gaps before committing."
    exit 1
fi

echo "✅ MSP audit passed."
```

---

## Implementation Timeline

| Week | Phase | Tasks | Files Changed |
|------|-------|-------|---------------|
| 1 | Phase 1 Setup | Stimulus schema, vitals expansion | 4 files |
| 2 | Phase 1 Complete | State_Snapshot expansion, orchestrator hooks | 3 files |
| 3 | Phase 2 Start | System integration (PhysioCore, Matrix) | 4 files |
| 4 | Phase 2 Complete | MSP write logic update | 1 file |
| 5 | Phase 3 Start | Validator + monitor | 3 files (new) |
| 6 | Phase 3 Complete | Audit script + pre-commit hook | 2 files (new) |

**Total Files:** 17 (4 new, 13 updated)

---

## Testing Strategy

### Unit Tests

```python
# tests/test_msp_stimulus_logging.py
def test_stimulus_logging():
    """Test that stimulus vectors are logged"""
    msp = MSP()

    stimulus_data = {
        "turn_id": "T001",
        "eva_stimuli": {"threat": 0.7, "novelty": 0.3},
        "timestamp": datetime.now().isoformat()
    }

    msp.log_stimulus_output(stimulus_data)

    # Verify stored
    assert msp._current_turn_stimulus[-1] == stimulus_data
```

### Integration Tests

```python
# tests/test_full_cognitive_cycle.py
def test_end_to_end_data_capture():
    """Test full cycle: Input → Stimulus → Physio → Matrix → Memory"""

    # 1. Process user input
    orchestrator.process_turn("I'm stressed about the deadline")

    # 2. Check stimulus was logged
    assert msp._current_turn_stimulus is not None

    # 3. Check PhysioCore state includes vitals
    physio_state = msp.active_state["physio_state"]
    assert "vitals" in physio_state
    assert "bpm" in physio_state["vitals"]

    # 4. Check episodic memory has full snapshot
    episode = msp.get_latest_episode()
    assert "resonance_texture" in episode["state_snapshot"]
    assert "trauma_flag" in episode["state_snapshot"]
```

---

## Rollback Plan

If issues arise:

1. **Schema changes are backward compatible** (only additions, no removals)
2. **Old code will ignore new fields** (graceful degradation)
3. **Revert commits** if validation breaks:
   ```bash
   git revert <commit-hash>
   ```

---

## Success Metrics

After implementation, verify:

- ✅ **Stimulus logging**: 100% of turns have `stimulus_output` in episodic memory
- ✅ **Vitals tracking**: `physio_state.vitals` present in real-time state
- ✅ **Qualia richness**: `depth` and `texture` in episodic snapshots
- ✅ **Zero validation errors**: All MSP writes pass schema validation
- ✅ **Gap monitoring**: Monitor reports 0 missing fields

---

## Conclusion

This strategy addresses all 18 identified data gaps through:
1. Schema expansion (non-breaking)
2. System hook integration
3. Validation enforcement
4. Continuous monitoring

**Next Step:** Review this proposal with team, then begin Phase 1 implementation.

---

**Prepared by:** Claude Code
**Date:** 2026-01-19
**Status:** Ready for Review
