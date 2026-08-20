# Future Product Architecture

## Target architecture

```text
┌────────────────────────────────────────────┐
│                BestNative UI               │
│  Dashboard / Runbook / Approval / Audit    │
└────────────────────────────────────────────┘
                    │
                    ▼
┌────────────────────────────────────────────┐
│              BestNative Backend            │
│  API / RBAC / Approval / Audit / History   │
└────────────────────────────────────────────┘
                    │
                    ▼
┌────────────────────────────────────────────┐
│              Hermes Ops Kit                │
│  env-map / check catalog / runbook schema  │
│  inspection schema / approval schema       │
└────────────────────────────────────────────┘
                    │
                    ▼
┌────────────────────────────────────────────┐
│              Hermes Agent                  │
│  skill loading / reasoning / tool calling  │
│  diagnostics / command generation / execute│
└────────────────────────────────────────────┘
                    │
                    ▼
┌────────────────────────────────────────────┐
│       Real Infra: K8s / DB / MQ / ES       │
│       Prometheus / Logs / Cloud / CI       │
└────────────────────────────────────────────┘
```

## Responsibility split

### Local Hermes

- Real private usage.
- Real env-map and real operational knowledge.
- Skill loading, reasoning, tool calling.
- Execution after approval.
- Local digest/oplog/ops docs.

### Hermes Ops Kit

- Sanitized template and contract provider.
- env-map schema.
- check catalog.
- inspection result schema.
- runbook metadata schema.
- approval/audit schema.
- checker skeletons and private checker guidance.
- sanitize and publish guard.

### BestNative

- Platform implementation.
- Web UI and API.
- Asset and topology display.
- Inspection history.
- Runbook catalog.
- Approval center.
- Audit center.
- Incident timeline and metrics.

## Final product pages

- Dashboard
- Environment / Asset Map
- Inspection Center
- Runbook Center
- Approval Center
- Audit Center
- Incident Center
- Hermes Copilot
- Metrics / Feedback

## Key data objects

- Environment
- EnvMap
- CheckCatalog
- InspectionRun
- InspectionCheck
- Runbook
- ApprovalRequest
- OperationAudit
- Incident
- IncidentTimeline
- ToolCall
- SafetyEvent
- KnowledgeItem
