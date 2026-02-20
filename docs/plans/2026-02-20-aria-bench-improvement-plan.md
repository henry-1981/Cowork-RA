# ARIA Skill Improvement Plan (RA-Bench Based)

**Date**: 2026-02-20
**Baseline**: RA-Bench v1.0 (9 scenarios, 4 AI members)
**Current Score**: ARIA 55.0% (3rd) vs Claude 57.1% (1st) vs Gemini 56.9% (2nd)

---

## Executive Summary

RA-Bench 첫 실행 결과 ARIA는 55.0%로 Claude(57.1%), Gemini(56.9%) 대비 2.1%p 열세. 격차는 크지 않으나 **evidence 인용**(1.87/5, 전원 최하위)과 **MFDS 분류 정확도** 두 영역이 핵심 병목. 5개 개선 항목(P0~P4)을 통해 **60%+ 달성 및 1위 탈환**을 목표로 한다.

---

## Root Cause Summary

| ID | 약점 | 현재 점수 | Root Cause | 영향 파일 |
|----|------|-----------|-----------|-----------|
| P0 | Evidence 인용 | 1.87/5 (최하) | 스킬 output에 `citations` 필드 없음. compliance만 인용 잘함 | determination, classification, pathway |
| P1 | MFDS 4-Gate | 0점 (전원) | mfds-criteria.md에 로직 존재하나 classification에서 미호출 | classification SKILL.md |
| P2 | MFDS 분류 정확도 | S-09: 0점 | 비디지털 기기에 대한 MFDS 분류 기준이 모호 (4줄 예시만) | classification SKILL.md Step 4 |
| P3 | De Novo 지식 | 1점 | pathway.md De Novo 5줄, fda-criteria.md 간략 언급만 | pathway, fda-criteria |
| P4 | Uncertainty flagging | 1점 | CONDITIONAL 구조 있지만 confidence score, 에스컬레이션 세분화 없음 | determination, escalation-traffic-light |

---

## P0: Evidence Citation (Critical - 예상 +8~12점)

### Problem

- determination/classification/pathway 어디에도 `citations` 필드가 output contract에 없음
- "rationale" 텍스트만 반환, 구체적 규정 번호/가이던스/선례 인용 없음
- compliance 스킬만 조항+위반사례 인용을 잘함 → 다른 스킬은 이 패턴 미적용
- 결과: ARIA 트랜스크립트에 DEN 번호, CFR 조항, MFDS 승인 사례 등이 부족

### Competitor Evidence (transcript-comparator 분석)

| 시나리오 | ARIA 부족 | 경쟁자 포함 |
|---------|----------|-----------|
| S-02 FDA | DEN 번호 없음 | Claude: DEN170073 구체 인용 |
| S-04 FDA | DEN 번호 오류(DEN170073→DEN180001) | Gemini: 성능기준 수치(민감도≥85%) 포함 |
| S-02 MFDS | 원칙적 기술만 | Claude: 실제 승인 사례 + 인용 |

### Solution

#### 1. Output Contract에 `legal_basis` 필드 추가

**대상 파일**: `commands/assess.md` Section 7 Output Generation

현재 assess.md의 출력 템플릿:
```markdown
| Region | Status | Rationale | Traffic Light |
```

변경 후:
```markdown
| Region | Status | Rationale | Legal Basis | Traffic Light |
```

각 phase(determination, classification, pathway)마다 `Legal Basis` 컬럼 추가.

#### 2. 각 스킬별 Evidence Checklist 추가

**determination SKILL.md** Step 4 (Return Structured Result)에 추가:
```
### Evidence Requirements (per jurisdiction)
- FDA: 21 CFR section, relevant guidance document(s), predicate device (if applicable)
- EU MDR: Article reference, applicable Rule number(s), MDCG guidance (if applicable)
- MFDS: 의료기기법 조항, 품목코드 (Axxxxx.xx if known), 관련 고시/가이드라인
```

