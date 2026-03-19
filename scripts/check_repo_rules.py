#!/usr/bin/env python3
"""
check_repo_rules.py — Ragnar DevOS Repo Rules Enforcement Script

อ่าน rules จาก .ragnar/checks/repo_rules.yaml
ตรวจสอบ changed files ตาม rules
รายงาน violations

Usage:
    python scripts/check_repo_rules.py --mode working   # manual check
    python scripts/check_repo_rules.py --mode staged    # pre-commit
    python scripts/check_repo_rules.py --mode ci        # CI (vs main branch)

Exit codes:
    0 = ผ่านทุก rules (หรือมีเฉพาะ warnings)
    1 = มี error-level violations
"""

import argparse
import fnmatch
import re
import subprocess
import sys
from pathlib import Path

# --------- ค้นหา repo root ---------


def find_repo_root() -> Path:
    """หา root ของ git repo จาก working directory"""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True,
        )
        return Path(result.stdout.strip())
    except subprocess.CalledProcessError:
        # ถ้าไม่อยู่ใน git repo ให้ใช้ cwd
        return Path.cwd()


# --------- โหลด YAML แบบ minimal (ไม่ใช้ PyYAML) ---------


def load_yaml_simple(path: Path) -> dict:
    """
    โหลด YAML แบบ minimal โดยใช้ stdlib เท่านั้น
    รองรับ structure ของ repo_rules.yaml โดยเฉพาะ
    """
    try:
        import yaml  # type: ignore
        with open(path, encoding="utf-8") as f:
            return yaml.safe_load(f)
    except ImportError:
        pass

    # Fallback: parse YAML แบบ basic (รองรับเฉพาะ structure ที่ใช้จริง)
    return _parse_rules_yaml(path)


def _parse_rules_yaml(path: Path) -> dict:
    """
    Parse repo_rules.yaml แบบ basic โดยไม่ใช้ PyYAML
    รองรับ nested structure ที่ใช้จริงในไฟล์นี้
    """
    text = path.read_text(encoding="utf-8")
    rules = []
    current_rule: dict = {}
    current_section: list[str] = []
    current_list_key = ""

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        stripped = line.lstrip()

        # ข้าม comments และ บรรทัดว่าง
        if stripped.startswith("#") or not stripped:
            continue

        indent = len(line) - len(stripped)

        # top-level key
        if indent == 0:
            if stripped.startswith("- id:"):
                # เริ่ม rule ใหม่
                if current_rule:
                    rules.append(current_rule)
                current_rule = {"id": stripped.split(":", 1)[1].strip()}
                current_section = []
                current_list_key = ""
            elif ":" in stripped and not stripped.startswith("-"):
                # version, etc.
                pass

        # rule-level keys (indent 2)
        elif indent == 2:
            if stripped.startswith("- id:"):
                # new rule in list
                if current_rule:
                    rules.append(current_rule)
                current_rule = {"id": stripped.split(":", 1)[1].strip()}
                current_list_key = ""
            elif ":" in stripped and not stripped.startswith("-"):
                key, _, val = stripped.partition(":")
                val = val.strip()
                if val:
                    current_rule[key.strip()] = val.strip('"').strip("'")
                else:
                    current_section = [key.strip()]

        # section keys (indent 4)
        elif indent == 4:
            if ":" in stripped and not stripped.startswith("-"):
                key, _, val = stripped.partition(":")
                key = key.strip()
                val = val.strip()
                section_key = ".".join(current_section + [key])
                if val:
                    current_rule[section_key] = val
                else:
                    current_list_key = section_key
                    if section_key not in current_rule:
                        current_rule[section_key] = []

        # list items (indent 6 or 8)
        elif indent >= 6 and stripped.startswith("- "):
            item = stripped[2:].strip().strip('"').strip("'")
            if current_list_key and current_list_key in current_rule:
                current_rule[current_list_key].append(item)

    if current_rule:
        rules.append(current_rule)

    return {"rules": rules}


# --------- ดึง changed files ตาม mode ---------


def get_changed_files(mode: str, repo_root: Path) -> list[str]:
    """ดึง list ของ files ที่เปลี่ยนแปลง ตาม mode"""
    try:
        if mode == "staged":
            # เฉพาะ staged files (สำหรับ pre-commit)
            result = subprocess.run(
                ["git", "diff", "--staged", "--name-only"],
                capture_output=True, text=True, check=True, cwd=repo_root,
            )
        elif mode == "ci":
            # เทียบกับ main branch (สำหรับ CI)
            result = subprocess.run(
                ["git", "diff", "origin/main...HEAD", "--name-only"],
                capture_output=True, text=True, cwd=repo_root,
            )
            if result.returncode != 0:
                # fallback: เทียบกับ HEAD~1
                result = subprocess.run(
                    ["git", "diff", "HEAD~1", "--name-only"],
                    capture_output=True, text=True, check=True, cwd=repo_root,
                )
        else:
            # working tree (manual check)
            result = subprocess.run(
                ["git", "diff", "HEAD", "--name-only"],
                capture_output=True, text=True, cwd=repo_root,
            )
            if result.returncode != 0 or not result.stdout.strip():
                # ถ้าไม่มี HEAD (repo ว่าง) หรือไม่มี changes
                result = subprocess.run(
                    ["git", "status", "--porcelain"],
                    capture_output=True, text=True, check=True, cwd=repo_root,
                )
                # แยก filenames จาก porcelain output
                files = []
                for line in result.stdout.splitlines():
                    if line.strip():
                        files.append(line[3:].strip())
                return files

        return [f.strip() for f in result.stdout.splitlines() if f.strip()]

    except subprocess.CalledProcessError as e:
        print(f"[WARN] ไม่สามารถดึง changed files: {e}", file=sys.stderr)
        return []


