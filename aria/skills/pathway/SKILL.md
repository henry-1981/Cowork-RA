---
name: aria-pathway
description: >
  Regulatory submission pathway analysis and recommendation for FDA, EU MDR, and MFDS.
  Evaluates submission routes based on device classification and provides strategic pathway recommendations with timelines.
allowed-tools: Read Grep Glob
user-invocable: false
metadata:
  version: "0.1.2"
  category: "domain"
  status: "active"
  updated: "2026-02-19"
  modularized: "false"
  tags: "pathway, regulatory, FDA, EU-MDR, MFDS, submission, 510(k), PMA, CE-mark"
  knowledge-base-date: "2026-01"

# MoAI Extension: Progressive Disclosure
progressive_disclosure:
  enabled: true
  level1_tokens: 100
  level2_tokens: 2500

# MoAI Extension: Triggers
triggers:
  keywords: ["pathway", "submission route", "regulatory pathway", "510(k)", "PMA", "CE mark"]
  phases: ["run"]
---

# Regulatory Pathway Analysis Skill

## Purpose

Identify regulatory submission pathways for FDA, EU MDR, and MFDS based on device classification. This is a pure analysis unit that receives classification results and returns pathway recommendations.

**Input**: Device classification results (FDA Class I/II/III, EU Class I/IIa/IIb/III, MFDS Grade 1-4)
**Output**: Pathway recommendations, timeline ranges, key requirements, traffic light indicator
**Knowledge Base Date**: 2026-01

---

## Decision Framework

### FDA Pathways

#### Class I Devices
- **510(k) Exempt**: Devices listed in exempt categories (21 CFR 862-892)
  - Pathway: Registration only
  - Timeline: 1-2 months
  - Requirements: Establishment registration, Device listing
  - Traffic Light: GREEN

- **510(k) Required**: Class I devices not in exempt categories
  - Pathway: 510(k) Premarket Notification
  - Timeline: 3-6 months (standard) or 1-3 months (expedited)
  - Requirements: Substantial equivalence to predicate device
  - Traffic Light: GREEN

#### Class II Devices
- **510(k) Premarket Notification** (most common)
  - Pathway: 510(k) submission with predicate device
  - Timeline: 3-6 months (standard) or 1-3 months (expedited)
  - Requirements: Predicate search, substantial equivalence demonstration, performance testing
  - Traffic Light: GREEN

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

#### Class III Devices
- **PMA (Premarket Approval)**
  - Pathway: Full clinical study and PMA submission
  - Timeline: 12-18+ months
  - Requirements: Clinical data, manufacturing quality system, risk analysis
  - Traffic Light: YELLOW (escalate to expert)

- **HDE (Humanitarian Device Exemption)**
  - When: Rare disease (<8,000 patients/year in US)
  - Timeline: 9-15 months
  - Requirements: IRB approval, probable benefit demonstration
  - Traffic Light: YELLOW (escalate to expert)

---

### EU MDR Pathways

#### Class I Devices
- **Self-Declaration (Annex IV)**
  - When: Non-sterile, non-measuring function
  - Pathway: Technical documentation + DoC
  - Timeline: 2-4 months
  - Requirements: Technical file, risk management, clinical evaluation
  - Notified Body: Not required
  - Traffic Light: GREEN

- **Notified Body Certification (Annex IV for sterile/measuring)**
  - When: Sterile or with measuring function
  - Pathway: Technical documentation + Notified Body review
  - Timeline: 4-6 months
  - Requirements: Technical file, sterility validation (if sterile)
  - Traffic Light: GREEN

#### Class IIa Devices
- **Notified Body Certification (Annex IX or X)**
  - Pathway: QMS certification (Annex IX) or Type Examination (Annex X)
  - Timeline: 6-12 months
  - Requirements: Technical documentation, Clinical Evaluation Report, Post-Market Surveillance Plan
  - Traffic Light: YELLOW (moderate complexity)

