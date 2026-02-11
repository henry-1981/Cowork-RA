# Test Scenarios for SPEC-ARIA-001 Phase 3

**SPEC**: SPEC-ARIA-001 v4.0.0
**Scope**: Phase 3 acceptance criteria validation (Pathway Skills + Commands)
**Status**: Test scenarios documented
**Coverage Target**: 85%+ of Phase 3 requirements

---

## Executive Summary

This document defines comprehensive test scenarios for ARIA Cowork Plugin Phase 3, covering:
- **Pathway Skill**: Regulatory submission pathway selection for FDA/EU MDR/MFDS
- **Estimation Skill**: Cost and timeline estimation with optimistic/expected/pessimistic ranges
- **Planning Skill**: Regulatory milestone planning with dependency mapping
- **Commands**: /aria:pathway, /aria:estimate, /aria:plan

Test design follows TDD methodology with 85%+ coverage target for all Phase 3 acceptance criteria.

---

## Test Strategy

### Test Categories

1. **Positive Tests** (60%): Expected behavior validation
2. **Negative Tests** (20%): Error handling and edge cases
3. **Integration Tests** (15%): Command-to-skill-to-output workflow
4. **Pipeline Tests** (5%): Context Simplifier data flow from Phase 2

### Coverage Mapping

All test scenarios map to acceptance criteria in `acceptance.md`:
- **Event-Driven Requirements**: ER-004 (pathway), ER-005 (estimate), ER-006 (plan)
- **Ubiquitous Requirements**: UR-001 (Korean), UR-002 (disclaimer), UR-003 (data source), UR-004 (VALID), UR-005 (traffic light), UR-006 (storage path)
- **State-Driven Requirements**: SR-001 (degradation), SR-007 (versioning)
- **Unwanted Behaviors**: WR-001 through WR-005

---

## Phase 3: Pathway Skill Test Scenarios

### PW-001: FDA Pathway Selection
**Requirement**: ER-004 - Identify correct FDA submission pathway
**Priority**: Critical

**Test Cases**:

**PW-001.1**: Class I device with 510(k) exemption
```gherkin
Given a Class I device with confirmed 510(k) exemption status
When /aria:pathway is executed with classification results
Then the FDA pathway shall be "Exempt (510(k))"
And the output shall include required registration steps
And the traffic light shall be GREEN
And the timeline range shall be "1-2 months"
```

**PW-001.2**: Class II device requiring 510(k)
```gherkin
Given a Class II device classified as non-exempt
When /aria:pathway is executed
Then the FDA pathway shall be "510(k) Premarket Notification"
And the output shall include predicate device search requirement
And the timeline range shall be "3-6 months (standard) or 1-3 months (expedited)"
And key requirements shall list substantial equivalence demonstration
```

**PW-001.3**: Class III device requiring PMA
```gherkin
Given a Class III device classification
When /aria:pathway is executed
Then the FDA pathway shall be "PMA (Premarket Approval)"
And the output shall include clinical study requirement
And the timeline range shall be "12-18+ months"
And the traffic light shall be YELLOW with escalation to regulatory expert
```

**PW-001.4**: De Novo pathway for novel low/moderate risk device
```gherkin
Given a Class II device with no valid predicate
And the device poses low to moderate risk
When /aria:pathway is executed
Then the FDA pathway shall be "De Novo Classification Request"
And the output shall include special controls requirement
And the timeline range shall be "6-12 months"
```

---

### PW-002: EU MDR Pathway Selection
**Requirement**: ER-004 - Identify correct EU MDR CE marking route
**Priority**: Critical

**Test Cases**:

**PW-002.1**: Class I non-sterile, non-measuring device
```gherkin
Given a Class I device (non-sterile, non-measuring function)
When /aria:pathway is executed
Then the EU pathway shall be "Self-declaration (Annex IV)"
And the output shall indicate no Notified Body required
And the timeline range shall be "2-4 months"
And the traffic light shall be GREEN
```

**PW-002.2**: Class IIa/IIb device requiring Notified Body
```gherkin
Given a Class IIa or IIb device
When /aria:pathway is executed
Then the EU pathway shall be "Notified Body Certification (Annex IX or X)"
And the output shall include Technical Documentation requirement
And the output shall include Clinical Evaluation Report requirement
And the timeline range shall be "6-12 months"
```

**PW-002.3**: Class III device requiring full Notified Body approval
```gherkin
Given a Class III device
When /aria:pathway is executed
Then the EU pathway shall be "Notified Body Full QMS Certification (Annex IX)"
And the output shall include clinical investigation requirement
And the timeline range shall be "12-18+ months"
And the traffic light shall be YELLOW
```

---

