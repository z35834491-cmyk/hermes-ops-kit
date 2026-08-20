# Contributing

Hermes Ops Kit is a template and contract project. Contributions should preserve its local-first and security-first boundary.

## Contribution rules

- Do not commit real IP addresses, internal hostnames, business domains, credentials, kubeconfig contents, or raw incident logs.
- Use placeholders such as `<ENV>`, `<NAMESPACE>`, `<COMPONENT_NAME>`, `<KUBECONFIG_PATH>`.
- Public scripts must default to read-only or skeleton behavior.
- Generated discovery output must remain candidate-only until reviewed by a human.
- L2/L3 execution flows must include approval, rollback, and audit contracts.

## Before submitting changes

Run:

```bash
make check
```

This includes:

- script compile checks
- publish guard
- sensitive-content scan
- JSON template validation
- inspection/onboarding skeleton checks
- local Hermes health-check template
- `git diff --check`

## Adding a runbook example

1. Put metadata under `examples/runbooks/<name>.yaml`.
2. Use `risk_level` and `mode` explicitly.
3. Keep examples sanitized.
4. For L1+ examples, include rollback and approval requirements.
5. Update `examples/runbooks/README.md` and `CHANGELOG.md`.

## Adding a schema

1. Put it under `config/schema/`.
2. Document it in `docs/schema-index.md`.
3. Add at least one sanitized template/example.
4. Extend `make check` if machine validation is possible.
