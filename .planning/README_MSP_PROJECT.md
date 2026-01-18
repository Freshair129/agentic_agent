# MSP Data Logging Project - Documentation Index

**Project:** Fix MSP Data Flow Gaps in EVA v9.6.2
**Status:** Ready for Implementation
**Phase:** Phase 1 (Critical Gaps)
**Date:** 2026-01-19

---

## 📚 Project Documents

### 1. Analysis Documents (Read First)

#### MSP_DATA_FLOW_GAP_ANALYSIS.md
**Purpose:** Problem identification and analysis
**Audience:** All stakeholders
**Summary:**
- System-by-system audit of MSP data coverage
- Identified 18 missing data fields across 4 systems
- Critical finding: Stimulus input from LLM not logged
- Gap severity ratings and impact assessment

**Key Findings:**
- 🔴 **Critical**: Stimulus logging missing (breaks causal chain)
- 🔴 **High**: PhysioCore vitals not captured
- 🟡 **Medium**: RMS texture and trauma flags missing
- 🟡 **Medium**: Artifact Qualia depth/texture missing

**Read this to:** Understand what's broken and why it matters

---

#### MSP_LOGGING_STRATEGY_PROPOSAL.md
**Purpose:** Solution design and implementation plan
**Audience:** Technical team
**Summary:**
- 3-phase implementation plan (6 weeks)
- Phase 1: Critical gaps (stimulus, vitals, schema expansion)
- Phase 2: System integration and pipeline
- Phase 3: Validation and monitoring
- Includes code examples and testing strategy

**Key Deliverables:**
- New schema: `Stimulus_Output_Schema.json`
- Expanded schemas: `State_Storage_Schema.json`, `State_Snapshot_Schema.json`
- New MSP method: `log_stimulus_output()`
- Orchestrator hooks for stimulus logging

**Read this to:** Understand the solution and implementation approach

---

### 2. Implementation Documents (For Gemini 3.0 Pro)

#### HANDOFF_TO_GEMINI.md
**Purpose:** Onboarding and context for implementation engineer
**Audience:** Gemini 3.0 Pro
**Summary:**
- Mission briefing and objectives
- Environment setup instructions
- Quick start guide
- Critical warnings and gotchas
- Communication protocol

**Contains:**
- Reading list (required before starting)
- Environment details (paths, Python version)
- Quick start commands
- Tips for success
- Issue reporting protocol

**Use this to:** Onboard Gemini and set expectations

---

#### MSP_IMPLEMENTATION_CHECKLIST.md
**Purpose:** Step-by-step implementation guide
**Audience:** Gemini 3.0 Pro (Developer)
**Summary:**
- Detailed checklist for all Phase 1 tasks
- Task 1.1: Stimulus logging (4 steps)
- Task 1.2: Vitals expansion (1 step)
- Task 1.3: Schema expansion (1 step)
- Validation commands for each step
- Integration test suite

**Structure:**
```
Phase 1: Critical Gaps
├── Task 1.1: Stimulus Input Logging
│   ├── Step 1.1.1: Create schema ✅
│   ├── Step 1.1.2: Update episodic schema ✅
│   ├── Step 1.1.3: Add MSP method ✅
│   └── Step 1.1.4: Hook Orchestrator ✅
├── Task 1.2: Expand State_Storage_Schema ✅
└── Task 1.3: Expand State_Snapshot_Schema ✅
```

**Use this to:** Follow exact implementation steps with validation

---

### 3. Review Documents (For Claude Code)

#### CLAUDE_REVIEW_GUIDE.md
**Purpose:** Code review checklist and quality gates
**Audience:** Claude Code (Reviewer)
**Summary:**
- File-by-file review checklist
- Validation commands for each file
- Code quality criteria
- Integration testing procedures
- Approval decision matrix

**Review Criteria:**
- Schema correctness (JSON syntax, structure, types)
- Code quality (syntax, type hints, error handling)
- Integration (MSP method, Orchestrator hook)
- Backward compatibility
- Testing (all tests pass)

