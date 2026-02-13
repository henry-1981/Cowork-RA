# ARIA (AI Regulatory Intelligence Assistant)

의료기기 규제 준수를 위한 AI 어시스턴트 - Anthropic Cowork Plugin

## 개요

ARIA는 의료기기 규제 업무 담당자를 위한 AI 기반 규제 인텔리전스 어시스턴트입니다. 미국 FDA, EU MDR, 한국 MFDS의 의료기기 규제 요구사항을 분석하고, 규제 전략을 수립하며, 제출 경로를 제안합니다.

### 주요 기능

- **규제 평가 파이프라인**: 의료기기 판정, 등급 분류, 규제 경로를 통합 분석
- **프로젝트 계획 파이프라인**: 비용/일정 추정, 마일스톤 계획을 통합 생성
- **대화형 규제 자문**: 자연스러운 대화를 통한 규제 질의응답 및 제품 프로파일링
- **종합 브리핑 보고서**: 모든 파이프라인 데이터를 통합한 임원 보고서 생성
- **다국가 비교 분석**: 2개 이상 시장 진출 시 자동 비교 및 전략 제안
- **마케팅 컴플라이언스 자문**: 한국 공정경쟁규약 기반 마케팅 활동 적법성 판단 및 검토 보고서 생성

### v0.1.0 아키텍처 (SPEC-ARIA-003)

- **4개 명령어**: 복잡한 비즈니스 워크플로우를 오케스트레이션하는 명령어
- **6개 스킬**: 순수 분석 로직 단위 (I/O 없음, 파일 관리 없음)
- **명령어-스킬 분리**: 명확한 역할 분리로 유지보수성 향상

### 버전 정책

- 플러그인/커맨드/스킬 버전 정책: `aria/VERSIONING.md`
- 자동 검증: `.github/workflows/version-policy.yml`

### 대상 사용자

- 규제 업무(RA) 담당자
- 품질 보증(QA) 엔지니어
- 설계 엔지니어
- 임상 전문가
- 비개발자 비즈니스 전문가

### 지원 규제 지역

- **미국 FDA** (Food and Drug Administration)
- **EU MDR** (Medical Device Regulation 2017/745)
- **한국 MFDS** (식품의약품안전처)

---

## 설치

### 전제 조건

- Anthropic Cowork 플랫폼 접근 권한
- Node.js 및 npx 설치 (MCP 커넥터용)

### 플러그인 설치

다음 두 가지 방법 중 하나로 ARIA 플러그인을 Cowork 플랫폼에 설치할 수 있습니다:

**방법 1: GitHub URL로 설치**

Cowork 플랫폼의 플러그인 설치 화면에서 다음 GitHub URL을 입력합니다:

```
https://github.com/henry-1981/Cowork-RA.git
```

**방법 2: .zip 파일 업로드**

