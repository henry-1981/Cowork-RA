---
name: aria-pathway
description: >
  Regulatory submission pathway analysis and recommendation for FDA, EU MDR, and MFDS.
  Evaluates submission routes based on device classification and provides strategic pathway recommendations with timelines.
allowed-tools: Read Grep Glob ToolSearch
user-invocable: false
metadata:
  version: "0.0.4"
  category: "domain"
  status: "active"
  updated: "2026-02-11"
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

## Quick Reference

**Purpose**: Identify regulatory submission pathways for FDA, EU MDR, and MFDS based on device classification.

**Input**: Device classification results (Class I/II/III for FDA, Class I/IIa/IIb/III for EU, Grade 1-4 for MFDS)
**Output**: Pathway recommendations, timeline ranges, key requirements, traffic light indicator
**Knowledge Base Date**: 2026-01

---

## Decision Framework

### FDA Pathways

#### Class I Devices
- **510(k) Exempt**: Devices listed in exempt categories (21 CFR 862-892)
  - Pathway: Registration only
  - Timeline: 1-2개월
  - Requirements: Establishment registration, Device listing
  - Traffic Light: 🟢 GREEN

- **510(k) Required**: Class I devices not in exempt categories
  - Pathway: 510(k) Premarket Notification
  - Timeline: 3-6개월 (standard) or 1-3개월 (expedited)
  - Requirements: Substantial equivalence to predicate device
  - Traffic Light: 🟢 GREEN

#### Class II Devices
- **510(k) Premarket Notification** (most common)
  - Pathway: 510(k) submission with predicate device
  - Timeline: 3-6개월 (standard) or 1-3개월 (expedited)
  - Requirements: Predicate search, substantial equivalence demonstration, performance testing
  - Traffic Light: 🟢 GREEN

- **De Novo Classification Request**
  - When: No valid predicate exists, low-moderate risk device
  - Timeline: 6-12개월
  - Requirements: Special controls, risk mitigation documentation
  - Traffic Light: 🟡 YELLOW (escalate to expert)

#### Class III Devices
- **PMA (Premarket Approval)**
  - Pathway: Full clinical study and PMA submission
  - Timeline: 12-18+개월
  - Requirements: Clinical data, manufacturing quality system, risk analysis
  - Traffic Light: 🟡 YELLOW (escalate to expert)

- **HDE (Humanitarian Device Exemption)**
  - When: Rare disease (<8,000 patients/year in US)
  - Timeline: 9-15개월
  - Requirements: IRB approval, probable benefit demonstration
  - Traffic Light: 🟡 YELLOW (escalate to expert)

---

### EU MDR Pathways

#### Class I Devices
- **Self-Declaration (Annex IV)**
  - When: Non-sterile, non-measuring function
  - Pathway: Technical documentation + DoC
  - Timeline: 2-4개월
  - Requirements: Technical file, risk management, clinical evaluation
  - Notified Body: Not required
  - Traffic Light: 🟢 GREEN

- **Notified Body Certification (Annex IV for sterile/measuring)**
  - When: Sterile or with measuring function
  - Pathway: Technical documentation + Notified Body review
  - Timeline: 4-6개월
  - Requirements: Technical file, sterility validation (if sterile)
  - Traffic Light: 🟢 GREEN

#### Class IIa Devices
- **Notified Body Certification (Annex IX or X)**
  - Pathway: QMS certification (Annex IX) or Type Examination (Annex X)
  - Timeline: 6-12개월
  - Requirements: Technical documentation, Clinical Evaluation Report, Post-Market Surveillance Plan
  - Traffic Light: 🟡 YELLOW (moderate complexity)

#### Class IIb Devices
- **Notified Body Certification (Annex IX or X)**
  - Pathway: Full QMS certification (Annex IX) or Type Examination + Product QMS (Annex X)
  - Timeline: 8-14개월
  - Requirements: Technical documentation, Clinical Evaluation Report, PMCF plan
  - Traffic Light: 🟡 YELLOW (moderate-high complexity)

#### Class III Devices
- **Notified Body Full QMS Certification (Annex IX)**
  - Pathway: Full QMS review + clinical investigation
  - Timeline: 12-18+개월
  - Requirements: Clinical investigation data, comprehensive technical documentation
  - Traffic Light: 🟡 YELLOW (escalate to expert)

---

### MFDS Pathways

#### Grade 1 (Class I equivalent)
- **제품 신고 (Product Registration)**
  - Pathway: Registration with MFDS
  - Timeline: 1-3개월
  - Requirements: Product specifications, labeling, manufacturing documentation
  - Clinical Data: Not required
  - Traffic Light: 🟢 GREEN

