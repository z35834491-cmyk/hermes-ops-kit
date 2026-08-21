# v0.4.0-preview inspection framework close-out

Date: 2026-08-21
Scope: Hermes Ops Kit public/private boundary and inspection contract

## Summary

Closed the v0.4 inspection framework without adding new live infrastructure checks.

## Changes

- Removed the public kubectl default runner from `scripts/checkers/k8s.py`.
- Kept K8s output parsers for injected-runner unit tests.
- Aligned inspection-result schema/template/example/validator fields.
- `inspect.py all` now sets `checks[].env`; missing config exits non-zero.
- `onboard.py` include list matches the check catalog.
- Dropped catalog-missing include ids from `config/env-map.example.yaml`.
- Removed unused parsers from `scripts/inspect.py`.
- `make check` no longer depends on `make health-check`.

## Boundary

No real kubeconfig, credential file, or local Hermes home was modified.
This is an Ops Kit contract/template change only.