# --------- ตรวจ content patterns ---------


def files_match_content_pattern(
    changed_files: list[str],
    trigger_files: list[str],
    pattern: str,
    repo_root: Path,
) -> bool:
    """ตรวจสอบว่า files ที่ match trigger มี content ตาม pattern หรือไม่"""
    for changed in changed_files:
        # ตรวจว่า file match trigger patterns ไหม
        matched_trigger = any(
            fnmatch.fnmatch(changed, pat) for pat in trigger_files
        )
        if not matched_trigger:
            continue

        # ตรวจ content
        file_path = repo_root / changed
        if not file_path.exists():
            continue
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            if re.search(pattern, content):
                return True
        except (OSError, PermissionError):
            continue

    return False


# --------- ตรวจ rule ---------


def check_rule(
    rule: dict,
    changed_files: list[str],
    repo_root: Path,
) -> tuple[bool, str]:
    """
    ตรวจสอบ rule หนึ่ง rule
    คืนค่า (passed, message)
    """
    rule_id = rule.get("id", "unknown")
    message = rule.get("message", f"Rule '{rule_id}' violated")

    # ดึง trigger patterns (flat keys: trigger_files, content_pattern)
    raw_trigger = rule.get("trigger_files", [])
    trigger_files: list[str] = raw_trigger if isinstance(raw_trigger, list) else [raw_trigger]

    content_pattern: str = rule.get("content_pattern", "") or ""

    # ดึง require patterns (flat key: require_files)
    raw_require = rule.get("require_files", [])
    require_files: list[str] = raw_require if isinstance(raw_require, list) else [raw_require]

    if not trigger_files:
        return True, ""

    # ตรวจว่า trigger match ไหม
    triggered_files = [
        f for f in changed_files
        if any(fnmatch.fnmatch(f, pat) for pat in trigger_files)
    ]

    if not triggered_files:
        return True, ""

    # ถ้ามี content_pattern ตรวจเพิ่มเติม
    if content_pattern:
        has_pattern = files_match_content_pattern(
            triggered_files, trigger_files, content_pattern, repo_root
        )
        if not has_pattern:
            return True, ""

    # trigger fired — ตรวจ require
    if not require_files:
        return True, ""

    # ตรวจว่า required files ถูก changed หรือมีอยู่
    for req_pattern in require_files:
        matched = any(
            fnmatch.fnmatch(f, req_pattern) for f in changed_files
        )
        # ถ้า pattern มี wildcard และไม่มีใน changed files → check ใน filesystem
        if not matched and "*" in req_pattern:
            matched_paths = list(repo_root.glob(req_pattern))
            # ยังต้องการให้ file ถูก changed ไม่ใช่แค่มีอยู่
            # ดังนั้น ถ้า changed_files ไม่มี → fail
            matched = False

        if not matched:
            return False, message.strip()

    return True, ""


# --------- Main ---------


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Ragnar DevOS — Repo Rules Check"
    )
    parser.add_argument(
        "--mode",
        choices=["staged", "ci", "working"],
        default="working",
        help="Check mode: staged (pre-commit), ci, working (manual)",
    )
    parser.add_argument(
        "--rules",
        default=".ragnar/checks/repo_rules.yaml",
        help="Path to rules file",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="แสดงข้อมูลเพิ่มเติม",
    )
    args = parser.parse_args()

    repo_root = find_repo_root()
    rules_path = repo_root / args.rules

    print(f"🔍 Ragnar DevOS — Repo Rules Check (mode: {args.mode})")
    print(f"   Repo root : {repo_root}")
    print(f"   Rules     : {rules_path}")
    print()

    # โหลด rules
    if not rules_path.exists():
        print(f"[ERROR] ไม่พบ rules file: {rules_path}")
        return 1

    config = load_yaml_simple(rules_path)
    rules = config.get("rules", [])

    if not rules:
        print("[WARN] ไม่พบ rules ใน config file")
        return 0

    # ดึง changed files
    changed_files = get_changed_files(args.mode, repo_root)

    if args.verbose or not changed_files:
        print(f"📁 Changed files ({len(changed_files)}):")
        for f in changed_files:
            print(f"   {f}")
        print()

    if not changed_files:
        print("✅ ไม่มี changed files — ผ่านทุก rules")
        return 0

    # ตรวจสอบ rules
    violations: list[tuple[str, str, str]] = []  # (severity, rule_id, message)
    passed = 0

    for rule in rules:
        rule_id = rule.get("id", "unknown")
        severity = rule.get("severity", "warn")
        ok, msg = check_rule(rule, changed_files, repo_root)

        if ok:
            passed += 1
            if args.verbose:
                print(f"  ✅ {rule_id}")
        else:
            violations.append((severity, rule_id, msg))

    # แสดงผล
    print(f"📊 Results: {passed} passed, {len(violations)} violations")
    print()

    has_errors = False
    for severity, rule_id, msg in violations:
        icon = "❌" if severity == "error" else "⚠️ "
        print(f"{icon} [{severity.upper()}] {rule_id}")
        print(f"   {msg}")
        print()
        if severity == "error":
            has_errors = True

    if not violations:
        print("✅ ผ่านทุก rules!")
        return 0

    if has_errors:
        print("❌ พบ error-level violations — กรุณาแก้ไขก่อน commit")
        return 1
    else:
        print("⚠️  พบ warnings — ควรแก้ไข แต่ไม่ block commit")
        return 0


if __name__ == "__main__":
    sys.exit(main())
