# MSP Logging Implementation Checklist

**For:** Gemini 3.0 Pro (Developer)
**Reviewer:** Claude Code (Dev Lead)
**Date:** 2026-01-19
**Related:** MSP_LOGGING_STRATEGY_PROPOSAL.md

---

## 📋 Pre-Implementation Checklist

Before starting, verify:

- [ ] Read `MSP_DATA_FLOW_GAP_ANALYSIS.md` completely
- [ ] Read `MSP_LOGGING_STRATEGY_PROPOSAL.md` completely
- [ ] Current working directory: `E:\The Human Algorithm\T2\agent`
- [ ] Git branch: Create new branch `feature/msp-logging-gaps`
- [ ] Backup: Commit current state before modifications
- [ ] Test environment: Python 3.13.7 available

**Create branch:**
```bash
git checkout -b feature/msp-logging-gaps
git commit -m "chore: checkpoint before MSP logging implementation"
```

---

## Phase 1: Critical Gaps (Priority 1)

### Task 1.1: Stimulus Input Logging

#### Step 1.1.1: Create Stimulus_Output_Schema.json ✅

**File:** `memory_n_soul_passport/schema/Stimulus_Output_Schema.json`
**Action:** Create new file
**Content:** See MSP_LOGGING_STRATEGY_PROPOSAL.md Section 1.1 Step 1.1.1

**Validation:**
```bash
# Verify file exists
ls -la memory_n_soul_passport/schema/Stimulus_Output_Schema.json

# Validate JSON syntax
python -c "import json; json.load(open('memory_n_soul_passport/schema/Stimulus_Output_Schema.json'))"
```

**Expected Output:**
```
File exists: Stimulus_Output_Schema.json
JSON is valid
```

**Claude Code Review:**
- [ ] File created at correct path
- [ ] JSON syntax valid
- [ ] Contains required fields: turn_id, eva_stimuli, timestamp
- [ ] Schema version is draft-07

---

#### Step 1.1.2: Update Episodic_Memory_Schema_v2.json ✅

**File:** `memory_n_soul_passport/schema/Episodic_Memory_Schema_v2.json`
**Action:** Modify existing file
**Line:** Find `"turn_llm"` definition (around line 249)

**Change:**
Add this property inside `turn_llm.properties`:
```json
"stimulus_output": {
  "$ref": "Stimulus_Output_Schema.json#"
}
```

**Exact Location:**
```json
"turn_llm": {
  "type": "object",
  "required": ["speaker"],
  "properties": {
    "turn_id": {...},
    "speaker": {...},
    "text_excerpt": {...},
    "summary": {...},
    "epistemic_mode": {...},
    "confidence": {...},
    "salience_anchor": {...},
    "stimulus_output": {  // <-- ADD THIS
      "$ref": "Stimulus_Output_Schema.json#"
    }
  }
}
```

**Validation:**
```bash
# Validate JSON syntax after edit
python -c "import json; json.load(open('memory_n_soul_passport/schema/Episodic_Memory_Schema_v2.json'))"
```

**Claude Code Review:**
- [ ] stimulus_output added to turn_llm.properties
- [ ] JSON still valid
- [ ] Reference path correct: "Stimulus_Output_Schema.json#"

---

#### Step 1.1.3: Add log_stimulus_output() to MSP Engine ✅

**File:** `memory_n_soul_passport/memory_n_soul_passport_engine.py`
**Action:** Add new method
**Location:** After `set_active_state()` method (around line 200-300)

**Add this method:**
```python
def log_stimulus_output(self, stimulus_data: Dict[str, Any]):
    """
    Log LLM-generated stimulus vectors for causal chain tracking.

    Args:
        stimulus_data: Dict containing turn_id, eva_stimuli, timestamp
    """
    # TODO: Add schema validation when validator is implemented
    # For now, basic validation
    required_fields = ["turn_id", "eva_stimuli", "timestamp"]
    for field in required_fields:
        if field not in stimulus_data:
            print(f"[MSP] Warning: Missing required field '{field}' in stimulus_data")
            return

    # Store in active turn buffer
    if not hasattr(self, '_current_turn_stimulus'):
        self._current_turn_stimulus = []

    self._current_turn_stimulus.append(stimulus_data)

    # Also store in active_state for immediate access
    self.set_active_state("last_stimulus", stimulus_data)

    print(f"[MSP] Logged stimulus output for turn {stimulus_data['turn_id']}")
```

