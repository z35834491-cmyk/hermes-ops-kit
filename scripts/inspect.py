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
import time
from datetime import datetime, timezone
from typing import Any

from lib.check_catalog import get_check, load_check_catalog
from lib.env_map import get_environment, load_env_map

TARGETS = ["all", "dev", "test", "prd"]
DEFAULT_CATALOG = "config/check-catalog.yaml"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


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


def with_env(check: dict[str, Any], env: str) -> dict[str, Any]:
    stamped = dict(check)
    stamped["env"] = env
    return stamped


def skipped_check(
    check_id: str,
    env: str,
    component: str,
    title: str,
    evidence: str,
    suggestion: str,
    severity: str = "info",
) -> dict[str, Any]:
    return with_env({
        "id": check_id,
        "component": component,
        "status": "skipped",
        "severity": severity,
        "title": title,
        "evidence": evidence,
        "suggestion": suggestion,
        "duration_seconds": 0.0,
    }, env)


def timed_dispatch(check_id: str, env: str, env_config: dict[str, Any], catalog_entry: dict[str, str], execute: bool) -> dict[str, Any]:
    started = time.monotonic()
    result = dispatch_check(check_id, env, env_config, catalog_entry, execute)
    result["duration_seconds"] = round(time.monotonic() - started, 3)
    return with_env(result, env)


def build_result(target: str, config: str, catalog_path: str, plan: bool, execute_readonly: bool) -> dict[str, Any]:
    started = utc_now()
    started_mono = time.monotonic()
    try:
        env_map = load_env_map(config)
        envs = list(env_map.environments.keys())
    except FileNotFoundError:
        env_map = None
        envs = []
    config_exists = pathlib.Path(config).exists()
    catalog = load_check_catalog(catalog_path) if pathlib.Path(catalog_path).exists() else None
    selected_envs = envs if target == "all" else ([target] if target in envs else [])
    checks: list[dict[str, Any]] = []

    checks.append(with_env({
        "id": "env_map_contract",
        "component": "env-map",
        "status": "ok" if config_exists and selected_envs else "warning",
        "severity": "info" if config_exists and selected_envs else "warning",
        "title": "Environment map contract accepted" if config_exists and selected_envs else ("Environment map file not found" if not config_exists else "Environment not selected"),
        "evidence": f"config={config}; environments={','.join(envs) if envs else '(none)'}; selected={','.join(selected_envs) if selected_envs else '(none)'}",
        "suggestion": "" if selected_envs else "Create env-map.local.yaml or choose an existing environment.",
        "duration_seconds": 0.0,
    }, target))

    if not selected_envs:
        checks.append(with_env({
            "id": "real_checks_not_implemented",
            "component": "template",
            "status": "skipped",
            "severity": "info",
            "title": "No environment selected",
            "evidence": "no checker dispatch was attempted",
            "suggestion": "validate env-map and target name",
            "duration_seconds": 0.0,
        }, target))
    else:
        for env in selected_envs:
            loaded_env = get_environment(env_map, env) if env_map is not None else None
            if loaded_env is not None and loaded_env.has_inspection_include:
                include = list(loaded_env.inspection_include)
            elif catalog is not None:
                include = list(catalog.checks.keys())
            else:
                include = []
            exclude = set(loaded_env.inspection_exclude if loaded_env else [])
            disabled = loaded_env.disabled_components if loaded_env else {}
            env_config = {
                "kubeconfig": loaded_env.kubeconfig if loaded_env else "",
                "inspection_include": include,
            }
            for check_id in include:
                if check_id in exclude:
                    checks.append(skipped_check(
                        check_id,
                        env,
                        "excluded",
                        check_id,
                        f"env={env}; excluded by inspection.exclude",
                        "remove it from exclude to run this check",
                    ))
                    continue
                definition = get_check(catalog, check_id) if catalog is not None else None
                entry = definition.settings if definition is not None else None
                if not entry:
                    checks.append(skipped_check(
                        check_id,
                        env,
                        "unknown",
                        check_id,
                        f"env={env}; check not found in {catalog_path}",
                        "add the check to check-catalog.yaml or remove it from env-map include list",
                        severity="warning",
                    ))
                    continue
                component = entry.get("component", "")
                if component in disabled:
                    reason = disabled[component] or "component mode=disabled"
                    checks.append(skipped_check(
                        check_id,
                        env,
                        component,
                        entry.get("title", check_id),
                        f"env={env}; component {component} is disabled: {reason}",
                        "enable the component in env-map or remove this check from include",
                    ))
                    continue
                checks.append(timed_dispatch(
                    check_id,
                    env,
                    env_config,
                    entry,
                    execute=execute_readonly and not plan,
                ))

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
        "duration_seconds": round(time.monotonic() - started_mono, 3),
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
            f"- env: `{check.get('env', '-')}`",
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
    p.add_argument("--execute-readonly", action="store_true", help="ask checkers to execute; public checkers still skip real infrastructure unless a private overlay injects a runner")
    p.add_argument("--json", action="store_true", help="print inspection JSON to stdout")
    p.add_argument("--save", action="store_true", help="save JSON and Markdown reports")
    p.add_argument("--reports-dir", default="reports", help="output directory for --save")
    return p.parse_args(argv)


def result_exit_code(result: dict[str, Any]) -> int:
    if result.get("status") in {"failed", "critical"}:
        return 1
    for check in result.get("checks") or []:
        if check.get("id") == "env_map_contract" and check.get("status") == "warning":
            return 1
    return 0


def main(argv=None) -> int:
    args = parse_args(argv)
    result = build_result(args.target, args.config, args.catalog, plan=args.plan, execute_readonly=args.execute_readonly)

    if args.save:
        json_path, md_path = save_outputs(result, args.reports_dir)
        print(f"saved_json={json_path}")
        print(f"saved_markdown={md_path}")

    if args.json or not args.save:
        print(json.dumps(result, ensure_ascii=False, indent=2))

    return result_exit_code(result)


if __name__ == "__main__":
    raise SystemExit(main())
