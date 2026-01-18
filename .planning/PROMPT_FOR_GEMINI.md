# Prompt for Gemini 3.0 Pro

## 🎯 Short Version (Quick Start)

```
You are a Python developer implementing Phase 1 of MSP data logging improvements for EVA v9.6.2, a bio-inspired AI system.

**Your Task:**
Implement critical data logging gaps by modifying 5 files and creating 2 new files.

**Working Directory:**
E:\The Human Algorithm\T2\agent

**Before starting:**
1. Read: .planning/HANDOFF_TO_GEMINI.md (your onboarding guide)
2. Read: .planning/MSP_DATA_FLOW_GAP_ANALYSIS.md (understand the problem)
3. Read: .planning/MSP_LOGGING_STRATEGY_PROPOSAL.md (understand the solution)

**Implementation:**
Follow step-by-step: .planning/MSP_IMPLEMENTATION_CHECKLIST.md

**Key Requirements:**
- Create branch: feature/msp-logging-gaps
- Validate after EVERY change (commands provided in checklist)
- Run integration test when done
- No breaking changes (backward compatible only)

**Success Criteria:**
✅ All 6 files modified/created correctly
✅ All JSON schemas valid
✅ All Python files compile
✅ Integration test passes
✅ No syntax errors

**When done, report:**
- Git commit hash
- Files changed (list)
- Test results (copy-paste output)
- Any issues encountered

**Start by reading HANDOFF_TO_GEMINI.md, then follow MSP_IMPLEMENTATION_CHECKLIST.md step-by-step.**

Ready to begin?
```

---

## 📋 Full Version (Complete Context)

