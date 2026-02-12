---
name: aria-estimation
description: >
  Regulatory project cost and timeline estimation framework with three-point estimates.
  Provides optimistic/expected/pessimistic cost ranges and milestone-based timeline breakdowns.
allowed-tools: Read Grep Glob
user-invocable: false
metadata:
  version: "0.1.0"
  category: "domain"
  status: "active"
  updated: "2026-02-12"
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

## Purpose

Provide three-point cost and timeline estimates for regulatory submissions based on pathway selections. This is a pure analysis unit that receives pathway data and returns structured cost/timeline estimates.

**Input**: Pathway selection results (selected pathways per region, device class/grade)
**Output**: Cost breakdown (optimistic/expected/pessimistic), timeline with milestones, traffic light indicator
**Knowledge Base Date**: 2026-01

---

## Cost Estimation Framework

### Cost Categories

1. **Consulting Services**
   - Regulatory strategy consulting
   - Documentation review and guidance
   - Submission preparation support

2. **Testing & Validation**
   - Biocompatibility testing
   - Electrical safety testing
   - Performance testing
   - Sterilization validation (if applicable)
   - Software validation (if applicable)

3. **Regulatory Fees**
   - FDA user fees (510(k), PMA, De Novo)
   - MFDS application fees
   - Annual establishment fees

4. **Notified Body Fees** (EU only)
   - Initial assessment
   - QMS audit
   - Annual surveillance

5. **Clinical Study Costs** (if applicable)
   - IRB fees
   - Patient recruitment
   - Data collection and analysis
   - Clinical study report

---

## Three-Point Cost Estimation

### Class I Devices

| Region | Pathway | Optimistic | Expected | Pessimistic | Categories |
|--------|---------|------------|----------|-------------|------------|
| FDA | 510(k) Exempt | W5-10M | W10-20M | W20-30M | Consulting 40%, Testing 30%, Fees 30% |
| FDA | 510(k) Required | W15-25M | W25-40M | W40-60M | Consulting 35%, Testing 35%, Fees 30% |
| EU MDR | Self-Declaration | W8-15M | W15-25M | W25-40M | Consulting 45%, Testing 35%, Docs 20% |
| MFDS | Grade 1 Registration | W5-12M | W12-20M | W20-35M | Consulting 40%, Testing 35%, Fees 25% |

### Class II / IIa Devices

| Region | Pathway | Optimistic | Expected | Pessimistic | Categories |
|--------|---------|------------|----------|-------------|------------|
| FDA | 510(k) | W30-60M | W60-100M | W100-150M | Consulting 30%, Testing 40%, Fees 20%, Docs 10% |
| EU MDR | IIa NB | W40-80M | W80-130M | W130-200M | Consulting 25%, Testing 35%, NB 25%, Docs 15% |
| MFDS | Grade 2 Approval | W30-70M | W70-120M | W120-180M | Consulting 30%, Testing 45%, Fees 15%, Docs 10% |

### Class II / IIb Devices

| Region | Pathway | Optimistic | Expected | Pessimistic | Categories |
|--------|---------|------------|----------|-------------|------------|
| FDA | De Novo | W80-120M | W120-200M | W200-300M | Consulting 30%, Testing 35%, Special Controls 20%, Fees 15% |
| EU MDR | IIb NB | W70-120M | W120-180M | W180-280M | Consulting 25%, Testing 30%, NB 30%, PMCF 15% |

### Class III Devices

| Region | Pathway | Optimistic | Expected | Pessimistic | Categories |
|--------|---------|------------|----------|-------------|------------|
| FDA | PMA | W200-400M | W400-800M | W800-1,500M | Consulting 20%, Testing 25%, Clinical 40%, Fees 10%, QMS 5% |
| EU MDR | Class III CI | W180-350M | W350-700M | W700-1,200M | Consulting 20%, Testing 20%, Clinical 35%, NB 20%, QMS 5% |
| MFDS | Grade 4 CT | W150-300M | W300-600M | W600-1,000M | Consulting 20%, Testing 25%, Clinical 40%, Fees 10%, QMS 5% |

---

## Timeline Estimation Framework

### Milestone-Based Timeline

#### 510(k) Pathway (FDA Class II)

**Phase 1: Preparation**
- Duration: 1-2 months
- Deliverables: Predicate device identification, Gap analysis, Test protocol development

**Phase 2: Testing**
- Duration: 2-4 months
- Deliverables: Biocompatibility, Electrical safety, Performance testing

**Phase 3: Documentation**
- Duration: 1-2 months
- Deliverables: 510(k) submission package, Substantial equivalence report

**Phase 4: Submission & Review**
- Duration: 3-6 months (standard) or 1-3 months (expedited)
- Deliverables: FDA submission, Deficiency response (if any)

