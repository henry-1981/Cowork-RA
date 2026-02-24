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

if [ "${ARIA_BATCH_MODE:-0}" = "1" ]; then
  activation_context="${activation_context}\n\n<ARIA_BATCH_MODE>\nBenchmark batch mode is enabled.\n- Do NOT ask follow-up questions.\n- Do NOT return conversational checkback requests.\n- Return structured output in one shot.\n- If critical information is missing, return structured insufficiency fields instead of questions:\n  - \"insufficient\": true\n  - \"missing_fields\": [..]\n  - \"reason\": \"...\"\n  - \"next_required_inputs\": [..]\n- If the user prompt requests JSON-only, output JSON only.\n</ARIA_BATCH_MODE>"
fi

# Knowledge DB refresh check
KNOWLEDGE_DIR="$(dirname "$0")/../knowledge/regulations"
if [ -d "$KNOWLEDGE_DIR" ]; then
  TODAY=$(date +%Y-%m-%d)
  REFRESH_DUE=""
  for f in "$KNOWLEDGE_DIR"/*.md; do
    NEXT_REVIEW=$(head -10 "$f" | grep "next_review" | sed 's/.*"\(.*\)".*/\1/' || true)
    if [ -n "$NEXT_REVIEW" ] && [[ "$TODAY" > "$NEXT_REVIEW" ]]; then
      REFRESH_DUE="true"
      break
    fi
  done
  if [ "$REFRESH_DUE" = "true" ]; then
    activation_context="${activation_context}\n\n⚠️ Knowledge DB 갱신이 필요합니다. /aria-knowledge-refresh를 실행하세요."
  fi
fi

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
