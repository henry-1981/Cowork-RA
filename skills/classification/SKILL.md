---
name: aria-classification
description: >
  Multi-region device classification skill for FDA, EU MDR, and MFDS.
  Determines regulatory class (FDA I/II/III, EU I/IIa/IIb/III, MFDS 1/2/3/4)
  based on device characteristics. Supports classification optimization analysis
  with --optimize flag. Use for regulatory class determination and pathway planning.
---

# Medical Device Classification Skill

## Quick Reference

**Purpose**: Determine regulatory class across FDA, EU MDR, and MFDS jurisdictions.

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

**Expected Input**:
- Device characteristics (from determination step or direct input)
- Invasiveness level
- Duration of use
- Active/passive classification
- Body system interaction

**Expected Output**:
- Multi-region classification matrix
- Rationale and rule references
- Traffic light per region
- Optional: Classification optimization analysis (--optimize flag)

**Knowledge Base Date**: 2026-01

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
- Short-term invasive devices (≤30 days)
- Transient use with specific body systems
- Examples: Contact lenses, hearing aids

**Decision Rules**:
- Rule 5: Non-invasive devices channeling/storing body substances - IIa
- Rule 6: Short-term invasive surgically devices - IIa

#### Class IIb (Medium-High Risk)
- Long-term invasive devices (>30 days)
- Active therapeutic devices
- Examples: Lung ventilators, bone screws

**Decision Rules**:
- Rule 8: Long-term implantable devices (except teeth/Rule 8 exceptions) - IIb
- Rule 11: Active therapeutic devices for energy delivery - IIb

#### Class III (High Risk)
- Devices in direct contact with heart, central circulatory system, CNS
- Implantable/long-term devices affecting vital functions
- Examples: Heart valves, drug-eluting stents

**Decision Rules**:
- Rule 9: Active therapeutic devices for life-support/vital functions - III
- Rule 10: Devices with biological substances - III

### MFDS Classification Criteria

#### Class 1 (낮은 위해도)
- 인체에 미치는 잠재적 위해성이 거의 없음
- 예: 의료용 가위, 핀셋, 설압자

#### Class 2 (낮은 위해도 ~ 중간 위해도)
- 인체에 미치는 잠재적 위해성이 낮거나 그 사용 방법이 간단한 의료기기
- 예: MRI, 초음파 영상진단기, 전동휠체어

**분류 기준**:
- 비침습 또는 최소 침습
- 일시적 접촉
- 고장 시 위해 가능성 낮음

#### Class 3 (중간 위해도 ~ 높은 위해도)
- 인체에 미치는 잠재적 위해성이 중간이거나 그 사용 방법이 비교적 복잡한 의료기기
- 예: 인공호흡기, 혈액투석기, 콘택트렌즈

**분류 기준**:
- 침습적 사용
- 중기 또는 장기 접촉
- 능동형 의료기기

#### Class 4 (높은 위해도)
- 인체에 미치는 잠재적 위해성이 높거나 고장 및 오작동 시 생명에 중대한 위해를 줄 수 있는 의료기기
- 예: 심박조율기, 인공심장판막, 스텐트

**분류 기준**:
- 이식형 의료기기
- 생명 유지 장치
- 중추신경계 또는 심혈관계 직접 접촉

---

## Declarative Workflow

### Step 1: Extract Device Characteristics
- Device type and intended use
- Invasiveness level (non-invasive, invasive, implantable)
- Duration of contact (transient <60min, short-term ≤30 days, long-term >30 days)
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
1. Assess potential harm level
2. Evaluate complexity of use
3. Check for implantable or life-sustaining characteristics
4. Consider Korean regulatory nuances
5. Assign MFDS Class (1, 2, 3, or 4)

### Step 5: Generate Classification Matrix
- Consolidate multi-region classifications
- Identify classification rationale per region
- Reference applicable rules and regulations
- Flag any discrepancies between regions
- Attribute data sources

### Step 6: (Optional) Classification Optimization Analysis
**Triggered by**: --optimize flag (OR-004)

Analyze key decision factors for potential class reduction:
- Invasiveness: Can design reduce invasiveness level?
- Duration: Can contact duration be shortened?
- Active/Passive: Can device be made passive?
- Body System: Can device avoid high-risk anatomical locations?

**Output**:
- Abstract guidance per factor (no specific design changes)
- Potential class reduction pathways
- Mandatory YELLOW traffic light
- Mandatory escalation recommendation
- Supplementary disclaimer

### Step 7: Summary Generation (Context Simplifier)
Generate compressed summary in Key-Value Markdown format:

```markdown
- **FDA Class**: [I/II/III]
- **EU MDR Class**: [I/IIa/IIb/III]
- **MFDS Class**: [1/2/3/4]
- **Traffic Light**: [GREEN/YELLOW/RED per region]
- **Key Factors**: [Invasiveness, Duration, Active/Passive]
- **Optimization Analyzed**: [Yes/No]
- **Escalation**: [Yes/No + reason]
- **Sources**: [Data sources: Notion/Built-in/Context7]
```

---

## Output Template

### Header
```
Command: /aria:classify
Product: {product-name}
Date: {YYYY-MM-DD}
Version: {version-number}
Optimization: {enabled/disabled}
```

### Input Summary
- Device Description: {description}
- Invasiveness: {non-invasive/invasive/implantable}
- Duration: {transient/short-term/long-term}
- Active/Passive: {active/passive}
- Body System: {system}
- Anatomical Location: {location}

### Multi-Region Classification Matrix

