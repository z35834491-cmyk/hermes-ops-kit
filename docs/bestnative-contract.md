<p align="right">
  <b>简体中文</b> · <a href="bestnative-contract.en.md">English</a>
</p>

# BestNative 合同

BestNative 第一期只**只读消费** Hermes Ops Kit 文件，不执行、不存凭据、不改 kit 源码。

```text
HERMES_OPS_KIT_PATH=/path/to/hermes-ops-kit
```

合仓条件见 [../future-product/merge-readiness.md](../future-product/merge-readiness.md)。现在不要物理合并。

## 只读输入

| 路径 | 用途 | 备注 |
|---|---|---|
| `config/check-catalog.yaml` | 检查项与 checker 名 | 巡检分发与 catalog UI |
| `config/schema/env-map.schema.yaml` | env-map 形状 | 合同文档，不是 JSON Schema 引擎 |
| `config/schema/inspection-result.schema.yaml` | 巡检 JSON | 历史 UI |
| `config/schema/runbook.schema.yaml` | runbook 元数据 | 目录页 |
| `config/schema/lesson-candidate.schema.yaml` | 脱敏教训候选 | `precipitate.py` 草稿 |
| `config/schema/approval.schema.yaml` | 审批/审计对象 | 执行能力出现之前 |
| `examples/runbooks/*.yaml` | 脱敏 L0 runbook 示例 | 给 catalog UI 用 |
| `templates/runbook-metadata-template.yaml` | 空模板 | 新建 runbook 时用 |
| `reports/<env>/inspection-*.json` | 巡检历史 | **本地私有产物，不要发布** |
| `config/env-map.local.yaml` | 真实环境地图 | **本地私有，不在 Git** |
| `CHANGELOG.md` + `CHANGELOG.d/` | 项目演进 | 不是运维 oplog |

Schema 文件目前是给人看的 YAML 合同，不是可执行 JSON Schema。BestNative 不要把字段定义 fork 一份后自行演化；以本仓库 `schema_version` 为准。

## 巡检 JSON 最低字段

BestNative 应按当前 inspect 输出消费（`schema_version`: `0.2`）。完整示例：[../examples/inspection-result.example.json](../examples/inspection-result.example.json)。

`target` 可以是 `all` 或 env-map 里的任意环境名。`checks[].env` 在 `target=all` 时用来区分同名检查。

巡检检查项到 runbook 的关联：目前靠 `suggestion` 里的 runbook `name`（例如 `k8s-pod-abnormal-diagnostic`）以及文件 `examples/runbooks/<name>.yaml`。尚未单独提供 `related_checks` 字段。

## 审批对象生命周期

```text
pending → approved | rejected | expired → executed | cancelled
```

- L2/L3 执行必须带 approval id。
- `commands_hash` 把审批绑到那一组命令；命令变更则审批作废。
- 执行结果必须写 `operation_audit`。

模板：[../templates/approval-request-template.json](../templates/approval-request-template.json)。

## 第一期非目标

- 不直接执行 kubectl
- 不在 BestNative 存凭据值
- 不自动把 discovery 晋升为正式 env-map
- 不自动把 lesson-candidate 晋升为正式 runbook
- 不对 PRD 直接执行
