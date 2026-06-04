#!/usr/bin/env python3
"""Regenerate install page and fail if artifacts drift (CI)."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

SITE_ROOT = Path(__file__).resolve().parents[1]
INSTALL = SITE_ROOT / "cursorassistant" / "install"


def main() -> int:
    package_root = os.environ.get("CURSOR_ASSISTANT_PACKAGE_ROOT")
    if not package_root:
        print("check_cursorassistant_install: skip — no CURSOR_ASSISTANT_PACKAGE_ROOT", file=sys.stderr)
        return 0

    gen = SITE_ROOT / "scripts" / "generate_cursorassistant_install.py"
    subprocess.run(
        [sys.executable, str(gen), "--package-root", package_root],
        cwd=SITE_ROOT,
        check=True,
    )

    version = Path(package_root).joinpath("VERSION").read_text(encoding="utf-8").strip().splitlines()[0]
    html = (INSTALL / "index.html").read_text(encoding="utf-8")
    deeplinks = (INSTALL / "deeplinks.json").read_text(encoding="utf-8")
    issues: list[str] = []
    if f"Version <strong>{version}</strong>" not in html:
        issues.append(f"index.html missing version {version}")
    if f'"version": "{version}"' not in deeplinks:
        issues.append("deeplinks.json version mismatch")
    if "v0.12." in html or "v0.12." in deeplinks:
        issues.append("stale v0.12.x reference")

    diff = subprocess.run(
        ["git", "diff", "--", "cursorassistant/install/index.html", "cursorassistant/install/deeplinks.json"],
        cwd=SITE_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if diff.stdout.strip():
        issues.append("install artifacts out of date — run scripts/sync-cursorassistant-install.sh")

    if issues:
        for item in issues:
            print(f"check_cursorassistant_install: {item}", file=sys.stderr)
        return 1
    print(f"check_cursorassistant_install: ok (v{version})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
