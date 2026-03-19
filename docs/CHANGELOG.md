# Changelog

รูปแบบ: [Semantic Versioning](https://semver.org/)
Template สำหรับ entry ใหม่: `.ragnar/templates/changelog-entry.md`

---

## [Unreleased]

---

## [1.0.0] — 2026-03-19

### Added
- Governance layer (`.ragnar/`) — config, routing, policies, templates, agents, checks
- Agent bootstrap files — `CLAUDE.md`, `AGENTS.md`
- Shared behavioral contract — `.ragnar/agents/common.md`
- Claude Code adapter — `.ragnar/agents/claude_adapter.md`
- Codex adapter — `.ragnar/agents/codex_adapter.md`
- Project documentation — `docs/AI_CONTEXT.md`, `PRD.md`, `ARCHITECTURE.md`, `RUNBOOK.md`
- ADR template — `docs/DECISIONS/000-template.md`
- Structured prompts — `docs/PROMPTS/feature.md`, `debug.md`, `refactor.md`
- Enforcement script — `scripts/check_repo_rules.py`
- Pull request template — `.github/pull_request_template.md`
- Makefile with check commands
- Python-Dash-uv starter pack — `packs/python-dash-uv/`

### Notes
- Initial release ของ Ragnar DevOS v1 Starter Kit
- ออกแบบให้ใช้เป็น template repo สำหรับ project ใหม่
