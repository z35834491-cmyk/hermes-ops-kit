# Runbook Metadata Template

Use this file to describe a Hermes skill/runbook in a UI-friendly way.

```yaml
name: example-runbook
category: k8s
risk_level: L0
requires_approval: false
requires_backup: false
mode: read-only
related_skills: [k8s-env-map, safe-operations]
inputs:
  - name: env
    required: true
prechecks:
  - Verify env exists in env-map.
execution:
  - Run read-only diagnostic commands.
rollback: Not required for read-only mode.
verification:
  - Confirm result JSON has summary and checks.
outputs: [inspection_result, digest]
```

Rules:

- L0 read-only runbooks do not require approval.
- L1/L2/L3 modifying runbooks require approval and rollback description.
- L3 data/irreversible runbooks require explicit limitation notes and oplog.
- PRD runbooks default to command-generation unless hard RBAC/audit exists.