#### Class IIb Devices
- **Notified Body Certification (Annex IX or X)**
  - Pathway: Full QMS certification (Annex IX) or Type Examination + Product QMS (Annex X)
  - Timeline: 8-14 months
  - Requirements: Technical documentation, Clinical Evaluation Report, PMCF plan
  - Traffic Light: YELLOW (moderate-high complexity)

#### Class III Devices
- **Notified Body Full QMS Certification (Annex IX)**
  - Pathway: Full QMS review + clinical investigation
  - Timeline: 12-18+ months
  - Requirements: Clinical investigation data, comprehensive technical documentation
  - Traffic Light: YELLOW (escalate to expert)

---

### MFDS Pathways

#### MFDS Grade→Pathway Mapping (HARDCODED — Override NOT Permitted)

| Grade | Pathway (Korean) | Pathway (English) | Legal Basis | Timeline | Traffic Light |
|-------|------------------|--------------------|-------------|----------|---------------|
| **1등급** | **신고** (제품 신고) | Notification | 「의료기기법」 제12조 | 1-3 months | GREEN |
| **2등급** | **인증** (제품 인증) | Certification (TPR) | 「의료기기법」 제9조 | 3-9 months | GREEN-YELLOW |
| **3등급** | **허가** (품목 허가) | Approval (MFDS review) | 「의료기기법」 제6조 | 9-15 months | YELLOW |
| **4등급** | **허가** (품목 허가 + 임상) | Approval (MFDS review + clinical trial) | 「의료기기법」 제6조 | 12-18+ months | YELLOW |

**GROUND TRUTH RULES (absolute, no exceptions)**:
1. **1등급 = 신고 ONLY** — 1등급 제품은 절대로 인증이나 허가 대상이 아님
2. **2등급 = 인증 ONLY** — 2등급 제품은 반드시 인증 경로 (「의료기기법」 제9조). 허가(제6조)가 아님
3. **3-4등급 = 허가 ONLY** — 3등급 이상은 반드시 허가 경로 (「의료기기법」 제6조)
4. **하향 불가** — 허가 대상 제품을 인증이나 신고로 하향 불가
5. **상향 불가** — 인증 대상 제품을 불필요하게 허가로 상향 불가

#### Grade 1 Detail
- **Pathway**: 신고 (Notification) — 제조/수입 신고
- Requirements: Product specifications, labeling, manufacturing documentation
- Clinical Data: Not required
- MFDS Technical Review: Not required

#### Grade 2 Detail
- **Pathway**: 인증 (Certification/TPR) — 지정된 인증기관 심사
- Requirements: Non-clinical test data, risk analysis, labeling, 기술문서
- Clinical Data: Non-clinical testing sufficient for most devices
- MFDS Direct Review: Not required (인증기관이 심사)

#### Grade 3 Detail
- **Pathway**: 허가 (Approval) — MFDS 직접 심사
- Requirements: Clinical or comprehensive non-clinical data, risk management
- Clinical Data: Required for most Grade 3 devices

#### Grade 4 Detail
- **Pathway**: 허가 (Approval) — MFDS 직접 심사 + 임상시험
- Requirements: IRB-approved clinical trial, comprehensive clinical data
- Clinical Data: Mandatory clinical trial

---

## Analysis Workflow

### Step 1: Receive Classification Data

Accept classification results as input:
- FDA Class (I/II/III)
- EU MDR Class (I/IIa/IIb/III)
- MFDS Grade (1/2/3/4)
- Target regions

If classification data is not provided, return an error indicating classification is required first.

### Step 2: Select Pathways per Region

**FDA Pathway Selection Logic**:
- Class I + Exempt -> Registration only (GREEN, 1-2 months)
- Class I + Non-exempt -> 510(k) (GREEN, 3-6 months)
- Class II + Valid predicate -> 510(k) (GREEN, 3-6 months)
- Class II + No predicate -> De Novo (YELLOW, 6-12 months)
- Class III -> PMA (YELLOW, 12-18+ months)

