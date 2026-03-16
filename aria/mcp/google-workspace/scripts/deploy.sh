#!/bin/bash
# Google Workspace MCP — Apps Script 자동 배포
#
# 사전 준비:
#   1. https://script.google.com/home/usersettings 에서 Apps Script API "사용" 토글
#   2. 이 스크립트 실행
#
# 사용법:
#   cd aria/mcp/google-workspace
#   bash scripts/deploy.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
APPS_SCRIPT_DIR="$PROJECT_DIR/apps-script"
CLASP="npx @google/clasp"

echo "=== Google Workspace MCP — Apps Script 배포 ==="
echo ""

# Step 1: clasp 로그인 확인
if ! $CLASP login --status 2>/dev/null | grep -q "You are logged in"; then
  echo "[1/4] Google 로그인이 필요합니다. 브라우저가 열립니다..."
  $CLASP login
else
  echo "[1/4] Google 로그인 확인 ✓"
fi

# Step 2: 프로젝트 생성 (이미 있으면 스킵)
if [ -f "$APPS_SCRIPT_DIR/.clasp.json" ]; then
  echo "[2/4] 기존 Apps Script 프로젝트 발견 ✓"
else
  echo "[2/4] Apps Script 프로젝트 생성 중..."
  cd "$APPS_SCRIPT_DIR"
  $CLASP create --type webapp --title "ARIA Google Workspace MCP" --rootDir .
  echo "    프로젝트 생성 완료 ✓"
fi

# Step 3: 코드 푸시
echo "[3/4] 코드 업로드 중..."
cd "$APPS_SCRIPT_DIR"
$CLASP push --force
echo "    코드 업로드 완료 ✓"

# Step 4: 웹앱 배포
echo "[4/4] 웹앱 배포 중..."
DEPLOY_OUTPUT=$($CLASP deploy --description "ARIA MCP $(date +%Y-%m-%d)")
DEPLOY_URL=$(echo "$DEPLOY_OUTPUT" | grep -oP 'https://script\.google\.com/macros/s/[^/]+/exec' || true)

if [ -z "$DEPLOY_URL" ]; then
  echo ""
  echo "⚠️  자동 URL 추출 실패. 아래 출력에서 웹앱 URL을 직접 확인해주세요:"
  echo "$DEPLOY_OUTPUT"
  echo ""
  echo "또는 https://script.google.com 에서 프로젝트 → 배포 관리 → URL 확인"
else
  echo ""
  echo "=== 배포 완료 ==="
  echo ""
  echo "웹앱 URL: $DEPLOY_URL"
  echo ""
  echo "이 URL을 ARIA의 setup 도구에 입력하면 됩니다."
fi
