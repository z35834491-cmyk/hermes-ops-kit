# Runbook Examples

These are sanitized runbook metadata examples. They are not real production runbooks and do not contain private infrastructure details.

## Current examples

| Runbook | Category | Risk | Mode | Purpose |
|---|---|---|---|---|
| `k8s-pod-abnormal-diagnostic.yaml` | k8s | L0 | read-only | Diagnose abnormal pods without restart/delete |
| `mysql-replication-lag-diagnostic.yaml` | mysql | L0 | read-only | Read replica status and lag without replication changes |
| `rabbitmq-stale-queue-diagnostic.yaml` | rabbitmq | L0 | read-only | Identify stale queue candidates without purge/delete |

## Rules

- Use placeholders and generic names.
- Keep L0 examples strictly read-only.
- L1/L2/L3 examples must include approval and rollback metadata.
- Do not include real IPs, hostnames, queue names, database names, or credential values.

## Future examples

Planned sanitized examples:

- Redis health diagnostic
- Elasticsearch disk/index diagnostic
- Node memory high diagnostic
- Longhorn PVC usage diagnostic
- ArgoCD sync drift diagnostic
