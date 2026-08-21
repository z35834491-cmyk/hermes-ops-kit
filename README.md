# Hermes Ops Kit

当前阶段 Current stage: **`v0.4-preview`**

面向 Hermes Agent 的本地优先 AI SRE Runbook **模板/契约包**。
A local-first AI SRE Runbook **template and contract kit** for Hermes Agent.

它不是在线运维平台，也不是真实环境备份；它把巡检、Runbook、审批、审计和安全规则抽成可复用、可脱敏发布的骨架。
It is not an online ops platform and not a backup of a real environment. It turns inspection, runbooks, approval, audit, and safety rules into reusable, sanitized templates.

---

## 三层边界 / Three layers

```text
Local Hermes   = 私有运维 copilot；真实 env-map 与真实使用循环（不在本仓库）
Hermes Ops Kit = 本仓库：脱敏模板、schema、脚本骨架、安全规则、示例
BestNative     = 未来的 Web/API 控制面（独立代码库）：资产、巡检历史、审批、审计
```

```text
Local Hermes   = private operational copilot; real env-map and usage loop (not this repo)
Hermes Ops Kit = this repo: sanitized templates, schemas, script skeletons, safety rules, examples
BestNative     = future Web/API control plane (separate codebase): assets, history, approval, audit
```

终局愿景见 [`future-product/`](future-product/README.md)。那是规划，不是当前实现。
The end-state vision lives in [`future-product/`](future-product/README.md). That folder is planning, not the current product.

---

## 本仓库提供什么 / What this kit provides

- env-map schema 与示例 / env-map schema and examples
- 巡检 JSON/Markdown 合同 / inspection JSON and Markdown contract
- check catalog 与默认只规划（plan-only）的 checker / check catalog and plan-only checkers
- Runbook 元数据 schema 与 L0 示例 / runbook metadata schema and L0 examples
- 审批/审计 schema 与请求模板 / approval and audit schema plus request template
- 脱敏扫描与发布护栏 / sanitize scanner and publish guard
- 可选的本地 Hermes 体检模板（不是仓库门禁） / optional local Hermes health-check template (not a repo gate)
- BestNative 只读消费合同 / BestNative read-only consumption contract

## 本仓库不做什么 / What it does not do

- 不存储密码、token、私钥、kubeconfig 内容 / does not store passwords, tokens, private keys, or kubeconfig contents
- 不自动执行高风险操作 / does not auto-execute high-risk operations
- 不替代 Prometheus、Elasticsearch、Alertmanager / does not replace Prometheus, Elasticsearch, or Alertmanager
- 不提供生产 Web UI / does not ship a production Web UI
- **公开脚本不连接真实 Kubernetes / SSH / 数据库 / 外部服务** / **public scripts do not connect to real Kubernetes, SSH, databases, or external services**

---

## 克隆与运行 / Clone and run

```bash
git clone <REPO_URL> hermes-ops-kit
cd hermes-ops-kit
make check
```

创建仅本机使用的 env-map（只填路径、别名、凭据来源，不填凭据值）：
Create a private local env-map (paths, aliases, and credential sources only — never credential values):

```bash
cp config/env-map.example.yaml config/env-map.local.yaml
```

跑巡检骨架（默认不连集群）：
Run the inspection skeleton (no cluster access by default):

```bash
python3 scripts/inspect.py test --config config/env-map.local.yaml --catalog config/check-catalog.yaml --plan --json
python3 scripts/inspect.py test --config config/env-map.local.yaml --json --save
```

预期产物 Expected output:

```text
reports/test/inspection-<run_id>.json
reports/test/inspection-<run_id>.md
```

生成 onboarding 候选（必须人工审阅后才能晋升为 `env-map.local.yaml`）：
Generate an onboarding candidate (human review required before promotion):

```bash
python3 scripts/onboard.py --env test --output config/env-map.generated.yaml --force
```

更完整的步骤见 [`docs/clone-and-run.md`](docs/clone-and-run.md)。端到端合同流见 [`docs/end-to-end-example.md`](docs/end-to-end-example.md)。
Full steps: [`docs/clone-and-run.md`](docs/clone-and-run.md). End-to-end contract flow: [`docs/end-to-end-example.md`](docs/end-to-end-example.md).