1. [Cowork-RA 레포지토리](https://github.com/henry-1981/Cowork-RA)에서 `.zip` 파일을 다운로드합니다.
2. Cowork 플랫폼의 플러그인 설치 화면에서 다운로드한 `.zip` 파일을 업로드합니다.

### 설치 확인

플러그인이 정상적으로 설치되면 다음 디렉토리 구조가 생성됩니다:

```
aria/
├── .claude-plugin/plugin.json    # 플러그인 매니페스트
├── .mcp.json                     # HTTP MCP 서버 구성 (플러그인 레벨)
├── CONNECTORS.md                 # MCP 커넥터 문서 (표준 형식)
├── README.md                     # 본 파일
├── commands/                     # 4개 슬래시 커맨드
│   ├── chat.md                  # /aria:chat - 대화형 규제 자문
│   ├── assess.md                # /aria:assess - 규제 평가 파이프라인
│   ├── project.md               # /aria:project - 프로젝트 계획 파이프라인
│   └── report.md                # /aria:report - 종합 브리핑 보고서
└── skills/                       # 6개 도메인 스킬 (순수 분석 로직)
    ├── determination/SKILL.md    # 의료기기 판정
    ├── classification/SKILL.md   # 다지역 등급 분류
    ├── pathway/SKILL.md          # 규제 제출 경로
    ├── estimation/SKILL.md       # 비용/일정 추정
    ├── planning/SKILL.md         # 마일스톤 계획
    └── compliance/               # 공정경쟁규약 마케팅 컴플라이언스
        ├── SKILL.md              # 컴플라이언스 판단 스킬
        └── references/           # 규약 참조 문서
            ├── regulation.md     # 공정경쟁규약 원문 (2017.11.10)
            ├── activity-guide.md # 활동별 체크리스트 + 내부지침 (2024.07.12)
            └── faq.md            # 70+ FAQ + 위반 사례 (2023.05.02)
```

---

## MCP 커넥터 설정

ARIA는 5가지 카테고리의 MCP(Model Context Protocol) 커넥터를 통해 외부 도구와 통합됩니다.

### 커넥터 아키텍처

**플러그인 레벨 `.mcp.json`**: ARIA 플러그인은 `aria/.mcp.json` 파일에 HTTP MCP 서버를 사전 구성합니다. 이 서버들은 플러그인 설치 시 자동으로 Claude Code에서 사용 가능합니다.

**시스템 레벨 `.mcp.json`**: Context7과 같은 로컬 npx 기반 MCP 서버는 시스템 레벨 설정(`~/.claude/settings.json`)에서 별도로 구성해야 합니다.

### 카테고리 기반 설계

ARIA는 **도구 독립적(tool-agnostic)** 설계를 사용합니다. 워크플로우는 특정 제품 이름 대신 **카테고리 플레이스홀더**로 설명됩니다:

- `~~knowledge base`: 조직 특화 규제 데이터 (Notion, Confluence)
- `~~project tracker`: 규제 프로젝트 마일스톤 추적 (Jira, Linear)
- `~~chat`: 팀 커뮤니케이션 및 알림 (Slack, Teams)
- `~~cloud storage`: 문서 내보내기 및 저장 (Microsoft 365, Google Drive)
- `~~regulatory docs`: 외부 규제 문서 검증 (Context7)

자세한 커넥터 정보는 `CONNECTORS.md`를 참조하세요.

### HTTP MCP 서버 (플러그인 사전 구성)

다음 HTTP MCP 서버는 `aria/.mcp.json`에 사전 구성되어 있습니다:

| 서버 | 카테고리 | URL | 설명 |
|-----|---------|-----|------|
| **notion** | ~~knowledge base | https://mcp.notion.com/mcp | 조직 규제 데이터베이스 |
| **atlassian** | ~~knowledge base / ~~project tracker | https://mcp.atlassian.com/v1/mcp | Confluence, Jira |
| **slack** | ~~chat | https://mcp.slack.com/mcp | 팀 알림 및 공유 |
| **ms365** | ~~cloud storage | https://microsoft365.mcp.claude.com/mcp | OneDrive, SharePoint |

이 서버들은 **추가 구성 없이** 사용할 수 있습니다. ARIA 스킬은 런타임에 `ToolSearch`를 통해 필요한 MCP 도구를 자동으로 로드합니다.

### 로컬 MCP 서버 (사용자 구성 필요)

Context7과 같은 로컬 npx 기반 MCP 서버는 시스템 레벨에서 별도로 구성해야 합니다.

**설정 방법 (Context7 예시)**:

`~/.claude/settings.json` 파일에 다음을 추가합니다:

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    }
  }
}
```

**macOS/Linux 설정 위치**:
```
~/.claude/settings.json
```

**Windows 설정 위치**:
```
%USERPROFILE%\.claude\settings.json
```

**참고**:
- MCP 설정 변경 후 Claude Code를 재시작해야 합니다
- Context7은 별도 인증이 필요하지 않습니다
- 시스템 레벨 설정은 모든 Claude Code 프로젝트에서 공유됩니다

### 데이터 소스 우선순위

ARIA는 다음 순서로 데이터를 검색합니다:

1. **내장 지식** (Priority 1) - 스킬에 포함된 의사결정 프레임워크 (항상 사용 가능)
2. **모듈 파일** (Priority 2) - 상세한 규제 기준 (필요시 로드)
3. **~~knowledge base** (Priority 3) - 조직 특화 규제 데이터 (선택)
4. **~~regulatory docs** (Priority 4) - 외부 규제 문서 검증 (선택)

**중요**: 외부 MCP 소스가 구성되지 않은 상태가 기본 동작 모드입니다. ARIA는 내장 지식만으로 완전히 작동하며, 외부 소스는 보완 기능을 제공합니다.

### 우아한 저하 (Graceful Degradation)

MCP 커넥터를 사용할 수 없을 경우 ARIA는 자동으로 내장 지식으로 대체하여 계속 작동합니다:

- `~~knowledge base` 불가용 → 내장 규제 지식 사용 (무음 저하)
- `~~regulatory docs` 불가용 → 내장 규제 지식 사용 (소스 섹션에 표시)
- `~~cloud storage` 불가용 → Markdown 형식으로 대체
- `~~project tracker` 불가용 → Markdown 형식으로 대체
- `~~chat` 불가용 → 로컬 파일로 저장

자세한 우아한 저하 매트릭스는 `CONNECTORS.md`를 참조하세요.

---

## 명령어 참조

ARIA는 4개의 슬래시 커맨드를 제공하며, 모두 `/aria:` 접두사를 사용합니다.

### 파이프라인 흐름

```
/aria:chat ──(대화를 통한 제품 프로파일링)──> profile.json
                                                  │
