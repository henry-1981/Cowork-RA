# Test Scenarios for SPEC-ARIA-003: /aria:report

**SPEC**: SPEC-ARIA-003 - Command & Skill Architecture Restructure
**Scope**: /aria:report comprehensive report generator
**Status**: Test scenarios documented
**Coverage Target**: 85%+ of brief command requirements

---

## Executive Summary

This document defines comprehensive test scenarios for the `/aria:report` command, the comprehensive report generator that absorbs the former briefing skill. Tests cover pipeline data loading, data completeness assessment, two-phase output (ER-017 report issuance policy), focus area selection, backward compatibility with legacy data, and multi-format output generation.

---

## Test Strategy

### Test Categories

1. **Positive Tests** (50%): Expected behavior for report generation
2. **Negative Tests** (20%): Missing data and error handling
3. **Integration Tests** (20%): Pipeline data loading and format conversion
4. **Backward Compatibility Tests** (10%): Legacy data format handling

### Coverage Mapping

- Pipeline data loading (new and legacy formats)
- Data completeness assessment (4 states)
- Two-phase output (ER-017 policy)
- Focus area identification
- Output template compliance
- Summary generation
- Format conversion (markdown, pdf, notion, gdocs)
- Backward compatibility with legacy output files

---

## BR-001: Product Context Loading

**Requirement**: Workflow Step 1 - Product context management
**Priority**: Critical

### BR-001.1: Active product with pipeline data
```gherkin
Given .aria/active_product.json exists with valid product
And .aria/products/{product}/{date}/ contains assess.md and project.md
When /aria:report is executed
Then active product shall be loaded
And pipeline data scan shall proceed
```

### BR-001.2: No products exist
```gherkin
Given .aria/products/ directory is empty
When /aria:report is executed
Then user shall be warned that briefing requires pipeline data
And suggestion to run /aria:assess first shall be provided
```

---

## BR-002: Pipeline Data Loading

**Requirement**: Workflow Step 2 - Scan for available pipeline data
**Priority**: Critical

### BR-002.1: New format data loading
```gherkin
Given .aria/products/{product}/{date}/ contains:
  - profile.json (from /aria:chat)
  - assess.md + assess.summary.md (from /aria:assess)
  - project.md + project.summary.md (from /aria:project)
When /aria:report loads pipeline data
Then all new format files shall be loaded
And .summary.md files shall be used for executive summary
And full .md files shall be used for detailed analysis sections
```

### BR-002.2: Legacy format data loading
```gherkin
Given .aria/products/{product}/{date}/ contains:
  - determination.summary.md + determination.md
  - classification.summary.md + classification.md
  - pathway.summary.md + pathway.md
  - estimation.summary.md + estimation.md
  - plan.summary.md + plan.md
And NO new format files exist
When /aria:report loads pipeline data
Then legacy format files shall be loaded
And briefing shall be generated from legacy data
```

### BR-002.3: Mixed format - new preferred over legacy
```gherkin
Given both assess.md and determination.md exist in the same directory
When /aria:report loads pipeline data
Then new format files (assess.md) shall be preferred
And legacy format files shall be ignored when new format exists
```

---

## BR-003: Data Completeness Assessment

**Requirement**: Workflow Step 3 - Determine briefing scope
**Priority**: Critical

### BR-003.1: Full pipeline (assess + project data)
```gherkin
Given assess.md and project.md both exist
When data completeness is assessed
Then comprehensive briefing with ALL sections shall be generated:
  - Executive Summary
  - Detailed Analysis (all 6 subsections)
  - Recommendations
  - Appendices
```

### BR-003.2: Assessment only (no project data)
```gherkin
Given assess.md exists but project.md does NOT exist
When data completeness is assessed
Then focused briefing covering regulatory assessment shall be generated
And sections shall include: device status, classification, pathways, comparison
And missing project data shall be indicated
And recommendation to run /aria:project shall be included
```

### BR-003.3: Project only (no assess data)
```gherkin
Given project.md exists but assess.md does NOT exist
When data completeness is assessed
Then focused briefing covering project plan shall be generated
And sections shall include: cost/timeline estimates, milestone plan
And missing assessment data shall be indicated
And recommendation to run /aria:assess shall be included
```

