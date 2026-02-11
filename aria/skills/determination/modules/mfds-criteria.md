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
6. Determine device status: YES (Medical Device / IVD) / NO / CONDITIONAL

**If Step 1 = NO**: Product is NOT a medical device → STOP (not subject to MFDS regulation)

**If Step 1 = YES**: Proceed to Step 2 for digital medical product assessment

---

## STEP 2: Digital Medical Product Act Assessment (디지털의료제품법)

**Legal Basis**: Digital Medical Product Act (디지털의료제품법) Article 2, Article 3, and Guidelines (2025.11)

### Required Input Variables (6 Core Parameters)

| Variable | Data Type | Purpose |
|----------|-----------|---------|
| Representative Model Name | String | Baseline for multi-model products |
| Primary Intended Use | Enum | A(검사)~I(융합제품) - determines 1st-2nd code + risk matrix row |
| Input Data & Processing Principle | String | Defines 2nd digit of product code |
| Applied Technology Type | Enum | A(독립형SW), B(AI), C(지능형로봇), D(HPC), E(가상융합기술) - determines 3rd-5th code |
| Base Device Type | Enum | A(의료기기), B(체외진단의료기기), C(융합) - determines 6th code |
| Hardware Integration Form | Enum | 1(독립형SW), 2(내장형), 3(혼합) - determines 7th code |

### 4-Gate Decision Logic

#### Gate 1: Medical Device Status
- **Question**: Does the product meet the definition of medical device under 「의료기기법」 or 「체외진단의료기기법」?
- **NO** → NOT a digital medical device (EXIT)

#### Gate 2: Technology Applicability
- **Question**: Does the product apply one or more of the following technologies?
  - Standalone SW (독립형 SW)
  - AI (인공지능)
  - Intelligent Robot (지능형 로봇)
  - High-Performance Computing (초고성능 컴퓨팅)
  - Virtual/Fusion Technology (가상융합기술: VR/AR/XR/Metaverse)
- **NO** → NOT a digital medical device (EXIT)

#### Gate 3: Core Function Impact
- **Question**: Does the technology affect the intended use through ONE OR MORE of the following?
  - Control and operation of medical device hardware
  - Data analysis and processing (embedded or standalone SW)
  - Accessory (SW) functionality
- **NO** → NOT a digital medical device (EXIT)

#### Gate 4: Exclusion Principle
- **Question**: Is the technology limited to ONLY the following?
  - Simple electronic interface (data transmission only)
  - Simple component (unrelated to intended use)
  - Simple infrastructure (generic server, communication device)

  **Exception**: SW performing analysis/processing on cloud infrastructure IS considered embedded/standalone → qualifies as digital medical device

- **YES (limited to simple functions)** → NOT a digital medical device (EXIT)
- **NO (performs core medical functions)** → Digital medical device (PROCEED to coding)

### 7-Digit Product Code Generation

**Format**: `[Primary Use 2 digits][Technology 3 digits][Base Type 1 digit][Form 1 digit]`

**Example**: `B1ABXA1` (no hyphens)

#### Digits 1-2: Primary Intended Use

| 1st Digit | 2nd Digit Sub-Classification |
|-----------|------------------------------|
| A (검사) | 1:의료영상, 2:생체신호, 3:체외진단지표, 4:기타, 5:2개 이상 |
| B (진단) | 1:의료영상, 2:생체신호, 3:체외진단지표, 4:기타, 5:2개 이상 |
| C (치료) | 1:수술/시술지원, 2:치료계획/모의시술, 3:디지털치료기기, 4:기타 |
| D (임상관리) | 1:의료영상, 2:생체신호, 3:체외진단지표, 4:기타, 5:2개 이상 |
| E (장애보조) | 1:운동장치, 2:기능보조, 3:기타 |
| F (정보제공) | 1:의료영상, 2:기타 |
| G (의약품보조) | 1:복약모니터링, 2:약물주입량 계산, 3:동반진단, 4:병용요법 활용 |
| H (기타) | 1:마약류 중독 재활, 2:기타 |
| I (융합제품) | N:주된 사용 목적의 개수 (예: I2 = 2개 목적) |

#### Digits 3-5: Technology Type (Priority Order)

**Priority**: A(독립형SW) > B(AI) > C(지능형로봇) > D(HPC) > E(가상융합기술)

