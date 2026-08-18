# Hermes Ops Kit

Hermes Ops Kit 是一套基于 Hermes Agent 的个人/团队运维模板，用于把巡检、审批、oplog、skill、手机远程入口和故障复盘沉淀成可复用体系。

当前定位：本地私有 v0.1 模板。

## 目标

- 快速接入 dev/test/prd 运维环境
- 自动发现 K8s 资产并生成 env-map 草稿
- 手动触发全面巡检
- 高风险操作前强制审批和 oplog
- 故障处理后沉淀 skill / 运维日志
- 支持手机端 ChatOps
- 后续逐步演进成运维平台

## 非目标

- 不自动执行高风险修复
- 不绕过审批
- 不保存密码/token/API key
- 不直接替代 Prometheus / Alertmanager
- v0.1 不做 Web UI

## 快速开始（规划）

```bash
cp config/env-map.example.yaml config/env-map.local.yaml
vim config/env-map.local.yaml
python3 scripts/onboard.py --config config/env-map.local.yaml
python3 scripts/inspect.py --config config/env-map.local.yaml all
```

## 结构

```text
config/       环境地图和模型路由示例
docs/         架构、接入、手机端、安全、维护文档
scripts/      巡检/发现/脱敏检查脚本骨架
templates/    oplog、故障报告、变更审批模板
examples/     脱敏示例和案例
CHANGELOG.d/  模板演进记录片段
```

## 安全原则

1. 只记录凭据来源，不记录凭据值
2. 自动发现只生成草稿，必须人工确认
3. 删除/重建/回滚类操作必须审批 + oplog
4. 外发报告必须脱敏
5. 高风险/反复失败场景建议切 GPT-5.5
