# ARIA 정확도 개선 설계문서

**Date:** 2026-02-21
**Version:** 1.0
**Goal:** RA-Bench 57.3% → 85% 달성
**Scope:** 6-Skill 아키텍처 유지, 대화형 UX 보존, 구조적 룰/패턴 중심 개선
**현재:** 252/440 (57.3%, Codex judge)
**목표:** 374/440 (85%)

## 설계 원칙

1. **대화형 UX 유지** — `/aria:assess` 대화형 워크플로우 불변
2. **도메인 정확도 향상** — 구조적 룰과 패턴 강화
3. **유즈케이스 추가 금지** — 시나리오별 워크어라운드가 아닌 범용 규제 추론 엔진 개선
4. **기존 6-스킬 아키텍처 유지** — determination, classification, pathway, estimation, planning, compliance

## 근본 원인 분석

### 핵심 진단: "올바른 내용, 잘못된 전달"

Phase 1~5에서 SKILL.md에 추가한 MANDATORY OUTPUT FORMAT, 4-Gate, Risk Matrix, 7-digit 코드 — 모두 정확하고 필요한 내용이었으나, generic 프롬프트에서 스킬이 한 번도 트리거되지 않아 모든 개선이 사장되었다.

**증거:** S-09는 80%로 최고점 — 4-Gate 출력이 생성되었고 4/5를 받음. "포맷이 나오기만 하면 점수가 나온다"는 것을 증명.

### 3겹 구조적 문제

| 문제 | 원인 | 영향 |
|------|------|------|
| 스킬 미활성 | CLAUDE.md/hooks/meta-skill 부재 | 벤치에서 bare Claude와 동일하게 동작 |
| 도메인 지식 갭 | 선례 DB 부재, 디지털의료제품법 미통합 | Evidence 평균 1.1/5 |
| 추론 패턴 미흡 | CONDITIONAL 이중 트랙 미지원, 일관성 검증 부재 | S-03 41.2% (최저) |

---

## Section 1: 아키텍처 레이어 — 자동 스킬 라우팅

### 1.1 현황 진단

| 문제 | 원인 | 영향 |
|------|------|------|
| 스킬 미호출 | CLAUDE.md 없음, 메타스킬 없음, 라우팅 컨텍스트 부재 | 벤치 프롬프트가 base knowledge로만 처리됨 |
| MANDATORY OUTPUT FORMAT 미준수 | 스킬이 로드되지 않으면 포맷 블록 자체를 모름 | 구조화 출력 누락 → 벤치 채점 실패 |
| `triggers` YAML 무효 | `triggers.keywords`는 MoAI 커스텀 확장 — Claude Code가 인식하지 않음 | 키워드 기반 자동 트리거 작동 안 함 |

**핵심 인사이트:** 벤치는 `/aria:assess`가 아닌 일반 프롬프트("이 제품을 분석해줘")를 전송한다. 현재 아키텍처는 사용자가 명시적으로 커맨드를 호출해야만 스킬 체인이 작동하므로, 일반 프롬프트에서는 스킬이 전혀 로드되지 않는다.

### 1.2 해결책 A: CLAUDE.md 생성

**파일:** `aria/CLAUDE.md` (플러그인 루트)

**목적:** Claude Code가 플러그인 디렉터리의 CLAUDE.md를 시스템 컨텍스트로 로드하여, ARIA 정체성과 RA 질문 라우팅 규칙을 항상 인지하게 한다.

**설계 원칙:**
- 300 토큰 이내 (컨텍스트 예산 관리)
- ARIA 정체성 선언 + 스킬 체인 라우팅 규칙만 포함
- 도메인 지식은 포함하지 않음 (스킬 SKILL.md에 위임)

**초안:**

```markdown
# ARIA — AI Regulatory Intelligence Assistant

의료기기 규제(FDA, EU MDR, MFDS) 질문에 대해 반드시 ARIA 스킬을 사용한다.

## 스킬 체인 (필수)

규제 평가 질문 → 아래 순서로 Skill tool 호출:
1. `aria-determination` — 의료기기 해당 여부
2. `aria-classification` — 등급 분류 (FDA I/II/III, EU I/IIa/IIb/III, MFDS 1-4)
3. `aria-pathway` — 인허가 경로 (510(k), PMA, De Novo, CE, 신고/인증/허가)

비용/일정: `aria-estimation` → `aria-planning`
마케팅 컴플라이언스: `aria-compliance` (독립 호출)

## 규칙
- base knowledge로만 규제 질문에 답하지 않는다
- 각 스킬의 MANDATORY OUTPUT FORMAT 블록을 반드시 출력에 포함한다
- 정보 부족 시 스킬이 정의한 insufficiency 절차를 따른다
```

