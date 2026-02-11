---
name: aria-planning
description: >
  Regulatory milestone planning with phase management, deliverables, and dependencies.
  Creates structured regulatory project plans based on pathway and estimation data.
allowed-tools: Read Grep Glob
user-invocable: false
metadata:
  version: "1.0.1"
  category: "domain"
  status: "active"
  updated: "2026-02-11"
  modularized: "false"
  tags: "planning, milestones, phases, dependencies, project-management"
  knowledge-base-date: "2026-01"

# MoAI Extension: Progressive Disclosure
progressive_disclosure:
  enabled: true
  level1_tokens: 100
  level2_tokens: 2000

# MoAI Extension: Triggers
triggers:
  keywords: ["plan", "milestone", "schedule", "roadmap", "project plan"]
  phases: ["run"]
---

# Regulatory Milestone Planning Skill

## Quick Reference

**Purpose**: Generate phase-based regulatory project plans with milestones, dependencies, and critical path analysis.

**Input**: Pathway and estimation results from `/aria:pathway` and `/aria:estimate`
**Output**: Milestone plan with phases, deliverables, dependencies, Gantt-style timeline, traffic light indicator
**Knowledge Base Date**: 2026-01

---

## Planning Framework

### Phase Structure

All regulatory plans follow a standard 4-6 phase structure:

1. **준비 단계 (Preparation)**
   - Gap analysis
   - Resource allocation
   - Strategy finalization

2. **시험 단계 (Testing & Validation)**
   - Biocompatibility testing
   - Performance testing
   - Electrical safety testing
   - Software validation (if applicable)

3. **문서화 단계 (Documentation)**
   - Technical file creation
   - Submission package assembly
   - Clinical evaluation report (if applicable)

4. **제출 및 심사 단계 (Submission & Review)**
   - Regulatory submission
   - Deficiency response
   - Approval/certification

5. **임상시험 단계 (Clinical Study)** (if applicable)
   - Protocol development
   - IRB approval
   - Patient enrollment
   - Data collection and analysis

6. **사후 관리 단계 (Post-Market)** (optional in initial plan)
   - Post-market surveillance setup
   - Vigilance system implementation

---

## Dependency Types

### Sequential Dependencies
- **Hard Dependency**: Task B cannot start until Task A completes
  - Example: "Documentation" depends on "Testing completion"
  - Notation: A → B

### Parallel Dependencies
- **Shared Resource**: Tasks can run in parallel but share common inputs
  - Example: FDA and EU submissions both depend on "Common Testing"
  - Notation: C ⇒ A, C ⇒ B

### Milestone Dependencies
- **Checkpoint**: Multiple tasks must complete before next phase begins
  - Example: All testing must finish before documentation starts
  - Notation: [A, B, C] ⟹ D

---

## Plan Templates by Pathway

| Pathway | Phase 1 | Phase 2 | Phase 3 | Phase 4 | Critical Path |
|---------|---------|---------|---------|---------|---------------|
| **510(k)** | 준비 (1-2mo): Predicate search, Gap analysis | 시험 (2-4mo): Biocomp, Electrical, Performance | 문서화 (1-2mo): 510(k) package, SE report | 심사 (3-6mo): Submission, Deficiency response | Phase 4 (FDA review) |
| **PMA** | IDE 준비 (2-4mo): IDE app, IRB approval | 임상시험 (12-24mo): Patient enrollment, Data collection | PMA 문서화 (3-6mo): PMA package, QMS docs | FDA 심사 (6-12mo): Panel meeting, Approval | Phase 2 (Clinical study) |
| **EU IIa** | 준비 (1-3mo): NB selection, Tech file structure | 시험/CER (3-6mo): Testing, CER, PMSP | 인증 심사 (2-4mo): NB audit, CE cert | - | Phase 2 (Testing/CER) |
| **MFDS G2** | 준비 (1-2mo): Protocol, Doc plan | 시험 (2-4mo): Non-clinical tests, Validation | 문서화 (1-2mo): Approval package | 심사 (2-4mo): MFDS submission | Phase 2 (Testing) |

---

## Multi-Region Planning

### Parallel Submission Strategy

When submitting to multiple regions simultaneously:

**Shared Phases** (run once, benefit all):
- Common Testing (biocompatibility, electrical safety, performance)
- Clinical data collection (if shared across regions)

**Region-Specific Phases** (run in parallel):
- FDA 510(k) documentation
- EU MDR technical file
- MFDS approval application

**Dependency Map**:
```
Common Testing → FDA Documentation → FDA Submission
              → EU Documentation → EU Submission
              → MFDS Documentation → MFDS Submission
```

