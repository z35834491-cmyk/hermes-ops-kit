#!/usr/bin/env python3
"""Validate an inspection result JSON file semantically."""
from __future__ import annotations

import argparse
import json
import pathlib
from collections import Counter

VALID_STATUSES = {"ok", "warning", "critical", "unreachable", "failed", "skipped"}


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Validate Hermes Ops Kit inspection result")
    p.add_argument("json_path")
    p.add_argument("--no-failed", action="store_true", help="fail if any check has status=failed")
    p.add_argument("--no-missing-catalog", action="store_true", help="fail if a check was skipped because it is not in the catalog")
    args = p.parse_args(argv)

    data = json.loads(pathlib.Path(args.json_path).read_text(encoding="utf-8"))
    errors: list[str] = []
    for field in ["schema_version", "run_id", "env", "mode", "status", "summary", "checks", "duration_seconds"]:
        if field not in data:
            errors.append(f"missing top-level field: {field}")
    summary = data.get("summary") or {}
    if not isinstance(summary, dict):
        errors.append("summary must be an object")
    else:
        for key in ["ok", "warning", "critical", "unreachable", "failed", "skipped"]:
            if key not in summary:
                errors.append(f"summary missing field: {key}")
    checks = data.get("checks") or []
    if not isinstance(checks, list) or not checks:
        errors.append("checks must be a non-empty list")
    for idx, check in enumerate(checks):
        status = check.get("status")
        if status not in VALID_STATUSES:
            errors.append(f"checks[{idx}] invalid status: {status}")
        for field in ["id", "component", "title", "evidence", "env"]:
            if not check.get(field):
                errors.append(f"checks[{idx}] missing field: {field}")
        if "duration_seconds" not in check:
            errors.append(f"checks[{idx}] missing field: duration_seconds")
        if args.no_failed and status == "failed":
            errors.append(f"checks[{idx}] failed: {check.get('id')}")
        if args.no_missing_catalog and "check not found" in str(check.get("evidence", "")):
            errors.append(f"checks[{idx}] missing from catalog: {check.get('id')}")
    ids = [c.get("id") for c in checks if isinstance(c, dict)]
    counted = Counter(ids)
    for idx, check in enumerate(checks):
        if not isinstance(check, dict):
            continue
        check_id = check.get("id")
        if counted.get(check_id, 0) > 1 and not check.get("env"):
            errors.append(f"checks[{idx}] duplicate id {check_id} needs env")
    if errors:
        print("result=FAIL")
        for e in errors:
            print(f"error={e}")
        return 1
    print("result=OK")
    print(f"checks={len(checks)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
