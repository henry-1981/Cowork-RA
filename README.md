# Cowork-RA

Anthropic Cowork plugin marketplace for Regulatory Affairs workflows.

[![한국어](https://img.shields.io/badge/Language-한국어-0A66C2)](#ko) [![English](https://img.shields.io/badge/Language-English-4C566A)](#en)

<a id="ko"></a>
## 한국어

### 개요

`Cowork-RA`는 Cowork에서 ARIA 플러그인을 설치하고 사용할 수 있도록 제공하는 마켓플레이스 저장소입니다.

### 포함 플러그인

| 플러그인 | 설명 | 핵심 기능 |
|----------|------|-----------|
| [aria](./aria/) | AI Regulatory Intelligence Assistant | 의료기기 판정, 등급 분류, 규제 경로 분석, 비용/일정 추정, 마일스톤 계획, 종합 브리핑 |

### 설치

1. Cowork에서 플러그인 설치 화면으로 이동합니다.
2. 아래 방식 중 하나를 사용합니다.

- GitHub URL 설치
  - `https://github.com/henry-1981/Cowork-RA.git`
- ZIP 업로드 설치
  - 저장소 ZIP 다운로드 후 업로드

### Quick Start

| 명령어 | 용도 | 예시 |
|--------|------|------|
| `/aria:chat` | 대화형 자문 + 제품 정보 수집 | `/aria:chat 심전도 웨어러블이 의료기기인가요?` |
| `/aria:assess` | 규제 평가(판정/분류/경로) 통합 실행 | `/aria:assess 부정맥 감지 웨어러블 장치` |
| `/aria:project` | 비용/일정/마일스톤 계획 생성 | `/aria:project --format markdown` |
| `/aria:report` | 전체 결과 통합 브리핑 생성 | `/aria:report --lang en` |

권장 실행 순서:
`/aria:chat -> /aria:assess -> /aria:project -> /aria:report`

### 문제 해결

- 일부 MCP 커넥터가 없어도 ARIA는 내장 지식 기반으로 동작합니다.
- 출력 형식(`pdf`, `notion`, `gdocs`)은 사용 환경의 도구/커넥터 가용성에 따라 달라집니다.

### 문서 링크

- ARIA 파워 유저 가이드: [`aria/README.md`](./aria/README.md)
- 명령 상세 스펙:
  - [`aria/commands/chat.md`](./aria/commands/chat.md)
  - [`aria/commands/assess.md`](./aria/commands/assess.md)
  - [`aria/commands/project.md`](./aria/commands/project.md)
  - [`aria/commands/report.md`](./aria/commands/report.md)
- 커넥터 상세: [`aria/CONNECTORS.md`](./aria/CONNECTORS.md)
- 변경 이력: [`CHANGELOG.md`](./CHANGELOG.md), [`aria/CHANGELOG.md`](./aria/CHANGELOG.md)

### 라이선스

[Apache-2.0](./aria/LICENSE)

<a id="en"></a>
## English

### Overview

`Cowork-RA` is a marketplace repository for installing and using the ARIA plugin in Cowork.

### Included Plugin

| Plugin | Description | Core Capabilities |
|--------|-------------|-------------------|
| [aria](./aria/) | AI Regulatory Intelligence Assistant | Device determination, classification, pathway analysis, cost/timeline estimation, milestone planning, executive briefing |

### Installation

1. Open the plugin installation page in Cowork.
2. Use one of the following methods:

- Install via GitHub URL
  - `https://github.com/henry-1981/Cowork-RA.git`
- Install via ZIP upload
  - Download the repository ZIP and upload it

### Quick Start

| Command | Purpose | Example |
|---------|---------|---------|
| `/aria:chat` | Conversational advisory + product profiling | `/aria:chat Is an ECG wearable a medical device?` |
| `/aria:assess` | Integrated assessment (determination/classification/pathway) | `/aria:assess Wearable device for arrhythmia detection` |
| `/aria:project` | Cost/timeline and milestone planning | `/aria:project --format markdown` |
| `/aria:report` | End-to-end executive briefing | `/aria:report --lang en` |

Recommended flow:
`/aria:chat -> /aria:assess -> /aria:project -> /aria:report`

### Troubleshooting

- ARIA works with built-in regulatory knowledge even when some MCP connectors are unavailable.
- Output formats (`pdf`, `notion`, `gdocs`) depend on connector/tool availability in your environment.

### Documentation Links

- ARIA power-user guide: [`aria/README.md`](./aria/README.md)
- Command specs:
  - [`aria/commands/chat.md`](./aria/commands/chat.md)
  - [`aria/commands/assess.md`](./aria/commands/assess.md)
  - [`aria/commands/project.md`](./aria/commands/project.md)
  - [`aria/commands/report.md`](./aria/commands/report.md)
- Connector details: [`aria/CONNECTORS.md`](./aria/CONNECTORS.md)
- Changelogs: [`CHANGELOG.md`](./CHANGELOG.md), [`aria/CHANGELOG.md`](./aria/CHANGELOG.md)

### License

[Apache-2.0](./aria/LICENSE)
