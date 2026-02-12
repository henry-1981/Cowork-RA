# Test Scenarios for SPEC-ARIA-003: /aria:assess

**SPEC**: SPEC-ARIA-003 - Command & Skill Architecture Restructure
**Scope**: /aria:assess regulatory assessment pipeline
**Status**: Test scenarios documented
**Coverage Target**: 85%+ of assess command requirements

---

## Executive Summary

This document defines comprehensive test scenarios for the `/aria:assess` command, the regulatory assessment orchestrator that replaces `/aria:determine`, `/aria:classify`, `/aria:pathway`, and `/aria:compare` (for assessment context). Tests cover the integrated pipeline from product context loading through determination, classification, pathway analysis, and multi-region comparison.

---

## Test Strategy

### Test Categories

1. **Positive Tests** (55%): Expected behavior validation for pipeline flow
2. **Negative Tests** (20%): Error handling and edge cases
3. **Integration Tests** (15%): Skill chaining and context passing
4. **Degradation Tests** (10%): Graceful degradation and fallback scenarios

### Coverage Mapping

- Product context loading (5 cases)
- Input collection (3 modes)
- Determination phase with decision gate
- Classification phase with multi-region matrix
- Pathway phase with route selection
- Multi-region comparison logic
- Output generation (assess.md + assess.summary.md)
- Flag handling (--lang, --format)
- Skill invocation chain

---

## AS-001: Product Context Loading

**Requirement**: Workflow Step 1 - Product context management
**Priority**: Critical

### AS-001.1: Active product auto-load (Case 1)
```gherkin
Given .aria/active_product.json exists with valid product reference "cardiac-monitor-x1"
And .aria/products/cardiac-monitor-x1/ directory exists
When /aria:assess is executed
Then the active product shall be loaded automatically
And last_accessed date shall be updated
And no product selection menu shall be displayed
```

### AS-001.2: Multiple products with no active selection (Case 2)
```gherkin
Given .aria/products/ contains 3 products: cardiac-monitor-x1, glucose-meter, pulse-oximeter
And .aria/active_product.json does NOT exist
When /aria:assess is executed
Then a product selection menu shall be displayed
And menu shall list all 3 products with most recent dates
And user selection shall be persisted to .aria/active_product.json
```

### AS-001.3: Stale active product reference (Case 3)
```gherkin
Given .aria/active_product.json references "deleted-product"
And .aria/products/deleted-product/ does NOT exist
When /aria:assess is executed
Then active_product.json shall be treated as stale
And product selection menu shall be displayed
And active_product.json shall be updated with new selection
```

### AS-001.4: Single product auto-select (Case 4)
```gherkin
Given .aria/products/ contains exactly 1 product: cardiac-monitor-x1
And .aria/active_product.json does NOT exist
When /aria:assess is executed
Then cardiac-monitor-x1 shall be auto-selected
And active_product.json shall be persisted
And no selection menu shall be displayed
```

### AS-001.5: No products exist (Case 5)
```gherkin
Given .aria/products/ directory is empty or does not exist
When /aria:assess is executed
Then user shall be prompted to create a new product entry
And product naming convention shall be enforced (lowercase, hyphens, alphanumeric)
And new product shall be persisted to active_product.json
```

---

## AS-002: Input Collection

**Requirement**: Workflow Step 2 - Input modes
**Priority**: Critical

### AS-002.1: Technical document input
```gherkin
Given user provides a technical specification PDF
When /aria:assess processes the document
Then device description, intended use, product form, and primary function shall be extracted
And gap detection shall identify missing required fields
And targeted Q&A shall ask only for missing fields (max 1-3 rounds)
And assessment pipeline shall proceed after all fields are collected
```

### AS-002.2: Prior profile.json from /aria:chat
```gherkin
Given .aria/products/{product}/{date}/profile.json exists with completeness >= 70%
When /aria:assess is executed
Then product profile shall be loaded from profile.json
And only missing critical fields shall be requested
And collected information shall not be re-requested
```

### AS-002.3: No document and no prior context
```gherkin
Given no technical document is provided
And no prior profile.json exists
When /aria:assess is executed
Then conversational Q&A shall collect:
  - Device description and physical characteristics
  - Intended use statement (medical purpose)
  - Product form (hardware/software/IVD/combination)
  - Primary function and mechanism of action
  - Target markets (default: FDA, EU MDR, MFDS)
And once all fields are collected, pipeline shall proceed directly to Step 3
And Q&A conversation shall NOT be repeated or re-displayed
```

---

## AS-003: Determination Phase

**Requirement**: Workflow Step 3 - Device determination with decision gate
**Priority**: Critical

### AS-003.1: YES determination - continue to classification
```gherkin
Given a device clearly qualifying as a medical device (e.g., insulin pump)
When determination phase executes via Skill("aria-determination")
Then determination status shall be YES across FDA, EU MDR, MFDS
And traffic light shall be GREEN
And workflow shall continue to Step 4 (Classification)
```

