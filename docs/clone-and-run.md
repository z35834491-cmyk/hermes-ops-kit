# Clone and Run

This guide shows what happens after someone clones Hermes Ops Kit locally.

## 1. Clone

```bash
git clone <REPO_URL> hermes-ops-kit
cd hermes-ops-kit
```

## 2. Run the public template checks

```bash
make check
```

This verifies:

- Python scripts compile
- no tracked private env-map / credential-like files
- sensitive-content scan passes
- JSON templates are valid
- inspection skeleton can generate JSON/Markdown
- onboarding skeleton can generate an env-map candidate
- local Hermes health-check template can run in read-only mode

## 3. Create a private local env-map

```bash
cp config/env-map.example.yaml config/env-map.local.yaml
```

Edit `config/env-map.local.yaml` and fill only local paths, aliases, and credential sources.

Do not put credential values in this file.

## 4. Run the inspection skeleton

```bash
python3 scripts/validate_env_map.py config/env-map.local.yaml --expect-env test
python3 scripts/inspect.py test --config config/env-map.local.yaml --json --save
```

The public template does not connect to Kubernetes, SSH, databases, or external services. It only demonstrates the output contract.

Expected local output:

```text
reports/test/inspection-<run_id>.json
reports/test/inspection-<run_id>.md
```

## 5. Generate an onboarding candidate

```bash
python3 scripts/onboard.py --env test --output config/env-map.generated.yaml --force
```

The generated file is a candidate only. Review it manually before copying anything into `env-map.local.yaml`.

## 6. Optional: run local Hermes health check

```bash
python3 scripts/hermes_local_health_check.py --ops-kit .
```

It is read-only and does not read `.env`, private keys, kubeconfig contents, or credential values.

## Current limitation

This repository is currently a template/contract kit. Real environment discovery and real inspection checks must be implemented privately and safely on top of the schemas.
