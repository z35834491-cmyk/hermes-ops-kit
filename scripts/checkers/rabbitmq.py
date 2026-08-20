from __future__ import annotations

from .base import CheckResult, plan_result

SUPPORTED = {"rabbitmq_stale_queues"}


def run(check_id: str, env: str, env_config: dict, catalog_entry: dict, execute: bool = False) -> CheckResult:
    title = catalog_entry.get("title", check_id)
    detail = "would list queues and identify stale candidates; no RabbitMQ API call in public template"
    return plan_result(check_id, "rabbitmq", title, env, detail)
