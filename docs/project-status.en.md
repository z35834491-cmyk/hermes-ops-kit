<p align="right">
  <a href="project-status.md">简体中文</a> · <b>English</b>
</p>

# Project status

Current status: **`v0.4-preview`**

Hermes Ops Kit is a sanitized template/contract kit. It is **not** a Hermes feature branch, not a live copilot, and not a BestNative deployment.

Product: [product.en.md](product.en.md).

## Completed

- Local-first repository layout
- README / LICENSE / SECURITY / CONTRIBUTING (Chinese and English files)
- `make check` as a repository-only gate
- GitHub Actions check workflow
- Sanitize scanner and publish guard
- env-map / inspection / runbook / approval schemas
- Check catalog and inspect dispatcher; public checkers stay plan-only
- Inspection JSON fields aligned (`schema_version`, `mode`, `summary.skipped`, `checks[].env`, `duration_seconds`)
- Env-map loader honors exclude and `mode=disabled`; empty include does not expand to all checks
- Validators, summary renderer, onboard candidate skeleton
- Sanitized lesson-candidate → `precipitate.py` L0 runbook draft (does not read local Hermes)
- Optional local Hermes health-check template (not a gate)
- BestNative read-only contract and handoff docs
- Sanitized L0 runbook examples
- `future-product/` planning docs
- Public-release human review procedure
- `inspect.py` accepts any env-map name; `--save` notices go to stderr

## Not yet complete

- Real read-only discovery (private overlay)
- BestNative adapter (separate codebase)
- Approval/audit state machine (BestNative)
- Owner still must run [public-release-review.md](public-release-review.md) before making the repo public

## Next milestone

Run the public-release review before considering `v0.5`. Keep public checkers plan-only. See [implementation-roadmap.md](implementation-roadmap.md).
