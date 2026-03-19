# Feature Implementation Prompt

> ใช้ prompt นี้เมื่อต้องการให้ AI implement feature ใหม่
> Copy และแทนที่ `{PLACEHOLDERS}` ก่อนใช้

---

## Prompt Template

```
Task Type: feature

Feature: {ชื่อ feature}

Requirements:
- {requirement 1}
- {requirement 2}
- {requirement 3}

Context:
- อ่าน docs/AI_CONTEXT.md เพื่อเข้าใจ project
- อ่าน docs/PRD.md section ที่เกี่ยวข้อง
- Feature นี้ relate กับ: {component/module ที่เกี่ยวข้อง}

Acceptance Criteria:
- [ ] {criteria 1}
- [ ] {criteria 2}

Notes:
- {ข้อมูลเพิ่มเติม หรือ constraints}
- {edge cases ที่ต้องระวัง}

After implementation:
- Update docs/CHANGELOG.md ด้วย entry ใหม่
- Run: python scripts/check_repo_rules.py --mode working
```

---

## Example

```
Task Type: feature

Feature: Revenue Summary Card

Requirements:
- แสดง total revenue ของวันนี้
- เปรียบเทียบกับ yesterday (% change)
- ดึงข้อมูลจาก DuckDB

Context:
- อ่าน docs/AI_CONTEXT.md เพื่อเข้าใจ project
- อ่าน docs/PRD.md section Dashboard Features
- Feature นี้ relate กับ: app/components/, app/data/

Acceptance Criteria:
- [ ] Card แสดง total revenue formatted เป็น THB
- [ ] แสดง % change พร้อม color (green/red)
- [ ] Query ใช้ DuckDB ไม่ใช่ mock data

Notes:
- ใช้ duckdb.connect() pattern ที่มีอยู่แล้วใน codebase
- Handle กรณี no data gracefully

After implementation:
- Update docs/CHANGELOG.md ด้วย entry ใหม่
- Run: python scripts/check_repo_rules.py --mode working
```
