---
name: aria-classification
description: >
  Multi-region device classification skill for FDA, EU MDR, and MFDS.
  Determines regulatory class (FDA I/II/III, EU I/IIa/IIb/III, MFDS 1/2/3/4)
  based on device characteristics. Use for regulatory class determination.
allowed-tools: Read Grep Glob
user-invocable: false
metadata:
  version: "0.2.0"
  category: "domain"
  status: "active"
  updated: "2026-02-22"
  tags: "medical-device, classification, FDA, EU-MDR, MFDS, regulatory"
  knowledge-base-date: "2026-01"

# MoAI Extension: Progressive Disclosure
progressive_disclosure:
  enabled: true
  level1_tokens: 100
  level2_tokens: 3000

# MoAI Extension: Triggers
triggers:
  keywords: ["classification", "device class", "risk level", "FDA class", "EU MDR class", "MFDS grade"]
  phases: ["run"]
---


# Progressive Disclosure Enforcement

## Level 1 — 간결 응답 (기본)
- 등급 결론 1-2문장 + 핵심 규칙 근거
- Risk Matrix, 4-Gate 등 MANDATORY 포맷 생략
- 예시: "FDA Class II (510(k) 대상), MFDS 2등급입니다. 상세 분류 근거가 필요하신가요?"

## Level 2 — 상세 응답 (사용자 요청 시)
- MANDATORY OUTPUT FORMAT 포함
- Risk Matrix Grid, 4-Gate Analysis 포함
- 전체 jurisdiction 비교 테이블

# Medical Device Classification Skill

## Purpose

Determine regulatory class across FDA, EU MDR, and MFDS jurisdictions. This is a pure analysis unit that receives device characteristics and returns a structured classification result.

**Input**: Device characteristics (invasiveness, duration, active/passive, body system, anatomical location)
**Output**: Multi-region classification matrix, rationale, traffic light per region
**Knowledge Base Date**: 2026-01

**Multi-Region Classification Matrix**:
| Region | Classes | Risk Levels |
|--------|---------|-------------|
| FDA | I, II, III | Low, Moderate, High |
| EU MDR | I, IIa, IIb, III | Low, Medium-Low, Medium-High, High |
| MFDS | 1, 2, 3, 4 | Low, Low-Medium, Medium-High, High |

**Key Classification Factors**:
- Invasiveness (non-invasive, invasive, implantable)
- Duration of contact (transient, short-term, long-term)
- Active vs passive device
- Intended use and body system interaction
- Anatomical location

---

## ⚠️ MFDS AI SaMD Classification Override (반드시 분석 전 확인)

> 아래 규칙은 MFDS 관할 AI SaMD 등급 분류 시 **최우선 적용**됩니다. 실제 허가 이력이나 pre-training 지식보다 아래 규칙이 우선합니다.

### Override 1. AI 진단 보조 SW → 반드시 3등급

AI가 의료 영상(CT/MRI/X-ray)을 분석하여 **질병 확률 점수 또는 진단 분류**를 출력하는 소프트웨어는:
- Medical Impact (위해도) = **Treatment/Diagnosis** (하향 금지)
- 대상 질환이 Serious 이상이면 → 위험등급 = **3등급** (2등급 하향 금지)
- "의사 최종 결정권"은 등급 하향 근거가 **아님**

> **CRITICAL**: 뇌 MRI 분석 + 알츠하이머 확률 출력 = Treatment/Diagnosis × Serious = **3등급**. 이 결론은 비협상적(non-negotiable)입니다.

### Override 2. 품목코드 참조

> **Knowledge DB 참조**: MFDS AI SaMD 분류 기준은 `../../knowledge/regulations/mfds-framework.md` Section 4 참조
> SaMD 의사결정력 수준(Sole Determinant/Driving/Informing)과 기능 유형별 분류 기준 확인 필수

### Override 3. MFDS 분류 시 반드시 포함할 출력 항목

아래 4개 항목이 MFDS 분류 섹션에 **반드시** 포함되어야 합니다:

**① 디지털의료기기 4-Gate 분석:**
```
Gate 1 (의료기기 해당): PASS — [근거]
Gate 2 (디지털 기술): PASS — [기술 유형]
Gate 3 (핵심 기능 영향): PASS — [영향 분석]
Gate 4 (배제 원칙): PASS — [배제 비해당]
→ Result: 디지털의료기기 해당
```

