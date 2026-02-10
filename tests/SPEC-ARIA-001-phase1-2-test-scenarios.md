# Test Scenarios for SPEC-ARIA-001 Phase 1-2

**SPEC**: SPEC-ARIA-001 v3.2.0
**Scope**: Phase 1-2 acceptance criteria validation
**Status**: Test scenarios documented
**Coverage Target**: 85%+ of Phase 1-2 requirements

---

## Executive Summary

This document defines comprehensive test scenarios for ARIA Cowork Plugin Phase 1-2, covering:
- **Phase 1**: Plugin recognition, MCP configuration, scaffold validation
- **Phase 2**: Determination and classification skills with document-first input, context compression, graceful degradation

Test design follows TDD methodology with 85%+ coverage target for all Phase 1-2 acceptance criteria.

---

## Test Strategy

### Test Categories

1. **Positive Tests** (60%): Expected behavior validation
2. **Negative Tests** (20%): Error handling and edge cases
3. **Integration Tests** (15%): Command-to-skill-to-output workflow
4. **Degradation Tests** (5%): Graceful degradation scenarios

### Coverage Mapping

All test scenarios map to acceptance criteria in `acceptance.md`:
- **Ubiquitous Requirements**: UR-001 through UR-006
- **Event-Driven Requirements**: ER-002 (determine), ER-003 (classify), ER-009 (next steps), ER-011 (context), ER-012 (multi-format), ER-013/014 (document), ER-015 (compression), ER-016 (stale data)
- **State-Driven Requirements**: SR-001 (degradation), SR-006 (multi-product), SR-007 (versioning)
- **Unwanted Behaviors**: WR-001 through WR-005
- **Quality Gates**: VALID framework, quantitative targets

---

## Phase 1: Plugin Scaffold Test Scenarios

### PS-001: Plugin Recognition by Cowork Platform
**Requirement**: Phase 1 Success Criterion - Plugin recognized by Cowork platform
**Priority**: Critical

**Test Cases**:

**PS-001.1**: Valid plugin.json loads successfully
```gherkin
Given .claude-plugin/plugin.json exists with valid structure
When the Cowork platform loads the plugin
Then the plugin shall be recognized without errors
And the plugin name shall be "aria"
And the version shall be "2.0.0"
```

**PS-001.2**: plugin.json references valid component paths
```gherkin
Given plugin.json declares commands path "../commands/"
And plugin.json declares skills path "../skills/"
And plugin.json declares mcpServers path "../.mcp.json"
When the Cowork platform validates component paths
Then all paths shall be validated successfully
And no missing path errors shall be raised
```

**PS-001.3**: Missing plugin.json causes recognition failure
```gherkin
Given .claude-plugin/plugin.json does NOT exist
When the Cowork platform attempts to load the plugin
Then a clear error message shall be displayed
And the error shall indicate missing plugin manifest
```

---

### PS-002: MCP Configuration Validation
**Requirement**: Phase 1 Success Criterion - MCP configuration validates without errors
**Priority**: Critical

**Test Cases**:

**PS-002.1**: Valid .mcp.json with environment variables
```gherkin
Given .mcp.json contains Notion MCP configuration with env var NOTION_API_KEY
And .mcp.json contains Google Drive MCP configuration with env var GOOGLE_CREDENTIALS
And .mcp.json contains Context7 MCP configuration with env var CONTEXT7_API_KEY
When MCP configuration is validated
Then all three MCP servers shall be recognized
And no hardcoded credentials shall be present
```

**PS-002.2**: Environment variables placeholder validation
```gherkin
Given .mcp.json references environment variables for all MCP connectors
When configuration is parsed
Then no actual credentials shall be present in .mcp.json
And environment variable placeholders shall be preserved
```

---

### PS-003: README Completeness
**Requirement**: Phase 1 Success Criterion - README provides complete setup instructions
**Priority**: High

**Test Cases**:

**PS-003.1**: README includes all required sections
```gherkin
Given README.md exists in plugin root
When the document is reviewed
Then the following sections shall be present:
- ARIA overview and capabilities
- Installation instructions
- MCP connector setup (Notion, Google Drive, Context7)
- Command reference with /aria: prefix
- aria.local.md playbook template
- Data security warning for .aria/ directory
- Troubleshooting and FAQ
```

**PS-003.2**: All command references use /aria: prefix
```gherkin
Given README.md contains command examples
When all command references are extracted
Then every command shall use /aria: namespace prefix
And no bare command names (e.g., "determine" without "/aria:") shall appear
```

---

