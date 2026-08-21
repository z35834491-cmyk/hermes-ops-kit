<p align="right">
  <a href="architecture.md">简体中文</a> · <b>English</b>
</p>

# Architecture

This repository is a **contract layer beside Hermes**, not a Hermes feature branch and not BestNative.

Product: [product.en.md](product.en.md).

## Three layers

Keep separate:

```text
Local Hermes   = private copilot; real env-map and real actions (not this repo)
Hermes Ops Kit = this repo: sanitized templates, schemas, plan-only scripts
BestNative     = separate control plane: assets, history, approval, audit (not built)
```

```mermaid
flowchart LR
  subgraph L["1. Local Hermes"]
    H["runtime copilot<br/>not this repo"]
  end
  subgraph K["2. Hermes Ops Kit"]
    T["this repo · contracts/templates"]
  end
  subgraph B["3. BestNative"]
    P["separate repo · future read-only"]
  end
  H -.->|sanitized experience| T
  T -.->|read-only contracts| P
```

A private overlay for real checks stays next to Hermes; do not commit it here.

```mermaid
flowchart TB
  Hermes["Local Hermes Agent<br/>runtime copilot · not this repo"]
  Kit["Hermes Ops Kit<br/>this repo · templates/contracts"]
  Overlay["private overlay<br/>real read-only checks"]
  BN["BestNative<br/>separate repo · future read-only"]
  Infra["real cluster / middleware"]
  Hermes -->|"reads contracts"| Kit
  Overlay -->|"implements the same contracts"| Kit
  Hermes --> Overlay --> Infra
  Kit -.->|"schema / catalog / inspection JSON / runbooks"| BN
```

This repository does not run a live agent against real infrastructure. The public side does not connect to Kubernetes, SSH, or databases. `--execute-readonly` stays skipped without a private overlay.

## Inspection path now

```mermaid
flowchart TD
  EM["env-map.local.yaml"] --> IN["scripts/inspect.py"]
  CAT["check-catalog.yaml"] --> IN
  IN --> FLT["skip exclude and disabled components"]
  FLT --> CHK["public checkers: plan / skipped"]
  CHK --> OUT["inspection JSON + Markdown"]
  OUT --> VAL["validate_inspection.py"]
```

## Core layers

- **env-map**: environment facts and credential sources (paths/aliases, never values)
- **check catalog**: checks, risk level, checker module
- **scripts**: dispatch, validate, sanitize, onboard candidate
- **runbook metadata**: read-only diagnostic procedure contract
- **docs / future-product**: docs and end-state planning

## Roadmap

1. v0.1: local templates, manual trigger
2. v0.2: schema contract + inspection JSON/Markdown skeleton
3. v0.3-prep: GitHub gates, BestNative read-only contract
4. **v0.4-preview (current)**: env-map + catalog read-only inspection framework
5. v0.5: public-release human review via [public-release-review.md](public-release-review.md)
6. v1.0: BestNative read-only control plane (separate codebase)

Details: [implementation-roadmap.md](implementation-roadmap.md). Vision: [../future-product/](../future-product/README.md) — planning only.
