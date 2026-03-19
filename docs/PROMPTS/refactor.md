# Refactor Prompt

> ใช้ prompt นี้เมื่อต้องการให้ AI refactor code
> Copy และแทนที่ `{PLACEHOLDERS}` ก่อนใช้

---

## Prompt Template

```
Task Type: refactor

Scope: {ไฟล์หรือ module ที่จะ refactor}

Goal:
{อธิบายเป้าหมายของ refactor}

Current Problems:
- {ปัญหา 1 ที่อยากแก้}
- {ปัญหา 2}

Constraints:
- ห้ามเปลี่ยน external behavior
- {constraint อื่นๆ}

Context:
- อ่าน docs/AI_CONTEXT.md เพื่อเข้าใจ project
- อ่าน docs/ARCHITECTURE.md เพื่อเข้าใจ design intent
- Files ที่เกี่ยวข้อง: {file paths}

After refactor:
- Update docs/CHANGELOG.md พร้อม refactor entry
- Run: python scripts/check_repo_rules.py --mode working
- ตรวจสอบว่า behavior ไม่เปลี่ยน (รัน tests ถ้ามี)
```

---

## Refactor Types

| Type | When to Use |
|------|------------|
| **Extract Function** | function ยาวเกิน 50 บรรทัด |
| **Extract Module** | file ใหญ่เกิน 300 บรรทัด |
| **Rename** | ชื่อไม่ชัดเจน หรือไม่ตรง convention |
| **Simplify Logic** | nested if/loop ที่ซับซ้อนเกิน |
| **Remove Duplication** | code เหมือนกันมากกว่า 2 ที่ |
| **Add Type Hints** | function ไม่มี type annotations |

---

## Example

```
Task Type: refactor

Scope: app/data/queries.py

Goal:
แยก query functions ออกจาก database connection logic
เพื่อให้ test ง่ายขึ้นและ reuse ได้

Current Problems:
- query functions ทุกอันเปิด/ปิด connection เอง (ซ้ำซ้อน)
- ไม่มี type hints
- function ยาวเกิน 80 บรรทัด

Constraints:
- ห้ามเปลี่ยน function signatures ที่ component อื่นใช้อยู่
- ยังใช้ DuckDB เหมือนเดิม

Context:
- อ่าน docs/AI_CONTEXT.md
- อ่าน docs/ARCHITECTURE.md → Data Flow section
- Files: app/data/queries.py, app/components/ (consumers)
```
