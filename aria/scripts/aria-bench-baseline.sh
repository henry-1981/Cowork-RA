#!/usr/bin/env bash
# ARIA Bench Baseline — bare Claude sonnet without plugin or reference DB
set -euo pipefail

PROMPT="$1"

exec claude -p --model sonnet -- "$PROMPT"