#### Grade 2 (Class II equivalent)
- **제품 허가 (Product Approval)**
  - Pathway: Pre-market approval submission
  - Timeline: 3-9개월
  - Requirements: Non-clinical test data, risk analysis, labeling
  - Clinical Data: Non-clinical testing sufficient for most devices
  - Traffic Light: 🟢 GREEN to 🟡 YELLOW (depending on complexity)

#### Grade 3 (Class III equivalent)
- **제품 허가 (Product Approval with Clinical Data)**
  - Pathway: Pre-market approval with clinical/non-clinical data
  - Timeline: 9-15개월
  - Requirements: Clinical or comprehensive non-clinical data, risk management
  - Traffic Light: 🟡 YELLOW (escalate to expert)

#### Grade 4 (Highest risk)
- **제품 허가 with 임상시험 (Product Approval with Clinical Trial)**
  - Pathway: Clinical trial + pre-market approval
  - Timeline: 12-18+개월
  - Requirements: IRB-approved clinical trial, comprehensive clinical data
  - Traffic Light: 🟡 YELLOW (escalate to expert)

---

## Workflow

### Step 1: Load Classification Data

Use classification results from prior `/aria:classify` execution:
- Check for `.aria/products/<product-name>/<date>/classification.summary.md`
- Extract device classification for each target region
- If classification data NOT available:
  - Display warning: **"⚠️ 분류 데이터가 없습니다. 먼저 `/aria:classify` 명령을 실행하세요."**
  - Traffic Light: 🟡 YELLOW
  - STOP workflow

### Step 2: Select Pathways per Region

Based on loaded classification data:

**FDA Pathway Selection Logic**:
- Class I + Exempt → Registration only (🟢 GREEN, 1-2개월)
- Class I + Non-exempt → 510(k) (🟢 GREEN, 3-6개월)
- Class II + Valid predicate → 510(k) (🟢 GREEN, 3-6개월)
- Class II + No predicate → De Novo (🟡 YELLOW, 6-12개월)
- Class III → PMA (🟡 YELLOW, 12-18+개월)

**EU MDR Pathway Selection Logic**:
- Class I (non-sterile, non-measuring) → Self-declaration (🟢 GREEN, 2-4개월)
- Class I (sterile or measuring) → Notified Body Annex IV (🟢 GREEN, 4-6개월)
- Class IIa → Notified Body Annex IX/X (🟡 YELLOW, 6-12개월)
- Class IIb → Notified Body Annex IX/X (🟡 YELLOW, 8-14개월)
- Class III → Notified Body Annex IX + Clinical Investigation (🟡 YELLOW, 12-18+개월)

**MFDS Pathway Selection Logic**:
- Grade 1 → 신고 (🟢 GREEN, 1-3개월)
- Grade 2 → 허가 (🟢-🟡, 3-9개월)
- Grade 3 → 허가 with clinical data (🟡 YELLOW, 9-15개월)
- Grade 4 → 허가 with clinical trial (🟡 YELLOW, 12-18+개월)

### Step 3: Multi-Region Comparison

When multiple target regions selected:
- Generate comparison table: Region | Pathway | Timeline | Key Requirements
- Identify critical path (longest timeline)
- Highlight common dependencies (e.g., shared testing data)
- Recommend parallel vs. sequential submission strategy

### Step 4: Assign Overall Traffic Light

- **🟢 GREEN**: All pathways are low-risk (Class I/IIa, Grade 1-2, no clinical trials)
- **🟡 YELLOW**: Any pathway requires Notified Body, clinical data, or De Novo/PMA

### Step 5: Generate Output

Output structure (Korean language):

