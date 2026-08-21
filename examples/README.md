# 示例数据 / Example data

本目录只有脱敏示例，不含真实环境数据。
This directory contains sanitized examples only. No real environment data.

- `inspection-result.example.json` — 给 UI/API 用的巡检输出形状 / example inspection output for UI/API work
- `runbooks/*.yaml` — runbook 元数据示例 / example runbook metadata
- `env-map.dev-test.example.yaml` — env-map 形状示例 / example environment map shape
- `private-checker-template.py` — 私有 overlay 模板，不要把真实拓扑提交回来 / private overlay template; do not commit real topology

规则 Rules:

- 不要真实 IP / no real IP addresses
- 不要真实主机名 / no real hostnames
- 不要真实凭据 / no real credentials
- 不要原始故障日志 / no raw incident logs
- 使用占位符和通用服务名 / use placeholders and generic service names
