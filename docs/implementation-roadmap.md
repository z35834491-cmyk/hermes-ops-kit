# Hermes Ops Kit → BestNative Implementation Roadmap

## North Star

Build a private-first AI SRE Runbook Platform by combining:

```text
Local Hermes   = real operational copilot and execution loop
Hermes Ops Kit = reusable/sanitized contracts, runbooks, schemas, safety rules
BestNative     = Web/API control plane for assets, inspection history, approval and audit
```

The end state is not “AI chat for ops”. The end state is a controlled SRE platform where AI can diagnose, propose, execute only after approval, verify, audit, and feed lessons back into runbooks.

## Non-negotiable boundaries

1. Local Hermes remains private and may contain real environment knowledge.
2. Hermes Ops Kit remains sanitized and template-oriented.
3. BestNative consumes Ops Kit contracts; it does not redefine them.
4. Discovery output is candidate-only until human review.
5. L2/L3 operations require approval, rollback plan, and audit.
6. PRD defaults to command-generation mode unless hard RBAC/audit exists.
7. Public examples never contain real IPs, hostnames, credentials, raw logs, or business names.

## Current baseline

Current repository status: `v0.4-preview`.

Completed:

- Project README / LICENSE / SECURITY / CONTRIBUTING
- `make check` as a repository-only gate
- GitHub Actions check workflow
- sanitize scanner + publish guard
- env-map / inspection / runbook / approval schemas
- check catalog, inspect dispatcher, `--plan`
- public checkers remain plan-only (no default kubectl/SSH/DB calls)
- env-map validator and inspection JSON validator
- inspection summary renderer
- onboarding candidate skeleton
- optional local Hermes health-check template
- sanitized runbook examples
- end-to-end example flow
- BestNative read-only contract documentation
- `future-product/` planning docs

Not complete:

- Additional sanitized runbook examples listed in Phase 2
- Real read-only discovery (private overlay)
- BestNative adapter implementation
- Approval/audit database state machine
- Controlled execution

---

## Phase 1 — v0.4: Env-map driven read-only inspection framework

Goal: Move from pure skeleton to a pluggable read-only inspection framework without embedding private environment facts.

### Deliverables

- `config/check-catalog.yaml`
- `scripts/checkers/base.py`
- `scripts/checkers/k8s.py`
- `scripts/checkers/mysql.py`
- `scripts/checkers/redis.py`
- `scripts/checkers/rabbitmq.py`
- `scripts/checkers/elasticsearch.py`
- `scripts/inspect.py` dispatches checks from `env-map.local.yaml` + check catalog
- `docs/checker-development.md`
- More sanitized runbook examples

### Acceptance criteria

- `make check` passes.
- `inspect.py --plan` shows what would be checked without touching infrastructure.
- Public template does not connect to K8s/SSH/DB, including when `--execute-readonly` is set.
- Private users can replace checkers in an overlay; unit tests may inject a fake runner.
- Output still conforms to `inspection-result.schema.yaml`.
- Inspect skips `inspection.exclude` and checks whose catalog component is `mode=disabled`.
- Dispatched checks include `duration_seconds`.
- `validate_env_map.py --catalog` rejects include/exclude ids missing from the check catalog.
- Empty `inspection.include` does not expand to every catalog check.

### Anti-drift checks

- Do not copy real local `k8s-env-map/scripts/inspect.py` into this repo.
- Do not hardcode private IPs or hostnames.
- Do not add write/repair actions.

---

## Phase 2 — v0.5: GitHub-ready public template review

Goal: Prepare a clean public release candidate.

### Deliverables

- README polished for public readers
- More sanitized examples:
  - Redis health diagnostic (added)
  - Elasticsearch health/disk diagnostic (added)
  - Node memory high diagnostic
  - ArgoCD sync drift diagnostic
  - Longhorn PVC usage diagnostic
