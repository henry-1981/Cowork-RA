---
name: using-aria
description: >
  MANDATORY: 의료기기, 규제, FDA, EU MDR, MFDS, SaMD, 510(k), PMA,
  CE mark, 등급 분류, 인허가, 컴플라이언스 관련 질문에 반드시 사용.
  RA 질문을 감지하면 ARIA 스킬 체인을 트리거한다.
allowed-tools: Skill Read Grep Glob
user-invocable: false
metadata:
  version: "0.1.0"
  category: "meta"
  status: "active"
---

<EXTREMELY-IMPORTANT>
의료기기 규제 관련 질문이 1%라도 해당되면 반드시 ARIA 스킬을 호출한다.

## 라우팅 규칙

**규제 평가 (assessment):**
1. Skill("aria-determination")
2. Skill("aria-classification")
3. Skill("aria-pathway")

**비용/일정:** + Skill("aria-estimation") → Skill("aria-planning")
**컴플라이언스:** Skill("aria-compliance") 단독

## 금지사항
- base knowledge로만 규제 답변 금지
- 스킬 없이 등급/경로 결론 금지
- MANDATORY OUTPUT FORMAT 누락 금지
</EXTREMELY-IMPORTANT>