/aria:assess ──(판정 → 분류 → 경로 통합 평가)──> assess.md
                                                  │
/aria:project ──(비용/일정 추정 → 마일스톤 계획)──> project.md
                                                  │
/aria:report ──(전체 파이프라인 데이터 통합)──> briefing.md
```

각 명령어는 독립적으로 실행 가능하며, 이전 단계 데이터가 있을 경우 자동으로 불러옵니다.

---

### /aria:chat

**설명**: 자연스러운 대화를 통한 규제 자문, 제품 프로파일 구축, 스킬 자동 라우팅

**사용법**:
```
/aria:chat [질문 또는 요청사항]
```

**플래그**:
- `--lang ko|en`: 출력 언어 선택 (기본값: ko)

**예시**:
```
/aria:chat 심장 모니터링 장치가 의료기기인가요?
/aria:chat What is the FDA classification for a glucose meter?
/aria:chat [기술문서 PDF 업로드]
```

**기능**:
- 대화를 통한 점진적 제품 프로파일 구축 (profile.json)
- 프로파일 충분도에 따른 투명한 스킬 자동 실행
- 일반 규제 지식 질의응답
- 파이프라인 명령어 자동 추천 (사용자 승인 필요)

---

### /aria:assess

**설명**: 규제 평가 파이프라인 - 판정, 분류, 경로 분석을 통합 실행

**사용법**:
```
/aria:assess [제품 설명 또는 문서]
```

**플래그**:
- `--lang ko|en`: 출력 언어 선택 (기본값: ko)
- `--format markdown|pdf|notion|gdocs`: 출력 형식 선택 (기본값: markdown)

**예시**:
```
/aria:assess
/aria:assess 심장 박동을 측정하고 부정맥을 감지하는 웨어러블 장치
/aria:assess --lang en --format pdf
/aria:assess [기술문서 PDF 업로드]
```

**실행 흐름**:
1. 제품 컨텍스트 로드 (기존 프로파일 또는 신규 입력)
2. 의료기기 판정 (YES/NO/CONDITIONAL)
3. 다지역 등급 분류 (FDA/EU MDR/MFDS)
4. 규제 제출 경로 선택
5. 다국가 비교 분석 (2개 이상 시장)
6. 통합 보고서 생성

**출력**: `assess.md` + `assess.summary.md`

**대체 명령어**: `/aria:determine`, `/aria:classify`, `/aria:pathway`, `/aria:compare` (평가 문맥)

---

### /aria:project

**설명**: 프로젝트 계획 파이프라인 - 비용/일정 추정과 마일스톤 계획을 통합 실행

**사용법**:
```
/aria:project [옵션]
```

**플래그**:
- `--lang ko|en`: 출력 언어 선택 (기본값: ko)
- `--format markdown|pdf|notion|gdocs`: 출력 형식 선택 (기본값: markdown)

**예시**:
```
/aria:project
/aria:project --lang en --format gdocs
/aria:project --format pdf
```

**실행 흐름**:
1. 평가 데이터 로드 (assess.summary.md 또는 수동 입력)
2. 비용/일정 3점 추정 (낙관/예상/비관)
3. 마일스톤 계획 생성
4. 다국가 최적화 (2개 이상 시장)
5. 통합 프로젝트 계획 생성

**출력**: `project.md` + `project.summary.md`

**대체 명령어**: `/aria:estimate`, `/aria:plan`, `/aria:compare` (프로젝트 문맥)

---

### /aria:report

**설명**: 종합 규제 브리핑 보고서 생성 (모든 파이프라인 데이터 통합)

**사용법**:
```
/aria:report [초점 영역]
```

**플래그**:
- `--format markdown|notion|gdocs|pdf`: 출력 형식 선택 (기본값: markdown)
- `--lang ko|en`: 출력 언어 선택 (기본값: ko)

**예시**:
```
/aria:report
/aria:report Clinical Strategy
/aria:report --format notion
/aria:report 임원 보고용 --format pdf --lang en
```

**실행 흐름**:
1. 파이프라인 데이터 수집 (assess + project 결과)
2. 데이터 충분도 평가
3. Phase A: 핵심 분석 요약 제시 (사용자 확인 필요)
4. Phase B: 사용자 확인 후 전체 보고서 생성

**출력**: `briefing.md` + `briefing.summary.md`

**출력 형식**:
- **Markdown** (기본): `.aria/products/{제품명}/{날짜}/briefing.md`
- **Notion**: Notion 페이지 생성 (Notion MCP 필요)
- **Google Docs**: Google Docs 문서 생성 (Google Drive MCP 필요)
- **PDF**: PDF 문서 생성

---

## 출력 파일 구조

### .aria/ 디렉토리 구조

```
.aria/
├── active_product.json              # 현재 활성 제품 (로컬, 공유 금지)
└── products/
    └── {제품명}/
        └── {날짜}/
            ├── profile.json         # 제품 프로파일 (/aria:chat)
            ├── assess.md            # 통합 규제 평가 보고서
            ├── assess.summary.md    # 평가 요약 (하위 명령어용)
            ├── project.md           # 통합 프로젝트 계획
            ├── project.summary.md   # 프로젝트 요약 (하위 명령어용)
            ├── briefing.md          # 종합 브리핑 보고서
            └── briefing.summary.md  # 브리핑 요약 (감사 추적용)