**Contains:**
- Validation commands
- Common issues and debugging
- Response templates (Approve/Request Changes/Critical)

**Use this to:** Systematically review Gemini's implementation

---

## 🎯 Project Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                    Project Workflow                         │
└─────────────────────────────────────────────────────────────┘

Step 1: Analysis (COMPLETE ✅)
├── Claude Code analyzed EVA codebase
├── Identified 18 data gaps
└── Created MSP_DATA_FLOW_GAP_ANALYSIS.md

Step 2: Solution Design (COMPLETE ✅)
├── Claude Code designed 3-phase solution
├── Created implementation plan
└── Created MSP_LOGGING_STRATEGY_PROPOSAL.md

Step 3: Implementation Prep (COMPLETE ✅)
├── Claude Code created checklist
├── Created handoff document
├── Created review guide
└── Ready for handoff to Gemini

Step 4: Implementation (NEXT - For Gemini)
├── Gemini reads all documents
├── Creates feature branch
├── Implements Phase 1 (6 tasks)
├── Runs validation after each step
└── Runs integration tests

Step 5: Review (For Claude Code)
├── Claude Code reviews implementation
├── Runs all validation commands
├── Checks code quality
├── Verifies tests pass
└── APPROVE / REQUEST CHANGES

Step 6: Merge (If approved)
├── Merge to main branch
├── Tag as msp-phase1-complete
└── Begin Phase 2 planning
```

---

## 📂 File Structure

```
E:\The Human Algorithm\T2\agent\
├── .planning/
│   ├── README_MSP_PROJECT.md           ← You are here
│   ├── MSP_DATA_FLOW_GAP_ANALYSIS.md   ← Problem analysis
│   ├── MSP_LOGGING_STRATEGY_PROPOSAL.md ← Solution design
│   ├── MSP_IMPLEMENTATION_CHECKLIST.md  ← Step-by-step guide
│   ├── HANDOFF_TO_GEMINI.md            ← Gemini onboarding
│   └── CLAUDE_REVIEW_GUIDE.md          ← Review checklist
│
├── memory_n_soul_passport/
│   ├── schema/
│   │   ├── Stimulus_Output_Schema.json          ← CREATE NEW
│   │   ├── Episodic_Memory_Schema_v2.json       ← MODIFY
│   │   ├── State_Storage_Schema.json            ← MODIFY
│   │   └── State_Snapshot_Schema.json           ← MODIFY
│   └── memory_n_soul_passport_engine.py         ← MODIFY
│
├── orchestrator/
│   └── orchestrator.py                          ← MODIFY
│
└── tests/
    └── test_msp_phase1.py                       ← CREATE NEW