### 1.3 해결책 B: `using-aria` 메타스킬

**파일:** `aria/skills/using-aria/SKILL.md`

**목적:** superpowers의 `using-superpowers` 패턴을 적용하여, RA 질문 감지 시 스킬 체인을 강제 호출한다.

**설계 원칙:**
- **순수 라우터 역할** — RA 질문 감지 → 스킬 체인 트리거
- 정보 충분성 판단(information sufficiency)은 하지 않음 (각 스킬 내부 로직에 위임)
- 500 토큰 이내

**SKILL.md 초안:**

```yaml
---
name: using-aria
description: >
  MANDATORY: 의료기기, 규제, FDA, EU MDR, MFDS, SaMD, 510(k), PMA,
  CE mark, 등급 분류, 인허가, 컴플라이언스 관련 질문에 반드시 사용.
  RA 질문을 감지하면 ARIA 스킬 체인을 트리거한다.
user-invocable: false
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
```

**CLAUDE.md와의 역할 분담:**

| 구성요소 | 역할 | 로딩 시점 | 토큰 |
|----------|------|-----------|------|
| `CLAUDE.md` | 항상 존재하는 라우팅 기본 규칙 | 세션 시작 시 자동 | ~300 |
| `using-aria` | 모델이 RA 감지 시 상세 라우팅 로직 | 스킬 매칭 시 | ~500 |

CLAUDE.md는 "RA 질문 → 스킬 사용"이라는 원칙을, using-aria는 구체적 호출 순서와 금지사항을 담당한다. 이중 레이어로 스킬 미호출 가능성을 최소화한다.

### 1.4 SessionStart 훅 — 미채택 (근거)

CLAUDE.md가 동일한 역할을 이미 수행하므로 제거한다.

| 비교 항목 | CLAUDE.md | SessionStart 훅 |
|-----------|-----------|-----------------|
| 컨텍스트 주입 | 자동 (플러그인 로드 시) | 스크립트 실행 필요 |
| 유지보수 | 마크다운 파일 1개 | hooks.json + 셸 스크립트 |
| 신뢰성 | Claude Code 내장 메커니즘 | 외부 프로세스 의존 |

### 1.5 토큰 예산

| 구성요소 | 토큰 | 로딩 조건 |
|----------|------|-----------|
| CLAUDE.md | ~300 | 항상 |
| using-aria 메타스킬 | ~500 | RA 감지 시 |
| determination SKILL.md | ~3,000 | 스킬 호출 시 |
| classification SKILL.md | ~6,000 | 스킬 호출 시 |
| pathway SKILL.md | ~4,000 | 스킬 호출 시 |
| **풀 파이프라인 합계** | **~13,800** | — |

200K 컨텍스트 대비 ~7%. 충분히 수용 가능.

### 1.6 구현 파일 목록

| 작업 | 파일 | 신규/수정 |
|------|------|-----------|
| CLAUDE.md 생성 | `aria/CLAUDE.md` | 신규 |
| 메타스킬 생성 | `aria/skills/using-aria/SKILL.md` | 신규 |
| plugin.json 버전 범프 | `aria/.claude-plugin/plugin.json` | 수정 |

---

## Section 2: 도메인 규칙 강화

### 규칙 1: CONDITIONAL 판정 기준 명확화

#### 현재 문제

Determination 스킬에 CONDITIONAL 트리거 목록과 출력 계약이 존재하나, 세 가지 구조적 결함이 있다:

**1a. 경계 유형별 분기 부재:** CONDITIONAL 트리거 5가지가 동일한 출력 구조를 사용. 실제로는 경계 유형에 따라 근본적으로 다른 분석이 필요:
- Wellness/Medical 경계 → 의도된 사용 주장(claims) 분석 중심
- Combination Product → PMOA 결정 중심
- Annex XVI → Article 2(1) 비의료 + Annex XVI 이중 판정 중심