```

### 이전 버전 호환성

기존 `.aria/products/` 데이터(determination.md, classification.md 등)는 `/aria:report` 명령어에서 레거시 형식으로 자동 인식합니다.

---

## 설정 (aria.local.md)

### aria.local.md 개요

`aria.local.md`는 조직별 규제 전략, 선호 경로, 비용 벤치마크 등을 설정하는 플레이북 파일입니다.

**위치**: 프로젝트 루트 디렉토리 (플러그인 디렉토리가 아님)

**사용 방법**:
1. 아래 템플릿을 복사하여 프로젝트 루트에 `aria.local.md` 파일 생성
2. 조직 정보 및 선호 설정 입력
3. ARIA가 자동으로 설정을 불러와 적용

### aria.local.md 템플릿 (요약)

```markdown
# ARIA Local Playbook

## Organization Profile
company_name: "Your Company Name"
regulatory_department: "RA/QA Department"
primary_device_types: ["Active", "Implantable"]
active_markets: ["US", "EU", "Korea"]

## Language Preference
# 출력 언어 설정 (Output Language)
# Options: ko (Korean, default) | en (English)
output_language: ko

## Preferred Regulatory Pathways
# FDA 선호 경로
fda_class_i_preferred: "510(k) Exempt"
fda_class_ii_preferred: "510(k)"
fda_class_iii_preferred: "PMA"

