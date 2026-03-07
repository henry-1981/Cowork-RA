# Cowork-RA

Anthropic Cowork plugin marketplace repository for ARIA.

[한국어 (기본)](./README.md) | [English](./README.en.md)

## 개요

`Cowork-RA`는 Cowork에서 ARIA 플러그인을 설치하고 사용하는 데 필요한 현재 v1.0 자산만 담는 저장소입니다.

ARIA는 하나의 진입점에서 두 가지 RA 핵심 업무를 처리합니다.

- `determination`: 제품의 의료기기 해당 여부 판단
- `fair-competition`: 공정경쟁규약 검토와 사내 승인용 기안 지원

과거 파이프라인 설계 문서와 일회성 리팩토링 자산은 repo에 남기지 않고 로컬 `_archive/`에만 보관합니다.

## V1.0 범위

| 구성 | 현재 범위 |
|---|---|
| Entry command | `/aria:assist` |
| Skill 1 | `determination` |
| Skill 2 | `fair-competition` |
| 응답 방식 | 기본은 짧고 대화형, 필요 시 심화 |
| 지식 자산 | 스킬별 번들 reference 또는 모듈 |

## 언제 쓰면 좋은가

| 상황 | ARIA가 하는 일 |
|---|---|
| 제품이 의료기기인지 먼저 판단해야 할 때 | intended use와 작동 원리를 바탕으로 determination을 수행합니다. |
| 공정경쟁규약 이슈를 빠르게 점검해야 할 때 | 활동 유형을 매핑하고 규약 기준으로 검토 흐름을 안내합니다. |
| 사전심의/지출보고서용 초안이 필요할 때 | fair-competition 맥락에서 내부 승인 문안 작성을 돕습니다. |

## Quick Start

모든 요청은 `/aria:assist`로 시작합니다.

```text
/aria:assist 심전도 웨어러블이 의료기기에 해당하나요?
/aria:assist 자사제품설명회 사전심의용 검토와 초안이 필요해요.
```

ARIA는 질문 의도를 보고 내부적으로 `determination` 또는 `fair-competition`으로 라우팅합니다.

## 설치

1. Claude Desktop App을 설치합니다.
   - https://claude.com/download
2. Claude Desktop App에서 Cowork 탭을 선택합니다.
3. Cowork에서 플러그인 설치 화면으로 이동합니다.
   - 플러그인 -> `+` 버튼 -> 플러그인 탐색 -> 개인 -> GitHub에서 마켓플레이스 추가
4. 아래 GitHub URL을 입력합니다.
   - `https://github.com/henry-1981/Cowork-RA.git`

## 문서

- ARIA 사용 가이드: [`aria/README.md`](./aria/README.md)
- 단일 명령 진입점: [`aria/commands/assist.md`](./aria/commands/assist.md)
- 플러그인 변경 이력: [`aria/CHANGELOG.md`](./aria/CHANGELOG.md)

## 문제 해결

- 일부 MCP 커넥터가 없어도 ARIA는 번들 reference와 스킬 로직만으로 기본 동작합니다.
- 상세 문서 출력은 사용 환경의 도구/커넥터 가용성에 따라 달라질 수 있습니다.

## 라이선스

[Apache-2.0](./aria/LICENSE)
