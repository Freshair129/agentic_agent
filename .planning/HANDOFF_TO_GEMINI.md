# Handoff Document: MSP Logging Implementation

**To:** Gemini 3.0 Pro (Implementation Engineer)
**From:** Claude Code (Development Lead)
**Date:** 2026-01-19
**Project:** EVA v9.6.2 MSP Data Flow Gap Fix

---

## 🎯 Mission

You are implementing **Phase 1** of the MSP logging improvements for EVA v9.6.2. Your goal is to fix critical data logging gaps that break the causal chain in EVA's cognitive cycle.

**Success = All tests pass + No syntax errors + Backward compatible**

---

## 📚 Required Reading (In Order)

1. **MSP_DATA_FLOW_GAP_ANALYSIS.md** - Understand the problem
2. **MSP_LOGGING_STRATEGY_PROPOSAL.md** - Understand the solution
3. **MSP_IMPLEMENTATION_CHECKLIST.md** - Your step-by-step guide

**Time to read:** 20-30 minutes
**Do NOT skip reading** - You need context to make correct decisions.

---

## 🛠️ Your Environment

**Working Directory:**
```
E:\The Human Algorithm\T2\agent
```

**Python Version:**
```
Python 3.13.7
```

**Git Status:**
```bash
# Current branch: main
# You will create: feature/msp-logging-gaps
```

**Key Files You'll Modify:**
1. `memory_n_soul_passport/schema/Stimulus_Output_Schema.json` (CREATE NEW)
2. `memory_n_soul_passport/schema/Episodic_Memory_Schema_v2.json` (MODIFY)
3. `memory_n_soul_passport/schema/State_Storage_Schema.json` (MODIFY)
4. `memory_n_soul_passport/schema/State_Snapshot_Schema.json` (MODIFY)
5. `memory_n_soul_passport/memory_n_soul_passport_engine.py` (MODIFY)
6. `orchestrator/orchestrator.py` (MODIFY)

---

## 🚀 Quick Start

### Step 0: Setup

```bash
# 1. Verify working directory
pwd  # Should be: E:\The Human Algorithm\T2\agent

# 2. Create feature branch
git checkout -b feature/msp-logging-gaps

# 3. Create checkpoint
git add -A
git commit -m "chore: checkpoint before MSP Phase 1 implementation"

# 4. Verify Python
python --version  # Should be 3.13.7
```

### Step 1: Follow the Checklist

Open `MSP_IMPLEMENTATION_CHECKLIST.md` and work through **Task 1.1, 1.2, 1.3** sequentially.

**DO NOT SKIP VALIDATION COMMANDS** - Run every validation after each change.

---

## 🎯 Phase 1 Goals (What You're Doing)

### Task 1.1: Stimulus Input Logging
**Problem:** LLM→PhysioCore stimulus is not logged, breaking causal chain.
**Solution:** Create schema + Hook Orchestrator to log stimulus before sending to PhysioCore.

**Files:**
- NEW: `Stimulus_Output_Schema.json`
- MODIFY: `Episodic_Memory_Schema_v2.json` (reference new schema)
- MODIFY: `memory_n_soul_passport_engine.py` (add method)
- MODIFY: `orchestrator.py` (add hook)

### Task 1.2: Vitals Tracking
**Problem:** PhysioCore vitals (bpm, rpm, vagus_tone) not captured in MSP.
**Solution:** Expand State_Storage_Schema to include vitals field.

**Files:**
- MODIFY: `State_Storage_Schema.json`

### Task 1.3: Episodic Snapshot Expansion
**Problem:** State_Snapshot only captures emotional summary, missing bio-cognitive details.
**Solution:** Add missing fields from all systems.

**Files:**
- MODIFY: `State_Snapshot_Schema.json`

---

## 🧪 Testing Strategy

### After EACH file modification:

1. **JSON Syntax Validation**
   ```bash
   python -c "import json; json.load(open('path/to/file.json'))"
   ```

2. **Python Syntax Validation**
   ```bash
   python -m py_compile path/to/file.py
   ```

### After ALL modifications:

3. **Integration Test**
   ```bash
   python tests/test_msp_phase1.py
   ```

**Expected:** All tests pass with ✅

---

## 🚨 CRITICAL: Orchestrator Hook Location

This is the **trickiest part**. You need to find where `eva_stimuli` is generated in `orchestrator/orchestrator.py`.

**Search for:**
```bash
grep -n "eva_stimuli" orchestrator/orchestrator.py
```

**You're looking for code like:**
```python
eva_stimuli = self._extract_eva_stimuli(llm_response)
# OR
eva_stimuli = {...}  # Dict construction
# OR
eva_stimuli = some_function_call()
```

**What to do:**
1. Find the line where `eva_stimuli` is first assigned/created
2. Add MSP logging RIGHT AFTER that line, BEFORE `self.physio.step()`

**If you cannot find it:**
- Use `grep -A 5 -B 5 "eva_stimuli"` to see context
- Look for PhysioCore.step() calls
- **If still stuck:** STOP and report to Claude Code

---

## 🔍 What Claude Code Will Review