**Validation:**
```bash
# Check syntax
python -m py_compile memory_n_soul_passport/memory_n_soul_passport_engine.py

# Test method exists
python -c "from memory_n_soul_passport.memory_n_soul_passport_engine import MSP; print(hasattr(MSP, 'log_stimulus_output'))"
```

**Expected Output:**
```
True
```

**Claude Code Review:**
- [ ] Method added to MSP class
- [ ] Signature matches: `log_stimulus_output(self, stimulus_data: Dict[str, Any])`
- [ ] Creates `_current_turn_stimulus` buffer
- [ ] Validates required fields
- [ ] No syntax errors

---

#### Step 1.1.4: Hook Orchestrator to Log Stimulus ✅

**File:** `orchestrator/orchestrator.py`
**Action:** Modify existing method
**Method:** Find where stimulus is sent to PhysioCore

**Search for:** `self.physio.step` or `eva_stimuli`

**Current code (approximate line 400-500):**
```python
# Somewhere in process_turn() or similar
eva_stimuli = self._extract_eva_stimuli(llm_response)
if self.physio:
    self.physio.step(eva_stimuli=eva_stimuli, dt=0.033)
```

**Change to:**
```python
# Extract stimulus
eva_stimuli = self._extract_eva_stimuli(llm_response)

# NEW: Log stimulus to MSP BEFORE sending to PhysioCore
if self.msp and eva_stimuli:
    from datetime import datetime, timezone
    stimulus_data = {
        "turn_id": getattr(self, 'current_turn_id', 'UNKNOWN'),
        "eva_stimuli": eva_stimuli,
        "stimulus_context": {
            "reasoning": "LLM function call output",
            "confidence": 0.8  # Default confidence
        },
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    self.msp.log_stimulus_output(stimulus_data)

# Send to PhysioCore
if self.physio:
    self.physio.step(eva_stimuli=eva_stimuli, dt=0.033)
```

**Important:** Need to find exact location where `eva_stimuli` is generated.

**Validation Commands:**
```bash
# Find the exact location
grep -n "eva_stimuli" orchestrator/orchestrator.py

# Check syntax after edit
python -m py_compile orchestrator/orchestrator.py
```

**Claude Code Review:**
- [ ] Found correct location for stimulus extraction
- [ ] Added MSP logging BEFORE PhysioCore.step()
- [ ] Timestamp uses UTC timezone
- [ ] No syntax errors
- [ ] Handles case where msp is None

**🚨 CRITICAL:** If you cannot find where `eva_stimuli` is generated in Orchestrator, STOP and report to Claude Code.

---

### Task 1.2: Expand State_Storage_Schema (Vitals)

#### Step 1.2.1: Update State_Storage_Schema.json ✅

**File:** `memory_n_soul_passport/schema/State_Storage_Schema.json`
**Action:** Modify existing file
**Location:** Find `"physio_state"` property (around line 27)

**Current structure:**
```json
"physio_state": {
  "type": "object",
  "properties": {
    "blood": {...},
    "autonomic": {...}
  },
  "required": ["blood", "autonomic"]
}
```

**Change to:**
```json
"physio_state": {
  "type": "object",
  "properties": {
    "blood": {
      "type": "object",
      "additionalProperties": {
        "type": "number",
        "minimum": 0.0
      }
    },
    "autonomic": {
      "type": "object",
      "properties": {
        "sympathetic": {
          "type": "number",
          "minimum": 0.0,
          "maximum": 1.0
        },
        "parasympathetic": {
          "type": "number",
          "minimum": 0.0,
          "maximum": 1.0
        }
      },
      "required": ["sympathetic", "parasympathetic"]
    },
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
      "description": "Transduced hormone to neural signals",
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
```

