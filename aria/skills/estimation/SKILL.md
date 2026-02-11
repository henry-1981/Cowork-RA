---
name: aria-estimation
description: >
  Regulatory project cost and timeline estimation framework with three-point estimates.
  Provides optimistic/expected/pessimistic cost ranges and milestone-based timeline breakdowns.
allowed-tools: Read Grep Glob
user-invocable: false
metadata:
  version: "1.0.0"
  category: "domain"
  status: "active"
  updated: "2026-02-11"
  modularized: "false"
  tags: "estimation, cost, timeline, budget, three-point, milestones"
  knowledge-base-date: "2026-01"

# MoAI Extension: Progressive Disclosure
progressive_disclosure:
  enabled: true
  level1_tokens: 100
  level2_tokens: 2200

# MoAI Extension: Triggers
triggers:
  keywords: ["estimate", "cost", "timeline", "budget", "schedule"]
  phases: ["run"]
---

# Regulatory Cost & Timeline Estimation Skill

## Quick Reference

**Purpose**: Provide three-point cost and timeline estimates for regulatory submissions based on pathway selections.

**Input**: Pathway selection results from `/aria:pathway`
**Output**: Cost breakdown (optimistic/expected/pessimistic), timeline with milestones, traffic light indicator
**Knowledge Base Date**: 2026-01

---

## Cost Estimation Framework

### Cost Categories

1. **Consulting Services (컨설팅 비용)**
   - Regulatory strategy consulting
   - Documentation review and guidance
   - Submission preparation support

2. **Testing & Validation (시험 비용)**
   - Biocompatibility testing
   - Electrical safety testing
   - Performance testing
   - Sterilization validation (if applicable)
   - Software validation (if applicable)

3. **Regulatory Fees (규제 수수료)**
   - FDA user fees (510(k), PMA, De Novo)
   - MFDS application fees
   - Annual establishment fees

4. **Notified Body Fees (인증 기관 비용)** (EU only)
   - Initial assessment
   - QMS audit
   - Annual surveillance

5. **Clinical Study Costs (임상시험 비용)** (if applicable)
   - IRB fees
   - Patient recruitment
   - Data collection and analysis
   - Clinical study report

---

## Three-Point Cost Estimation

### Class I Devices

| Region | Pathway | Optimistic | Expected | Pessimistic | Categories |
|--------|---------|------------|----------|-------------|------------|
| FDA | 510(k) Exempt | ₩5-10M | ₩10-20M | ₩20-30M | Consulting 40%, Testing 30%, Fees 30% |
| FDA | 510(k) Required | ₩15-25M | ₩25-40M | ₩40-60M | Consulting 35%, Testing 35%, Fees 30% |
| EU MDR | Self-Declaration | ₩8-15M | ₩15-25M | ₩25-40M | Consulting 45%, Testing 35%, Docs 20% |
| MFDS | Grade 1 신고 | ₩5-12M | ₩12-20M | ₩20-35M | Consulting 40%, Testing 35%, Fees 25% |

### Class II / IIa Devices

| Region | Pathway | Optimistic | Expected | Pessimistic | Categories |
|--------|---------|------------|----------|-------------|------------|
| FDA | 510(k) | ₩30-60M | ₩60-100M | ₩100-150M | Consulting 30%, Testing 40%, Fees 20%, Docs 10% |
| EU MDR | IIa NB | ₩40-80M | ₩80-130M | ₩130-200M | Consulting 25%, Testing 35%, NB 25%, Docs 15% |
| MFDS | Grade 2 허가 | ₩30-70M | ₩70-120M | ₩120-180M | Consulting 30%, Testing 45%, Fees 15%, Docs 10% |

### Class II / IIb Devices

| Region | Pathway | Optimistic | Expected | Pessimistic | Categories |
|--------|---------|------------|----------|-------------|------------|
| FDA | De Novo | ₩80-120M | ₩120-200M | ₩200-300M | Consulting 30%, Testing 35%, Special Controls 20%, Fees 15% |
| EU MDR | IIb NB | ₩70-120M | ₩120-180M | ₩180-280M | Consulting 25%, Testing 30%, NB 30%, PMCF 15% |

