# From Local Hermes to Hermes Ops Kit

This document defines how real local Hermes experience becomes a reusable, sanitized template.

## Source layers

1. Local Hermes skill / workflow improvement
2. Local operational digest / oplog / incident notes
3. User correction and stable preference
4. Verified scripts such as inspection or health-check utilities

## Transformation process

```text
real usage
→ identify reusable pattern
→ remove real IPs, hostnames, business names, credentials, raw logs
→ write a lesson-candidate YAML (or copy templates/lesson-candidate-template.yaml)
→ python3 scripts/precipitate.py --from <candidate> --output <name>.generated.yaml
→ human review, then promote into examples/runbooks/<name>.yaml
→ update CHANGELOG.md and CHANGELOG.d
→ run sanitize_check and make check
```

Public `precipitate.py` does not read `~/.hermes`. Hermes (or a private skill) must already emit sanitized candidate YAML. Details: [precipitation.md](precipitation.md).

## What can move into Ops Kit

- Workflow structure
- Schema contracts
- Runbook metadata format
- Safety gates
- Sanitized examples
- Script skeletons
- Validation tools

## What must stay local

- Real env-map
- Real kubeconfig paths if they reveal private topology
- SSH key names tied to private infra
- Credential values
- Raw incident logs
- Raw oplog entries
- Internal hostnames, IPs, and business domains

## Logging boundary

- Local Hermes operation: local digest / local ops docs.
- Hermes Ops Kit evolution: project `CHANGELOG.md` and `CHANGELOG.d/`.
- BestNative evolution: BestNative project log.
