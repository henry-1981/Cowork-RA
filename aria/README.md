# ARIA Power User Guide

의료기기 규제 업무를 빠르게 수행하기 위한 ARIA 고급 활용 가이드입니다.

- 설치/온보딩: 루트 [`README.md`](../README.md)
- 본 문서 대상: 파워 유저 (RA/QA/기술 리더, 반복 분석 사용자)

## ARIA at a Glance

ARIA는 4개 명령어와 6개 스킬을 조합해 규제 의사결정을 지원합니다.

### 권장 실행 흐름

`/aria:chat -> /aria:assess -> /aria:project -> /aria:report`

### 구성 요약

- Commands (오케스트레이션): `chat`, `assess`, `project`, `report`
- Skills (분석 엔진): `determination`, `classification`, `pathway`, `estimation`, `planning`, `compliance`

## 질문 유형별 빠른 라우팅

| 질문/업무 유형 | 시작 명령어 | 내부 핵심 스킬 |
|---|---|---|
| 의료기기 해당 여부가 궁금함 | `/aria:chat` 또는 `/aria:assess` | determination |
| FDA/EU/MFDS 등급을 알고 싶음 | `/aria:assess` | classification |
| 510(k)/PMA/CE/MFDS 경로를 비교하고 싶음 | `/aria:assess` | pathway |
| 예산/일정/병목이 궁금함 | `/aria:project` | estimation + planning |
| 임원 보고용 요약이 필요함 | `/aria:report` | assess/project 통합 |
| 한국 마케팅 활동 적법성 검토 | `/aria:chat` | compliance |

## Command Usage Patterns

### 1) `/aria:chat`

언제 쓰나:
- 제품 개념이 아직 모호할 때
- 대화형으로 프로파일을 쌓고 싶을 때
- 일반 규제 Q&A가 필요할 때

입력 팁:
- 의도된 사용 목적(intended use)과 사용자(환자/의료진)를 먼저 명시
- 진단/치료/모니터링 여부를 분명히 표현

응답 깊이 조절:
- 기본: 1-2문장 결론 + 핵심 근거 (express)
- "상세 분석", "자세히" → 상세 응답 + MANDATORY OUTPUT FORMAT
- "심화 수준", "deep dive" → 심층 분석 (modules/, 4-Gate 포함)
- "전체 분석" → ARIA가 확인 후 determination → classification → pathway 순차 실행 (각 단계에서 중단 가능)

예시:
```text
/aria:chat ECG 측정과 부정맥 감지를 제공하는 웨어러블을 개발 중입니다. 미국/한국 진출 기준으로 시작해줘.
/aria:chat [제품 설명] 상세 분석
/aria:chat [제품 설명] 전체 분석해줘
```

### 2) `/aria:assess`

언제 쓰나:
- 판정/분류/경로를 한 번에 확정하고 싶을 때

입력 팁:
- 제품 형태(하드웨어/소프트웨어/IVD/복합)
- 침습성, 사용 기간, 활성/수동 여부
- 타깃 시장(FDA, EU MDR, MFDS)

예시:
```text
/aria:assess 비침습 ECG 웨어러블, 실시간 부정맥 탐지 및 의사 알림 기능, US/EU/KR 출시 예정
```

### 3) `/aria:project`

언제 쓰나:
- 비용/일정의 낙관-기대-비관 범위가 필요할 때
- 마일스톤/의존성 계획이 필요할 때

예시:
```text
/aria:project --format markdown
```

### 4) `/aria:report`

언제 쓰나:
- 의사결정권자/이사회/타부서 공유용 종합 브리핑이 필요할 때

예시:
```text
/aria:report Timeline Acceleration --lang en
```

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

### `classification`

목적:
- 지역별 등급 매핑 (FDA I/II/III, EU I/IIa/IIb/III, MFDS 1/2/3/4)

고품질 입력 체크리스트:
- 침습성(invasive/implantable)
- 접촉 기간(transient/short/long-term)
- 활성 장치 여부(active/passive)
- 신체 시스템 영향 범위

### `pathway`

목적:
- 등급 결과 기반 제출 경로 추천

주요 출력:
- FDA: Exempt / 510(k) / De Novo / PMA
- EU MDR: Self-declaration / Annex IV/IX/X
- MFDS: 신고/인증/허가