文档目录 Documentation index: [`docs/README.md`](docs/README.md).

---

## 仓库结构 / Repository layout

```text
config/           env-map、check catalog、schema 合同
scripts/          inspect / onboard / 校验 / 脱敏（公开默认不连真实系统）
scripts/lib/      env-map 与 catalog 加载器
scripts/checkers/ 巡检插件（公开为 plan/skipped；解析逻辑仅供测试注入 runner）
templates/        JSON/YAML/Markdown 模板
examples/         脱敏示例与 L0 runbook 元数据
tests/            单元测试与合同测试
docs/             说明文档（见 docs/README.md）
future-product/   终局产品愿景（规划，非实现）
.github/          make check CI
```

---

## 安全模型 / Safety model

1. 真实配置只留在本地 `config/env-map.local.yaml`。 / Real config stays in local `config/env-map.local.yaml`.
2. 自动发现只写 `config/env-map.generated.yaml`，人工确认后才能晋升。 / Discovery writes `env-map.generated.yaml` only; humans promote it.
3. 只读巡检不需要审批。 / Read-only inspection does not require approval.
4. 修改、敏感、外写、影响服务、不可逆操作需要审批。 / Changes, sensitive, external-write, service-affecting, or irreversible ops need approval.
5. PRD 默认只出命令，除非已有硬 RBAC、审批和审计。 / PRD defaults to command-generation unless hard RBAC, approval, and audit exist.

详情 Details: [`SECURITY.md`](SECURITY.md), [`docs/safety-model.md`](docs/safety-model.md).

---

## 检查 / Checks

```bash
make check
```

`make check` 只检查**本仓库**：编译、发布护栏、脱敏扫描、JSON/env-map/inspection 校验、单元测试、onboard 候选、`git diff --check`。
`make check` is a **repository-only** gate: compile, publish guard, sanitize scan, JSON/env-map/inspection validation, unit tests, onboard candidate, `git diff --check`.

它不检查你机器上正在运行的 Hermes。下面这个目标是可选模板，不是门禁：
It does not inspect a running Hermes on your machine. This target is an optional template, not a gate:

```bash
make health-check
```

发布前请再人工过一遍 `config/`、`docs/`、`examples/`、`templates/`、`scripts/`、`CHANGELOG.d/`。
Before publishing, also review those directories manually.

---

## BestNative

BestNative 应把本仓库当合同/模板提供者来**只读消费**，不要在运行时改 Ops Kit 源码，也不要在审批/审计落地前执行 L2/L3。
BestNative should **read** this repo as a contract/template provider. It must not mutate Ops Kit sources at runtime, and must not execute L2/L3 before approval and audit exist.

- [`docs/bestnative-contract.md`](docs/bestnative-contract.md)
- [`docs/bestnative-integration.md`](docs/bestnative-integration.md)
- [`future-product/merge-readiness.md`](future-product/merge-readiness.md)

---

## 路线图 / Roadmap

| 阶段 Stage | 内容 What |
|---|---|
| `v0.3-prep` | GitHub 门禁、体检模板、BestNative 只读合同 / GitHub-ready checks, health-check template, read-only contract |
| `v0.4-preview`（当前 current） | env-map + catalog 驱动的只读巡检框架；公开 checker 保持 plan-only / env-map-driven read-only inspection framework; public checkers stay plan-only |
| `v0.5` | 公开模板评审与更多脱敏示例 / public template review and more sanitized examples |
| `v1.0` | BestNative 只读控制面接入（独立仓库） / BestNative read-only control-plane integration (separate repo) |

阶段计划 Phase plan: [`docs/implementation-roadmap.md`](docs/implementation-roadmap.md).
当前成熟度 Status: [`docs/project-status.md`](docs/project-status.md).

---

## 贡献 / Contributing

见 [`CONTRIBUTING.md`](CONTRIBUTING.md)。不要提交真实 IP、主机名、凭据或原始故障日志。
See [`CONTRIBUTING.md`](CONTRIBUTING.md). Do not commit real IPs, hostnames, credentials, or raw incident logs.

## 许可 / License

MIT