**Total Timeline**:
- Optimistic: 3-6 months
- Expected: 6-9 months
- Pessimistic: 9-12 months

#### PMA Pathway (FDA Class III)

**Phase 1: IDE Preparation**
- Duration: 2-4 months
- Deliverables: IDE application, IRB approval

**Phase 2: Clinical Study**
- Duration: 12-24 months
- Deliverables: Patient enrollment, Data collection, Clinical study report

**Phase 3: PMA Documentation**
- Duration: 3-6 months
- Deliverables: PMA submission package, Manufacturing QMS documentation

**Phase 4: FDA Review**
- Duration: 6-12 months
- Deliverables: FDA panel meeting, Deficiency responses, Approval

**Total Timeline**:
- Optimistic: 12-18 months
- Expected: 18-30 months
- Pessimistic: 30-48 months

#### EU MDR Class IIa (Notified Body)

**Phase 1: Preparation**
- Duration: 1-3 months
- Deliverables: Notified Body selection, Technical file structure

**Phase 2: Testing & CER**
- Duration: 3-6 months
- Deliverables: Testing, Clinical Evaluation Report, PMSP

**Phase 3: Notified Body Assessment**
- Duration: 2-4 months
- Deliverables: Technical file submission, QMS audit, Certificate

**Total Timeline**:
- Optimistic: 6-9 months
- Expected: 9-13 months
- Pessimistic: 13-18 months

#### MFDS Grade 2 (Approval)

**Phase 1: Preparation**
- Duration: 1-2 months
- Deliverables: Test protocol, Documentation plan

**Phase 2: Testing**
- Duration: 2-4 months
- Deliverables: Non-clinical testing, Performance validation

**Phase 3: Documentation**
- Duration: 1-2 months
- Deliverables: Approval application package

**Phase 4: MFDS Review**
- Duration: 2-4 months
- Deliverables: Application submission, Deficiency response

**Total Timeline**:
- Optimistic: 3-6 months
- Expected: 6-10 months
- Pessimistic: 10-14 months

---

## Analysis Workflow

### Step 1: Receive Pathway Data

Accept pathway selection results as input:
- Selected pathways per region
- Device class/grade per region
- Target regions

If pathway data is not provided, return an error indicating pathway analysis is required first.

### Step 2: Apply Cost Estimation Logic

**For each region**:
1. Identify pathway type (510(k), PMA, De Novo, CE Mark, Registration, Approval, etc.)
2. Determine device class/grade
3. Lookup cost ranges from framework above
4. Apply three-point estimate (optimistic, expected, pessimistic)
5. Break down by cost categories

**Multi-region scenarios**:
- Identify shared costs (common testing, consulting overlap)
- Calculate total cost range accounting for shared activities
- Highlight cost-saving opportunities from parallel submissions

### Step 3: Apply Timeline Estimation Logic

**For each region**:
1. Identify pathway milestones
2. Assign duration ranges to each phase
3. Calculate total timeline (optimistic/expected/pessimistic)

**Multi-region scenarios**:
- Identify critical path (longest timeline)
- Show parallel vs. sequential track options
- Highlight timeline dependencies

### Step 4: Assign Traffic Light

- **GREEN**: Total cost < W150M, timeline < 12 months
- **YELLOW**: Total cost W150-500M or timeline 12-24 months or clinical study required

### Step 5: Return Structured Result

Return the estimation result containing:
- Cost breakdown per region (optimistic/expected/pessimistic)
- Cost category analysis
- Timeline per region with milestones
- Multi-region cost-saving opportunities
- Critical path identification
- Traffic light assessment

---

## Traffic Light Definitions

- **GREEN**: Low cost/short timeline (< W150M, < 12 months)
- **YELLOW**: Moderate-high cost/long timeline (W150-500M, 12-24 months, clinical study)
- **RED**: Not used (all pathways have estimates)

---

## Escalation Scenarios

Highlight high uncertainty when:
- Clinical trials required (cost +/-50%, timeline +/-100%)
- Class III devices (PMA, EU MDR Class III, MFDS Grade 4)
- Novel device categories (De Novo pathway)
- Multi-region submissions with regulatory conflicts

---

## Data Source Strategy

1. **Built-in Knowledge** (Primary): Industry average costs and timelines (2026-01)
2. **Pathway Data** (Input): Pathway selection results from pathway skill
3. **MCP Connectors** (Supplementary): Organization-specific cost data and timeline benchmarks

For MCP integration patterns (tool discovery, graceful degradation, source attribution), see `CONNECTORS.md`.

**Note**: Cost ranges are based on Korean regulatory consulting industry averages as of 2026-01. Actual costs vary by project complexity, testing requirements, and market conditions.
