# Merge Readiness Criteria

Do not physically merge Hermes Ops Kit and BestNative until these criteria are met.

## Ops Kit readiness

- [ ] `make check` passes.
- [ ] env-map loader is stable.
- [ ] check-catalog loader is stable.
- [ ] inspection-result schema is stable enough for UI consumption.
- [ ] runbook metadata schema is stable enough for a catalog page.
- [ ] approval/audit schema is stable enough for approval center design.
- [ ] public examples are fully sanitized.
- [ ] real environment details remain local only.

## BestNative readiness

- [ ] BestNative has an Ops Kit adapter path, e.g. `backend/app/integrations/hermes_ops_kit/`.
- [ ] Adapter is read-only.
- [ ] Adapter can read check catalog, runbooks and inspection results.
- [ ] BestNative does not mutate Ops Kit files at runtime.
- [ ] Existing direct execution endpoints are disabled or converted to plan/approval flow.
- [ ] RBAC model is defined.
- [ ] Approval and audit data models are defined.

## Security readiness

- [ ] L2/L3 actions require approval id.
- [ ] command-plan hash is stored and enforced.
- [ ] execution results write audit.
- [ ] credential values are never stored in Ops Kit or BestNative DB.
- [ ] PRD defaults to command-generation/manual mode.

## Merge options

### Option A: Keep separate repositories

BestNative consumes Ops Kit via configured local path:

```text
HERMES_OPS_KIT_PATH=/path/to/hermes-ops-kit
```

This is safest during early development.

### Option B: Submodule or subtree

BestNative vendors Ops Kit contracts under:

```text
integrations/hermes-ops-kit/
```

Use only after contracts stabilize.

### Option C: Monorepo merge

Only consider after the platform is stable and release boundaries are clear.

## Stop conditions

Stop and realign if:

- BestNative starts redefining Ops Kit schemas independently.
- Ops Kit starts storing real environment facts.
- Any execution path bypasses approval/audit.
- Longhorn or any optional component becomes a default assumption.
- The project starts becoming a generic AIOps dashboard instead of an AI SRE Runbook Platform.