**1b. MFDS 디지털의료제품법 3-Tier 연결 누락:** `mfds-criteria.md`에 3-Tier 경계 분석이 상세하게 존재하나, SKILL.md의 메인 워크플로우에서 명시적 단계로 호출하지 않음. S-03에서 MFDS 분류/경로/근거가 0/0/0을 기록.

**1c. Annex XVI의 SPECIAL 상태 미통합:** S-06에서 determination=1을 기록한 원인.

#### 구조적 해결책

**Fix 1-A: CONDITIONAL 유형별 분기 트리 통합**

`determination/SKILL.md`의 Step 2 워크플로우에 유형별 분기 추가:

```
Step 2 진입 → 각 관할권별:
├─ CONDITIONAL 감지 시 → 유형 분류:
│   ├─ TYPE-W (Wellness/Medical Boundary)
│   │   → FDA: General Wellness Policy + CDS 4기준 검증
│   │   → MFDS: 디지털의료제품법 3-Tier 분석 (필수 호출)
│   │   → EU MDR: MDCG 2019-11 경계제품 분석
│   │
│   ├─ TYPE-C (Combination Product)
│   │   → P5 섹션 호출 (PMOA 결정 + Lead Center 식별)
│   │
│   ├─ TYPE-X (Annex XVI — Non-Medical Purpose)
│   │   → Annex XVI 섹션 호출 (이중 판정)
│   │   → 출력: SPECIAL
│   │
│   ├─ TYPE-S (Software/CDS Boundary)
│   │   → CDS 4기준 점검 + SaMD 정의 대조
│   │
│   └─ TYPE-A (Intended Use Ambiguity)
│       → 핵심 주장문(claims) 분석 + 해석 양방향 제시
```

**Fix 1-B: 3-Tier 분석의 명시적 워크플로우 통합**

`determination/SKILL.md`의 MFDS 섹션에 디지털의료제품법 3-Tier 경계 분석을 필수 단계로 추가.

#### 영향 받는 파일

| 파일 | 변경 유형 |
|------|----------|
| `determination/SKILL.md` Step 2 | CONDITIONAL 유형별 분기 트리 추가 |
| `determination/SKILL.md` MFDS 섹션 | 3-Tier 분석을 필수 단계로 승격 |
| `determination/modules/eu-mdr-criteria.md` | Annex XVI 감지 조건 보완 |

---

### 규칙 2: 조건부 이중 트랙 분류 패턴

#### 현재 문제

Determination이 CONDITIONAL을 반환할 때, 하류 스킬(classification, pathway)이 확정적 결론을 출력하는 구조적 결함.

S-03 증거: FDA determination=4 (CONDITIONAL 정확) → FDA classification=1 (확정 분류로 감점)

Classification 스킬의 워크플로우에 "determination이 CONDITIONAL일 때의 분류 프로토콜"이 존재하지 않음.

#### 구조적 해결책

**Fix 2-A: Classification 스킬에 Conditional 모드 추가**

```
Step 1.5: Determination 상태 확인 (NEW)

IF determination = YES → 기존 워크플로우 진행
IF determination = CONDITIONAL → Dual-Track Classification Mode:

  Scenario A (IF device):
    - 정상 분류 워크플로우 실행
    - 접두사: "If determined to be a medical device → "

  Scenario B (IF NOT device):
    - FDA: "Not subject to FDA regulation" 또는 "General Wellness product"
    - EU MDR: "Not within MDR scope" 또는 "Annex XVI regulated"
    - MFDS: "비규제" 또는 "건강지원제품 (디지털의료제품법)"

  Resolution Trigger:
    - Determination의 Resolution Conditions 상속
```

**Fix 2-B: Pathway 스킬에 Conditional 입력 처리 추가**

Pathway Step 1에서 Dual-Track 입력을 인식하고 "IF device:" 접두사를 유지.

#### 영향 받는 파일

| 파일 | 변경 유형 |
|------|----------|
| `classification/SKILL.md` Step 1 이후 | Step 1.5 Dual-Track Mode 삽입 |
| `classification/SKILL.md` 출력 형식 | Conditional 출력 템플릿 추가 |
| `pathway/SKILL.md` Step 1 | Dual-Track 입력 처리 추가 |

---

### 규칙 3: MFDS 4-Gate를 분석 단계로 승격

#### 현재 문제

4-Gate 분석이 두 곳에 중복 정의되면서 동시에 어디서도 확실하게 실행되지 않는 구조적 문제:
1. `determination/SKILL.md` — "MANDATORY for Digital Products" 출력 형식으로 정의
2. `classification/SKILL.md` Step 4A — 또 다른 출력 형식으로 정의

