from __future__ import annotations

import pathlib
import re


class Environment:
    def __init__(self, name: str, kubeconfig: str = "", inspection_include: list[str] | None = None, raw_block: str = ""):
        self.name = name
        self.kubeconfig = kubeconfig
        self.inspection_include = inspection_include or []
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


def _extract_inspection_include(block: str) -> list[str]:
    include: list[str] = []
    in_include = False
    for line in block.splitlines():
        if re.match(r"^\s{6}include:\s*$", line):
            in_include = True
            continue
        if in_include:
            if re.match(r"^\s{6}[A-Za-z0-9_-]+:", line):
                break
            match = re.match(r"^\s{8}-\s*([A-Za-z0-9_-]+)\s*$", line)
            if match:
                include.append(match.group(1))
    return include


def load_env_map(path: str) -> EnvMap:
    text = read_text(path)
    envs: dict[str, Environment] = {}
    for name in extract_environment_names(text):
        block = _env_block(text, name)
        envs[name] = Environment(
            name=name,
            kubeconfig=_extract_kubeconfig(block),
            inspection_include=_extract_inspection_include(block),
            raw_block=block,
        )
    return EnvMap(path=path, environments=envs)


def get_environment(env_map: EnvMap, name: str) -> Environment | None:
    return env_map.environments.get(name)
