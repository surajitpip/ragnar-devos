# Dockerfile — Python Dash uv Pack
# Multi-stage build: builder + runtime-slim
# Stage 1: builder — ติดตั้ง dependencies ด้วย uv
# Stage 2: runtime — copy เฉพาะ venv ที่ต้องการ

# --------- Stage 1: Builder ---------
FROM python:3.12-slim AS builder

# ติดตั้ง uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# ตั้งค่า environment สำหรับ uv
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/app/.venv

WORKDIR /app

# Copy project files สำหรับ dependency resolution
COPY pyproject.toml .
COPY .python-version .
COPY uv.lock .
COPY README.md .

# Install dependencies (ไม่รวม dev dependencies)
RUN uv sync --frozen --no-dev

# --------- Stage 2: Runtime ---------
FROM python:3.12-slim AS runtime

# สร้าง non-root user เพื่อ security
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Copy venv จาก builder stage
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY app/ app/

# ตั้งค่า PATH ให้ใช้ venv
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    APP_HOST=0.0.0.0 \
    APP_PORT=8050 \
    APP_DEBUG=false

# เปลี่ยน ownership
RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 8050

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8050')" || exit 1

# รัน app ด้วย gunicorn ใน production
CMD ["gunicorn", "app.main:server", \
     "--bind", "0.0.0.0:8050", \
     "--workers", "2", \
     "--threads", "4", \
     "--timeout", "60", \
     "--access-logfile", "-", \
     "--error-logfile", "-"]
