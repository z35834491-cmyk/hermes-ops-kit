#!/usr/bin/env python3
"""Validate a Hermes Ops Kit env-map file without external dependencies.

This is a lightweight structural validator for template usage. It intentionally
checks only the public contract basics and does not read credentials.
"""
from __future__ import annotations

import argparse
import pathlib

from lib.env_map import extract_environment_names, load_env_map

REQUIRED_TOP_LEVEL = "environments:"


def read_text(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def validate(path: pathlib.Path) -> tuple[bool, list[str], list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if not path.exists():
        return False, [f"file not found: {path}"], warnings, []
    text = read_text(path)
    if REQUIRED_TOP_LEVEL not in text:
        errors.append("missing top-level environments block")
    envs = extract_environment_names(text)
    if not envs:
        errors.append("no environments found")
    if "password:" in text or "token:" in text or "api_key:" in text:
        warnings.append("possible secret-like key found; store credential sources, not values")
    try:
        load_env_map(str(path))
    except Exception as exc:  # noqa: BLE001
        errors.append(f"env-map parse failed: {type(exc).__name__}: {str(exc)[:120]}")
    return not errors, errors, warnings, envs


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Validate Hermes Ops Kit env-map structure")
    p.add_argument("config", help="env-map yaml path")
    p.add_argument("--expect-env", help="optional environment name expected in the file")
    args = p.parse_args(argv)

    path = pathlib.Path(args.config)
    ok, errors, warnings, envs = validate(path)
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
