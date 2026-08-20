# BestNative Integration Plan

BestNative is the third-stage platform shell. Do not connect it to real execution before Hermes Ops Kit schemas and safety boundaries are stable.

## Responsibility split

```text
Local Hermes   = private operational copilot, real environment knowledge, real usage loop
Hermes Ops Kit = sanitized template, schemas, runbook metadata, safety rules, examples
BestNative     = Web/API control plane for assets, inspection history, approval, audit
```

## Phase 1: read-only control plane

BestNative should first read:

- `config/env-map.local.yaml` or a sanitized generated copy
- `reports/<env>/inspection-*.json`
- `templates/runbook-metadata-template.yaml` and future runbook metadata files
- `config/schema/*.schema.yaml`
- project changelog and docs

No execution endpoint in this phase.

## Phase 2: approval and audit objects

Add storage/API for:

- `approval_requests`
- `operation_audit`
- `agent_tool_calls`
- `safety_events`
- `incident_timeline`

Rules:

- No approval id, no L2/L3 execution.
- Command plan changes invalidate approval.
- Execution result must write audit.
- PRD defaults to command-generation mode.

## Phase 3: controlled execution

Only after RBAC, audit, command hashing, and rollback plans exist:

- L0 read-only queries
- L1 low-risk changes after approval
- L2/L3 changes after explicit approval and backup/rollback checks

## Anti-goals

- Do not build a dangerous Web kubectl.
- Do not store credentials in BestNative database.
- Do not auto-promote discovery output to official env-map.
