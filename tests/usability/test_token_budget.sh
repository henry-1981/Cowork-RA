#!/bin/bash
# Measure ARIA token consumption for a simple regulatory query
# Expected: captures response length as proxy for token cost
set -euo pipefail

PLUGIN_DIR="$(cd "$(dirname "$0")/../.." && pwd)/aria"
QUERY="혈압 측정 앱을 개발 중입니다. 의료기기에 해당하나요?"

echo "=== ARIA Token Budget Test ==="
echo "Query: $QUERY"

RESPONSE=$(printf "%s" "$QUERY" | claude -p --model sonnet --plugin-dir "$PLUGIN_DIR" 2>/dev/null)
RESPONSE_LEN=${#RESPONSE}

echo "Response length (chars): $RESPONSE_LEN"
echo "---"

# Check for auto-chain indicators
DETERMINATION=$(echo "$RESPONSE" | grep -c "determination\|Determination\|해당 여부" || true)
CLASSIFICATION=$(echo "$RESPONSE" | grep -c "classification\|Classification\|등급" || true)
PATHWAY=$(echo "$RESPONSE" | grep -c "pathway\|Pathway\|경로\|510(k)\|인증\|허가" || true)

echo "Skills auto-triggered:"
echo "  determination: $DETERMINATION"
echo "  classification: $CLASSIFICATION"
echo "  pathway: $PATHWAY"

# Check for user confirmation gate
ASKS_USER=$(echo "$RESPONSE" | grep -c "하시겠습니까\|원하시나요\|확인해\|알려주세요\|어떤\|할까요" || true)
echo "  asks user before proceeding: $ASKS_USER"

# Verdict
if [ "$CLASSIFICATION" -gt 0 ] && [ "$PATHWAY" -gt 0 ] && [ "$ASKS_USER" -eq 0 ]; then
  echo ""
  echo "FAIL: Auto-chained all 3 skills without user confirmation"
  exit 1
elif [ "$RESPONSE_LEN" -gt 8000 ]; then
  echo ""
  echo "WARN: Response exceeds 8000 chars (likely full-chain output)"
  exit 1
else
  echo ""
  echo "PASS: Progressive disclosure respected"
  exit 0
fi
