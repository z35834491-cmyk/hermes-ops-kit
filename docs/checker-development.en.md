<p align="right">
  <a href="checker-development.md">简体中文</a> · <b>English</b>
</p>

# Checker development

Hermes Ops Kit checkers are small plugins that produce `CheckResult` objects.

Public checkers must stay safe: no Kubernetes API, SSH, database, credential-value reads, or write/repair actions. `inspect.py` already skips `inspection.exclude` and `mode=disabled` components. The public `run()` must not call kubectl/SSH/DB unless a test or private overlay injects a `runner`.

Files live under `scripts/checkers/`. Each checker exposes `run(...) -> CheckResult`.

To add a check: catalog entry, `SUPPORTED` set, `CheckResult`, optional sanitized runbook, `make check`.

L0 read-only may run without approval. Writes, restarts, deletes, scale, patch, or external writes are not checkers.
