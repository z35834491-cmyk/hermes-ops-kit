<p align="right">
  <a href="precipitation.md">简体中文</a> · <b>English</b>
</p>

# How lessons are deposited

Without a return path the kit stays a snapshot of the current examples. This repo supplies a **repeatable deposit contract**, not a scraper of your local Hermes chat.

Public `precipitate.py` does **not** read `~/.hermes`, oplogs, or raw logs, and it does not talk to a cluster. It also does not commit to Git or edit `check-catalog.yaml`. That would pull secrets into a publishable tree.

The living loop is:

```text
local Hermes finishes an incident
        ↓
you (or a private skill) write an already-sanitized lesson-candidate.yaml
        ↓
python3 scripts/precipitate.py --from ...   →  *.generated.yaml draft
        ↓
human review → promote to examples/runbooks/<name>.yaml
        ↓
make check / sanitize_check
```

Same rule as `onboard.py`: the script writes a **candidate**; a human promotes it.

## Run it once

1. Copy the template and strip IPs, hostnames, business names, passwords, and raw logs:

```bash
cp templates/lesson-candidate-template.yaml /tmp/lesson-candidate.yaml
```

See also `examples/lesson-candidate.example.yaml` and `config/schema/lesson-candidate.schema.yaml`.

2. Write a runbook draft (filename must be `*.generated.yaml`):

```bash
python3 scripts/precipitate.py \
  --from /tmp/lesson-candidate.yaml \
  --output /tmp/example-component-health-diagnostic.generated.yaml \
  --force
```

3. After the draft validates, **copy by hand** into the example catalog (do not commit `.generated.yaml`):

```bash
python3 scripts/validate_runbook.py /tmp/example-component-health-diagnostic.generated.yaml
# then, after review:
# cp ... examples/runbooks/<name>.yaml
```

Auto-drafts accept **L0 / read-only** only. Write L1+ change, rollback, and approval fields by hand.

## Hermes side (private)

Give local Hermes a prompt like this so it emits **candidate YAML**, not raw oplog into Git:

```text
From the incident just resolved, write a Hermes Ops Kit lesson-candidate YAML.
It must already be sanitized: no IPs, hostnames, business domains, passwords,
tokens, kubeconfig contents, or raw logs. Use placeholders such as <NAMESPACE>
and <COMPONENT>. risk_level must be L0 and mode must be read-only.
Follow hermes-ops-kit/templates/lesson-candidate-template.yaml.
Do not read or change production config outside ~/.hermes; do not edit
examples/runbooks/ directly.
```

A private overlay / Hermes skill can write that YAML outside this repo and then call `precipitate.py`. That layer does not belong in this tree.

## Done when

- The candidate passes `precipitate.py` and the draft passes `validate_runbook.py`
- The promoted runbook passes `make check`
- `sanitize_check.py` reports no private IPs or plaintext secrets
- New catalog checks are a separate human edit, not merged by this script

Sanitizing rules: [local-hermes-to-ops-kit.md](local-hermes-to-ops-kit.md).
