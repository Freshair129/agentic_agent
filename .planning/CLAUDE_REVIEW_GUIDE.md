# Claude Code Review Guide for MSP Phase 1

**Reviewer:** Claude Code (You)
**Developer:** Gemini 3.0 Pro
**Phase:** Phase 1 - Critical Data Logging Gaps
**Date:** 2026-01-19

---

## 🎯 Review Objectives

Your role is to verify that Gemini 3.0 Pro's implementation:
1. ✅ Meets all functional requirements
2. ✅ Maintains code quality standards
3. ✅ Preserves backward compatibility
4. ✅ Follows EVA architectural principles
5. ✅ Has no security issues

---

## 📋 Review Checklist

### Pre-Review Setup

When Gemini reports completion, run these commands first:

```bash
# 1. Check current branch
git branch  # Should show: feature/msp-logging-gaps

# 2. See what changed
git diff main...feature/msp-logging-gaps --stat

# 3. Review commit log
git log --oneline main..feature/msp-logging-gaps
```

---

## 🔍 File-by-File Review

### File 1: Stimulus_Output_Schema.json (NEW)

**Location:** `memory_n_soul_passport/schema/Stimulus_Output_Schema.json`

**Review Checklist:**
- [ ] File exists at correct location
- [ ] Valid JSON syntax
- [ ] Schema version: `"$schema": "http://json-schema.org/draft-07/schema#"`
- [ ] Title: `"Stimulus_Output_Schema"`
- [ ] Required fields: `["turn_id", "eva_stimuli", "timestamp"]`
- [ ] eva_stimuli type: `object` with `additionalProperties: number`
- [ ] Number constraints: `minimum: -1.0, maximum: 1.0`
- [ ] timestamp format: `"date-time"`

**Validation Commands:**
```bash
# Syntax check
python -c "import json; s=json.load(open('memory_n_soul_passport/schema/Stimulus_Output_Schema.json')); print('✅ Valid JSON')"

# Schema structure check
python -c "
import json
s = json.load(open('memory_n_soul_passport/schema/Stimulus_Output_Schema.json'))
assert s['title'] == 'Stimulus_Output_Schema', 'Wrong title'
assert set(s['required']) == {'turn_id', 'eva_stimuli', 'timestamp'}, 'Wrong required fields'
print('✅ Schema structure correct')
"
```

**Common Issues:**
- Missing `additionalProperties` for eva_stimuli
- Wrong type for stimulus values (should be number, not integer)
- Missing min/max constraints

**Acceptance Criteria:**
✅ All validation commands pass
✅ Schema matches specification in MSP_LOGGING_STRATEGY_PROPOSAL.md

---

### File 2: Episodic_Memory_Schema_v2.json (MODIFIED)

**Location:** `memory_n_soul_passport/schema/Episodic_Memory_Schema_v2.json`

**Changes Expected:**
- Added `stimulus_output` to `turn_llm` definition

**Review Checklist:**
- [ ] `definitions.turn_llm.properties` contains `stimulus_output`
- [ ] Reference: `"$ref": "Stimulus_Output_Schema.json#"`
- [ ] No other changes (this file should have minimal modification)
- [ ] JSON still valid

**Validation Commands:**
```bash
# Syntax check
python -c "import json; json.load(open('memory_n_soul_passport/schema/Episodic_Memory_Schema_v2.json')); print('✅ Valid JSON')"

# Check stimulus_output exists
python -c "
import json
s = json.load(open('memory_n_soul_passport/schema/Episodic_Memory_Schema_v2.json'))
turn_llm_props = s['definitions']['turn_llm']['properties']
assert 'stimulus_output' in turn_llm_props, 'stimulus_output not found'
assert turn_llm_props['stimulus_output']['\$ref'] == 'Stimulus_Output_Schema.json#', 'Wrong reference'
print('✅ stimulus_output correctly added')
"
```