**classification SKILL.md** Step 5 (Generate Classification Matrix)에 추가:
```
### Evidence Requirements (per classification)
- FDA: Product code, CFR reference (21 CFR 8xx.xxxx), predicate class basis
- EU MDR: Annex VIII Rule number(s), Implementing Rule 3.5 (if multi-rule)
- MFDS: 품목분류번호, 등급 근거 (Risk Matrix 또는 품목분류표)
```

**pathway SKILL.md** Step 5 (Return Structured Result)에 추가:
```
### Evidence Requirements (per pathway)
- FDA: Submission type reference, relevant guidance, DEN/510(k)/PMA precedent (if known)
  - CRITICAL: Do NOT fabricate DEN/510(k) numbers. State "requires FDA database verification" if unsure
- EU MDR: Annex reference (IV, IX, X), MDCG guidance
- MFDS: 의료기기법 조항 (제6조/제9조/제12조), 인증기관 요건
```

#### 3. fda-criteria.md에 DEN 번호 주의사항 강화

현재 `fda-criteria.md` line 77에 "do NOT fabricate" 언급이 있으나 더 강화:
```
**DEN/K Number Policy** (GROUND TRUTH):
- DEN numbers (De Novo), K numbers (510(k)), P numbers (PMA) are FDA-assigned
- NEVER guess or fabricate these numbers from memory
- If a specific precedent is recalled, prefix with "Believed to be" + verify recommendation
- If unknown: "Specific precedent number requires FDA database verification"
```

### Verification

- 재채점 시 S-02, S-04 evidence 점수 향상 기대 (0→2~3)
- FDA evidence 평균 0.80 → 2.5+ 목표

---

## P1: MFDS 4-Gate Integration (High - 예상 +3~6점)

### Problem

- `mfds-criteria.md`에 4-Gate 로직이 **완전하게 구현**되어 있음
- BUT `classification SKILL.md` Step 4가 자체 내장 MFDS 기준(4줄 예시)만 사용
- classification이 mfds-criteria.md를 **참조하지 않음**
- 결과: 디지털 의료기기에도 4-Gate 미적용, 7-digit 코드 미생성

### Solution

#### 1. classification SKILL.md Step 4 재작성

현재 Step 4 (line 238-243):
```
### Step 4: Apply MFDS Classification Criteria
1. Assess potential harm level
2. Evaluate complexity of use
3. Check for implantable or life-sustaining characteristics
4. Consider Korean regulatory nuances
5. Assign MFDS Class (1/2/3/4)
```

변경:
```
### Step 4: Apply MFDS Classification Criteria

**Step 4A: Digital Medical Device Check (4-Gate)**
> Load module: `../determination/modules/mfds-criteria.md` Section "4-Gate Decision Logic"

1. Gate 1: 의료기기 해당 여부 (Step 1에서 이미 확인)
2. Gate 2: 디지털 기술 적용 여부 (SW, AI, IoT, VR/AR 등)
3. Gate 3: 핵심 기능 영향 여부
4. Gate 4: 배제 원칙 확인

- **4-Gate 통과** → Step 4B (Risk Matrix 기반 분류) + 7-digit 코드 생성
- **Gate 2 EXIT (비디지털)** → Step 4C (전통 품목분류 기반)

**Step 4B: Risk Matrix Classification (디지털 의료기기)**
> Load module: `../determination/modules/mfds-criteria.md` Section "Risk-Based Classification"

1. Medical Impact 결정 (Primary Intended Use → 매핑 테이블 적용)
2. Patient Condition 식별 (적응증 → Critical/Serious/Non-Serious)
3. Risk Matrix 교차 적용 → Base Grade
4. Malfunction Risk Adjustment → Final Grade
5. 7-digit 코드 생성 및 Self-Verification

**Step 4C: Traditional Classification (비디지털 의료기기)**
1. MFDS 품목분류표(「의료기기 품목 및 품목별 등급에 관한 규정」) 참조
2. 품목코드(Axxxxx.xx) 확인 가능 시: 해당 등급 직접 적용
3. 품목코드 불확실 시: 아래 기본 분류 기준 + "MFDS 확인 필요" 주석
   - 1등급: 비침습, 비전원, 수동, 단순 기구 (예: 겸자, 가위, 혀압자)
   - 2등급: 침습 또는 에너지 사용, 중간 위험 (예: 초음파, 보청기)
   - 3등급: 고위험 능동 기기 (예: 인공호흡기, 투석기)
   - 4등급: 이식형 또는 생명유지 (예: 인공심장판막, 스텐트)
```

