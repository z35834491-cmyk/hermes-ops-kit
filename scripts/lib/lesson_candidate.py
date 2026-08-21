"""Load and validate sanitized lesson candidates for precipitate.py."""
from __future__ import annotations

import pathlib
import re

CATEGORIES = {"k8s", "mysql", "redis", "rabbitmq", "es", "longhorn", "network", "cicd", "prd"}
SECRETISH = re.compile(
    r"(?i)(\b(10|192\.168|172\.(?:1[6-9]|2[0-9]|3[0-1]))\.\d+\.\d+\b"
    r"|-----BEGIN (?:RSA |OPENSSH |EC |)PRIVATE KEY-----"
    r"|\b(password|token|api[_-]?key)\s*[:=]\s*\S{8,})"
)
PLACEHOLDER = re.compile(r"^<[^>]+>$")


class LessonCandidateError(ValueError):
    pass


def yaml_quote(value: str) -> str:
    escaped = str(value).replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def parse_candidate(text: str) -> dict:
    result: dict = {}
    current_list: str | None = None
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        top = re.match(r"^([A-Za-z0-9_]+):\s*(.*)$", line)
        if top and not line.startswith(" "):
            key = top.group(1)
            value = top.group(2).strip().strip("\"'")
            if value == "":
                result[key] = []
                current_list = key
            else:
                result[key] = value
                current_list = None
            continue
        item = re.match(r"^\s+-\s+(.*)$", line)
        if item and current_list:
            result[current_list].append(item.group(1).strip().strip("\"'"))
    return result


def validate_candidate(data: dict, raw_text: str) -> list[str]:
    errors: list[str] = []
    for field in ("name", "title", "category", "lesson", "verification"):
        if not data.get(field):
            errors.append(f"missing required field: {field}")
    name = str(data.get("name", ""))
    if name and ("<" in name or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name)):
        errors.append(f"name must be lowercase-with-hyphens: {name}")
    category = data.get("category")
    if category and category not in CATEGORIES:
        errors.append(f"invalid category: {category}")
    risk = str(data.get("risk_level") or "L0")
    if risk != "L0":
        errors.append("auto-drafts must be risk_level L0; write L1+ runbooks by hand")
    mode = str(data.get("mode") or "read-only")
    if mode != "read-only":
        errors.append("auto-drafts must be mode read-only")
    lesson = str(data.get("lesson", "")).strip()
    if lesson and (PLACEHOLDER.fullmatch(lesson) or lesson.startswith("<One sanitized")):
        errors.append("lesson is still a placeholder")
    if SECRETISH.search(raw_text):
        errors.append("candidate looks unsanitized (private IP, password assignment, or private key)")
    verification = data.get("verification")
    if isinstance(verification, list) and not verification:
        errors.append("missing required field: verification")
    return errors


def load_lesson_candidate(path: pathlib.Path) -> dict:
    text = path.read_text(encoding="utf-8")
    data = parse_candidate(text)
    errors = validate_candidate(data, text)
    if errors:
        raise LessonCandidateError("; ".join(errors))
    data.setdefault("risk_level", "L0")
    data.setdefault("mode", "read-only")
    data.setdefault("prechecks", ["Verify env exists in env-map."])
    data.setdefault("execution", ["Run only read-only checks.", "Do not mutate the workload."])
    if not isinstance(data.get("prechecks"), list):
        data["prechecks"] = [str(data["prechecks"])]
    if not isinstance(data.get("execution"), list):
        data["execution"] = [str(data["execution"])]
    if not isinstance(data.get("verification"), list):
        data["verification"] = [str(data["verification"])]
    return data


def _yaml_list(items: list[str]) -> str:
    lines = []
    for item in items:
        text = str(item).strip()
        if ":" in text or text.startswith(("{", "[", "<", '"')):
            lines.append(f"  - {yaml_quote(text)}")
        else:
            lines.append(f"  - {text}")
    return "\n".join(lines)


def render_runbook_draft(candidate: dict) -> str:
    name = candidate["name"]
    related = str(candidate.get("related_check") or "").strip()
    if related and "<" in related:
        related = ""
    related_comment = f"# related_check: {related}\n" if related else ""
    execution = list(candidate["execution"]) + [candidate["lesson"]]
    return f"""# GENERATED RUNBOOK DRAFT
# review_required: true
# source: scripts/precipitate.py
# Do not commit this file. Promote into examples/runbooks/{name}.yaml after human review.
{related_comment}
name: {name}
title: {yaml_quote(candidate["title"])}
category: {candidate["category"]}
risk_level: L0
requires_approval: false
requires_backup: false
supports_env: [dev, test]
mode: read-only
related_skills: []
inputs:
  - name: env
    required: true
    description: Environment name from env-map.
prechecks:
{_yaml_list(candidate["prechecks"])}
execution:
{_yaml_list(execution)}
rollback: Not required for read-only mode.
verification:
{_yaml_list(candidate["verification"])}
outputs:
  - inspection_result
  - digest
"""