### AS-003.2: CONDITIONAL determination - warning and continue
```gherkin
Given a borderline device (e.g., fitness tracker with heart rate monitoring)
When determination phase executes
Then determination status shall be CONDITIONAL
And a warning with rationale shall be displayed
And expert review shall be recommended
And workflow shall continue to Step 4 (Classification)
```

### AS-003.3: NO determination - stop workflow
```gherkin
Given a product that is clearly not a medical device (e.g., consumer electronics)
When determination phase executes
Then determination status shall be NO
And workflow shall STOP with rationale
And output shall contain determination-only result
And suggestion to consult expert if user disagrees shall be included
And NO classification or pathway analysis shall be performed
```

---

## AS-004: Classification Phase

**Requirement**: Workflow Step 4 - Multi-region classification
**Priority**: Critical

### AS-004.1: Multi-region classification matrix
```gherkin
Given a device confirmed as a medical device (determination = YES)
When classification phase executes via Skill("aria-classification")
Then classification matrix shall include:
  - FDA: Class I, II, or III
  - EU MDR: Class I, IIa, IIb, or III
  - MFDS: Grade 1, 2, 3, or 4
And each region shall have a traffic light indicator
And classification rationale shall reference applicable rules
```

### AS-004.2: Classification with determination context
```gherkin
Given determination phase has completed successfully
When classification phase executes
Then device characteristics from determination shall be passed as context
And classification shall NOT re-ask for device information already collected
And results shall be consistent with determination findings
```

---

## AS-005: Pathway Phase

**Requirement**: Workflow Step 5 - Regulatory pathway selection
**Priority**: Critical

### AS-005.1: FDA pathway selection based on classification
```gherkin
Given FDA classification result (Class I/II/III)
When pathway phase executes via Skill("aria-pathway")
Then appropriate FDA pathway shall be identified:
  - Class I: Exempt or 510(k) Exempt
  - Class II: 510(k) or De Novo
  - Class III: PMA
And timeline ranges shall be included
And key requirements shall be listed
```

### AS-005.2: EU MDR pathway selection
```gherkin
Given EU MDR classification result
When pathway phase executes
Then appropriate EU pathway shall be identified:
  - Class I: Self-declaration (Annex IV)
  - Class IIa/IIb: Notified Body Certification (Annex IX or X)
  - Class III: Full Notified Body QMS Certification (Annex IX)
And Notified Body requirement shall be indicated where applicable
```

### AS-005.3: MFDS pathway selection
```gherkin
Given MFDS classification result
When pathway phase executes
Then appropriate MFDS pathway shall be identified:
  - Grade 1: Product Registration
  - Grade 2-4: Product Approval
And clinical data requirements shall be indicated for higher grades
```

### AS-005.4: Critical path identification
```gherkin
Given pathways for 2+ target markets
When pathway phase completes
Then the critical path (longest timeline) shall be identified
And critical path region shall be highlighted in output
```

---

## AS-006: Multi-Region Comparison

**Requirement**: Workflow Step 6 - Comparison logic for 2+ markets
**Priority**: High

### AS-006.1: Comparison dimensions
```gherkin
Given a product targeting US + EU + Korea
When multi-region comparison logic executes
Then comparison shall include:
  - Regulatory basis and classification alignment across regions
  - Pathway complexity and timeline comparison
  - Shared testing activities and documentation overlap
  - Harmonized standards applicability (ISO 13485, ISO 14971, IEC 60601)
```

### AS-006.2: Strategic recommendation
```gherkin
Given multi-region comparison data
When strategic recommendation is generated
Then one of the following approaches shall be recommended:
  - Harmonized (design to most stringent, usually EU MDR)
  - Parallel (simultaneous multi-region submission)
  - Sequential (easiest market first)
And rationale shall be provided for the recommendation
```

### AS-006.3: Single market - no comparison
```gherkin
Given a product targeting only 1 market (e.g., FDA only)
When assessment pipeline completes
Then no multi-region comparison section shall be generated
And output shall contain determination, classification, and pathway only
```

---

## AS-007: Output Generation

**Requirement**: Workflow Step 7 - assess.md and assess.summary.md
**Priority**: Critical

### AS-007.1: Full report structure
```gherkin
Given a complete assessment pipeline execution
When output is generated
Then assess.md shall contain all sections:
  - Product Information
  - Device Determination (status table, applicable regulations)
  - Classification (multi-region matrix, key factors)
  - Regulatory Pathways (recommendations, critical path)
  - Multi-Region Comparison (if applicable)
  - Overall Assessment (traffic light summary, escalation items, next steps)
  - Disclaimer
```

