# 项目状态 / Project status

当前状态 Current status: **`v0.4-preview`**

Hermes Ops Kit 是脱敏后的模板/契约包。它不是正在运行的 copilot，也不是 BestNative。
Hermes Ops Kit is a sanitized template/contract kit. It is not a live copilot and not a BestNative deployment.

## 已完成 / Completed

- 本地优先的仓库结构 / local-first repository layout
- README / LICENSE / SECURITY / CONTRIBUTING（中英） / bilingual GitHub-facing docs
- `make check`（只作为本仓库门禁） / repository-only gate
- GitHub Actions 检查工作流 / GitHub Actions check workflow
- 脱敏扫描与发布护栏 / sanitize scanner and publish guard
- env-map / inspection / runbook / approval schema
- check catalog 与 inspect 分发 / check catalog and inspect dispatcher
- 公开 checker 为 plan-only；K8s 解析由测试注入 runner 覆盖 / public checkers stay plan-only; K8s parsers covered by injected-runner tests
- Inspection JSON 对齐 `schema_version` / `mode` / `summary.skipped` / `checks[].env` / inspection JSON fields aligned
- env-map loader 识别 `inspection.exclude` 与 `components.*.mode=disabled`；inspect 跳过对应检查并记录单条 `duration_seconds` / env-map loader honors exclude/disabled components; inspect records per-check duration
- env-map include/exclude 对照 check catalog 校验；空 include 不再回退到全部检查 / env-map include/exclude validated against the catalog; empty include does not expand to all checks
- 中英双语 GitHub 入口文档（README、文档索引、贡献与安全说明） / bilingual GitHub-facing docs
- env-map 与 inspection 校验器 / validators
- 巡检摘要渲染 / inspection summary renderer
- onboard 候选骨架 / onboarding candidate skeleton
- 可选本地 Hermes 体检模板（`make health-check`，非门禁） / optional health-check template (not a repo gate)
- BestNative 只读合同 / read-only contract
- 脱敏 L0 runbook 示例（K8s / MySQL / RabbitMQ / Redis / ES / 节点 / ArgoCD / Longhorn） / sanitized L0 runbook examples (K8s / MySQL / RabbitMQ / Redis / ES / node / ArgoCD / Longhorn)
- `future-product/` 规划文档（仅愿景） / planning docs (vision only)

## 尚未完成 / Not yet complete

- 真实只读发现（私有 overlay） / real read-only discovery (private overlay)
- BestNative 适配器（独立代码库） / BestNative adapter (separate codebase)
- 审批/审计状态机（BestNative） / approval/audit state machine (BestNative)
- 公开发布人工评审（`v0.5`） / public release manual review (`v0.5`)

## 建议的下一里程碑 / Next milestone

收口 `v0.4` 验收：公开 checker 保持 plan-only，catalog 与 env-map include 对齐，inspection JSON 字段稳定。不要在公开树里加真实集群调用。
Finish `v0.4` acceptance: keep public checkers plan-only, keep catalog and env-map includes aligned, keep inspection JSON fields stable. Do not add live infrastructure calls in the public tree.

见 See [`implementation-roadmap.md`](implementation-roadmap.md).