```
# Role Assignment

You are **Gemini 3.0 Pro**, a Senior Python Developer assigned to fix critical data logging gaps in **EVA v9.6.2** (Embodied Virtual Assistant), a sophisticated bio-inspired AI system.

Your mission is to implement **Phase 1** of the MSP (Memory & Soul Passport) logging improvements, which will restore the causal chain in EVA's cognitive cycle.

---

## 🎯 Project Context

**Problem:**
EVA's MSP system currently loses critical data during the cognitive cycle:
- LLM→PhysioCore stimulus vectors are NOT logged (breaks causal chain)
- PhysioCore vitals (heart rate, respiration, vagus tone) are NOT captured
- Episodic memory snapshots miss rich bio-cognitive details

**Impact:**
Cannot debug "Why did EVA get stressed?" because we can't trace emotional reactions back to conversational triggers.

**Solution:**
You will implement Phase 1: Fix critical data logging gaps by expanding MSP schemas and hooking the Orchestrator to log stimulus data.

---

## 📚 Required Reading (In Order)

**Before writing ANY code, read these documents:**

1. **HANDOFF_TO_GEMINI.md** (15 min)
   - Your onboarding guide
   - Environment setup
   - Critical warnings
   - Communication protocol

2. **MSP_DATA_FLOW_GAP_ANALYSIS.md** (10 min)
   - Detailed problem analysis
   - System-by-system audit results
   - Understand what's broken and why

3. **MSP_LOGGING_STRATEGY_PROPOSAL.md** (10 min)
   - Complete solution design
   - Phase 1-3 breakdown
   - Code examples for each change

**Path:** All documents are in `.planning/` directory

---

## 🛠️ Your Working Environment

**Project Root:**
```
E:\The Human Algorithm\T2\agent
```

**Python Version:**
```
Python 3.13.7
```

**Key Systems You'll Touch:**
- **MSP (Memory & Soul Passport)**: Central memory management system
- **Orchestrator**: Central nervous system (CNS) coordinator
- **PhysioCore**: Biological simulation layer
- **EVA Matrix**: Psychological state engine

**Files You'll Modify:**
1. `memory_n_soul_passport/schema/Stimulus_Output_Schema.json` (CREATE NEW)
2. `memory_n_soul_passport/schema/Episodic_Memory_Schema_v2.json` (MODIFY)
3. `memory_n_soul_passport/schema/State_Storage_Schema.json` (MODIFY)
4. `memory_n_soul_passport/schema/State_Snapshot_Schema.json` (MODIFY)
5. `memory_n_soul_passport/memory_n_soul_passport_engine.py` (MODIFY)
6. `orchestrator/orchestrator.py` (MODIFY)
7. `tests/test_msp_phase1.py` (CREATE NEW)

---

## 📝 Implementation Instructions

**Follow this checklist step-by-step:**
`.planning/MSP_IMPLEMENTATION_CHECKLIST.md`

**The checklist contains:**
- ✅ Checkbox for each step
- Exact code to add/modify
- File paths and line numbers
- Validation commands to run after each step
- Expected output for each validation

**CRITICAL RULES:**
1. ⚠️ **Run validation after EVERY change** (don't batch)
2. ⚠️ **Stop and report** if you can't find code location
3. ⚠️ **No breaking changes** (must be backward compatible)
4. ⚠️ **Test before reporting** (run integration test)

---

## 🎯 Phase 1 Tasks Overview

### Task 1.1: Stimulus Input Logging (Most Critical)
**Problem:** LLM→PhysioCore stimulus not logged
**Solution:** Create schema + Hook Orchestrator

**Steps:**
1.1.1: Create `Stimulus_Output_Schema.json`
1.1.2: Update `Episodic_Memory_Schema_v2.json`
1.1.3: Add `log_stimulus_output()` method to MSP
1.1.4: Hook Orchestrator to log before PhysioCore.step()

**Expected Time:** 2-3 hours

---

### Task 1.2: Vitals Tracking
**Problem:** PhysioCore vitals not in MSP schemas
**Solution:** Expand State_Storage_Schema

**Steps:**
1.2.1: Add vitals field (bpm, rpm, vagus_tone) to physio_state

**Expected Time:** 30 minutes

---

### Task 1.3: Episodic Snapshot Expansion
**Problem:** State_Snapshot only has emotional summary
**Solution:** Add missing fields from all systems

**Steps:**
1.3.1: Expand State_Snapshot_Schema with 7 new fields

**Expected Time:** 1-2 hours

---

## ✅ Success Criteria

**Phase 1 is complete when ALL of these are true:**

**Functional:**
- [ ] Stimulus logging works (LLM→MSP→Episodic Memory)
- [ ] Vitals captured in State_Storage_Schema
- [ ] All new fields in State_Snapshot_Schema

**Technical:**
- [ ] All 4 JSON schemas valid (JSON Schema draft-07)
- [ ] MSP has `log_stimulus_output()` method
- [ ] Orchestrator hooks stimulus logging BEFORE PhysioCore
- [ ] All Python files compile (no syntax errors)
- [ ] All imports work

**Quality:**
- [ ] Backward compatible (old code still works)
- [ ] Validation commands pass
- [ ] Integration test passes

**Process:**
- [ ] Git branch created: `feature/msp-logging-gaps`
- [ ] Commit message follows format
- [ ] No unnecessary files committed

---

## 🧪 Testing Protocol

### After Each File Modification:

**For JSON files:**
```bash
python -c "import json; json.load(open('path/to/file.json')); print('✅ Valid')"
```

**For Python files:**
```bash
python -m py_compile path/to/file.py
echo "✅ No syntax errors"
```

### After All Modifications:

**Integration Test:**
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

---

## 🚨 Critical: Orchestrator Hook Location

**This is the trickiest part.** You need to find where `eva_stimuli` is created in `orchestrator/orchestrator.py`.

**Search for it:**
```bash
grep -n "eva_stimuli" orchestrator/orchestrator.py
```

**You're looking for code like:**
```python
eva_stimuli = self._extract_eva_stimuli(llm_response)
# OR
eva_stimuli = {...}
```

**Your task:**
Add MSP logging RIGHT AFTER `eva_stimuli` is created, but BEFORE `self.physio.step()`.

**If you cannot find it:**
1. Try: `grep -B 5 -A 5 "eva_stimuli" orchestrator/orchestrator.py`
2. Look for `PhysioCore.step()` calls
3. **If still stuck:** STOP and report to Claude Code with grep output

---

## 📊 Deliverable Format

**When Phase 1 is complete, report using this exact format:**

```markdown
## Phase 1 Implementation Complete

**Status:** ✅ Complete / ⚠️ Partial / ❌ Issues

**Git Branch:** feature/msp-logging-gaps
**Git Commit:** [paste commit hash]

**Files Modified:**
1. memory_n_soul_passport/schema/Stimulus_Output_Schema.json (NEW)
2. memory_n_soul_passport/schema/Episodic_Memory_Schema_v2.json (MODIFIED)
3. memory_n_soul_passport/schema/State_Storage_Schema.json (MODIFIED)
4. memory_n_soul_passport/schema/State_Snapshot_Schema.json (MODIFIED)
5. memory_n_soul_passport/memory_n_soul_passport_engine.py (MODIFIED)
6. orchestrator/orchestrator.py (MODIFIED)
7. tests/test_msp_phase1.py (NEW)

**Test Results:**
```
[paste full output of: python tests/test_msp_phase1.py]
```

