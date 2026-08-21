<p align="right">
  <a href="private-checker-guide.md">简体中文</a> · <b>English</b>
</p>

# Private Checker Guide

How to attach real read-only checks without leaking private environment details into the public template.

```text
public repo     = contracts, skeletons, sanitized examples
private overlay = real env-map.local.yaml, real checker implementations, credential sources
```

Do not edit public checker files for private topology. Overlay outside the repo:

```text
~/hermes-ops-private/
  env-map.local.yaml
  checkers/
    k8s_private.py
    mysql_private.py
  creds/
    <credential files>
```

A checker must return `CheckResult` from `run(check_id, env, env_config, catalog_entry, execute=False, runner=None)` with `id`, `component`, `status`, `severity`, `title`, `evidence`, `suggestion`.

Safety: read-only; no delete/restart/scale/patch/apply/edit; no external writes; no `shell=True`; do not print secrets; do not put real IPs/hostnames in public examples.

See `examples/private-checker-template.py`.

If a private checker becomes generally useful: strip real facts, add simulated-output tests, run `make check`, update CHANGELOG.