활용 포인트:
- 다국가 진행 시 critical path(최장 일정 시장) 먼저 확인

### `estimation`

목적:
- 비용/일정 3점 추정 (Optimistic / Expected / Pessimistic)

주요 출력:
- 비용 카테고리별 범위(컨설팅/시험/수수료/임상 등)
- 경로별 타임라인 범위

활용 포인트:
- 내부 예산안은 Expected 기준으로, 리스크 버퍼는 Pessimistic 대비로 설계

### `planning`

목적:
- 단계별 마일스톤/산출물/의존성 계획 수립

주요 출력:
- 단계별 일정, 의존성 맵, 병목 구간, 병렬화 기회

활용 포인트:
- 다국가일수록 공통 시험 항목 재사용 전략을 먼저 설계

### `compliance`

목적:
- 한국 공정경쟁규약 기반 마케팅 활동 적법성 검토

주요 입력:
- 활동 유형(샘플/기증/학술대회/제품설명회/강연/시장조사 등)
- 대상자(보건의료인/의료기관/기타)
- 금액/빈도/절차(사전심의/사후신고)

주요 출력:
- 허용/불가/조건부/사안별 판단
- 관련 조항, 위반사례, 필수 절차 체크리스트

참조 문서:
- [`aria/skills/compliance/references/regulation.md`](./skills/compliance/references/regulation.md)
- [`aria/skills/compliance/references/activity-guide.md`](./skills/compliance/references/activity-guide.md)
- [`aria/skills/compliance/references/faq.md`](./skills/compliance/references/faq.md)

## 입력 품질을 높이는 템플릿

### 제품 프로파일 템플릿

```text
제품명:
핵심 기능:
의도된 사용 목적:
주 사용자:
제품 형태(하드웨어/소프트웨어/IVD/복합):
침습성:
사용/접촉 기간:
활성/수동:
임상 데이터 보유 여부:
진출 시장(US/EU/KR):
```

### 컴플라이언스 검토 템플릿

```text
활동 유형:
대상자:
제공 내역(금액/물품/지원):
빈도:
장소/일시:
사전심의 여부:
사후신고 계획:
관련 증빙:
```

## 출력 해석 가이드

### Traffic Light

- `GREEN`: 현재 입력 기준으로 명확한 경로
- `YELLOW`: 경계 사례/추가 검증 필요
- `RED`: 현재 조건에서 진행 곤란 또는 비해당

### Summary 파일 활용

- `assess.summary.md`: 경영진 공유용 핵심 요약
- `project.summary.md`: 일정/비용 의사결정 요약
- 상세 설명이 필요하면 full report(`assess.md`, `project.md`) 확인

## 실전 플레이북

### 시나리오 A: 신제품 초기 검토

1. `/aria:chat`로 제품 프로파일 형성
2. `/aria:assess`로 규제 경로 확정
3. 불확실한 시장은 `YELLOW` 항목 중심으로 추가 조사

### 시나리오 B: 다국가 동시 진입

1. `/aria:assess`에서 시장별 경로/리스크 비교
2. `/aria:project`로 병렬/순차 전략 비용-일정 비교
3. 공통 시험 재사용 항목 우선 결정

### 시나리오 C: 임원 보고 준비

1. `assess` + `project` 결과 확보
2. `/aria:report`로 종합 브리핑 생성
3. focus area(예: Cost Control, Timeline Acceleration) 지정

### 시나리오 D: 한국 마케팅 활동 검토

1. `/aria:chat`에 활동 시나리오 상세 입력
2. `compliance` 결과의 조항/조건/사례 확인
3. 사전심의·사후신고·증빙 준비 여부 체크

## Related Docs

- 설치/온보딩: [`../README.md`](../README.md)
- Command spec:
  - [`commands/chat.md`](./commands/chat.md)
  - [`commands/assess.md`](./commands/assess.md)
  - [`commands/project.md`](./commands/project.md)
  - [`commands/report.md`](./commands/report.md)
- Connector architecture: [`CONNECTORS.md`](./CONNECTORS.md)
- Release notes: [`CHANGELOG.md`](./CHANGELOG.md)

## Disclaimer

ARIA outputs are AI-generated regulatory intelligence for reference only.
Final regulatory and compliance decisions must be validated by qualified professionals.
