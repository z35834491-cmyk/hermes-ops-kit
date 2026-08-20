from __future__ import annotations

import subprocess
from typing import Callable

from .base import CheckResult, plan_result

SUPPORTED = {"k8s_nodes_ready", "pod_abnormal", "warning_events", "pvc_status"}
Runner = Callable[[str, int], str]


def default_runner(cmd: str, timeout: int = 30) -> str:
    result = subprocess.run(cmd, shell=True, text=True, capture_output=True, timeout=timeout)
    if result.returncode != 0:
        return (result.stdout + result.stderr).strip()
    return result.stdout.strip()


def run(check_id: str, env: str, env_config: dict, catalog_entry: dict, execute: bool = False, runner: Runner | None = None) -> CheckResult:
    kubeconfig = env_config.get("kubeconfig", "<KUBECONFIG_PATH>")
    title = catalog_entry.get("title", check_id)
    if not execute:
        detail = f"would use kubeconfig path {kubeconfig!r}; no Kubernetes API call in public template"
        return plan_result(check_id, "k8s", title, env, detail)
    run_cmd = runner or default_runner
    if check_id == "k8s_nodes_ready":
        return check_nodes_ready(check_id, title, kubeconfig, run_cmd)
    if check_id == "pod_abnormal":
        return check_pod_abnormal(check_id, title, kubeconfig, run_cmd)
    if check_id == "warning_events":
        return check_warning_events(check_id, title, kubeconfig, run_cmd)
    if check_id == "pvc_status":
        return check_pvc_status(check_id, title, kubeconfig, run_cmd)
    return CheckResult(check_id, "k8s", "skipped", "warning", title, f"unsupported k8s check: {check_id}", "add checker implementation")


def check_nodes_ready(check_id: str, title: str, kubeconfig: str, runner: Runner) -> CheckResult:
    cmd = f"kubectl --kubeconfig {kubeconfig} get nodes --no-headers"
    output = runner(cmd, 30)
    lines = [line for line in output.splitlines() if line.strip()]
    if not lines:
        return CheckResult(check_id, "k8s", "failed", "warning", title, "kubectl returned no node rows", "verify kubeconfig and cluster access")
    total = len(lines)
    bad = []
    for line in lines:
        parts = line.split()
        name = parts[0] if parts else "(unknown)"
        status = parts[1] if len(parts) > 1 else "Unknown"
        if status != "Ready":
            bad.append(name)
    ok = total - len(bad)
    if bad:
        return CheckResult(check_id, "k8s", "warning", "warning", title, f"{ok}/{total} Ready; not ready: {', '.join(bad)}", "inspect NotReady nodes before any change")
    return CheckResult(check_id, "k8s", "ok", "info", title, f"{ok}/{total} Ready")


def check_pod_abnormal(check_id: str, title: str, kubeconfig: str, runner: Runner) -> CheckResult:
    cmd = f"kubectl --kubeconfig {kubeconfig} get pods -A --no-headers"
    output = runner(cmd, 30)
    lines = [line for line in output.splitlines() if line.strip()]
    abnormal = []
    for line in lines:
        parts = line.split()
        if len(parts) < 4:
            continue
        namespace, name, ready, status = parts[0], parts[1], parts[2], parts[3]
        if status in {"Completed", "Succeeded"}:
            continue
        ready_parts = ready.split("/", 1)
        not_ready = len(ready_parts) == 2 and ready_parts[0].isdigit() and ready_parts[1].isdigit() and int(ready_parts[0]) < int(ready_parts[1])
        bad_status = status not in {"Running", "Completed", "Succeeded"}
        if not_ready or bad_status:
            abnormal.append(f"{namespace}/{name} {ready} {status}")
    if abnormal:
        sample = "; ".join(abnormal[:5])
        return CheckResult(check_id, "k8s", "warning", "warning", title, f"{len(abnormal)} abnormal pod(s): {sample}", "run pod diagnostic runbook; do not restart/delete automatically")
    return CheckResult(check_id, "k8s", "ok", "info", title, "no abnormal pods detected")


def check_warning_events(check_id: str, title: str, kubeconfig: str, runner: Runner) -> CheckResult:
    cmd = f"kubectl --kubeconfig {kubeconfig} get events -A --field-selector type=Warning --sort-by=.lastTimestamp --no-headers"
    output = runner(cmd, 30)
    warnings = []
    for line in output.splitlines():
        if not line.strip():
            continue
        parts = line.split()
        if len(parts) >= 3 and parts[2] == "Warning":
            warnings.append(line.strip())
    if warnings:
        sample = "; ".join(warnings[-5:])
        return CheckResult(check_id, "k8s", "warning", "warning", title, f"{len(warnings)} warning event(s): {sample}", "inspect warning events before any change")
    return CheckResult(check_id, "k8s", "ok", "info", title, "no warning events detected")


def check_pvc_status(check_id: str, title: str, kubeconfig: str, runner: Runner) -> CheckResult:
    cmd = f"kubectl --kubeconfig {kubeconfig} get pvc -A --no-headers"
    output = runner(cmd, 30)
    bad = []
    for line in output.splitlines():
        if not line.strip():
            continue
        parts = line.split()
        if len(parts) < 3:
            continue
        namespace, name, status = parts[0], parts[1], parts[2]
        if status != "Bound":
            bad.append(f"{namespace}/{name} {status}")
    if bad:
        return CheckResult(check_id, "k8s", "warning", "warning", title, f"{len(bad)} non-Bound PVC(s): {'; '.join(bad[:5])}", "inspect PVC/storage before any change")
    return CheckResult(check_id, "k8s", "ok", "info", title, "all PVCs are Bound")
