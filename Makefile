.PHONY: check sanitize inspect-check health-check onboard-check compile-check publish-guard git-status

check: compile-check publish-guard sanitize inspect-check onboard-check health-check
	git diff --check

compile-check:
	python3 -m py_compile scripts/*.py

publish-guard:
	! git ls-files | grep -E '(^|/)(env-map\.local\.yaml|env-map\.generated\.yaml|\.env|reports/|\.backup/|.*\.pw|.*\.pem|.*\.key)$$'

sanitize:
	python3 scripts/sanitize_check.py .

inspect-check:
	python3 -m json.tool templates/inspection-result-template.json >/dev/null
	python3 -m json.tool templates/approval-request-template.json >/dev/null
	python3 scripts/inspect.py test --config config/env-map.example.yaml --json --save --reports-dir /tmp/hermes-ops-kit-check >/tmp/hermes-ops-kit-inspect.json

onboard-check:
	python3 scripts/onboard.py --env demo --output /tmp/hermes-ops-kit-generated.yaml --force >/tmp/hermes-ops-kit-onboard.txt
	test -s /tmp/hermes-ops-kit-generated.yaml

git-status:
	git status --short

health-check:
	python3 scripts/hermes_local_health_check.py --ops-kit .
