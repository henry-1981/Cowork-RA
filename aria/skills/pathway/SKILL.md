---
name: aria-pathway
description: >
  Regulatory submission pathway analysis and recommendation for FDA, EU MDR, and MFDS.
  Evaluates submission routes based on device classification and provides strategic pathway recommendations with timelines.
allowed-tools: Read Grep Glob
user-invocable: false
metadata:
  version: "0.1.0"
  category: "domain"
  status: "active"
  updated: "2026-02-12"
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
  - When: No valid predicate exists, low-moderate risk device
  - Timeline: 6-12 months
  - Requirements: Special controls, risk mitigation documentation
  - Traffic Light: YELLOW (escalate to expert)

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

#### Grade 1
- **Product Registration (제품 신고)**
  - Pathway: Registration with MFDS
  - Timeline: 1-3 months
  - Requirements: Product specifications, labeling, manufacturing documentation
  - Clinical Data: Not required
  - Traffic Light: GREEN

#### Grade 2
- **Product Approval (제품 허가)**
  - Pathway: Pre-market approval submission
  - Timeline: 3-9 months
  - Requirements: Non-clinical test data, risk analysis, labeling
  - Clinical Data: Non-clinical testing sufficient for most devices
  - Traffic Light: GREEN to YELLOW (depending on complexity)

#### Grade 3
- **Product Approval with Clinical Data (제품 허가)**
  - Pathway: Pre-market approval with clinical/non-clinical data
  - Timeline: 9-15 months
  - Requirements: Clinical or comprehensive non-clinical data, risk management
  - Traffic Light: YELLOW (escalate to expert)

#### Grade 4
- **Product Approval with Clinical Trial (제품 허가 with 임상시험)**
  - Pathway: Clinical trial + pre-market approval
  - Timeline: 12-18+ months
  - Requirements: IRB-approved clinical trial, comprehensive clinical data
  - Traffic Light: YELLOW (escalate to expert)

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

**MFDS Pathway Selection Logic**:
- Grade 1 -> Registration (GREEN, 1-3 months)
- Grade 2 -> Approval (GREEN-YELLOW, 3-9 months)
- Grade 3 -> Approval with clinical data (YELLOW, 9-15 months)
- Grade 4 -> Approval with clinical trial (YELLOW, 12-18+ months)

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