## Phase 2: Foundation Skills Test Scenarios

### FS-001: Determination Skill - Active Medical Device
**Requirement**: ER-002, Phase 2 Success Criterion
**Priority**: Critical

**Product**: Insulin pump
**Expected Result**: YES (medical device), GREEN traffic light

**Test Cases**:

**FS-001.1**: FDA determination
```gherkin
Given product description: "Insulin pump for continuous glucose-responsive insulin delivery"
And intended use: "Deliver insulin to diabetic patients for blood glucose control"
When determination skill is activated
Then FDA status shall be "YES - Medical Device"
And classification logic shall reference 21 CFR 201(h) criteria
And traffic light shall be GREEN
```

**FS-001.2**: EU MDR determination
```gherkin
Given same product description and intended use
When EU MDR criteria are applied
Then EU MDR status shall be "YES - Medical Device"
And rationale shall reference Article 2(1) medical purpose
And traffic light shall be GREEN
```

**FS-001.3**: MFDS determination
```gherkin
Given same product description and intended use
When MFDS criteria are applied
Then MFDS status shall be "YES - Medical Device (의료기기)"
And Korean regulatory scope shall be confirmed
And traffic light shall be GREEN
```

---

### FS-002: Determination Skill - Wellness Product (Borderline)
**Requirement**: ER-002, Escalation Path
**Priority**: High

**Product**: Fitness tracker with heart rate monitor
**Expected Result**: CONDITIONAL, YELLOW traffic light, escalation recommended

**Test Cases**:

**FS-002.1**: Borderline determination with escalation
```gherkin
Given product description: "Fitness tracker monitoring heart rate, steps, sleep quality"
And intended use: "General wellness and fitness monitoring"
When determination skill is activated
Then determination status may be CONDITIONAL
And traffic light shall be YELLOW if medical claims unclear
And escalation recommendation shall be present
And escalation reason shall reference wellness vs medical device boundary
```

---

### FS-003: Classification Skill - Class II FDA Device
**Requirement**: ER-003, Phase 2 Success Criterion
**Priority**: Critical

**Product**: Infusion pump
**Expected Result**: FDA Class II, EU MDR Class IIb, MFDS Class 3

**Test Cases**:

**FS-003.1**: Multi-region classification matrix
```gherkin
Given device characteristics:
- Invasiveness: Invasive (intravenous access)
- Duration: Short-term (hours to days)
- Active: Yes (powered device)
- Intended use: Fluid/medication delivery
When classification skill is activated
Then FDA class shall be II
And EU MDR class shall be IIb
And MFDS class shall be 3
And all three traffic lights shall be GREEN
```

**FS-003.2**: Classification rationale
```gherkin
Given same device characteristics
When classification matrix is generated
Then FDA rationale shall reference special controls requirement
And EU MDR rationale shall reference Annex VIII Rule 11 (active therapeutic)
And MFDS rationale shall reference invasive use and moderate risk
```

---

### FS-004: Classification Optimization Analysis (OR-004)
**Requirement**: OR-004, Classification optimization
**Priority**: Medium

**Product**: Long-term implantable sensor
**Expected Result**: Optimization suggestions, YELLOW traffic light, mandatory escalation

**Test Cases**:

**FS-004.1**: Optimization analysis with --optimize flag
```gherkin
Given device characteristics:
- Invasiveness: Implantable
- Duration: Long-term (>30 days)
- Active: Yes
- Current classification: FDA Class III, EU MDR Class III
When classify command is invoked with --optimize flag
Then optimization analysis section shall be present
And suggestions shall include abstract guidance on:
  - Reducing invasiveness (e.g., non-implantable alternatives)
  - Shortening duration (e.g., transient monitoring)
  - Passive design alternatives
And traffic light shall be YELLOW (mandatory)
And escalation shall be mandatory to R&D + Regulatory affairs
And supplementary optimization disclaimer shall be present
```

**FS-004.2**: No specific design recommendations
```gherkin
Given optimization analysis is performed
When optimization output is reviewed
Then no specific design changes shall be provided
And all guidance shall be abstract and strategic
And output shall state "requires R&D feasibility assessment"
```

---

### FS-005: Document-First Input Workflow (S9)
**Requirement**: ER-013, ER-014, Document analysis
**Priority**: High

**Test Cases**:

**FS-005.1**: Complete document with all fields
```gherkin
Given technical specification document with:
- Device description: Complete
- Intended use: Complete
- Product form: Specified
- Primary function: Described
When determine command is invoked with document
Then system shall extract all fields from document
And Q&A rounds shall be 0 (no missing fields)
And determination analysis shall proceed immediately
```