### Class III Devices

| Region | Pathway | Optimistic | Expected | Pessimistic | Categories |
|--------|---------|------------|----------|-------------|------------|
| FDA | PMA | ₩200-400M | ₩400-800M | ₩800-1,500M | Consulting 20%, Testing 25%, Clinical 40%, Fees 10%, QMS 5% |
| EU MDR | Class III CI | ₩180-350M | ₩350-700M | ₩700-1,200M | Consulting 20%, Testing 20%, Clinical 35%, NB 20%, QMS 5% |
| MFDS | Grade 4 CT | ₩150-300M | ₩300-600M | ₩600-1,000M | Consulting 20%, Testing 25%, Clinical 40%, Fees 10%, QMS 5% |

---

## Timeline Estimation Framework

### Milestone-Based Timeline

#### 510(k) Pathway (FDA Class II)

**Phase 1: Preparation (준비)**
- Duration: 1-2개월
- Deliverables: Predicate device identification, Gap analysis, Test protocol development

**Phase 2: Testing (시험)**
- Duration: 2-4개월
- Deliverables: Biocompatibility, Electrical safety, Performance testing

**Phase 3: Documentation (문서화)**
- Duration: 1-2개월
- Deliverables: 510(k) submission package, Substantial equivalence report

**Phase 4: Submission & Review (제출 및 심사)**
- Duration: 3-6개월 (standard) or 1-3개월 (expedited)
- Deliverables: FDA submission, Deficiency response (if any)

**Total Timeline**:
- Optimistic: 3-6개월
- Expected: 6-9개월
- Pessimistic: 9-12개월

#### PMA Pathway (FDA Class III)

**Phase 1: IDE Preparation**
- Duration: 2-4개월
- Deliverables: IDE application, IRB approval

**Phase 2: Clinical Study**
- Duration: 12-24개월
- Deliverables: Patient enrollment, Data collection, Clinical study report

**Phase 3: PMA Documentation**
- Duration: 3-6개월
- Deliverables: PMA submission package, Manufacturing QMS documentation

**Phase 4: FDA Review**
- Duration: 6-12개월
- Deliverables: FDA panel meeting, Deficiency responses, Approval

**Total Timeline**:
- Optimistic: 12-18개월
- Expected: 18-30개월
- Pessimistic: 30-48개월

#### EU MDR Class IIa (Notified Body)

**Phase 1: Preparation**
- Duration: 1-3개월
- Deliverables: Notified Body selection, Technical file structure

**Phase 2: Testing & CER**
- Duration: 3-6개월
- Deliverables: Testing, Clinical Evaluation Report, PMSP

**Phase 3: Notified Body Assessment**
- Duration: 2-4개월
- Deliverables: Technical file submission, QMS audit, Certificate

**Total Timeline**:
- Optimistic: 6-9개월
- Expected: 9-13개월
- Pessimistic: 13-18개월

#### MFDS Grade 2 (허가)

**Phase 1: Preparation**
- Duration: 1-2개월
- Deliverables: Test protocol, Documentation plan

**Phase 2: Testing**
- Duration: 2-4개월
- Deliverables: Non-clinical testing, Performance validation

**Phase 3: Documentation**
- Duration: 1-2개월
- Deliverables: Approval application package

**Phase 4: MFDS Review**
- Duration: 2-4개월
- Deliverables: Application submission, Deficiency response

**Total Timeline**:
- Optimistic: 3-6개월
- Expected: 6-10개월
- Pessimistic: 10-14개월

---

## Workflow

### Step 1: Load Pathway Data

Use pathway results from prior `/aria:pathway` execution:
- Check for `.aria/products/<product-name>/<date>/pathway.summary.md`
- Extract selected pathways for each target region
- If pathway data NOT available:
  - Display warning: **"⚠️ 경로 선택 데이터가 필요합니다. 먼저 `/aria:pathway` 명령을 실행하세요."**
  - Traffic Light: 🟡 YELLOW
  - STOP workflow

### Step 2: Apply Cost Estimation Logic

Based on loaded pathway data:

**For each region**:
1. Identify pathway type (510(k), PMA, De Novo, CE Mark, 신고, 허가, etc.)
2. Determine device class/grade
3. Lookup cost ranges from framework above
4. Apply three-point estimate (optimistic, expected, pessimistic)
5. Break down by cost categories

**Multi-region scenarios**:
- Identify shared costs (common testing, consulting overlap)
- Calculate total cost range accounting for shared activities
- Highlight cost-saving opportunities from parallel submissions

### Step 3: Apply Timeline Estimation Logic

Based on loaded pathway data:

**For each region**:
1. Identify pathway milestones
2. Assign duration ranges to each phase
3. Calculate total timeline (optimistic/expected/pessimistic)

**Multi-region scenarios**:
- Identify critical path (longest timeline)
- Show parallel vs. sequential track options
- Highlight timeline dependencies

### Step 4: Assign Traffic Light

- **🟢 GREEN**: Total cost < ₩150M, timeline < 12 months
- **🟡 YELLOW**: Total cost ₩150-500M or timeline 12-24 months or clinical study required
- **🔴 RED**: Not used (all pathways have estimates)

### Step 5: Generate Output

Output structure (Korean language):

```markdown
# 비용 및 일정 추정 결과

## 제품 정보
- 제품명: [Product Name]
- 분석 일자: [YYYY-MM-DD]
- 대상 시장: [Target Markets]

## 비용 추정

### 총 비용 범위

| 시나리오 | 비용 범위 (₩) |
|---------|--------------|
| 낙관적 (Optimistic) | [X]-[Y]M |
| 예상 (Expected) | [Y]-[Z]M |
| 비관적 (Pessimistic) | [Z]-[W]M |

### 비용 카테고리 분석

#### FDA (미국)
- **컨설팅**: [X]%
- **시험**: [Y]%
- **규제 수수료**: [Z]%
- **임상시험** (해당시): [W]%

**비용 범위**:
- 낙관적: ₩[X]M
- 예상: ₩[Y]M
- 비관적: ₩[Z]M

#### EU MDR (유럽)
- **컨설팅**: [X]%
- **시험**: [Y]%
- **인증 기관**: [Z]%
- **문서화**: [W]%

**비용 범위**:
- 낙관적: ₩[X]M
- 예상: ₩[Y]M
- 비관적: ₩[Z]M

#### MFDS (한국)
- **컨설팅**: [X]%
- **시험**: [Y]%
- **규제 수수료**: [Z]%
- **문서화**: [W]%

**비용 범위**:
- 낙관적: ₩[X]M
- 예상: ₩[Y]M
- 비관적: ₩[Z]M

### 다중 시장 비용 절감 기회
- **공통 시험 활용**: [Shared testing activities]
- **컨설팅 통합**: [Consulting overlap]
- **병렬 제출 이점**: [Parallel submission benefits]

## 일정 추정

### 총 소요 기간

| 시나리오 | 기간 |
|---------|------|
| 낙관적 | [X]-[Y]개월 |
| 예상 | [Y]-[Z]개월 |
| 비관적 | [Z]-[W]개월 |

### 주요 마일스톤

#### FDA (미국) - [Pathway Name]
1. **준비 단계**: [X-Y]개월
   - Deliverables: [...]
2. **시험 단계**: [Y-Z]개월
   - Deliverables: [...]
3. **문서화**: [Z-W]개월
   - Deliverables: [...]
4. **심사**: [W-V]개월
   - Deliverables: [...]

**총 소요 기간**: [X-Y]개월 (낙관), [Y-Z]개월 (예상), [Z-W]개월 (비관)

#### EU MDR (유럽) - [Pathway Name]
[Similar milestone breakdown]

#### MFDS (한국) - [Pathway Name]
[Similar milestone breakdown]

### 최장 경로 (Critical Path)
- **지역**: [Region]
- **예상 소요 기간**: [Duration]
- **주요 병목 구간**: [Bottleneck phase]

## 위험도 평가
- **Traffic Light**: [🟢 GREEN / 🟡 YELLOW]
- **평가**: [Risk assessment]

[If YELLOW]: **⚠️ 주의**: 이 추정치는 불확실성이 높습니다. 임상시험 소요 기간, 심사 기간, 인증 기관 대기 시간 등은 변동 가능성이 큽니다.

## 비용 절감 전략
1. [Cost-saving strategy 1]
2. [Cost-saving strategy 2]
3. [Cost-saving strategy 3]

## 다음 단계 제안
1. `/aria:plan` 명령으로 세부 실행 계획 수립
2. 예산 확보 및 내부 승인 절차 진행
3. 컨설팅 업체 및 시험 기관 견적 요청

## 면책 조항
⚠️ **본 자료는 참고 정보이며, 확정 견적이 아닙니다.** 실제 비용과 일정은 제품 복잡도, 시험 결과, 규제 기관 요구사항, 시장 상황 등에 따라 크게 달라질 수 있습니다. 특히 Class III 의료기기의 경우 임상시험 비용과 기간의 불확실성이 매우 높습니다. 실제 프로젝트 진행 전 전문 컨설팅 업체와 상세 견적을 받으시기 바랍니다.

---
**생성 일시**: [Timestamp]
**ARIA Plugin Version**: 2.0.0
**데이터 출처**: 규제 컨설팅 업계 평균 비용 (2026-01 기준)
```

