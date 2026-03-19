# Codex Adapter

> Codex-specific behavioral instructions
> อ่านร่วมกับ `.ragnar/agents/common.md`

---

## Codex Capabilities in This Repo

Codex (OpenAI Codex / GitHub Copilot agent) มี capabilities:
- Code generation และ completion
- File read/write ผ่าน tools
- Terminal command execution
- Web search (ถ้า enabled)

---

## Codex-Specific Instructions

### Session Start Protocol
```
1. Read AGENTS.md (ไฟล์นี้ถูกโหลดแล้ว)
2. Read docs/AI_CONTEXT.md — project context
3. Read .ragnar/agents/common.md — shared rules
4. ระบุ task type จาก user request
5. Read docs ตาม .ragnar/routing.yaml[task_type].read
```

### Code Generation Standards
- Generate code ด้วย Python 3.12+ syntax
- ใช้ type hints สำหรับ function signatures
- Comments เป็น Thai, code เป็น English
- Import order: stdlib → third-party → local

### Terminal Commands
```bash
# ตรวจสอบ repo rules
python scripts/check_repo_rules.py --mode working

# Install dependencies ด้วย uv
cd packs/python-dash-uv && uv sync

# รัน tests (ถ้ามี)
uv run pytest
```

### File Creation Rules
- สร้างไฟล์ใหม่เฉพาะเมื่อ explicitly required
- ตรวจสอบ file structure ก่อนสร้าง
- ทำตาม naming conventions ใน `.ragnar/config.yaml`

---

## Task Execution Pattern

```
User: "implement X"
Codex:
  1. อ่าน AI_CONTEXT.md → เข้าใจ project
  2. ระบุ task type: feature/bugfix/etc.
  3. อ่าน routing docs
  4. Plan → แสดง plan ให้ user confirm
  5. Implement
  6. Update docs (CHANGELOG, etc.)
  7. แสดง summary ของ changes
```

---

## Anti-Patterns (อย่าทำ)

- อย่า generate boilerplate code โดยไม่เข้าใจ context
- อย่า ignore policies ใน `.ragnar/policies/global.yaml`
- อย่า suggest `pip install` — ใช้ `uv add` แทน
- อย่า create `.env` ไฟล์จริง — แก้เฉพาะ `.env.example`