**Validation:**
```bash
# Validate JSON syntax
python -c "import json; json.load(open('memory_n_soul_passport/schema/State_Storage_Schema.json'))"
```

**Claude Code Review:**
- [ ] vitals field added with bpm, rpm, vagus_tone
- [ ] receptor_signals field added
- [ ] vitals added to required array
- [ ] JSON valid

---

### Task 1.3: Expand State_Snapshot_Schema

#### Step 1.3.1: Update State_Snapshot_Schema.json ✅

**File:** `memory_n_soul_passport/schema/State_Snapshot_Schema.json`
**Action:** Major expansion of schema

**Current version:** Simple schema with EVA_matrix, Resonance_index, qualia (intensity only)

**Replace entire file with:** See MSP_LOGGING_STRATEGY_PROPOSAL.md Section 1.3 Step 1.3.1

**Key additions:**
1. EVA_matrix.momentum
2. qualia expanded: tone, coherence, depth, texture
3. resonance_texture (5D)
4. trauma_flag
5. reflex_directives

**Validation:**
```bash
# Validate JSON
python -c "import json; json.load(open('memory_n_soul_passport/schema/State_Snapshot_Schema.json'))"

# Check new fields exist
python -c "
import json
schema = json.load(open('memory_n_soul_passport/schema/State_Snapshot_Schema.json'))
props = schema['properties']
assert 'resonance_texture' in props, 'Missing resonance_texture'
assert 'trauma_flag' in props, 'Missing trauma_flag'
assert 'reflex_directives' in props, 'Missing reflex_directives'
assert 'tone' in props['qualia']['properties'], 'Missing qualia.tone'
assert 'depth' in props['qualia']['properties'], 'Missing qualia.depth'
print('✅ All new fields present')
"
```

**Expected Output:**
```
✅ All new fields present
```

**Claude Code Review:**
- [ ] File replaced with expanded version
- [ ] All 5 new top-level fields present
- [ ] qualia expanded from 1 to 5 properties
- [ ] JSON valid
- [ ] Schema version still draft-07

---

## Phase 1 Verification

### Integration Test

After completing all Phase 1 tasks, run this test:

**File:** `tests/test_msp_phase1.py` (create this)

```python
"""
Integration test for Phase 1 MSP logging improvements
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_phase1_schemas():
    """Test all Phase 1 schema files are valid"""
    import json
    from pathlib import Path

    schema_dir = Path("memory_n_soul_passport/schema")

    # Test 1: Stimulus schema exists and valid
    stimulus_schema = schema_dir / "Stimulus_Output_Schema.json"
    assert stimulus_schema.exists(), "Stimulus_Output_Schema.json not found"
    schema = json.load(open(stimulus_schema))
    assert schema["title"] == "Stimulus_Output_Schema"
    print("✅ Stimulus_Output_Schema.json valid")

    # Test 2: State_Storage has vitals
    state_storage = schema_dir / "State_Storage_Schema.json"
    schema = json.load(open(state_storage))
    assert "vitals" in schema["properties"]["physio_state"]["properties"]
    print("✅ State_Storage_Schema.json has vitals")

    # Test 3: State_Snapshot expanded
    state_snapshot = schema_dir / "State_Snapshot_Schema.json"
    schema = json.load(open(state_snapshot))
    assert "resonance_texture" in schema["properties"]
    assert "trauma_flag" in schema["properties"]
    assert "depth" in schema["properties"]["qualia"]["properties"]
    print("✅ State_Snapshot_Schema.json expanded")

    # Test 4: Episodic Memory references stimulus
    episodic = schema_dir / "Episodic_Memory_Schema_v2.json"
    schema = json.load(open(episodic))
    turn_llm_props = schema["definitions"]["turn_llm"]["properties"]
    assert "stimulus_output" in turn_llm_props
    print("✅ Episodic_Memory_Schema_v2.json references stimulus")

def test_msp_method():
    """Test MSP has new method"""
    from memory_n_soul_passport.memory_n_soul_passport_engine import MSP

    assert hasattr(MSP, 'log_stimulus_output'), "MSP missing log_stimulus_output method"
    print("✅ MSP.log_stimulus_output() exists")

def test_orchestrator_hooks():
    """Test Orchestrator imports and syntax"""
    try:
        from orchestrator.orchestrator import EVAOrchestrator
        print("✅ Orchestrator imports successfully")
    except SyntaxError as e:
        print(f"❌ Orchestrator syntax error: {e}")
        raise

if __name__ == "__main__":
    print("\n=== Phase 1 Integration Test ===\n")

    test_phase1_schemas()
    test_msp_method()
    test_orchestrator_hooks()

    print("\n✅ All Phase 1 tests passed!")
```

