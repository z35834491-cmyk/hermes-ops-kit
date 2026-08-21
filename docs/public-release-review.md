# 公开发布人工评审 / Public release review

这份文档是 `v0.5` 把仓库从「本地模板」切到「可公开」之前的**人工评审程序**。它补充 [`github-ready-checklist.md`](github-ready-checklist.md)：那边是门禁和扫描器，这边是扫描器覆盖不到的判断。
This is the **human review procedure** before switching Hermes Ops Kit from a local template to a public repository (`v0.5`). It complements [`github-ready-checklist.md`](github-ready-checklist.md): that file is gates and scanners; this file is judgment the scanner cannot make.

不要用这份清单去检查本机 Hermes（`~/.hermes`）或真实集群。
Do not use this review to inspect local Hermes (`~/.hermes`) or a live cluster.

## 何时做 / When

在以下任一时刻完整做一遍：

- 第一次把远程仓库设为 public 之前 / before the first public GitHub switch
- 准备把已有 private 仓库改 public 之前 / before making an existing private repo public
- 合入可能带环境事实的大改动之后 / after a large change that might include environment facts

## 自动门禁先过 / Automated gates first

```bash
make check
python3 scripts/sanitize_check.py .
git ls-files
git status --short
```

`make check` 必须通过。它覆盖编译、脱敏扫描、publish-guard、env-map/catalog 对齐、巡检 JSON 合同和单元测试。
`make check` must pass. It covers compile, sanitize scan, publish-guard, env-map/catalog alignment, inspection JSON contract, and unit tests.

不要把 `make health-check` 当发布门禁。它是可选模板，可能碰到本机 Hermes 目录。
Do not treat `make health-check` as a publish gate. It is an optional template and may look at a local Hermes home.

## 三层边界 / Three-layer boundary

评审时确认 README 和文档仍清楚分开：

| 层 Layer | 允许出现在本仓库 Allowed here | 不允许 Must not appear |
|---|---|---|
| Local Hermes | 不出现（只允许「不在本仓库」的说明） / mention only as out-of-repo | 真实 env-map、skill 全文、本机路径探查结果 / real env-map, full skills, local path reconnaissance |
| Hermes Ops Kit | 脱敏模板、schema、plan-only 脚本、L0 元数据 / sanitized templates, schemas, plan-only scripts, L0 metadata | 真实 IP、主机名、密码值、原始日志 / real IPs, hostnames, password values, raw logs |
| BestNative | 只读合同与规划文档 / read-only contract and planning docs | 适配器实现、审批状态机代码 / adapter implementation, approval state-machine code |

`future-product/` 只能是愿景，不能读起来像已经上线。
`future-product/` must remain vision/planning, not a claim that the product is live.

## 人工过目录 / Directory pass

扫描器偏保守，不能替代读文件。至少打开：

| 目录 Path | 看什么 Look for |
|---|---|
| `config/` | env-map 示例只有占位符和凭据**来源**；include 都在 catalog 里 / example env-map has placeholders and credential **sources** only; include ids exist in the catalog |
| `examples/` | runbook 是元数据不是生产规程；巡检 JSON 没有真实拓扑 / runbooks are metadata, not production SOPs; inspection JSON has no real topology |
| `docs/` | 不暗示公开脚本会连真实集群；规划文档有「未实现」边界 / docs do not imply public scripts hit real clusters; planning docs are labeled unfinished |
| `templates/` | 无真实 run_id 对应的私有环境 / no private environment baked into templates |
| `scripts/` | 公开 checker 默认 skipped/plan-only；无硬编码地址 / public checkers stay skipped/plan-only; no hardcoded addresses |
| `CHANGELOG.d/` | 无真实故障叙述或内部主机名 / no real incident narrative or internal hostnames |

禁止跟踪 Do not ship tracked copies of:

- `config/env-map.local.yaml`
- `config/env-map.generated.yaml`（来自真实环境 / from a real environment）
- `reports/`
- `.backup/`
- `*.pw` / `*.key` / `*.pem` / `.env`

## 凭据与中间件 / Credentials and middleware

公开合同写的是来源类型，不是某一种文件格式。

- 允许：`file` / `env` / `k8s_secret` / `external_secret` / `manual`
- `.pw` 只是 `file` 的一种示例，不是规定
- 没有的中间件：`components.<name>.mode: disabled`，并从 `inspection.include` 拿掉
- 另一种产品（例如 PostgreSQL）：留在私有 overlay，不要把真实连接信息写进本仓库

## 公开脚本行为 / Public script behavior

发布前确认：

- `scripts/inspect.py` 默认不连 Kubernetes / SSH / DB / HTTP
- `scripts/checkers/k8s.py` 没有注入 runner 时不调用 kubectl
- 中间件 checker 保持 plan-only
- `--execute-readonly` 在公开树里仍然 skipped，除非私有 overlay 自己接真实实现

## 文档表述 / Wording

拒绝这些说法：

- 「clone 后即可巡检你的生产集群」 / "clone it and inspect your production cluster"
- 「这是完整的运维平台」 / "this is a complete ops platform"
- 「已与 BestNative 打通」 / "BestNative is already integrated"

需要保留：

- 当前阶段是 `v0.4-preview`（直到 owner 明确升到 `v0.5`）
- 公开侧是模板/契约；真实检查在私有 overlay

## 通过标准 / Pass criteria

可以考虑公开，仅当：

1. `make check` 与 GitHub Actions 通过 / `make check` and GitHub Actions pass
2. 上表目录人工过完，无真实环境事实 / directory pass found no real environment facts
3. README 三层边界与非目标仍准确 / README boundary and non-goals remain accurate
4. Owner 已选择 LICENSE（当前 MIT） / LICENSE is chosen (currently MIT)

未通过则保持 private，修完再评。
If any item fails, keep the repository private and review again after the fix.

## 评审记录 / Review record

发布前由 owner 填写（不要把真实环境细节写进仓库）：

```text
reviewer:
date:
make_check: pass | fail
directory_pass: pass | fail
notes: (sanitized only)
publish_decision: keep-private | publish
```

记录可以留在 issue/PR 或私有笔记，不必提交进 Git。
Keep the filled record in an issue/PR or private notes. It does not have to be committed.
