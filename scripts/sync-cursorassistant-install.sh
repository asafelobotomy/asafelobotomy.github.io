#!/usr/bin/env bash
# Clone cursorAssistant, regenerate install page into this github.io repo.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REF="${CURSOR_ASSISTANT_REF:-master}"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

git clone --depth 1 --branch "$REF" https://github.com/asafelobotomy/cursorassistant.git "$TMP/repo"

export CURSOR_ASSISTANT_PACKAGE_ROOT="$TMP/repo"
python3 "$ROOT/scripts/generate_cursorassistant_install.py" --package-root "$TMP/repo"
touch "$ROOT/cursorassistant/install/.nojekyll"

echo "Generated cursorassistant/install from asafelobotomy/cursorassistant@${REF}"
