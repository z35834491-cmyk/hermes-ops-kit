.PHONY: check sanitize inspect-check health-check onboard-check compile-check publish-guard git-status env-map-check runbook-check render-check plan-check unit-test

check: compile-check publish-guard sanitize env-map-check runbook-check unit-test inspect-check plan-check render-check onboard-check
	git diff --check

compile-check:
	python3 -m py_compile scripts/*.py scripts/lib/*.py scripts/checkers/*.py

publish-guard:
	! git ls-files | grep -E '(^|/)(env-map\.local\.yaml|env-map\.generated\.yaml|\.env|reports/|\.backup/|.*\.pw|.*\.pem|.*\.key)$$'

sanitize:
	python3 scripts/sanitize_check.py .

env-map-check:
	python3 scripts/validate_env_map.py config/env-map.example.yaml --expect-env test --catalog config/check-catalog.yaml

runbook-check:
	python3 scripts/validate_runbook.py examples/runbooks templates/runbook-metadata-template.yaml

unit-test:
	python3 -m unittest discover -s tests -v

inspect-check:
	python3 -m json.tool templates/inspection-result-template.json >/dev/null
	python3 -m json.tool templates/approval-request-template.json >/dev/null
	python3 -m json.tool examples/inspection-result.example.json >/dev/null
	python3 scripts/validate_inspection.py templates/inspection-result-template.json
	python3 scripts/validate_inspection.py examples/inspection-result.example.json
	python3 scripts/inspect.py test --config config/env-map.example.yaml --json --save --reports-dir /tmp/hermes-ops-kit-check >/tmp/hermes-ops-kit-inspect.json
	latest=$$(ls -t /tmp/hermes-ops-kit-check/test/inspection-*.json | head -1); python3 scripts/validate_inspection.py "$$latest"

plan-check:
	python3 scripts/inspect.py test --config config/env-map.example.yaml --catalog config/check-catalog.yaml --plan --json >/tmp/hermes-ops-kit-plan.json
	python3 -m json.tool /tmp/hermes-ops-kit-plan.json >/dev/null
	python3 scripts/validate_inspection.py /tmp/hermes-ops-kit-plan.json --no-failed --no-missing-catalog
	python3 scripts/inspect.py all --config config/env-map.example.yaml --catalog config/check-catalog.yaml --plan --json >/tmp/hermes-ops-kit-plan-all.json
	python3 scripts/validate_inspection.py /tmp/hermes-ops-kit-plan-all.json --no-failed --no-missing-catalog

render-check:
	python3 scripts/render_summary.py examples/inspection-result.example.json --only-abnormal >/tmp/hermes-ops-kit-summary.txt
	test -s /tmp/hermes-ops-kit-summary.txt

onboard-check:
	python3 scripts/onboard.py --env test --output /tmp/hermes-ops-kit-generated.yaml --force >/tmp/hermes-ops-kit-onboard.txt
	test -s /tmp/hermes-ops-kit-generated.yaml
	python3 scripts/inspect.py test --config /tmp/hermes-ops-kit-generated.yaml --catalog config/check-catalog.yaml --plan --json >/tmp/hermes-ops-kit-onboard-plan.json
	python3 scripts/validate_inspection.py /tmp/hermes-ops-kit-onboard-plan.json --no-failed --no-missing-catalog

git-status:
	git status --short

health-check:
	python3 scripts/hermes_local_health_check.py --ops-kit .
