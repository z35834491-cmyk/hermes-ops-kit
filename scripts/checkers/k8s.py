from __future__ import annotations

from .base import CheckResult, plan_result

SUPPORTED = {"k8s_nodes_ready", "pod_abnormal"}


def run(check_id: str, env: str, env_config: dict, catalog_entry: dict, execute: bool = False) -> CheckResult:
    kubeconfig = env_config.get("kubeconfig", "<KUBECONFIG_PATH>")
    title = catalog_entry.get("title", check_id)
    detail = f"would use kubeconfig path {kubeconfig!r}; no Kubernetes API call in public template"
    return plan_result(check_id, "k8s", title, env, detail)
