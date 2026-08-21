<p align="right">
  <b>简体中文</b> · <a href="bestnative-integration.en.md">English</a>
</p>

# 后续怎么接 BestNative

**先把 BestNative 做成独立仓库，再在那边读本仓库。不要在 Ops Kit 里写适配器或审批状态机。**

当前 kit（`v0.4-preview`）已经提供合同。缺的是 BestNative 产品本身：页面、API、数据库、RBAC。

```text
现在：Hermes 本机 + Ops Kit 合同
下一步：新建 BestNative 仓，一期只读
再往后：BestNative 审批/审计
最后：审批通过后再桥接 Hermes 执行
```

---

## 谁先谁后

| 顺序 | 在哪做 | 做什么 |
|---|---|---|
| 1（当前） | **本仓库 Ops Kit** | 合同稳定：catalog、inspection JSON、runbook、approval schema |
| 2（下一步） | **BestNative 新仓** | 最小控制面：能跑起来的 Web/API，**还不要执行** |
| 3 | BestNative 仓 | 适配器：`HERMES_OPS_KIT_PATH` 只读加载 kit |
| 4 | BestNative 仓 | 审批队列 + 审计库 |
| 5 | BestNative 仓 + 本机 Hermes | 有 approval id 才允许受控执行 |

合仓排在最后，条件见 [../future-product/merge-readiness.md](../future-product/merge-readiness.md)。早期用独立仓 + 本地路径最安全。

---

## 怎么联动

```mermaid
flowchart TB
  subgraph kit["Hermes Ops Kit · 本仓库"]
    CAT["check-catalog.yaml"]
    RB["examples/runbooks/*.yaml"]
    SCH["config/schema/*.yaml"]
    INS["inspect.py → reports/*.json"]
  end
  subgraph priv["本机私有 · 不进 Git"]
    EM["env-map.local.yaml"]
    OV["私有 overlay 真实只读"]
  end
  subgraph bn["BestNative · 独立仓 · 尚未实现"]
    AD["只读适配器 loader"]
    UI["资产 / 历史 / Runbook 目录"]
    AP["审批中心"]
    AU["审计时间线"]
  end
  Hermes["Local Hermes"]

  EM --> INS
  OV --> INS
  CAT --> AD
  RB --> AD
  SCH --> AD
  INS --> AD
  EM -.->|"路径配置，不把凭据值入库"| AD
  AD --> UI
  UI --> AP
  AP -->|"以后：带 approval id"| Hermes
  Hermes -->|"读同一套合同"| kit
```

```text
HERMES_OPS_KIT_PATH=/path/to/hermes-ops-kit
HERMES_OPS_REPORTS_DIR=/path/to/reports
HERMES_OPS_ENV_MAP=/path/to/env-map.local.yaml
```

BestNative **只读**这些文件，不改 kit 源码，不把 schema fork 一份自己演化（跟 `schema_version`）。

可读文件清单：[bestnative-contract.md](bestnative-contract.md)。

---

## BestNative 一期（只读）

在 **BestNative 仓库**实现，不在本仓库：

1. 配置 `HERMES_OPS_KIT_PATH`，路径无效时给出明确错误。
2. 加载 catalog、`examples/runbooks/*.yaml`、`reports/<env>/inspection-*.json`、schema。
3. API 建议：`GET /api/ops-kit/status|inspection-runs|runbooks|schemas`。语义不要改成执行。
4. **没有** `POST /execute`、没有 Web kubectl、没有把密码写入 BestNative DB。

验收：打开 BestNative 能看到 kit 的 catalog / runbook / 本地历史；关掉 kit 路径会失败而不是静默编造数据。

---

## 二期、三期

**二期**：按 `approval.schema.yaml` 做审批单和审计表。没有 approval id，不能进入 L2/L3。`commands_hash` 变了则审批作废。

**三期**：RBAC、命令哈希、回滚计划齐了，再把已批准的计划交给本机 Hermes。执行结果写回 `operation_audit`。PRD 默认仍只出命令。

不要颠倒：没有审批中心就不要做执行桥。

---

## 本仓库不再加什么

- BestNative 前端/后端代码
- `backend/app/integrations/hermes_ops_kit/`
- 审批状态机实现
- 把 BestNative 当 git submodule 塞进本仓库

kit 侧后续只维护合同。联动代码属于 BestNative。阶段拆解见 [implementation-roadmap.md](implementation-roadmap.md) Phase 3–5。

## 禁止

- 危险的 Web kubectl
- 凭据值进 BestNative 数据库
- 自动把 discovery 晋升为正式 env-map
- 在 kit 里「顺便」实现控制面
