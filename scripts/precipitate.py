#!/usr/bin/env python3
"""Turn a sanitized lesson candidate into a runbook draft.

Public/template behavior:
- Does not read local Hermes directories, oplog, or raw incident logs.
- Does not connect to Kubernetes, SSH, databases, or external services.
- Input must already be sanitized YAML matching the lesson-candidate schema.
- Output is a candidate runbook; humans review before promoting to examples/runbooks/.
- Auto-drafts are L0 read-only only.
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

from lib.lesson_candidate import LessonCandidateError, load_lesson_candidate, render_runbook_draft


def parse_args(argv=None):
    p = argparse.ArgumentParser(description="Generate a runbook draft from a sanitized lesson candidate")
    p.add_argument("--from", dest="source", required=True, help="path to sanitized lesson-candidate YAML")
    p.add_argument(
        "--output",
        default="",
        help="output file path; default is <name>.generated.yaml next to the candidate or in --output-dir",
    )
    p.add_argument("--output-dir", default="", help="directory for <name>.generated.yaml when --output is omitted")
    p.add_argument("--force", action="store_true", help="overwrite output if it exists")
    return p.parse_args(argv)


def default_output(source: pathlib.Path, name: str, output: str, output_dir: str) -> pathlib.Path:
    if output:
        return pathlib.Path(output)
    directory = pathlib.Path(output_dir) if output_dir else source.parent
    return directory / f"{name}.generated.yaml"


def main(argv=None) -> int:
    args = parse_args(argv)
    source = pathlib.Path(args.source)
    try:
        candidate = load_lesson_candidate(source)
        draft = render_runbook_draft(candidate)
    except (OSError, LessonCandidateError) as exc:
        print(f"error={exc}", file=sys.stderr)
        return 1
    out = default_output(source, candidate["name"], args.output, args.output_dir)
    if out.exists() and not args.force:
        print(f"Refusing to overwrite existing {out}. Re-run with --force after review.", file=sys.stderr)
        return 1
    if not re.search(r"\.generated\.ya?ml$", out.name):
        print("error=output filename must end with .generated.yaml so drafts are not mistaken for promoted runbooks", file=sys.stderr)
        return 1
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(draft, encoding="utf-8")
    print(f"generated={out}")
    print("review_required=true")
    print("note=draft only; do not auto-promote into examples/runbooks/ or check-catalog.yaml")
    print("note=public precipitate.py does not read local Hermes directories")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
