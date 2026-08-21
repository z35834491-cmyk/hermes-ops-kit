# Lesson-candidate precipitation (v0.4-preview)

Date: 2026-08-21
Scope: candidate-only deposit of sanitized L0 lessons

## Summary

Added a precipitation contract so incidents can return to the kit without scraping `~/.hermes`.

## Changes

- `scripts/precipitate.py` turns a sanitized lesson-candidate into a `*.generated.yaml` runbook draft.
- Schema / template / example for lesson candidates; auto-drafts are L0 read-only only.
- Docs: `docs/precipitation.md` and English twin.
- `make check` runs `precipitate-check`; generated files stay out of Git.

## Boundary

Public precipitate does not read `~/.hermes`, oplog, or live infrastructure.
Drafts are not auto-promoted into `examples/runbooks/` or `check-catalog.yaml`.
