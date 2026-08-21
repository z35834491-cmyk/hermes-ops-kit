# Changelog

## v0.4.0-preview - inspection framework close-out

- env-map loader now reads `inspection.exclude` and `components.*.mode=disabled`. Inspect emits skipped results for those checks instead of dispatching them.
- Each dispatched check records `duration_seconds`; skipped/filter results stay `0.0`.
- Empty `inspection.include: []` no longer falls through to the full catalog; missing include still uses catalog keys as a skeleton default.
- `validate_env_map.py --catalog` fails on include/exclude ids that are not in `check-catalog.yaml`, and warns when include lists a disabled component.
- Public K8s checker no longer shells out to kubectl. Parsers stay for unit tests that inject a fake runner; `--execute-readonly` without a private overlay stays skipped.
- Inspection JSON contract aligned: `schema_version`, `mode`, and `summary.skipped` are required across schema, template, example, inspect output, and `validate_inspection.py`.
- `inspect.py all` stamps `env` on every check so duplicate check ids across environments stay distinguishable.
- Missing env-map / unknown target now exits non-zero.
- `onboard.py` candidate include list matches `check-catalog.yaml` (`pvc_status` instead of `pvc_usage`).
- `config/env-map.example.yaml` include lists now match `check-catalog.yaml` (`pvc_usage` / `node_disk` removed until they exist in the catalog).
- `make check` is repository-only: compiles `scripts/lib` and `scripts/checkers`, validates template/example JSON semantically, plans `test` and `all`, and no longer runs the optional Hermes health-check template as a gate.
- Docs (`README`, `architecture`, `project-status`, `implementation-roadmap`) now describe the current stage as `v0.4-preview`.
- GitHub-facing docs (README, docs index, CONTRIBUTING, SECURITY, clone-and-run) are bilingual Chinese/English.
- Added sanitized Redis and Elasticsearch L0 runbook metadata. Credential handling stays source-based (`file` / `env` / `k8s_secret` / `external_secret` / `manual`); `.pw` files are not required.
- Added remaining sanitized L0 runbook metadata for node memory, ArgoCD sync drift, and Longhorn PVC/volume health.
- Added `docs/public-release-review.md`, the v0.5 human review procedure before making the repository public.
- `make check` now validates runbook metadata. Inspection examples/templates require `mode` and per-check `duration_seconds`.
- Private checker template no longer uses `shell=True`.
- `inspect.py` accepts any env-map environment name, not only `dev`/`test`/`prd`. `--save` path notices go to stderr so `--json` stdout stays valid JSON.
- GitHub-facing README, architecture, and BestNative contract updated for upload: usage, structure diagrams, current inspection JSON fields, and `examples/runbooks/` as the runbook catalog source.
- Added `docs/product.md`: Hermes Ops Kit is a companion contract kit, not a Hermes feature branch; README now states capabilities and advantages.
- Expanded `docs/clone-and-run.md` into a full usage flow: first-time env-map fields, inspect flags, reports, runbooks, private overlay, and Hermes.
- Documented the BestNative handoff: build BestNative as a separate repo first, then read this kit; linkage stays out of Ops Kit.
- Split GitHub landing into Chinese `README.md` and English `README.en.md` with a language switcher and logo.
- Split user-facing docs the same way (`product`, `clone-and-run`, `architecture`, BestNative, overlay, onboarding). Default files are Chinese; `*.en.md` is English.
- README now states in concrete terms what you write, what `inspect.py` emits, and what Hermes is supposed to read.

## v0.3.0-prep - GitHub-ready and BestNative preparation

