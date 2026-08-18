# AI SRE Runbook Platform

## 定位

这套体系更准确地说是：

```text
AI-native SRE / AI 运维体系工程
```

如果用更产品化的名字，可以叫：

```text
AI SRE Runbook Platform
```

它不是单纯的 “vibe coding”，也不是普通脚本集合，而是一套把 SRE 运维经验、Runbook、审批、审计、巡检、ChatOps 和故障复盘整合起来的 AI-native 运维体系。

## 一句话描述

通过 Hermes Agent 构建 AI-native SRE 运维体系，将 K8s / MySQL / RabbitMQ / ES / Longhorn 等日常运维场景沉淀为可复用 Runbook，并结合手机端 ChatOps、审批机制、oplog 审计、巡检脚本、模型路由和每周知识库维护，实现“诊断—执行—验证—复盘—沉淀”的闭环。

## 这套体系解决什么问题

传统运维里，很多经验沉淀在个人脑子里：

- 哪个环境怎么连
- 哪个组件在哪个 namespace
- MySQL 从库怎么查
- RabbitMQ 残留队列怎么判断
- Longhorn/PVC 操作有哪些坑
- 什么操作必须审批
- 哪些历史故障不能再用旧方案处理

AI SRE Runbook Platform 的目标是把这些经验从“个人记忆”变成“系统能力”。

也就是说：

```text
不是让 AI 临场猜命令，而是让 AI 按已沉淀的 Runbook、审批规则和历史教训执行。
```

## 和 vibe coding 的区别

| 维度 | vibe coding | AI SRE Runbook Platform |
|------|-------------|--------------------------|
| 工作方式 | 临场生成命令/代码 | 先查 skill / env-map / oplog / 历史教训 |
| 可复用性 | 弱 | 强，经验沉淀为 Runbook/skill |
| 审计 | 基本没有 | oplog + 运维日志 + session 历史 |
| 安全 | 容易 YOLO | 审批、备份、oplog、模型升级 |
| 手机端 | 普通聊天 | ChatOps 远程巡检/排查入口 |
| 故障复盘 | 手工总结 | 故障 → skill/oplog/文档闭环 |
| 模型选择 | 随意 | 日常 DeepSeek，高风险 GPT-5.5 |
| 平台化潜力 | 低 | 可发展为 Runbook/审批/审计平台 |

一句话：

```text
vibe coding = AI 临场帮你写/跑
AI SRE Runbook Platform = AI 带着操作规程、环境地图、审批和审计干活
```

## 当前已有能力

### 1. 环境地图与命令入口

通过 `k8s-env-map` skill 沉淀：

- DEV / TEST / PRD 环境边界
- K8s kubeconfig 路径
- 中间件位置
- 高频命令速查
- 巡检脚本入口
- 常见命令坑（字段顺序、转义、输出解析）

### 2. 手动巡检体系

当前已具备手动触发巡检能力：

- CLI 触发
- 微信手机端触发
- 覆盖 K8s 节点、Pod、MySQL 从库、RabbitMQ、ES、Flink、QuestDB、Longhorn/PVC、节点磁盘等
- 与 Prometheus 不冲突，是独立的个人巡检工具

### 3. 手机端 ChatOps

通过 Hermes Gateway 接入微信：

- 手机发“巡检”即可触发 Hermes 运维会话
- 可远程只读排查
- 高风险操作仍需审批
- gateway 由 launchd 守护，Mac 登录后自动恢复

### 4. 操作审批与安全边界

核心安全原则：

- 执行前说明意图、工具和影响
- 敏感/不可逆操作二次确认
- 修改前备份
- 不可逆操作写 oplog
- BLOCKED 后禁止绕过
- 外发内容脱敏

### 5. oplog 审计

不可逆或高风险操作会记录：

- 背景
- 原因
- 命令
- 影响范围
- 回滚方式
- 验证结果
- 最终结论

这让操作可以被回溯，不再只存在聊天上下文里。

### 6. skill 知识沉淀

把运维经验固化为可复用 skill，例如：

- MySQL 从库修复
- RabbitMQ 残留队列处理
- K8s 环境地图
- 模型选择策略
- 每周 Hermes 维护
- Ops Kit 模板演进

### 7. 模型路由

当前策略：

- DeepSeek v4 Pro：日常巡检、只读排查、标准流程、文档总结
- GPT-5.5：复杂根因、高风险变更、MySQL binlog/DDL/位点、Longhorn、PRD、连续失败后的策略判断

目的不是盲目用贵模型，而是在成本和风险之间做路由。

### 8. 每周维护机制

通过 `hermes-weekly-maintenance` skill 做周期性检查：

- skill 是否冲突/过期
- oplog 是否收尾
- memory 是否堆积技术细节
- gateway/pairing/cron 是否正常
- 巡检脚本是否误报
- 是否存在越权或幻觉风险

## 技术架构

当前架构可以抽象为：

```text
CLI / 微信 ChatOps / 后续 Web UI
        ↓
Hermes Agent
        ↓
Skills / Memory / Env Map / Approval Gate / Oplog
        ↓
K8s / MySQL / Redis / RabbitMQ / ES / Longhorn / Prometheus / Shark
```

