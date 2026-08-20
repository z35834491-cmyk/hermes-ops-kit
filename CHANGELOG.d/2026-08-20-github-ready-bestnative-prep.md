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
