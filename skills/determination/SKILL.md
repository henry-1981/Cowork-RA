---
name: aria-determination
description: >
  Medical device determination skill for FDA, EU MDR, and MFDS regulations.
  Evaluates whether a product qualifies as a medical device and determines
  initial classification. Use for device status evaluation, borderline
  product analysis, and regulatory scope determination.
---

# Medical Device Determination Skill

## Quick Reference

**Purpose**: Evaluate whether a product qualifies as a medical device under FDA, EU MDR, and MFDS regulations.

**Key Decision Criteria**:
- Intended use for diagnosis, treatment, cure, or mitigation
- Structure and function characteristics
- Regulatory definitions and exclusions

**Expected Input**:
- Device description
- Intended use statement
- Product form (hardware, software, combination)
- Primary function

**Expected Output**:
- Determination result (YES/NO/CONDITIONAL)
- Traffic light status (GREEN/YELLOW/RED)
- Applicable regulations
- Escalation recommendations

**Knowledge Base Date**: 2026-01

---

## Decision Framework

### FDA Device Definition (21 CFR 201(h))

A medical device is an instrument, apparatus, implement, machine, contrivance, implant, in vitro reagent, or other similar or related article that is:

1. **Intended Use Criteria**:
   - Diagnosis of disease or other conditions
   - Cure, mitigation, treatment, or prevention of disease
   - Affecting the structure or function of the body

2. **Key Decision Factors**:
   - Does NOT achieve primary intended purpose through chemical action
   - Does NOT achieve primary intended purpose by being metabolized

3. **Exclusions**:
   - Products that achieve effects primarily through chemical/metabolic means (typically drugs)
   - General wellness products without medical claims

### EU MDR Article 2(1) Classification

Medical device means any instrument, apparatus, appliance, software, implant, reagent, material or other article intended by the manufacturer to be used for human beings for one or more specific medical purposes:

1. **Medical Purpose Criteria**:
   - Diagnosis, prevention, monitoring, prediction, prognosis, treatment or alleviation of disease
   - Diagnosis, monitoring, treatment, alleviation or compensation for an injury or disability
   - Investigation, replacement or modification of anatomy or physiological/pathological process or state
   - Providing information by means of in vitro examination of specimens from human body

2. **Borderline Products**:
   - Products with ancillary medical purpose may still qualify
   - Combination products require case-by-case evaluation

### MFDS Device Criteria

의료기기는 사람이나 동물에게 다음 목적으로 사용되는 기구, 기계, 장치, 재료, 소프트웨어 또는 이와 유사한 제품:

1. **적용 범위**:
   - 질병의 진단, 치료, 경감, 처치 또는 예방 목적
   - 상해 또는 장애의 진단, 치료, 경감 또는 보정 목적
   - 구조 또는 기능의 검사, 대체 또는 변형 목적
   - 임신 조절 목적

2. **한국 고유 규정**:
   - 의약품과의 명확한 구분
   - 화학적 작용이 주된 효과가 아님

---

## Declarative Workflow

### Step 1: Extract Device Information
- Device description and physical characteristics
- Intended use statement (medical purpose)
- Product form (hardware, software, IVD, combination)
- Primary function and mechanism of action

### Step 2: Apply FDA Decision Tree
1. Check intended use against FDA criteria
2. Evaluate structure/function characteristics
3. Assess chemical action vs mechanical/physical action
4. Review exclusions and exemptions
5. Determine device status: YES/NO/CONDITIONAL

### Step 3: Apply EU MDR Criteria
1. Check intended use against medical purpose criteria
2. Evaluate if ancillary medical purpose applies
3. Assess borderline product scenarios
4. Consider combination product rules
5. Determine device status: YES/NO/CONDITIONAL

### Step 4: Apply MFDS Criteria
1. Check intended use against Korean regulatory scope
2. Evaluate distinction from pharmaceuticals
3. Assess mechanism of action (chemical vs non-chemical)
4. Review local classification nuances
5. Determine device status: YES/NO/CONDITIONAL

### Step 5: Generate Determination Result
- Consolidate multi-region determination
- Assign traffic light status based on criteria
- Identify applicable regulations
- Flag escalation scenarios if borderline
- Attribute data sources (Notion DB, built-in, Context7)

