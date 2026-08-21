from __future__ import annotations

import pathlib
import re


class Environment:
    def __init__(
        self,
        name: str,
        kubeconfig: str = "",
        inspection_include: list[str] | None = None,
        inspection_exclude: list[str] | None = None,
        disabled_components: dict[str, str] | None = None,
        has_inspection_include: bool = False,
        raw_block: str = "",
    ):
        self.name = name
        self.kubeconfig = kubeconfig
        self.inspection_include = inspection_include or []
        self.inspection_exclude = inspection_exclude or []
        self.disabled_components = disabled_components or {}
        self.has_inspection_include = has_inspection_include
        self.raw_block = raw_block


class EnvMap:
    def __init__(self, path: str, environments: dict[str, Environment]):
        self.path = path
        self.environments = environments


def read_text(path: str) -> str:
    return pathlib.Path(path).read_text(encoding="utf-8", errors="replace")


def extract_environment_names(text: str) -> list[str]:
    names: list[str] = []
    in_envs = False
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith("environments:"):
            in_envs = True
            continue
        if in_envs:
            if line and not line.startswith(" ") and not line.startswith("\t"):
                break
            match = re.match(r"^\s{2}([A-Za-z0-9_-]+):\s*$", line)
            if match:
                names.append(match.group(1))
    return names


def _env_block(text: str, env: str) -> str:
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if re.match(rf"^\s{{2}}{re.escape(env)}:\s*$", line):
            start = i
            break
    if start is None:
        return ""
    block: list[str] = []
    for line in lines[start + 1 :]:
        if re.match(r"^\s{2}[A-Za-z0-9_-]+:\s*$", line):
            break
        block.append(line)
    return "\n".join(block)


def _extract_kubeconfig(block: str) -> str:
    match = re.search(r"^\s{4}kubeconfig:\s*[\"']?([^\"'\n]+)", block, re.M)
    return match.group(1).strip() if match else ""


def _extract_inspection_list(block: str, key: str) -> tuple[list[str], bool]:
    items: list[str] = []
    in_list = False
    found = False
    header = re.compile(rf"^\s{{6}}{re.escape(key)}:\s*$")
    inline_empty = re.compile(rf"^\s{{6}}{re.escape(key)}:\s*\[\s*\]\s*$")
    for line in block.splitlines():
        if inline_empty.match(line):
            return [], True
        if header.match(line):
            found = True
            in_list = True
            continue
        if in_list:
            if re.match(r"^\s{6}[A-Za-z0-9_-]+:", line):
                break
            match = re.match(r"^\s{8}-\s*([A-Za-z0-9_-]+)\s*$", line)
            if match:
                items.append(match.group(1))
    return items, found


def _strip_yaml_scalar(value: str) -> str:
    return value.strip().strip("\"'")


def _extract_disabled_components(block: str) -> dict[str, str]:
    disabled: dict[str, str] = {}
    pending_reason: dict[str, str] = {}
    in_components = False
    current: str | None = None
    for line in block.splitlines():
        if re.match(r"^\s{4}components:\s*$", line):
            in_components = True
            current = None
            continue
        if not in_components:
            continue
        if re.match(r"^\s{4}[A-Za-z0-9_-]+:", line) and not line.startswith("      "):
            break
        match = re.match(r"^\s{6}([A-Za-z0-9_-]+):\s*$", line)
        if match:
            current = match.group(1)
            continue
        if current is None:
            continue
        mode = re.match(r"^\s{8}mode:\s*[\"']?([A-Za-z0-9_-]+)", line)
        if mode and mode.group(1) == "disabled":
            disabled[current] = pending_reason.get(current, disabled.get(current, ""))
        reason = re.match(r"^\s{8}disabled_reason:\s*(.+)$", line)
        if reason:
            text = _strip_yaml_scalar(reason.group(1))
            if current in disabled:
                disabled[current] = text
            else:
                pending_reason[current] = text
    return disabled


def load_env_map(path: str) -> EnvMap:
    text = read_text(path)
    envs: dict[str, Environment] = {}
    for name in extract_environment_names(text):
        block = _env_block(text, name)
        include, has_include = _extract_inspection_list(block, "include")
        exclude, _has_exclude = _extract_inspection_list(block, "exclude")
        envs[name] = Environment(
            name=name,
            kubeconfig=_extract_kubeconfig(block),
            inspection_include=include,
            inspection_exclude=exclude,
            disabled_components=_extract_disabled_components(block),
            has_inspection_include=has_include,
            raw_block=block,
        )
    return EnvMap(path=path, environments=envs)


def get_environment(env_map: EnvMap, name: str) -> Environment | None:
    return env_map.environments.get(name)
