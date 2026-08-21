# Runbook 示例 / Runbook examples

这些是脱敏的 runbook **元数据**示例，不是生产规程，不含私有基础设施细节。
These are sanitized runbook **metadata** examples. They are not production runbooks and do not contain private infrastructure details.

## 当前示例 / Current examples

| Runbook | 类别 Category | 风险 Risk | 模式 Mode | 用途 Purpose |
|---|---|---|---|---|
| `k8s-pod-abnormal-diagnostic.yaml` | k8s | L0 | read-only | 只读诊断异常 Pod，不重启/删除 / diagnose abnormal pods without restart/delete |
| `mysql-replication-lag-diagnostic.yaml` | mysql | L0 | read-only | 只读复制延迟，不改复制 / read replica lag without replication changes |
| `rabbitmq-stale-queue-diagnostic.yaml` | rabbitmq | L0 | read-only | 识别残留队列候选，不清空/删除 / identify stale queue candidates without purge/delete |
| `redis-health-diagnostic.yaml` | redis | L0 | read-only | 只读角色/内存/复制状态，不 FLUSH / read role, memory, and replication without FLUSH |
| `elasticsearch-health-diagnostic.yaml` | es | L0 | read-only | 只读集群健康与磁盘水位，不删索引 / read cluster health and disk watermarks without index deletes |
| `node-memory-high-diagnostic.yaml` | k8s | L0 | read-only | 只读节点内存，不 cordon/drain / read node memory without cordon/drain |
| `argocd-sync-drift-diagnostic.yaml` | cicd | L0 | read-only | 只读 sync/health，不 sync/prune / read sync drift without sync or prune |
| `longhorn-pvc-usage-diagnostic.yaml` | longhorn | L0 | read-only | 只读 volume/PVC 健康，不删卷 / read volume/PVC health without deletes |

## 规则 / Rules

- 使用占位符和通用名 / use placeholders and generic names
- L0 必须严格只读 / keep L0 examples strictly read-only
- L1/L2/L3 必须包含审批和回滚元数据 / L1+ must include approval and rollback metadata
- 不要真实 IP、主机名、队列名、库名或凭据 / no real IPs, hostnames, queue names, database names, or credentials
- 凭据只引用 env-map 来源（file / env / k8s_secret / external_secret / manual），不规定必须用 `.pw` 文件 / credentials are env-map sources only; `.pw` files are one option, not a requirement

## 计划中的示例 / Planned examples

当前路线图中的 L0 示例已齐。后续如有新组件，按同样规则补元数据即可。
The planned L0 examples are complete. Add more only when a new component needs a sanitized metadata example.
