#!/bin/bash
# Google Workspace MCP — 자동 배포
# 사용법: bash scripts/deploy.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
APPS_SCRIPT_DIR="$PROJECT_DIR/apps-script"
CLASP="npx -y @google/clasp"
OPEN_CMD="open"
command -v xdg-open &>/dev/null && OPEN_CMD="xdg-open"

echo ""
echo "  ARIA Google Workspace MCP — 자동 배포"
echo "  ─────────────────────────────────────"
echo ""

# --- Login ---
if $CLASP login --status 2>/dev/null | grep -q "You are logged in"; then
  echo "  ✓ Google 로그인 확인"
else
  echo "  → 브라우저에서 Google 로그인..."
  $CLASP login
fi

# --- Create or reuse project ---
cd "$APPS_SCRIPT_DIR"
if [ -f ".clasp.json" ]; then
  echo "  ✓ 기존 프로젝트 사용"
else
  echo "  → 프로젝트 생성 중..."
  if ! $CLASP create --type webapp --title "ARIA Google Workspace MCP" --rootDir . 2>/tmp/clasp-err.log; then
    if grep -qi "apps script api" /tmp/clasp-err.log 2>/dev/null; then
      echo ""
      echo "  ⚠ Apps Script API 활성화 필요"
      echo "    브라우저에서 토글을 켜주세요..."
      $OPEN_CMD "https://script.google.com/home/usersettings" 2>/dev/null || true
      read -rp "    → 완료 후 Enter "
      $CLASP create --type webapp --title "ARIA Google Workspace MCP" --rootDir .
    else
      cat /tmp/clasp-err.log
      exit 1
    fi
  fi
fi

# --- Push + Deploy ---
echo "  → 코드 업로드..."
$CLASP push --force 2>/dev/null
echo "  → 웹앱 배포..."
DEPLOY_OUTPUT=$($CLASP deploy --description "v$(date +%Y%m%d)" 2>&1)
DEPLOY_ID=$(echo "$DEPLOY_OUTPUT" | grep -oE 'AKfycb[a-zA-Z0-9_-]+' | head -1 || true)

if [ -n "$DEPLOY_ID" ]; then
  URL="https://script.google.com/macros/s/${DEPLOY_ID}/exec"
else
  URL=$(echo "$DEPLOY_OUTPUT" | grep -oE 'https://script\.google\.com/macros/s/[^[:space:]]+' | head -1 || true)
fi

# --- Save config ---
if [ -n "$URL" ]; then
  CONFIG_DIR="$HOME/.config/google-workspace-mcp"
  mkdir -p "$CONFIG_DIR"
  python3 -c "
import json, os
p = '$CONFIG_DIR/config.json'
c = json.load(open(p)) if os.path.exists(p) else {}
c['webAppUrl'] = '$URL'
json.dump(c, open(p,'w'), indent=2)
" 2>/dev/null || echo "{\"webAppUrl\": \"$URL\"}" > "$CONFIG_DIR/config.json"

  echo ""
  echo "  ✓ 배포 완료"
  echo ""
  echo "  URL: $URL"
  echo "  설정 저장: ~/.config/google-workspace-mcp/config.json"
  echo ""
else
  echo ""
  echo "  ⚠ URL 추출 실패. 수동 확인:"
  echo "  $DEPLOY_OUTPUT"
  echo ""
fi
