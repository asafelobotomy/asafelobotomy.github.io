#!/usr/bin/env bash
# Copy cursorAssistant install page artifacts into this github.io repo.
# Run from repo root after cloning cursorassistant, or let CI do it.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEST="${ROOT}/cursorassistant/install"
REF="${CURSOR_ASSISTANT_REF:-master}"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

git clone --depth 1 --branch "$REF" https://github.com/asafelobotomy/cursorassistant.git "$TMP/repo"

mkdir -p "$DEST"
cp "$TMP/repo/install/index.html" "$DEST/"
cp "$TMP/repo/install/deeplinks.json" "$DEST/"
touch "$DEST/.nojekyll"

echo "Synced install page from asafelobotomy/cursorassistant@${REF} -> ${DEST}"