**EU MDR Pathway Selection Logic**:
- Class I (non-sterile, non-measuring) -> Self-declaration (GREEN, 2-4 months)
- Class I (sterile or measuring) -> Notified Body Annex IV (GREEN, 4-6 months)
- Class IIa -> Notified Body Annex IX/X (YELLOW, 6-12 months)
- Class IIb -> Notified Body Annex IX/X (YELLOW, 8-14 months)
- Class III -> Notified Body Annex IX + Clinical Investigation (YELLOW, 12-18+ months)

**MFDS Pathway Selection Logic** (HARDCODED):
- Grade 1 -> 신고/Notification (GREEN, 1-3 months) — 「의료기기법」 제12조
- Grade 2 -> 인증/Certification (GREEN-YELLOW, 3-9 months) — 「의료기기법」 제9조
- Grade 3 -> 허가/Approval (YELLOW, 9-15 months) — 「의료기기법」 제6조
- Grade 4 -> 허가/Approval + Clinical Trial (YELLOW, 12-18+ months) — 「의료기기법」 제6조

### Step 3: Multi-Region Comparison

When multiple target regions selected:
- Generate comparison table: Region | Pathway | Timeline | Key Requirements
- Identify critical path (longest timeline)
- Highlight common dependencies (e.g., shared testing data)
- Recommend parallel vs. sequential submission strategy

### Step 4: Assign Overall Traffic Light

- **GREEN**: All pathways are low-risk (Class I/IIa, Grade 1-2, no clinical trials)
- **YELLOW**: Any pathway requires Notified Body, clinical data, or De Novo/PMA

### Step 5: Return Structured Result

Return the pathway analysis containing:
- Selected pathway per region with rationale
- Timeline ranges (optimistic/expected/pessimistic)
- Key requirements per pathway
- Multi-region comparison (if applicable)
- Critical path identification
- Traffic light assessment

#### Evidence Requirements (per pathway)

Each pathway recommendation MUST include specific regulatory citations:

- **FDA**: Submission type reference (e.g., 21 CFR 807 Subpart E for 510(k)), relevant guidance document(s), DEN/510(k)/PMA precedent (if known)
  - **CRITICAL**: Do NOT fabricate DEN/510(k)/PMA numbers. These are FDA-assigned identifiers.
  - If a specific precedent is recalled, prefix with "Believed to be" + recommend verification
  - If unknown: "Specific precedent number requires FDA database verification"
- **EU MDR**: Annex reference (IV, IX, X), applicable MDCG guidance (e.g., MDCG 2020-5 for clinical evaluation)
- **MFDS**: 의료기기법 조항 (제6조 허가/제9조 인증/제12조 신고), 인증기관 요건 (if applicable)

---

## Traffic Light Definitions

- **GREEN**: Low-risk pathways (Class I/IIa, Grade 1-2, no clinical trials, no Notified Body for complex reviews)
- **YELLOW**: Moderate-high risk (Class IIb/III, Grade 3-4, De Novo, PMA, clinical trials required, Notified Body for Class IIb/III)
- **RED**: Not used in pathway skill (all valid classifications have a pathway)

---

## Escalation Scenarios

Escalate to regulatory expert when:
- FDA Class III device (PMA pathway)
- EU MDR Class III device (clinical investigation required)
- MFDS Grade 4 device (clinical trial required)
- De Novo pathway (no predicate device)
- Multi-region submission with conflicting timelines

---

## Data Source Strategy

1. **Built-in Knowledge** (Primary): Embedded pathway frameworks from FDA, EU MDR, MFDS regulations
2. **Classification Data** (Input): Classification results from determination/classification skills
3. **MCP Connectors** (Supplementary): Organization-specific pathway precedents and timeline data

For MCP integration patterns (tool discovery, graceful degradation, source attribution), see `CONNECTORS.md`.
