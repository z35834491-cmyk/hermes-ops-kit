<p align="right">
  <b>简体中文</b> · <a href="onboarding.en.md">English</a>
</p>

# 接入

把一个环境接到 Hermes Ops Kit 的步骤。公开脚本不扫真实集群。逐步命令见 [clone-and-run.md](clone-and-run.md)。

## 接入流程

1. 准备 kubeconfig **路径**或节点清单别名（不要把文件内容提交进 Git）
2. 复制 `config/env-map.example.yaml` → `config/env-map.local.yaml`
3. 填写环境名、kubeconfig 路径、namespace、凭据**来源**、`inspection.include`
4. 没有的中间件：`components.<name>.mode: disabled`，并从 include 拿掉
5. `python3 scripts/validate_env_map.py ... --catalog config/check-catalog.yaml`
6. 可选：`python3 scripts/onboard.py` 只生成**草稿**候选，必须人工审阅
7. `inspect.py <env> --plan`，确认后 `--save`
8. 对照 `examples/runbooks/`；真实只读检查走私有 overlay
9. 可选：脱敏 lesson-candidate → `precipitate.py` 草稿，人工晋升；见 [precipitation.md](precipitation.md)

## 自动发现边界

公开 `onboard.py` 只写候选 YAML，**不**连接 Kubernetes / SSH / DB，也不直接改 `env-map.local.yaml`。
公开 `precipitate.py` 同样只写草稿，**不**读 `~/.hermes` 或原始 oplog。

以后私有 overlay 若做只读发现，仍然只生成草稿。可发现的是清单类事实；主从角色、可清理队列、生产边界必须人工确认。
