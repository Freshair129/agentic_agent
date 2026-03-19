# Changelog System — EVA v9.6.2

**Version:** Sliding Window v2
**Effective:** 2026-03-19
**Author:** System Architecture Team

---

## โครงสร้าง

```
CHANGELOG.md  (docs/00_Governance/)    ← sliding window (ขนาดคงที่เสมอ)
changelog/                              ← full detail entries
  CL-YYYYMMDD-NNN.md                   ← individual entry files
CHANGELOG_SYSTEM.md                     ← ไฟล์นี้ (spec)
```

---

## CHANGELOG.md Format

```markdown
**LATEST:** CL-[YYYYMMDD]-[NNN] | v[X.Y.Z] | [YYYY-MM-DD]

---

## Recent (last 5 — full content)

### [CL-20260319-001] v9.6.3 — Description
...full content...

---

## Index (older entries)

| ID | Name | Version | Date | Severity | Tags |
|---|---|---|---|---|---|
| CL-20260118-001 | Cognitive Flow 2.0 | v9.6.2 | 2026-01-18 | MAJOR | #architecture #orchestrator |
```

### กฎ Sliding Window
- **Recent section** = 5 entries ล่าสุดเท่านั้น (full content)
- เมื่อเพิ่ม entry ใหม่ที่ทำให้ Recent เกิน 5 → entry เก่าสุดถูกย้ายไป Index table
- Index table เก็บ summary เท่านั้น — full detail อยู่ใน `changelog/{id}.md`

---

## CL-[YYYYMMDD]-[NNN].md Format

```markdown
# [CL-ID] — [ชื่อ]

**Version:** vX.Y.Z
**Date:** YYYY-MM-DD
**Severity:** PATCH | MINOR | MAJOR | HOTFIX
**Tags:** #tag1 #tag2
**Commits:** abc1234, def5678
**Author:** Claude | Gemini

---

## Summary
[1-2 ประโยคสรุป]

## Changes
[รายละเอียดทุกอย่างที่เปลี่ยน]

## Files Modified
[list ไฟล์]

## Verification
[วิธีตรวจสอบว่าแก้ถูก]
```

---

## Severity Levels

| Level | ใช้เมื่อ | ตัวอย่าง |
|---|---|---|
| `HOTFIX` | Production emergency, crash | API crash fix |
| `MAJOR` | Breaking change, schema drop, contract เปลี่ยน | Cognitive Flow 2.0 |
| `MINOR` | Feature ใหม่, module ใหม่, backward compatible | Add Engram System |
| `PATCH` | Bugfix, config tweak, doc fix | Fix hormone decay rate |

---

## ID Format

```
CL-[YYYYMMDD]-[NNN]

YYYYMMDD = วันที่ commit
NNN      = serial ต่อวัน (001, 002, ...)

ตัวอย่าง: CL-20260319-001
```

---

## Tags Reference

| Tag | ความหมาย |
|---|---|
| `#architecture` | System architecture เปลี่ยน |
| `#orchestrator` | Orchestrator / CIM / CognitiveFlow |
| `#physio` | PhysioCore (hormones, vitals, reflex) |
| `#matrix` | EVA Matrix (9D psychology) |
| `#memory` | MSP / episodic / semantic / sensory |
| `#rag` | AgenticRAG / 7-stream retrieval |
| `#rms` | Resonance Memory System |
| `#bus` | Resonance Bus channels |
| `#schema` | JSON Schema เปลี่ยน |
| `#config` | YAML config เปลี่ยน |
| `#api` | FastAPI / WebSocket endpoints |
| `#webui` | Vue.js frontend |
| `#breaking` | Breaking change |
| `#bugfix` | Bug fix |
| `#docs` | Documentation only |

---

## Agent Behavior Rules

### Claude (Lead Architect)
- เป็นผู้อัปเดต CHANGELOG เท่านั้น
- ต้องทำหลัง commit ทุกครั้ง
- สร้าง `changelog/CL-{id}.md` + อัปเดต `docs/00_Governance/CHANGELOG.md`

### Gemini (Partner Agent)
- อ่าน LATEST pointer ก่อนเริ่มงานทุกครั้ง
- ไม่ต้องแตะ CHANGELOG — แจ้ง Claude ว่าจบงานแล้ว
