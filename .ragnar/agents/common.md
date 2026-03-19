# Agent Common Behavioral Contract

> ไฟล์นี้กำหนด shared behavioral contract สำหรับ AI agents ทุกตัว
> Claude Code และ Codex ต้องปฏิบัติตาม contract นี้

---

## Core Principle

**อ่าน context ก่อน code** — เสมอ

ก่อนเขียน code หรือ suggest changes ใดๆ:
1. อ่าน `docs/AI_CONTEXT.md`
2. ดู task type → อ่าน docs ใน `.ragnar/routing.yaml[task_type].read`
3. ตรวจสอบ policies ใน `.ragnar/policies/global.yaml`

---

## Behavioral Rules

### 1. Context-First Workflow
```
Task รับมา → ระบุ task type → อ่าน docs ตาม routing → ทำงาน → update docs
```

### 2. Documentation Updates
- **เมื่องานเสร็จ**: update docs ตาม `routing.yaml[task_type].update`
- **ห้ามลืม**: CHANGELOG entry สำหรับทุก code change
- **Architecture changes**: ต้องมี ADR เสมอ

### 3. Code Standards
- Language: ดู `.ragnar/config.yaml` → `conventions.language_policy`
- Naming: snake_case (Python), follow existing patterns
- Comments: Thai language
- Function/variable names: English

### 4. Safety Rules
- ห้าม hardcode secrets → ใช้ env vars เสมอ
- ห้าม destructive DB ops โดยไม่ confirm
- ห้าม force-push protected branches
- ถ้าไม่แน่ใจ → ถามก่อน อย่า assume

### 5. Response Style
- อธิบายสิ่งที่กำลังทำและทำไม
- ถ้าทำ assumption → บอก user ให้ชัด
- ถ้ามี trade-offs → อธิบาย options
- ภาษาใน response: ตาม user's language (Thai ถ้า user พูด Thai)

---

## Task Type Identification

| คำบ่งชี้ | Task Type |
|---------|-----------|
| "implement", "add feature", "create" | `feature` |
| "fix", "bug", "error", "broken" | `bugfix` |
| "refactor", "clean up", "improve code" | `refactor` |
| "redesign", "change architecture", "migrate" | `architecture` |
| "docker", "deploy", "CI", "environment" | `infrastructure` |
| "env var", "config", "secret" | `env_change` |

---

## Completion Checklist

ก่อน report งานเสร็จ ตรวจสอบ:
- [ ] Code ทำงานตาม requirements
- [ ] ไม่มี hardcoded secrets
- [ ] CHANGELOG.md updated (ถ้า code change)
- [ ] Relevant docs updated ตาม routing
- [ ] ทำตาม language policy
- [ ] ไม่มี TODO ที่ยังค้างอยู่โดยไม่บอก user
