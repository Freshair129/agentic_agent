---
description: Create a project checkpoint by updating documentation, syncing context, and commiting to git.
---

# Checkpoint Protocol

This workflow defines the standard procedure for "Checkpointing" the project. It ensures that code, documentation, and agent rules are synchronized before generating a git commit.

## 1. Documentation & ADR Scan

- **Review:** Scan `agent/docs/*.md` and `agent/docs/adr/*.md`
- **Update:** If recent code changes affect Architecture or Decisions, update the relevant MD files.
- **Log:** Update `agent/docs/CHANGELOG.md` with a summary of changes in this checkpoint.
- **Create ADR:** If a major decision was made (e.g., "MSP Centric Memory"), ensure an ADR exists for it.

## 2. Context Synchronization

- **Run Archivist:** Execute the `run_archivist` workflow to sync `.agent/rules/`.

   // turbo
   python tools/subagents/archivist_subagent.py --sync-rules

## 3. Git Snapshot

- **Stage:** Add all changes.
- **Commit:** Create a commit with a descriptive message including the `[Checkpoint]` tag.

   ```powershell
   git add .
   git commit -m "[Checkpoint] Updated docs, synced agent rules, and snapshot codebase."
   ```

---
*Trigger this workflow by saying "Checkpoint" or "/checkpoint".*
