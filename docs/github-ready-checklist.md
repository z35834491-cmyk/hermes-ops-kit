# GitHub-ready Checklist

Hermes Ops Kit can be published only after the template is detached from the author's private environment.

## Required gates

- [x] No real private IP addresses (scanner + this review of tracked files).
- [x] No internal hostnames or business domains in tracked examples.
- [x] No passwords, tokens, API keys, private keys, kubeconfig contents, or database URLs.
- [x] No real machine inventory or raw oplog/incident logs.
- [x] Examples use placeholders such as `<ENV>`, `<KUBECONFIG_PATH>`, `<NAMESPACE>`, `<COMPONENT_NAME>`.
- [x] `python3 scripts/sanitize_check.py .` passes.
- [x] `make check` passes, including `publish-guard` to ensure private local files are not tracked.
- [x] GitHub Actions workflow exists and runs `make check`.
- [x] README explains the local-first boundary and non-goals.
- [x] Auto discovery writes `env-map.generated.yaml` only; humans review before promotion.
- [x] High-risk execution is disabled by default. Public checkers do not invoke kubectl/SSH/DB.
- [x] `SECURITY.md` exists.
- [x] LICENSE is selected by the owner (MIT).
- [x] `templates/approval-request-template.json` validates with `python3 -m json.tool`.
- [x] BestNative read-only file contract is documented in `docs/bestnative-contract.md`.

## Manual review points

The scanner is intentionally conservative but not perfect. Before publishing, follow [`public-release-review.md`](public-release-review.md) and manually review:

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
