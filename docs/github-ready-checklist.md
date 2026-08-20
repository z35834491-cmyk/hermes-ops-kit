# GitHub-ready Checklist

Hermes Ops Kit can be published only after the template is detached from the author's private environment.

## Required gates

- [ ] No real private IP addresses.
- [ ] No internal hostnames or business domains.
- [ ] No passwords, tokens, API keys, private keys, kubeconfig contents, or database URLs.
- [ ] No real machine inventory or raw oplog/incident logs.
- [ ] All examples use placeholders such as `<ENV>`, `<KUBECONFIG_PATH>`, `<NAMESPACE>`, `<COMPONENT_NAME>`.
- [ ] `python3 scripts/sanitize_check.py .` passes.
- [ ] `make check` passes, including `publish-guard` to ensure private local files are not tracked.
- [ ] README explains the local-first boundary and non-goals.
- [ ] Auto discovery writes `env-map.generated.yaml` only; humans review before promotion.
- [ ] High-risk execution is disabled by default.
- [x] `SECURITY.md` exists.
- [x] LICENSE is selected by the owner (MIT).
- [ ] `templates/approval-request-template.json` validates with `python3 -m json.tool`.
- [ ] BestNative read-only file contract is documented in `docs/bestnative-contract.md`.

## Manual review points

The scanner is intentionally conservative but not perfect. Before publishing, manually review:

- `config/`
- `examples/`
- `docs/`
- `templates/`
- `scripts/`
- `CHANGELOG.d/`

## Do not publish

- `config/env-map.local.yaml`
- `config/env-map.generated.yaml` from a real environment
- `reports/`
- `.backup/`
- credential files (`*.pw`, `*.key`, `*.pem`, `.env`)
