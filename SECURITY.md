# Security Policy

Hermes Ops Kit is a template project. It must never contain real operational secrets or private infrastructure data.

## Data handling rules

Do not commit:

- Passwords, tokens, API keys, private keys, certificates, or kubeconfig contents
- Database URLs containing credentials
- Real private IP addresses, internal hostnames, or business domains
- Raw oplog, raw incident logs, machine inventory, or credential files
- `config/env-map.local.yaml`, `config/env-map.generated.yaml`, `reports/`, `.backup/`

Allowed in this repository:

- Placeholder values such as `<ENV>`, `<KUBECONFIG_PATH>`, `<NAMESPACE>`, `<COMPONENT_NAME>`
- Credential source references without values
- Sanitized examples
- Schema contracts and script skeletons

## Pre-publish checks

Run before pushing or publishing:

```bash
make check
python3 scripts/sanitize_check.py .
git status --short
git diff --check
```

The scanner is conservative but not complete. Manual review is required before publication.

## Execution safety

Public scripts in this repository must default to read-only or skeleton behavior.

- `scripts/inspect.py` does not connect to real infrastructure in the public template.
- `scripts/onboard.py` generates candidates only; humans must review before promotion.
- High-risk actions require approval, rollback plan, and audit design before any platform integration.
- PRD integrations default to command-generation mode unless hard RBAC and audit are implemented.

## Reporting issues

For private deployments, do not paste secrets or raw internal topology into public issues. Provide sanitized reproduction steps and placeholders.
