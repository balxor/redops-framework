#!/usr/bin/env python3
"""Validate all committed JSON in the repo.

- schemas/*.json and package.json must be strict JSON.
- tsconfig*.json may contain comments/trailing commas (JSONC), which TypeScript
  permits; those are normalised before parsing.

Dependency and build directories are skipped. Exits non-zero on any failure so
it can gate CI.
"""
from __future__ import annotations

import json
import os
import re
import sys

SKIP_DIRS = {".git", "node_modules", ".venv", "dist", ".pytest_cache", "__pycache__"}


def strip_jsonc(text: str) -> str:
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    text = re.sub(r"(^|[^:])//.*", lambda m: m.group(1), text)
    text = re.sub(r",(\s*[}\]])", r"\1", text)
    return text


def main() -> int:
    failures: list[str] = []
    checked = 0
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files:
            if not name.endswith(".json"):
                continue
            path = os.path.join(root, name)
            raw = open(path, encoding="utf-8").read()
            text = strip_jsonc(raw) if name.startswith("tsconfig") else raw
            checked += 1
            try:
                json.loads(text)
            except json.JSONDecodeError as exc:
                failures.append(f"{path}: {exc}")

    print(f"Checked {checked} JSON file(s).")
    if failures:
        print("\nInvalid JSON:")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("All JSON files are valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
