#!/usr/bin/env python3
"""Validate a Hermes Ops Kit env-map file without external dependencies.

This is a lightweight structural validator for template usage. It intentionally
checks only the public contract basics and does not read credentials.
"""
from __future__ import annotations

import argparse
import pathlib
import re

REQUIRED_TOP_LEVEL = "environments:"


def read_text(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def extract_environment_names(text: str) -> list[str]:
    names: list[str] = []
    in_envs = False
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith("environments:"):
            in_envs = True
            continue
        if in_envs:
            # Top-level non-indented key means environments block ended.
            if line and not line.startswith(" ") and not line.startswith("\t"):
                break
            m = re.match(r"^\s{2}([A-Za-z0-9_-]+):\s*$", line)
            if m:
                names.append(m.group(1))
    return names


def validate(path: pathlib.Path) -> tuple[bool, list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if not path.exists():
        return False, [f"file not found: {path}"], warnings
    text = read_text(path)
    if REQUIRED_TOP_LEVEL not in text:
        errors.append("missing top-level environments block")
    envs = extract_environment_names(text)
    if not envs:
        errors.append("no environments found")
    if "password:" in text or "token:" in text or "api_key:" in text:
        warnings.append("possible secret-like key found; store credential sources, not values")
    return not errors, errors, warnings


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Validate Hermes Ops Kit env-map structure")
    p.add_argument("config", help="env-map yaml path")
    p.add_argument("--expect-env", help="optional environment name expected in the file")
    args = p.parse_args(argv)

    path = pathlib.Path(args.config)
    ok, errors, warnings = validate(path)
    envs = extract_environment_names(read_text(path)) if path.exists() else []
    if args.expect_env and args.expect_env not in envs and args.expect_env != "all":
        ok = False
        errors.append(f"expected env not found: {args.expect_env}")

    print(f"config={path}")
    print(f"environments={','.join(envs) if envs else '(none)'}")
    for w in warnings:
        print(f"warning={w}")
    for e in errors:
        print(f"error={e}")
    print(f"result={'OK' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
