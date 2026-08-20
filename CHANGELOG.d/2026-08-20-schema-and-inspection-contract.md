# v0.2.0 schema and inspection contract

Date: 2026-08-20
Scope: Hermes Ops Kit project evolution

## Summary

Optimized Hermes Ops Kit for current standalone Hermes usage before any BestNative integration work.

## Changes

- Added schema contracts under `config/schema/`:
  - `env-map.schema.yaml`
  - `inspection-result.schema.yaml`
  - `runbook.schema.yaml`
  - `approval.schema.yaml`
- Added structured templates:
  - `templates/runbook-metadata-template.yaml`
  - `templates/runbook-metadata-template.md`
  - `templates/inspection-result-template.json`
  - `templates/digest-jsonl-template.jsonl`
- Upgraded `scripts/inspect.py` from a print-only skeleton to a safe JSON/Markdown output contract skeleton.
- Updated `config/env-map.example.yaml` with version, discovery output, disabled components, risk fields, and credential-source examples.
- Rewrote `README.md` to clarify local-first usage, standalone Hermes priority, and BestNative as a later control plane.
- Added `.gitignore` to keep local env maps, generated maps, reports, backups, and credential-like files out of Git.
- Updated `CHANGELOG.md` with v0.2.0 notes.

## Validation

Commands run:

```bash
python3 scripts/inspect.py test --config config/env-map.example.yaml --json --save --reports-dir /tmp/hermes-ops-kit-reports
python3 scripts/sanitize_check.py .
git diff --check
python3 -m json.tool templates/inspection-result-template.json
python3 scripts/inspect.py dev --json --save --reports-dir /tmp/hermes-ops-kit-reports2
```

Results:

- Inspection skeleton generated JSON and Markdown reports successfully.
- Sensitive-content scan passed: no obvious sensitive content found.
- `git diff --check` passed.
- JSON template parsed successfully.
- Inspect JSON contract assertion passed.

## Boundary

This project log belongs to Hermes Ops Kit. It is not a local Hermes operational incident/change record.

No real kubeconfig, SSH key, credential file, real environment topology, cron job, BestNative code, or GitHub upload was modified.