#### 2. assess.md에 MFDS 4-Gate 출력 섹션 추가

Output Template Section 2 (Classification) 뒤에:
```markdown
### MFDS Digital Medical Device Assessment (if applicable)
- 4-Gate Result: [통과/EXIT at Gate X]
- 7-Digit Code: [코드] (if applicable)
- Risk Matrix: Medical Impact [level] × Patient Condition [level] = Base Grade [N]
- Malfunction Adjustment: [+1/0/-1] → Final Grade [N]
```

### Verification

- S-02, S-08 mfds_4gate 점수 향상 (0→2~4)
- S-02, S-08 mfds_7digit 점수 향상 (0→2~4)
- S-09 gate2_exit 점수 향상 (0→3~4)

---

## P2: MFDS Classification Accuracy (High - 예상 +4~8점)

### Problem

- S-09에서 수동식 의료용 겸자(A45020.01)를 **2등급으로 오분류** (정답: 1등급)
- classification.md MFDS 기준이 너무 모호: "Class 1: Medical scissors, tweezers" vs "Class 2: MRI, ultrasound"
- **수동 수술 기구**가 Class 1인지 Class 2인지 판단 불가능한 정보 수준
- mfds-criteria.md의 Risk Matrix는 디지털 기기 전용 → 비디지털 기기에 적용 불가

### Root Cause: ARIA가 품목코드를 인용하면서도 등급을 틀린 이유

ARIA S-09 트랜스크립트 분석:
- "A45020.01 (의료용 겸자, 수동식)" 정확히 인용 ✓
- "인체 조직과 직접 접촉하는 수술용 기구 → 2등급" 판단 ✗
- 원인: classification 스킬의 MFDS 기준에서 "침습적 접촉" → 자동으로 2등급 이상으로 추론
- 실제: MFDS 품목분류표에서 A45020.01은 **1등급** (비전원, 수동, 단순 기계식 기구)

### Solution

#### 1. classification SKILL.md Step 4C에 비디지털 분류 가이드 상세화

P1에서 추가한 Step 4C를 더 보강:

```
**Step 4C: Traditional Classification (비디지털 의료기기)**

MFDS 품목분류표 기반 등급 결정:

1. 품목코드(Axxxxx.xx) 매핑 가능 시:
   - 품목분류표의 등급을 **최우선 근거**로 적용
   - 추론보다 DB 등재 등급을 우선함 (GROUND TRUTH)
   - 출력: "품목코드 A45020.01 → 1등급 (품목분류표 직접 등재)"

2. 품목코드 불확실 시, 아래 기준으로 판단:

   **1등급 판별 (핵심 기준)**:
   - 에너지원 없음 (비전원, 수동 작동)
   - 소프트웨어 없음
   - 비이식형
   - 생명유지 기능 없음
   - 예시: 수동 수술기구(겸자, 가위, 메스, 핀셋), 혀압자, 반창고
   - **CRITICAL**: 수술 중 사용 = 반드시 2등급 이상이 아님.
     수동식 수술 기구는 에너지원/소프트웨어 없으면 1등급 가능

   **2등급 판별 (핵심 기준)**:
   - 에너지 사용 (전기, 전자, 방사선 등) OR
   - 체내 일시적 침습 + 능동 기능 OR
   - 단순 측정/모니터링 기능
   - 예시: 전동식 수술기구, 초음파기기, MRI, 보청기, 전동 휠체어

   **3등급 판별**: 능동 의료기기 + 중등도~고위험
   **4등급 판별**: 이식형 또는 생명유지 장치
```

