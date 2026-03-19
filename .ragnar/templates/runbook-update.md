# Runbook Update Template

> ใช้ template นี้เมื่อต้อง update docs/RUNBOOK.md
> หลังจาก change Dockerfile, docker-compose, หรือ deployment config

---

## Template

```markdown
## {Section Title} — updated {YYYY-MM-DD}

### Changes
{อธิบาย changes ที่เกิดขึ้น}

### New Steps / Updated Steps

1. {ขั้นตอนที่ 1}
2. {ขั้นตอนที่ 2}

### Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `{VAR}` | Yes/No | `{default}` | {คำอธิบาย} |

### Rollback
{วิธี rollback ถ้า deployment มีปัญหา}
```

---

## Example

```markdown
## Docker Build — updated 2026-03-19

### Changes
เปลี่ยน base image จาก python:3.11 เป็น python:3.12-slim
และเพิ่ม uv สำหรับ package management

### New Steps / Updated Steps

1. Build image: `docker build -t app:latest .`
2. รัน container: `docker run -p 8050:8050 --env-file .env app:latest`

### Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `APP_PORT` | No | `8050` | Port ที่ expose |

### Rollback
`docker run -p 8050:8050 app:previous`
```
