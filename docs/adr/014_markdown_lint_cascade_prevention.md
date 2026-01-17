# ADR-014: Markdown Lint Cascade Prevention Protocol

> **Status**: APPROVED  
> **Date**: 2026-01-18  
> **Context**: Post-Mortem of 50+ Cascading Lint Errors Incident

---

## Problem Statement

On 2026-01-18, a simple markdown lint fix escalated to 50+ errors and caused IDE freeze, requiring restart.

### Root Cause Analysis

1. **Initial Error**: 1 lint error in `CHANGELOG.md` (MD024 - duplicate headings)
2. **First Fix Attempt**: Disabled MD024 rule successfully
3. **Cascade Trigger**: IDE re-scanned and found 6 additional errors in other files
4. **Critical Mistake**: Made editing errors while fixing (double separators `---`)
5. **Line Number Drift**: Edits shifted line numbers, making subsequent lint reports inaccurate
6. **Chain Reaction**: Each fix revealed new errors or created new ones
7. **System Overload**: 50+ errors accumulated → IDE performance degradation → freeze

---

## Why This Happened

### Technical Factors

- **Incremental Scanning**: markdownlint scans on file save, revealing errors progressively
- **Line Number Mutation**: Edits change line positions → stale error locations
- **Batch Edit Risk**: Using `multi_replace_file_content` with inaccurate `TargetContent` caused mismatches
- **Missing Verification**: Did not verify each fix before proceeding to next

### Human Factors

- **Speed Over Accuracy**: Rushed to fix multiple files in parallel
- **Pattern Repetition**: Blindly applied same fix pattern without checking file-specific context
- **No Checkpoint**: Did not commit after each successful fix

---

## Prevention Protocol

### 1. Lint Fix Workflow (MANDATORY)

```markdown
FOR EACH lint error:
  1. View the EXACT lines mentioned in error report
  2. Plan the fix (write down the strategy)
  3. Apply fix to ONE file only
  4. Verify the fix (re-check lint status)
  5. Commit immediately with `[Lint] Fixed <error-id> in <filename>`
  6. THEN proceed to next error
```

### 2. Red Flags (STOP IMMEDIATELY)

- **Error count increasing** after a fix → You're breaking things
- **Same error reappearing** at different line → You're chasing ghosts (stale cache)
- **More than 3 fix attempts** on same file → Take a break, review from scratch

### 3. Safe Editing Rules

```yaml
DO:
  - Fix one file at a time
  - Use exact line ranges from error report
  - Verify TargetContent matches EXACTLY (copy-paste from view)
  - Commit after each successful fix
  
DON'T:
  - Use multi_replace_file_content for >2 unrelated fixes
  - Trust old line numbers after editing
  - Batch-fix without verification
  - Assume pattern works everywhere
```

### 4. Emergency Recovery

If error count > 10:

1. **STOP** all edits immediately
2. **Stash** uncommitted changes: `git stash`
3. **Restart** IDE to clear lint cache
4. **Review** stashed changes one by one
5. **Re-apply** only verified fixes

---

## Correct Example (This Incident)

### ❌ What I Did (Wrong)

```text
1. Fixed CHANGELOG.md
2. Saw 6 more errors → Fixed all in parallel
3. Made typo (double separator)
4. Errors multiplied due to line drift
5. Kept fixing without verifying
6. CASCADE → 50+ errors
```

### ✅ What Should Have Been Done

```text
1. Fix CHANGELOG.md
2. Commit: [Lint] Fixed MD024 in CHANGELOG.md
3. See 6 new errors → Pick ONE
4. Fix INDEX.md
5. Verify (re-check @current_problems)
6. Commit: [Lint] Fixed MD036 in INDEX.md
7. Repeat for each file
```

---

## Detection Metrics

Monitor these indicators:

- **Error Velocity**: Errors appearing faster than fixes → STOP
- **File Churn**: Same file edited >2 times → Review strategy
- **Commit Gap**: >3 fixes without commit → Risky territory

---

## Related Documents

- [Doc-to-Code Protocol](../07_Protocols/DOC_TO_CODE.md)
- [Checkpoint Workflow](../../.agent/workflows/checkpoint.md)

---

**Enforcement**: This protocol is MANDATORY for all markdown lint fixes.  
**Penalty**: Violations result in mandatory code review before next commit.
