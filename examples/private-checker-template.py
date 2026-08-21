#!/usr/bin/env python3
"""Private checker template.

Copy this file outside the public repository before adding real environment details.
Do not commit private implementations that contain real topology or credential paths.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

# In private code, import from the public repo path or package your overlay cleanly.
from scripts.checkers.base import CheckResult


def run_readonly_command(argv: list[str], timeout: int = 30) -> str:
    """Run a read-only command and return sanitized stdout.

    This template intentionally does not include real cluster details.
    Pass argument lists, never shell=True.
    """
    result = subprocess.run(argv, shell=False, text=True, capture_output=True, timeout=timeout)
    return result.stdout.strip() if result.returncode == 0 else (result.stdout + result.stderr).strip()


def check_k8s_nodes_ready(kubeconfig: str, runner=run_readonly_command) -> CheckResult:
    """Example private K8s checker. Replace placeholders in your private overlay only."""
    if not kubeconfig or not Path(kubeconfig).expanduser().exists():
        return CheckResult(
            id="k8s_nodes_ready",
            component="k8s",
            status="failed",
            severity="warning",
            title="K8s nodes readiness",
            evidence="kubeconfig path missing or not configured",
            suggestion="set kubeconfig path in private env-map.local.yaml",
        )

    output = runner(["kubectl", "--kubeconfig", kubeconfig, "get", "nodes", "--no-headers"], 30)
    # Parse output in your private implementation or reuse the public k8s checker parser.
    return CheckResult(
        id="k8s_nodes_ready",
        component="k8s",
        status="skipped",
        severity="info",
        title="K8s nodes readiness",
        evidence="template placeholder: parse kubectl output here",
        suggestion="keep this private unless fully sanitized",
    )
