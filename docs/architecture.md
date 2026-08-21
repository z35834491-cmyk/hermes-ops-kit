# 架构 / Architecture

```text
Local Hermes   = 私有运维 copilot（不在本仓库） / private copilot (out of this repository)
Hermes Ops Kit = 脱敏模板、schema、脚本、安全规则 / sanitized templates, schemas, scripts, safety rules
BestNative     = 未来 Web/API 控制面（独立代码库） / future Web/API control plane (separate codebase)
```

本仓库只做中间层，不会拿真实集群跑一套在线 Agent。
This repository is only the middle layer. It does not run a live agent against real infrastructure.

```text
env-map + check catalog
        ↓
scripts/inspect.py （默认 --plan / --plan by default）
        ↓
跳过 inspection.exclude 与 mode=disabled 组件 / skip exclude and disabled components
        ↓
checker 插件（公开：plan/skipped） / plugins (public: plan/skipped only)
        ↓
巡检 JSON/Markdown + validate_inspection.py
```

## 核心层 / Core layers

- **env-map**：环境事实和凭据来源（路径/别名，不含凭据值） / environment facts and credential sources (paths/aliases, never values)
- **check catalog**：检查项、风险级、对应 checker / checks, risk level, checker module
- **scripts**：巡检分发、校验、脱敏、onboard 候选 / dispatch, validate, sanitize, onboard candidate
- **runbook metadata**：只读诊断规程合同 / read-only diagnostic procedure contract
- **docs / future-product**：接入说明与终局规划 / docs and end-state planning

## 演进路线 / Roadmap

1. v0.1：本地模板，手动触发 / local templates, manual trigger
2. v0.2：schema 合同 + 巡检 JSON/Markdown 骨架 / schema contract + inspection skeleton
3. v0.3-prep：GitHub 门禁、BestNative 只读合同 / GitHub-ready gates, read-only contract
4. **v0.4-preview（当前 current）**：env-map + catalog 驱动的只读巡检框架 / env-map + catalog read-only inspection framework
5. v0.5：公开模板评审与更多脱敏示例 / public template review, more examples
6. v1.0：BestNative 只读控制面消费本仓库合同 / BestNative read-only control plane consumes these contracts

详细阶段见 [`implementation-roadmap.md`](implementation-roadmap.md)。终局愿景见 [`../future-product/`](../future-product/README.md)，不是当前实现。
Details: [`implementation-roadmap.md`](implementation-roadmap.md). End-state vision: [`../future-product/`](../future-product/README.md) — planning only.