**Common Issues:**
- Added to wrong location (should be in `definitions.turn_llm.properties`)
- Incorrect reference path
- Accidentally broke other parts of schema

**Acceptance Criteria:**
✅ stimulus_output added to correct location
✅ Reference path correct
✅ No breaking changes to existing structure

---

### File 3: State_Storage_Schema.json (MODIFIED)

**Location:** `memory_n_soul_passport/schema/State_Storage_Schema.json`

**Changes Expected:**
- Added `vitals` to `physio_state.properties`
- Added `receptor_signals` to `physio_state.properties`
- Updated `physio_state.required` to include `"vitals"`

**Review Checklist:**
- [ ] `vitals` object with bpm, rpm, vagus_tone properties
- [ ] bpm range: 40-200
- [ ] rpm range: 8-40
- [ ] vagus_tone range: 0.0-1.0
- [ ] `receptor_signals` with proper structure
- [ ] `required` array includes "vitals"

**Validation Commands:**
```bash
# Syntax check
python -c "import json; json.load(open('memory_n_soul_passport/schema/State_Storage_Schema.json')); print('✅ Valid JSON')"

# Check vitals structure
python -c "
import json
s = json.load(open('memory_n_soul_passport/schema/State_Storage_Schema.json'))
physio = s['properties']['physio_state']
assert 'vitals' in physio['properties'], 'vitals not found'
vitals = physio['properties']['vitals']
assert 'bpm' in vitals['properties'], 'bpm not found'
assert 'rpm' in vitals['properties'], 'rpm not found'
assert 'vagus_tone' in vitals['properties'], 'vagus_tone not found'
assert vitals['properties']['bpm']['minimum'] == 40, 'Wrong bpm min'
assert vitals['properties']['bpm']['maximum'] == 200, 'Wrong bpm max'
assert 'vitals' in physio['required'], 'vitals not required'
print('✅ vitals structure correct')
"
```

**Common Issues:**
- Wrong min/max values for vitals
- Missing required fields
- receptor_signals structure incorrect

**Acceptance Criteria:**
✅ All new fields present
✅ Ranges match physiological reality
✅ vitals marked as required

---

### File 4: State_Snapshot_Schema.json (MODIFIED)

**Location:** `memory_n_soul_passport/schema/State_Snapshot_Schema.json`

**Changes Expected:** Major expansion
- EVA_matrix: added `momentum` property
- qualia: expanded from 1 to 5 properties (intensity, tone, coherence, depth, texture)
- Added top-level: `resonance_texture`, `trauma_flag`, `reflex_directives`

**Review Checklist:**
- [ ] `EVA_matrix` still has original 9D structure
- [ ] `EVA_matrix` has new `momentum` property
- [ ] `qualia.properties` has 5 fields (intensity, tone, coherence, depth, texture)
- [ ] `resonance_texture` is object with 5 properties (stress, warmth, clarity, drive, calm)
- [ ] `trauma_flag` is boolean
- [ ] `reflex_directives` is object with additionalProperties

**Validation Commands:**
```bash
# Syntax check
python -c "import json; json.load(open('memory_n_soul_passport/schema/State_Snapshot_Schema.json')); print('✅ Valid JSON')"

# Check all new fields
python -c "
import json
s = json.load(open('memory_n_soul_passport/schema/State_Snapshot_Schema.json'))
props = s['properties']

# Check top-level additions
assert 'resonance_texture' in props, 'Missing resonance_texture'
assert 'trauma_flag' in props, 'Missing trauma_flag'
assert 'reflex_directives' in props, 'Missing reflex_directives'

# Check qualia expansion
qualia_props = props['qualia']['properties']
assert len(qualia_props) == 5, f'qualia should have 5 props, has {len(qualia_props)}'
assert 'tone' in qualia_props, 'Missing qualia.tone'
assert 'coherence' in qualia_props, 'Missing qualia.coherence'
assert 'depth' in qualia_props, 'Missing qualia.depth'
assert 'texture' in qualia_props, 'Missing qualia.texture'

# Check resonance_texture structure
rt = props['resonance_texture']['properties']
assert len(rt) == 5, 'resonance_texture should have 5 axes'
assert 'stress' in rt and 'warmth' in rt and 'clarity' in rt and 'drive' in rt and 'calm' in rt

print('✅ All expansions correct')
"
```

