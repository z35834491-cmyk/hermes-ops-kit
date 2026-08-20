.PHONY: check sanitize inspect-check health-check onboard-check compile-check publish-guard git-status env-map-check render-check plan-check unit-test

check: compile-check publish-guard sanitize env-map-check unit-test inspect-check plan-check render-check onboard-check health-check
	git diff --check

compile-check:
	python3 -m py_compile scripts/*.py

publish-guard:
	! git ls-files | grep -E '(^|/)(env-map\.local\.yaml|env-map\.generated\.yaml|\.env|reports/|\.backup/|.*\.pw|.*\.pem|.*\.key)$$'

sanitize:
	python3 scripts/sanitize_check.py .

env-map-check:
	python3 scripts/validate_env_map.py config/env-map.example.yaml --expect-env test

unit-test:
	python3 -m unittest discover -s tests -v

inspect-check:
	python3 -m json.tool templates/inspection-result-template.json >/dev/null
	python3 -m json.tool templates/approval-request-template.json >/dev/null
	python3 -m json.tool examples/inspection-result.example.json >/dev/null
	python3 scripts/inspect.py test --config config/env-map.example.yaml --json --save --reports-dir /tmp/hermes-ops-kit-check >/tmp/hermes-ops-kit-inspect.json
	latest=$$(ls -t /tmp/hermes-ops-kit-check/test/inspection-*.json | head -1); python3 scripts/validate_inspection.py "$$latest" >/tmp/hermes-ops-kit-inspect-validate.txt

plan-check:
	python3 scripts/inspect.py test --config config/env-map.example.yaml --catalog config/check-catalog.yaml --plan --json >/tmp/hermes-ops-kit-plan.json
	python3 -m json.tool /tmp/hermes-ops-kit-plan.json >/dev/null
	python3 scripts/validate_inspection.py /tmp/hermes-ops-kit-plan.json --no-failed

render-check:
	python3 scripts/render_summary.py examples/inspection-result.example.json --only-abnormal >/tmp/hermes-ops-kit-summary.txt
	test -s /tmp/hermes-ops-kit-summary.txt

onboard-check:
	python3 scripts/onboard.py --env demo --output /tmp/hermes-ops-kit-generated.yaml --force >/tmp/hermes-ops-kit-onboard.txt
	test -s /tmp/hermes-ops-kit-generated.yaml

git-status:
	git status --short

health-check:
	python3 scripts/hermes_local_health_check.py --ops-kit .
