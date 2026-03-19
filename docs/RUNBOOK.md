# Operations Runbook

**Project**: Ragnar DevOS
**Last Updated**: 2026-03-19

> อัพเดตไฟล์นี้ทุกครั้งที่เปลี่ยน Dockerfile, docker-compose, หรือ deployment procedures
> ใช้ template: `.ragnar/templates/runbook-update.md`

---

## Prerequisites

| Tool | Version | Install |
|------|---------|---------|
| Python | 3.12+ | [python.org](https://python.org) |
| uv | latest | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| Docker | 24+ | [docker.com](https://docker.com) |
| Git | 2.40+ | system package manager |

---

## Local Development

### Setup
```bash
# Clone repo
git clone <repo-url>
cd ragnar-devos

# Copy env file
cp .env.example .env
# แก้ไข .env ตามต้องการ

# Setup Dash app
cd packs/python-dash-uv
uv sync
```

### Run App
```bash
cd packs/python-dash-uv

# Development mode
uv run python app/main.py

# หรือด้วย environment file
APP_ENV=development uv run python app/main.py
```

App จะรันที่ `http://localhost:8050`

---

## Docker

### Build Image
```bash
cd packs/python-dash-uv

# Build
docker build -t ragnar-app:latest .

# Build with tag
docker build -t ragnar-app:1.0.0 .
```

### Run Container
```bash
# Development
docker run -p 8050:8050 --env-file .env ragnar-app:latest

# Production
docker run -d \
  -p 8050:8050 \
  --env-file .env \
  --name ragnar-app \
  ragnar-app:latest
```

### Container Management
```bash
# ดู logs
docker logs ragnar-app

# หยุด container
docker stop ragnar-app

# ลบ container
docker rm ragnar-app

# ดู running containers
docker ps
```

---

## CI/CD

### Run Checks
```bash
# Pre-commit check (staged files)
make check-staged

# CI check (all changes vs main)
make check-ci

# Manual check (working tree)
make check
```

### Check Script Options
```bash
python scripts/check_repo_rules.py --help
python scripts/check_repo_rules.py --mode staged
python scripts/check_repo_rules.py --mode ci
python scripts/check_repo_rules.py --mode working
```

---

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `APP_ENV` | No | `development` | Environment name |
| `APP_HOST` | No | `0.0.0.0` | Server host |
| `APP_PORT` | No | `8050` | Server port |
| `APP_DEBUG` | No | `true` | Enable debug mode |
| `DUCKDB_PATH` | No | `./data/app.duckdb` | DuckDB file path |
| `LOG_LEVEL` | No | `INFO` | Log level |

---

## Troubleshooting

### App ไม่ start
1. ตรวจสอบ Python version: `python --version` (ต้อง 3.12+)
2. ตรวจสอบ dependencies: `cd packs/python-dash-uv && uv sync`
3. ดู error logs: `uv run python app/main.py` และดู stderr

### Docker build fail
1. ตรวจสอบ Docker daemon รันอยู่: `docker info`
2. ตรวจสอบ Dockerfile syntax
3. Build แบบ verbose: `docker build --progress=plain -t ragnar-app .`

### check_repo_rules.py fail
1. ดู output ว่า rule ไหน fail
2. ตรวจสอบว่า required file ถูก stage แล้ว
3. รัน `git diff --staged --name-only` เพื่อดู staged files

---

## Deployment Checklist

ก่อน deploy production:
- [ ] `APP_ENV=production` ตั้งค่าแล้ว
- [ ] `APP_DEBUG=false`
- [ ] Secrets ทั้งหมดมาจาก env vars (ไม่ใช่ hardcoded)
- [ ] Docker image build ผ่าน
- [ ] `make check-ci` ผ่าน
- [ ] CHANGELOG.md updated
