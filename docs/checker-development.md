# Checker Development

Hermes Ops Kit checkers are small plugins that produce `CheckResult` objects for inspection reports.

## Public vs private behavior

Public repository checkers must remain safe:

- no Kubernetes API calls
- no SSH
- no database connections
- no credential reads
- no write/repair actions

They should return plan/skipped results explaining what a private checker would do.

Parsers may be unit-tested by injecting a fake `runner`. The public `run()` function must not call kubectl, SSH, or databases when no runner is injected.

Private deployments may replace or extend checkers with real read-only implementations.

## Files

```text
scripts/checkers/base.py
scripts/checkers/k8s.py
scripts/checkers/mysql.py
scripts/checkers/redis.py
scripts/checkers/rabbitmq.py
scripts/checkers/elasticsearch.py
```

## Contract

Each checker exposes:

```python
def run(check_id: str, env: str, env_config: dict, catalog_entry: dict, execute: bool = False, runner=None) -> CheckResult:
    ...
```

It returns:

```python
CheckResult(
    id="pod_abnormal",
    component="k8s",
    status="skipped",
    severity="info",
    title="Abnormal pods",
    evidence="plan-only: ...",
    suggestion="Implement private read-only checker",
)
```

## Adding a check

1. Add it to `config/check-catalog.yaml`.
2. Add it to the relevant checker module's `SUPPORTED` set.
3. Ensure it returns `CheckResult`.
4. Add or update a sanitized runbook example if useful.
5. Run `make check`.

## Safety rules

- L0 read-only checks may run without approval.
- Any write, restart, delete, scale, patch, or external write is not a checker; it belongs to approval/execution workflow.
- Public examples should remain generic and sanitized.
