# Private Checker Guide

This guide explains how to attach real read-only checks to Hermes Ops Kit without leaking private environment details into the public template.

## Goal

Keep the public repository generic while allowing private deployments to run real checks.

```text
public repo     = contracts, skeletons, sanitized examples
private overlay = real env-map.local.yaml, real checker implementations, credential sources
```

## Recommended private layout

Do not edit public checker files directly for private environment details. Create a private overlay outside the repo:

```text
~/hermes-ops-private/
  env-map.local.yaml
  checkers/
    k8s_private.py
    mysql_private.py
  creds/
    <credential files>
```

Then wire the private checker through your own wrapper or future adapter.

## Checker contract

A checker function must return `CheckResult`:

```python
def run(check_id, env, env_config, catalog_entry, execute=False, runner=None):
    ...
    return CheckResult(...)
```

Required output fields:

- `id`
- `component`
- `status`: `ok|warning|critical|unreachable|failed|skipped`
- `severity`: `info|warning|critical`
- `title`
- `evidence`
- `suggestion`

## Safety rules

- Read-only only.
- No delete/restart/scale/patch/apply/edit.
- No external writes.
- Do not print credential values.
- Do not store real IPs or hostnames in public examples.
- If a checker needs credentials, read from a credential source and only report whether it exists.

## Example: K8s read-only checker

See:

```text
examples/private-checker-template.py
```

## Promotion rule

If a private checker becomes generally useful:

1. Remove real IPs, hostnames, namespaces, service names and credential paths.
2. Convert it into a generic checker or sanitized example.
3. Add tests using simulated command output.
4. Run `make check`.
5. Update `CHANGELOG.md` and `CHANGELOG.d/`.
