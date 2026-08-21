<p align="right">
  <a href="end-to-end-example.md">简体中文</a> · <b>English</b>
</p>

# End-to-end example

How env-map → inspection JSON → runbook → approval contracts fit together, without touching real infrastructure.

```text
env-map.example.yaml
  ↓
scripts/inspect.py --json --save
  ↓
reports/<env>/inspection-*.json
  ↓
runbook metadata selection
  ↓
approval request if risk >= L1
  ↓
BestNative read-only display / future approval center
```

```bash
cp config/env-map.example.yaml config/env-map.local.yaml
python3 scripts/inspect.py test --config config/env-map.local.yaml --json --save
```

`env-map.local.yaml` describes paths and credential sources, not values. Public inspect emits contract-shaped output only.

Example JSON: [../examples/inspection-result.example.json](../examples/inspection-result.example.json). A UI or agent maps `pod_abnormal` to `examples/runbooks/k8s-pod-abnormal-diagnostic.yaml`.

L0 runbooks do not need approval. L1+ uses `templates/approval-request-template.json`. BestNative should store approval state later; this kit only provides the contract.

Safety: discovery is a candidate; public inspection stays read-only until a private overlay adds safe checkers; execution needs approval/audit before platform integration; public examples stay sanitized.
