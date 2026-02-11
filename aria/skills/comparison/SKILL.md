---
name: aria-comparison
description: >
  Multi-country regulatory comparison skill for FDA, EU MDR, and MFDS.
  Compares regulatory requirements across target regions and identifies key differences.
  Use for strategic multi-market planning and harmonization analysis.
allowed-tools: Read Grep Glob
user-invocable: false
metadata:
  version: "1.0.1"
  category: "domain"
  status: "active"
  updated: "2026-02-11"
  modularized: "false"
  tags: "comparison, multi-country, FDA, EU-MDR, MFDS, regulatory-analysis"
  knowledge-base-date: "2026-01"

# MoAI Extension: Progressive Disclosure
progressive_disclosure:
  enabled: true
  level1_tokens: 100
  level2_tokens: 2500

# MoAI Extension: Triggers
triggers:
  keywords: ["comparison", "compare", "multi-country", "regulatory difference", "harmonization"]
  phases: ["run"]
---

# Multi-Country Regulatory Comparison Skill

## Quick Reference

**Purpose**: Compare regulatory requirements across FDA (US), EU MDR (Europe), and MFDS (Korea) for specific regulatory topics or requirement areas.

**Input**: Regulatory topic or requirement area, target countries
**Output**: Side-by-side comparison matrix, key differences, harmonized standards, strategic recommendations
**Knowledge Base Date**: 2026-01

---

## Decision Framework

### Common Comparison Topics

#### Clinical Evidence Requirements
- **FDA**: Clinical data requirements per 21 CFR 860, IDE regulations for investigational devices
- **EU MDR**: Clinical evaluation per Annex XIV, clinical investigation per Article 62
- **MFDS**: 임상시험 계획 승인 (Clinical Trial Plan Approval), 임상적 성능시험 (Clinical Performance Testing)

#### Quality System Requirements
- **FDA**: 21 CFR Part 820 (Quality System Regulation)
- **EU MDR**: ISO 13485 + EU MDR Annex IX (QMS certification)
- **MFDS**: 의료기기 제조 및 품질관리 기준 (GMP for medical devices)

#### Post-Market Surveillance
- **FDA**: MDR (Medical Device Reporting), Post-approval studies
- **EU MDR**: PMCF (Post-Market Clinical Follow-up), PMS (Post-Market Surveillance)
- **MFDS**: 시판 후 조사 (Post-Market Surveillance), 부작용 보고 (Adverse Event Reporting)

#### Labeling and IFU Requirements
- **FDA**: 21 CFR Part 801 (Labeling requirements)
- **EU MDR**: Annex I Section 23 (Information supplied by manufacturer)
- **MFDS**: 의료기기 표시·기재 등에 관한 규정

#### Technical Documentation
- **FDA**: Design history file, Device master record
- **EU MDR**: Technical documentation per Annex II/III
- **MFDS**: 기술문서 (Technical File) per 의료기기법 시행규칙

#### Risk Management
- **FDA**: Risk analysis per FDA Guidance on risk management
- **EU MDR**: ISO 14971 compliance (harmonized standard)
- **MFDS**: ISO 14971 compliance + 위해성 평가 (Risk Assessment)

---

## Workflow

### Step 1: Load Prior Context (Optional)

Check for prior pipeline data:
- Classification results (`.aria/products/<product-name>/<date>/classification.summary.md`)
- Pathway selection (`.aria/products/<product-name>/<date>/pathway.summary.md`)
- Use prior context to inform comparison focus areas

If NO prior context: Proceed with user-specified comparison topic

### Step 2: Identify Comparison Topic

User provides either:
- Specific regulatory topic (e.g., "clinical evidence requirements", "post-market surveillance")
- Requirement area (e.g., "labeling", "quality system")
- Product-specific comparison (when prior context available)

Extract target countries from user input (default: FDA, EU MDR, MFDS)

### Step 3: Apply Comparison Framework

For each target country and topic:

**Comparison Dimensions**:
1. **Regulatory Basis**: Specific regulation/standard referenced
2. **Key Requirements**: Core mandatory elements
3. **Submission Timing**: When documentation is required (pre-market, post-market)
4. **Verification Method**: How compliance is verified (self-declaration, third-party audit, regulatory review)
5. **Penalties for Non-Compliance**: Enforcement consequences