### BR-003.4: No pipeline data - stop workflow
```gherkin
Given no assess.md, no project.md, and no legacy files exist
When data completeness is assessed
Then user shall be warned: "No pipeline data found."
And suggestion shall be: "Run /aria:assess first, then /aria:project for a complete briefing."
And workflow shall STOP
And no briefing report shall be generated
```

---

## BR-004: Two-Phase Output (ER-017)

**Requirement**: Workflow Step 5 - Report issuance policy
**Priority**: Critical

### BR-004.1: Phase A - Analysis summary presented first
```gherkin
Given sufficient pipeline data exists
When /aria:report is executed
Then Phase A analysis summary shall be presented:
  - Product Overview (name, device status, classification)
  - Key Findings (pathways, critical path, budget range, risks)
  - Top 3 Recommendations
  - Overall Traffic Light
And user confirmation shall be requested before full report
```

### BR-004.2: Phase B - Full report after confirmation
```gherkin
Given Phase A analysis summary has been presented
And user confirms to proceed
When Phase B executes
Then full briefing report shall be generated
And complete output template shall be followed
And report shall be saved to .aria/products/
```

### BR-004.3: Full report NOT generated in same turn as analysis
```gherkin
Given Phase A analysis is presented
When checking the ER-017 policy
Then full formatted report shall NOT appear in the same response as analysis
And user must explicitly confirm before Phase B generation
```

---

## BR-005: Focus Area Identification

**Requirement**: Workflow Step 4 - Optional focus area
**Priority**: Medium

### BR-005.1: Clinical Strategy focus
```gherkin
Given user specifies: /aria:report Clinical Strategy
When briefing is generated
Then recommendations section shall emphasize:
  - Clinical evidence requirements
  - Trial planning details
  - Clinical study timeline and cost implications
```

### BR-005.2: Cost Control focus
```gherkin
Given user specifies focus on cost control
When briefing is generated
Then recommendations shall emphasize:
  - Budget optimization opportunities
  - Cost reduction strategies
  - Shared testing cost savings
```

### BR-005.3: Timeline Acceleration focus
```gherkin
Given user specifies focus on timeline acceleration
When briefing is generated
Then recommendations shall emphasize:
  - Parallel submission opportunities
  - Expedited pathway options
  - Critical path optimization
```

### BR-005.4: Default - balanced coverage
```gherkin
Given no focus area is specified
When briefing is generated
Then all aspects shall receive balanced coverage
And no single dimension shall be over-emphasized
```

---

## BR-006: Output Template Compliance

**Requirement**: Workflow Step 6 - Full report structure
**Priority**: Critical

### BR-006.1: Complete report sections
```gherkin
Given full pipeline data and user confirmation
When full briefing report is generated
Then briefing.md shall include:
  - Table of Contents
  - 1. Executive Summary (product overview, regulatory status, pathways, cost/timeline, risks, recommendations)
  - 2. Detailed Analysis (determination, classification, pathways, comparison, estimation, milestone plan)
  - 3. Recommendations (immediate actions, dependencies, resources, risk mitigation)
  - 4. Appendices (regulatory citations, data sources, escalation items, glossary)
  - Disclaimer
```

### BR-006.2: Executive Summary completeness
```gherkin
Given all pipeline data is available
When executive summary section is generated
Then all of the following shall be present:
  - Product overview (name, intended use, regulatory scope)
  - Medical device status with traffic light
  - Classification per region (FDA, EU MDR, MFDS)
  - Recommended pathways with timelines
  - Critical path identification
  - Total budget range (optimistic ~ expected ~ pessimistic)
  - Total timeline
  - Key risks with traffic light
  - Top 3 strategic recommendations
```

### BR-006.3: Disclaimer present
```gherkin
Given any /aria:report execution
When briefing.md is generated
Then disclaimer shall state: "This briefing is an AI-based regulatory intelligence synthesis, not official regulatory advice."
And knowledge base date shall be included
```

---

## BR-007: Summary Generation

**Requirement**: Workflow Step 7 - briefing.summary.md
**Priority**: High

### BR-007.1: Summary content
```gherkin
Given briefing.md is generated
When briefing.summary.md is created
Then summary shall include:
  - Product name and date
  - Pipeline steps covered
  - Traffic light (overall)
  - Critical path (region and timeline)
  - Total budget (expected range)
  - Key risks (top 3)
  - Top recommendations (top 3)
  - Escalation items (yes/no with count)
  - Sources
And summary shall note it is for audit trail
```

