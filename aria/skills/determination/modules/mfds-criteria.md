# MFDS Device Criteria

## Overview

Two-step determination process for Korean (MFDS) regulatory assessment:
1. **Step 1**: Medical Device / IVD Device Status
2. **Step 2**: Digital Medical Product Act Applicability (디지털의료제품법)

---

## STEP 1: Medical Device / IVD Device Determination

### Definition

Medical devices are instruments, machines, apparatus, materials, software or similar products used for human beings for the following purposes.

### Scope

- Diagnosis, treatment, alleviation, management or prevention of disease
- Diagnosis, treatment, alleviation or correction of injury or disability
- Examination, replacement or modification of structure or function
- Pregnancy control

### In Vitro Diagnostic (IVD) Medical Device

- Reagents, calibrators, control materials, kits, instruments, apparatus, equipment, software, or systems
- Used alone or in combination to examine specimens derived from the human body
- Purpose: diagnosis, prevention, monitoring, or treatment of disease or physiological conditions

### Korea-Specific Rules

- Clear distinction from pharmaceuticals required
- Chemical action must NOT be the primary effect
- Korean-language labeling and IFU mandatory
- MFDS pre-market approval (허가) or notification (신고) required

### Step 1 Decision Workflow

1. Check intended use against Korean regulatory scope
2. Identify if IVD (in vitro) or general medical device
3. Evaluate distinction from pharmaceuticals
4. Assess mechanism of action (chemical vs non-chemical)
5. Review local classification nuances
6. **Evaluate 디지털의료제품법 3-tier boundary** (see below)
7. Determine device status: YES (Medical Device / IVD) / NO / CONDITIONAL

#### 디지털의료제품법 3-Tier Boundary Assessment

**Legal basis**: 디지털의료제품법 (시행 2025.01.24), 디지털의료·건강지원제품 카테고리 (시행 2026.01.24)

```
Product classification under 디지털의료제품법:

Tier 1: 의료기기 (Medical Device)
  - Clear medical purpose (진단, 치료, 예방, 모니터링)
  - Meets 「의료기기법」 definition
  → Determination: YES → Proceed to Step 2 (4-Gate)

Tier 2: 건강지원제품 (Health Support Product)
  - Health management purpose but NOT medical device
  - Manages/tracks health data without medical claims
  - Does NOT diagnose, treat, or prevent disease
  - May include: fitness tracking, sleep quality scoring, nutrition management
  → Determination: CONDITIONAL
     Uncertainty basis: "Product may qualify as 건강지원제품 under 디지털의료제품법 — separate regulatory pathway from medical device"
     Resolution: Detailed intended use review by MFDS required
     If YES (의료기기): Apply 4-Gate → classification → pathway
     If 건강지원제품: Separate 디지털의료제품법 pathway (not 「의료기기법」)

Tier 3: 비규제 (Non-regulated)
  - General wellness, lifestyle, entertainment
  - No health management claims
  → Determination: NO
```

**Boundary indicators for Tier 1 vs Tier 2 (의료기기 vs 건강지원제품)**:
- SpO2/심박/호흡 모니터링 + 이상 감지 알림 → CONDITIONAL (Tier 1/2 경계)
- 수면 패턴 분석 + 수면 위생 조언만 → Tier 2 (건강지원) or Tier 3 (비규제)
- 호흡 이상 패턴 + "의사 상담 권유" → CONDITIONAL (likely Tier 1)
- 생체신호 측정 + 질병 스크리닝/진단 → Tier 1 (의료기기)

**CRITICAL**: When product straddles Tier 1/Tier 2 boundary, determination MUST be CONDITIONAL. Do NOT default to YES (의료기기). The 건강지원제품 category is a legally distinct pathway.

**If Step 1 = NO**: Product is NOT a medical device → STOP (not subject to MFDS regulation)

**If Step 1 = YES**: Proceed to Step 2 for digital medical product assessment

**If Step 1 = CONDITIONAL**: Output CONDITIONAL with 3-tier analysis. Provide both "If 의료기기" and "If 건강지원제품" scenarios with respective classification/pathway.

---

## STEP 2: Digital Medical Product Act Assessment (디지털의료제품법)

**Legal Basis**: Digital Medical Product Act (디지털의료제품법) Article 2, Article 3, and Guidelines (2025.11)

### Required Input Variables (6 Core Parameters)

> **Loaded Knowledge**: `../../knowledge/catalog.yaml` → id: mfds-notice-cls2025-product-code (제품코드 생성 기준 — 입력 변수 정의 포함)

### 4-Gate Decision Logic

> **Loaded Knowledge**: `../../knowledge/catalog.yaml` → id: mfds-law-dmp-act-art2 (디지털의료제품법 정의) + 본 모듈 내장 4-Gate 로직
> 요약: Gate 1(의료기기)→ Gate 2(디지털 기술)→ Gate 3(핵심 기능)→ Gate 4(배제)

### 7-Digit Product Code Generation

> **Loaded Knowledge**: `../../knowledge/catalog.yaml` → id: mfds-notice-cls2025-product-code (고시 별표3 제품코드 생성 기준)
> 요약: [사용목적 2][기술유형 3][기기유형 1][형태 1] 형식

### Risk-Based Classification

> **Loaded Knowledge**: `../../knowledge/catalog.yaml` → id: mfds-notice-cls2025-risk-matrix (고시 별표4 등급 지정 세부 기준)
> 요약: Medical Impact × Patient Condition → 1~4등급, Malfunction Adjustment 적용

### Step 2 Output Format

```
[디지털의료기기 규제 분석 결과]

1. 디지털의료기기 해당 여부: [해당/비해당]
   - 판단 근거: Gate [1/2/3/4] 결과

2. 제품 코드: [예: B1BXXA2]

3. 위해도 등급 분석:
   - Medical Impact: [Treatment/Diagnosis / Clinical Management / Information/Monitoring]
   - Patient Condition: [Critical / Serious / Non-Serious]
   - Base Grade: 제 [ ] 등급
   - Malfunction Risk: [사망(+1) / 부상(0) / 피해없음(-1)]
   - 최종 등급: 제 [1/2/3/4] 등급

4. 법적 근거: 「디지털의료제품법」 제3조 및 가이드라인(2025.11) 별표 3, 4
```

---

## Summary: Two-Step Decision Tree

```
Product Input
    ↓
[STEP 1] Medical Device / IVD?
    ↓ NO → NOT subject to MFDS
    ↓ YES
[STEP 2] Digital Medical Product Act
    ↓
Gate 1: Medical Device Status? → NO → EXIT
    ↓ YES
Gate 2: Digital Technology Applied? → NO → EXIT
    ↓ YES
Gate 3: Core Function Impact? → NO → EXIT
    ↓ YES
Gate 4: Exclusion Principle? → YES (simple only) → EXIT
    ↓ NO (core medical function)
Digital Medical Device CONFIRMED
    ↓
Generate 7-Digit Code + Risk Grade (1-4)
```
