<p align="right">
  <b>简体中文</b> · <a href="README.en.md">English</a>
</p>

# 文档目录

本目录是 Hermes Ops Kit 的说明。本仓库是**模板/契约包**，不是 Hermes 的功能分支，也不是正在运行的 Agent，也不是 BestNative。

先读根目录 [README.md](../README.md)。入口文档都有顶栏 **简体中文 / English** 切换。

建议阅读顺序：

1. [product.md](product.md) — 定位、能力、优势
2. [clone-and-run.md](clone-and-run.md) — 使用流程
3. [architecture.md](architecture.md) — 三层边界与巡检链路
4. [private-checker-guide.md](private-checker-guide.md) — 私有 overlay
5. [bestnative-integration.md](bestnative-integration.md) — 后续怎么接 BestNative
6. [public-release-review.md](public-release-review.md) — 公开发布人工评审

## 上手

| 文档 | 说明 |
|---|---|
| [product.md](product.md) | 产品定位、能力、优势；与 Hermes / BestNative 的关系 |
| [clone-and-run.md](clone-and-run.md) | env-map、inspect 参数、报告、Runbook、overlay、Hermes |
| [end-to-end-example.md](end-to-end-example.md) | env-map → 巡检 JSON → runbook → 审批 |
| [onboarding.md](onboarding.md) | 接入步骤与自动发现边界 |
| [precipitation.md](precipitation.md) | 故障教训如何变成 runbook 草稿 |
| [project-status.md](project-status.md) | 当前成熟度与未完成项 |

## 架构与合同

| 文档 | 说明 |
|---|---|
| [architecture.md](architecture.md) | 合同层与巡检链路 |
| [schema-index.md](schema-index.md) | schema / catalog 列表 |
| [implementation-roadmap.md](implementation-roadmap.md) | 阶段、验收、防跑偏 |
| [bestnative-contract.md](bestnative-contract.md) | BestNative 可只读的文件 |
| [bestnative-integration.md](bestnative-integration.md) | 先做独立仓；只读 → 审批 → Hermes |

## 安全与巡检插件

| 文档 | 说明 |
|---|---|
| [safety-model.md](safety-model.md) | 审批、备份、oplog、防幻觉 |
| [checker-development.md](checker-development.md) | 如何扩展 checker |
| [private-checker-guide.md](private-checker-guide.md) | 私有 overlay |
| [local-hermes-to-ops-kit.md](local-hermes-to-ops-kit.md) | 本地经验如何脱敏进入本仓库 |
| [github-ready-checklist.md](github-ready-checklist.md) | 上传 GitHub 前门禁清单 |
| [public-release-review.md](public-release-review.md) | v0.5 公开发布人工评审 |

## 规划材料（不是本仓库运行时）

这些描述更完整的 AI SRE 体系，部分能力属于本地 Hermes 或未来 BestNative，不要当成「本仓库已经实现」。

| 文档 | 说明 |
|---|---|
| [ai-sre-runbook-platform.md](ai-sre-runbook-platform.md) | 平台化叙述 |
| [audit-system.md](audit-system.md) | 审计分层 |
| [metrics-and-feedback.md](metrics-and-feedback.md) | 指标 |
| [mobile-ops.md](mobile-ops.md) | 手机端边界 |
| [weekly-maintenance.md](weekly-maintenance.md) | 每周维护清单 |

终局愿景：[../future-product/](../future-product/README.md)