**Common Issues:**
- Forgot some new fields
- Broke existing EVA_matrix structure
- Wrong types for new fields

**Acceptance Criteria:**
✅ All 7 new fields/properties added
✅ Original structure preserved
✅ Types match data contracts

---

### File 5: memory_n_soul_passport_engine.py (MODIFIED)

**Location:** `memory_n_soul_passport/memory_n_soul_passport_engine.py`

**Changes Expected:**
- New method: `log_stimulus_output(self, stimulus_data: Dict[str, Any])`

**Review Checklist:**
- [ ] Method exists in MSP class
- [ ] Signature: `log_stimulus_output(self, stimulus_data: Dict[str, Any])`
- [ ] Validates required fields: turn_id, eva_stimuli, timestamp
- [ ] Creates `_current_turn_stimulus` buffer if not exists
- [ ] Stores stimulus in buffer
- [ ] Also stores in `active_state["last_stimulus"]`
- [ ] Prints log message
- [ ] No syntax errors

**Validation Commands:**
```bash
# Syntax check
python -m py_compile memory_n_soul_passport/memory_n_soul_passport_engine.py
echo "✅ No syntax errors"

# Check method exists
python -c "
from memory_n_soul_passport.memory_n_soul_passport_engine import MSP
import inspect

assert hasattr(MSP, 'log_stimulus_output'), 'Method not found'

# Check signature
sig = inspect.signature(MSP.log_stimulus_output)
params = list(sig.parameters.keys())
assert params == ['self', 'stimulus_data'], f'Wrong params: {params}'

print('✅ Method exists with correct signature')
"
```

**Code Quality Review:**
```bash
# Read the method
grep -A 20 "def log_stimulus_output" memory_n_soul_passport/memory_n_soul_passport_engine.py
```

**Check for:**
- [ ] Proper error handling (if field missing, log warning and return)
- [ ] Type hints present
- [ ] Docstring explains purpose
- [ ] No unnecessary complexity

**Common Issues:**
- Missing field validation
- Throws exception instead of warning
- Doesn't create buffer
- Wrong storage key

**Acceptance Criteria:**
✅ Method compiles
✅ Has proper signature
✅ Validates inputs gracefully
✅ Stores in both buffer and active_state

---

### File 6: orchestrator.py (MODIFIED)

**Location:** `orchestrator/orchestrator.py`

**Changes Expected:**
- Added MSP logging call BEFORE PhysioCore.step()

**Review Checklist:**
- [ ] Found correct location (where eva_stimuli is generated)
- [ ] Calls `self.msp.log_stimulus_output()` BEFORE `self.physio.step()`
- [ ] Checks if `self.msp` exists before calling
- [ ] Passes correct data structure
- [ ] Uses UTC timezone for timestamp
- [ ] No syntax errors

**Validation Commands:**
```bash
# Syntax check
python -m py_compile orchestrator/orchestrator.py
echo "✅ No syntax errors"

# Find the modification
grep -B 5 -A 5 "log_stimulus_output" orchestrator/orchestrator.py
```

**Code Review:**
Look for this pattern:
```python
# Extract/generate eva_stimuli
eva_stimuli = ...

# NEW CODE: Log to MSP
if self.msp and eva_stimuli:
    stimulus_data = {
        "turn_id": ...,
        "eva_stimuli": eva_stimuli,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    self.msp.log_stimulus_output(stimulus_data)

# Send to PhysioCore
if self.physio:
    self.physio.step(eva_stimuli=eva_stimuli, ...)
```