其中：

- Hermes Agent：执行与推理核心
- Skill：Runbook 和可复用流程
- Memory：铁律和长期偏好
- Env Map：环境拓扑和凭据来源
- Approval Gate：审批边界
- Oplog：审计记录
- ChatOps：手机端入口

## 和 Prometheus / Shark 的关系

这套体系不替代 Prometheus 或 Shark。

更合理的分工是：

```text
Prometheus / Alertmanager：指标监控、告警、趋势
Shark：告警分析、AI 归因平台
Hermes Ops Kit：现场诊断、Runbook 执行、审批、审计、故障复盘、知识沉淀
```

Prometheus 负责“发现问题”。
Hermes 负责“确认问题、按 Runbook 处理、留下审计和教训”。

未来可以进一步打通：

```text
Prometheus Alert → Shark 分析 → Hermes 跑诊断 Runbook → 人审批 → 执行修复 → 回写结果
```

## 典型案例

### RabbitMQ 残留队列治理

问题：

- fanout + durable 队列 + 动态实例 ID
- Pod 重建后旧队列残留
- 消息持续广播导致磁盘暴涨

沉淀：

- RabbitMQ 速查命令
- 残留队列判断逻辑
- oplog 审计
- 给开发的 auto-delete 根治说明
- 巡检脚本检查项

### MySQL 从库修复教训

问题：

- 从库 SQL 线程停
- 缺表 / DDL 历史演进 / 手动补表冲突
- 曾误判结构漂移，差点全量重建

沉淀：

- 从库缺表不能直接按当前主库结构补表
- SQL 线程停止时做结构对比是无效证据
- 必须先恢复 SQL 线程并追平，再判断是否真正漂移
- 从库保持 `flush_log=2` / `sync_binlog=0` 合理，不必恢复 1/1
- 反复失败时建议切 GPT-5.5

这些案例体现了这套体系的价值：

```text
不是只修一次问题，而是把错误和经验沉淀成下次不会再犯的系统规则。
```

## 后续平台化路线

### v0.1：本地模板

- README
- env-map 示例
- 巡检脚本骨架
- oplog / incident / approval 模板
- 安全文档
- 手机端说明
- 模板演进 skill

### v0.2：自动发现

- `onboard.py` 自动发现 K8s 节点、namespace、svc、sts、pvc
- 生成 `env-map.generated.yaml`
- 人工确认后生效

### v0.3：配置化巡检

- `inspect.py` 从 env-map 读取配置
- 不再硬编码环境
- 支持多环境套用

### v0.4：巡检结果归档与 diff

- 巡检结果 JSON 化
- 最近 N 次趋势对比
- 异常变化报告

### v0.5：GitHub-ready 模板

- 脱敏案例
- sanitize_check 通过
- README 完整
- 示例可跑
- 默认安全策略

### v1.0：平台雏形

- Web UI
- Runbook 管理
- 审批中心
- 审计查询
- 巡检历史
- Alertmanager/Shark webhook 接入
- 多用户权限

## 简历可用表述

### 简洁版

设计并落地 AI-native SRE 运维体系，基于 Hermes Agent 构建 Runbook、巡检、审批、oplog 审计、手机端 ChatOps 与故障复盘闭环，覆盖 K8s、MySQL、RabbitMQ、ES、Longhorn 等组件，显著提升故障处置复用性和运维安全性。

### 强调平台化版

主导设计 AI SRE Runbook Platform，将个人运维经验抽象为可复用 skill/runbook，通过环境地图、自动巡检、审批矩阵、操作审计、模型路由和微信 ChatOps，实现从“临场排障”到“标准化、可审计、可沉淀”的 AI 运维体系。

### 强调安全治理版

构建基于 AI Agent 的运维安全执行框架，引入执行前审批、敏感操作二次确认、oplog 审计、数据防泄露、模型升级策略和每周知识库维护机制，降低 AI 运维中的越权执行、幻觉误判和历史规则漂移风险。

### 强调技术深度版

基于 Hermes Agent 构建 AI-native SRE 工作流，沉淀 K8s/Middleware 运维 Runbook，设计 env-map 环境抽象、巡检脚本、ChatOps 入口、oplog 审计和 skill 演进机制，并规划自动发现、巡检 diff、Webhook 告警联动和平台化能力。

## 面试时可以怎么讲

可以这样描述：

> 我不是简单用 AI 帮我写命令，而是把 AI Agent 当作一个可审计的运维执行层来设计。  
> 我把环境信息、巡检命令、故障处理流程、安全审批和历史教训分别沉淀到 env-map、skill、oplog 和运维文档里。  
> 日常巡检可以通过微信触发，高风险操作必须审批和记录。  
> 每次故障处理后，会把教训反写回 Runbook，避免下次重复踩坑。  
> 这套体系后续可以进一步抽象为 AI SRE Runbook Platform。

## 价值总结

这套体系的核心价值不是“用了 AI”，而是：

```text
把 SRE 的隐性经验变成显性流程，
把一次性故障处理变成可复用 Runbook，
把 AI 执行变成可审批、可审计、可复盘的工程体系。
```

这也是它和普通 AI 聊天、vibe coding、脚本集合最大的区别。
