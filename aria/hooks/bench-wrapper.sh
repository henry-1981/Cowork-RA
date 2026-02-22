#!/usr/bin/env bash
# bench-wrapper.sh — Wrapper for ARIA bench execution
# Prepends skill invocation instruction to the user prompt
# so it's treated as part of the user message (highest priority)
# rather than additionalContext (lower priority)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
PLUGIN_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

PROMPT="$1"

PREPEND="<ARIA_INSTRUCTION>
You have 3 specialized Skill tools available. You MUST call each one before writing your answer.

Step 1: Call Skill tool → Skill(skill=\"aria-determination\")
Step 2: Call Skill tool → Skill(skill=\"aria-classification\")
Step 3: Call Skill tool → Skill(skill=\"aria-pathway\")

After all 3 Skill calls complete, integrate their outputs into your final answer.
Do NOT generate answers from pre-training knowledge. Use the Skill tools.
</ARIA_INSTRUCTION>

"

FULL_PROMPT="${PREPEND}${PROMPT}"

exec claude -p --model sonnet --plugin-dir "$PLUGIN_DIR" -- "$FULL_PROMPT"
