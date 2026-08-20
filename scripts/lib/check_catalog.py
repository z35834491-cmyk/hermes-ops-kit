from __future__ import annotations

import pathlib
import re


class CheckDefinition:
    def __init__(self, name: str, settings: dict[str, str]):
        self.name = name
        self.settings = settings
        self.component = settings.get("component", "")
        self.risk_level = settings.get("risk_level", "")
        self.mode = settings.get("mode", "")
        self.requires_approval = settings.get("requires_approval", "false").lower() == "true"
        self.checker = settings.get("checker", "")
        self.title = settings.get("title", name)


class CheckCatalog:
    def __init__(self, path: str, checks: dict[str, CheckDefinition]):
        self.path = path
        self.checks = checks


def read_text(path: str) -> str:
    return pathlib.Path(path).read_text(encoding="utf-8", errors="replace")


def parse_check_catalog_text(text: str) -> dict[str, CheckDefinition]:
    checks: dict[str, CheckDefinition] = {}
    current: str | None = None
    in_checks = False
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith("checks:"):
            in_checks = True
            continue
        if not in_checks:
            continue
        match = re.match(r"^\s{2}([A-Za-z0-9_-]+):\s*$", line)
        if match:
            current = match.group(1)
            checks[current] = CheckDefinition(current, {})
            continue
        if current is not None:
            kv = re.match(r"^\s{4}([A-Za-z0-9_-]+):\s*(.+?)\s*$", line)
            if kv:
                current_name = str(current)
                key = kv.group(1)
                value = kv.group(2).strip().strip('"\'')
                checks[current_name].settings[key] = value
                # refresh derived attributes
                checks[current_name] = CheckDefinition(current_name, checks[current_name].settings)
    return checks


def load_check_catalog(path: str) -> CheckCatalog:
    return CheckCatalog(path=path, checks=parse_check_catalog_text(read_text(path)))


def get_check(catalog: CheckCatalog, name: str) -> CheckDefinition | None:
    return catalog.checks.get(name)