**Critical Path**: Region with longest review time

---

### Sequential Submission Strategy

When staggering submissions (e.g., US first, then EU/Korea):

**Phase Order**:
1. Common Testing
2. FDA Submission → FDA Approval
3. EU Submission (using FDA approval data)
4. MFDS Submission (using FDA/EU data)

**Advantage**: Later submissions can reference earlier approvals
**Disadvantage**: Longer total timeline

---

## Workflow

### Step 1: Load Input Data

Load data from prior executions:
- **Pathway Data**: `.aria/products/<product-name>/<date>/pathway.summary.md`
- **Estimation Data**: `.aria/products/<product-name>/<date>/estimate.summary.md`

If either NOT available:
- Display warning: **"⚠️ 경로 및 비용 추정 데이터가 필요합니다. 먼저 `/aria:pathway` 및 `/aria:estimate` 명령을 실행하세요."**
- Traffic Light: 🟡 YELLOW
- STOP workflow

### Step 2: Select Plan Template

Based on loaded pathway data, select appropriate template:
- 510(k) → 4-phase plan
- PMA → 4-phase plan with clinical trial
- De Novo → 4-phase plan with special controls
- EU MDR IIa/IIb → 3-phase plan with Notified Body
- MFDS Grade 1-2 → 4-phase plan
- MFDS Grade 3-4 → 5-phase plan with clinical data/trial

### Step 3: Map Milestones to Timeline

Use timeline estimates from `/aria:estimate`:
- Assign duration to each phase (optimistic, expected, pessimistic)
- Calculate cumulative timeline
- Identify phase dependencies

### Step 4: Multi-Region Integration

If multiple target regions:
- Identify shared phases (common testing)
- Determine parallel vs. sequential strategy
- Map dependencies across regions
- Calculate critical path

### Step 5: Assign Traffic Light

- **🟢 GREEN**: Total timeline < 12 months, no clinical study, low complexity
- **🟡 YELLOW**: Timeline 12-24 months or clinical study required or multi-region complex dependencies

### Step 6: Generate Output

Output structure (Korean language):

```markdown
# 규제 프로젝트 실행 계획

## 제품 정보
- 제품명: [Product Name]
- 분석 일자: [YYYY-MM-DD]
- 대상 시장: [Target Markets]
- 예상 총 소요 기간: [Timeline]

## 프로젝트 개요

### 목표
- [Target regions and pathways]

### 전략
- [Parallel / Sequential submission strategy]

### 예상 일정
- 낙관적: [X]개월
- 예상: [Y]개월
- 비관적: [Z]개월

## 단계별 실행 계획

### Phase 1: 준비 단계 ([Duration])

**목표**: [Phase objective]

**주요 활동**:
1. [Activity 1]
2. [Activity 2]
3. [Activity 3]

**산출물 (Deliverables)**:
- [Deliverable 1]
- [Deliverable 2]
- [Deliverable 3]

**의존성 (Dependencies)**: [Dependencies or "없음"]

**비용 배분**: ₩[X]M ([%])

**담당 조직**: [Consulting / Internal / Testing Lab]

---

### Phase 2: 시험 단계 ([Duration])

**목표**: [Phase objective]

**주요 활동**:
1. [Activity 1]
2. [Activity 2]

**산출물 (Deliverables)**:
- [Deliverable 1]
- [Deliverable 2]

**의존성 (Dependencies)**: Phase 1 완료

**비용 배분**: ₩[X]M ([%])

**담당 조직**: [Testing labs, Validation teams]

---

[Repeat for all phases]

---

## 다중 시장 병렬 제출 계획

### 공통 단계 (Common Phases)
- **시험 (Testing)**: [Duration]
  - 모든 시장에서 공통 활용
  - 비용 절감 효과: [Amount or %]

### 지역별 병렬 단계

#### FDA (미국)
- **문서화**: [Duration]
- **제출 및 심사**: [Duration]
- **Total**: [Duration]

#### EU MDR (유럽)
- **문서화**: [Duration]
- **인증 기관 심사**: [Duration]
- **Total**: [Duration]

#### MFDS (한국)
- **문서화**: [Duration]
- **심사**: [Duration]
- **Total**: [Duration]

**최장 경로 (Critical Path)**: [Region] ([Duration])

---

## 의존성 맵 (Dependency Map)

```
Phase 1 (준비)
    ↓
Phase 2 (시험) ⟹ [FDA 문서화, EU 문서화, MFDS 문서화]
                       ↓              ↓               ↓
                 FDA 심사        EU 심사         MFDS 심사