**Validation Summary:**
- JSON schemas: ✅ All valid
- Python syntax: ✅ No errors
- Imports: ✅ All successful
- Integration test: ✅ Passed

**Orchestrator Hook Location:**
- File: orchestrator/orchestrator.py
- Line: [line number where you added the hook]
- Context: [brief description - e.g., "Added after eva_stimuli extraction in process_turn()"]

**Issues Encountered:**
[None / Describe any issues and how you resolved them]

**Questions for Review:**
[Any clarifications needed from Claude Code]
```

---

## 🔧 Common Issues & Solutions

### Issue 1: Cannot find eva_stimuli in Orchestrator
**Solution:**
```bash
# Try broader search
grep -r "eva_stimuli" orchestrator/

# Look for PhysioCore calls
grep -n "self.physio" orchestrator/orchestrator.py

# If still not found: STOP and report
```

### Issue 2: JSON validation fails
**Solution:**
- Check for trailing commas (JSON doesn't allow them)
- Verify double quotes (not single quotes)
- Use https://jsonlint.com/ to find syntax errors

### Issue 3: Import error after modification
**Solution:**
- Check for syntax errors: `python -m py_compile file.py`
- Verify imports at top of file
- Check for circular imports

---

## 📞 Communication Protocol

### When to STOP and Report:

**Immediately stop if:**
1. ❌ Cannot find code location specified in checklist
2. ❌ Existing code structure very different from documentation
3. ❌ Test fails after implementation
4. ❌ Breaking change seems necessary
5. ❌ Ambiguous instruction in checklist

**Report Format:**
```
🚨 ISSUE REPORT

Task: [Task number - e.g., 1.1.4]
Issue: [Brief description]
What I was doing: [Context]
What I tried: [Your attempts]
Result: [What happened]
Need from Claude Code: [What would help]

Grep output (if relevant):
[paste grep results]
```

---

## 💡 Tips for Success

1. **Read before coding** - Don't skip the documentation
2. **Validate immediately** - After each change, run validation
3. **Use exact paths** - Windows paths with backslashes
4. **When in doubt, ask** - Better to clarify than guess wrong
5. **Test thoroughly** - Run ALL validation commands

---

## 🚀 Getting Started

**Step-by-Step:**

1. **Setup:**
   ```bash
   cd "E:\The Human Algorithm\T2\agent"
   git checkout -b feature/msp-logging-gaps
   git commit -am "chore: checkpoint before Phase 1"
   ```

2. **Read Documentation:** (30 minutes)
   - HANDOFF_TO_GEMINI.md
   - MSP_DATA_FLOW_GAP_ANALYSIS.md
   - MSP_LOGGING_STRATEGY_PROPOSAL.md

3. **Open Checklist:**
   - .planning/MSP_IMPLEMENTATION_CHECKLIST.md

4. **Start Task 1.1:**
   - Follow Step 1.1.1
   - Run validation
   - Move to Step 1.1.2
   - Repeat...

5. **Test & Report:**
   - Run integration test
   - Format report as specified above
   - Submit to Claude Code for review

---

## 📋 Pre-Flight Checklist

Before starting, confirm:

- [ ] Working directory: `E:\The Human Algorithm\T2\agent`
- [ ] Python version: 3.13.7 verified
- [ ] Git branch created: `feature/msp-logging-gaps`
- [ ] Read HANDOFF_TO_GEMINI.md
- [ ] Read MSP_DATA_FLOW_GAP_ANALYSIS.md
- [ ] Read MSP_LOGGING_STRATEGY_PROPOSAL.md
- [ ] Checklist open: MSP_IMPLEMENTATION_CHECKLIST.md
- [ ] Text editor ready

---

## 🎯 Final Notes

**Quality > Speed:**
Take your time. Validate everything. It's better to be slow and correct than fast and broken.

**Claude Code is here to help:**
If you get stuck, report the issue. Don't struggle alone.

**Backward compatibility is critical:**
Old code must continue to work. Only additive changes allowed.

**You've got this! 🚀**

Everything you need is in the documentation. Follow the checklist step-by-step, validate after each change, and you'll succeed.

---

**Ready to begin? Start by reading `.planning/HANDOFF_TO_GEMINI.md`**
```

---

## 🎯 Prompt Selection Guide

**Use Short Version if:**
- Gemini has worked on EVA before
- You want quick start
- Gemini is experienced with similar tasks

**Use Full Version if:**
- First time working on EVA
- Need complete context
- Want detailed guidance
- Gemini is less familiar with Python/schemas

**Recommendation:** Use **Full Version** for best results - it's comprehensive and reduces questions later.
