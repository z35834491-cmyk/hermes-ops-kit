#!/usr/bin/env python3
"""Validate an inspection result JSON file semantically."""
from __future__ import annotations

import argparse
import json
import pathlib

VALID_STATUSES = {"ok", "warning", "critical", "unreachable", "failed", "skipped"}


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Validate Hermes Ops Kit inspection result")
    p.add_argument("json_path")
    p.add_argument("--no-failed", action="store_true", help="fail if any check has status=failed")
    args = p.parse_args(argv)

    data = json.loads(pathlib.Path(args.json_path).read_text(encoding="utf-8"))
    errors: list[str] = []
    for field in ["schema_version", "run_id", "env", "status", "summary", "checks"]:
        if field not in data:
            errors.append(f"missing top-level field: {field}")
    checks = data.get("checks") or []
    if not isinstance(checks, list) or not checks:
        errors.append("checks must be a non-empty list")
    for idx, check in enumerate(checks):
        status = check.get("status")
        if status not in VALID_STATUSES:
            errors.append(f"checks[{idx}] invalid status: {status}")
        for field in ["id", "component", "title", "evidence"]:
            if not check.get(field):
                errors.append(f"checks[{idx}] missing field: {field}")
        if args.no_failed and status == "failed":
            errors.append(f"checks[{idx}] failed: {check.get('id')}")
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
