#!/usr/bin/env python3
"""Sensitive-content scanner for Hermes Ops Kit.

This is a conservative GitHub-ready preflight. It reports file, line, and pattern
kind. It is not a substitute for human review.
"""
from __future__ import annotations

import argparse
import pathlib
import re
from collections import namedtuple
SKIP_DIRS = {".git", ".backup", "reports", "__pycache__", ".venv", "venv", "node_modules"}
SKIP_SUFFIXES = {".pyc", ".png", ".jpg", ".jpeg", ".gif", ".ico", ".pdf", ".zip", ".gz"}
SKIP_FILENAMES = {"env-map.local.yaml", "env-map.generated.yaml", ".env"}
FORBIDDEN_FILENAMES = {}


Pattern = namedtuple("Pattern", "kind regex message")


PATTERNS = [
    Pattern("aws_access_key", re.compile(r"AKIA[0-9A-Z]{16}"), "possible AWS access key"),
    Pattern("private_key", re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC |)PRIVATE KEY-----"), "private key material"),
    Pattern("kubeconfig_user_token", re.compile(r"(?i)\b(client-key-data|client-certificate-data|certificate-authority-data|token):\s*[A-Za-z0-9+/=]{20,}"), "possible kubeconfig embedded secret"),
    Pattern("db_url_with_password", re.compile(r"[a-zA-Z][a-zA-Z0-9+.-]*://[^\s:@/]+:[^\s@/]+@"), "connection URL with password"),
    Pattern("secret_assignment", re.compile(r"(?i)\b(password|token|api[_-]?key|secret)\s*[:=]\s*['\"]?[A-Za-z0-9_./+=-]{16,}"), "possible plaintext secret assignment"),
    Pattern("private_ip", re.compile(r"\b(?:10|192\.168|172\.(?:1[6-9]|2[0-9]|3[0-1]))\.\d+\.\d+\b"), "private IP address"),
]

ALLOW_HINTS = [
    "<PRIVATE_IP>",
    "<KUBECONFIG_PATH>",
    "<CREDENTIAL_FILE_PATH>",
    "password_key",
    "username_key",
    "Path only",
    "do not store credential values",
]


def should_skip(path: pathlib.Path) -> bool:
    if any(part in SKIP_DIRS for part in path.parts):
        return True
    if path.name in SKIP_FILENAMES:
        return True
    if path.suffix.lower() in SKIP_SUFFIXES:
        return True
    return False


def allowed_line(line: str) -> bool:
    return any(hint in line for hint in ALLOW_HINTS)


def scan_file(path: pathlib.Path) -> list[tuple[int, str, str]]:
    hits = []
    if path.name in FORBIDDEN_FILENAMES:
        hits.append((0, "forbidden_filename", FORBIDDEN_FILENAMES[path.name]))
        return hits
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return hits
    for lineno, line in enumerate(text.splitlines(), 1):
        if allowed_line(line):
            continue
        for pat in PATTERNS:
            if pat.regex.search(line):
                hits.append((lineno, pat.kind, pat.message))
    return hits


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Scan for obvious sensitive content")
    parser.add_argument("path", nargs="?", default=".")
    args = parser.parse_args(argv)
    root = pathlib.Path(args.path)
    hits = []
    for f in root.rglob("*"):
        if not f.is_file() or should_skip(f):
            continue
        for lineno, kind, message in scan_file(f):
            hits.append((f, lineno, kind, message))

    if hits:
        print("Potential sensitive content found:")
        for f, lineno, kind, message in hits:
            loc = f"{f}:{lineno}" if lineno else str(f)
            print(f"- {loc} [{kind}] {message}")
        raise SystemExit(1)
    print("No obvious sensitive content found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
