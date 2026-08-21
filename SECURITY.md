# 安全策略 / Security Policy

Hermes Ops Kit 是模板项目，不得包含真实运维秘密或私有基础设施数据。
Hermes Ops Kit is a template project. It must never contain real operational secrets or private infrastructure data.

## 数据处理 / Data handling

不要提交 Do not commit:

- 密码、token、API key、私钥、证书、kubeconfig 内容 / passwords, tokens, API keys, private keys, certificates, kubeconfig contents
- 带凭据的数据库 URL / database URLs containing credentials
- 真实私网 IP、内部主机名、业务域名 / real private IPs, internal hostnames, or business domains
- 原始 oplog、故障日志、机器清单、凭据文件 / raw oplog, incident logs, machine inventory, or credential files
- `config/env-map.local.yaml`、`config/env-map.generated.yaml`、`reports/`、`.backup/`

允许出现在本仓库 Allowed in this repository:

- 占位符，如 `<ENV>`、`<KUBECONFIG_PATH>`、`<NAMESPACE>`、`<COMPONENT_NAME>` / placeholders
- 不含值的凭据来源引用 / credential source references without values
- 脱敏示例 / sanitized examples
- schema 合同与脚本骨架 / schema contracts and script skeletons

## 发布前检查 / Pre-publish checks

```bash
make check
python3 scripts/sanitize_check.py .
git status --short
git diff --check
```

扫描器偏保守，不能替代人工审查。
The scanner is conservative but not complete. Manual review is required before publication.

## 执行安全 / Execution safety

公开脚本必须默认只读或骨架行为。
Public scripts in this repository must default to read-only or skeleton behavior.

- `scripts/inspect.py` 在公开模板中不连接真实基础设施。 / does not connect to real infrastructure in the public template.
- `scripts/checkers/k8s.py` 除非测试或私有 overlay 注入 runner，否则不调用 kubectl。 / does not invoke kubectl unless a test or private overlay injects a runner.
- `scripts/onboard.py` 只生成候选，人工审阅后才能晋升。 / generates candidates only; humans must review before promotion.
- 高风险动作在平台接入前必须有审批、回滚和审计设计。 / high-risk actions need approval, rollback, and audit design before platform integration.
- PRD 默认命令生成模式，除非已实现硬 RBAC 和审计。 / PRD defaults to command-generation unless hard RBAC and audit exist.

## 报告问题 / Reporting issues

私有部署不要把密钥或原始内部拓扑贴进公开 issue。请用脱敏复现步骤和占位符。
For private deployments, do not paste secrets or raw internal topology into public issues. Provide sanitized reproduction steps and placeholders.
