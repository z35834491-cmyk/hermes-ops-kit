# Hermes Ops Kit

Hermes Ops Kit 是一套本地优先的 AI SRE Runbook 模板，用于把 Hermes Agent 的巡检、排障、变更、审批、审计、oplog、skill 和故障复盘沉淀成可复用体系。

当前定位：本地私有 v0.3-prep 模板骨架。优先服务“单独使用 Hermes”的运维体验，并为 GitHub-ready 与后续 BestNative 只读控制平面接入做准备。

## 一句话分层

```text
Hermes Agent   = 推理 / ChatOps / 工具执行引擎
Hermes Ops Kit = env-map / Runbook / schema / 安全规则 / 模板资产
BestNative     = 后续 Web UI / 审批 / 审计 / 巡检历史控制平面
```

## 目标

- 快速接入 dev/test/prd 等运维环境
- 用 env-map 描述环境地图，但不保存任何凭据值
- 手动触发巡检，输出 Markdown + JSON
- 高风险操作前提供审批矩阵、备份、oplog 模板
- 故障处理后沉淀 skill / 运维日志 / Runbook metadata
- 后续可被 UI 读取并展示资产、巡检历史、审批和审计

## 非目标

- 不自动执行高风险修复
- 不绕过审批
- 不保存密码/token/API key/私钥/kubeconfig 内容
- 不直接替代 Prometheus / Alertmanager
- v0.3-prep 不提供生产级 Web UI

## 快速开始

```bash
cp config/env-map.example.yaml config/env-map.local.yaml
# 编辑 env-map.local.yaml：只填路径、别名和凭据来源，不填密码值
vim config/env-map.local.yaml

# 模板巡检 skeleton：不会连接真实基础设施
python3 scripts/inspect.py test --config config/env-map.local.yaml --json --save
```

输出示例：

```text
reports/test/inspection-<run_id>.json
reports/test/inspection-<run_id>.md
```

## 目录

```text
config/
  env-map.example.yaml              # 环境地图示例
  model-routing.example.yaml        # 模型路由示例
  schema/                           # env-map / inspection / runbook / approval schema
scripts/
  inspect.py                        # JSON/Markdown 输出契约 skeleton
  onboard.py                        # env-map.generated.yaml 候选生成 skeleton
  sanitize_check.py                 # GitHub-ready 敏感信息扫描
  hermes_local_health_check.py      # 本地 Hermes 只读体检模板
Makefile                            # make check / sanitize / inspect-check / health-check
docs/
  bestnative-integration.md
  bestnative-contract.md
  github-ready-checklist.md
  local-hermes-to-ops-kit.md
SECURITY.md                         # 安全边界和发布前检查
schemas/templates/docs/examples
```

## 本地使用原则

1. 真实配置放 `config/env-map.local.yaml`，不要提交。
2. 自动发现只能生成 `env-map.generated.yaml`，人工确认后才合并。
3. 普通巡检手动触发，不设 cron。
4. 只读巡检不需要审批；变更/敏感/外部写入/不可逆操作必须审批。
5. PRD 默认生成命令给人工执行，除非已有硬 RBAC、审批和审计。

## GitHub-ready 前检查

```bash
make check
# 或分步执行：
python3 scripts/sanitize_check.py .
# 确认本地私有文件没有进入 Git 跟踪：
git ls-files | grep -E '(^|/)(env-map\.local\.yaml|env-map\.generated\.yaml|\.env|reports/|\.backup/|.*\.pw|.*\.pem|.*\.key)$' && echo 'BLOCKED: private file tracked'
python3 scripts/inspect.py test --config config/env-map.example.yaml --json --save --reports-dir /tmp/hermes-ops-kit-check
python3 scripts/hermes_local_health_check.py --ops-kit .
git status --short
git diff --check
```

公开前必须确认：

- 无真实内网 IP / 主机名 / 业务域名
- 无密码 / token / API key / 私钥 / kubeconfig 内容
- 示例数据均为 example / placeholder
- 高风险执行能力默认禁用

## 下一步路线

- v0.2：schema + JSON 输出契约
- v0.3-prep：GitHub-ready 检查、health check 模板、BestNative 只读契约
- v0.4：inspect.py 从 env-map.local.yaml 读取并执行私有只读检查 + 脱敏案例完善
- v0.5：GitHub-ready
- v1.0：BestNative 只读控制平面接入
