#!/usr/bin/env python3
"""Render a concise inspection summary from Hermes Ops Kit inspection JSON."""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

STATUS_ICON = {
    "ok": "✅",
    "warning": "⚠️",
    "critical": "🔴",
    "unreachable": "❓",
    "failed": "❌",
    "skipped": "⏭️",
}


def load_json(path: str) -> dict:
    if path == "-":
        return json.load(sys.stdin)
    return json.loads(pathlib.Path(path).read_text(encoding="utf-8"))


def render(data: dict, only_abnormal: bool = False) -> str:
    lines: list[str] = []
    status = data.get("status", "unknown")
    icon = STATUS_ICON.get(status, "•")
    lines.append(f"{icon} inspection {data.get('run_id', '(no-run-id)')} env={data.get('env', '(unknown)')} status={status}")
    summary = data.get("summary") or {}
    if summary:
        parts = [f"{k}={v}" for k, v in summary.items()]
        lines.append("summary: " + " ".join(parts))
    checks = data.get("checks") or []
    for check in checks:
        c_status = check.get("status", "unknown")
        if only_abnormal and c_status in {"ok", "skipped"}:
            continue
        c_icon = STATUS_ICON.get(c_status, "•")
        line = f"{c_icon} {check.get('id', '(no-id)')} [{check.get('component', '-')}] {check.get('title', '')}"
        evidence = check.get("evidence")
        suggestion = check.get("suggestion")
        lines.append(line)
        if evidence:
            lines.append(f"  evidence: {evidence}")
        if suggestion:
            lines.append(f"  suggestion: {suggestion}")
    return "\n".join(lines)


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Render Hermes Ops Kit inspection JSON summary")
    p.add_argument("json_path", help="inspection JSON path, or '-' for stdin")
    p.add_argument("--only-abnormal", action="store_true", help="hide ok/skipped checks")
    args = p.parse_args(argv)
    print(render(load_json(args.json_path), only_abnormal=args.only_abnormal))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
