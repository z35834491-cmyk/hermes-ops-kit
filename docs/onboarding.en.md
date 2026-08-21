<p align="right">
  <a href="onboarding.md">简体中文</a> · <b>English</b>
</p>

# Onboarding

How to attach an environment. Public scripts do not scan a live cluster. Commands: [clone-and-run.en.md](clone-and-run.en.md).

1. Prepare a kubeconfig **path** or node-inventory alias (do not commit file contents)
2. Copy `config/env-map.example.yaml` → `config/env-map.local.yaml`
3. Fill env name, kubeconfig path, namespaces, credential **sources**, `inspection.include`
4. Unused middleware: `mode: disabled`, drop from include
5. `validate_env_map.py ... --catalog config/check-catalog.yaml`
6. Optional `onboard.py` writes a **draft** only; human review required
7. `inspect.py <env> --plan`, then `--save`
8. Map to `examples/runbooks/`; real read-only checks go in a private overlay

Public `onboard.py` does not connect to Kubernetes / SSH / DB and does not rewrite `env-map.local.yaml`. Future private discovery still produces drafts. Replica roles, purgeable queues, and production boundaries need a human.