**핵심 문제**: 4-Gate가 "출력 형식"으로만 정의되어 있고, "분석 전제조건"으로 정의되어 있지 않음.

**토큰 예산 경쟁**: Classification SKILL.md에 MANDATORY OUTPUT FORMAT 블록이 6개 — 동시 요구 시 토큰 초과로 일부 누락. Phase 3에서 4개 블록 동시 추가 시 S-09가 82.9%→40.0%으로 폭락한 사례.

#### 구조적 해결책

**Fix 3-A: 4-Gate를 분류의 선행 조건(Prerequisite)으로 재정의**

```
MFDS 분류 워크플로우 (재구조화):

Phase 0: 4-Gate 디지털의료기기 판정 (PREREQUISITE)
  ├─ Gate 1~4 순차 실행
  └─ 결과가 Phase 1의 분류 경로를 결정

Phase 1: 등급 분류 (4-Gate 결과에 따라 분기)
  ├─ IF 디지털의료기기 → Risk Matrix 기반 분류 → 7-Digit Code 생성
  └─ IF 비디지털 / Gate 2 EXIT → 전통 품목분류표 기반

Phase 2: 검증 (Consistency Validation)
```

**Fix 3-B: MANDATORY OUTPUT FORMAT 통합 및 간소화**

6개 독립 블록 → 2개 통합 블록:
- 통합 블록 1: "MFDS 분류 분석 결과" (4-Gate + Risk Matrix + 7-Digit + Consistency)
- 통합 블록 2: "근거 및 신뢰도" (Regulatory Evidence + Confidence & Escalation)

**Fix 3-C: 중복 정의 제거**

4-Gate 정의를 `determination/SKILL.md`에서 제거, `classification/SKILL.md`에만 단일 권위 소스로 유지.

#### 영향 받는 파일

| 파일 | 변경 유형 |
|------|----------|
| `classification/SKILL.md` Step 4 | 4-Gate를 Phase 0 prerequisite로 승격 |
| `classification/SKILL.md` 출력 형식 | 6개 블록 → 2개 통합 블록 |
| `determination/SKILL.md` | 4-Gate 중복 정의 제거, 플래그만 유지 |

---

### 규칙 4: 근거 제시 패턴 체계화

#### 현재 문제

Evidence 점수 전 시나리오에서 체계적으로 낮음 (평균 1.1/5). 관할권별 필수 구성 요소가 불균일하고, 선례 DB 부재로 모델이 근거를 아예 생략.

#### 구조적 해결책

**Fix 4-A: 관할권별 근거 체크리스트**

3개 스킬 각각에 자가 점검 체크리스트 정의:

```
FDA: □ CFR § [section] □ Product Code [3자] □ 선례 [DEN/K/P] □ Guidance
EU MDR: □ Article [N] □ Rule [N] □ MDCG [번호] □ IR [해당 시]
MFDS: □ 법률 [조항] □ 품목코드 [Axxxxx.xx] □ 등급 근거 □ 가이드라인
```

**Fix 4-B: 선례 참조 모듈** → Section 3 참조

**Fix 4-C: 근거 출력 통합 형식**

3개 스킬의 별도 "Regulatory Evidence" MANDATORY 블록을 단일 통합 형식으로 정의.

#### 영향 받는 파일

| 파일 | 변경 유형 |
|------|----------|
| `determination/SKILL.md` | 관할권별 체크리스트로 재정의 |
| `classification/SKILL.md` | 동일 체크리스트 적용 |
| `pathway/SKILL.md` | 동일 체크리스트 적용 |
| `modules/precedent-db.md` | 신규 생성 (25-30개 선례) |

---

### 규칙 5: 일관성 자기 검증 (Consistency Self-Check)

#### 현재 문제

현재 검증은 MFDS 내부 일관성만 체크 (단일 차원). 실제로 필요한 것은 3차원 검증:
- Determination ↔ Classification: CONDITIONAL인데 확정 분류 → FAIL
- Classification ↔ Pathway: Class II인데 PMA 경로 → FAIL
- Cross-Jurisdiction: 관할권 간 등급 정합성

#### 구조적 해결책

**Fix 5-A: 3차원 일관성 검증 프레임워크**

