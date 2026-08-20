#!/usr/bin/env python3
"""Config-driven inspection skeleton for Hermes Ops Kit.

Public/template behavior:
- Does not connect to Kubernetes, SSH, databases, or external services.
- Defines the stable CLI and JSON/Markdown output contract.
- Uses env-map + check catalog to dispatch plan-only checker plugins.
- Private users can replace checker plugins with real read-only implementations.
"""
from __future__ import annotations

import argparse
import importlib
import json
import pathlib
import re
from datetime import datetime, timezone
from typing import Any

TARGETS = ["all", "dev", "test", "prd"]
DEFAULT_CATALOG = "config/check-catalog.yaml"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_text(path: str) -> str:
    return pathlib.Path(path).read_text(encoding="utf-8", errors="replace")


def extract_environment_names(config_path: str) -> list[str]:
    path = pathlib.Path(config_path)
    if not path.exists():
        return []
    text = read_text(config_path)
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


def extract_env_block(config_path: str, env: str) -> dict[str, Any]:
    """Tiny parser for the example env-map shape; not a general YAML parser."""
    path = pathlib.Path(config_path)
    if not path.exists():
        return {}
    text = read_text(config_path)
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if re.match(rf"^\s{{2}}{re.escape(env)}:\s*$", line):
            start = i
            break
    if start is None:
        return {}
    block: list[str] = []
    for line in lines[start + 1 :]:
        if re.match(r"^\s{2}[A-Za-z0-9_-]+:\s*$", line):
            break
        block.append(line)
    raw = "\n".join(block)
    kubeconfig = ""
    m = re.search(r"^\s{4}kubeconfig:\s*[\"']?([^\"'\n]+)", raw, re.M)
    if m:
        kubeconfig = m.group(1).strip()
    include: list[str] = []
    in_include = False
    for line in block:
        if re.match(r"^\s{6}include:\s*$", line):
            in_include = True
            continue
        if in_include:
            if re.match(r"^\s{6}[A-Za-z0-9_-]+:", line):
                break
            m = re.match(r"^\s{8}-\s*([A-Za-z0-9_-]+)\s*$", line)
            if m:
                include.append(m.group(1))
    return {"kubeconfig": kubeconfig, "inspection_include": include}


def parse_check_catalog(path: str) -> dict[str, dict[str, str]]:
    catalog_path = pathlib.Path(path)
    if not catalog_path.exists():
        return {}
    checks: dict[str, dict[str, str]] = {}
    current: str | None = None
    in_checks = False
    for line in read_text(path).splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith("checks:"):
            in_checks = True
            continue
        if not in_checks:
            continue
        m = re.match(r"^\s{2}([A-Za-z0-9_-]+):\s*$", line)
        if m:
            current = m.group(1)
            checks[str(current)] = {}
            continue
        if current:
            kv = re.match(r"^\s{4}([A-Za-z0-9_-]+):\s*(.+?)\s*$", line)
            if kv:
                checks[current][kv.group(1)] = kv.group(2).strip().strip('"\'')
    return checks


def dispatch_check(check_id: str, env: str, env_config: dict[str, Any], catalog_entry: dict[str, str], execute: bool) -> dict[str, Any]:
    checker_name = catalog_entry.get("checker", catalog_entry.get("component", ""))
    if not checker_name:
        return {
            "id": check_id,
            "component": "unknown",
            "status": "skipped",
            "severity": "warning",
            "title": check_id,
            "evidence": "no checker configured in catalog",
            "suggestion": "add checker field to check-catalog.yaml",
        }
    try:
        module = importlib.import_module(f"checkers.{checker_name}")
        result = module.run(check_id, env, env_config, catalog_entry, execute=execute)
        return result.to_dict() if hasattr(result, "to_dict") else result
    except Exception as exc:  # noqa: BLE001 - template should report plugin failure, not crash
        return {
            "id": check_id,
            "component": catalog_entry.get("component", checker_name),
            "status": "failed",
            "severity": "warning",
            "title": catalog_entry.get("title", check_id),
            "evidence": f"checker dispatch failed: {type(exc).__name__}: {str(exc)[:160]}",
            "suggestion": "fix checker plugin or catalog entry",
        }