### Step 6: Generate Context Simplifier Summary

Create `.summary.md` file for downstream pipeline:

```markdown
# Estimation Summary

**Product**: [Product Name]
**Date**: [YYYY-MM-DD]

## Cost Ranges
- **Optimistic**: ₩[X]M
- **Expected**: ₩[Y]M
- **Pessimistic**: ₩[Z]M

## Timeline Ranges
- **Optimistic**: [X]개월
- **Expected**: [Y]개월
- **Pessimistic**: [Z]개월

## Critical Path
- **Region**: [Region]
- **Duration**: [Duration]

## Traffic Light
- **Overall Risk**: [GREEN/YELLOW]

---
This summary is consumed by `/aria:plan` command.
```

---

## Data Source Strategy

1. **Built-in Knowledge** (Primary): Industry average costs and timelines (2026-01)
2. **Loaded Pathway Data** (Input): `.summary.md` from `/aria:pathway`
3. **External Tools** (Supplementary): Only when explicitly configured

**Note**: Cost ranges are based on Korean regulatory consulting industry averages as of 2026-01. Actual costs vary by project complexity, testing requirements, and market conditions.

---

## Output Template (Korean)

See Step 5 for complete output structure. All user-facing text MUST be in Korean except:
- Currency symbols (₩)
- Technical abbreviations (FDA, PMA, QMS, etc.)

---

## Traffic Light Definitions

- **🟢 GREEN**: Low cost/short timeline (< ₩150M, < 12 months)
- **🟡 YELLOW**: Moderate-high cost/long timeline (₩150-500M, 12-24 months, clinical study)
- **🔴 RED**: Not used (all pathways have estimates)

---

## Escalation Scenarios

Highlight high uncertainty when:
- Clinical trials required (cost ±50%, timeline ±100%)
- Class III devices (PMA, EU MDR Class III, MFDS Grade 4)
- Novel device categories (De Novo pathway)
- Multi-region submissions with regulatory conflicts

---

## VALID Framework Compliance

- **Verified**: Cost ranges cite industry average data sources (2026-01)
- **Accurate**: Estimates reflect current regulatory timelines and consulting rates
- **Linked**: References to pathway types from `/aria:pathway`
- **Inspectable**: Breakdown by cost categories and timeline phases transparent
- **Deliverable**: Output stored in `.aria/products/<product-name>/<date>/estimate.md`

---

## Version History

**v1.0.0** (2026-02-11):
- Initial implementation for Phase 3
- Three-point cost estimation (optimistic/expected/pessimistic)
- Milestone-based timeline framework
- Multi-region cost breakdown
- Context Simplifier integration
- Korean language output
- Traffic light system
- VALID framework compliance

---

**Knowledge Base Cutoff**: 2026-01
**Next Update**: Quarterly cost/timeline updates based on industry trends
