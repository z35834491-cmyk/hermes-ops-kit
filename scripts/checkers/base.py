from __future__ import annotations

from typing import Any


class CheckResult:
    def __init__(self, id: str, component: str, status: str, severity: str, title: str, evidence: str, suggestion: str = "", duration_seconds: float = 0.0):
        self.id = id
        self.component = component
        self.status = status
        self.severity = severity
        self.title = title
        self.evidence = evidence
        self.suggestion = suggestion
        self.duration_seconds = duration_seconds

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "component": self.component,
            "status": self.status,
            "severity": self.severity,
            "title": self.title,
            "evidence": self.evidence,
            "suggestion": self.suggestion,
            "duration_seconds": self.duration_seconds,
        }


def plan_result(check_id: str, component: str, title: str, env: str, detail: str) -> CheckResult:
    return CheckResult(
        id=check_id,
        component=component,
        status="skipped",
        severity="info",
        title=title,
        evidence=f"plan-only: env={env}; {detail}",
        suggestion="Implement a private read-only checker or run with an approved private adapter.",
    )
