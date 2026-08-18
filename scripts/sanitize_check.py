#!/usr/bin/env python3
"""Basic sensitive pattern scanner skeleton."""
import argparse
import pathlib
import re

PATTERNS = [
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"-----BEGIN (RSA |OPENSSH |EC |)PRIVATE KEY-----"),
    # 只拦截疑似明文赋值，不拦截 password_key / secret name 这类配置字段
    re.compile(r"(?i)\\b(password|token|api[_-]?key)\\s*[:=]\\s*['\"]?[A-Za-z0-9_./+=-]{12,}"),
    re.compile(r"\b(?:10|192\.168|172\.(?:1[6-9]|2[0-9]|3[0-1]))\.\d+\.\d+\b"),
]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("path", nargs="?", default=".")
    args = p.parse_args()
    root = pathlib.Path(args.path)
    hits = []
    for f in root.rglob("*"):
        if not f.is_file() or any(part.startswith(".git") for part in f.parts):
            continue
        try:
            text = f.read_text(errors="ignore")
        except Exception:
            continue
        for pat in PATTERNS:
            if pat.search(text):
                hits.append(str(f))
                break
    if hits:
        print("Potential sensitive content found:")
        for h in hits:
            print("-", h)
        raise SystemExit(1)
    print("No obvious sensitive content found.")


if __name__ == "__main__":
    main()