def build_result(target: str, config: str, catalog_path: str, plan: bool, execute_readonly: bool) -> dict[str, Any]:
    started = utc_now()
    envs = extract_environment_names(config)
    config_exists = pathlib.Path(config).exists()
    catalog = parse_check_catalog(catalog_path)
    selected_envs = envs if target == "all" else ([target] if target in envs else [])
    checks: list[dict[str, Any]] = []

    checks.append({
        "id": "env_map_contract",
        "component": "env-map",
        "status": "ok" if config_exists and selected_envs else "warning",
        "severity": "info" if config_exists and selected_envs else "warning",
        "title": "Environment map contract accepted" if config_exists else "Environment map file not found",
        "evidence": f"config={config}; environments={','.join(envs) if envs else '(none)'}; selected={','.join(selected_envs) if selected_envs else '(none)'}",
        "suggestion": "" if selected_envs else "Create env-map.local.yaml or choose an existing environment.",
        "duration_seconds": 0.0,
    })

    if not selected_envs:
        checks.append({
            "id": "real_checks_not_implemented",
            "component": "template",
            "status": "skipped",
            "severity": "info",
            "title": "No environment selected",
            "evidence": "no checker dispatch was attempted",
            "suggestion": "validate env-map and target name",
            "duration_seconds": 0.0,
        })
    else:
        for env in selected_envs:
            env_config = extract_env_block(config, env)
            include = env_config.get("inspection_include") or list(catalog.keys())
            for check_id in include:
                entry = catalog.get(check_id)
                if not entry:
                    checks.append({
                        "id": check_id,
                        "component": "unknown",
                        "status": "skipped",
                        "severity": "warning",
                        "title": check_id,
                        "evidence": f"env={env}; check not found in {catalog_path}",
                        "suggestion": "add the check to check-catalog.yaml or remove it from env-map include list",
                    })
                    continue
                checks.append(dispatch_check(check_id, env, env_config, entry, execute=execute_readonly and not plan))

    summary_keys = ["ok", "warning", "critical", "unreachable", "failed", "skipped"]
    summary = {k: 0 for k in summary_keys}
    for check in checks:
        status = check.get("status", "failed")
        summary[status if status in summary else "failed"] += 1
    status = "critical" if summary["critical"] else "failed" if summary["failed"] else "warning" if summary["warning"] else "ok"
    finished = utc_now()
    return {
        "schema_version": "0.2",
        "run_id": f"{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{target}",
        "env": target,
        "target": target,
        "mode": "plan" if plan else ("execute-readonly" if execute_readonly else "skeleton"),
        "started_at": started,
        "finished_at": finished,
        "duration_seconds": 0.0,
        "status": status,
        "summary": summary,
        "checks": checks,
    }


def to_markdown(result: dict[str, Any]) -> str:
    lines = [
        f"# Inspection Report: {result['env']}",
        "",
        f"- schema_version: `{result.get('schema_version', 'unknown')}`",
        f"- run_id: `{result['run_id']}`",
        f"- mode: `{result.get('mode', 'unknown')}`",
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
            f"- component: `{check.get('component', '-')}`",
            f"- status: `{check.get('status', '-')}`",
            f"- severity: `{check.get('severity', '-')}`",
            f"- evidence: {check.get('evidence', '')}",
            f"- suggestion: {check.get('suggestion', '')}",
            "",
        ])
    return "\n".join(lines)


def save_outputs(result: dict[str, Any], reports_dir: str) -> tuple[pathlib.Path, pathlib.Path]:
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
    p.add_argument("--catalog", default=DEFAULT_CATALOG, help="check catalog yaml path")
    p.add_argument("--plan", action="store_true", help="plan-only mode; do not execute real checks")
    p.add_argument("--execute-readonly", action="store_true", help="reserved for private read-only checkers; public checkers still plan-only")
    p.add_argument("--json", action="store_true", help="print inspection JSON to stdout")
    p.add_argument("--save", action="store_true", help="save JSON and Markdown reports")
    p.add_argument("--reports-dir", default="reports", help="output directory for --save")
    return p.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    result = build_result(args.target, args.config, args.catalog, plan=args.plan, execute_readonly=args.execute_readonly)

    if args.save:
        json_path, md_path = save_outputs(result, args.reports_dir)
        print(f"saved_json={json_path}")
        print(f"saved_markdown={md_path}")

    if args.json or not args.save:
        print(json.dumps(result, ensure_ascii=False, indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
