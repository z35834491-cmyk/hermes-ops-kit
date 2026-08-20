#!/usr/bin/env python3
"""Config-driven inspection skeleton for Hermes Ops Kit.

Public/template behavior:
- Does not connect to Kubernetes, SSH, databases, or external services.
- Defines the stable CLI and JSON/Markdown output contract.
- Private users can replace `build_example_result()` with env-map-driven read-only checks.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
from datetime import datetime, timezone

TARGETS = ["all", "dev", "test", "prd"]


def extract_environment_names(config_path: str) -> list[str]:
    path = pathlib.Path(config_path)
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8", errors="replace")
    names: list[str] = []
    in_envs = False
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith("environments:"):
            in_envs = True
            continue
        if in_envs:
            if line and not line.startswith(" ") and not line.startswith("\t"):
                break
            m = re.match(r"^\s{2}([A-Za-z0-9_-]+):\s*$", line)
            if m:
                names.append(m.group(1))
    return names


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def build_example_result(target: str, config: str) -> dict:
    started = utc_now()
    envs = extract_environment_names(config)
    config_exists = pathlib.Path(config).exists()
    checks = [
        {
            "id": "env_map_contract",
            "component": "env-map",
            "status": "ok" if config_exists else "warning",
            "severity": "info" if config_exists else "warning",
            "title": "Environment map contract accepted" if config_exists else "Environment map file not found",
            "evidence": f"config path recorded: {config}; environments={','.join(envs) if envs else '(none)'}",
            "suggestion": "Private implementations should validate schema and credential-source existence without reading secret values." if config_exists else "Create config/env-map.local.yaml from config/env-map.example.yaml.",
            "duration_seconds": 0.0,
        },
        {
            "id": "real_checks_not_implemented",
            "component": "template",
            "status": "skipped",
            "severity": "info",
            "title": "Real infrastructure checks are disabled in the public template",
            "evidence": "No Kubernetes, SSH, database, or external-service connection was attempted.",
            "suggestion": "Wire private read-only checkers to env-map.local.yaml after review.",
            "duration_seconds": 0.0,
        },
    ]
    summary = {"ok": 1 if config_exists else 0, "warning": 0 if config_exists else 1, "critical": 0, "unreachable": 0, "failed": 0, "skipped": 1}
    finished = utc_now()
    return {
        "schema_version": "0.2",
        "run_id": f"{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{target}",
        "env": target,
        "target": target,
        "started_at": started,
        "finished_at": finished,
        "duration_seconds": 0.0,
        "status": "ok",
        "summary": summary,
        "checks": checks,
    }


def to_markdown(result: dict) -> str:
    lines = [
        f"# Inspection Report: {result['env']}",
        "",
        f"- schema_version: `{result.get('schema_version', 'unknown')}`",
        f"- run_id: `{result['run_id']}`",
        f"- status: `{result['status']}`",
        f"- started_at: `{result['started_at']}`",
        f"- finished_at: `{result['finished_at']}`",
        "",
        "## Summary",
        "",
    ]
    for key, value in result["summary"].items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Checks", ""])
    for check in result["checks"]:
        lines.extend([
            f"### {check['id']}",
            "",
            f"- component: `{check['component']}`",
            f"- status: `{check['status']}`",
            f"- severity: `{check['severity']}`",
            f"- evidence: {check['evidence']}",
            f"- suggestion: {check['suggestion']}",
            "",
        ])
    return "\n".join(lines)


def save_outputs(result: dict, reports_dir: str) -> tuple[pathlib.Path, pathlib.Path]:
    root = pathlib.Path(reports_dir) / result["env"]
    root.mkdir(parents=True, exist_ok=True)
    base = root / f"inspection-{result['run_id']}"
    json_path = base.with_suffix(".json")
    md_path = base.with_suffix(".md")
    json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(to_markdown(result), encoding="utf-8")
    return json_path, md_path


def parse_args(argv=None):
    p = argparse.ArgumentParser(description="Hermes Ops Kit inspection contract skeleton")
    p.add_argument("target", nargs="?", default="all", choices=TARGETS, help="inspection target")
    p.add_argument("--config", default="config/env-map.local.yaml", help="env-map yaml path")
    p.add_argument("--json", action="store_true", help="print inspection JSON to stdout")
    p.add_argument("--save", action="store_true", help="save JSON and Markdown reports")
    p.add_argument("--reports-dir", default="reports", help="output directory for --save")
    return p.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    result = build_example_result(args.target, args.config)

    if args.save:
        json_path, md_path = save_outputs(result, args.reports_dir)
        print(f"saved_json={json_path}")
        print(f"saved_markdown={md_path}")

    if args.json or not args.save:
        print(json.dumps(result, ensure_ascii=False, indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