**Check for:**
- [ ] MSP logging happens BEFORE PhysioCore.step()
- [ ] Null check for self.msp
- [ ] Timestamp uses timezone.utc
- [ ] turn_id is captured (verify it exists in context)

**Common Issues:**
- Logged AFTER PhysioCore (wrong order)
- No null check for msp
- Missing timezone (uses naive datetime)
- turn_id doesn't exist in scope

**Acceptance Criteria:**
✅ Hook added in correct location
✅ Logging happens before PhysioCore
✅ Proper null checking
✅ Correct data structure

---

## 🧪 Integration Testing

### Test 1: Run Provided Test Suite

```bash
cd "E:\The Human Algorithm\T2\agent"
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

**If tests fail:**
- Review the specific failing test
- Check Gemini's implementation against checklist
- Provide specific feedback on what needs fixing

---

### Test 2: Manual Validation

```bash
# Test all schemas are valid JSON
for schema in memory_n_soul_passport/schema/*.json; do
    python -c "import json; json.load(open('$schema'))" && echo "✅ $schema"
done

# Test Python files compile
python -m py_compile memory_n_soul_passport/memory_n_soul_passport_engine.py
python -m py_compile orchestrator/orchestrator.py

# Test imports work
python -c "from memory_n_soul_passport.memory_n_soul_passport_engine import MSP; print('✅ MSP imports')"
python -c "from orchestrator.orchestrator import EVAOrchestrator; print('✅ Orchestrator imports')"
```

---

## 🔄 Backward Compatibility Check

### Test with Existing Code

**Goal:** Ensure old code still works

```python
# Test old MSP methods still work
from memory_n_soul_passport.memory_n_soul_passport_engine import MSP

# Initialize MSP (old way)
msp = MSP()

# Old methods should still work
msp.set_active_state("test_key", {"value": 123})
state = msp.get_active_state("test_key")
assert state == {"value": 123}

print("✅ Backward compatibility maintained")
```

**Check:**
- [ ] Old MSP methods unchanged
- [ ] Old schema files still work
- [ ] No breaking changes to public APIs

---

## 📊 Review Decision Matrix

| Criteria | Weight | Status | Notes |
|----------|--------|--------|-------|
| All tests pass | HIGH | ☐ Pass / ☐ Fail | |
| No syntax errors | HIGH | ☐ Pass / ☐ Fail | |
| Schemas valid | HIGH | ☐ Pass / ☐ Fail | |
| Backward compatible | HIGH | ☐ Pass / ☐ Fail | |
| Code quality | MEDIUM | ☐ Pass / ☐ Fail | |
| Documentation | LOW | ☐ Pass / ☐ Fail | |

**Decision Rules:**
- All HIGH criteria = PASS → **APPROVE**
- Any HIGH criteria = FAIL → **REQUEST CHANGES**
- All HIGH = PASS, MEDIUM = FAIL → **APPROVE WITH SUGGESTIONS**

---

## ✅ Approval Checklist

Before approving, verify:

- [ ] All 6 files modified/created correctly
- [ ] All validation commands pass
- [ ] Integration tests pass
- [ ] No breaking changes
- [ ] Code quality acceptable
- [ ] Git commit properly formatted
- [ ] No security issues

---

## 📝 Review Response Templates

### Template 1: Full Approval

```markdown
## ✅ Phase 1 Review: APPROVED

Great work! All implementation requirements met.

**Summary:**
- All 6 files correctly modified/created
- All tests passing
- No breaking changes
- Code quality good

**Validation Results:**
✅ All JSON schemas valid
✅ All Python files compile
✅ Integration tests pass
✅ Backward compatibility maintained

**Next Steps:**
1. Merge branch to main
2. Tag as msp-phase1-complete
3. Begin Phase 2 planning

**Commit for merge:** [commit hash]
```

### Template 2: Request Changes

```markdown
## ⚠️ Phase 1 Review: CHANGES REQUESTED

Good progress, but some issues need fixing.

**Issues Found:**

1. **[File Name]** - [Issue description]
   - Problem: [Specific problem]
   - Fix: [How to fix]
   - Location: [File path:line number]

2. **[File Name]** - [Issue description]
   - Problem: [Specific problem]
   - Fix: [How to fix]

**Test Results:**
❌ [Test name] failed: [error message]

**Action Required:**
Please fix the issues listed above and re-submit.

**Still Good:**
✅ [List what was done correctly]
```

### Template 3: Critical Issues

```markdown
## 🚨 Phase 1 Review: CRITICAL ISSUES

Implementation has critical issues that need immediate attention.

**Critical Issues:**

1. **[Issue]** - [Why critical]
   - Impact: [What breaks]
   - Fix: [Detailed fix instructions]

**Required Actions:**
1. [Step 1]
2. [Step 2]

**Do Not Proceed** until these are resolved.

I'm available to help debug if needed.
```

---

## 🔧 Common Issues & Debugging

### Issue 1: Tests Fail - Schema Validation Error

**Symptoms:**
```
ValidationError: 'X' is a required property
```

**Debug:**
```bash
python -c "
import json
from jsonschema import validate
schema = json.load(open('path/to/schema.json'))
data = {...}  # Test data
validate(data, schema)
"
```

**Common Causes:**
- Missing required field in schema
- Field name typo
- Wrong schema reference

---

### Issue 2: Import Error

**Symptoms:**
```
ImportError: cannot import name 'X' from 'Y'
```

**Debug:**
```bash
# Check if file exists
ls -la path/to/file.py

# Check if method/class defined
grep "class X\|def X" path/to/file.py

# Check for syntax errors
python -m py_compile path/to/file.py
```

**Common Causes:**
- Syntax error preventing import
- Class/method name typo
- Circular import

---

### Issue 3: Orchestrator Hook Not Working

**Symptoms:**
- Stimulus not logged
- PhysioCore works but no MSP entry

**Debug:**
```bash
# Find where eva_stimuli is used
grep -n "eva_stimuli" orchestrator/orchestrator.py

# Check hook location
grep -B 10 -A 10 "log_stimulus_output" orchestrator/orchestrator.py
```

**Common Causes:**
- Hook added in wrong method
- Hook after PhysioCore.step()
- self.msp is None (not initialized)

---

## 📞 Communication with Gemini

### When to Request Clarification

Ask Gemini to clarify if:
- Implementation differs significantly from checklist
- New approach taken (not in plan)
- File structure different than expected
- "Creative" solutions added

### When to Provide Guidance

Guide Gemini if:
- First attempt had issues
- Stuck on specific problem
- Misunderstood requirement
- Need architectural context

### When to Approve Deviations

Allow deviations if:
- Achieves same goal better way
- Fixes additional bugs
- Improves code quality
- Better performance

**But:** Must explain reasoning and verify no breaking changes.

---

## 🎯 Success Criteria Summary

Phase 1 is successful when:

1. ✅ All 6 files correctly modified/created
2. ✅ All schemas valid JSON Schema draft-07
3. ✅ MSP has log_stimulus_output() method
4. ✅ Orchestrator hooks stimulus logging
5. ✅ All tests pass
6. ✅ No syntax errors
7. ✅ Backward compatible
8. ✅ Git commit clean

**If all met → APPROVE**
**If any fail → REQUEST CHANGES**

---

## 📚 Reference Documents

Keep these open during review:
1. MSP_IMPLEMENTATION_CHECKLIST.md - What should be done
2. MSP_LOGGING_STRATEGY_PROPOSAL.md - Why and how
3. MSP_DATA_FLOW_GAP_ANALYSIS.md - Problem context

---

**Review carefully, but trust Gemini's implementation if it meets criteria. Your role is to verify, not rewrite. 🎯**
