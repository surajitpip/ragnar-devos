# Debug / Bug Fix Prompt

> ใช้ prompt นี้เมื่อต้องการให้ AI debug หรือ fix bug
> Copy และแทนที่ `{PLACEHOLDERS}` ก่อนใช้

---

## Prompt Template

```
Task Type: bugfix

Bug Description: {อธิบาย bug}

Error / Symptoms:
{error message หรือ behavior ที่ผิดปกติ}
{stack trace ถ้ามี}

Steps to Reproduce:
1. {ขั้นตอน 1}
2. {ขั้นตอน 2}
3. Bug เกิดขึ้น

Expected Behavior:
{อธิบายสิ่งที่ควรเกิดขึ้น}

Actual Behavior:
{อธิบายสิ่งที่เกิดขึ้นจริง}

Context:
- อ่าน docs/AI_CONTEXT.md เพื่อเข้าใจ project
- อ่าน docs/RUNBOOK.md สำหรับ troubleshooting tips
- Files ที่อาจเกี่ยวข้อง: {file paths}

Investigation Notes:
- {สิ่งที่ลองแล้ว}
- {hypothesis}

After fix:
- Update docs/CHANGELOG.md พร้อม fix entry
- Run: python scripts/check_repo_rules.py --mode working
```

---

## Debug Checklist

ก่อน ask AI ให้ debug:
- [ ] Reproduce ได้สม่ำเสมอ
- [ ] มี error message หรือ stack trace
- [ ] รู้ว่า expected vs actual behavior ต่างกันอย่างไร
- [ ] ลอง reproduce ใน environment ที่ clean แล้ว

---

## Example

```
Task Type: bugfix

Bug Description: DuckDB query return empty result แม้มีข้อมูลใน database

Error / Symptoms:
DataFrame empty — ไม่มี error แต่ไม่มีข้อมูล
console log แสดง: "Query returned 0 rows"

Steps to Reproduce:
1. รัน app ด้วย APP_ENV=development
2. เปิดหน้า Dashboard
3. Revenue chart แสดง "No data available"

Expected Behavior:
Chart แสดง revenue data สำหรับ 30 วันล่าสุด

Actual Behavior:
Chart ว่างเปล่า ไม่มีข้อมูล

Context:
- อ่าน docs/AI_CONTEXT.md เพื่อเข้าใจ project
- Files ที่เกี่ยวข้อง: app/data/queries.py, app/components/revenue_chart.py

Investigation Notes:
- DUCKDB_PATH ใน .env ชี้ถูก path
- Database file มีขนาด > 0 bytes (มีข้อมูล)
- ยังไม่ได้ trace query จริงๆ
```