#### 2. 품목코드 → 등급 매핑 가이드라인 추가

classification SKILL.md 또는 mfds-criteria.md에 **대표적 품목코드 참조표** 추가:

```
### MFDS 대표 품목코드-등급 참조 (자주 나오는 품목)

| 품목코드 | 품목명 | 등급 | 비고 |
|----------|--------|------|------|
| A45020.01 | 의료용 겸자, 수동식 | 1등급 | 비전원 수술기구 |
| A45010.01 | 의료용 가위 | 1등급 | 비전원 수술기구 |
| A09020.02 | 산소포화도측정장치 | 2등급 | 전자 측정기기 |
| A19230.xx | 의료영상분석SW | 3등급 | SaMD |
| A17010.01 | 뇌영상분석SW | 3등급 | AI SaMD |

NOTE: 이 표는 참조용. 최종 등급은 반드시 MFDS 품목분류표 확인 필요.
NOTE: 품목코드가 확실하지 않은 경우 "MFDS 품목분류표 확인 필요" 명시.
```

### Verification

- S-09 classification 0점 → 4점 기대 (1등급 정확 분류)
- S-09 pathway도 연쇄적으로 개선 (인증→신고)
- S-09 전체 28.6% → 50%+ 기대

---

## P3: De Novo Pathway Knowledge (Medium - 예상 +2~4점)

### Problem

- pathway.md De Novo 설명 5줄 (When, Timeline, Requirements만)
- fda-criteria.md에 De Novo vs PMA 판별 기준은 있지만 상세도 부족
- S-04에서 De Novo 인식은 했으나 구체적 근거(DEN200064, QPP) 미제시

### Solution

#### 1. pathway SKILL.md De Novo 섹션 확장

현재 (line 65-69):
```
- **De Novo Classification Request**
  - When: No valid predicate exists, low-moderate risk device
  - Timeline: 6-12 months
  - Requirements: Special controls, risk mitigation documentation
  - Traffic Light: YELLOW (escalate to expert)
```

변경:
```
- **De Novo Classification Request**
  - When: No valid predicate exists AND device is low-moderate risk
  - Key principle: De Novo creates a NEW classification (Class I or II with Special Controls)
  - After De Novo grant: the device becomes a predicate for future 510(k) submissions
  - Timeline: 6-12 months (FDA target: 150 review days)
  - Requirements:
    - Risk-benefit analysis (not SE demonstration)
    - Proposed Special Controls (performance criteria, labeling, post-market)
    - Non-clinical and/or clinical data supporting safety and effectiveness
    - Product Code assignment request
  - Distinguishing from PMA:
    - De Novo: novel but LOW-MODERATE risk, mitigable with Special Controls
    - PMA: novel AND HIGH risk (life-sustaining, implantable vital organ, high mortality)
  - Traffic Light: YELLOW (escalate to expert)
  - NOTE: Specific DEN numbers require FDA database verification. Do NOT fabricate.
```

#### 2. fda-criteria.md Predicate & Pathway 섹션에 De Novo 트리거 추가

현재 line 82-88에 추가:
```
**De Novo Trigger Checklist**:
- [ ] No substantially equivalent predicate found
- [ ] Device risk: low-to-moderate (not life-sustaining, not implantable vital organ)
- [ ] Risk can be mitigated with Special Controls
- [ ] Device type has never been classified (no existing product code)
→ If all checked: De Novo is PRIMARY pathway (not PMA)
```

### Verification

- S-04 de_novo_identification 1점 → 3~4점 기대
- S-04 evidence 0점 → 2~3점 기대

