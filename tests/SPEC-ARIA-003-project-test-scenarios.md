# Test Scenarios for SPEC-ARIA-003: /aria:project

**SPEC**: SPEC-ARIA-003 - Command & Skill Architecture Restructure
**Scope**: /aria:project project planning pipeline
**Status**: Test scenarios documented
**Coverage Target**: 85%+ of project command requirements

---

## Executive Summary

This document defines comprehensive test scenarios for the `/aria:project` command, the project planning orchestrator that replaces `/aria:estimate`, `/aria:plan`, and `/aria:compare` (for project context). Tests cover the integrated pipeline from assessment data loading through cost/timeline estimation, milestone planning, and multi-region optimization.

---

## Test Strategy

### Test Categories

1. **Positive Tests** (55%): Expected behavior validation for pipeline flow
2. **Negative Tests** (20%): Error handling and edge cases
3. **Integration Tests** (15%): Skill chaining and assessment data loading
4. **Degradation Tests** (10%): Missing data and fallback scenarios

### Coverage Mapping

- Assessment data loading (3 cases: new format, legacy, no data)
- Estimation phase with three-point ranges
- Planning phase with milestone generation
- Multi-region optimization
- Output generation (project.md + project.summary.md)
- Flag handling (--lang, --format)
- Downstream integration (brief command)

---

## PJ-001: Product Context Loading

**Requirement**: Workflow Step 1 - Same as assess command
**Priority**: Critical

### PJ-001.1: Active product auto-load
```gherkin
Given .aria/active_product.json exists with valid product reference
When /aria:project is executed
Then the active product shall be loaded automatically
And no product selection menu shall be displayed
```

### PJ-001.2: Product selection required
```gherkin
Given multiple products exist with no active_product.json
When /aria:project is executed
Then product selection menu shall be displayed
And user selection shall be persisted
```

---

## PJ-002: Assessment Data Loading

**Requirement**: Workflow Step 2 - Load assessment results
**Priority**: Critical

### PJ-002.1: New format assess.summary.md exists (Case A)
```gherkin
Given .aria/products/{product}/{date}/assess.summary.md exists
When /aria:project loads assessment data
Then classification and pathway data shall be extracted from assess.summary.md
And user shall be informed: "Assessment data loaded from {date}."
And estimation shall proceed with loaded pathway types
```

### PJ-002.2: Legacy pipeline data exists (Case B)
```gherkin
Given assess.summary.md does NOT exist
And legacy files exist: determination.summary.md, classification.summary.md, pathway.summary.md
When /aria:project loads assessment data
Then legacy summaries shall be loaded as fallback
And pathway and classification data shall be extracted
And user shall be informed: "Legacy pipeline data loaded. Consider running /aria:assess for integrated results."
```

### PJ-002.3: No assessment data found (Case C)
```gherkin
Given no assess.summary.md and no legacy pipeline data exists
When /aria:project attempts to load assessment data
Then user shall be informed: "No assessment data found. For best results, run /aria:assess first."
And manual input shall be accepted:
  - Target markets (FDA, EU MDR, MFDS)
  - Device class per market
  - Expected pathway per market
And pipeline shall proceed with user-provided data
```

---

## PJ-003: Estimation Phase

**Requirement**: Workflow Step 3 - Three-point cost/timeline estimation
**Priority**: Critical

### PJ-003.1: Three-point cost estimation per region
```gherkin
Given pathway selections and classification data are loaded
When estimation phase executes via Skill("aria-estimation")
Then cost estimation shall include three scenarios:
  - Optimistic: Best-case scenario
  - Expected: Most likely scenario (industry average)
  - Pessimistic: Worst-case scenario
And cost categories shall include:
  - Consulting services
  - Testing and validation
  - Regulatory fees
  - Notified Body fees (EU only)
  - Clinical study costs (if applicable)
```

### PJ-003.2: Class I low-cost estimation
```gherkin
Given a Class I exempt device pathway
When estimation phase executes
Then total cost range shall reflect low regulatory burden
And no clinical study costs shall be included
And timeline shall be the shortest among all classes
```

