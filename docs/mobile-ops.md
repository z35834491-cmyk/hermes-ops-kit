# Mobile Ops

手机端通过 Hermes Gateway 接入，适合：

- 手动巡检
- 只读排查
- 低风险标准操作

不建议手机端直接执行：

- DROP / DELETE / RESET
- Longhorn 删除/迁移
- etcd/kube-apiserver 操作
- PRD 变更

高风险场景建议回 CLI 或切换 GPT-5.5，并要求审批 + oplog。
