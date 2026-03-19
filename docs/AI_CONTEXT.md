# AI_CONTEXT.md — Core Brain

> **AI Agent**: อ่านไฟล์นี้ก่อนเริ่มทุก task เสมอ
> ไฟล์นี้คือ source of truth สำหรับ context ของ project นี้

---

## Project Identity

| Field | Value |
|-------|-------|
| **Name** | Ragnar DevOS |
| **Type** | AI-native Engineering Operating System |
| **Purpose** | Standardize AI agent workflows ข้าม projects ทั้งหมด |
| **Phase** | v1 — Starter Kit |
| **Owner** | พี่โอ๊ค |

**Mission**: สร้าง governance system ที่ทำให้ AI agents (Claude Code, Codex) ทำงานได้ consistent, safe, และ aligned กับ engineering standards ของทีม

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Runtime** | Python 3.12 |
| **Package Manager** | uv |
| **Web Framework** | Dash (Plotly) |
| **Database** | DuckDB |
| **Visualization** | Plotly |
| **App Server** | Gunicorn (production) |
| **Containerization** | Docker (multi-stage) |
| **CI** | GitHub Actions |

---

## Repository Structure

```
ragnar-devos/
├── CLAUDE.md              # Claude Code bootstrap loader
├── AGENTS.md              # Codex bootstrap loader
├── docs/
│   ├── AI_CONTEXT.md      # (ไฟล์นี้) — อ่านก่อนเสมอ
│   ├── PRD.md             # Product requirements
│   ├── ARCHITECTURE.md    # System architecture
│   ├── CHANGELOG.md       # Change history
│   ├── RUNBOOK.md         # Operations guide
│   ├── DECISIONS/         # Architecture Decision Records (ADRs)
│   └── PROMPTS/           # Structured prompts สำหรับ task types
├── .ragnar/               # Governance layer (อ่านทั้งหมดนี้)
│   ├── config.yaml        # Project identity & stack
│   ├── routing.yaml       # Task-type → doc routing (สำคัญมาก)
│   ├── policies/global.yaml  # Rules ที่ต้องทำตาม
│   ├── templates/         # Document templates
│   ├── agents/            # Agent behavioral contracts
│   └── checks/            # Rule definitions สำหรับ enforcement
├── packs/
│   └── python-dash-uv/    # Starter pack
└── scripts/
    └── check_repo_rules.py  # Enforcement script
```

---

## Key Conventions

### Naming
- **Python files**: `snake_case.py`
- **YAML/config files**: `kebab-case.yaml` หรือ `snake_case.yaml`
- **Markdown docs**: `UPPER_CASE.md` (สำหรับ primary docs) หรือ `kebab-case.md`
- **Variables/functions**: `snake_case` (Python)
- **Constants**: `UPPER_SNAKE_CASE`
- **Classes**: `PascalCase`

### Branching
- `main` — production-ready เท่านั้น
- `feature/<name>` — new features
- `fix/<name>` — bug fixes
- `refactor/<name>` — refactoring
- `chore/<name>` — maintenance, config changes
- ห้าม force-push `main`

### Commit Messages
Format: `<type>(<scope>): <description>`

Types: `feat`, `fix`, `refactor`, `docs`, `chore`, `test`, `perf`

ตัวอย่าง:
- `feat(dashboard): add revenue chart`
- `fix(data): handle null values in duckdb query`
- `docs(runbook): update deployment steps`

### Language Policy
- **Code, variables, function names, commit messages**: English
- **Comments, docstrings, doc body, user-facing text**: Thai
- **Section headers, technical terms**: English

---

## Domain Knowledge

> _Placeholder สำหรับ project-specific domain knowledge_
> อัพเดตส่วนนี้เมื่อ instantiate repo นี้ใน project จริง

- **Business Domain**: (ระบุ domain ของ project)
- **Key Entities**: (ระบุ entities หลัก)
- **Business Rules**: (ระบุ rules ที่สำคัญ)
- **External Dependencies**: (APIs, services ภายนอก)

---

## Current State

### What Exists
- [x] Governance layer (`.ragnar/`) — config, routing, policies, templates, agents, checks
- [x] Agent bootstrap files — `CLAUDE.md`, `AGENTS.md`
- [x] Project docs — PRD, ARCHITECTURE, CHANGELOG, RUNBOOK
- [x] Starter pack — `packs/python-dash-uv/`
- [x] Enforcement script — `scripts/check_repo_rules.py`

### In Progress
- [ ] (ว่างเปล่า — เพิ่มเมื่อมี active work)

### Next
- [ ] Instantiate pack ใน project จริง
- [ ] Add project-specific domain knowledge
- [ ] Setup CI/CD pipeline
- [ ] Add more packs (FastAPI, Next.js, etc.)

---

## Task Routing

ดู `.ragnar/routing.yaml` สำหรับ mapping เต็ม

| Task Type | Read Before | Update After |
|-----------|------------|--------------|
| `feature` | PRD, ARCHITECTURE, CHANGELOG | CHANGELOG |
| `bugfix` | RUNBOOK, CHANGELOG | CHANGELOG |
| `refactor` | ARCHITECTURE | CHANGELOG |
| `architecture` | ARCHITECTURE, all ADRs | ARCHITECTURE, new ADR |
| `infrastructure` | RUNBOOK | RUNBOOK, CHANGELOG |
| `env_change` | .env.example | .env.example |

---

_Last updated: 2026-03-19_
_ไฟล์นี้ควร update ทุกครั้งที่ project state เปลี่ยน_
