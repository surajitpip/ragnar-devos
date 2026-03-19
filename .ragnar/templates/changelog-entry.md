# Changelog Entry Template

> คัดลอก block ด้านล่างไปเพิ่มใน docs/CHANGELOG.md
> ใส่ไว้ใต้ version header ที่เกี่ยวข้อง

---

## Template

```markdown
### {YYYY-MM-DD} — {brief description}

**Type**: feat | fix | refactor | chore | docs | perf

**Changed**:
- {สิ่งที่เปลี่ยนแปลง 1}
- {สิ่งที่เปลี่ยนแปลง 2}

**Why**: {เหตุผลที่เปลี่ยน}

**Impact**: {ผลกระทบต่อ system หรือ users}

**Files**: {ไฟล์หลักที่เปลี่ยน}
```

---

## Example

```markdown
### 2026-03-19 — add DuckDB revenue aggregation query

**Type**: feat

**Changed**:
- เพิ่ม query `get_daily_revenue()` ใน `app/data/queries.py`
- เพิ่ม chart component ใน `app/components/revenue_chart.py`

**Why**: ต้องการแสดง daily revenue trend บน dashboard

**Impact**: dashboard หน้าหลักมี chart ใหม่

**Files**: app/data/queries.py, app/components/revenue_chart.py
```