**Run test:**
```bash
python tests/test_msp_phase1.py
```

**Expected Output:**
```
=== Phase 1 Integration Test ===

✅ Stimulus_Output_Schema.json valid
✅ State_Storage_Schema.json has vitals
✅ State_Snapshot_Schema.json expanded
✅ Episodic_Memory_Schema_v2.json references stimulus
✅ MSP.log_stimulus_output() exists
✅ Orchestrator imports successfully

✅ All Phase 1 tests passed!
```

---

## Phase 1 Commit

After all tests pass:

```bash
# Stage changes
git add memory_n_soul_passport/schema/*.json
git add memory_n_soul_passport/memory_n_soul_passport_engine.py
git add orchestrator/orchestrator.py
git add tests/test_msp_phase1.py

# Commit
git commit -m "feat(msp): Phase 1 - Critical data logging gaps fixed

- Add Stimulus_Output_Schema for LLM→PhysioCore logging
- Expand State_Storage_Schema with vitals and receptor_signals
- Expand State_Snapshot_Schema with missing fields:
  * EVA_matrix.momentum
  * qualia.tone, coherence, depth, texture
  * resonance_texture (5D)
  * trauma_flag
  * reflex_directives
- Add MSP.log_stimulus_output() method
- Hook Orchestrator to log stimulus before PhysioCore

Closes: MSP Data Flow Gap Analysis Phase 1
Related: .planning/MSP_LOGGING_STRATEGY_PROPOSAL.md"

# Tag
git tag -a msp-phase1-complete -m "MSP Logging Phase 1 Complete"
```

---

## 🚨 Critical Issues - Stop and Report

If you encounter any of these, STOP and report to Claude Code:

1. **Cannot find where eva_stimuli is generated in Orchestrator**
   - Report: "Unable to locate stimulus generation in orchestrator.py"

2. **MSP class structure different than expected**
   - Report: "MSP class layout differs from documentation"

3. **Schema files have different structure**
   - Report: "Schema file X has unexpected structure at line Y"

4. **Tests fail after implementation**
   - Report: "Test X failed with error Y"

5. **Import errors**
   - Report: "Cannot import X from Y"

---

## Phase 1 Success Criteria

Before moving to Phase 2, verify:

- [ ] All 4 schema files modified/created
- [ ] MSP has log_stimulus_output() method
- [ ] Orchestrator calls MSP before PhysioCore
- [ ] All tests pass
- [ ] No syntax errors
- [ ] Git commit created
- [ ] No breaking changes (backward compatible)

---

## Handoff to Claude Code for Review

After Phase 1 completion, provide:

1. **Git commit hash**
2. **Test output** (copy-paste from terminal)
3. **Files changed** (list all modified files)
4. **Any issues encountered**
5. **Questions or clarifications needed**

**Format:**
```
Phase 1 Complete

Commit: abc123def456
Files Changed: 6 files
- memory_n_soul_passport/schema/Stimulus_Output_Schema.json (NEW)
- memory_n_soul_passport/schema/Episodic_Memory_Schema_v2.json (MODIFIED)
- memory_n_soul_passport/schema/State_Storage_Schema.json (MODIFIED)
- memory_n_soul_passport/schema/State_Snapshot_Schema.json (MODIFIED)
- memory_n_soul_passport/memory_n_soul_passport_engine.py (MODIFIED)
- orchestrator/orchestrator.py (MODIFIED)

Test Results:
[paste test output]

Issues: None / [describe any issues]
```

---

**Next:** Phase 2 will be provided after Phase 1 review.