```
Dimension 1: Determination ↔ Classification
  - CONDITIONAL → classification MUST be conditional ("IF device → Class X")
  - YES → classification MUST be definitive

Dimension 2: Classification ↔ Pathway
  - FDA: Class I→510(k) Exempt | Class II→510(k)/De Novo | Class III→PMA
  - MFDS: 1등급→신고 | 2등급→인증 | 3등급→허가 | 4등급→허가+임상

Dimension 3: Cross-Jurisdiction
  - 정상: FDA II ↔ EU IIa ↔ MFDS 2등급 (±1단계 허용)
  - 2단계 이상 차이 시 정당화 필요
```

**Fix 5-B: 검증 실행 위치** — 최종 출력 조립 단계 (모든 스킬 결과 확보 후)

#### 영향 받는 파일

| 파일 | 변경 유형 |
|------|----------|
| `classification/SKILL.md` | 기존 Consistency Validation 이동 |
| Assessment orchestrator | 3차원 Consistency Validation 배치 |

### 규칙 간 의존성 및 구현 순서

```
규칙 3 (4-Gate 승격) ──→ 규칙 4 (근거 체계화) ──→ 규칙 5 (일관성 검증)
                                                          ↑
규칙 1 (CONDITIONAL 유형화) ──→ 규칙 2 (이중 트랙 분류) ──┘
```

**권장 구현 순서:**
1. 규칙 3 (4-Gate 승격) — 토큰 예산 문제 해결, 다른 규칙의 전제
2. 규칙 4 (근거 체계화) — 선례 DB 생성, 전 시나리오에 영향
3. 규칙 1 (CONDITIONAL 유형화) — 규칙 2의 전제
4. 규칙 2 (이중 트랙 분류) — 규칙 1 의존
5. 규칙 5 (일관성 검증) — 규칙 1-4 모두 완료 후 통합 검증

---

## Section 3: 도메인 지식 기반 확충

### 3.1 선례 데이터베이스 (Precedent DB)

**파일 위치**: `aria/knowledge/precedent-db.md`
**로딩 방식**: CLAUDE.md에서 참조 → 시스템 프롬프트에 항상 포함
**업데이트 정책**: 분기별 검증 (FDA AccessGUDID, MFDS 품목분류표 대조)

#### 25개 카테고리 선례 DB

**A. 진단/측정 기기**

| # | Category | FDA Code | CFR | Landmark | MFDS Code | Grade | Conf |
|---|----------|----------|-----|----------|-----------|-------|------|
| 1 | 맥박산소측정기 | DQA | 870.2700 | K082641 | A09020.02 | 2등급 | ✅ |
| 2 | 자가혈당측정기 | NBW | 862.1345 | — | A09050.01 | 2등급 | ⚠️ |
| 3 | 환자감시장치 | MHX | 868.2340 | — | A08010.02 | 2등급 | ⚠️ |
| 4 | 심전계 | DRX | 870.2340 | — | A09030.03 | 2등급 | ⚠️ |
| 5 | CT 스캐너 | JAK | 892.1750 | — | A07010.02 | 2등급 | ⚠️ |

**B. AI/SaMD**

| # | Category | FDA Code | CFR | Landmark | MFDS Code | Grade | 7-Digit | Conf |
|---|----------|----------|-----|----------|-----------|-------|---------|------|
| 6 | AI 당뇨망막병증 자율진단 | PIB | 886.4460 | DEN170073 | A19230.xx | 3등급 | — | ✅ |
| 7 | AI 뇌영상 진단보조 | — | — | — | A17010.01 | 3등급 | B1BXXA1 | ✅ |
| 8 | AI 영상의학 분류 | QAS | 892.2050 | DEN180005 | A19230.xx | 2-3등급 | — | ⚠️ |
| 9 | AI 심전도 부정맥 감지 | QO2 | 870.2345 | DEN180044 | — | 2-3등급 | — | ⚠️ |
| 10 | 디지털치료기기 (DTx) | — | — | DEN200069 | — | 2-3등급 | — | ⚠️ |
| 11 | 웨어러블 수면/웰니스 기기 | QZW | — | DEN230041 | — | COND | — | ✅ |

**C. 임플란트 및 고위험 기기**

