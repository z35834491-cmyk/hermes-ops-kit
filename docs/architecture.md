# Architecture

```text
CLI / Mobile Gateway / Web UI（未来）
        ↓
Hermes Agent
        ↓
Skills + Env Map + Approval Gate + Oplog
        ↓
K8s / MySQL / Redis / RabbitMQ / ES / Prometheus / 其他系统
```

## 核心层

- env-map：环境事实和凭据来源
- skills：可复用 runbook
- scripts：自动发现、巡检、对比、脱敏检查
- oplog：不可逆操作审计
- docs：给人看的故障/变更/接入文档

## 演进路线

1. v0.1：本地模板，手动触发
2. v0.2：自动发现 + env-map 生成
3. v0.3：巡检结果归档 + diff
4. v0.4：Alertmanager/Webhook 接入
5. v1.0：Web UI / 审批 / 多用户
