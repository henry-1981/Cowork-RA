#!/usr/bin/env bash
# SessionStart hook for ARIA plugin
# Injects skill activation context to guarantee skill invocation in -p mode

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
PLUGIN_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

escape_for_json() {
    local s="$1"
    s="${s//\\/\\\\}"
    s="${s//\"/\\\"}"
    s="${s//$'\n'/\\n}"
    s="${s//$'\r'/\\r}"
    s="${s//$'\t'/\\t}"
    printf '%s' "$s"
}

activation_context="<ARIA_SKILL_ACTIVATION>
You are ARIA (AI Regulatory Intelligence Assistant).

If Skill tools are available, call them before writing your answer:
1. Skill(skill=\"aria-determination\")
2. Skill(skill=\"aria-classification\")
3. Skill(skill=\"aria-pathway\")

If a Skill's reference data conflicts with your training data, the Skill's data is AUTHORITATIVE.
</ARIA_SKILL_ACTIVATION>"

context_escaped=$(escape_for_json "$activation_context")

cat <<EOF
{
  "additional_context": "${context_escaped}",
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "${context_escaped}"
  }
}
EOF

exit 0
