# Architecture

**Project**: Ragnar DevOS
**Version**: v1
**Last Updated**: 2026-03-19

---

## System Overview

Ragnar DevOS เป็น **file-based governance system** ที่ทำงานผ่าน structured files ที่ AI agents อ่าน — ไม่ใช่ runtime service

```
┌─────────────────────────────────────────┐
│           AI Agent Session              │
│                                         │
│  Claude Code          Codex             │
│      │                  │               │
│  CLAUDE.md          AGENTS.md           │
│      │                  │               │
│      └──────────┬───────┘               │
│                 ▼                       │
│         .ragnar/ system                 │
│  ┌──────────────────────────────┐       │
│  │ config.yaml (project identity)│       │
│  │ routing.yaml (task routing)   │       │
│  │ policies/global.yaml (rules)  │       │
│  │ agents/common.md (contract)   │       │
│  │ agents/*_adapter.md           │       │
│  └──────────────────────────────┘       │
│                 │                       │
│                 ▼                       │
│         docs/ (knowledge base)          │
│  AI_CONTEXT.md → PRD → ARCHITECTURE    │
│  CHANGELOG → RUNBOOK → DECISIONS/      │
└─────────────────────────────────────────┘
         │
         ▼
┌─────────────────────┐
│  Enforcement Layer  │
│  check_repo_rules.py│
│  (pre-commit / CI)  │
└─────────────────────┘
```

---

## Two-Layer Agent Architecture

### Layer 1: Bootstrap (Root files)
```
/CLAUDE.md   →  thin loader  →  loads .ragnar/ system
/AGENTS.md   →  thin loader  →  loads .ragnar/ system
```

**Design rationale**: ทำให้ rules อยู่ที่เดียว (`.ragnar/`) — update ครั้งเดียว ทุก agent ได้รับ

### Layer 2: Governance (`.ragnar/`)
```
config.yaml      — project identity, conventions
routing.yaml     — task → docs mapping
policies/        — enforcement rules
templates/       — document templates
agents/          — behavioral contracts
checks/          — rule definitions
```

---

## Routing System

Task routing เป็น innovation หลักของระบบ:

```
User request → AI identifies task type → reads routing.yaml
→ loads required docs (read) → does work → updates docs (update)
→ runs checks (check)
```

6 task types: `feature`, `bugfix`, `refactor`, `architecture`, `infrastructure`, `env_change`

---

## Enforcement Script Architecture

`scripts/check_repo_rules.py`:
- **Input**: `.ragnar/checks/repo_rules.yaml`
- **Mode**: `staged` | `ci` | `working`
- **Logic**:
  1. Get changed files (จาก git diff ตาม mode)
  2. ตรวจ trigger patterns (fnmatch)
  3. ถ้า trigger match → ตรวจ require patterns
  4. ถ้า require ไม่ match → รายงาน violation
- **Output**: exit 0 (pass) หรือ exit 1 (fail)

---

## Starter Pack Architecture (python-dash-uv)

```
packs/python-dash-uv/
├── pack.yaml          — pack metadata
├── pyproject.toml     — Python project (uv)
├── app/
│   └── main.py        — Dash app entry point
├── Dockerfile         — multi-stage build
└── .dockerignore
```

**Multi-stage Dockerfile**:
```
Stage 1 (builder): python + uv → install deps
Stage 2 (runtime): python-slim + copy from builder
```

---

## Key Decisions

- [ADR-000](DECISIONS/000-template.md) — ADR Template

---

## Data Flow

```
Engineer → describes task to AI
AI → reads AI_CONTEXT.md
AI → identifies task type
AI → reads routing.yaml → loads required docs
AI → implements → updates docs
Engineer → commits
pre-commit / CI → runs check_repo_rules.py
check passes → merge allowed
```
