#!/usr/bin/env python3
"""Hermes Ops Kit onboarding skeleton.

Public/template behavior:
- Does not connect to Kubernetes, SSH, databases, or external services.
- Generates an env-map.generated.yaml candidate skeleton only.
- Generated output must be reviewed by a human before promotion to env-map.local.yaml.
"""
from __future__ import annotations

import argparse
import pathlib
from datetime import datetime, timezone


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def build_generated_env_map(env: str, source_config: str) -> str:
    return f"""# Generated env-map candidate
# Generated at: {utc_now()}
# Source config: {source_config}
# Review required: true
#
# This public skeleton does not perform real discovery. Replace placeholders
# after running private read-only discovery in your own environment.

version: "0.2"

environments:
  {env}:
    type: k8s
    kubeconfig: "<KUBECONFIG_PATH>"
    description: "Generated candidate for <ENV_DESCRIPTION>"
    discovery:
      enabled: true
      confirm_before_write: true
      generated_by: "scripts/onboard.py"
    credentials:
      example_component:
        type: file
        path: "<CREDENTIAL_FILE_PATH>"
        note: "Path only; do not store credential values."
    components:
      kubernetes:
        mode: auto
      mysql:
        mode: manual
        endpoints:
          - "<MYSQL_PRIMARY_ALIAS>"
      redis:
        mode: manual
        endpoints:
          - "<REDIS_ALIAS>"
    inspection:
      mode: manual
      include:
        - k8s_nodes_ready
        - pod_abnormal
        - pvc_status
      exclude: []
    risk:
      default_level: L0
      prd_direct_access: false
"""


def parse_args(argv=None):
    p = argparse.ArgumentParser(description="Generate env-map.generated.yaml candidate skeleton")
    p.add_argument("--config", default="config/env-map.local.yaml", help="source env-map path; path is recorded only")
    p.add_argument("--env", default="example", help="environment name to generate")
    p.add_argument("--output", default="config/env-map.generated.yaml", help="candidate output path")
    p.add_argument("--force", action="store_true", help="overwrite output if it exists")
    return p.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    out = pathlib.Path(args.output)
    if out.exists() and not args.force:
        raise SystemExit(f"Refusing to overwrite existing {out}. Re-run with --force after review.")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build_generated_env_map(args.env, args.config), encoding="utf-8")
    print(f"generated={out}")
    print("review_required=true")
    print("note=generated output is a candidate; do not auto-promote")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
