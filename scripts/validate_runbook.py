#!/usr/bin/env python3
"""Validate Hermes Ops Kit runbook metadata without external dependencies."""
from __future__ import annotations

import argparse
import pathlib
import re

REQUIRED = ["name", "category", "risk_level", "requires_approval", "inputs", "verification"]
CATEGORIES = {"k8s", "mysql", "redis", "rabbitmq", "es", "longhorn", "network", "cicd", "prd"}
MODES = {"read-only", "change", "mixed", "command-generation"}
RISKS = {"L0", "L1", "L2", "L3"}


def parse_runbook(text: str) -> dict:
    result: dict = {}
    current_list: str | None = None
    current_item: dict | None = None
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        top = re.match(r"^([A-Za-z0-9_]+):\s*(.*)$", line)
        if top and not line.startswith(" "):
            key = top.group(1)
            value = top.group(2).strip()
            current_item = None
            if value == "":
                result[key] = []
                current_list = key
            elif value.startswith("[") and value.endswith("]"):
                inner = value[1:-1].strip()
                result[key] = [part.strip().strip("\"'") for part in inner.split(",") if part.strip()] if inner else []
                current_list = None
            else:
                result[key] = value.strip("\"'")
                current_list = None
            continue
        if current_list is None:
            continue
        item = re.match(r"^\s+-\s+(.*)$", line)
        if item:
            payload = item.group(1).strip()
            nested = re.match(r"^([A-Za-z0-9_]+):\s*(.*)$", payload)
            if nested:
                current_item = {nested.group(1): nested.group(2).strip().strip("\"'")}
                result[current_list].append(current_item)
            else:
                current_item = None
                result[current_list].append(payload.strip("\"'"))
            continue
        field = re.match(r"^\s{4}([A-Za-z0-9_]+):\s*(.*)$", line)
        if field and current_item is not None:
            current_item[field.group(1)] = field.group(2).strip().strip("\"'")
    return result


def _as_bool(value: str) -> bool | None:
    lowered = str(value).strip().lower()
    if lowered in {"true", "yes"}:
        return True
    if lowered in {"false", "no"}:
        return False
    return None


def validate_runbook(path: pathlib.Path, data: dict) -> list[str]:
    errors: list[str] = []
    for field in REQUIRED:
        if field not in data or data[field] in ("", None, []):
            errors.append(f"missing required field: {field}")
    name = str(data.get("name", ""))
    if name and not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        errors.append(f"name must be lowercase-with-hyphens: {name}")
    if path.parent.name == "runbooks" and name and path.stem != name:
        errors.append(f"filename stem {path.stem} does not match name {name}")
    category = data.get("category")
    if category and category not in CATEGORIES:
        errors.append(f"invalid category: {category}")
    risk = data.get("risk_level")
    if risk and risk not in RISKS:
        errors.append(f"invalid risk_level: {risk}")
    mode = data.get("mode")
    if mode and mode not in MODES:
        errors.append(f"invalid mode: {mode}")
    approval = _as_bool(str(data.get("requires_approval", "")))
    if data.get("requires_approval") not in (None, "") and approval is None:
        errors.append("requires_approval must be true or false")
    if risk == "L0":
        if mode and mode != "read-only":
            errors.append("L0 runbooks must use mode: read-only")
        if approval is True:
            errors.append("L0 runbooks must set requires_approval: false")
    if risk in {"L2", "L3"} and approval is False:
        errors.append(f"{risk} runbooks must set requires_approval: true")
    if risk in {"L1", "L2", "L3"} and not str(data.get("rollback", "")).strip():
        errors.append(f"{risk} runbooks must define rollback")
    inputs = data.get("inputs")
    if isinstance(inputs, list):
        if not inputs:
            errors.append("inputs must contain at least one item")
        for idx, item in enumerate(inputs):
            if not isinstance(item, dict) or not item.get("name"):
                errors.append(f"inputs[{idx}] must be a map with name")
    verification = data.get("verification")
    if isinstance(verification, list) and not verification:
        errors.append("verification must contain at least one item")
    return errors


def collect_paths(targets: list[str]) -> list[pathlib.Path]:
    paths: list[pathlib.Path] = []
    for target in targets:
        path = pathlib.Path(target)
        if path.is_dir():
            paths.extend(sorted(path.glob("*.yaml")))
        else:
            paths.append(path)
    return paths


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Validate Hermes Ops Kit runbook metadata")
    p.add_argument("paths", nargs="+", help="runbook yaml files or directories")
    args = p.parse_args(argv)

    exit_code = 0
    checked = 0
    for path in collect_paths(args.paths):
        if not path.exists():
            print(f"result=FAIL path={path} error=file not found")
            exit_code = 1
            continue
        data = parse_runbook(path.read_text(encoding="utf-8"))
        errors = validate_runbook(path, data)
        checked += 1
        if errors:
            exit_code = 1
            print(f"result=FAIL path={path}")
            for error in errors:
                print(f"error={error}")
        else:
            print(f"result=OK path={path} name={data.get('name')}")
    print(f"checked={checked}")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