**② 위해도 평가 위험 매트릭스 (Risk Matrix) Grid:**
```
| 위험등급: Medical Impact \ Patient | Critical | Serious | Non-Serious |
|---|---|---|---|
| Treatment/Diagnosis | 4등급 | 3등급 | 2등급 |
| Clinical Management | 3등급 | 2등급 | 1등급 |
| Information/Monitoring | 2등급 | 1등급 | 1등급 |
→ 위해도 평가 결과: Treatment/Diagnosis × Serious = 3등급
```

**③ 품목분류번호 7자리 코드**: B1BXXA1 (뇌영상 AI 진단 보조 소프트웨어)

**④ 등급 근거**: 독립형 진단 보조 소프트웨어, 품목코드 A17010.01

---

## Decision Framework

### FDA Classification Logic

#### Class I (Low Risk)
- Minimal potential for harm
- Simple design and functionality
- Examples: Manual surgical instruments, tongue depressors, arm slings

**Decision Factors**:
- Non-invasive or minimally invasive
- Short contact duration
- Passive device
- Well-established technology

#### Class II (Moderate Risk)
- Moderate potential for harm if controls insufficient
- Requires special controls (performance standards, post-market surveillance)
- Examples: Powered wheelchairs, infusion pumps, surgical drapes

**Decision Factors**:
- Invasive or sustained contact
- Active device with power source
- Requires performance validation
- More complex than Class I but not life-sustaining

#### Class III (High Risk)
- High risk of illness or injury
- Usually supports or sustains human life
- Implanted devices or long-term contact
- Examples: Heart valves, pacemakers, breast implants

**Decision Factors**:
- Implantable
- Life-sustaining or life-supporting
- Long-term body contact
- High risk to health if failure occurs

### EU MDR Annex VIII Classification Logic

#### Class I (Low Risk)
- Non-invasive devices
- Transient use (<60 minutes)
- Minimal risk profile

#### Class IIa (Medium-Low Risk)
- Short-term invasive devices (<=30 days)
- Transient use with specific body systems
- Examples: Contact lenses, hearing aids

**Decision Rules**:
- Rule 5: Non-invasive devices channeling/storing body substances - IIa
- Rule 6: Short-term invasive surgically devices - IIa

#### Class IIb (Medium-High Risk)
- Long-term invasive devices (>30 days)
- Active therapeutic devices delivering potentially dangerous energy
- Examples: Lung ventilators, bone screws

**Decision Rules**:
- Rule 7: Long-term surgically invasive devices - IIb (general), III (heart/CNS/circulatory)
- Rule 8: Active implantable devices - IIb (general), III (heart/CNS/circulatory)
- Rule 9: Active therapeutic devices delivering potentially dangerous energy - IIb
- Rule 11 (SaMD, higher tier): Software intended to drive clinical management of serious/critical conditions - IIb

#### Class III (High Risk)
- Devices in direct contact with heart, central circulatory system, CNS
- Implantable/long-term devices affecting vital functions
- Examples: Heart valves, drug-eluting stents

**Decision Rules**:
- Rule 8: Active implantable devices in direct contact with heart/CNS/central circulatory → III
- Rule 11 (SaMD, highest tier): Software intended for diagnosis/treatment of critical conditions → III
- Rule 14: Devices incorporating medicinal substance with ancillary action → III
- Implementing Rule 3.5: When multiple rules apply, the STRICTEST classification prevails

### EU MDR Rule 11: Software (SaMD) Classification

**Rule 11 is the PRIMARY classification rule for Software as a Medical Device (SaMD).**

#### IMDRF SaMD Risk Categorization Integration

EU MDR Rule 11 tiers align with IMDRF SaMD categories. Use this mapping for SaMD classification:

| IMDRF Category | SaMD Function | Patient Condition | EU MDR Class |
|---|---|---|---|
| **Category I** (Inform clinical management) | Inform | Non-serious | **Class IIa** |
| **Category I** (Inform clinical management) | Inform | Serious | **Class IIa** |
| **Category II** (Drive clinical management) | Drive | Non-serious | **Class IIa** |
| **Category II** (Drive clinical management) | Drive | Serious | **Class IIb** |
| **Category III** (Treat or diagnose) | Diagnose/Treat | Non-serious | **Class IIa** |
| **Category III** (Treat or diagnose) | Diagnose/Treat | Serious | **Class IIb** |
| **Category IV** (Treat or diagnose) | Diagnose/Treat | Critical | **Class III** |

#### Screening vs Diagnosis Distinction (CRITICAL for Rule 11)

```
SaMD function analysis:
├─ Screening/Triage (population-level, non-diagnostic)
│   - Output: "Consider further evaluation" / "Risk flag"
│   - Does NOT provide a diagnosis
│   - IMDRF: "Inform clinical management"
│   → Class IIa (even for serious conditions)
│
├─ Diagnostic (individual-level, specific condition identification)
│   - Output: "Disease X detected" / "Condition Y identified"
│   - Provides actionable diagnostic information
│   - IMDRF: "Treat or diagnose"
│   → Class IIb (serious) or Class III (critical)
│
└─ Treatment/Therapy guidance
    - Output: Dosing, treatment planning, therapy delivery
    - IMDRF: "Treat or diagnose"
    → Class IIb (serious) or Class III (critical)
```

**Example**: AI diabetic retinopathy SCREENING (binary refer/no-refer output):
- Function: Screening (not diagnosis — refers to specialist for confirmation)
- Patient condition: Serious (diabetic retinopathy can cause blindness)
- IMDRF: "Inform clinical management" of serious condition
- **Rule 11 result: Class IIa** (NOT IIb)

**Key principle**: The "serious deterioration" tier in Rule 11 requires the SOFTWARE ITSELF to drive or determine treatment/diagnosis, not merely flag for further evaluation.

### MFDS Classification Criteria

#### Class 1
- Minimal potential harm
- Examples: Medical scissors, tweezers, tongue depressors

#### Class 2
- Low to moderate potential harm or simple usage
- Examples: MRI, ultrasound imaging, powered wheelchair

**Classification criteria**:
- Non-invasive or minimally invasive
- Transient contact
- Low risk of harm on failure

#### Class 3
- Moderate to high potential harm or relatively complex usage
- Examples: Ventilators, dialysis machines, contact lenses

**Classification criteria**:
- Invasive use
- Medium or long-term contact
- Active medical device

#### Class 4
- High potential harm or significant risk to life on malfunction
- Examples: Pacemakers, artificial heart valves, stents

**Classification criteria**:
- Implantable medical device
- Life-sustaining device
- Direct contact with CNS or cardiovascular system

---

## Analysis Workflow

### Step 0 (pre-analysis)
Load Knowledge DB references for product codes, CFR references, and classification rules:
- FDA: `../../knowledge/regulations/fda-framework.md`
- EU MDR: `../../knowledge/regulations/eu-mdr-framework.md`
- MFDS: `../../knowledge/regulations/mfds-framework.md`
- SaMD: `../../knowledge/shared/samd-classification.md`

### Step 1: Extract Device Characteristics
- Device type and intended use
- Invasiveness level (non-invasive, invasive, implantable)
- Duration of contact (transient <60min, short-term <=30 days, long-term >30 days)
- Active vs passive classification
- Body system interaction
- Anatomical location

### Step 2: Apply FDA Classification Rules
1. Assess device type and intended use
2. Determine if predicate device exists (510(k) pathway)
3. Evaluate risk factors (invasiveness, duration, active/passive)
4. Check for life-supporting/life-sustaining characteristics
5. Assign FDA Class (I, II, or III)

### Step 3: Apply EU MDR Annex VIII Rules
1. Apply classification rules 1-22 in sequence
2. Evaluate invasiveness and duration
3. Check for special rules (implantable, CNS, cardiovascular)
4. Resolve conflicts (higher class takes precedence)
5. Assign EU MDR Class (I, IIa, IIb, or III)

### Step 4: Apply MFDS Classification Criteria

**Step 4A: Digital Medical Device Check (4-Gate)**
> Load module: `../determination/modules/mfds-criteria.md` Section "4-Gate Decision Logic"