# EU MDR 선호 Notified Body
eu_preferred_notified_body: "TUV SUD"

# MFDS 선호 경로
mfds_preferred_pathway: "인증"

## Risk Tolerance
# 조직 위험 선호도: conservative | moderate | aggressive
risk_appetite: conservative

## Data Management
# 데이터 보존 기간 (일)
data_retention_days: 365
# 보존 기간 초과 데이터 경고
warn_on_stale_data: true
```

**전체 템플릿**: `aria.local.md` 파일 참조 (플러그인 루트에 포함)

---

## 보안 경고

### .aria/ 디렉토리 민감성

ARIA는 모든 작업 데이터를 `.aria/products/{제품명}/{날짜}/` 경로에 저장합니다.

**주의사항**:
- `.aria/` 디렉토리는 **영업 비밀 및 독점 설계 정보**를 포함할 수 있습니다
- `.gitignore`에 `.aria/` 추가 권장
- 민감한 제품 정보가 포함되므로 외부 공유 금지

**데이터 분류**: `.aria/` 내 모든 파일은 조직 기밀로 취급하세요.

### active_product.json 공유 금지

**중요**: `.aria/active_product.json` 파일은 **개인 로컬 작업 상태**를 저장합니다.

**절대 금지사항**:
- Git에 커밋하지 마세요
- 팀원과 공유하지 마세요
- 버전 관리에 포함하지 마세요

**이유**: 이 파일은 개인의 현재 작업 중인 제품을 추적하며, 다른 팀원의 로컬 환경과 충돌을 일으킬 수 있습니다.

**권장 .gitignore 설정**:
```
.aria/
```

### MCP 인증 정보 관리

**모든 MCP 인증 정보는 환경 변수로 관리**:
- 환경 변수 사용: `export NOTION_API_KEY="..."`
- 파일에 직접 저장 금지
- Git에 커밋 금지

`.mcp.json` 파일은 환경 변수 플레이스홀더만 포함하며, 실제 값은 포함하지 않습니다.

---

## 문제 해결

### 일반 설치 문제

**Q: 플러그인이 인식되지 않습니다**
- `.claude-plugin/plugin.json` 파일이 존재하는지 확인
- Cowork 플랫폼에서 플러그인 재등록
- 플러그인 디렉토리 경로 확인

**Q: 명령어가 작동하지 않습니다**
- `/aria:` 접두사를 올바르게 입력했는지 확인
- 명령어 이름 철자 확인 (예: `/aria:assess`, `/aria:project`)
- Cowork 플랫폼 로그 확인

### MCP 연결 문제

**Q: Notion 연결이 실패합니다**
- `NOTION_API_KEY` 환경 변수가 설정되었는지 확인
- Notion 통합이 데이터베이스에 공유되었는지 확인
- API 키가 유효한지 확인

**Q: Google Drive 연결이 실패합니다**
- `GOOGLE_CREDENTIALS` 경로가 올바른지 확인
- 인증 정보 파일이 존재하는지 확인
- OAuth 권한이 부여되었는지 확인

**Q: Context7이 작동하지 않습니다**
- 인터넷 연결 확인
- `npx -y @upstash/context7-mcp` 명령어 직접 실행 테스트
- Context7 서비스 상태 확인

### 데이터 소스 불가용

**Q: "Notion database unavailable" 경고가 표시됩니다**
- 이는 정상적인 우아한 저하(graceful degradation)입니다
- ARIA는 내장 지식으로 대체하여 계속 작동합니다
- 조직 특화 데이터가 필요한 경우 Notion 연결 복구 권장

**Q: 모든 데이터 소스가 불가용합니다**
- 최소한 내장 지식은 항상 사용 가능해야 합니다
- 플러그인 설치 상태 확인 (스킬 파일 존재 여부)
- 설치를 다시 시도하세요

---

## FAQ

### 명령어 선택 가이드

**Q: 어떤 명령어부터 시작해야 하나요?**
- 처음 사용: `/aria:chat`으로 자연스러운 대화 시작
- 규제 평가: `/aria:assess`로 통합 규제 평가 실행
- 프로젝트 계획: `/aria:project`로 비용/일정 추정 (assess 데이터 권장)
- 종합 보고서: `/aria:report`로 전체 결과 통합 보고서 생성

**Q: 반드시 순서대로 실행해야 하나요?**
- 아니요. 각 명령어는 독립적으로 실행 가능합니다
- 권장 순서: chat -> assess -> project -> report
- 이전 단계 데이터가 있으면 자동으로 활용합니다
- 없어도 수동 입력으로 진행 가능합니다

**Q: 이전 버전의 `/aria:determine`, `/aria:classify` 등은 어디 갔나요?**
- v0.1.0에서 4개 통합 명령어로 재구조화되었습니다
- `/aria:assess`가 determine + classify + pathway + compare(평가 문맥)를 대체합니다
- `/aria:project`가 estimate + plan + compare(프로젝트 문맥)를 대체합니다
- 기존 `.aria/` 데이터는 호환성이 유지됩니다

### 조직별 커스터마이징

**Q: 우리 조직의 선호 경로를 어떻게 설정하나요?**
- `aria.local.md` 파일을 프로젝트 루트에 생성
- `Preferred Regulatory Pathways` 섹션에 선호 경로 입력
- ARIA가 자동으로 불러와 적용합니다

**Q: 비용 추정을 조직 실제 비용으로 업데이트할 수 있나요?**
- `aria.local.md`의 `Cost/Timeline Benchmarks` 섹션에 입력
- 과거 프로젝트 실제 비용 및 일정 입력
- ARIA가 추정 시 조직 벤치마크를 우선 사용합니다

### 데이터 보존 정책

**Q: .aria/ 디렉토리 데이터를 언제 삭제해야 하나요?**
- ARIA는 자동 삭제하지 않습니다 (데이터 손실 방지)
- `aria.local.md`의 `data_retention_days` 설정 시 경고 표시
- 수동으로 오래된 날짜 디렉토리 삭제 권장

**Q: 규제 감사 대비 데이터 보존 기간은?**
- FDA: 제품 단종 후 최소 2년
- EU MDR: 시장 출시 후 10년 (이식형은 15년)
- MFDS: 의료기기법 보존 요구사항 준수
- 조직 정책에 따라 `.aria/` 데이터 관리 필요

**Q: 여러 제품을 동시에 작업할 수 있나요?**
- 가능합니다. 각 제품은 `.aria/products/{제품명}/` 하위에 저장됩니다
- 여러 제품 존재 시 ARIA가 활성 제품 선택 요청
- `.aria/active_product.json`에 현재 작업 제품 저장 (공유 금지)

---

## 면책 조항

**본 출력물은 AI 생성 참조 정보이며, 규제 자문, 법률 지도, 또는 공식 규제 판정을 구성하지 않습니다.**

모든 규제 결정은 자격을 갖춘 규제 업무 전문가가 검증해야 하며, 현행 적용 규정에 대해 확인되어야 합니다.

ARIA는 의사결정 지원 도구이며, 전문가 판단을 대체하지 않습니다.

---

## 추가 정보

- **CONNECTORS.md**: MCP 커넥터 카테고리 및 확장성 가이드 (표준 Cowork 플러그인 형식)
- **aria.local.md**: 조직 설정 전체 템플릿 (플러그인 루트)
- **aria/.mcp.json**: HTTP MCP 서버 사전 구성 (플러그인 레벨)

**버전**: 0.1.2
**라이선스**: Apache-2.0
**지원**: GitHub Issues에서 문제 보고 및 기능 요청
