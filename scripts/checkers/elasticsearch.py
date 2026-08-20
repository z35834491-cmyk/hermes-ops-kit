from __future__ import annotations

from .base import CheckResult, plan_result

SUPPORTED = {"elasticsearch_health"}


def run(check_id: str, env: str, env_config: dict, catalog_entry: dict, execute: bool = False) -> CheckResult:
    title = catalog_entry.get("title", check_id)
    detail = "would inspect Elasticsearch cluster health/disk; no ES HTTP request in public template"
    return plan_result(check_id, "elasticsearch", title, env, detail)