- 增加 `future-product/`，保存最终产品愿景、架构和合并条件，明确当前 Ops Kit 与 BestNative 仍保持独立。
- 新增 `docs/private-checker-guide.md` 与 `examples/private-checker-template.py`，说明如何在私有 overlay 中接入真实只读检查而不污染 public 模板。
- 新增 `scripts/lib/check_catalog.py` 共享 check-catalog loader，并让 `inspect.py` 复用该加载入口；当前单元测试总数提升到 14。
- 新增 `scripts/lib/env_map.py` 共享 env-map loader，并让 `inspect.py` 与 `validate_env_map.py` 复用同一配置加载入口。
- 增加 env-map loader 单元测试，当前单元测试总数提升到 12。
- `argocd_sync` 和 `longhorn_health` 作为可选 K8s checker 加入 catalog；Longhorn 默认 disabled，只有使用该存储后端的环境才应 include。
- K8s checker 增加 `high_restart` 与 `node_resource_top` 只读解析，并补充对应单元测试。
- K8s checker 增加 `warning_events` 与 `pvc_status` 只读解析，并补充对应单元测试。
- K8s checker 在 `execute=True` 时具备已测试的只读节点 Ready 和 Pod 异常解析能力；public plan mode 仍不执行真实命令。
- 增加 K8s checker 单元测试，覆盖 plan 不执行、节点 Ready 解析、Pod 异常解析。
- 增加 `scripts/validate_inspection.py`，对 inspection JSON 做语义校验，防止计划模式中隐藏 checker failed。
- `scripts/inspect.py` 增加 `--plan`、`--catalog` 和 checker dispatcher，可基于 env-map + check catalog 输出 plan-only 检查结果。
- 增加 `config/check-catalog.yaml` 和 `scripts/checkers/` 插件骨架（K8s/MySQL/Redis/RabbitMQ/Elasticsearch），public 版仍不连接真实环境。
- 增加 `docs/checker-development.md`，说明如何安全扩展私有只读 checker。
- 增加 `docs/implementation-roadmap.md`，固定 Hermes Ops Kit → BestNative 运维平台的阶段计划、验收标准和防跑偏检查。
- 增加 `scripts/render_summary.py`，可把 inspection JSON 渲染为终端摘要，便于 CLI/BestNative mock 复用。
- 增加 `scripts/validate_env_map.py`，提供无外部依赖的 env-map 结构校验。
- `scripts/inspect.py` 开始读取 env-map 名称并在输出中展示 contract 校验证据（仍不连接真实环境）。
- 增加 `scripts/hermes_local_health_check.py`，把本地 Hermes 只读体检能力抽象成可复用模板
- 增强 `scripts/inspect.py`：固定 target choices、schema_version、help 行为和无真实连接的 public contract
- 增强 `scripts/onboard.py`：生成 `env-map.generated.yaml` 候选 skeleton，强调人工确认后才能提升为正式 env-map
- 增强 `scripts/sanitize_check.py`：输出文件/行号/命中类型，检查私钥、kubeconfig 片段、连接串、明文 secret、真实私网 IP、本地 env-map 文件等
- 增加 `Makefile`，提供 `make check` / `make sanitize` / `make inspect-check` / `make health-check`
- 增加 `SECURITY.md`、`docs/bestnative-contract.md` 和 `templates/approval-request-template.json`
- 增强 `Makefile`，加入 py_compile、onboard、approval JSON 校验
- 修正 README v0.3-prep 路线和 GitHub-ready 检查入口
- 增加 `docs/end-to-end-example.md` 和 `examples/inspection-result.example.json`，展示 env-map → inspection result → runbook → approval 的端到端消费路径。
- 增加 `examples/README.md`，明确示例数据脱敏规则。
- 增加 `docs/clone-and-run.md`，说明 clone 后如何 `make check`、创建 `env-map.local.yaml`、运行 inspect/onboard skeleton。
- 增加 GitHub Actions workflow `.github/workflows/check.yml`，push/PR 时运行 `make check`。
- 重写 README 为上传前版本，明确项目定位、clone-and-run、目录、检查、BestNative 接入方向。
- 增加 `LICENSE`（MIT）。
- 增加 Runbook metadata 示例：K8s Pod 异常、MySQL 复制延迟、RabbitMQ 残留队列
- 调整 `sanitize_check.py`：默认跳过本地私有 env-map/.env 文件内容，配合 `publish-guard` 检查它们不能进入 Git 跟踪
- 增强 `Makefile` 的 `publish-guard`，防止本地私有配置/凭据文件被纳入仓库

## v0.2.0 - local Hermes usability + schema contract

- 增加 `config/schema/`：env-map、inspection-result、runbook、approval/audit 四类 schema 草案
- 增加 `templates/runbook-metadata-template.yaml` 和说明文档，便于 skill/runbook 被 UI 或脚本消费
- 增加 `templates/inspection-result-template.json` 和 `templates/digest-jsonl-template.jsonl`
- 将 `scripts/inspect.py` 从纯 skeleton 升级为 JSON/Markdown 输出契约 skeleton，支持 `--json --save`
- 优化 `config/env-map.example.yaml`：加入 version、discovery output、disabled component、risk、凭据来源示例
- 重写 README：明确本地优先、真实配置不提交、普通巡检手动触发、不设 cron、BestNative 后置

## v0.1.0 - draft

- 初始化 Hermes Ops Kit 本地私有模板骨架
- 增加 env-map 示例、模型路由示例
- 增加安全模型、接入、手机端、每周维护文档
- 增加 oplog/incident/change/approval 模板
- 增加 onboard/inspect/sanitize_check 脚本骨架
- 增加 `docs/ai-sre-runbook-platform.md`，定义 AI-native SRE / AI SRE Runbook Platform 定位、架构、案例、平台化路线和简历表述
- 增加 `docs/audit-system.md`，定义文件级审计、审批审计、安全事件和未来 BestNative Audit Center 设计
- 增加 `docs/metrics-and-feedback.md`，定义 MTTR、Runbook 命中率、审批覆盖率、误判次数等度量体系