### AS-007.2: Summary generation
```gherkin
Given assess.md is generated
When assess.summary.md is created
Then summary shall include:
  - Product name and date
  - Target markets
  - Determination status and traffic light
  - FDA/EU MDR/MFDS classification
  - Pathway per region with timelines
  - Critical path
  - Overall traffic light
  - Recommended strategy
And summary shall note it is consumed by /aria:project
```

### AS-007.3: Storage path convention
```gherkin
Given a product named "cardiac-monitor-x1"
And the command is executed on 2026-02-12
When output files are generated
Then files shall be stored at:
  - .aria/products/cardiac-monitor-x1/2026-02-12/assess.md
  - .aria/products/cardiac-monitor-x1/2026-02-12/assess.summary.md
```

---

## AS-008: Flag Handling

**Requirement**: Flags --lang and --format
**Priority**: High

### AS-008.1: Korean language output (default)
```gherkin
Given no --lang flag is specified
When /aria:assess generates output
Then all user-facing text shall be in Korean
And regulation codes shall remain in English (e.g., "FDA 510(k)")
```

### AS-008.2: English language output
```gherkin
Given --lang en flag is specified
When /aria:assess generates output
Then all user-facing text shall be in English
And report structure shall match the English template
```

### AS-008.3: Format flag - Markdown (default)
```gherkin
Given no --format flag is specified
When output is generated
Then Markdown file shall be saved to .aria/products/
And no format conversion shall occur
```

### AS-008.4: Format flag - PDF
```gherkin
Given --format pdf flag is specified
When output is generated
Then Markdown shall be generated first
And PDF conversion shall be attempted
And if PDF tool unavailable, Markdown shall be preserved with a notice
```

### AS-008.5: Format flag - Notion graceful degradation
```gherkin
Given --format notion flag is specified
And Notion MCP connector is NOT configured
When output is generated
Then Markdown shall be generated as fallback
And a notice shall explain Notion MCP is unavailable
```

---

## AS-009: Traffic Light System

**Requirement**: Traffic light interpretation for assess command
**Priority**: High

### AS-009.1: Overall traffic light - most conservative
```gherkin
Given determination = GREEN, classification = GREEN, pathway = YELLOW
When overall traffic light is calculated
Then overall traffic light shall be YELLOW (most conservative)
```

### AS-009.2: RED traffic light triggers
```gherkin
Given insufficient information to determine or classify
When any phase produces RED traffic light
Then overall assessment shall be RED
And fundamental approach change recommendation shall be included
```

### AS-009.3: All GREEN assessment
```gherkin
Given all phases produce GREEN traffic light
When overall assessment is generated
Then overall traffic light shall be GREEN
And no escalation items shall appear
```

---

## AS-010: Skill Invocation Chain

**Requirement**: Correct skill chaining (determination -> classification -> pathway)
**Priority**: Critical

### AS-010.1: Sequential skill execution with context passing
```gherkin
Given product information is collected
When /aria:assess executes the pipeline
Then Skill("aria-determination") shall execute first
And determination results shall be passed to Skill("aria-classification")
And classification results shall be passed to Skill("aria-pathway")
And no skill shall re-request information already collected by a previous skill
```

### AS-010.2: Pipeline stops on NO determination
```gherkin
Given determination phase returns NO
When pipeline evaluates the decision gate
Then Skill("aria-classification") shall NOT be invoked
And Skill("aria-pathway") shall NOT be invoked
And output shall contain only determination results
```

---

## AS-011: Disclaimer

**Requirement**: Standard disclaimer in all output
**Priority**: High

### AS-011.1: Disclaimer present in assess.md
```gherkin
Given /aria:assess generates assess.md
When the output is reviewed
Then the disclaimer section shall be present
And it shall state: "This assessment is an AI-based regulatory intelligence analysis, not official regulatory advice."
And knowledge base date shall be included
```

---

## Negative Tests

### NT-AS-001: Empty product description
```gherkin
Given user provides no product description
And no document is uploaded
When /aria:assess attempts input collection
Then system shall prompt for minimum required information
And pipeline shall NOT proceed until required fields are collected
```

### NT-AS-002: Large document handling
```gherkin
Given a technical document with >100 pages
When /aria:assess processes the document
Then Table of Contents shall be analyzed first
And only relevant sections shall be extracted
And token efficiency shall be maintained
```

### NT-AS-003: Invalid product form
```gherkin
Given user provides an unrecognized product form (e.g., "quantum device")
When input validation occurs
Then system shall request clarification
And suggest valid options: hardware, software, IVD, combination
```

---

## Summary

**Total Test Scenarios**: 30+ test cases
**Coverage**: Product context loading, input collection, determination, classification, pathway, comparison, output generation, flags, traffic light, skill chain, disclaimer
**Focus**: End-to-end integrated assessment pipeline validation
**Quality Target**: 85%+ acceptance criteria coverage

---

**Version**: 1.0.0
**Created**: 2026-02-12
**Author**: team-tester (ARIA Plugin Team)