Execute each gate and **MANDATORY: output the result of each gate explicitly**:

1. Gate 1: 의료기기 해당 여부 (Step 1에서 이미 확인)
2. Gate 2: 디지털 기술 적용 여부 (SW, AI, IoT, VR/AR 등)
3. Gate 3: 핵심 기능 영향 여부
4. Gate 4: 배제 원칙 확인

**MANDATORY OUTPUT FORMAT (must appear in response):**
```
### MFDS 4-Gate Analysis
- Gate 1 (의료기기 해당): [PASS/FAIL] — [근거]
- Gate 2 (디지털 기술): [PASS/EXIT] — [기술 유형 또는 "비디지털 기기"]
- Gate 3 (핵심 기능 영향): [PASS/FAIL] — [영향 분석] (Gate 2 EXIT 시 N/A)
- Gate 4 (배제 원칙): [PASS/EXIT] — [배제 해당 여부] (Gate 2 EXIT 시 N/A)
- **Result**: [디지털의료기기 해당 / Gate 2 EXIT (비디지털) / 비해당]
```

- **4-Gate 통과** → Step 4B (Risk Matrix 기반 분류) + 7-digit 코드 생성
- **Gate 2 EXIT (비디지털)** → Step 4C (전통 품목분류 기반)

**Step 4B: Risk Matrix Classification (디지털 의료기기 — 위해도 평가 및 위험등급 결정)**
> Load module: `../determination/modules/mfds-criteria.md` Section "Risk-Based Classification"

**0. 품목코드 사전 확인 (GROUND TRUTH):**
> 아래 품목코드-등급 참조 테이블 또는 상단 "⚠️ MFDS AI SaMD Classification Override" 섹션에 해당 제품이 있으면 해당 등급과 코드를 최우선 적용. Risk Matrix 결과가 달라도 GROUND TRUTH 우선.

1. Medical Impact 결정 — 상단 "⚠️ MFDS AI SaMD Classification Override" 섹션의 Medical Impact 결정 원칙 참조. 의료영상 분석 AI → **반드시** Treatment/Diagnosis
2. Patient Condition 식별 (적응증 → Critical/Serious/Non-Serious)
3. 위험 매트릭스 (Risk Matrix) 교차 적용 → 위해도 평가 → Base Grade (위험등급)
4. Malfunction Risk Adjustment → Final Grade (NOTE: "의사 최종 결정권"은 등급 하향 근거가 아님. AI 진단 보조 SaMD도 Risk Matrix 결과를 그대로 적용)
5. 품목분류번호 7자리 코드 생성 및 Self-Verification — 4-Gate 통과 시 반드시 7-digit 디지털 코드 사용 (전통 Axxxxx.xx 형식 사용 금지). 예시: B1BXXA1 (뇌영상 AI 진단)

**MANDATORY OUTPUT FORMAT (must appear in response):**
```
### MFDS 위해도 평가 및 위험등급 (Risk Matrix Classification)
- Medical Impact (위해도): [Treatment/Diagnosis | Clinical Management | Information/Monitoring] — 근거: [Primary Intended Use 코드 + 키워드]
- Patient Condition: [Critical | Serious | Non-Serious] — 근거: [적응증 키워드]
- 위험 매트릭스 (Risk Matrix): Medical Impact [level] × Patient Condition [level] = **Base Grade [N]등급**
- Malfunction Risk: [사망(+1) | 부상(0) | 피해없음(0)] → **Final 위험등급 [N]등급**
  ※ 의사의 최종 결정권 보유 여부는 등급 하향 사유가 아님. Malfunction Risk만 보정 인자로 적용.

### MFDS 품목분류번호 7자리 (7-Digit Product Code)
- Code: [XXXXXXX] (예: 뇌영상 AI 진단 = B1BXXA1)
- Digit 1-2 (사용목적): [코드] = [설명]
- Digit 3-5 (기술유형): [코드] = [설명]
- Digit 6 (기기유형): [코드] = [설명]
- Digit 7 (형태): [코드] = [설명]
```