**Comparison Matrix Structure**:

| Dimension | FDA | EU MDR | MFDS |
|-----------|-----|--------|------|
| Regulatory Basis | [Citation] | [Citation] | [Citation] |
| Key Requirements | [List] | [List] | [List] |
| Submission Timing | [When] | [When] | [When] |
| Verification | [Method] | [Method] | [Method] |

### Step 4: Identify Similarities and Differences

**Harmonized Areas** (similarities across regions):
- ISO 13485 (Quality Management)
- ISO 14971 (Risk Management)
- IEC 60601 series (Electrical safety for medical devices)
- IEC 62304 (Medical device software)
- IEC 62366 (Usability engineering)

**Key Differences**:
- Clinical evidence depth (EU MDR most stringent, FDA varies by class, MFDS moderate)
- Notified Body role (EU only)
- Post-market surveillance intensity (EU MDR PMCF most extensive)
- Language requirements (Korea requires Korean labeling)

### Step 5: Strategic Recommendations

Based on comparison results:

**Multi-Market Strategy Options**:
1. **Harmonized Approach**: Design documentation to meet the most stringent requirement (usually EU MDR), reducing regional adaptation
2. **Sequential Submission**: Target easiest market first (often FDA 510(k) or MFDS Grade 1-2), build precedent for other markets
3. **Parallel Submission**: Simultaneous multi-region submission when resources permit

**Cost-Benefit Analysis**:
- Harmonization upfront cost vs. later adaptation cost
- Translation and localization budget (especially for Korea)
- Notified Body fees (EU only)
- Clinical data reuse potential across regions

### Step 6: Assign Traffic Light

- **🟢 GREEN**: Requirements substantially aligned across regions, minimal adaptation needed
- **🟡 YELLOW**: Significant differences exist, expert consultation recommended for harmonization strategy
- **🔴 RED**: Conflicting requirements detected, fundamental approach change needed per region

### Step 7: Generate Output

Output structure (Korean language):

```markdown
# 다국가 규제 비교 분석 결과

## 비교 주제
- **주제**: [Comparison Topic]
- **대상 국가**: FDA (미국), EU MDR (유럽), MFDS (한국)
- **분석 일자**: [YYYY-MM-DD]

## 비교 매트릭스

### [Topic Area 1]

| 항목 | FDA | EU MDR | MFDS |
|------|-----|--------|------|
| 규제 근거 | [FDA Citation] | [EU Citation] | [MFDS Citation] |
| 핵심 요구사항 | - [Req 1]<br>- [Req 2] | - [Req 1]<br>- [Req 2] | - [Req 1]<br>- [Req 2] |
| 제출 시점 | [Timing] | [Timing] | [Timing] |
| 검증 방법 | [Method] | [Method] | [Method] |

**데이터 출처**: FDA [Citation], EU MDR [Citation], MFDS [Citation]

### [Topic Area 2]
[...동일한 구조 반복...]

## 공통 표준 (Harmonized Standards)
- **ISO 13485**: 의료기기 품질경영시스템 (FDA, EU, MFDS 모두 인정)
- **ISO 14971**: 의료기기 위해성 관리 (공통 적용)
- **IEC 60601 시리즈**: 전기 의료기기 안전성 (공통 표준)

## 주요 차이점
1. **임상 데이터 요구 수준**:
   - EU MDR: 가장 엄격 (Class IIa 이상 대부분 임상 데이터 요구)
   - FDA: 등급별 차등 (Class III는 PMA 임상 필수, Class II는 510(k) 실질적 동등성)
   - MFDS: 중간 수준 (Grade 3-4 임상/비임상 데이터)

2. **인증 기관 역할**:
   - EU MDR: Notified Body 필수 (Class IIa 이상)
   - FDA: 해당 없음 (FDA 직접 심사)
   - MFDS: 해당 없음 (MFDS 직접 심사)

3. **사후 관리 강도**:
   - EU MDR: PMCF 계획 및 보고서 필수
   - FDA: MDR 보고 + PAS (Post-Approval Study, Class III)
   - MFDS: 시판 후 조사 + 재심사 (일부 품목)

## 전략 권장사항
- **접근 방식**: [Harmonized / Sequential / Parallel]
- **근거**: [Rationale in Korean]
- **우선 시장**: [Recommended first market]
- **조화 가능성**: [Harmonization opportunities]

## 위험도 평가
- **Traffic Light**: [🟢 GREEN / 🟡 YELLOW / 🔴 RED]
- **평가**: [Risk assessment]

[If YELLOW or RED]: **⚠️ 전문가 검토 권장**: 규제 요구사항 차이가 크므로 다국가 전략 수립 시 규제 전문가 상담을 권장합니다.

## 다음 단계 제안
1. 가장 엄격한 요구사항(보통 EU MDR) 기준으로 문서 작성 고려
2. 번역/현지화 예산 계획 (특히 한국 라벨링)
3. 규제 전문가와 다국가 전략 검토

## 면책 조항
⚠️ **본 자료는 참고 정보이며, 규제 자문이 아닙니다.** 각국 규제는 지속적으로 업데이트되므로, 실제 제출 전 최신 규제 요구사항을 확인하시고 규제 전문가와 상담하시기 바랍니다.

---
**생성 일시**: [Timestamp]
**ARIA Plugin Version**: 2.0.0
```

