#!/usr/bin/env python3
"""Generate cursorassistant/install/index.html from template + upstream VERSION."""

from __future__ import annotations

import argparse
import base64
import json
import os
from pathlib import Path

REPO = "asafelobotomy/cursorassistant"
REPO_GIT = f"https://github.com/{REPO}.git"
SITE_ROOT = Path(__file__).resolve().parents[1]
INSTALL_DIR = SITE_ROOT / "cursorassistant" / "install"
TEMPLATE = INSTALL_DIR / "index.template.html"


def read_version(package_root: Path) -> str:
    text = (package_root / "VERSION").read_text(encoding="utf-8").strip()
    return text.splitlines()[0]


def mcp_install_deeplink(name: str, server: dict) -> str:
    payload = base64.b64encode(json.dumps(server, separators=(",", ":")).encode()).decode()
    return f"cursor://anysphere.cursor-deeplink/mcp/install?name={name}&config={payload}"


def combined_cursor_assistant_mcp(version: str) -> dict:
    base = "${userHome}/.local/share/cursorassistant"
    ver_dir = f"{base}/v{version}"
    current = f"{base}/current"
    launch = f"{current}/mcp/scripts/mcp-launch.sh"
    inner = (
        f'if [ ! -f "{launch}" ]; then '
        f'mkdir -p "{base}" && '
        f'git clone --depth 1 --branch "v{version}" "{REPO_GIT}" "{ver_dir}" && '
        f'ln -sfn "{ver_dir}" "{current}"; '
        f"fi; "
        f'exec bash "{launch}"'
    )
    return {"command": "bash", "args": ["-lc", inner]}


def cursor_tools_mcp() -> dict:
    launch = "${userHome}/.local/share/cursorassistant/current/mcp/scripts/mcp-launch.sh"
    return {"command": "bash", "args": ["-lc", f'exec bash "{launch}"']}


def package_blurb(package_root: Path, version: str) -> str:
    catalog_path = package_root / "template/setup/catalog.json"
    if catalog_path.is_file():
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        agents = len(catalog.get("agents", []))
        skills = len(catalog.get("skills", []))
        packs = len(catalog.get("packs", []))
        return (
            f"Release v{version} installs {agents} subagents and {skills} core skills "
            f"(+ {packs} optional packs in the interview)."
        )
    return f"Release v{version} installs managed agents, skills, and rules via the project interview."


def mcp_preview_text(version: str) -> str:
    tag = f"v{version}"
    ver_dir = f"${{userHome}}/.local/share/cursorassistant/{version}"
    return (
        f"git clone --depth 1 --branch {tag} {REPO_GIT} → {ver_dir}\n"
        f"ln -sfn …/cursorassistant/{version} → …/cursorassistant/current\n"
        f"exec …/current/mcp/scripts/mcp-launch.sh"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--package-root",
        type=Path,
        default=None,
        help="cursorAssistant package checkout (or set CURSOR_ASSISTANT_PACKAGE_ROOT)",
    )
    args = parser.parse_args()
    package_root = args.package_root
    if package_root is None:
        env = os.environ.get("CURSOR_ASSISTANT_PACKAGE_ROOT")
        if not env:
            raise SystemExit("Set --package-root or CURSOR_ASSISTANT_PACKAGE_ROOT")
        package_root = Path(env)
    package_root = package_root.resolve()
    if not (package_root / "VERSION").is_file():
        raise SystemExit(f"Not a cursorAssistant package: {package_root}")

    version = read_version(package_root)
    tag = f"v{version}"
    bootstrap_curl = (
        f"curl -fsSL https://raw.githubusercontent.com/{REPO}/{tag}/scripts/bootstrap-from-github.sh | bash"
    )
    bootstrap_git = (
        f'git clone --depth 1 --branch "{tag}" {REPO_GIT} '
        f'"$HOME/.local/share/cursorassistant/{version}"'
    )

    deeplinks = {
        "version": version,
        "bootstrapCurl": bootstrap_curl,
        "bootstrapGit": bootstrap_git,
        "mcpCombined": mcp_install_deeplink("cursorAssistant", combined_cursor_assistant_mcp(version)),
        "mcpCursorTools": mcp_install_deeplink("cursorTools", cursor_tools_mcp()),
    }

    INSTALL_DIR.mkdir(parents=True, exist_ok=True)
    (INSTALL_DIR / "deeplinks.json").write_text(
        json.dumps(deeplinks, indent=2) + "\n",
        encoding="utf-8",
    )

    if not TEMPLATE.is_file():
        raise SystemExit(f"Missing template: {TEMPLATE}")

    html = TEMPLATE.read_text(encoding="utf-8")
    for key, value in (
        ("@@VERSION@@", version),
        ("@@REPO@@", REPO),
        ("@@BOOTSTRAP_CURL@@", bootstrap_curl),
        ("@@BOOTSTRAP_GIT@@", bootstrap_git),
        ("@@MCP_COMBINED@@", deeplinks["mcpCombined"]),
        ("@@MCP_CURSOR_TOOLS@@", deeplinks["mcpCursorTools"]),
        ("@@MCP_PREVIEW@@", mcp_preview_text(version)),
        ("@@PACKAGE_BLURB@@", package_blurb(package_root, version)),
    ):
        html = html.replace(key, value)
    (INSTALL_DIR / "index.html").write_text(html, encoding="utf-8")
    print(f"Wrote {INSTALL_DIR / 'index.html'}")
    print(f"Wrote {INSTALL_DIR / 'deeplinks.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
