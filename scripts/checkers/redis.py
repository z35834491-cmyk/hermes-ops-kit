from __future__ import annotations

from .base import CheckResult, plan_result

SUPPORTED = {"redis_health"}


def run(check_id: str, env: str, env_config: dict, catalog_entry: dict, execute: bool = False) -> CheckResult:
    title = catalog_entry.get("title", check_id)
    detail = "would inspect Redis health from env-map component definition; no Redis connection in public template"
    return plan_result(check_id, "redis", title, env, detail)