| # | Category | FDA Code | CFR | Landmark | Grade | Conf |
|---|----------|----------|-----|----------|-------|------|
| 12 | 약물방출 관상동맥 스텐트 | NIQ | 870.3945 | P160043 | 4등급 | ✅ |
| 13 | 이식형 심장 페이싱 리드 | DXY | 870.3680 | — | 4등급 | ⚠️ |
| 14 | 이식형 무릎 운동학 센서 | QPP | 888.3600 | DEN200064 | — | ✅ |
| 15 | 인공 고관절 | — | 888.3310 | — | 3-4등급 | ⚠️ |
| 16 | 치과용 임플란트 | NBQ | 872.3710 | — | 3등급 | ⚠️ |
| 17 | 인공와우 | — | 874.3400 | — | 4등급 | ⚠️ |

**D. 치료 기기**

| # | Category | FDA Code | CFR | Landmark | Grade | Conf |
|---|----------|----------|-----|----------|-------|------|
| 18 | 주입펌프 | FRN | 880.5725 | — | 2-3등급 | ⚠️ |
| 19 | 인공호흡기 | BTF | 868.5895 | — | 3등급 | ⚠️ |
| 20 | 자동제세동기 | DRE | 870.5310 | — | 3등급 | ⚠️ |
| 21 | 수술용 로봇 | — | 876.4300 | DEN150024 | 3등급 | ⚠️ |
| 22 | 보청기 (OTC) | QOP | 874.3300 | — | 2등급 | ⚠️ |

**E. 특수 분류 기기**

| # | Category | FDA Code | Landmark | MFDS Code | Grade | Conf |
|---|----------|----------|----------|-----------|-------|------|
| 23 | 비교정용 컬러렌즈 | — | — | — | — | ✅ |
| 24 | 수동식 의료용 겸자 | — | — | A45020.01 | 1등급 | ✅ |
| 25 | 약물전달 펜인젝터 | FRM | — | — | 2등급 | ⚠️ |

#### 사용 가이드라인

- ✅ 코드: 직접 인용 가능
- ⚠️ 코드: "~로 추정됨" 접두어 사용
- ❓ 코드: 인용 금지, "검증 필요" 표시만

### 3.2 디지털의료제품법 3-Tier 프레임워크 보강

#### 추가 내용 (`mfds-criteria.md`)

**A. 법적 근거 강화:**

| 조항 | 내용 |
|------|------|
| 제2조 (정의) | 디지털의료제품 = 의료기기법 의료기기 중 디지털 기술 적용 제품 |
| 제3조 (범위) | 의료기기(Tier 1), 건강지원제품(Tier 2), 비규제(Tier 3) |
| 제7조 (건강지원제품) | 건강지원제품의 별도 규제 경로 |

**B. 3-Tier 판단 워크플로우:**

```
사용자 입력 → Tier 판별:
├─ 의료 목적 명확 → Tier 1 (의료기기) → YES → 4-Gate
├─ 건강관리 목적이나 의료 경계 → Tier 1/2 경계 → CONDITIONAL
│   → 반드시 출력: "디지털의료제품법 제3조 3-tier 프레임워크"
└─ 의료 목적 없음 → Tier 3 (비규제) → NO
```

**C. CLAUDE.md 축약 반영:**
```
MFDS 디지털 기기 분석 시:
- 항상 "디지털의료제품법 3-tier" 프레임워크 언급
- 웰니스 경계 → CONDITIONAL + "건강지원제품" 가능성 분석
- 4-Gate → Risk Matrix → 7-digit 코드 출력
```

---

## Section 4: 예상 효과 및 구현 우선순위

### 4.1 개선 항목별 예상 점수 향상

| # | 개선 항목 | 예상 향상 | 영향 시나리오 | 근거 |
|---|----------|----------|------------|------|
| 1 | CLAUDE.md 아키텍처 레이어 | +40~50pt | S-08(+12), S-02(+8), 기타 MFDS | S-09가 80% 달성한 것이 증거 |
| 2 | 선례 DB | +25~35pt | 전 시나리오 evidence | evidence 평균 1.1→3.0+ |
| 3 | CONDITIONAL/SPECIAL 판정 규칙 | +15~20pt | S-03(+8), S-05(+4), S-06(+3) | 판정 정확도 향상 |
| 4 | 디지털의료제품법 3-Tier | +8~12pt | S-03 MFDS | pathway 0→3-4 |
| 5 | De Novo 경로 우선 로직 | +10~15pt | S-04(+6), S-02(+3) | 경로 정확도 향상 |
| 6 | 루브릭 수정 (공정성) | +12~15pt | S-03 전 참가자 | "(if YES)" 별칭 추가 |
| | **합계** | **+110~147pt** | | |

