# Schema Index

Hermes Ops Kit schemas define contracts that local Hermes, scripts, and future BestNative adapters can consume.

## Schemas

| Schema | Purpose | Consumer |
|---|---|---|
| `config/schema/env-map.schema.yaml` | Describes environments, credential sources, components, inspection targets and risk defaults | onboard, inspect, BestNative asset view |
| `config/schema/inspection-result.schema.yaml` | Describes inspection run JSON output | inspection history UI, reporting, recurrence detection |
| `config/schema/runbook.schema.yaml` | Describes runbook metadata | runbook catalog, agent selection, UI detail page |
| `config/schema/approval.schema.yaml` | Describes approval request and operation audit objects | approval center, audit center, controlled execution |

## Contract principles

- Schema files are reusable contracts, not real environment state.
- Local/private values stay in `env-map.local.yaml` and are not committed.
- Generated discovery output is a candidate and must be reviewed before promotion.
- BestNative should consume these contracts through adapters, not redefine them.

## Versioning

Current schema version: `0.2`.

Breaking schema changes should update:

- schema file
- templates
- examples
- `docs/bestnative-contract.md`
- `CHANGELOG.md` and `CHANGELOG.d/`
