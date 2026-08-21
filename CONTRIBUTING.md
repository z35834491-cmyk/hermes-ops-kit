# 贡献指南 / Contributing

Hermes Ops Kit 是模板和契约项目。贡献必须保持本地优先、安全优先的边界。
Hermes Ops Kit is a template and contract project. Contributions must keep the local-first, security-first boundary.

## 规则 / Rules

- 不要提交真实 IP、内部主机名、业务域名、凭据、kubeconfig 内容或原始故障日志。
  Do not commit real IPs, internal hostnames, business domains, credentials, kubeconfig contents, or raw incident logs.
- 使用占位符，例如 `<ENV>`、`<NAMESPACE>`、`<COMPONENT_NAME>`、`<KUBECONFIG_PATH>`。
  Use placeholders such as `<ENV>`, `<NAMESPACE>`, `<COMPONENT_NAME>`, `<KUBECONFIG_PATH>`.
- 公开脚本必须默认只读或骨架行为，不得默认连接真实集群/SSH/数据库。
  Public scripts must default to read-only or skeleton behavior and must not connect to real clusters, SSH, or databases.
- 自动发现输出只能是候选，人工确认后才能晋升。
  Discovery output is a candidate only until a human reviews it.
- L2/L3 执行流必须包含审批、回滚和审计合同。
  L2/L3 execution flows must include approval, rollback, and audit contracts.

## 提交前 / Before submitting

```bash
make check
```

包含 Includes: 脚本编译、发布护栏、脱敏扫描、JSON 模板校验、巡检/onboard 骨架检查、`git diff --check`。
This includes compile, publish guard, sanitize scan, JSON validation, inspection/onboarding skeleton checks, and `git diff --check`.

不要把 `make health-check` 当仓库门禁。那是可选模板，会碰到本机 Hermes 目录。
Do not treat `make health-check` as a repository gate. It is an optional template and may look at a local Hermes home.

## 增加 Runbook 示例 / Adding a runbook example

1. 元数据放到 `examples/runbooks/<name>.yaml`。 / Put metadata in `examples/runbooks/<name>.yaml`.
2. 明确写出 `risk_level` 和 `mode`。 / Set `risk_level` and `mode` explicitly.
3. 保持脱敏。 / Keep examples sanitized.
4. L1+ 必须包含回滚和审批要求。 / L1+ examples must include rollback and approval requirements.
5. 更新 `examples/runbooks/README.md` 和 `CHANGELOG.md`。 / Update `examples/runbooks/README.md` and `CHANGELOG.md`.

## 增加 schema / Adding a schema

1. 放到 `config/schema/`。 / Put it under `config/schema/`.
2. 在 `docs/schema-index.md` 登记。 / Document it in `docs/schema-index.md`.
3. 至少提供一份脱敏模板/示例。 / Add at least one sanitized template or example.
4. 能机器校验的，补进 `make check`。 / Extend `make check` when machine validation is possible.
