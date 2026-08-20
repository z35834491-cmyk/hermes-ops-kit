# Hermes Ops Kit

Hermes Ops Kit is a local-first AI SRE Runbook template kit for Hermes Agent.

它不是一个在线运维平台，也不是你的真实环境备份；它是把巡检、Runbook、审批、审计、oplog、故障复盘和安全规则抽象成可复用模板的一套项目骨架。

Current stage: `v0.3-prep` — GitHub-ready preparation and BestNative read-only contract preparation.

## Layering

```text
Local Hermes   = private operational copilot, real env-map, real usage loop
Hermes Ops Kit = sanitized templates, schemas, scripts, safety rules, examples
BestNative     = future Web/API control plane for assets, inspection history, approval and audit
```

## What this kit provides

- `env-map` schema and example
- inspection result JSON/Markdown contract
- runbook metadata schema and examples
- approval/audit schema and request example
- sanitize scanner and publish guard
- local Hermes health-check template
- GitHub-ready checklist and security policy
- BestNative read-only integration contract

## What it does not do

- It does not store passwords, tokens, private keys, or kubeconfig contents.
- It does not auto-execute high-risk operations.
- It does not replace Prometheus, Elasticsearch, or Alertmanager.
- It does not provide a production Web UI.
- Public scripts do not connect to real Kubernetes, SSH, databases, or external services.

## Clone and run

```bash
git clone <REPO_URL> hermes-ops-kit
cd hermes-ops-kit
make check
```

Then create a private local env-map:

```bash
cp config/env-map.example.yaml config/env-map.local.yaml
# Fill paths, aliases, and credential sources only. Do not write credential values.
vim config/env-map.local.yaml
```

Run the inspection skeleton:

```bash
python3 scripts/inspect.py test --config config/env-map.local.yaml --json --save
```

Expected output:

```text
reports/test/inspection-<run_id>.json
reports/test/inspection-<run_id>.md
```

Generate an onboarding candidate:

```bash
python3 scripts/onboard.py --env test --output config/env-map.generated.yaml --force
```

`env-map.generated.yaml` is a candidate only. Review it manually before promotion.

More details: `docs/clone-and-run.md`.

End-to-end flow: `docs/end-to-end-example.md`.

## Repository layout

```text
config/
  env-map.example.yaml
  model-routing.example.yaml
  schema/
    env-map.schema.yaml
    inspection-result.schema.yaml
    runbook.schema.yaml
    approval.schema.yaml
scripts/
  inspect.py
  onboard.py
  sanitize_check.py
  validate_env_map.py
  hermes_local_health_check.py
templates/
  inspection-result-template.json
  runbook-metadata-template.yaml
  approval-request-template.json
  digest-jsonl-template.jsonl
examples/
  runbooks/
docs/
  clone-and-run.md
  end-to-end-example.md
  schema-index.md
  project-status.md
  github-ready-checklist.md
  bestnative-contract.md
  bestnative-integration.md
  local-hermes-to-ops-kit.md
SECURITY.md
LICENSE
Makefile
```

## Safety model

1. Real configuration stays local: `config/env-map.local.yaml`.
2. Auto-discovery writes `config/env-map.generated.yaml` only; humans review before promotion.
3. Read-only inspection does not require approval.
4. Modifying, sensitive, external-write, service-affecting, or irreversible operations require approval.
5. PRD defaults to command-generation mode unless hard RBAC, approval and audit exist.

## GitHub-ready checks

```bash
make check
```

`make check` runs:

- Python compile check
- publish guard for private local files
- sensitive-content scanner
- JSON template validation
- env-map lightweight validation
- inspection skeleton contract check
- onboarding skeleton contract check
- local Hermes health-check template
- `git diff --check`

Before publishing, also manually review:

- `config/`
- `docs/`
- `examples/`
- `templates/`
- `scripts/`
- `CHANGELOG.d/`

## BestNative integration direction

BestNative should consume Hermes Ops Kit as a contract/template provider:

```text
BestNative reads schemas/reports/runbook metadata
BestNative stores approval/audit state
BestNative does not mutate Ops Kit source files at runtime
BestNative does not directly execute L2/L3 operations before approval/audit exists
```

See:

- `docs/bestnative-contract.md`
- `docs/bestnative-integration.md`

## Roadmap

- `v0.3-prep`: GitHub-ready checks, health-check template, BestNative read-only contract
- `v0.4`: env-map-driven private read-only inspection + more sanitized cases
- `v0.5`: GitHub-ready public template review
- `v1.0`: BestNative read-only control-plane integration

## License

MIT
