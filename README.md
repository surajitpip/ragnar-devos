# Ragnar DevOS

**AI-native Engineering Operating System** — standardize วิธีการทำงานของ AI agents ข้าม projects ทั้งหมด

ไม่ใช่แค่ template repo แต่เป็น **AI Governance System for Engineering** ที่มี routing, policies, enforcement, และ agent adapters

---

## What is this?

Ragnar DevOS กำหนด "สัญญา" ระหว่าง engineer และ AI agent:
- **AI รู้ว่าต้องอ่านอะไรก่อนเริ่มงาน** (routing.yaml)
- **AI รู้ว่าต้อง update อะไรเมื่องานเสร็จ** (routing.yaml)
- **AI รู้ rules ที่ต้องทำตาม** (policies/global.yaml)
- **ระบบ enforce rules อัตโนมัติ** (check_repo_rules.py)

## Repository Structure

```
ragnar-devos/
├── CLAUDE.md              # Bootstrap loader สำหรับ Claude Code
├── AGENTS.md              # Bootstrap loader สำหรับ Codex
├── docs/
│   ├── AI_CONTEXT.md      # Core brain — AI อ่านก่อนเสมอ
│   ├── PRD.md             # Product requirements
│   ├── ARCHITECTURE.md    # System architecture
│   ├── CHANGELOG.md       # Change log
│   ├── RUNBOOK.md         # Operations runbook
│   ├── DECISIONS/         # Architecture Decision Records
│   └── PROMPTS/           # Structured prompts สำหรับ AI
├── .ragnar/               # Governance layer
│   ├── config.yaml        # Project identity & stack
│   ├── routing.yaml       # Task-type → doc routing
│   ├── policies/          # AI rules
│   ├── templates/         # Document templates
│   ├── agents/            # Agent behavioral contracts
│   └── checks/            # Rule definitions
├── packs/
│   └── python-dash-uv/    # Starter pack: Python + Dash + uv
└── scripts/
    └── check_repo_rules.py # Enforcement script
```

## Quick Start

```bash
# Clone และ setup
git clone <repo-url>
cd ragnar-devos
cp .env.example .env

# ดู project identity
cat .ragnar/config.yaml

# รัน check (ควร pass เมื่อไม่มี changes)
make check

# รัน Dash app (ต้องมี uv)
cd packs/python-dash-uv
uv run python app/main.py
```

## Make Commands

```bash
make check          # รัน repo rules check (working tree)
make check-staged   # รัน check สำหรับ staged files (pre-commit)
make check-ci       # รัน check สำหรับ CI
make help           # แสดง commands ทั้งหมด
```

## For AI Agents

- **Claude Code**: อ่าน `CLAUDE.md` → โหลด `.ragnar/` system อัตโนมัติ
- **Codex**: อ่าน `AGENTS.md` → โหลด `.ragnar/` system อัตโนมัติ
- **Core brain**: `docs/AI_CONTEXT.md` — อ่านก่อนทุก task เสมอ
- **Task routing**: `.ragnar/routing.yaml` — บอก AI ว่าต้องอ่าน/update อะไร

## Language Policy

| Context | Language |
|---------|----------|
| Code, variables, function names, commits | **English** |
| Comments, docstrings, docs body, user-facing text | **Thai** |
| Section headers, technical terms | **English** |

---

_Ragnar DevOS — Built for AI-native engineering teams_
