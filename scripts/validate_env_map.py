#!/usr/bin/env python3
"""Validate a Hermes Ops Kit env-map file without external dependencies.

This is a lightweight structural validator for template usage. It intentionally
checks only the public contract basics and does not read credentials.
"""
from __future__ import annotations

import argparse
import pathlib

from lib.check_catalog import get_check, load_check_catalog
from lib.env_map import extract_environment_names, load_env_map

REQUIRED_TOP_LEVEL = "environments:"
DEFAULT_CATALOG = "config/check-catalog.yaml"


def read_text(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _validate_against_catalog(env_map, catalog, errors: list[str], warnings: list[str]) -> None:
    known = set(catalog.checks.keys())
    for name, env in env_map.environments.items():
        for check_id in env.inspection_include:
            if check_id not in known:
                errors.append(f"{name}.inspection.include unknown check: {check_id}")
                continue
            definition = get_check(catalog, check_id)
            component = definition.component if definition is not None else ""
            if component and component in env.disabled_components:
                warnings.append(
                    f"{name}.inspection.include {check_id} is skipped because component {component} is disabled"
                )
        for check_id in env.inspection_exclude:
            if check_id not in known:
                errors.append(f"{name}.inspection.exclude unknown check: {check_id}")
        for component, reason in env.disabled_components.items():
            if not reason:
                warnings.append(f"{name}.components.{component} is disabled without disabled_reason")


def validate(
    path: pathlib.Path,
    catalog_path: pathlib.Path | None = None,
) -> tuple[bool, list[str], list[str], list[str]]:
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
    env_map = None
    try:
        env_map = load_env_map(str(path))
    except Exception as exc:  # noqa: BLE001
        errors.append(f"env-map parse failed: {type(exc).__name__}: {str(exc)[:120]}")
    if env_map is not None and catalog_path is not None:
        if not catalog_path.exists():
            errors.append(f"catalog not found: {catalog_path}")
        else:
            try:
                catalog = load_check_catalog(str(catalog_path))
                _validate_against_catalog(env_map, catalog, errors, warnings)
            except Exception as exc:  # noqa: BLE001
                errors.append(f"catalog parse failed: {type(exc).__name__}: {str(exc)[:120]}")
    return not errors, errors, warnings, envs


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Validate Hermes Ops Kit env-map structure")
    p.add_argument("config", help="env-map yaml path")
    p.add_argument("--expect-env", help="optional environment name expected in the file")
    p.add_argument(
        "--catalog",
        default=DEFAULT_CATALOG,
        help="check catalog used to verify include/exclude ids",
    )
    p.add_argument(
        "--no-catalog",
        action="store_true",
        help="skip catalog alignment checks",
    )
    args = p.parse_args(argv)

    path = pathlib.Path(args.config)
    catalog_path = None if args.no_catalog else pathlib.Path(args.catalog)
    if catalog_path is not None and args.catalog == DEFAULT_CATALOG and not catalog_path.exists():
        catalog_path = None
    ok, errors, warnings, envs = validate(path, catalog_path=catalog_path)
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
