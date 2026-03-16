# Google Workspace MCP 서버

ARIA 플러그인의 Google Docs 연동을 위한 MCP 서버.
Google Apps Script를 백엔드로 사용하여 Cloud Console 설정 없이 동작합니다.

## 구조

```
MCP 서버 (Node.js, 로컬) → HTTP POST → Google Apps Script (웹앱) → Docs/Drive
```

## 도구 목록

| 도구 | 설명 |
|------|------|
| `setup` | 최초 설정 (Apps Script URL + 사용자 이메일) |
| `read_document` | Google Docs 본문 읽기 |
| `inspect_template` | 템플릿 `{{placeholder}}` 필드 목록 추출 |
| `copy_template` | 템플릿 복사 → 새 문서 생성 (소유권 자동 이전) |
| `fill_fields` | 필드 자동 채움 + 미치환 감지 |
| `get_share_link` | 공유 권한 설정 + 링크 반환 |

## 설정

### 관리자 (1회, 2분)

**자동 배포 (권장):**

```bash
# 사전 준비: https://script.google.com/home/usersettings → Apps Script API "사용"
cd aria/mcp/google-workspace
bash scripts/deploy.sh
```

스크립트가 브라우저 로그인 → 프로젝트 생성 → 코드 업로드 → 배포까지 자동 처리합니다.

**수동 배포:**

1. Google Drive → **새로 만들기 → Google Apps Script**
2. `apps-script/Code.gs` 전체 내용 복사-붙여넣기
3. **배포 → 새 배포 → 웹 앱**:
   - 실행 계정: **나**
   - 액세스 권한: **[회사 도메인] 내 누구나**
4. 배포 URL 복사

### 사용자 (1회)

ARIA에서 처음 사용 시 `setup` 도구가 호출됩니다:
- Apps Script 웹앱 URL 입력 (관리자에게 받음)
- 본인 회사 이메일 입력
- 끝. 이후 자동으로 동작합니다.

설정은 `~/.config/google-workspace-mcp/config.json`에 저장됩니다.

## 빌드

```bash
cd aria/mcp/google-workspace
npm install
npm run build
```

## 동작 원리

- Apps Script가 **관리자 계정으로** 문서를 생성합니다
- 생성 즉시 `setOwner(userEmail)`로 **사용자에게 소유권 이전**
- 사용자의 Google Drive에 문서가 나타납니다
- 같은 Google Workspace 도메인 내에서만 동작합니다
