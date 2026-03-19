# Claude Code Adapter

> Claude-specific behavioral instructions
> อ่านร่วมกับ `.ragnar/agents/common.md`

---

## Claude Code Capabilities in This Repo

### Tools Available
- **Read/Write/Edit**: จัดการ files ทั้งหมดใน repo
- **Bash**: รัน scripts เช่น `python scripts/check_repo_rules.py`
- **Glob/Grep**: ค้นหา files และ content
- **Agent**: spawn subagents สำหรับงานซับซ้อน

### Recommended Workflows

**เริ่ม feature ใหม่**:
```
1. Read docs/AI_CONTEXT.md
2. Read docs/PRD.md
3. Read .ragnar/routing.yaml → feature section
4. Implement
5. Update docs/CHANGELOG.md
6. Run: python scripts/check_repo_rules.py --mode working
```

**Debug issue**:
```
1. Read docs/AI_CONTEXT.md
2. Read docs/RUNBOOK.md (troubleshooting section)
3. Grep for error pattern ใน codebase
4. Fix + Update CHANGELOG
```

---

## Claude-Specific Instructions

### Memory System
- บันทึก important project context ใน Claude memory
- อ้างอิง `docs/AI_CONTEXT.md` เมื่อต้องการ project context
- อัพเดต memory เมื่อ project state เปลี่ยน significantly

### File Operations
- อ่านไฟล์ก่อน edit เสมอ (ไม่ overwrite โดยไม่ดูก่อน)
- ใช้ Edit tool สำหรับ small changes, Write tool สำหรับ new files
- Commit ด้วย conventional commit format

### Bash Commands
```bash
# ตรวจสอบ repo rules
python scripts/check_repo_rules.py --mode working

# รัน Dash app
cd packs/python-dash-uv && uv run python app/main.py

# Build Docker image
docker build -t ragnar-app packs/python-dash-uv/
```

### Code Review Mode
เมื่อ review code ให้ check:
1. ตาม `policies/global.yaml` rules
2. Language policy (Thai comments, English code)
3. No hardcoded secrets
4. CHANGELOG updated

---

## Anti-Patterns (อย่าทำ)

- อย่า skip อ่าน AI_CONTEXT.md
- อย่า modify files หลายๆ ไฟล์พร้อมกันโดยไม่บอก plan ก่อน
- อย่า assume project structure — ใช้ Glob/Read ตรวจสอบก่อน
- อย่า create files ที่ไม่จำเป็น
- อย่า hardcode ค่าที่ควรเป็น env var