### PW-003: MFDS Pathway Selection
**Requirement**: ER-004 - Identify correct MFDS certification route
**Priority**: Critical

**Test Cases**:

**PW-003.1**: Class I device (Grade 1)
```gherkin
Given a MFDS Grade 1 device (Class I equivalent)
When /aria:pathway is executed
Then the MFDS pathway shall be "Product Registration (신고)"
And the output shall indicate no clinical data required
And the timeline range shall be "1-3 months"
And the traffic light shall be GREEN
```

**PW-003.2**: Class II/III device (Grade 2-4) requiring approval
```gherkin
Given a MFDS Grade 2, 3, or 4 device
When /aria:pathway is executed
Then the MFDS pathway shall be "Product Approval (허가)"
And the output shall include clinical/non-clinical data requirement
And the timeline range shall be "3-9 months (Grade 2) or 9-15+ months (Grade 3-4)"
```

**PW-003.3**: Class IV highest risk device
```gherkin
Given a MFDS Grade 4 device (highest risk)
When /aria:pathway is executed
Then the MFDS pathway shall be "Product Approval with Clinical Trial (허가 with 임상시험)"
And the output shall include mandatory clinical trial requirement
And the timeline range shall be "12-18+ months"
And the traffic light shall be YELLOW
```

---

### PW-004: Multi-Region Pathway Comparison
**Requirement**: ER-004 - Produce comparison table for multi-market scenarios
**Priority**: High

**Test Cases**:

**PW-004.1**: Class II device targeting US + EU + Korea
```gherkin
Given a Class II device (FDA), Class IIa (EU MDR), Grade 2 (MFDS)
When /aria:pathway is executed for all three markets
Then the output shall include a comparison table with columns: Region, Pathway, Timeline, Key Requirements
And the FDA row shall show "510(k), 3-6 months, Predicate device"
And the EU row shall show "Notified Body Annex IX/X, 6-12 months, Technical Documentation + CER"
And the MFDS row shall show "허가, 3-9 months, Non-clinical data"
And the critical path shall be identified (longest timeline highlighted)
```

**PW-004.2**: Class I device across all regions (fastest pathway)
```gherkin
Given a Class I exempt (FDA), Class I non-sterile (EU), Grade 1 (MFDS)
When /aria:pathway is executed
Then all three pathways shall be GREEN traffic light
And the combined timeline estimate shall be "2-4 months"
And the output shall recommend parallel submission strategy
```

**PW-004.3**: High-risk Class III device across all regions
```gherkin
Given a Class III (FDA), Class III (EU), Grade 4 (MFDS)
When /aria:pathway is executed
Then all three pathways shall be YELLOW traffic light
And the combined timeline shall exceed 12 months for all regions
And the output shall include mandatory escalation recommendation
And the disclaimer shall emphasize clinical study complexity
```

---

### PW-005: Context Simplifier Integration
**Requirement**: Phase 3 Success Criterion - Pipeline data flow from Phase 2
**Priority**: High

**Test Cases**:

**PW-005.1**: Load classification summary from prior step
```gherkin
Given /aria:classify has been executed previously
And the classification output includes .summary.md file
When /aria:pathway is invoked
Then the skill shall load classification results from .summary.md
And shall NOT re-ask for device class information
And the pathway selection shall use the loaded classification data
```

**PW-005.2**: Pathway skill without prior classification data
```gherkin
Given NO prior classification data exists in .aria/products/
When /aria:pathway is executed
Then the skill shall display a warning in Korean: "분류 데이터가 없습니다"
And shall request the user to run /aria:classify first
And the traffic light shall be YELLOW
```

**PW-005.3**: Generate .summary.md for downstream use
```gherkin
Given /aria:pathway executes successfully
When the output is generated
Then a .summary.md file shall be created in the product directory
And the file shall include pathway selections for all target regions
And the file shall be readable by /aria:estimate and /aria:plan
```

---

### PW-006: Traffic Light System
**Requirement**: UR-005 - Traffic light system for regulatory risk
**Priority**: High

**Test Cases**:

**PW-006.1**: GREEN - Low risk pathways
```gherkin
Given a Class I exempt device across all regions
When /aria:pathway is executed
Then the traffic light shall be GREEN
And the output shall include "낮은 위험도" indicator
And no escalation recommendation shall appear
```

**PW-006.2**: YELLOW - Moderate risk or complex pathways
```gherkin
Given a Class II/IIa device with Notified Body requirement
When /aria:pathway is executed
Then the traffic light shall be YELLOW
And the output shall include "전문가 검토 권장" recommendation
```

**PW-006.3**: RED - Not applicable (pathway skill does not use RED)
```gherkin
Given any valid device classification
When /aria:pathway is executed
Then the traffic light shall NEVER be RED
And only GREEN or YELLOW indicators shall be used
```

