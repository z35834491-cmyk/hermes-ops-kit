# Audit System

## 定位

审计系统是 AI SRE Runbook Platform 的安全底座，用来回答：

```text
谁在什么时间、通过什么入口、对哪个环境、执行/计划了什么操作，是否审批，结果如何，如何回滚。
```

当前阶段采用文件级审计，未来在 BestNative 中平台化为 Audit Center。

## 当前审计数据源

| 数据源 | 位置 | 作用 |
|--------|------|------|
| oplog | `~/.hermes/oplog/` | 高风险/不可逆操作的结构化审计主线 |
| session | `~/.hermes/state.db` / `~/.hermes/sessions/` | CLI/微信/cron 对话与工具调用流水 |
| 运维日志 | `~/Documents/运维日志/` | 给人看的故障、配置、巡检、资产归档 |
| skill | `~/.hermes/skills/` | 把审计中发现的教训沉淀为 Runbook |
| weekly maintenance | `hermes-weekly-maintenance` | 周期性检查审计是否完整、是否有未收尾项 |

## 审计分层

### 1. 操作审计

记录真实或计划中的变更操作：

- DB DROP / RESET / CHANGE REPLICATION
- kubectl delete / patch / apply / scale
- 文件删除/覆盖
- Longhorn/PVC 操作
- PRD 变更
- cron 创建/删除

当前用 oplog 记录。

### 2. 审批审计

记录用户是否授权、授权范围和是否二次确认。

重点记录：

- 是否明确同意
- 是否二次确认
- 是否被 BLOCKED
- 被 BLOCKED 后是否停止
- 是否存在用户锁屏/未响应时继续执行敏感操作

### 3. 工具调用审计

记录 agent 调用过哪些工具。

当前主要在 session 历史中，可通过 `session_search` 回查。

未来平台化后应落入 `agent_tool_calls` 表。

### 4. 安全事件审计

记录防幻觉、防越权、防泄露相关事件：

- BLOCKED 命令
- 误判后纠正
- 敏感输出风险
- 模型升级建议
- cron 遗留风险
- gateway/pairing 异常

### 5. 复盘审计

记录一次故障是否完成闭环：

- 是否写 oplog
- 是否写运维日志
- 是否更新 skill
- 是否有最终结论
- 是否清理临时文件
- 是否沉淀到模板

## oplog 标准字段

每个高风险操作 oplog 至少包含：

```markdown
# <环境> <操作主题> — <日期>

## 背景

## 影响范围

## 审批记录

## 执行命令

## 回滚方式

## 验证结果

## 最终结论
```

## 风险等级

| 等级 | 类型 | 示例 | 审计要求 |
|------|------|------|----------|
| L0 | 只读 | get/logs/status | session 记录即可 |
| L1 | 低风险写入 | 写本地文档、生成报告 | 记录文件变更 |
| L2 | 服务影响 | restart pod、scale、patch deploy | 审批 + oplog + 观察 |
| L3 | 数据/不可逆 | DROP、RESET、删 PVC、PRD 变更 | 二次审批 + 备份 + oplog + 回滚 |

## BestNative Audit Center 设计

未来 BestNative 可增加审计中心，核心表：

### operation_audit

```text
id
timestamp
environment
actor              # user / agent / cron / gateway
source             # cli / weixin / cron / web
action_type        # read / write / delete / restart / db / k8s
risk_level         # L0/L1/L2/L3
target
command_preview    # 脱敏摘要
approval_status
approved_by
oplog_path
session_id
rollback_plan
result
verification
```

### approval_requests

```text
id
operation_id
requested_by
approved_by
status             # pending / approved / rejected / expired
scope
impact
rollback
created_at
approved_at
```

### agent_tool_calls

```text
id
session_id
tool_name
arguments_redacted
result_summary
risk_level
created_at
```

### safety_events

```text
id
timestamp
event_type         # blocked / hallucination / sensitive_output / model_escalation
severity
description
related_session
related_oplog
resolved
resolution_note
```

## 每周审计检查

由 `hermes-weekly-maintenance` 执行：

- 最近 7 天 L2/L3 操作是否都有 oplog
- 被 BLOCKED 操作是否没有绕过
- 误判是否写最终结论并更新 skill
- 是否有临时 dump/backup 未清理
- cron 是否存在隐形执行源
- 手机端是否仍只做低风险或经审批操作

## GitHub / 对外发布注意

公开模板时，审计示例必须脱敏：

- 不写真实 IP
- 不写真实主机名
- 不写真实 secret 名称和值
- 不写真实连接串
- 案例只保留机制、流程和教训

## 价值

审计系统让 AI 运维从“聊天式操作”变成“可追踪、可回滚、可复盘”的工程体系。
