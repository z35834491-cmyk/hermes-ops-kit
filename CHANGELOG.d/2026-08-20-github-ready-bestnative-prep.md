# v0.3.0-prep GitHub-ready and BestNative preparation

Date: 2026-08-20
Scope: Hermes Ops Kit project evolution

## Source

This evolution abstracts the latest local Hermes improvements into the sanitized Hermes Ops Kit template:

- Local Hermes health-check script pattern
- Real `inspect.py` argument/help/lazy-loading lessons
- Memory/logging boundary correction
- Three-layer product boundary: Local Hermes → Hermes Ops Kit → BestNative

## Changes

- Added optional `argocd_sync` and `longhorn_health` K8s checkers to the catalog; Longhorn is disabled by default and should be included only when the environment uses Longhorn.
- K8s checker now supports tested read-only parsing for `high_restart` and `node_resource_top`.
- K8s checker now supports tested read-only parsing for `warning_events` and `pvc_status`.
- K8s checker now has tested private read-only implementations for nodes readiness and abnormal pods when `execute=True`; public plan mode remains non-executing.
- Added unit tests for K8s checker plan/no-execute behavior and parsing.
- Added `scripts/validate_inspection.py` for semantic inspection-result validation so plan mode cannot hide checker failures.
- Updated `scripts/inspect.py` with `--plan`, `--catalog`, and checker dispatching to produce plan-only results from env-map + check catalog.
- Added `config/check-catalog.yaml` and `scripts/checkers/` plugin skeletons for K8s/MySQL/Redis/RabbitMQ/Elasticsearch; public checkers still do not connect to real infrastructure.
- Added `docs/checker-development.md` for safe private read-only checker extensions.
- Added `docs/implementation-roadmap.md` to pin the phase plan, acceptance criteria, and anti-drift checks from Ops Kit to BestNative platform.
- Added `scripts/render_summary.py` to render inspection JSON as a concise terminal summary for CLI/BestNative mock usage.
- Added `scripts/validate_env_map.py` for dependency-free env-map structural validation.
- Updated `scripts/inspect.py` to read env-map names and include contract validation evidence without connecting to real infrastructure.
- Added `scripts/hermes_local_health_check.py` as a read-only reusable template.
- Updated `scripts/inspect.py` to expose a stricter public inspection contract:
  - fixed target choices
  - `schema_version`
  - safe help behavior
  - no real infrastructure connections in public template
- Updated `scripts/onboard.py` to generate `env-map.generated.yaml` candidate skeletons.
- Strengthened `scripts/sanitize_check.py` with line-level findings and more GitHub-ready checks.
- Added `Makefile` with `check`, `sanitize`, `inspect-check`, and `health-check` targets.
- Added project docs:
  - `docs/github-ready-checklist.md`
  - `docs/bestnative-integration.md`
  - `docs/local-hermes-to-ops-kit.md`
- Added `SECURITY.md` and `docs/bestnative-contract.md`.
- Added `templates/approval-request-template.json`.
- Strengthened `Makefile` with py_compile, onboard, and approval-template checks.
- Fixed README version residue and clarified v0.3-prep / v0.4 roadmap.
- Updated GitHub-ready checklist to reflect SECURITY.md and BestNative contract gates.
- Added `docs/end-to-end-example.md` and `examples/inspection-result.example.json` to show the env-map → inspection result → runbook → approval consumption flow.
- Added `examples/README.md` to document sanitized example data rules.
- Added `docs/clone-and-run.md`.
- Added GitHub Actions workflow `.github/workflows/check.yml` to run `make check` on push/PR.
- Rewrote README for first-upload readiness: positioning, clone-and-run, layout, checks, and BestNative direction.
- Added `LICENSE` (MIT).
- Added sanitized Runbook metadata examples for K8s abnormal pods, MySQL replication lag, and RabbitMQ stale queues.
- Adjusted `sanitize_check.py` to skip local private env-map/.env file contents while `publish-guard` ensures they are not tracked by Git.
- Added `publish-guard` to `Makefile` to block accidental tracking of local private config and credential-like files.

## Boundary

This is a Hermes Ops Kit project evolution record. It is not a local Hermes operational incident/change record.

No real env-map, IP address, hostname, kubeconfig, SSH key, credential value, cron job, BestNative code, or GitHub upload was used.

## Validation

Expected validation:

```bash
make check
python3 scripts/sanitize_check.py .
python3 scripts/onboard.py --env demo --output /tmp/hermes-ops-kit-generated.yaml --force
python3 scripts/inspect.py test --json --save --reports-dir /tmp/hermes-ops-kit-check
python3 scripts/hermes_local_health_check.py --ops-kit .
```