```

---

## 🎯 Quick Reference

### For Gemini 3.0 Pro (Developer)

**Start here:**
1. Read `HANDOFF_TO_GEMINI.md` (onboarding)
2. Read `MSP_DATA_FLOW_GAP_ANALYSIS.md` (understand problem)
3. Read `MSP_LOGGING_STRATEGY_PROPOSAL.md` (understand solution)
4. Open `MSP_IMPLEMENTATION_CHECKLIST.md` (your step-by-step guide)
5. Create branch: `git checkout -b feature/msp-logging-gaps`
6. Start implementing Task 1.1

**When done:**
- Run all validation commands
- Run integration test
- Report results to Claude Code

---

### For Claude Code (Reviewer)

**When Gemini reports completion:**
1. Open `CLAUDE_REVIEW_GUIDE.md`
2. Run pre-review commands
3. Review each file systematically
4. Run all validation commands
5. Run integration tests
6. Make decision: APPROVE / REQUEST CHANGES

**Decision Criteria:**
- All tests pass → ✅
- No syntax errors → ✅
- Backward compatible → ✅
- Code quality good → ✅

**If all ✅ → APPROVE**

---

## 📊 Project Metrics

### Phase 1 Scope

| Metric | Value |
|--------|-------|
| Files to modify | 5 |
| Files to create | 2 |
| Total files changed | 7 |
| Lines of code (est.) | ~500 |
| Schemas updated | 4 |
| New methods | 1 |
| Integration points | 2 |
| Test files | 1 |

### Implementation Estimates

| Task | Complexity | Time Estimate |
|------|------------|---------------|
| Task 1.1: Stimulus logging | Medium | 2-3 hours |
| Task 1.2: Vitals expansion | Low | 30 minutes |
| Task 1.3: Schema expansion | Medium | 1-2 hours |
| Testing | Low | 30 minutes |
| **Total** | | **4-6 hours** |

### Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Cannot find stimulus location in Orchestrator | Medium | High | Detailed grep commands provided, escalation protocol |
| Breaking changes to schemas | Low | High | Backward compatibility checked, only additive changes |
| Test failures | Low | Medium | Validation commands at each step |
| Import errors | Low | Low | Syntax checking built in |

---

## ✅ Success Criteria

### Phase 1 is successful when:

**Functional:**
- [ ] Stimulus logging works (LLM→MSP→Episodic Memory)
- [ ] Vitals captured in real-time state
- [ ] All new fields present in episodic snapshots

**Technical:**
- [ ] All 4 schemas valid JSON Schema draft-07
- [ ] MSP method compiles and works
- [ ] Orchestrator hook in correct location
- [ ] All tests pass
- [ ] No syntax errors
- [ ] No import errors

**Quality:**
- [ ] Backward compatible (old code still works)
- [ ] Code follows EVA conventions
- [ ] Proper error handling
- [ ] Validation at boundaries

**Process:**
- [ ] Git branch clean
- [ ] Commit message follows format
- [ ] Documentation updated
- [ ] Claude Code approved

---

## 🚀 Getting Started

### For Gemini 3.0 Pro

```bash
# 1. Navigate to project
cd "E:\The Human Algorithm\T2\agent"

# 2. Read documentation
cat .planning/HANDOFF_TO_GEMINI.md

# 3. Create branch
git checkout -b feature/msp-logging-gaps

# 4. Start implementing
# Follow: .planning/MSP_IMPLEMENTATION_CHECKLIST.md
```

### For Claude Code

```bash
# When Gemini reports completion:

# 1. Check out branch
git checkout feature/msp-logging-gaps

# 2. Open review guide
cat .planning/CLAUDE_REVIEW_GUIDE.md

# 3. Start review
python tests/test_msp_phase1.py
```

---

## 📞 Support

**If Gemini has questions:**
- Refer to `HANDOFF_TO_GEMINI.md` Section "Communication Protocol"
- Use issue report format
- Tag Claude Code

**If Claude Code needs context:**
- Refer back to `MSP_DATA_FLOW_GAP_ANALYSIS.md`
- Check `MSP_LOGGING_STRATEGY_PROPOSAL.md` for design rationale
- Review `registry/eva_master_registry.yaml` for contracts

---

## 📝 Change Log

| Date | Event | Document |
|------|-------|----------|
| 2026-01-19 | Gap analysis completed | MSP_DATA_FLOW_GAP_ANALYSIS.md |
| 2026-01-19 | Solution designed | MSP_LOGGING_STRATEGY_PROPOSAL.md |
| 2026-01-19 | Implementation plan created | MSP_IMPLEMENTATION_CHECKLIST.md |
| 2026-01-19 | Handoff package prepared | HANDOFF_TO_GEMINI.md, CLAUDE_REVIEW_GUIDE.md |
| 2026-01-19 | Ready for implementation | README_MSP_PROJECT.md |

---

## 🎯 Next Steps

**Immediate (Now):**
1. User hands off to Gemini 3.0 Pro
2. Gemini reads all documentation
3. Gemini implements Phase 1

**After Phase 1:**
1. Claude Code reviews implementation
2. If approved: Merge and tag
3. Plan Phase 2 (System Integration)

**Future Phases:**
- Phase 2: Pipeline integration (Week 3-4)
- Phase 3: Validation & monitoring (Week 5-6)

---

**Project Status:** 🟢 Ready for Implementation
**Last Updated:** 2026-01-19
**Prepared By:** Claude Code
