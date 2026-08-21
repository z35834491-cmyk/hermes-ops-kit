# BestNative 合同 / BestNative contract

BestNative 第一期只**只读消费** Hermes Ops Kit 文件，不执行、不存凭据、不改 kit 源码。
BestNative Phase 1 **reads** Hermes Ops Kit files only. No execution, no credential storage, no mutation of kit sources.

推荐独立仓 + 本地路径 Recommended layout:

```text
HERMES_OPS_KIT_PATH=/path/to/hermes-ops-kit
```

合仓条件见 [../future-product/merge-readiness.md](../future-product/merge-readiness.md)。现在不要物理合并。
Merge conditions: [../future-product/merge-readiness.md](../future-product/merge-readiness.md). Do not merge repositories yet.

## 只读输入 / Read-only inputs

| 路径 Path | 用途 Purpose | 备注 Notes |
|---|---|---|
| `config/check-catalog.yaml` | 检查项与 checker 名 / checks and checker names | 巡检分发与 catalog UI / inspect + catalog UI |
| `config/schema/env-map.schema.yaml` | env-map 形状 / env-map shape | 合同文档，不是 JSON Schema 引擎 / contract doc, not a JSON Schema engine |
| `config/schema/inspection-result.schema.yaml` | 巡检 JSON / inspection JSON | 历史 UI / history UI |
| `config/schema/runbook.schema.yaml` | runbook 元数据 / runbook metadata | 目录页 / catalog page |
| `config/schema/approval.schema.yaml` | 审批/审计对象 / approval and audit | 执行能力出现之前 / before execution exists |
| `examples/runbooks/*.yaml` | 脱敏 L0 runbook 示例 / sanitized L0 examples | 给 catalog UI 用 / for catalog UI |
| `templates/runbook-metadata-template.yaml` | 空模板 / empty template | 新建 runbook 时用 / when adding a runbook |
| `reports/<env>/inspection-*.json` | 巡检历史 / inspection history | **本地私有产物，不要发布** / local-only; do not publish |
| `config/env-map.local.yaml` | 真实环境地图 / real env-map | **本地私有，不在 Git** / local-only, not in Git |
| `CHANGELOG.md` + `CHANGELOG.d/` | 项目演进 / project timeline | 不是运维 oplog / not an ops oplog |

Schema 文件目前是给人看的 YAML 合同，不是可执行 JSON Schema。BestNative 不要把字段定义 fork 一份后自行演化；以本仓库 `schema_version` 为准。
Schema files are human-readable YAML contracts, not an executable JSON Schema engine. BestNative must not fork and diverge field definitions; follow this repo's `schema_version`.

## 巡检 JSON 最低字段 / Minimum inspection fields

BestNative 应按当前 inspect 输出消费（`schema_version`: `0.2`）：

```json
{
  "schema_version": "0.2",
  "run_id": "20260820T120000Z-test",
  "env": "test",
  "target": "test",
  "mode": "plan",
  "started_at": "2026-08-20T12:00:00Z",
  "finished_at": "2026-08-20T12:00:05Z",
  "duration_seconds": 5.0,
  "status": "ok",
  "summary": {
    "ok": 1,
    "warning": 0,
    "critical": 0,
    "unreachable": 0,
    "failed": 0,
    "skipped": 1
  },
  "checks": [
    {
      "id": "k8s_nodes_ready",
      "component": "k8s",
      "env": "test",
      "status": "skipped",
      "severity": "info",
      "title": "K8s nodes readiness",
      "evidence": "plan-only: ...",
      "suggestion": "Run k8s-pod-abnormal-diagnostic",
      "duration_seconds": 0.0
    }
  ]
}
```

`target` 可以是 `all` 或 env-map 里的任意环境名。`checks[].env` 在 `target=all` 时用来区分同名检查。
`target` may be `all` or any env-map environment name. `checks[].env` distinguishes duplicate check ids when `target=all`.

完整示例：[../examples/inspection-result.example.json](../examples/inspection-result.example.json)。
Full example: [../examples/inspection-result.example.json](../examples/inspection-result.example.json).

巡检检查项到 runbook 的关联：目前靠 `suggestion` 里的 runbook `name`（例如 `k8s-pod-abnormal-diagnostic`）以及文件 `examples/runbooks/<name>.yaml`。尚未单独提供 `related_checks` 字段。
Mapping checks to runbooks: today via the runbook `name` in `suggestion` (for example `k8s-pod-abnormal-diagnostic`) and `examples/runbooks/<name>.yaml`. There is not yet a dedicated `related_checks` field.

## 审批对象生命周期 / Approval object lifecycle

```text
pending → approved | rejected | expired → executed | cancelled
```

规则 Rules:

- L2/L3 执行必须带 approval id。
- `commands_hash` 把审批绑到那一组命令；命令变更则审批作废。
- 执行结果必须写 `operation_audit`。

模板：[../templates/approval-request-template.json](../templates/approval-request-template.json)。

## 第一期非目标 / Non-goals for first integration

- 不直接执行 kubectl / no direct kubectl execution
- 不在 BestNative 存凭据值 / no credential storage
- 不自动把 discovery 晋升为正式 env-map / no automatic discovery promotion
- 不对 PRD 直接执行 / no PRD direct execution
