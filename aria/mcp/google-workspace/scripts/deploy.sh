#!/bin/bash
# Google Workspace MCP — 원클릭 배포
#
# 사용법: bash scripts/deploy.sh
# 이 스크립트가 모든 것을 처리합니다.

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
APPS_SCRIPT_DIR="$PROJECT_DIR/apps-script"

# macOS: open, Linux: xdg-open
OPEN_CMD="open"
command -v xdg-open &>/dev/null && OPEN_CMD="xdg-open"

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║  ARIA Google Workspace MCP — 자동 배포   ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# --- Step 1: Apps Script API 활성화 ---
echo "[1/5] Apps Script API 활성화 확인"
echo "      브라우저에서 설정 페이지를 엽니다."
echo "      'Google Apps Script API'가 '사용'인지 확인해주세요."
echo ""
$OPEN_CMD "https://script.google.com/home/usersettings" 2>/dev/null || true
read -rp "      → 확인 완료 후 Enter ▶ "
echo ""

# --- Step 2: clasp 설치 확인 ---
echo "[2/5] clasp 확인 중..."
if ! npx @google/clasp --version &>/dev/null 2>&1; then
  echo "      clasp 설치 중..."
  npm install -g @google/clasp
fi
CLASP="npx @google/clasp"
echo "      clasp 준비 완료 ✓"
echo ""

# --- Step 3: Google 로그인 ---
echo "[3/5] Google 로그인"
if $CLASP login --status 2>/dev/null | grep -q "You are logged in"; then
  echo "      이미 로그인됨 ✓"
else
  echo "      브라우저에서 Google 로그인 페이지가 열립니다..."
  $CLASP login
fi
echo ""

# --- Step 4: 프로젝트 생성 + 코드 업로드 ---
echo "[4/5] Apps Script 프로젝트 설정"
cd "$APPS_SCRIPT_DIR"

if [ -f ".clasp.json" ]; then
  echo "      기존 프로젝트 발견 → 코드 업데이트"
else
  echo "      새 프로젝트 생성 중..."
  $CLASP create --type webapp --title "ARIA Google Workspace MCP" --rootDir .
fi

echo "      코드 업로드 중..."
$CLASP push --force
echo "      업로드 완료 ✓"
echo ""

# --- Step 5: 웹앱 배포 ---
echo "[5/5] 웹앱 배포 중..."
DEPLOY_OUTPUT=$($CLASP deploy --description "ARIA MCP $(date +%Y-%m-%d)" 2>&1)

# URL 추출 시도
DEPLOY_ID=$(echo "$DEPLOY_OUTPUT" | grep -oE 'AKfycb[a-zA-Z0-9_-]+' | head -1 || true)

if [ -n "$DEPLOY_ID" ]; then
  DEPLOY_URL="https://script.google.com/macros/s/${DEPLOY_ID}/exec"
else
  # fallback: 전체 출력에서 URL 직접 추출
  DEPLOY_URL=$(echo "$DEPLOY_OUTPUT" | grep -oE 'https://script\.google\.com/macros/s/[^[:space:]]+' | head -1 || true)
fi

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║            배포 완료! 🎉                  ║"
echo "╚══════════════════════════════════════════╝"
echo ""

if [ -n "$DEPLOY_URL" ]; then
  echo "  웹앱 URL:"
  echo "  $DEPLOY_URL"
  echo ""
  echo "  이 URL을 ARIA에서 사용하면 됩니다."
  echo "  (setup 도구에서 자동으로 물어봅니다)"

  # config.json에 URL 자동 저장 (사용자 이메일은 나중에)
  CONFIG_DIR="$HOME/.config/google-workspace-mcp"
  mkdir -p "$CONFIG_DIR"
  if [ -f "$CONFIG_DIR/config.json" ]; then
    # 기존 config에 URL만 업데이트
    TMP=$(mktemp)
    python3 -c "
import json, sys
try:
    with open('$CONFIG_DIR/config.json') as f: c = json.load(f)
except: c = {}
c['webAppUrl'] = '$DEPLOY_URL'
with open('$CONFIG_DIR/config.json', 'w') as f: json.dump(c, f, indent=2)
" 2>/dev/null || echo "{\"webAppUrl\": \"$DEPLOY_URL\"}" > "$CONFIG_DIR/config.json"
  else
    echo "{\"webAppUrl\": \"$DEPLOY_URL\"}" > "$CONFIG_DIR/config.json"
  fi
  echo ""
  echo "  URL이 ~/.config/google-workspace-mcp/config.json에 저장됨 ✓"
else
  echo "  ⚠️ URL 자동 추출 실패. 아래에서 직접 확인:"
  echo "  $DEPLOY_OUTPUT"
  echo ""
  echo "  또는: https://script.google.com → 프로젝트 → 배포 관리"
fi

echo ""
