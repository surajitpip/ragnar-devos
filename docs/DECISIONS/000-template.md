# ADR-000: Architecture Decision Record Template

**Date**: 2026-03-19
**Status**: Template (ไม่ใช่ decision จริง)

> ใช้ไฟล์นี้เป็น template สำหรับ ADR ใหม่
> Copy → rename เป็น `NNN-short-title.md` → แทนที่ placeholders

---

## Context

> อธิบาย background และ problem ที่ต้องตัดสินใจ
> ทำไมถึงต้องมี decision นี้?

ตัวอย่าง:
- เราต้องการ database สำหรับเก็บ time-series data
- มี options หลายตัว: PostgreSQL, DuckDB, ClickHouse
- ต้องการ decision ที่ชัดเจนพร้อม rationale

---

## Decision

> ระบุ decision ที่เลือก อย่างชัดเจนและ specific

เราเลือกใช้ **{SOLUTION}** เพราะ:
- {เหตุผล 1}
- {เหตุผล 2}

---

## Consequences

### Positive
- {ข้อดีที่ได้รับ}
- {ผลดีต่อ system}

### Negative / Trade-offs
- {ข้อเสียที่ยอมรับ}
- {technical debt ที่จะเกิด}

### Neutral
- {การเปลี่ยนแปลงที่ไม่ได้ดีหรือแย่}

---

## Alternatives Considered

| Option | Pros | Cons | Why Rejected |
|--------|------|------|-------------|
| {Alt 1} | {ข้อดี} | {ข้อเสีย} | {เหตุผล} |
| {Alt 2} | {ข้อดี} | {ข้อเสีย} | {เหตุผล} |

---

## References
- {Link หรือ document ที่เกี่ยวข้อง}

---

## How to Use This Template

1. Copy ไฟล์นี้: `cp docs/DECISIONS/000-template.md docs/DECISIONS/NNN-title.md`
2. เปลี่ยน number ให้ sequential (001, 002, ...)
3. แทนที่ทุก placeholder ด้วยข้อมูลจริง
4. อัพเดต status: Proposed → Accepted (หลัง review)
5. เพิ่ม link ใน `docs/ARCHITECTURE.md` → Key Decisions section