---

### PW-007: Korean Language Output
**Requirement**: UR-001 - All user-facing output in Korean
**Priority**: Critical

**Test Cases**:

**PW-007.1**: All pathway descriptions in Korean
```gherkin
Given any pathway selection scenario
When the output is generated
Then all pathway names shall be in Korean (e.g., "사전 통지 (510(k))")
And all requirement descriptions shall be in Korean
And no English text shall appear except regulation codes (e.g., "FDA 510(k)")
```

**PW-007.2**: Timeline descriptions in Korean
```gherkin
Given timeline ranges are displayed
When the output is generated
Then timeline units shall be in Korean: "개월" (months), "년" (years)
And timeline descriptions shall use Korean phrases (e.g., "예상 소요 기간")
```

---

### PW-008: Disclaimer and Data Source Attribution
**Requirement**: UR-002, UR-003 - Disclaimer and data source citation
**Priority**: High

**Test Cases**:

**PW-008.1**: Standard disclaimer present
```gherkin
Given any /aria:pathway execution
When the output is generated
Then the standard disclaimer shall appear: "본 자료는 참고 정보이며, 규제 자문이 아닙니다"
```

**PW-008.2**: Data source attribution for pathway decisions
```gherkin
Given pathway recommendations are provided
When the output cites regulatory requirements
Then each requirement shall cite its source (e.g., "출처: FDA 510(k) Guidance", "출처: EU MDR Annex IX")
And no unsupported claims shall appear
```

---

### PW-009: VALID Framework Compliance
**Requirement**: UR-004 - VALID framework enforcement
**Priority**: High

**Test Cases**:

**PW-009.1**: Pathway output meets VALID checklist
```gherkin
Given /aria:pathway produces output
When the VALID checklist is applied
Then V (Verified): Data sources shall be cited
And A (Accurate): Pathway timelines shall match known regulatory ranges
And L (Linked): References to FDA/EU MDR/MFDS regulations shall be included
And I (Inspectable): Decision logic shall be transparent
And D (Deliverable): Output shall be stored in .aria/products/ with proper naming
```

---

### PW-010: Storage Path Convention
**Requirement**: UR-006 - Data storage path convention
**Priority**: Medium

**Test Cases**:

**PW-010.1**: Pathway output stored in correct directory
```gherkin
Given a product named "Cardiac Monitor X1"
And the command is executed on 2026-02-11
When /aria:pathway generates output
Then the output file shall be stored at:
  .aria/products/cardiac-monitor-x1/2026-02-11/pathway.md
And the .summary.md file shall be at:
  .aria/products/cardiac-monitor-x1/2026-02-11/pathway.summary.md
```

---

## Phase 3: Estimation Skill Test Scenarios

### ES-001: Cost Estimation with Three-Point Ranges
**Requirement**: ER-005 - Cost breakdown with optimistic/expected/pessimistic ranges
**Priority**: Critical

**Test Cases**:

**ES-001.1**: Class I device cost estimation
```gherkin
Given a Class I exempt device pathway
When /aria:estimate is executed
Then the cost breakdown shall include categories: Consulting, Testing, Regulatory Fees, Notified Body (if applicable)
And each category shall show three ranges: Optimistic, Expected, Pessimistic
And the total cost range for Class I shall be "₩5-15M (optimistic), ₩15-30M (expected), ₩30-50M (pessimistic)"
```

**ES-001.2**: Class II/IIa device cost estimation
```gherkin
Given a Class II (FDA) or IIa (EU) pathway
When /aria:estimate is executed
Then the cost breakdown shall reflect higher testing and documentation costs
And the total cost range shall be "₩30-80M (optimistic), ₩80-150M (expected), ₩150-250M (pessimistic)"
```

**ES-001.3**: Class III high-risk device cost estimation
```gherkin
Given a Class III device with PMA/clinical trial requirement
When /aria:estimate is executed
Then the cost breakdown shall include clinical study costs
And the total cost range shall exceed ₩200M
And the disclaimer shall emphasize high uncertainty in Class III estimates
```

---

### ES-002: Timeline Estimation with Milestones
**Requirement**: ER-005 - Timeline with milestones
**Priority**: Critical

**Test Cases**:

**ES-002.1**: Timeline breakdown for 510(k) pathway
```gherkin
Given a 510(k) pathway selection
When /aria:estimate is executed
Then the timeline shall include milestones:
  - Predicate device search: 1-2 months
  - Testing and documentation: 2-3 months
  - FDA review: 3-6 months (standard) or 1-3 months (expedited)
And the total timeline range shall be "3-6 months (optimistic), 6-9 months (expected), 9-12 months (pessimistic)"
```