| Region | Class | Risk Level | Rationale | Traffic Light |
|--------|-------|------------|-----------|---------------|
| FDA | {I/II/III} | {Low/Moderate/High} | {rationale} | {GREEN/YELLOW/RED} |
| EU MDR | {I/IIa/IIb/III} | {Low/Medium-Low/Medium-High/High} | {rationale} | {GREEN/YELLOW/RED} |
| MFDS | {1/2/3/4} | {낮음/낮음-중간/중간-높음/높음} | {rationale} | {GREEN/YELLOW/RED} |

### Rationale and Rule References

**FDA Classification**:
- Class: {I/II/III}
- Regulatory Pathway: {510(k)/PMA/De Novo}
- Key Decision Factors: {factors}

**EU MDR Classification**:
- Class: {I/IIa/IIb/III}
- Applicable Rules: {Annex VIII rules}
- Key Decision Factors: {factors}

**MFDS Classification**:
- Class: {1/2/3/4}
- 위해도 평가: {evaluation}
- 주요 분류 기준: {criteria}

### Traffic Light Per Region
- **FDA**: [GREEN/YELLOW/RED] - {explanation}
- **EU MDR**: [GREEN/YELLOW/RED] - {explanation}
- **MFDS**: [GREEN/YELLOW/RED] - {explanation}

### Data Source Attribution
- Notion DB: {used/not available}
- Built-in Knowledge: {used}
- Context7 Supplementation: {used/not needed}

### Escalation Recommendations
{If YELLOW or ambiguous classifications}:
- Escalation Reason: {reason}
- Recommended Actions: {actions}

### Next Steps
1. {Primary next step, typically /aria:pathway}
2. {Optional secondary step}
3. {Optional tertiary step}

### Standard Disclaimer
⚠️ **중요 고지사항**

본 분류 결과는 AI 기반 regulatory intelligence tool의 분석이며, 공식적인 규제 분류가 아닙니다.

- **법적 효력 없음**: 본 결과는 참고용이며 법적 구속력이 없습니다
- **전문가 검토 필수**: 실제 규제 제출 전 regulatory affairs 전문가 검토가 반드시 필요합니다
- **규제 기관 확인**: 최종 분류는 FDA, Notified Body, MFDS 등 규제 기관의 공식 결정을 따릅니다
- **책임 한계**: 본 도구 사용으로 인한 규제 미준수 책임은 사용자에게 있습니다

Knowledge Base Date: 2026-01 기준

{If --optimize flag used, add:}

### Supplementary Disclaimer (Classification Optimization)
⚠️ **분류 최적화 분석 추가 고지사항**

본 분류 최적화 분석은 잠재적 설계 변경 방향에 대한 추상적 가이드이며, 구체적인 설계 권고가 아닙니다.

- **YELLOW 트래픽 라이트 필수**: 최적화 분석은 항상 YELLOW 상태로 표시됩니다
- **필수 에스컬레이션**: Regulatory affairs + R&D 전문가 협의 필수
- **규제 전략 영향**: 설계 변경이 규제 전략에 미치는 영향 사전 평가 필요
- **임상 데이터**: 설계 변경 시 추가 임상 시험 필요 여부 검토 필수

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

## Traffic Light Criteria

### GREEN: Clear Classification
- All three regions have definitive class assignments
- Classification rules clearly applicable
- No borderline characteristics
- Standard regulatory pathway identified
- Low risk of classification challenge

### YELLOW: Conditional / Requires Attention
- One or more regions have borderline classification
- Classification optimization analysis requested (--optimize)
- Cross-region discrepancies exist
- Novel device type without clear precedent
- Requires regulatory specialist review before proceeding
- Mandatory escalation to human expert

### RED: Classification Blocked
- Unable to classify due to insufficient device information
- Conflicting classification rules with no resolution
- Device type outside known classification framework
- Cannot proceed without additional data or expert consultation

---

## Classification Optimization Logic (OR-004)

**Activation**: --optimize flag present in command invocation

**Purpose**: Analyze key decision factors to identify potential pathways for class reduction through design modifications.

**Analysis Framework**:

### 1. Invasiveness Factor
**Current State**: {non-invasive/invasive/implantable}

**Optimization Guidance**:
- If implantable: Consider alternative non-implantable designs
- If invasive: Evaluate minimally invasive or non-invasive approaches
- If non-invasive: Already optimal for this factor

**Potential Impact**: Invasiveness reduction may lower class assignment

### 2. Duration Factor
**Current State**: {transient/short-term/long-term}

**Optimization Guidance**:
- If long-term: Explore short-term or transient use designs
- If short-term: Consider transient use if clinically feasible
- If transient: Already optimal for this factor

**Potential Impact**: Duration reduction may lower class assignment

### 3. Active vs Passive Factor
**Current State**: {active/passive}

**Optimization Guidance**:
- If active: Assess feasibility of passive design alternatives
- If passive: Already optimal for this factor

**Potential Impact**: Passive devices generally lower class than active equivalents

### 4. Anatomical Location Factor
**Current State**: {CNS/cardiovascular/other}

**Optimization Guidance**:
- If CNS/cardiovascular: Explore designs avoiding direct contact with these systems
- If other high-risk locations: Consider alternative placement
- If low-risk location: Already optimal for this factor

**Potential Impact**: Avoiding high-risk anatomical locations may lower class

### Optimization Output Constraints
- **Abstract Only**: Provide general guidance, NOT specific design recommendations
- **Mandatory YELLOW**: All optimization analyses must show YELLOW traffic light
- **Mandatory Escalation**: Always escalate to R&D + Regulatory affairs collaboration
- **No Guarantees**: Optimization suggestions do not guarantee class reduction approval

### Optimization Disclaimer
Classification optimization analysis requires:
- R&D feasibility assessment
- Clinical performance validation
- Regulatory strategy alignment
- Potential additional clinical data requirements
