# 端到端示例 / End-to-end example

不连真实基础设施，只演示 env-map → 巡检 JSON → runbook → 审批合同如何串起来。
This example shows how Hermes Ops Kit pieces fit together without touching real infrastructure.

## Flow

```text
env-map.example.yaml
  ↓
scripts/inspect.py --json --save
  ↓
reports/<env>/inspection-*.json
  ↓
runbook metadata selection
  ↓
approval request if risk >= L1
  ↓
BestNative read-only display / future approval center
```

## 1. Environment map

Start with a local-only file:

```bash
cp config/env-map.example.yaml config/env-map.local.yaml
```

`env-map.local.yaml` describes local paths and credential sources, not credential values.

## 2. Inspection

```bash
python3 scripts/inspect.py test --config config/env-map.local.yaml --json --save
```

The public template generates contract-shaped output only. Private implementations can replace the example builder with real read-only checks.

## 3. Inspection result

Example output shape:

```json
{
  "schema_version": "0.2",
  "run_id": "20260820T120000Z-test",
  "env": "test",
  "mode": "skeleton",
  "status": "warning",
  "summary": {
    "ok": 12,
    "warning": 2,
    "critical": 0,
    "unreachable": 0,
    "failed": 0,
    "skipped": 1
  },
  "checks": [
    {
      "id": "pod_abnormal",
      "component": "k8s",
      "env": "test",
      "status": "warning",
      "severity": "warning",
      "title": "Abnormal pods detected",
      "evidence": "example namespace has 1 pod not ready",
      "suggestion": "Run k8s-pod-abnormal-diagnostic"
    }
  ]
}
```

## 4. Runbook metadata

A UI or agent can map `pod_abnormal` to:

```text
examples/runbooks/k8s-pod-abnormal-diagnostic.yaml
```

The runbook declares:

- risk level
- whether approval is required
- inputs
- prechecks
- execution mode
- verification

## 5. Approval

Read-only runbooks use `risk_level: L0` and do not need approval.

For L1/L2/L3 actions, create an approval object shaped like:

```text
templates/approval-request-template.json
```

BestNative should store approval state and audit results. Hermes Ops Kit only provides the contract.

## 6. Safety boundary

- Discovery output is a candidate, not truth.
- Inspection is read-only until private implementations add safe checkers.
- Execution requires approval/audit before any platform integration.
- Public examples remain sanitized.