**ES-002.2**: Timeline for multi-region submission
```gherkin
Given pathways for US + EU + Korea
When /aria:estimate is executed
Then the timeline shall show parallel tracks for each region
And the critical path shall be identified (longest timeline)
And the overall project timeline shall account for sequential dependencies
```

---

### ES-003: Context Simplifier Integration
**Requirement**: Phase 3 Success Criterion - Load pathway data
**Priority**: High

**Test Cases**:

**ES-003.1**: Load pathway summary from prior step
```gherkin
Given /aria:pathway has been executed previously
And the pathway output includes .summary.md file
When /aria:estimate is invoked
Then the skill shall load pathway data from .summary.md
And shall NOT re-ask for pathway selection
And cost/timeline estimates shall match the loaded pathway types
```

---

## Phase 3: Planning Skill Test Scenarios

### PL-001: Milestone Plan Generation
**Requirement**: ER-006 - Generate milestone plan with phases
**Priority**: Critical

**Test Cases**:

**PL-001.1**: Single-market milestone plan (FDA 510(k))
```gherkin
Given a 510(k) pathway with cost/timeline estimates
When /aria:plan is executed
Then the plan shall include phases:
  - Phase 1: Preparation (predicate search, gap analysis)
  - Phase 2: Testing (bench, biocompatibility, electrical safety)
  - Phase 3: Documentation (510(k) submission package)
  - Phase 4: Submission and Review
And each phase shall list deliverables, duration, and dependencies
```

**PL-001.2**: Multi-market parallel submission plan
```gherkin
Given pathways for US + EU + Korea
When /aria:plan is executed
Then the plan shall show parallel tracks per market
And common dependencies shall be highlighted (e.g., shared testing data)
And the critical path shall be identified with visual indicator
```

---

### PL-002: Dependency Mapping
**Requirement**: ER-006 - Include dependencies and checkpoints
**Priority**: High

**Test Cases**:

**PL-002.1**: Sequential dependencies within a phase
```gherkin
Given a PMA pathway plan
When the plan is generated
Then Phase 2 (Clinical Study) shall be marked as dependent on Phase 1 (IDE approval)
And Phase 3 (PMA Submission) shall depend on Phase 2 completion
And dependency arrows shall be shown in the plan diagram
```

**PL-002.2**: Parallel tasks with shared dependencies
```gherkin
Given a multi-market plan
When common testing is required across all regions
Then the plan shall show Testing as a shared dependency
And downstream phases (FDA submission, EU submission, MFDS submission) shall all depend on Testing completion
```

---

### PL-003: Context Simplifier Integration
**Requirement**: Phase 3 Success Criterion - Load pathway and estimate data
**Priority**: High

**Test Cases**:

**PL-003.1**: Load pathway and estimate summaries
```gherkin
Given /aria:pathway and /aria:estimate have been executed
And both output .summary.md files
When /aria:plan is invoked
Then the skill shall load pathway and estimate data from .summary.md
And the milestone plan shall reflect the loaded timeline estimates
And cost allocations per phase shall match estimate categories
```

---

## Integration Tests

### IT-001: Full Phase 3 Pipeline
**Requirement**: Phase 3 Success Criterion - Pipeline flow operational
**Priority**: Critical

**Test Cases**:

**IT-001.1**: Sequential execution from classification to planning
```gherkin
Given /aria:classify has produced classification results
When /aria:pathway, /aria:estimate, and /aria:plan are executed sequentially
Then each step shall load data from the previous step's .summary.md
And no data shall be re-requested from the user
And the final plan shall accurately reflect classification → pathway → estimate data flow
```

---

## Negative Tests

### NT-001: Missing Prerequisites
**Requirement**: Graceful degradation
**Priority**: Medium

**Test Cases**:

**NT-001.1**: Pathway invoked without classification data
```gherkin
Given NO classification data exists
When /aria:pathway is executed
Then a warning message shall appear: "분류 데이터를 먼저 생성하세요"
And the user shall be prompted to run /aria:classify first
```

**NT-001.2**: Estimate invoked without pathway data
```gherkin
Given NO pathway data exists
When /aria:estimate is executed
Then a warning shall appear: "경로 선택 데이터가 필요합니다"
And the user shall be prompted to run /aria:pathway first
```

---

## Summary

**Total Test Scenarios**: 30+ test cases
**Coverage**: ER-004, ER-005, ER-006, UR-001 through UR-006, SR-001, SR-007
**Focus**: Pathway selection accuracy, cost/timeline estimation, milestone planning, pipeline integration
**Quality Target**: 85%+ acceptance criteria coverage

---

**Version**: 1.0.0
**Created**: 2026-02-11
**Author**: Backend Developer (team-backend-dev)