**FS-005.2**: Partial document with gaps
```gherkin
Given technical document with:
- Device description: Complete
- Intended use: Missing
- Product form: Specified
When determine command is invoked with document
Then system shall extract available fields
And gap detection shall identify "intended use" as missing
And targeted Q&A shall ask ONLY for intended use (1 round)
And determination analysis shall proceed after Q&A
```

**FS-005.3**: Large document (>100 pages)
```gherkin
Given technical document with 150 pages and Table of Contents
When determine command is invoked with document
Then system shall analyze Table of Contents first
And system shall extract relevant sections only
And token efficiency target (<5000 tokens processed) shall be met
```

---

### FS-006: Context Simplifier Integration (S10)
**Requirement**: ER-015, Context compression
**Priority**: High

**Test Cases**:

**FS-006.1**: Summary generation for pipeline
```gherkin
Given determination command completes successfully
When output files are generated
Then both determination.md and determination.summary.md shall exist
And determination.summary.md shall follow Key-Value Markdown format
And summary token count shall be ~500 tokens (±100)
And summary shall include:
  - Decision (YES/NO/CONDITIONAL)
  - Traffic Light (GREEN/YELLOW/RED)
  - FDA/EU MDR/MFDS Status
  - Key Factors
  - Escalation (Yes/No + reason)
  - Sources (Notion/Built-in/Context7)
```

**FS-006.2**: Auto-loading in pipeline
```gherkin
Given determination.summary.md exists at .aria/products/{product-name}/{date}/
When classify command is invoked without document
Then system shall auto-load determination.summary.md
And device characteristics shall be pre-populated from summary
And Q&A shall ask only for classification-specific missing fields
```

---

### FS-007: Graceful Degradation (SR-001)
**Requirement**: SR-001, Notion unavailable scenario
**Priority**: High

**Test Cases**:

**FS-007.1**: Notion DB unavailable, fallback to built-in
```gherkin
Given Notion DB connection fails or is unavailable
When determination command is invoked
Then system shall detect Notion unavailability
And system shall fallback to built-in knowledge (priority 2)
And Context7 shall be used for supplementation (priority 3)
And data source attribution shall indicate "Built-in + Context7"
And no user-facing error shall occur (graceful degradation)
```

**FS-007.2**: Context7 unavailable, built-in only
```gherkin
Given Notion DB unavailable
And Context7 MCP unavailable
When determination command is invoked
Then system shall use built-in knowledge only
And data source attribution shall indicate "Built-in only"
And determination shall proceed with reduced data sources
```

---

### FS-008: Traffic Light System Validation
**Requirement**: ER-002, ER-003, Traffic light criteria
**Priority**: High

**Test Cases**:

**FS-008.1**: GREEN - Clear determination
```gherkin
Given product is clearly a medical device (e.g., surgical scalpel)
When determination is performed
Then traffic light shall be GREEN
And no escalation shall be recommended
And user may proceed to classification
```

**FS-008.2**: YELLOW - Borderline case
```gherkin
Given product has borderline characteristics (wellness + medical claims)
When determination is performed
Then traffic light shall be YELLOW
And escalation shall be mandatory
And escalation reason shall be provided
And user shall be advised to consult regulatory specialist
```

**FS-008.3**: RED - Non-medical device
```gherkin
Given product is clearly not a medical device (e.g., consumer electronics)
When determination is performed
Then traffic light shall be RED
And determination status shall be "NO - Not a medical device"
And no medical device regulatory pathway shall be applicable
```

---

### FS-009: Multi-Product Selection (SR-006)
**Requirement**: SR-006, Active product context
**Priority**: Medium

**Test Cases**:

**FS-009.1**: Multiple products exist, selection menu
```gherkin
Given .aria/products/ contains 3 products:
- insulin-pump
- glucose-meter
- surgical-stapler
When determine command is invoked without product specification
Then system shall display product selection menu
And user shall select one product
And selected product shall be set as active in .aria/active_product.json
```

**FS-009.2**: Active product auto-load
```gherkin
Given .aria/active_product.json specifies "insulin-pump"
When determine command is invoked
Then system shall auto-load insulin-pump context
And no product selection menu shall be displayed
```

---

### FS-010: Output Versioning (SR-007)
**Requirement**: SR-007, Version management
**Priority**: Medium

**Test Cases**:

**FS-010.1**: Versioned output creation
```gherkin
Given determination.md already exists at .aria/products/{product-name}/{date}/
When determine command is invoked again with same product
Then system shall offer to create determination-v2.md
And user confirmation shall be requested
And if confirmed, versioned output shall be created
And original determination.md shall be preserved
```

---

## Test Execution Plan

### Automated vs Manual Testing

**Automated Tests (70%)**:
- Plugin recognition (PS-001)
- MCP configuration validation (PS-002)
- Determination skill logic (FS-001, FS-003)
- Classification skill logic (FS-003)
- Document extraction (FS-005.1, FS-005.2)
- Context Simplifier integration (FS-006)
- Graceful degradation (FS-007)
- Traffic light system (FS-008)

**Manual Tests (30%)**:
- README completeness review (PS-003)
- Large document handling (FS-005.3)
- Optimization analysis review (FS-004)
- Multi-product workflow (FS-009)
- Output versioning UX (FS-010)

### Priority Levels

1. **Critical (45%)**: Must pass for Phase 1-2 completion
   - Plugin recognition
   - MCP configuration
   - Determination and classification core logic
   - Document-first workflow
   - Context Simplifier integration
   - Graceful degradation

2. **High (35%)**: Important for user experience and quality
   - README completeness
   - Traffic light system
   - Escalation scenarios
   - Borderline cases

3. **Medium (20%)**: Nice-to-have, can be deferred
   - Optimization analysis
   - Multi-product selection
   - Output versioning

### Coverage Targets

- **Overall**: 85%+ coverage of Phase 1-2 acceptance criteria
- **Critical Tests**: 100% pass rate required
- **High Tests**: 90%+ pass rate required
- **Medium Tests**: 80%+ pass rate required

---

## Test Fixtures

Test fixtures are prepared in `.aria/test-fixtures/`:

### Sample Products (7)
1. **insulin-pump**: Active implantable device (Class III)
2. **glucose-meter**: IVD device (Class II)
3. **surgical-stapler**: Surgical instrument (Class II)
4. **fitness-tracker**: Borderline wellness device
5. **wheelchair**: Non-invasive mobility device (Class I)
6. **heart-valve**: Implantable life-sustaining device (Class III)
7. **contact-lens**: Short-term invasive device (Class IIa)

### Technical Documents (4 types)
1. **product-spec.pdf**: Complete specification with all fields
2. **ifu.pdf**: Instructions for Use with partial device description
3. **large-doc-with-toc.pdf**: 150-page document with Table of Contents
4. **scanned-ocr.pdf**: OCR-scanned document with potential extraction issues

### MCP Mock Scenarios
1. **notion-unavailable**: Notion DB connection failure
2. **context7-unavailable**: Context7 MCP unavailable
3. **all-mcp-unavailable**: All MCPs unavailable (built-in only)

### Expected Outputs (Golden Masters)
- Sample determination.md and determination.summary.md
- Sample classification.md and classification.summary.md
- Expected traffic light assessments
- Expected escalation recommendations

---

## Acceptance Criteria Mapping Summary

### Ubiquitous Requirements (UR)
- UR-001 to UR-006: Covered by PS-001 (plugin recognition), PS-002 (MCP validation)

### Event-Driven Requirements (ER)
- ER-002 (determine): FS-001, FS-002, FS-005, FS-007, FS-008
- ER-003 (classify): FS-003, FS-004, FS-006, FS-007, FS-008
- ER-009 (next steps): Integrated in FS-001, FS-003
- ER-011 (context): FS-006
- ER-012 (multi-format): FS-006 (markdown + summary)
- ER-013/014 (document): FS-005
- ER-015 (compression): FS-006
- ER-016 (stale data): FS-010

### State-Driven Requirements (SR)
- SR-001 (degradation): FS-007
- SR-006 (multi-product): FS-009
- SR-007 (versioning): FS-010

### Unwanted Behaviors (WR)
- WR-001 to WR-005: Covered by negative test cases throughout

### Quality Gates
- VALID framework: All test scenarios validate Verified, Accurate, Linked, Inspectable, Deliverable
- Quantitative targets: FS-006 (token budget), FS-005 (Q&A rounds)

---

## Success Metrics

- **Test Pass Rate**: 90%+ overall (100% for critical tests)
- **Coverage**: 85%+ of Phase 1-2 acceptance criteria
- **Defect Density**: <5 defects per 100 test cases
- **Execution Time**: Automated test suite <10 minutes
- **Documentation Quality**: All test cases have clear Given-When-Then structure

---

**Test Plan Version**: 1.0.0
**Last Updated**: 2026-02-10
**Author**: team-tester (ARIA Plugin Team)