- `examples/private-checker-template.py`
- `docs/public-release-review.md`
- Manual sensitive-data review checklist completed

### Acceptance criteria

- `make check` passes locally and in GitHub Actions.
- No real environment data in `config/`, `docs/`, `examples/`, `templates/`, `scripts/`, `CHANGELOG.d/`.
- New user can clone and understand what is skeleton vs private implementation.
- Repository can safely be switched from private to public if desired.

### Anti-drift checks

- Do not market it as a complete ops platform yet.
- Do not imply public scripts perform real cluster checks.

---

## Phase 3 — BestNative Phase 1: Read-only Ops Kit adapter

Goal: Let BestNative consume Hermes Ops Kit outputs without execution capability.

### Deliverables in BestNative

- `backend/app/integrations/hermes_ops_kit/__init__.py`
- `backend/app/integrations/hermes_ops_kit/loader.py`
- `backend/app/integrations/hermes_ops_kit/schemas.py`
- API endpoints:
  - `GET /api/ops-kit/status`
  - `GET /api/ops-kit/inspection-runs`
  - `GET /api/ops-kit/runbooks`
  - `GET /api/ops-kit/schemas`
- UI pages/widgets:
  - Inspection history list
  - Runbook catalog list
  - Schema/contract status

### Acceptance criteria

- BestNative reads Ops Kit files from configured local path.
- BestNative does not mutate Ops Kit source files.
- No execution API is introduced.
- Missing/invalid Ops Kit path returns clear error.

### Anti-drift checks

- BestNative is consumer, not source of Ops Kit contracts.
- Do not copy and fork schema definitions into BestNative without version reference.

---

## Phase 4 — BestNative Phase 2: Approval and audit center

Goal: Implement the state layer needed before any controlled execution.

### Deliverables

- Database models / migrations:
  - `approval_requests`
  - `operation_audit`
  - `agent_tool_calls`
  - `safety_events`
- API endpoints:
  - create approval request
  - approve / reject / expire
  - list audit events
- UI:
  - Approval queue
  - Audit timeline

### Acceptance criteria

- L2/L3 operation cannot execute without approval id.
- Command-plan hash is stored.
- Changing command plan invalidates approval.
- Every execution result writes audit.

### Anti-drift checks

- Do not expose direct pod restart/rollback without approval.
- Do not store credentials in approval/audit records.

---

## Phase 5 — BestNative Phase 3: Controlled execution bridge

Goal: Allow approved low-risk operations to be executed through a controlled bridge.

### Deliverables

- Execution planner API
- Dry-run/plan mode for all actions
- Hermes Agent or worker execution bridge
- Post-change observation and verification hook
- Rollback reference display

### Acceptance criteria

- L0 remains read-only.
- L1/L2 require approval.
- L3 defaults to command-generation/manual mode.
- Post-change verification is recorded.

### Anti-drift checks

- No dangerous Web kubectl.
- No hidden background execution.
- No mobile high-risk execution without CLI-grade confirmation.

---

## Phase 6 — Feedback loop and platform metrics

Goal: Prove that the system improves SRE work over time.

### Metrics

- MTTR
- Runbook hit rate
- Repeat incident rate
- Approval coverage
- Audit coverage
- False diagnosis count
- Model escalation count
- Skill/runbook update rate

### Deliverables

- Metrics schema
- Weekly report page
- Recurrence detection
- Skill/runbook improvement suggestions

### Acceptance criteria

- Incident/runbook/audit data can produce trend reports.
- Repeated issues can be identified by fingerprint.
- Lessons can flow back into Ops Kit as sanitized templates.

---

## Decision points

Before moving from one phase to the next, answer:

1. Did `make check` pass?
2. Are private environment details still local only?
3. Are Ops Kit and BestNative responsibilities still separated?
4. Is execution still gated by approval/audit?
5. Is the next step still aligned with the North Star?

If any answer is “no”, stop and realign before coding.