### PJ-003.3: Class III high-cost estimation
```gherkin
Given a Class III PMA device pathway
When estimation phase executes
Then clinical study costs shall be included
And total cost shall significantly exceed Class I/II estimates
And timeline shall be the longest among all classes
And disclaimer shall emphasize high uncertainty in Class III estimates
```

### PJ-003.4: Timeline estimation with milestones
```gherkin
Given a 510(k) pathway selection
When estimation phase executes
Then milestone timeline shall include phases:
  - Predicate device search
  - Testing and documentation
  - FDA review period
And total timeline range shall show optimistic/expected/pessimistic
```

### PJ-003.5: Critical path identification
```gherkin
Given pathways for US + EU + Korea
When estimation phase completes
Then the critical path (longest timeline) shall be identified
And bottleneck phase shall be described
```

---

## PJ-004: Planning Phase

**Requirement**: Workflow Step 4 - Milestone plan generation
**Priority**: Critical

### PJ-004.1: Single-market milestone plan (510(k))
```gherkin
Given a 510(k) pathway with cost/timeline estimates
When planning phase executes via Skill("aria-planning")
Then a 4-phase plan shall be generated:
  - Phase 1: Preparation (predicate search, gap analysis)
  - Phase 2: Testing (bench, biocompatibility, electrical safety)
  - Phase 3: Documentation (510(k) submission package)
  - Phase 4: Submission and Review
And each phase shall include: objective, activities, deliverables, dependencies, cost allocation, responsible party
```

### PJ-004.2: PMA pathway plan with clinical trial
```gherkin
Given a PMA pathway selection
When planning phase executes
Then plan shall include clinical trial phase
And IDE (Investigational Device Exemption) approval shall be a dependency
And clinical study costs shall be allocated to a dedicated phase
```

### PJ-004.3: Multi-market parallel submission plan
```gherkin
Given pathways for US + EU + Korea
When planning phase executes
Then plan shall show parallel tracks per market
And common dependencies shall be highlighted (e.g., shared testing data)
And parallel submission scheduling shall be included
```

### PJ-004.4: Dependency mapping
```gherkin
Given a multi-phase plan
When dependency map is generated
Then sequential dependencies within each market shall be shown
And cross-market shared dependencies shall be identified
And critical path through dependencies shall be highlighted
```

---

## PJ-005: Multi-Region Optimization

**Requirement**: Workflow Step 5 - Comparison logic for 2+ markets
**Priority**: High

### PJ-005.1: Parallel execution analysis
```gherkin
Given a product targeting US + EU + Korea
When multi-region optimization executes
Then shared phases across regions shall be identified
And parallel vs. sequential timeline impact shall be calculated
And cost savings from shared activities shall be estimated (typically 15-30%)
```

### PJ-005.2: Optimization recommendations
```gherkin
Given multi-region comparison data
When optimization recommendations are generated
Then recommendations shall include:
  - Common testing reuse (biocompatibility, electrical safety, performance)
  - Harmonized documentation strategy
  - Parallel submission scheduling
  - Critical path optimization
```

### PJ-005.3: Single market - no optimization
```gherkin
Given a product targeting only 1 market
When project pipeline completes
Then no multi-region optimization section shall be generated
And output shall contain estimation and planning only
```

---

## PJ-006: Output Generation

**Requirement**: Workflow Step 6 - project.md and project.summary.md
**Priority**: Critical

### PJ-006.1: Full report structure
```gherkin
Given a complete project pipeline execution
When output is generated
Then project.md shall contain all sections:
  - Product Information
  - Cost Estimation (total range, breakdown by region, multi-region savings)
  - Timeline Estimation (total range, milestones per region, critical path)
  - Milestone Plan (overview, phase-by-phase, parallel submission, dependency map, milestones table)
  - Risk Assessment (traffic light summary, key risks, contingency plan)
  - Recommended Next Steps
  - Disclaimer
```