```

**Critical Path Highlighted**: [Longest path description]

---

## 주요 마일스톤 (Key Milestones)

| Milestone | 예상 완료 시점 | 의존성 | 중요도 |
|-----------|----------------|--------|--------|
| 시험 완료 | [Date] | Phase 1 | ★★★ High |
| FDA 제출 | [Date] | 시험 완료 | ★★★ High |
| EU 제출 | [Date] | 시험 완료 | ★★ Medium |
| MFDS 제출 | [Date] | 시험 완료 | ★★ Medium |
| FDA 승인 | [Date] | FDA 제출 | ★★★ High |

---

## 위험 요소 및 완화 전략

### 주요 위험
1. **시험 지연**: [Mitigation strategy]
2. **인증 기관 대기 시간**: [Mitigation strategy]
3. **Deficiency 대응**: [Mitigation strategy]

### 비상 계획 (Contingency)
- 예비 시간: [Duration]
- 대체 인증 기관 확보 (EU)
- Deficiency 대응 전담 팀 구성

---

## 다음 단계

1. 내부 예산 승인 및 자원 배분
2. 컨설팅 업체 및 시험 기관 계약
3. 프로젝트 팀 구성 및 킥오프 미팅
4. 주간 진행 상황 모니터링 체계 수립

---

## 위험도 평가
- **Traffic Light**: [🟢 GREEN / 🟡 YELLOW]
- **평가**: [Risk assessment]

[If YELLOW]: **⚠️ 주의**: 이 프로젝트는 복잡도가 높으며, 일정 지연 위험이 있습니다. 정기적인 진행 상황 점검과 유연한 자원 배분이 필요합니다.

---

## 면책 조항
⚠️ **본 계획은 참고 자료이며, 확정 실행 계획이 아닙니다.** 실제 프로젝트 일정은 시험 결과, 규제 기관 요구사항, 자원 가용성, 외부 환경 변화 등에 따라 조정될 수 있습니다. 프로젝트 진행 중 정기적인 계획 재검토와 업데이트가 필요합니다.

---
**생성 일시**: [Timestamp]
**ARIA Plugin Version**: 2.0.0
```

### Step 7: Generate Context Simplifier Summary

Create `.summary.md` file for downstream use:

```markdown
# Planning Summary

**Product**: [Product Name]
**Date**: [YYYY-MM-DD]

## Timeline
- **Total Duration**: [X]개월 (expected)
- **Critical Path**: [Region / Phase]

## Phases
1. 준비: [Duration]
2. 시험: [Duration]
3. 문서화: [Duration]
4. 심사: [Duration]

## Key Milestones
- [Milestone 1]: [Date]
- [Milestone 2]: [Date]

## Traffic Light
- **Overall Risk**: [GREEN/YELLOW]

---
This summary completes the Phase 3 pipeline (pathway → estimate → plan).
```

---

## Data Source Strategy

1. **Built-in Knowledge** (Primary): Phase templates and dependency frameworks
2. **Loaded Pathway Data** (Input): `.summary.md` from `/aria:pathway`
3. **Loaded Estimation Data** (Input): `.summary.md` from `/aria:estimate`

---

## Output Template (Korean)

See Step 6 for complete output structure. All user-facing text MUST be in Korean except technical abbreviations (FDA, PMA, etc.).

---

## Traffic Light Definitions

- **🟢 GREEN**: Total timeline < 12 months, no clinical study, single or dual-market, low complexity
- **🟡 YELLOW**: Timeline 12-24 months, clinical study required, or multi-region with complex dependencies
- **🔴 RED**: Not used (all plans are feasible with appropriate resources)

---

## VALID Framework Compliance

- **Verified**: Plan templates based on regulatory consulting best practices (2026-01)
- **Accurate**: Timelines match estimation data from `/aria:estimate`
- **Linked**: References to pathway and estimation outputs
- **Inspectable**: Dependency map and phase structure transparent
- **Deliverable**: Output stored in `.aria/products/<product-name>/<date>/plan.md`

---

## Version History

**v1.0.0** (2026-02-11):
- Initial implementation for Phase 3
- Phase-based plan structure (4-6 phases)
- Dependency mapping (sequential, parallel, milestone)
- Multi-region parallel/sequential strategies
- Critical path identification
- Context Simplifier integration
- Korean language output
- Traffic light system
- VALID framework compliance

---

**Knowledge Base Cutoff**: 2026-01
**Next Update**: Quarterly updates based on regulatory project management trends
