# Google Workspace MCP 서버

ARIA fair-competition 스킬의 Google Docs 연동을 위한 MCP 서버.

## 도구 목록

| 도구 | 설명 |
|------|------|
| `read_document` | Google Docs 본문 텍스트 읽기 (URL/ID 자동 파싱) |
| `inspect_template` | 템플릿 내 `{{placeholder}}` 필드 목록 추출 |
| `copy_template` | 템플릿 복사로 새 문서 생성 |
| `fill_fields` | `{{placeholder}}` 치환 + 미치환 필드 감지 |
| `get_share_link` | 공유 권한 설정 + 링크 반환 |

## 설정

### 1. Service Account 생성

1. [Google Cloud Console](https://console.cloud.google.com/) > IAM > Service Accounts
2. 서비스 계정 생성 후 JSON 키 다운로드
3. `credentials.json`으로 저장하여 `aria/mcp/google-workspace/` 디렉토리에 배치

### 2. API 활성화

Google Cloud Console에서 다음 API를 활성화:
- Google Docs API
- Google Drive API

### 3. 템플릿 파일 공유

Service Account 이메일 주소에 템플릿 Google Docs 파일의 편집자 권한을 부여해야 합니다.

### 4. `.mcp.json` 등록

프로젝트 루트의 `.mcp.json`에 추가:

```json
"google-workspace": {
  "$comment": "Google Workspace integration (MVP: Docs)",
  "command": "node",
  "args": ["aria/mcp/google-workspace/dist/index.js"],
  "env": {
    "GOOGLE_APPLICATION_CREDENTIALS": "./aria/mcp/google-workspace/credentials.json",
    "GOOGLE_DOMAIN": ""
  }
}
```

### 환경변수

| 변수 | 설명 | 기본값 |
|------|------|--------|
| `GOOGLE_APPLICATION_CREDENTIALS` | Service Account JSON 키 경로 | (필수) |
| `GOOGLE_DOMAIN` | 조직 도메인 (domain 공유 시 사용) | 빈 문자열 (미설정 시 `anyone` 공유로 fallback) |

## 빌드

```bash
cd aria/mcp/google-workspace
npm install
npm run build
```
