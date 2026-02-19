---
name: aria-classification
description: >
  Multi-region device classification skill for FDA, EU MDR, and MFDS.
  Determines regulatory class (FDA I/II/III, EU I/IIa/IIb/III, MFDS 1/2/3/4)
  based on device characteristics. Use for regulatory class determination.
allowed-tools: Read Grep Glob
user-invocable: false
metadata:
  version: "0.1.1"
  category: "domain"
  status: "active"
  updated: "2026-02-19"
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