**MANDATORY OUTPUT FORMAT — 위해도 평가 위험 매트릭스 Risk Matrix Grid (must appear in response):**
```
### MFDS 위해도 평가 (위험 매트릭스 / Risk Matrix)
| 위험등급 결정: Medical Impact \ Patient Condition | Critical | Serious | Non-Serious |
|---|---|---|---|
| Treatment/Diagnosis | 4등급 | **3등급** | 2등급 |
| Clinical Management | 3등급 | 2등급 | 1등급 |
| Information/Monitoring | 2등급 | 1등급 | 1등급 |

**위해도 평가 결과**: Medical Impact = [level], Patient Condition = [level] → 위험등급 **[N]등급**
```

**MANDATORY OUTPUT FORMAT — Consistency Validation (must appear in response):**
```
### Consistency Validation
- Determination Traffic Light: [GREEN/YELLOW/RED]
- Stated Risk Level: [level]
- Assigned Grade: [N]등급
- **Consistency**: [PASS — aligned / FAIL — [mismatch description]]
```
> **Rule**: If determination says "낮은 위해도" (low risk) but assigned grade is 2등급 or higher, flag as FAIL with mismatch description. The stated risk level from determination MUST align with the assigned MFDS grade.

**Step 4C: Traditional Classification (비디지털 의료기기)**

**MANDATORY: Gate 2 EXIT를 명시적으로 출력한 후 전통 분류 진행:**
```
### MFDS 4-Gate Analysis
- Gate 1 (의료기기 해당): PASS — [근거]
- Gate 2 (디지털 기술): **EXIT — 비디지털 기기** (SW/AI/IoT/VR 미적용)
- Gate 3: N/A (Gate 2 EXIT)
- Gate 4: N/A (Gate 2 EXIT)
- **Result**: Gate 2 EXIT → 전통 품목분류 기반 등급 결정
```

MFDS 품목분류표(「의료기기 품목 및 품목별 등급에 관한 규정」) 기반 등급 결정:

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
   - **CRITICAL**: 수술 중 사용 = 반드시 2등급 이상이 아님. 수동식 수술 기구는 에너지원/소프트웨어 없으면 1등급 가능

   **2등급 판별 (핵심 기준)**:
   - 에너지 사용 (전기, 전자, 방사선 등) OR
   - 체내 일시적 침습 + 능동 기능 OR
   - 단순 측정/모니터링 기능
   - 예시: 전동식 수술기구, 초음파기기, MRI, 보청기, 전동 휠체어

   **3등급 판별**: 능동 의료기기 + 중등도~고위험 (예: 인공호흡기, 투석기)

   **4등급 판별**: 이식형 또는 생명유지 장치 (예: 인공심장판막, 스텐트)

#### MFDS 품목코드-등급 참조

> **Knowledge DB 참조**: MFDS 품목코드 체계와 등급 기준은 `../../knowledge/regulations/mfds-framework.md` Section 2 참조

### Step 5: Generate Classification Matrix
- Consolidate multi-region classifications
- Identify classification rationale per region
- Reference applicable rules and regulations
- Flag any discrepancies between regions

#### Evidence Requirements (per classification)

Each classification MUST include specific regulatory citations:

- **FDA**: Product code (e.g., QAS), CFR reference (e.g., 21 CFR 892.2050), predicate class basis (if applicable)
- **EU MDR**: Annex VIII Rule number(s) (e.g., Rule 11), Implementing Rule 3.5 application (if multi-rule)
- **MFDS**: 품목분류번호 (e.g., A45020.01), 등급 근거 — Risk Matrix 결과 (디지털) 또는 품목분류표 직접 등재 (비디지털)

**CRITICAL**: Do NOT fabricate product codes or CFR references. If uncertain, state "requires regulatory database verification."

**MANDATORY OUTPUT FORMAT (must appear in response):**
```
### Regulatory Evidence
- **FDA**: Product Code [XXX] — 21 CFR § [section] (e.g., 21 CFR § 892.2050) — Predicate basis: [class basis or "N/A"]
- **EU MDR**: Rule [N] (Annex VIII) — [Implementing Rule 3.5 application if multi-rule] — MDCG: [guidance ref if applicable]
- **MFDS**: 품목분류번호 [Axxxxx.xx] or 7-Digit Code [XXXXXXX] — 등급 근거: [Risk Matrix 결과 (디지털) or 품목분류표 직접 등재 (비디지털)]
- **Citations**:
  - [FDA] 21 CFR § [specific section], Product Code: [code]
  - [EU MDR] Annex VIII Rule [N], [additional rules if applicable]
  - [MFDS] 품목코드 [code], [법적 근거]
```