After you complete Phase 1, Claude Code will check:

### 1. Code Quality
- [ ] All files have correct syntax
- [ ] No broken imports
- [ ] Proper error handling
- [ ] Type hints present (where applicable)

### 2. Schema Correctness
- [ ] All new schemas are valid JSON Schema draft-07
- [ ] Required fields marked correctly
- [ ] Types match EVA's data structures
- [ ] No breaking changes to existing schemas

### 3. Integration
- [ ] MSP.log_stimulus_output() signature correct
- [ ] Orchestrator calls MSP BEFORE PhysioCore
- [ ] Backward compatibility maintained (old code still works)

### 4. Testing
- [ ] All validation commands pass
- [ ] Integration test passes
- [ ] No new errors in logs

### 5. Git Hygiene
- [ ] Commits are atomic (one feature per commit)
- [ ] Commit messages follow format
- [ ] No unnecessary files in commit

---

## 📋 Deliverables for Claude Code Review

When done, provide in your response:

```markdown
## Phase 1 Implementation Complete

**Status:** ✅ Complete / ⚠️ Partial / ❌ Issues

**Git Commit:** [commit hash]

**Files Modified:**
1. [file path] - [NEW/MODIFIED] - [brief description]
2. ...

**Test Results:**
```
[paste output of python tests/test_msp_phase1.py]
```

**Validation Results:**
- JSON schemas: ✅ All valid
- Python syntax: ✅ No errors
- Imports: ✅ All successful

**Issues Encountered:**
[None / Describe any issues]

**Questions for Claude Code:**
[Any clarifications needed]

**Orchestrator Hook Location:**
File: orchestrator/orchestrator.py
Line: [line number]
Context: [brief description of where you added the hook]
```

---

## 💡 Tips for Success

### 1. Read Before Coding
Don't rush. Understanding the problem is 50% of the solution.

### 2. Validate After Every Change
Run validation commands immediately after each file modification. Don't batch them.

### 3. Use Exact Paths
EVA uses Windows paths. Double-check every file path.

### 4. Preserve Formatting
When modifying JSON schemas, keep existing formatting style:
- 2-space indentation
- Properties sorted alphabetically (if existing file does this)

### 5. When in Doubt, Ask
If something is unclear, STOP and report to Claude Code. Don't guess.

---

## 🔧 Common Issues & Solutions

### Issue 1: "Cannot find eva_stimuli in Orchestrator"
**Solution:**
- Try: `grep -r "eva_stimuli" orchestrator/`
- Look for: `process_turn()`, `_process_llm_output()`, similar methods
- If still not found: Report to Claude Code with grep output

### Issue 2: "JSON validation fails"
**Solution:**
- Check for trailing commas (JSON doesn't allow them)
- Verify all quotes are double quotes (not single)
- Use jsonlint.com to find syntax errors

### Issue 3: "MSP class structure different"
**Solution:**
- Read the current MSP __init__ to understand structure
- Adapt the checklist code to match current style
- Report structural differences to Claude Code

### Issue 4: "Import error after modifications"
**Solution:**
- Check for circular imports
- Verify all imports at top of file
- Use absolute imports: `from memory_n_soul_passport.X import Y`

---

## 📞 Communication Protocol

### When to Report to Claude Code

**Immediately report if:**
1. Cannot find code location specified in checklist
2. Existing code structure very different from documentation
3. Test fails after implementation
4. Breaking change necessary (discuss first)
5. Ambiguous instruction in checklist

**Format for reporting:**
```
🚨 Issue Report

Task: [Task number from checklist]
Issue: [Brief description]
Context: [What you were doing]
Attempted: [What you tried]
Result: [What happened]
Need: [What you need from Claude Code]
```

### After completing each task (1.1, 1.2, 1.3)

Provide brief update:
```
✅ Task [X.X] Complete
Files: [list files changed]
Tests: [pass/fail]
Issues: [none/describe]
```

---

## 🎓 Learning Resources

If you need to understand EVA's architecture better:

1. **Registry:** `registry/eva_master_registry.yaml` - System contracts
2. **Docs:** `docs/03_Architecture/EVA_System_Architecture.md` - Architecture overview
3. **Concerns:** `.planning/codebase/CONCERNS.md` - Known issues

---

## ✅ Pre-Flight Checklist

Before starting, confirm:

- [ ] Read MSP_DATA_FLOW_GAP_ANALYSIS.md
- [ ] Read MSP_LOGGING_STRATEGY_PROPOSAL.md
- [ ] Read MSP_IMPLEMENTATION_CHECKLIST.md
- [ ] Working directory is correct
- [ ] Git branch created
- [ ] Checkpoint commit created
- [ ] Python version verified
- [ ] Text editor ready

---

## 🚀 Ready to Start?

1. Open `MSP_IMPLEMENTATION_CHECKLIST.md`
2. Start with **Task 1.1 Step 1.1.1**
3. Follow each step sequentially
4. Validate after each change
5. Report progress to Claude Code

**Remember:** Quality > Speed. Take your time, validate everything.

---

**Good luck! Claude Code is here to review your work. 🎯**
