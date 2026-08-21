<p align="right">
  <b>简体中文</b> · <a href="project-status.en.md">English</a>
</p>

# 项目状态

当前状态：**`v0.4-preview`**

Hermes Ops Kit 是脱敏后的模板/契约包。它**不是** Hermes 的功能分支，也不是正在运行的 copilot，也不是 BestNative。

产品描述见 [product.md](product.md)。

## 已完成

- 本地优先的仓库结构
- README / LICENSE / SECURITY / CONTRIBUTING（中英分文件）
- `make check`（只作为本仓库门禁）
- GitHub Actions 检查工作流
- 脱敏扫描与发布护栏
- env-map / inspection / runbook / approval schema
- check catalog 与 inspect 分发；公开 checker 为 plan-only
- Inspection JSON 对齐 `schema_version` / `mode` / `summary.skipped` / `checks[].env` / `duration_seconds`
- env-map loader 识别 `inspection.exclude` 与 `mode=disabled`；空 include 不再回退到全部检查
- env-map 与 inspection / runbook 校验器
- 巡检摘要渲染、onboard 候选骨架
- 脱敏 lesson-candidate → `precipitate.py` L0 runbook 草稿（不读本机 Hermes）
- 可选本地 Hermes 体检模板（`make health-check`，非门禁）
- BestNative 只读合同与联动说明
- 脱敏 L0 runbook 示例（K8s / MySQL / RabbitMQ / Redis / ES / 节点 / ArgoCD / Longhorn）
- `future-product/` 规划文档（仅愿景）
- 公开发布人工评审程序
- `inspect.py` 接受任意环境名；`--save` 路径写到 stderr

## 尚未完成

- 真实只读发现（私有 overlay）
- BestNative 适配器（独立代码库）
- 审批/审计状态机（BestNative）
- 公开发布前由 owner 按 [public-release-review.md](public-release-review.md) 做一次人工评审

## 建议的下一里程碑

按 [public-release-review.md](public-release-review.md) 做一次人工评审后再考虑 `v0.5` 公开。公开 checker 保持 plan-only。见 [implementation-roadmap.md](implementation-roadmap.md)。
