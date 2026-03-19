# Ragnar DevOS Makefile
# ใช้ `make help` เพื่อดู commands ทั้งหมด

.DEFAULT_GOAL := help
PYTHON := python3
SCRIPTS_DIR := scripts
CHECK_SCRIPT := $(SCRIPTS_DIR)/check_repo_rules.py

.PHONY: help check check-staged check-ci check-verbose dash-run dash-install docker-build docker-run

## help: แสดง commands ทั้งหมด
help:
	@echo "Ragnar DevOS — Make Commands"
	@echo ""
	@echo "Repo Checks:"
	@echo "  make check          รัน repo rules check (working tree)"
	@echo "  make check-staged   รัน check สำหรับ staged files (pre-commit)"
	@echo "  make check-ci       รัน check สำหรับ CI (vs main branch)"
	@echo "  make check-verbose  รัน check พร้อม verbose output"
	@echo ""
	@echo "Dash App:"
	@echo "  make dash-install   Install Python dependencies ด้วย uv"
	@echo "  make dash-run       รัน Dash development server"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build   Build Docker image"
	@echo "  make docker-run     รัน Docker container"
	@echo ""

## check: รัน repo rules check บน working tree
check:
	@$(PYTHON) $(CHECK_SCRIPT) --mode working

## check-staged: รัน check สำหรับ staged files (ใช้ใน pre-commit hook)
check-staged:
	@$(PYTHON) $(CHECK_SCRIPT) --mode staged

## check-ci: รัน check สำหรับ CI (เทียบกับ main branch)
check-ci:
	@$(PYTHON) $(CHECK_SCRIPT) --mode ci

## check-verbose: รัน check พร้อมแสดง changed files
check-verbose:
	@$(PYTHON) $(CHECK_SCRIPT) --mode working --verbose

## dash-install: Install Python dependencies ด้วย uv
dash-install:
	@echo "Installing dependencies..."
	@cd packs/python-dash-uv && uv sync

## dash-run: รัน Dash development server
dash-run:
	@echo "Starting Dash app..."
	@cd packs/python-dash-uv && uv run python app/main.py

## docker-build: Build Docker image สำหรับ python-dash-uv pack
docker-build:
	@echo "Building Docker image..."
	@docker build -t ragnar-dash:latest packs/python-dash-uv/

## docker-run: รัน Docker container
docker-run:
	@echo "Running Docker container..."
	@docker run -p 8050:8050 --env-file packs/python-dash-uv/.env ragnar-dash:latest 2>/dev/null || \
	 docker run -p 8050:8050 ragnar-dash:latest
