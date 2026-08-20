#!/usr/bin/env python3
"""Hermes Ops Kit local health-check template (read-only).

This script is safe for template/public usage:
- It checks local Hermes metadata and repository structure.
- It does not read .env, private keys, kubeconfig contents, or credential values.
- It treats a literal pruned placeholder as a problem, but ignores documentation that merely mentions [SKILL_PRUNED].
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path


def run(cmd: list[str], cwd: Path | None = None, timeout: int = 30) -> tuple[int, str]:
    try:
        r = subprocess.run(cmd, cwd=str(cwd) if cwd else None, text=True, capture_output=True, timeout=timeout)
        return r.returncode, (r.stdout + r.stderr).strip()
    except FileNotFoundError:
        return 127, f"command not found: {cmd[0]}"
    except subprocess.TimeoutExpired:
        return 124, "timeout"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def scan_skills(skills_root: Path) -> dict:
    items = []
    if not skills_root.exists():
        return {"total": 0, "missing_root": True, "duplicates": {}, "root_skills": [], "missing_meta": [], "small": [], "truly_pruned": []}

    for p in skills_root.rglob("SKILL.md"):
        rel = p.relative_to(skills_root)
        text = read_text(p)
        name = None
        desc = None
        if text.startswith("---"):
            m = re.search(r"\n---\s*\n", text[3:])
            if m:
                fm = text[3 : m.start() + 3]
                for line in fm.splitlines():
                    if line.startswith("name:"):
                        name = line.split(":", 1)[1].strip().strip('"')
                    elif line.startswith("description:"):
                        desc = line.split(":", 1)[1].strip().strip('"')
        stripped = text.strip()
        truly_pruned = stripped == "[SKILL_PRUNED]" or (stripped.startswith("[SKILL_PRUNED]") and len(stripped) < 200)
        items.append({"path": str(rel), "name": name, "description": desc, "size": len(text), "root_skill": len(rel.parts) == 2, "small": len(text) < 400, "missing_meta": not name or not desc, "truly_pruned": truly_pruned})

    by_name = defaultdict(list)
    for item in items:
        if item["name"]:
            by_name[item["name"]].append(item["path"])
    return {
        "total": len(items),
        "missing_root": False,
        "duplicates": {k: v for k, v in by_name.items() if len(v) > 1},
        "root_skills": [i for i in items if i["root_skill"]],
        "missing_meta": [i for i in items if i["missing_meta"]],
        "small": [i for i in items if i["small"]],
        "truly_pruned": [i for i in items if i["truly_pruned"]],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only local Hermes health-check template")
    parser.add_argument("--hermes-home", default=os.environ.get("HERMES_HOME", str(Path.home() / ".hermes")))
    parser.add_argument("--ops-kit", default=str(Path.cwd()), help="Hermes Ops Kit repo path")
    args = parser.parse_args()

    hermes_home = Path(args.hermes_home).expanduser()
    ops_kit = Path(args.ops_kit).expanduser()
    skills_root = hermes_home / "skills"

    print("Hermes Ops Kit Health Check")
    print("===========================")

    rc, out = run(["hermes", "--version"], timeout=20)
    print(f"hermes_version: {'OK' if rc == 0 else 'WARN'}")
    if out:
        print("  " + out.splitlines()[0])

    rc, _ = run(["hermes", "config", "check"], timeout=40)
    print(f"config_check: {'OK' if rc == 0 else 'WARN'}")

    inv = scan_skills(skills_root)
    print(f"skills_total: {inv['total']}")
    print(f"duplicate_skill_names: {len(inv['duplicates'])}")
    print(f"root_skills: {len(inv['root_skills'])}")
    print(f"missing_frontmatter_or_description: {len(inv['missing_meta'])}")
    print(f"small_skills_lt400b: {len(inv['small'])}")
    print(f"true_pruned_skills: {len(inv['truly_pruned'])}")

    rc, status = run(["git", "status", "--short"], cwd=ops_kit, timeout=20)
    changed = len([line for line in status.splitlines() if line.strip()]) if rc == 0 else -1
    print(f"ops_kit_git_status: {'OK' if rc == 0 else 'WARN'} changed_entries={changed}")

    scan = ops_kit / "scripts" / "sanitize_check.py"
    if scan.exists():
        rc, _ = run([sys.executable, str(scan), str(ops_kit)], cwd=ops_kit, timeout=40)
        print(f"ops_kit_sanitize: {'OK' if rc == 0 else 'FAIL'}")
    else:
        print("ops_kit_sanitize: WARN missing scripts/sanitize_check.py")

    hard_fail = bool(inv["duplicates"] or inv["root_skills"] or inv["missing_meta"] or inv["small"] or inv["truly_pruned"])
    print("result:", "FAIL" if hard_fail else "OK")
    return 1 if hard_fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