### Step 6: Summary Generation (Context Simplifier)
Generate compressed summary in Key-Value Markdown format:

```markdown
- **Decision**: [YES/NO/CONDITIONAL]
- **Traffic Light**: [GREEN/YELLOW/RED]
- **FDA Status**: [Device/Non-device/Conditional]
- **EU MDR Status**: [Device/Non-device/Conditional]
- **MFDS Status**: [Device/Non-device/Conditional]
- **Key Factors**: [Primary factors affecting determination]
- **Escalation**: [Yes/No + reason]
- **Sources**: [Data sources: Notion/Built-in/Context7]
```

---

## Output Template

### Header
```
Command: /aria:determine
Product: {product-name}
Date: {YYYY-MM-DD}
Version: {version-number}
```

### Input Summary
- Device Description: {description}
- Intended Use: {intended-use}
- Product Form: {form}
- Primary Function: {function}

### Determination Checklist

**FDA Device Status**: [YES/NO/CONDITIONAL]
- Intended Use: {meets/does not meet} FDA criteria
- Structure/Function: {meets/does not meet} requirements
- Exclusions: {none apply / applicable exclusions}

**EU MDR Device Status**: [YES/NO/CONDITIONAL]
- Medical Purpose: {meets/does not meet} criteria
- Borderline Assessment: {clear medical device / requires evaluation}

**MFDS Device Status**: [YES/NO/CONDITIONAL]
- Regulatory Scope: {within/outside} Korean device definition
- Pharmaceutical Distinction: {clear distinction / requires evaluation}

### Traffic Light Assessment
- **Status**: [GREEN/YELLOW/RED]
- **Rationale**: {explanation}

### Data Source Attribution
- Notion DB: {used/not available}
- Built-in Knowledge: {used}
- Context7 Supplementation: {used/not needed}

### Escalation Recommendations
{If YELLOW or borderline scenarios}:
- Escalation Reason: {reason}
- Recommended Actions: {actions}

### Next Steps
1. {Primary next step, typically /aria:classify}
2. {Optional secondary step}
3. {Optional tertiary step}

### Disclaimer
⚠️ **중요 고지사항**

본 판정 결과는 AI 기반 regulatory intelligence tool의 분석이며, 공식적인 규제 자문이 아닙니다.

- **법적 효력 없음**: 본 결과는 참고용이며 법적 구속력이 없습니다
- **전문가 검토 필수**: 실제 규제 제출 전 regulatory affairs 전문가 검토가 반드시 필요합니다
- **규제 기관 확인**: 최종 판정은 FDA, Notified Body, MFDS 등 규제 기관의 공식 결정을 따릅니다
- **책임 한계**: 본 도구 사용으로 인한 규제 미준수 책임은 사용자에게 있습니다

Knowledge Base Date: 2026-01 기준

---

## Escalation Path

### Borderline Cases (YELLOW Traffic Light)
**Wellness vs Medical Device**:
- Product claims general wellness benefits but borders on medical claims
- Action: Regulatory affairs specialist review + FDA guidance consultation

**Combination Products**:
- Product combines device and drug/biologic components
- Action: Combination product classification determination (separate process)

**Novel Device Types**:
- New technology without clear regulatory precedent
- Action: Pre-submission meeting with regulatory agency recommended

### High-Risk Scenarios (Mandatory Escalation)
- Conflicting determinations across regions
- Ambiguous intended use statements
- Products with both medical and non-medical claims

---

## Traffic Light Criteria

### GREEN: Clear Medical Device Status
- Intended use clearly meets medical device definition
- All three regions (FDA, EU MDR, MFDS) agree on device status
- No borderline characteristics
- Standard regulatory pathway applicable

### YELLOW: Borderline / Conditional Status
- Intended use has medical and non-medical components
- One or more regions have conditional determination
- Borderline product characteristics present
- Requires regulatory specialist review before proceeding
- Mandatory escalation to human expert

### RED: Not a Medical Device
- Intended use does not meet medical device criteria in any region
- Product is clearly outside regulatory scope
- May be classified as consumer product, cosmetic, or other category
- No medical device regulatory pathway applicable