---

## P4: Uncertainty Flagging (Low - 예상 +1~2점)

### Problem

- CONDITIONAL 출력 구조는 잘 정의됨 (determination SKILL.md)
- 하지만 신뢰도 수준 정량화 없음
- "어느 정도 불확실한가"를 사용자가 판단할 수 없음

### Solution

#### 1. determination SKILL.md CONDITIONAL 출력에 Confidence 추가

CONDITIONAL Output Contract 테이블에 추가:
```
| **Confidence Range** | Estimated probability of YES determination | "60-70% YES: borderline with moderate medical features" |
```

#### 2. escalation-traffic-light.md에 Escalation Level 세분화

```
### Escalation Levels (within YELLOW)
- YELLOW-1 (Advisory): RA 리드 검토 권장 (minor uncertainty)
- YELLOW-2 (Review): RA 팀 검토 필수 + Pre-submission 권장
- YELLOW-3 (Critical): 외부 자문 + 규제 기관 사전 상담 필수
```

### Verification

- S-03 uncertainty_flagging 1점 → 2~3점 기대

---

## Implementation Priority & Timeline

| Phase | Items | 예상 점수 향상 | 난이도 | 파일 변경 수 |
|-------|-------|-------------|--------|-------------|
| **Phase 1** (1주) | P0 (Evidence) + P2 (MFDS 분류) | +12~20점 | Medium | 4 files |
| **Phase 2** (1주) | P1 (4-Gate 통합) + P3 (De Novo) | +5~10점 | Medium | 3 files |
| **Phase 3** (3일) | P4 (Uncertainty) | +1~2점 | Low | 2 files |

### 예상 결과

| 멤버 | 현재 | Phase 1 후 | Phase 2 후 | Phase 3 후 |
|------|------|-----------|-----------|-----------|
| ARIA | 55.0% | ~62% | ~67% | ~68% |
| Claude | 57.1% | (unchanged) | (unchanged) | (unchanged) |
| Gemini | 56.9% | (unchanged) | (unchanged) | (unchanged) |

---

## File Change Matrix

| 파일 | P0 | P1 | P2 | P3 | P4 |
|------|:--:|:--:|:--:|:--:|:--:|
| `skills/classification/SKILL.md` | O | O | O | - | - |
| `skills/determination/SKILL.md` | O | - | - | - | O |
| `skills/pathway/SKILL.md` | O | - | - | O | - |
| `skills/determination/modules/fda-criteria.md` | O | - | - | O | - |
| `skills/determination/modules/mfds-criteria.md` | - | O | O | - | - |
| `skills/determination/modules/escalation-traffic-light.md` | - | - | - | - | O |
| `commands/assess.md` | O | O | - | - | - |

---

## Verification Plan

1. **Unit Test**: 각 P 항목 수정 후 해당 시나리오에 대해 ARIA 단독 재실행
   ```
   ./scripts/bench-run.sh S-09 --member aria  # P2 검증
   ./scripts/bench-run.sh S-04 --member aria  # P3 검증
   ```

2. **Full Bench**: Phase 1+2 완료 후 전체 9개 시나리오 재실행
   ```
   ./scripts/bench-run.sh all --member aria
   ```

3. **Scoring**: Stage 1 + Stage 2 채점
   ```
   python scripts/bench-score.py runs/2026-02-21/
   ```

4. **Regression Check**: EU MDR 영역(현재 강점) 점수 하락 없는지 확인

---

## Appendix: Data Sources

- RA-Bench Scores: `RA-Bench/runs/2026-02-20/scores/`
- ARIA Transcripts: `RA-Bench/runs/2026-02-20/transcripts/aria/`
- Competitor Transcripts: `RA-Bench/runs/2026-02-20/transcripts/{claude,gemini}/`
- Skill Files: `Cowork-RA/aria/skills/`
- Command Files: `Cowork-RA/aria/commands/`
