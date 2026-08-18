# Onboarding

## 接入流程

1. 准备 kubeconfig 或节点清单
2. 复制 `config/env-map.example.yaml` 为本地配置
3. 填写环境名称、kubeconfig、namespace、凭据来源
4. 运行自动发现（后续实现）
5. 人工确认候选组件
6. 运行首次巡检
7. 生成 onboarding report

## 自动发现边界

自动发现只生成草稿，不直接执行修改。

可自动发现：节点、namespace、svc、deploy/sts、pvc、Longhorn、Prometheus/Grafana 候选。

需人工确认：MySQL 主从、RabbitMQ 可清理队列、ES 认证方式、跳板链路、生产边界。
