# Runbook 示例 / Runbook examples

这些是脱敏的 runbook **元数据**示例，不是生产规程，不含私有基础设施细节。
These are sanitized runbook **metadata** examples. They are not production runbooks and do not contain private infrastructure details.

## 当前示例 / Current examples

| Runbook | 类别 Category | 风险 Risk | 模式 Mode | 用途 Purpose |
|---|---|---|---|---|
| `k8s-pod-abnormal-diagnostic.yaml` | k8s | L0 | read-only | 只读诊断异常 Pod，不重启/删除 / diagnose abnormal pods without restart/delete |
| `mysql-replication-lag-diagnostic.yaml` | mysql | L0 | read-only | 只读复制延迟，不改复制 / read replica lag without replication changes |
| `rabbitmq-stale-queue-diagnostic.yaml` | rabbitmq | L0 | read-only | 识别残留队列候选，不清空/删除 / identify stale queue candidates without purge/delete |

## 规则 / Rules

- 使用占位符和通用名 / use placeholders and generic names
- L0 必须严格只读 / keep L0 examples strictly read-only
- L1/L2/L3 必须包含审批和回滚元数据 / L1+ must include approval and rollback metadata
- 不要真实 IP、主机名、队列名、库名或凭据 / no real IPs, hostnames, queue names, database names, or credentials

## 计划中的示例 / Planned examples

- Redis 健康诊断 / Redis health diagnostic
- Elasticsearch 磁盘/索引诊断 / Elasticsearch disk/index diagnostic
- 节点内存高诊断 / node memory high diagnostic
- Longhorn PVC 用量诊断 / Longhorn PVC usage diagnostic
- ArgoCD sync 漂移诊断 / ArgoCD sync drift diagnostic
