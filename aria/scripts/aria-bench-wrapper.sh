#!/usr/bin/env bash
# ARIA Bench Wrapper
# Prepends regulatory reference data to the user prompt before passing to claude -p
# This ensures ARIA has access to its domain knowledge even when Skill tool isn't invoked

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

# Read the reference document
REFERENCE="$(cat "${SCRIPT_DIR}/aria-reference.md")"

# The prompt is passed as the first argument by bench-run.sh
PROMPT="$1"

# Combine: reference + separator + original prompt
COMBINED="${REFERENCE}
${PROMPT}"

# Execute claude with the combined prompt
exec claude -p --model sonnet --plugin-dir "${PLUGIN_ROOT}" -- "${COMBINED}"