```markdown
# 규제 경로 분석 결과

## 제품 정보
- 제품명: [Product Name]
- 분석 일자: [YYYY-MM-DD]

## 경로 권장사항

### FDA (미국)
- **경로**: [Pathway Name in Korean]
- **예상 소요 기간**: [Timeline Range]
- **주요 요구사항**:
  - [Requirement 1]
  - [Requirement 2]
- **데이터 출처**: FDA 510(k) Guidance / FDA PMA Guidance

### EU MDR (유럽)
- **경로**: [Pathway Name in Korean]
- **예상 소요 기간**: [Timeline Range]
- **인증 기관 필요 여부**: [Yes/No]
- **주요 요구사항**:
  - [Requirement 1]
  - [Requirement 2]
- **데이터 출처**: EU MDR Annex IV/IX/X

### MFDS (한국)
- **경로**: [Pathway Name in Korean]
- **예상 소요 기간**: [Timeline Range]
- **주요 요구사항**:
  - [Requirement 1]
  - [Requirement 2]
- **데이터 출처**: 의료기기법 시행규칙

## 다중 시장 비교표

| 지역 | 경로 | 소요 기간 | 주요 요구사항 |
|------|------|-----------|---------------|
| FDA  | [...] | [...개월] | [...]         |
| EU MDR | [...] | [...개월] | [...]       |
| MFDS | [...] | [...개월] | [...]        |

**최장 경로 (Critical Path)**: [Region with longest timeline]

## 위험도 평가
- **Traffic Light**: [🟢 GREEN / 🟡 YELLOW]
- **평가**: [Risk assessment in Korean]

[If YELLOW]: **⚠️ 전문가 검토 권장**: 해당 경로는 복잡도가 높으므로 규제 전문가와 상담하시기 바랍니다.

## 다음 단계 제안
1. `/aria:estimate` 명령으로 비용 및 일정 추정
2. 규제 전문가와 경로 선택 검토
3. 각 시장별 준비 문서 목록 확인

## 면책 조항
⚠️ **본 자료는 참고 정보이며, 규제 자문이 아닙니다.** 실제 규제 경로는 제품 특성, 시장 상황, 규제 기관 요구사항에 따라 달라질 수 있습니다. 최종 결정 전 규제 전문가와 상담하시기 바랍니다.

---
**생성 일시**: [Timestamp]
```

### Step 6: Generate Context Simplifier Summary

Create `.summary.md` file for downstream pipeline:

```markdown
# Pathway Summary

**Product**: [Product Name]
**Date**: [YYYY-MM-DD]

## Selected Pathways
- **FDA**: [Pathway] ([Timeline])
- **EU MDR**: [Pathway] ([Timeline])
- **MFDS**: [Pathway] ([Timeline])

## Critical Path
- **Region**: [Region with longest timeline]
- **Duration**: [Timeline]

## Traffic Light
- **Overall Risk**: [GREEN/YELLOW]

---
This summary is consumed by `/aria:estimate` and `/aria:plan` commands.
```

---

## Data Source Strategy

1. **Built-in Knowledge** (Primary): Embedded pathway frameworks from FDA, EU MDR, MFDS regulations
2. **Loaded Classification Data** (Input): `.summary.md` from `/aria:classify`
3. **Notion MCP** (Supplementary): Organization-specific pathway precedents and timeline data
4. **Context7 MCP** (Verification): External regulatory pathway document verification

For MCP integration patterns (tool discovery, graceful degradation, source attribution), see `skills/connectors/SKILL.md`.

---

## Output Template (Korean)

See Step 5 for complete output structure. All user-facing text MUST be in Korean except:
- Regulation codes (FDA 510(k), EU MDR Annex IX, etc.)
- Technical abbreviations (PMA, CE, QMS, etc.)

---

## Traffic Light Definitions

- **🟢 GREEN**: Low-risk pathways (Class I/IIa, Grade 1-2, no clinical trials, no Notified Body for complex reviews)
- **🟡 YELLOW**: Moderate-high risk (Class IIb/III, Grade 3-4, De Novo, PMA, clinical trials required, Notified Body for Class IIb/III)
- **🔴 RED**: Not used in pathway skill (all valid classifications have a pathway)

---

## Escalation Scenarios

Escalate to regulatory expert when:
- FDA Class III device (PMA pathway)
- EU MDR Class III device (clinical investigation required)
- MFDS Grade 4 device (clinical trial required)
- De Novo pathway (no predicate device)
- Multi-region submission with conflicting timelines

---

## VALID Framework Compliance

- **Verified**: All pathway selections cite regulation sources (FDA Guidance, EU MDR Annex, MFDS regulations)
- **Accurate**: Timeline ranges match published regulatory data (2026-01)
- **Linked**: References to specific FDA/EU/MFDS regulation sections included
- **Inspectable**: Decision logic transparent (classification → pathway mapping clearly defined)
- **Deliverable**: Output stored in `.aria/products/<product-name>/<date>/pathway.md`

---

## Version History

**v1.0.0** (2026-02-11):
- Initial implementation for Phase 3
- FDA, EU MDR, MFDS pathway selection
- Multi-region comparison table
- Context Simplifier integration
- Korean language output
- Traffic light system
- VALID framework compliance

---

**Knowledge Base Cutoff**: 2026-01
**Next Update**: Quarterly regulatory updates
