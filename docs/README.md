# 文档目录 / Documentation index

本目录是 Hermes Ops Kit 的说明文档。本仓库是**模板/契约包**，不是 Hermes 的功能分支，也不是正在运行的 Agent，也不是 BestNative。
This folder is the documentation for Hermes Ops Kit. This repository is a **template/contract kit**, not a Hermes feature branch, not a running agent, and not BestNative.

先读根目录 [README.md](../README.md)，再按需要打开下面的文档。
Start from the root [README.md](../README.md), then open the docs below as needed.

建议阅读顺序 Suggested reading order:

1. [product.md](product.md) — 定位、能力、优势（不是 Hermes 功能分支）
2. [clone-and-run.md](clone-and-run.md) — 使用流程：第一次、日常、私有 overlay、和 Hermes 配合
3. [architecture.md](architecture.md) — 三层边界与巡检链路
4. [private-checker-guide.md](private-checker-guide.md) — 私有环境如何接真实只读检查
5. [bestnative-contract.md](bestnative-contract.md) — 未来控制面只读哪些文件
6. [public-release-review.md](public-release-review.md) — 上传 GitHub 前的人工评审

## 上手 / Getting started

| 文档 Doc | 中文 | English |
|---|---|---|
| [product.md](product.md) | 产品定位、能力、优势；与 Hermes / BestNative 的关系 | Positioning, capabilities, advantages vs Hermes / BestNative |
| [clone-and-run.md](clone-and-run.md) | 使用流程：env-map、inspect 参数、报告、Runbook、overlay、Hermes | How to use: env-map, inspect flags, reports, runbooks, overlay, Hermes |
| [end-to-end-example.md](end-to-end-example.md) | env-map → 巡检 JSON → runbook → 审批的合同流 | Contract flow from env-map to approval |
| [onboarding.md](onboarding.md) | 接入步骤与自动发现边界 | Onboarding steps and discovery boundary |
| [project-status.md](project-status.md) | 当前成熟度与未完成项 | Current maturity and remaining work |

## 架构与合同 / Architecture and contracts

| 文档 Doc | 中文 | English |
|---|---|---|
| [architecture.md](architecture.md) | 合同层与巡检链路 | Contract layer and inspection path |
| [schema-index.md](schema-index.md) | schema / catalog 列表与消费者 | Schema/catalog list and consumers |
| [implementation-roadmap.md](implementation-roadmap.md) | 到 BestNative 的阶段、验收、防跑偏 | Phases, acceptance, anti-drift |
| [bestnative-contract.md](bestnative-contract.md) | BestNative 可只读消费的文件合同 | Read-only files BestNative may consume |
| [bestnative-integration.md](bestnative-integration.md) | 只读控制面 → 审批 → 受控执行 | Read-only plane → approval → execution |

## 安全与巡检插件 / Safety and checkers

| 文档 Doc | 中文 | English |
|---|---|---|
| [safety-model.md](safety-model.md) | 审批、备份、oplog、防幻觉 | Approval, backup, oplog, anti-hallucination |
| [checker-development.md](checker-development.md) | 如何扩展 checker；公开侧禁止连真实系统 | How to extend checkers; public side must not touch real systems |
| [private-checker-guide.md](private-checker-guide.md) | 私有 overlay 如何接真实只读检查 | Private overlay for real read-only checks |
| [local-hermes-to-ops-kit.md](local-hermes-to-ops-kit.md) | 本地经验如何脱敏后进入本仓库 | How local experience becomes sanitized templates |
| [github-ready-checklist.md](github-ready-checklist.md) | 上传 GitHub 前的门禁清单 | Pre-publish gate checklist |
| [public-release-review.md](public-release-review.md) | v0.5 公开发布人工评审程序 | v0.5 human review before making the repo public |

## 规划中的平台材料 / Planning notes (not this repo's runtime)

这些文档描述更完整的 AI SRE 体系，其中部分能力属于**本地 Hermes** 或未来的 BestNative，不要当成「本仓库已经实现」。
These describe the broader AI SRE system. Some capabilities belong to **local Hermes** or future BestNative — do not treat them as implemented in this repo.

| 文档 Doc | 说明 Note |
|---|---|
| [ai-sre-runbook-platform.md](ai-sre-runbook-platform.md) | 产品定位与平台化叙述 / product positioning |
| [audit-system.md](audit-system.md) | 审计分层与未来 Audit Center / audit layers |
| [metrics-and-feedback.md](metrics-and-feedback.md) | MTTR、Runbook 命中率等指标 / metrics |
| [mobile-ops.md](mobile-ops.md) | 手机端适用/不适用场景 / mobile ops boundary |
| [weekly-maintenance.md](weekly-maintenance.md) | 每周维护清单 / weekly maintenance |

终局愿景（独立于当前实现）在 [`../future-product/`](../future-product/README.md)。
End-state vision (not current implementation): [`../future-product/`](../future-product/README.md).
