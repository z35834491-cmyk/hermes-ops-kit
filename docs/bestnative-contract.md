# BestNative Contract

This document lists the initial file contracts BestNative can consume from Hermes Ops Kit in read-only mode.

## Read-only inputs

| Source | Purpose | Notes |
|---|---|---|
| `config/check-catalog.yaml` | Supported checks and checker names | Used for inspect dispatch and catalog UI |
| `config/schema/env-map.schema.yaml` | Validate environment map shape | Schema contract only |
| `config/schema/inspection-result.schema.yaml` | Validate inspection JSON | Used for history UI |
| `config/schema/runbook.schema.yaml` | Validate runbook metadata | Used for runbook list/detail pages |
| `config/schema/approval.schema.yaml` | Validate approval/audit objects | Used before execution exists |
| `reports/<env>/inspection-*.json` | Inspection run history | Local/private output; do not publish raw reports |
| `templates/runbook-metadata-template.yaml` | Example runbook metadata | Replace with real sanitized metadata later |
| `CHANGELOG.md` + `CHANGELOG.d/` | Project evolution timeline | Project log, not operational log |

## Minimum inspection fields

BestNative should expect:

```json
{
  "schema_version": "0.2",
  "run_id": "20260820T120000Z-test",
  "env": "test",
  "target": "test",
  "mode": "skeleton",
  "status": "ok",
  "summary": {
    "ok": 1,
    "warning": 0,
    "critical": 0,
    "unreachable": 0,
    "failed": 0,
    "skipped": 1
  },
  "checks": []
}
```

## Approval object lifecycle

```text
pending → approved/rejected/expired → executed/cancelled
```

Rules:

- L2/L3 execution requires approval id.
- Command-plan hash binds approval to the exact operation.
- Changing commands invalidates approval.
- Execution result must write operation audit.

## Non-goals for first integration

- No direct kubectl execution.
- No credential storage.
- No automatic discovery promotion.
- No PRD direct execution.
