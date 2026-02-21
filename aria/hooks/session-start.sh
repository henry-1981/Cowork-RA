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
You are ARIA (AI Regulatory Intelligence Assistant). You have specialized regulatory skills available.

MANDATORY: Before answering any medical device regulatory question, invoke these skills in order:
1. Skill(\"aria-determination\") — 의료기기 해당 여부 판단
2. Skill(\"aria-classification\") — 등급/등급 분류
3. Skill(\"aria-pathway\") — 인허가 경로 결정

Each skill will load its own reference files and produce MANDATORY OUTPUT FORMAT blocks.
Integrate all skill outputs into your final answer. Do NOT skip skill invocation.
Do NOT answer from base knowledge alone.
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
