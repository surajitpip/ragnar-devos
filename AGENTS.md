# AGENTS.md — Bootstrap Loader for Codex

> ไฟล์นี้เป็น thin loader — rules และ context จริงอยู่ใน `.ragnar/` system

---

## Startup Protocol

เมื่อ Codex เริ่มทำงานใน repo นี้ ให้โหลดตามลำดับ:

1. **อ่าน** `docs/AI_CONTEXT.md` — core brain ของ project
2. **อ่าน** `.ragnar/agents/common.md` — shared behavioral contract
3. **อ่าน** `.ragnar/agents/codex_adapter.md` — Codex-specific instructions
4. **อ่าน** `.ragnar/routing.yaml` — task-type → doc routing
5. **อ่าน** `.ragnar/policies/global.yaml` — rules ที่ต้องทำตาม

---

## Quick Reference

| Need | File |
|------|------|
| Project context | `docs/AI_CONTEXT.md` |
| What to read/update per task | `.ragnar/routing.yaml` |
| Rules to follow | `.ragnar/policies/global.yaml` |
| Doc templates | `.ragnar/templates/` |
| Behavioral contract | `.ragnar/agents/common.md` |
| Run repo checks | `python scripts/check_repo_rules.py --mode working` |

---

## Core Rules (Summary)

1. **อ่าน AI_CONTEXT.md ก่อนเสมอ**
2. ระบุ task type → ทำตาม routing
3. ห้าม hardcode secrets
4. ห้าม force-push main
5. Code = English, Comments = Thai
6. Update CHANGELOG หลัง code change
7. ใช้ `uv` (ไม่ใช่ pip) สำหรับ Python packages
8. ถ้าไม่แน่ใจ → ถามก่อน

---

_Full rules: `.ragnar/policies/global.yaml`_
_Full routing: `.ragnar/routing.yaml`_
_Full behavioral contract: `.ragnar/agents/common.md`_
