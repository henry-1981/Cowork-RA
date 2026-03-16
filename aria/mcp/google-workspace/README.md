# Google Workspace MCP 서버

ARIA 플러그인의 Google Docs 연동을 위한 MCP 서버.

## 도구 목록

| 도구 | 설명 |
|------|------|
| `auth_google` | Google 인증 (최초 1회 브라우저 로그인) |
| `read_document` | Google Docs 본문 텍스트 읽기 (URL/ID 자동 파싱) |
| `inspect_template` | 템플릿 내 `{{placeholder}}` 필드 목록 추출 |
| `copy_template` | 템플릿 복사로 새 문서 생성 |
| `fill_fields` | `{{placeholder}}` 치환 + 미치환 필드 감지 |
| `get_share_link` | 공유 권한 설정 + 링크 반환 |

## 설정

### 1. Google Cloud OAuth Client 생성 (관리자 1회)

1. [Google Cloud Console](https://console.cloud.google.com/) > APIs & Services > Credentials
2. "Create Credentials" > "OAuth client ID"
3. Application type: **Desktop app**
4. 생성 후 JSON 다운로드 → `oauth-client.json`으로 저장
5. `aria/mcp/google-workspace/` 디렉토리에 배치

### 2. API 활성화 (관리자 1회)

Google Cloud Console에서 다음 API를 활성화:
- Google Docs API
- Google Drive API

### 3. `.mcp.json` 등록

프로젝트 루트의 `.mcp.json`에 추가:

```json
"google-workspace": {
  "$comment": "Google Workspace integration (MVP: Docs)",
  "command": "node",
  "args": ["aria/mcp/google-workspace/dist/index.js"],
  "env": {
    "GOOGLE_DOMAIN": ""
  }
}
```

### 4. 사용자 인증 (각 사용자 1회)

ARIA를 통해 `auth_google` 도구가 호출되면:
1. 브라우저에서 Google 로그인 URL이 열림
2. Google 계정으로 로그인 + 권한 허용
3. "인증 완료" 페이지 확인 → 끝

토큰은 `~/.config/google-workspace-mcp/tokens.json`에 자동 저장됩니다.
이후 자동 갱신되므로 재로그인 불필요.

### 환경변수 (선택)

| 변수 | 설명 | 기본값 |
|------|------|--------|
| `GOOGLE_CLIENT_ID` | OAuth Client ID (oauth-client.json 대체) | — |
| `GOOGLE_CLIENT_SECRET` | OAuth Client Secret | — |
| `GOOGLE_DOMAIN` | 조직 도메인 (domain 공유 시) | 빈 문자열 (미설정 시 `anyone` 공유) |

## 빌드

```bash
cd aria/mcp/google-workspace
npm install
npm run build
```

## Service Account vs OAuth

이 서버는 **OAuth 2.0**을 사용합니다:
- 사용자 본인의 Google 계정으로 인증
- 생성된 파일이 사용자 소유 (Drive에 직접 표시)
- 별도의 템플릿 공유 설정 불필요
- 관리자는 OAuth Client 1회 생성만 하면 됨
