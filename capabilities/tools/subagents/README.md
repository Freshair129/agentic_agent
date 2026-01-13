# The Archivist: Subagent Manual

> **"The Librarian of EVA's Memory System"**

This tool automates the maintenance of episodic memory, ensuring file names, IDs, and schemas are valid and synchronized.

## 🚀 Quick Command Cheat Sheet

### 1. 🔄 Sync Memories (Synchronization)

Fixes `episode_id` mismatches and renames files to match `EVA_EPxx` format. Scans both `archival_memory` and `session_memory/*/assets`.

**Safe Mode (Dry Run) - *Recommended First Step***

```bash
python tools/subagents/archivist_subagent.py --sync --dry-run
```

*Use this to see what WILL happen without changing any files.*

#### Apply Changes (Active Mode)

```bash
python tools/subagents/archivist_subagent.py --sync
```

*WARNING: This will rename files and edit JSON content.*

---

### 2. ✅ Validate Schemas (Quality Control)

Checks all `*.json` memory files against the official V2 Schema. Reports files with missing fields (e.g., `intent`, `bio_impacts`).

```bash
python tools/subagents/archivist_subagent.py --validate
```

---

### 3. 📝 Format Chat Logs (Readable Logs)

Converts a raw machine log (`.jsonl`) into a human-readable chat transcript.

```bash
python tools/subagents/archivist_subagent.py --format-log "path/to/input_log.jsonl" "path/to/output.txt"
```

**Example:**

```bash
python tools/subagents/archivist_subagent.py --format-log "eva/memory/episodic_log.jsonl" "debug_chat_session.txt"
```

---

## ⚙️ Configuration

You can change the folders it scans or the schema path here:
`tools/subagents/configs/archivist_config.yaml`