**MANDATORY OUTPUT FORMAT (must appear in response):**
```
### Confidence & Escalation
- **Confidence Score**: [0-100]% — [basis: e.g., "exact product code match in MFDS DB"]
- **Escalation Level**: [1-4]
  - 1 = Automated processing sufficient
  - 2 = Brief expert review recommended
  - 3 = Expert review required (cross-region discrepancy or novel device)
  - 4 = Regulatory authority consultation required
- **Next Action**: [recommended next step]
```

### Step 6: (Optional) Classification Optimization Analysis

Analyze key decision factors for potential class reduction:
- Invasiveness: Can design reduce invasiveness level?
- Duration: Can contact duration be shortened?
- Active/Passive: Can device be made passive?
- Body System: Can device avoid high-risk anatomical locations?

**Optimization output constraints**:
- Abstract guidance only, NOT specific design recommendations
- Mandatory YELLOW traffic light
- Mandatory escalation to R&D + Regulatory affairs collaboration
- No guarantees of class reduction approval

---

## Traffic Light Criteria

### GREEN: Clear Classification
- All three regions have definitive class assignments
- Classification rules clearly applicable
- No borderline characteristics
- Standard regulatory pathway identified

### YELLOW: Conditional / Requires Attention
- One or more regions have borderline classification
- Classification optimization analysis requested
- Cross-region discrepancies exist
- Novel device type without clear precedent
- Mandatory escalation to human expert

### RED: Classification Blocked
- Unable to classify due to insufficient device information
- Conflicting classification rules with no resolution
- Device type outside known classification framework

---

## Escalation Path

### Ambiguous Classification Scenarios (YELLOW Traffic Light)
**Cross-Region Discrepancies**:
- Different classes assigned across FDA, EU MDR, MFDS
- Action: Regulatory strategy consultation to align global approach

**Borderline Between Classes**:
- Device characteristics straddle two classes
- Action: Regulatory specialist review + agency pre-submission meeting

### Novel Device Types (Mandatory Escalation)
**No Clear Precedent**:
- New technology without established classification pathway
- Action: De Novo pathway (FDA) or Innovation Office consultation (EU MDR)

### High-Risk Scenarios
- Class III FDA or EU MDR Class III
- Class 4 MFDS
- Implantable or life-sustaining devices
- Always requires comprehensive regulatory strategy

---

## Classification Optimization Logic

**Purpose**: Analyze key decision factors to identify potential pathways for class reduction through design modifications.

### 1. Invasiveness Factor
**Optimization Guidance**:
- If implantable: Consider alternative non-implantable designs
- If invasive: Evaluate minimally invasive or non-invasive approaches
- If non-invasive: Already optimal for this factor

### 2. Duration Factor
**Optimization Guidance**:
- If long-term: Explore short-term or transient use designs
- If short-term: Consider transient use if clinically feasible
- If transient: Already optimal for this factor

### 3. Active vs Passive Factor
**Optimization Guidance**:
- If active: Assess feasibility of passive design alternatives
- If passive: Already optimal for this factor

### 4. Anatomical Location Factor
**Optimization Guidance**:
- If CNS/cardiovascular: Explore designs avoiding direct contact with these systems
- If other high-risk locations: Consider alternative placement
- If low-risk location: Already optimal for this factor

### Optimization Disclaimer
Classification optimization analysis requires:
- R&D feasibility assessment
- Clinical performance validation
- Regulatory strategy alignment
- Potential additional clinical data requirements

---

## Data Source Strategy

1. **Built-in Knowledge** (Primary): Embedded classification rules from FDA, EU MDR Annex VIII, MFDS regulations
2. **Module Files** (On-demand): Detailed classification rules and decision trees (future)
3. **MCP Connectors** (Supplementary): Organization-specific classification precedents and verification

For MCP integration patterns (tool discovery, graceful degradation, source attribution), see `CONNECTORS.md`.
