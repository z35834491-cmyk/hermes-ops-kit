# Schema 索引 / Schema index

Hermes Ops Kit 的 schema 是合同，供本仓库脚本和未来 BestNative 适配器消费，不是真实环境状态。
Hermes Ops Kit schemas are contracts for this repo's scripts and future BestNative adapters. They are not real environment state.

## 列表 / Schemas

| Schema | 用途 Purpose | 消费者 Consumer |
|---|---|---|
| `config/check-catalog.yaml` | 检查项、风险级、checker 模块 / checks, risk, checker modules | inspect 分发、未来 catalog UI / inspect dispatcher, catalog UI |
| `config/schema/env-map.schema.yaml` | 环境、凭据来源、组件、巡检目标 / environments, credential sources, components | onboard、inspect、资产视图 / onboard, inspect, asset view |
| `config/schema/inspection-result.schema.yaml` | 巡检 JSON 输出 / inspection JSON | 历史 UI、报告 / history UI, reporting |
| `config/schema/runbook.schema.yaml` | runbook 元数据 / runbook metadata | `validate_runbook.py`、目录、Agent 选择 / runbook validator, catalog, agent selection |
| `config/schema/approval.schema.yaml` | 审批请求与操作审计对象 / approval and audit objects | 审批/审计中心设计 / approval and audit design |

## 原则 / Principles

- schema 是可复用合同，不是环境事实 / schemas are reusable contracts, not environment facts
- `config/schema/*.yaml` 目前是给人看的合同，不是 JSON Schema 校验引擎 / schema files are human-readable contracts, not a JSON Schema engine
- 私有值只留在 `env-map.local.yaml`，不提交 / private values stay in `env-map.local.yaml` and are not committed
- 发现输出只是候选，人工确认后才能晋升 / discovery output is a candidate until reviewed
- BestNative 应通过适配器消费这些合同，不要另起一套 / BestNative should consume these contracts, not redefine them

## 版本 / Versioning

当前 schema 版本 Current schema version: `0.2`。

破坏性变更需要同时更新 Breaking changes should also update:

- schema 文件 / the schema file
- templates
- examples
- `docs/bestnative-contract.md`
- `CHANGELOG.md` 与 `CHANGELOG.d/`