- **1 technology**: `[A/B/C/D/E]XX` (4th-5th = XX)
- **2 technologies**: `[A/B][B/C/D/E]X` (5th = X)
- **3 technologies**: `[A/B/C][B/C/D][C/D/E]` (all 3 positions filled)
- **4+ technologies**: 5th position = `P` (예: ABCP)

#### Digits 6-7: Base Type + Form

- **6th Digit**:
  - A: Medical Device (의료기기)
  - B: IVD Medical Device (체외진단의료기기)
  - C: Fusion (A+B)

- **7th Digit**:
  - 1: Standalone SW (독립형)
  - 2: Embedded (내장형)
  - 3: Hybrid (1+2)

**Example**: `B1BXXA2` = Diagnosis using medical imaging + AI technology + Medical Device + Embedded SW

### Risk-Based Classification (등급 지정)

**Classification Process**: Medical Impact (1차) → Patient Condition (2차) → Malfunction Risk Adjustment (최종)

---

#### Step 1: Medical Impact Classification (제품 기능 기반)

**Primary Intended Use 코드와 매핑**:

| 제품 코드 | 사용 목적 | Medical Impact |
|----------|----------|----------------|
| A(검사) | 검사·측정 | **Treatment/Diagnosis** |
| B(진단) | 진단 보조 | **Treatment/Diagnosis** |
| C(치료) | 치료·재활 | **Treatment/Diagnosis** |
| D(임상관리) | 예측·예방·관리 유도 | **Clinical Management** |
| E(장애보조) | 재활·보조 | **Treatment/Diagnosis** or **Clinical Management** (사례별 판단) |
| F(정보제공) | 정보 제공·모니터링 | **Information/Monitoring** |
| G(의약품보조) | 복약·투약 지원 | **Treatment/Diagnosis** |
| H(기타) | - | 개별 평가 |
| I(융합제품) | 복수 목적 | 최고 위험도 목적 기준 |

---

#### Step 2: Patient Condition Identification (적응증 기반)

**제품 IFU/적응증에서 확인**:

| Patient Condition | 판단 기준 | 키워드 |
|-------------------|----------|--------|
| **Critical** (위독·치명적) | 24시간 내 사망 위험이 있는 환자 | 중환자, 응급, 생명 위협, ICU, 인공호흡기, 혈액투석, 심정지 |
| **Serious** (중증 질환) | 중증 질환으로 적절한 치료 없으면 악화 가능 | 중증, 만성 중증, 악화 시 입원, 암, 심부전, 뇌졸중 |
| **Non-Serious** (기타 질환) | 경증 또는 일반 질환 | 경증, 일반, 외래 관리, 건강관리 |

---

#### Step 3: Risk Matrix Application (Guideline Annex 4)

| Medical Impact | Critical<br>(위독·치명적) | Serious<br>(중증 질환) | Non-Serious<br>(기타 질환) |
|----------------|----------------------|---------------------|----------------------|
| **Treatment/Diagnosis/Drug Support**<br>(치료·진단·검사·의약품 보조) | **4등급** | **3등급** | **2등급** |
| **Clinical Management**<br>(임상적 관리 유도 - 예측·예방) | **3등급** | **2등급** | **1등급** |
| **Information/Monitoring**<br>(정보 제공·모니터링 및 기타) | **2등급** | **1등급** | **1등급** |

---

#### Step 4: Malfunction Risk Adjustment (성능저하·오작동 시 피해 기준)

**Base Grade에서 최종 등급 조정**:

| 오작동 시 피해 | 등급 조정 | 비고 |
|--------------|----------|------|
| **사망 가능성** | **+1 등급** | 4등급 초과 불가 (최대 4등급) |
| **부상/악화** | **조정 없음** | Base Grade 유지 |
| **피해 없음** | **-1 등급** | **단, 2등급 → 1등급 하향 조정 금지** |

**조정 제한 규칙**:
- 상향: 최대 4등급까지만 가능 (예: 3등급 + 사망 = 4등급)
- 하향: 2등급에서 1등급으로 하향 조정 절대 불가 (Ground Truth)

---

#### Final Grade Selection Rules

**복합 기능 제품**:
- **Embedded SW**: `Max(HW grade, SW function grade)`
- **Multi-function SW**: `Max(grade of each function)`

**최종 등급**: Base Grade + Malfunction Adjustment (조정 제한 규칙 적용)

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