### Step 8: Generate Context Simplifier Summary

Create `.summary.md` file for downstream pipeline:

```markdown
# Comparison Summary

**Topic**: [Comparison Topic]
**Date**: [YYYY-MM-DD]

- **Decision**: Multi-country comparison completed
- **Countries**: FDA, EU MDR, MFDS
- **Traffic Light**: [GREEN/YELLOW/RED]
- **Key Differences**: [Top 3 differences in bullet points]
- **Harmonized Standards**: ISO 13485, ISO 14971, IEC 60601
- **Recommended Strategy**: [Harmonized/Sequential/Parallel]
- **Escalation**: [Yes/No with reason if yes]
- **Sources**: FDA regulations, EU MDR text, MFDS 의료기기법

---
This summary is consumed by `/aria:brief` command.
```

---

## Data Source Strategy

1. **Built-in Knowledge** (Primary): Embedded regulatory comparison frameworks for FDA, EU MDR, MFDS
2. **Prior Pipeline Data** (Input): `.summary.md` files from classification/pathway steps (optional)
3. **External Tools** (Supplementary): Only when explicitly configured and available

---

## Traffic Light Definitions

- **🟢 GREEN**: Requirements substantially aligned, minimal adaptation needed
- **🟡 YELLOW**: Significant differences exist, harmonization strategy needed
- **🔴 RED**: Conflicting requirements, fundamental approach change required per region

---

## Escalation Scenarios

Escalate to regulatory expert when:
- Conflicting requirements across regions (RED traffic light)
- Significant cost impact from regional differences
- Novel device type with no clear precedent in any region
- Multi-market submission timing critical for business

---

## VALID Framework Compliance

- **Verified**: All comparisons cite specific regulation sources (FDA CFR, EU MDR Articles, MFDS 의료기기법)
- **Accurate**: Comparison data matches current regulatory state (2026-01)
- **Linked**: References to specific regulation sections included
- **Inspectable**: Decision logic transparent (comparison dimensions clearly defined)
- **Deliverable**: Output stored in `.aria/products/<product-name>/<date>/comparison.md`

---

## Common Comparison Topics (Examples)

### Clinical Evidence
- Pre-market clinical data requirements
- Clinical evaluation report standards
- Post-market clinical follow-up

### Quality System
- QMS certification requirements
- Design control processes
- Supplier management

### Post-Market Surveillance
- Adverse event reporting thresholds
- Periodic safety update requirements
- Field corrective actions

### Labeling
- IFU content requirements
- Symbol standards (ISO 15223)
- Language requirements

### Technical Documentation
- Design history file structure
- Risk management file
- Clinical evaluation documentation

---

## Version History

**v1.0.0** (2026-02-11):
- Initial implementation for Phase 4
- FDA, EU MDR, MFDS comparison framework
- Side-by-side matrix generation
- Strategic recommendations
- Context Simplifier integration
- Korean language output
- Traffic light system
- VALID framework compliance

---

**Knowledge Base Cutoff**: 2026-01
**Next Update**: Quarterly regulatory updates