### PJ-006.2: Summary generation for downstream
```gherkin
Given project.md is generated
When project.summary.md is created
Then summary shall include:
  - Product name and date
  - Cost ranges (optimistic/expected/pessimistic)
  - Timeline ranges (optimistic/expected/pessimistic)
  - Critical path (region, duration, bottleneck)
  - Submission strategy (parallel/sequential)
  - Overall traffic light
And summary shall note it is consumed by /aria:report
```

### PJ-006.3: Storage path convention
```gherkin
Given a product named "cardiac-monitor-x1"
And the command is executed on 2026-02-12
When output files are generated
Then files shall be stored at:
  - .aria/products/cardiac-monitor-x1/2026-02-12/project.md
  - .aria/products/cardiac-monitor-x1/2026-02-12/project.summary.md
```

---

## PJ-007: Traffic Light System

**Requirement**: Traffic light interpretation for project command
**Priority**: High

### PJ-007.1: GREEN - low cost and short timeline
```gherkin
Given total cost < W150M and timeline < 12 months and no clinical study
When traffic light is calculated
Then overall traffic light shall be GREEN
```

### PJ-007.2: YELLOW - moderate cost or long timeline
```gherkin
Given cost W150-500M or timeline 12-24 months or clinical study required
When traffic light is calculated
Then overall traffic light shall be YELLOW
```

### PJ-007.3: Most conservative applies
```gherkin
Given cost = GREEN, timeline = YELLOW, complexity = GREEN
When overall traffic light is calculated
Then overall shall be YELLOW (most conservative)
```

---

## PJ-008: Flag Handling

**Requirement**: Flags --lang and --format
**Priority**: High

### PJ-008.1: Korean language output (default)
```gherkin
Given no --lang flag is specified
When /aria:project generates output
Then all user-facing text shall be in Korean
```

### PJ-008.2: English language output
```gherkin
Given --lang en flag is specified
When /aria:project generates output
Then all user-facing text shall be in English
```

### PJ-008.3: Google Docs format
```gherkin
Given --format gdocs flag is specified
And Google Drive MCP connector is configured
When output is generated
Then Google Docs document shall be created
And Markdown backup shall also be saved to .aria/products/
```

### PJ-008.4: Format graceful degradation
```gherkin
Given --format notion flag is specified
And Notion MCP connector is NOT configured
When output is generated
Then Markdown shall be generated as fallback
And a notice shall explain Notion MCP is unavailable
```

---

## PJ-009: Skill Invocation Chain

**Requirement**: Correct skill chaining (estimation -> planning)
**Priority**: Critical

### PJ-009.1: Sequential skill execution with context passing
```gherkin
Given assessment data is loaded
When /aria:project executes the pipeline
Then Skill("aria-estimation") shall execute first
And estimation results shall be passed to Skill("aria-planning")
And planning shall use estimation timeline ranges for phase allocation
```

---

## Negative Tests

### NT-PJ-001: No assessment data and user declines manual input
```gherkin
Given no assessment data exists
And user declines to provide manual input
When /aria:project is executed
Then a guidance message shall recommend running /aria:assess first
And pipeline shall not proceed with empty data
```

### NT-PJ-002: Stale assessment data
```gherkin
Given assess.summary.md exists but is older than data_retention_days setting
When /aria:project loads assessment data
Then a warning about stale data shall be displayed
And user shall be given option to proceed or re-run /aria:assess
```

### NT-PJ-003: Inconsistent classification and pathway data
```gherkin
Given legacy data with conflicting classification and pathway selections
When estimation phase attempts to use the data
Then system shall detect the inconsistency
And shall present the conflict to user for resolution
```

---

## Summary

**Total Test Scenarios**: 28+ test cases
**Coverage**: Product context, assessment data loading, estimation, planning, multi-region optimization, output, traffic light, flags, skill chain
**Focus**: End-to-end integrated project planning pipeline validation
**Quality Target**: 85%+ acceptance criteria coverage

---

**Version**: 1.0.0
**Created**: 2026-02-12
**Author**: team-tester (ARIA Plugin Team)