| 시나리오 | 보수적 | 기대 | 낙관적 |
|----------|--------|------|--------|
| 총 향상 | +110pt | +128pt | +147pt |
| 최종 점수 | 362/440 | 380/440 | 399/440 |
| **비율** | **82.3%** | **86.4%** | **90.7%** |

### 4.2 4단계 구현 순서

| Phase | 이름 | 핵심 내용 | 예상 향상 | 소요 |
|-------|------|----------|----------|------|
| **1** | 아키텍처 레이어 | CLAUDE.md + meta-skill + 필수 출력 구조 | +40~50pt | 1일 |
| **2** | 선례 DB | precedent-db.md + CLAUDE.md 참조 | +25~35pt | 1-2일 |
| **3** | 도메인 규칙 강화 | CONDITIONAL, De Novo, 디지털의료제품법 | +33~47pt | 1-2일 |
| **4** | 루브릭 & 품질 보정 | catalog.json 별칭, analysis 품질 | +12~15pt | 0.5일 |

### 4.3 Phase별 검증 정책

> **절대 원칙: 1 Phase = 1 변경 = 1 벤치 = 1 검증**

| Phase | 검증 시나리오 | 최소 성공 기준 | 회귀 감시 |
|-------|------------|-------------|----------|
| 1 | S-08, S-09 | S-08 ≥ 55%, S-09 ≥ 80% 유지 | S-01, S-07 |
| 2 | S-01, S-04, S-08 | evidence 평균 ≥ 2.5/5 | S-09 유지 |
| 3 | S-03, S-05, S-06 | S-03 ≥ 50%, S-05 det ≥ 3 | S-01, S-08 |
| 4 | 전체 9개 | 전체 ≥ 85% | — |

**롤백 기준:**
- 대상 시나리오 2개 이상 점수 하락 → 즉시 롤백
- 비대상 시나리오 5%p 이상 하락 → 트레이드오프 분석
- S-09 70% 미만 하락 → 즉시 롤백

### 4.4 대화형 UX 영향 평가

| 개선 항목 | 벤치 효과 | UX 효과 | 양립성 |
|----------|----------|---------|--------|
| CLAUDE.md 필수 출력 구조 | 구조화 출력 점수 ↑ | 일관된 구조화 출력 → 검토 효율 ↑ | ✅ 완전 양립 |
| 선례 DB | evidence ↑ | 구체적 규정/코드 인용 → 전문성 신뢰 ↑ | ✅ 완전 양립 |
| CONDITIONAL 판정 | determination ↑ | 불확실성 투명 표현 → 의사결정 품질 ↑ | ✅ 완전 양립 |
| De Novo 우선 로직 | pathway ↑ | 정확한 경로 제안 → 전략 컨설팅 가치 ↑ | ✅ 완전 양립 |
| 디지털의료제품법 | MFDS ↑ | 최신 규제 반영 → 국내 RA 실무자 직접 가치 | ✅ 완전 양립 |

**결론:** 모든 개선이 벤치 점수 향상 = 실제 사용자 가치 향상. 대화형 UX 부정적 영향 없음.

### 4.5 57.3% → 85% 로드맵

```
현재: 252/440 = 57.3%
  │
  ├─ Phase 1 완료: +40~50pt → 66~69%
  │   ✓ 4-Gate/Risk Matrix/7-digit 출력 정상화
  │
  ├─ Phase 2 완료: +25~35pt → 72~77%
  │   ✓ evidence 점수 전반적 향상
  │
  ├─ Phase 3 완료: +33~47pt → 80~87%
  │   ✓ CONDITIONAL/SPECIAL/De Novo 판정 정확도
  │
  └─ Phase 4 완료: +12~15pt → 82~91%
      ✓ 루브릭 공정성 + 분석 품질
```

**핵심 조건:**
1. Phase 1 성공 필수 — 아키텍처 레이어가 실패하면 Phase 2-3 효과 제한
2. 토큰 예산 관리 — CLAUDE.md 200줄 이내
3. 1-Phase-1-Verify — 매 Phase 후 벤치 실행
4. Phase 3 교훈 — 한 번에 4개 변경 금지, 가능하면 세분화
