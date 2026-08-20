from __future__ import annotations

from .base import CheckResult, plan_result

SUPPORTED = {"mysql_replica"}


def run(check_id: str, env: str, env_config: dict, catalog_entry: dict, execute: bool = False) -> CheckResult:
    title = catalog_entry.get("title", check_id)
    detail = "would inspect MySQL replica status from credential source; no database connection in public template"
    return plan_result(check_id, "mysql", title, env, detail)
