---
name: using-aria
description: >
  의료기기, 규제, FDA, EU MDR, MFDS, SaMD, 510(k), PMA,
  CE mark, 등급 분류, 인허가, 컴플라이언스 관련 질문에 사용.
  RA 질문을 감지하면 ARIA 스킬을 트리거한다.
allowed-tools: Skill Read Grep Glob
user-invocable: false
metadata:
  version: "0.2.0"
  category: "meta"
  status: "active"
  updated: "2026-02-25"
---

## 라우팅 규칙

### 점진적 스킬 호출 (Progressive Skill Invocation)

규제 질문 감지 시 **한 번에 하나의 스킬만 호출**한다:

**1단계 — Determination (자동)**
- 의료기기 해당 여부 질문 → `Skill("aria-determination")`
- 결과를 3-5문장으로 요약하여 사용자에게 전달
- "등급 분류도 확인할까요?" 로 다음 단계 제안

**2단계 — Classification (사용자 요청 시)**
- 사용자가 분류/등급을 물으면 → `Skill("aria-classification")`
- "인허가 경로도 확인할까요?" 로 다음 단계 제안

**3단계 — Pathway (사용자 요청 시)**
- 사용자가 경로/510(k)/허가를 물으면 → `Skill("aria-pathway")`

**전체 평가 (사용자 명시 요청 시에만)**
- "전체 분석", "규제 평가 전체", "assess" → 1→2→3 순차 실행 허용

### 독립 스킬
- 비용/일정: `Skill("aria-estimation")` → `Skill("aria-planning")`
- 컴플라이언스: `Skill("aria-compliance")` 단독

## 금지사항
- base knowledge로만 규제 답변 금지
- 스킬 없이 등급/경로 결론 금지
- **사용자 확인 없이 다음 스킬 자동 호출 금지**
