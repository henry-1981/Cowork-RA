#!/usr/bin/env bash
# ARIA Bench Skills-only — plugin loaded with Skill tool allowed, NO reference DB prepend
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

PROMPT="$1"

exec claude -p --model sonnet \
  --plugin-dir "${PLUGIN_ROOT}" \
  --allowedTools "Skill,Read,Grep,Glob" \
  -- "$PROMPT"
