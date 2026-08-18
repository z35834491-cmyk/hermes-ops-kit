# Metrics and Feedback

## 定位

指标反馈体系用于证明 AI-native SRE 体系是否真的提升了运维效率、可靠性和安全性。

没有指标，体系只能靠感觉；有指标，才能持续优化并在简历/复盘/平台化时证明价值。

## 核心指标

| 指标 | 含义 | 目标 |
|------|------|------|
| MTTR | 故障平均恢复时间 | 持续下降 |
| Runbook Hit Rate | 故障是否命中已有 skill/runbook | 持续上升 |
| Repeat Error Rate | 同类错误重复发生率 | 持续下降 |
| Approval Coverage | 高风险操作审批覆盖率 | 100% |
| Oplog Coverage | L2/L3 操作 oplog 覆盖率 | 100% |
| Skill Update Rate | 故障后是否更新 skill | 高风险故障 100% |
| False Diagnosis Count | 误判次数 | 持续下降 |
| Model Escalation Count | 触发 GPT-5.5 升级次数 | 可解释、不过度 |
| Mobile Resolution Rate | 手机端可解决问题比例 | 低风险问题上升 |
| Cleanup Completion Rate | 临时文件/备份清理闭环率 | 持续上升 |

## 事件级记录建议

每次故障/变更后记录：

```yaml
incident_id: <id>
environment: dev/test/prd
started_at: <time>
resolved_at: <time>
mttr_minutes: <number>
trigger: alert/manual/mobile/cron
runbook_hit: true/false
skills_loaded:
  - k8s-env-map
  - mysql-replica-recovery
model_used: deepseek-v4-pro/gpt-5.5
model_escalated: true/false
high_risk_operation: true/false
approval_recorded: true/false
oplog_path: <path>
skill_updated: true/false
false_diagnosis: true/false
repeat_incident: true/false
```

## 周报指标

每周维护时汇总：

- 本周故障数
- 本周高风险操作数
- oplog 覆盖率
- skill 更新数
- 误判次数
- 重复故障数
- 手机端处理次数
- 被 BLOCKED 次数
- 清理/收尾项数量

## 如何使用指标

### 1. 优化 Runbook

如果某类问题重复发生但 runbook hit rate 低：

- 新建或完善对应 skill
- 将命令沉淀到 k8s-env-map references/scripts
- 更新 examples 脱敏案例

### 2. 优化模型路由

如果 false diagnosis count 上升：

- 检查是否低成本模型在高风险场景硬扛
- 更新 `ops-model-selection`
- 对 MySQL/Longhorn/PRD 等高风险问题提前升级 GPT-5.5

### 3. 优化安全治理

如果 approval coverage < 100%：

- 检查 approval-gate 是否漏触发
- 检查手机端是否越权
- 检查 cron 是否隐形执行

### 4. 优化模板平台化

如果同类环境接入时反复手写配置：

- 改进 env-map schema
- 增强 onboard.py 自动发现
- 增加 onboarding report

## 简历可用指标表达

示例：

```text
通过 Runbook 化和 ChatOps 改造，将常见故障处理流程标准化，建立高风险操作 100% 审批与 oplog 审计机制，并通过 weekly maintenance 持续降低重复误判和历史规则漂移风险。
```

后续如果有真实数据，可替换为：

```text
将同类故障 MTTR 从 X 分钟降低到 Y 分钟；高风险操作 oplog 覆盖率达到 100%；常见故障 Runbook 命中率提升到 Z%。
```

## 平台化路线

未来 BestNative 可增加 Metrics Dashboard：

- MTTR 趋势
- Runbook 命中率
- 审批覆盖率
- 误判次数
- 模型升级次数
- 手机端处理成功率
- 每周 skill 增长/修正趋势

这些指标是 AI SRE Runbook Platform 的价值证明。