---

## BR-008: File Storage

**Requirement**: Workflow Step 8 - Output location
**Priority**: High

### BR-008.1: Standard storage path
```gherkin
Given a product named "cardiac-monitor-x1" executed on 2026-02-12
When briefing output is generated
Then files shall be stored at:
  - .aria/products/cardiac-monitor-x1/2026-02-12/briefing.md (always)
  - .aria/products/cardiac-monitor-x1/2026-02-12/briefing.summary.md (always)
```

### BR-008.2: PDF output location
```gherkin
Given --format pdf flag is specified
When briefing output is generated
Then additional file shall be created:
  - .aria/products/{product}/{date}/briefing.pdf
And briefing.md shall also be generated as base
```

---

## BR-009: Format Output

**Requirement**: Format selection and graceful degradation
**Priority**: High

### BR-009.1: Markdown output (default)
```gherkin
Given no --format flag is specified
When /aria:report generates output
Then briefing.md shall be saved as Markdown
And no format conversion shall occur
```

### BR-009.2: PDF output with available tool
```gherkin
Given --format pdf flag is specified
And pandoc is available on the system
When /aria:report generates output
Then Markdown shall be generated first
And PDF shall be converted using pandoc
And briefing.pdf shall be saved alongside briefing.md
```

### BR-009.3: PDF graceful degradation
```gherkin
Given --format pdf flag is specified
And no PDF conversion tool is available
When /aria:report generates output
Then Markdown shall be preserved
And notice shall explain PDF tool is unavailable
And installation guidance for pandoc/wkhtmltopdf/weasyprint shall be provided
```

### BR-009.4: Notion format
```gherkin
Given --format notion flag is specified
And Notion MCP connector is configured
When /aria:report generates output
Then Notion page shall be created
And Markdown backup shall also be saved
```

### BR-009.5: Google Docs format
```gherkin
Given --format gdocs flag is specified
And Google Drive MCP connector is configured
When /aria:report generates output
Then Google Docs document shall be created with title: "{Product Name} - Regulatory Briefing Report ({date})"
And Markdown backup shall also be saved
```

---

## BR-010: Traffic Light System

**Requirement**: Traffic light for brief command
**Priority**: High

### BR-010.1: Most conservative across all pipeline steps
```gherkin
Given assess traffic light = GREEN and project traffic light = YELLOW
When overall briefing traffic light is calculated
Then overall shall be YELLOW (most conservative)
```

### BR-010.2: All GREEN
```gherkin
Given all pipeline steps have GREEN traffic light
When overall briefing traffic light is calculated
Then overall shall be GREEN
And no fundamental approach changes shall be recommended
```

### BR-010.3: RED flags present
```gherkin
Given any pipeline step has RED traffic light
When overall briefing traffic light is calculated
Then overall shall be RED
And recommendation for fundamental approach change shall be included
```

---

## Negative Tests

### NT-BR-001: Partial pipeline data - missing sections
```gherkin
Given only assess.summary.md exists (no full assess.md)
When /aria:report generates detailed analysis
Then summary data shall be used for available sections
And missing detailed data shall be noted in the report
```

### NT-BR-002: Corrupted or empty summary files
```gherkin
Given assess.summary.md exists but is empty or malformed
When /aria:report loads pipeline data
Then the corrupted file shall be skipped
And data completeness shall reflect the missing data
And user shall be informed of the issue
```

### NT-BR-003: User cancels after Phase A
```gherkin
Given Phase A analysis summary has been presented
And user declines to proceed with full report
When user response is processed
Then no full briefing report shall be generated
And no files shall be saved
And conversation shall return to normal state
```

---

## Summary

**Total Test Scenarios**: 30+ test cases
**Coverage**: Product context, pipeline data loading, data completeness, two-phase output, focus areas, template compliance, summary, file storage, format output, traffic light, backward compatibility
**Focus**: Report generation quality and ER-017 policy compliance
**Quality Target**: 85%+ acceptance criteria coverage

---

**Version**: 1.0.0
**Created**: 2026-02-12
**Author**: team-tester (ARIA Plugin Team)
