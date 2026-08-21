<p align="right">
  <a href="bestnative-integration.md">简体中文</a> · <b>English</b>
</p>

# How BestNative will connect

**Build BestNative as a separate repository first, then have it read this kit. Do not put the adapter or approval state machine in Ops Kit.**

This kit (`v0.4-preview`) already provides contracts. What is missing is BestNative itself: UI, API, database, RBAC.

```text
now: local Hermes + Ops Kit contracts
next: new BestNative repo, phase 1 read-only
then: BestNative approval/audit
last: bridge to Hermes execution after approval
```

| Order | Where | What |
|---|---|---|
| 1 (current) | **This Ops Kit repo** | Stable catalog, inspection JSON, runbook, approval schema |
| 2 (next) | **New BestNative repo** | Minimal Web/API, **no execution** |
| 3 | BestNative | Adapter: read-only `HERMES_OPS_KIT_PATH` |
| 4 | BestNative | Approval queue + audit store |
| 5 | BestNative + local Hermes | Controlled execution only with an approval id |

Do not merge repositories until [../future-product/merge-readiness.md](../future-product/merge-readiness.md). Separate repos plus a local path is safest early on.

Readable files: [bestnative-contract.en.md](bestnative-contract.en.md). Phase breakdown: [implementation-roadmap.md](implementation-roadmap.md) Phases 3–5.

Runtime paths:

```text
HERMES_OPS_KIT_PATH=/path/to/hermes-ops-kit
HERMES_OPS_REPORTS_DIR=/path/to/reports
HERMES_OPS_ENV_MAP=/path/to/env-map.local.yaml
```

BestNative **reads** these files. It must not mutate kit sources or fork schemas.

**Phase 1** (BestNative repo): load catalog, `examples/runbooks/*.yaml`, local reports, schemas. Suggested GETs only. No `POST /execute`, no Web kubectl, no passwords in the BestNative DB.

**Phase 2**: approval and audit tables from `approval.schema.yaml`. No L2/L3 without an approval id.

**Phase 3**: after RBAC, command hashing, and rollback, hand approved plans to local Hermes. Write `operation_audit`. PRD still defaults to commands only.

Do not invert this: no execution bridge before an approval center exists.
