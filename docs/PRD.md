# Product Requirements Document (PRD)

**Project**: Ragnar DevOS
**Version**: v1
**Status**: Active
**Last Updated**: 2026-03-19

---

## Problem Statement

Engineering teams ที่ใช้ AI agents (Claude Code, Codex) ประสบปัญหา:
1. **Inconsistency** — AI ทำงานต่างกันข้าม projects เพราะไม่มี shared context
2. **Missing updates** — AI implement feature แล้วลืม update CHANGELOG, docs
3. **Safety issues** — AI บาง instance hardcode secrets หรือ force-push main
4. **No governance** — ไม่มีระบบ enforce standards อัตโนมัติ

---

## Solution

**AI Governance Layer** ที่ standardize ทุกอย่าง:
- Context loading ที่ consistent ทุกครั้ง
- Task routing ที่บอก AI ว่าต้องทำอะไรก่อน/หลัง
- Policy enforcement อัตโนมัติ
- Agent adapters ที่ tailor behavior ต่อ agent type

---

## Users

| User | Context | Needs |
|------|---------|-------|
| **AI Agents** (Claude, Codex) | ทำงานใน repo | Context, routing, rules |
| **Engineers** | ใช้งาน AI agents | Consistency, safety, compliance |
| **Team Leads** | Govern AI usage | Visibility, enforcement |

---

## Core Features (v1)

### F1: Governance Layer (`.ragnar/`)
- **config.yaml** — project identity และ stack
- **routing.yaml** — task-type → doc read/update mapping
- **policies/global.yaml** — rules ที่ AI ต้องทำตาม
- **templates/** — document templates

### F2: Agent Adapters
- **CLAUDE.md** — bootstrap loader สำหรับ Claude Code
- **AGENTS.md** — bootstrap loader สำหรับ Codex
- **agents/common.md** — shared behavioral contract
- **agents/claude_adapter.md** / **codex_adapter.md** — agent-specific rules

### F3: Enforcement Script
- **check_repo_rules.py** — pure Python, stdlib only
- Modes: staged (pre-commit), ci, working (manual)
- อ่าน rules จาก `checks/repo_rules.yaml`
- Exit code 0 = pass, 1 = fail

### F4: Starter Pack (python-dash-uv)
- Python 3.12 + uv + Dash + DuckDB
- Multi-stage Dockerfile
- Minimal working app

---

## Non-Goals (v1)

- Web UI สำหรับ manage governance
- Automatic PR creation
- Multi-repo management
- Real-time monitoring

---

## Success Metrics

| Metric | Target |
|--------|--------|
| AI reads AI_CONTEXT.md ทุก session | 100% |
| CHANGELOG updated ทุก code PR | >95% |
| Zero hardcoded secrets ในทุก commit | 100% |
| `make check` pass ใน CI | 100% |

---

## Roadmap

### v1 (Current)
- [x] Governance layer
- [x] Agent adapters
- [x] Enforcement script
- [x] Python-Dash-uv pack

### v2
- [ ] FastAPI starter pack
- [ ] GitHub Actions workflow template
- [ ] Pre-commit hook integration
- [ ] More policy rules

### v3
- [ ] Next.js starter pack
- [ ] Multi-repo support
- [ ] Governance dashboard
