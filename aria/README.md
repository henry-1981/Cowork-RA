# ARIA Power User Guide

의료기기 규제 업무를 빠르게 수행하기 위한 ARIA 활용 가이드입니다.

- 설치/온보딩: 루트 [`README.md`](../README.md)

## ARIA at a Glance

ARIA는 2개 핵심 스킬로 RA 실무를 지원합니다.

### 단일 진입점

`/aria:assist`

### 구성 요약

- Command: `assist` (단일 진입점)
- Skills: `determination` (의료기기/비의료기기 분류), `fair-competition` (공정경쟁규약 기안 작성)

## 질문 유형별 라우팅

| 질문/업무 유형 | 내부 핵심 스킬 |
|---|---|
| 의료기기 해당 여부가 궁금함 | determination |
| 공정경쟁규약 관련 기안 작성 | fair-competition |

## Skill Deep Dive

### `determination`

목적:
- 제품이 의료기기에 해당하는지 FDA/EU MDR/MFDS 기준으로 판정

고품질 입력 체크리스트:
- 의학적 목적(진단/치료/완화/예방) 명시
- 1차 작동 원리(화학적 작용/대사작용 여부 포함)
- 사용 환경(병원/가정/원격)

출력 해석:
- `YES` / `NO` / `CONDITIONAL`
- `CONDITIONAL`이면 추가 법규 검토 또는 전문가 검토 필요

### `fair-competition`

목적:
- 한국 공정경쟁규약 기반 사내 승인용 기안 문서 작성 지원
- 사전심의 요청서, 지출보고서 등

주요 입력:
- 활동 유형(샘플/기증/학술대회/제품설명회/강연/시장조사 등)
- 대상자(보건의료인/의료기관/기타)
- 금액/빈도/절차(사전심의/사후신고)

참조: `aria/skills/fair-competition/references/` (공정경쟁규약 KD)

## Traffic Light

- `GREEN`: 현재 입력 기준으로 명확한 경로
- `YELLOW`: 경계 사례/추가 검증 필요
- `RED`: 현재 조건에서 진행 곤란 또는 비해당

## Disclaimer

ARIA outputs are AI-generated regulatory intelligence for reference only.
Final regulatory and compliance decisions must be validated by qualified professionals.
