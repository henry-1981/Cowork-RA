# ARIA Power User Guide

의료기기 판정과 공정경쟁규약 검토를 빠르게 수행하기 위한 ARIA v1.0 가이드입니다.

- 설치/온보딩: 루트 [`README.md`](../README.md)

## ARIA at a Glance

ARIA는 단일 명령에서 두 개의 핵심 스킬로 라우팅됩니다.

### 단일 진입점

`/aria:assist`

### 내부 구성

- `determination`
  - 의료기기 해당 여부 판단
  - 기본은 간결 응답, 필요 시 상세 판단으로 확장
- `fair-competition`
  - 공정경쟁규약 검토
  - 내부 승인용 검토 메모와 기안 지원

## 질문 유형별 라우팅

| 질문/업무 유형 | 내부 스킬 |
|---|---|
| 제품이 의료기기인지 궁금함 | `determination` |
| 활동이 공정경쟁규약에 맞는지 확인하고 싶음 | `fair-competition` |
| 사전심의/지출보고서용 초안이 필요함 | `fair-competition` |

## Prompt Examples

```text
/aria:assist 손목형 심전도 측정기가 의료기기에 해당하나요?
/aria:assist 학술대회 참가 지원이 규약상 가능한지 검토해 주세요.
/aria:assist 자사제품설명회 사전심의용 초안이 필요합니다.
```

## Output Style

- 첫 응답은 짧고 핵심만 전달합니다.
- 정보가 부족하면 바로 판단을 확정하지 않고 필요한 정보를 먼저 묻습니다.
- 사용자가 원할 때만 더 긴 분석이나 정리 문안을 제공합니다.

## Knowledge Model

- `determination`
  - 스킬 본문과 `modules/`의 판정 로직을 사용합니다.
  - 제거된 전역 knowledge 트리를 전제로 하지 않습니다.
- `fair-competition`
  - `aria/skills/fair-competition/references/`의 번들 reference를 사용합니다.
  - 토픽별 규정, FAQ, 체크리스트, 위반사례를 함께 참조합니다.

## Repository Policy

- repo에는 현재 v1.0 동작에 필요한 문서와 자산만 남깁니다.
- 과거 설계 문서, 실험용 테스트, 일회성 변환 스크립트는 로컬 `_archive/`에만 보관합니다.

## Disclaimer

ARIA outputs are AI-generated regulatory intelligence for reference only.
Final regulatory and compliance decisions must be validated by qualified professionals.
