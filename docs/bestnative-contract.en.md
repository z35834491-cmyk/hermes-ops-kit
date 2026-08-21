<p align="right">
  <a href="bestnative-contract.md">简体中文</a> · <b>English</b>
</p>

# BestNative contract

BestNative Phase 1 **reads** Hermes Ops Kit files only. No execution, no credential storage, no mutation of kit sources.

```text
HERMES_OPS_KIT_PATH=/path/to/hermes-ops-kit
```

Merge conditions: [../future-product/merge-readiness.md](../future-product/merge-readiness.md). Do not merge repositories yet.

| Path | Purpose | Notes |
|---|---|---|
| `config/check-catalog.yaml` | checks and checker names | inspect + catalog UI |
| `config/schema/env-map.schema.yaml` | env-map shape | contract doc, not a JSON Schema engine |
| `config/schema/inspection-result.schema.yaml` | inspection JSON | history UI |
| `config/schema/runbook.schema.yaml` | runbook metadata | catalog page |
| `config/schema/approval.schema.yaml` | approval and audit | before execution exists |
| `examples/runbooks/*.yaml` | sanitized L0 examples | catalog UI |
| `templates/runbook-metadata-template.yaml` | empty template | when adding a runbook |
| `reports/<env>/inspection-*.json` | inspection history | **local-only; do not publish** |
| `config/env-map.local.yaml` | real env-map | **local-only, not in Git** |
| `CHANGELOG.md` + `CHANGELOG.d/` | project timeline | not an ops oplog |

Schema files are human-readable YAML contracts. Follow this repo's `schema_version`. Full inspection example: [../examples/inspection-result.example.json](../examples/inspection-result.example.json).

`target` may be `all` or any env-map name. `checks[].env` distinguishes duplicate ids when `target=all`.

Mapping checks to runbooks today: runbook `name` in `suggestion` and `examples/runbooks/<name>.yaml`. There is not yet a `related_checks` field.

Approval lifecycle: `pending → approved | rejected | expired → executed | cancelled`. L2/L3 needs an approval id. Changing commands invalidates `commands_hash`. Execution writes `operation_audit`.

Phase 1 non-goals: no kubectl execution, no credential storage, no auto-promotion of discovery, no PRD direct execution.
