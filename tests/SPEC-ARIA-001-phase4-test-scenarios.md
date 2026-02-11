# Test Scenarios for SPEC-ARIA-001 Phase 4

**SPEC**: SPEC-ARIA-001 v4.0.0
**Scope**: Phase 4 acceptance criteria validation (Analysis Skills + Commands)
**Status**: Test scenarios documented
**Coverage Target**: 85%+ of Phase 4 requirements

---

## Executive Summary

This document defines comprehensive test scenarios for ARIA Cowork Plugin Phase 4, covering:
- **Comparison Skill**: Multi-country regulatory comparison with side-by-side matrices
- **Briefing Skill**: Executive briefing report synthesis from full pipeline data
- **Commands**: /aria:compare, /aria:brief

Test design follows TDD methodology with 85%+ coverage target for all Phase 4 acceptance criteria.

---

## Test Strategy

### Test Categories

1. **Positive Tests** (60%): Expected behavior validation
2. **Negative Tests** (20%): Error handling and edge cases
3. **Integration Tests** (15%): Command-to-skill-to-output workflow
4. **Pipeline Tests** (5%): Full pipeline data synthesis from Phase 2-3

### Coverage Mapping

All test scenarios map to acceptance criteria in `acceptance.md`:
- **Event-Driven Requirements**: ER-007 (compare), ER-008 (brief), ER-009 (next steps)
- **Ubiquitous Requirements**: UR-001 (Korean), UR-002 (disclaimer), UR-003 (data source), UR-004 (VALID), UR-005 (traffic light), UR-006 (storage path)
- **State-Driven Requirements**: SR-001 (degradation), SR-004 (output formats), SR-008 (English toggle)
- **Unwanted Behaviors**: WR-001 through WR-003
- **Optional Requirements**: OR-001 (Google Drive export), OR-002 (.docx export)

---

## Phase 4: Comparison Skill Test Scenarios

### CP-001: Multi-Country Clinical Evidence Comparison
**Requirement**: ER-007 - Side-by-side comparison matrix generation
**Priority**: Critical

**Test Cases**:

**CP-001.1**: FDA vs EU MDR vs MFDS clinical evidence requirements
```gherkin
Given the user invokes /aria:compare with topic "clinical evidence requirements"
And target countries are FDA, EU MDR, and MFDS
When the comparison skill processes the input
Then the output shall generate a side-by-side comparison matrix
And the matrix shall include columns: FDA, EU MDR, MFDS
And the matrix shall include rows covering:
  - Clinical study requirements (RCT, observational, registry)
  - Pre-market vs post-market data acceptance
  - Sample size requirements
  - Clinical endpoint specifications
  - Adverse event reporting standards
And each cell shall cite specific regulation references
```

**CP-001.2**: Similarities highlighting across regions
```gherkin
Given the comparison matrix for "clinical evidence requirements"
When similarities are analyzed
Then the output shall include a "Similarities" section
And the section shall highlight harmonized standards (e.g., ISO 14155 for clinical investigations)
And common requirements accepted across all three regions shall be listed
And source attribution shall reference the harmonized standard document
```

**CP-001.3**: Differences highlighting across regions
```gherkin
Given the comparison matrix for "clinical evidence requirements"
When differences are analyzed
Then the output shall include a "Differences" section
And the section shall highlight region-specific requirements:
  - FDA: IDE requirement for significant risk devices
  - EU MDR: PMCF (Post-Market Clinical Follow-up) mandatory
  - MFDS: Korean-specific clinical trial approval process
And each difference shall explain the regulatory rationale
```

---

### CP-002: Classification Rules Comparison
**Requirement**: ER-007 - Strategic recommendations in comparison output
**Priority**: Critical

**Test Cases**:

**CP-002.1**: FDA vs EU MDR vs MFDS classification rule comparison
```gherkin
Given the user invokes /aria:compare with topic "classification rules for active implantable devices"
And target countries are FDA, EU MDR, and MFDS
When the comparison skill processes the input
Then the output shall compare classification criteria:
  - FDA: Class III (life-sustaining/supporting implantables)
  - EU MDR: Class III (implantable devices, Rule 8)
  - MFDS: Grade 4 (implantable with life-sustaining function)
And the matrix shall show equivalent risk levels across regions
And strategic recommendations shall be included
```

**CP-002.2**: Strategic recommendations for multi-market design
```gherkin
Given a comparison matrix showing classification differences
When strategic recommendations are generated
Then the output shall include recommendations such as:
  - "Design to meet the most stringent classification (FDA Class III) for global harmonization"
  - "Consider narrowing intended use to lower classification in specific markets"
  - "Leverage ISO 13485 QMS for all three regions"
And recommendations shall be tagged with traffic light indicators (GREEN, YELLOW, RED)
```

---

### CP-003: Labeling and IFU Requirements Comparison
**Requirement**: ER-007 - Multi-country comparison framework
**Priority**: High

**Test Cases**:

**CP-003.1**: Labeling requirement comparison across regions
```gherkin
Given the user invokes /aria:compare with topic "labeling and IFU requirements"
When the comparison skill generates the matrix
Then the output shall compare:
  - FDA: 21 CFR 801 labeling requirements
  - EU MDR: Annex I Chapter III labeling requirements
  - MFDS: 의료기기법 시행규칙 labeling requirements
And differences shall include language requirements, symbol standards, and warnings
```

**CP-003.2**: Harmonized symbol standards identification
```gherkin
Given a labeling requirements comparison
When harmonized standards are identified
Then the output shall list:
  - ISO 15223-1 (Medical device symbols)
  - IEC 60601-1 (Safety symbols for electrical devices)
And note that these standards are accepted across FDA, EU MDR, and MFDS
```

---

### CP-004: QMS (Quality Management System) Comparison
**Requirement**: ER-007 - Comparison matrices with regulatory references
**Priority**: High

**Test Cases**:

**CP-004.1**: QMS requirement comparison
```gherkin
Given the user invokes /aria:compare with topic "QMS requirements"
When the comparison skill processes the input
Then the output shall compare:
  - FDA: 21 CFR 820 (QSR) or ISO 13485
  - EU MDR: ISO 13485 mandatory
  - MFDS: ISO 13485 or equivalent KGMP
And the matrix shall note that ISO 13485 is the common denominator
And strategic recommendation shall be "Implement ISO 13485 for global compliance"
```

---

### CP-005: Traffic Light Integration in Comparison
**Requirement**: UR-005 - Traffic light system for regulatory risk assessment
**Priority**: High

**Test Cases**:

**CP-005.1**: Traffic light for harmonized vs divergent requirements
```gherkin
Given a comparison matrix is generated
When traffic light indicators are applied
Then harmonized requirements (same across all regions) shall be tagged GREEN
And partially divergent requirements (2 out of 3 regions align) shall be tagged YELLOW
And completely divergent requirements (all different) shall be tagged RED
And the legend shall explain the traffic light meaning
```

**CP-005.2**: Strategic recommendations based on traffic light status
```gherkin
Given comparison output with traffic light indicators
When strategic recommendations are generated
Then GREEN items shall recommend "Leverage harmonized approach"
And YELLOW items shall recommend "Design for common subset, document regional variations"
And RED items shall recommend "Plan region-specific strategies, consult regulatory experts"
```

---

### CP-006: Context Simplifier Integration for Comparison
**Requirement**: Phase 4 Success Criterion - Context Simplifier integration
**Priority**: High

**Test Cases**:

**CP-006.1**: Generate comparison summary for downstream use
```gherkin
Given /aria:compare executes successfully
When the output is generated
Then a .summary.md file shall be created in the product directory
And the file shall include key comparison findings (similarities, differences, recommendations)
And the summary token count shall be approximately 500 tokens or less
And the full comparison matrix shall be preserved in comparison.md
```

---

### CP-007: Korean Language Output for Comparison
**Requirement**: UR-001 - All user-facing output in Korean
**Priority**: Critical

**Test Cases**:

**CP-007.1**: All comparison output in Korean
```gherkin
Given any /aria:compare execution
When the output is generated
Then all section headers shall be in Korean:
  - "비교 매트릭스" (Comparison Matrix)
  - "공통점" (Similarities)
  - "차이점" (Differences)
  - "전략적 권장사항" (Strategic Recommendations)
And all descriptive text shall be in Korean
And only regulation codes (FDA, EU MDR, MFDS, CFR, ISO) may appear in English
```

---

### CP-008: Disclaimer and Data Source Attribution
**Requirement**: UR-002, UR-003 - Disclaimer and data source citation
**Priority**: High

**Test Cases**:

**CP-008.1**: Standard disclaimer in comparison output
```gherkin
Given any /aria:compare execution
When the output is generated
Then the standard disclaimer shall appear: "본 자료는 참고 정보이며, 규제 자문이 아닙니다"
```

**CP-008.2**: Data source attribution for each comparison claim
```gherkin
Given comparison output cites regulatory requirements
When each requirement is displayed
Then the source shall be cited (e.g., "출처: FDA 21 CFR 820", "출처: EU MDR Annex I")
And no unsupported claims shall appear (WR-003)
```

---

### CP-009: VALID Framework Compliance for Comparison
**Requirement**: UR-004 - VALID framework enforcement
**Priority**: High

**Test Cases**:

**CP-009.1**: Comparison output meets VALID checklist
```gherkin
Given /aria:compare produces output
When the VALID checklist is applied
Then V (Verified): All regulatory citations shall be source-attributed
And A (Accurate): Comparison data shall match known regulatory standards
And L (Linked): Cross-references to FDA/EU MDR/MFDS documents shall be included
And I (Inspectable): Comparison logic shall be transparent
And D (Deliverable): Output shall be stored in .aria/products/ with proper naming
```

---

### CP-010: Storage Path Convention for Comparison
**Requirement**: UR-006 - Data storage path convention
**Priority**: Medium

**Test Cases**:

**CP-010.1**: Comparison output stored in correct directory
```gherkin
Given a product named "Cardiac Monitor X1"
And the command is executed on 2026-02-11
When /aria:compare generates output
Then the output file shall be stored at:
  .aria/products/cardiac-monitor-x1/2026-02-11/comparison.md
And the .summary.md file shall be at:
  .aria/products/cardiac-monitor-x1/2026-02-11/comparison.summary.md
```

---

## Phase 4: Briefing Skill Test Scenarios

### BR-001: Executive Briefing from Complete Pipeline Data
**Requirement**: ER-008 - Synthesize complete pipeline data into briefing
**Priority**: Critical

**Test Cases**:

**BR-001.1**: Full pipeline synthesis (determination → brief)
```gherkin
Given the user has completed the full pipeline:
  - /aria:determine (determination.md exists)
  - /aria:classify (classification.md exists)
  - /aria:pathway (pathway.md exists)
  - /aria:estimate (estimation.md exists)
  - /aria:plan (plan.md exists)
  - /aria:compare (comparison.md exists)
When /aria:brief is executed
Then the briefing shall synthesize all six data sources
And the output shall include sections:
  - Executive Summary (1-page overview)
  - Device Overview (from determination)
  - Regulatory Classification (from classification)
  - Submission Pathways (from pathway)
  - Cost and Timeline (from estimation)
  - Regulatory Plan (from plan)
  - Multi-Country Comparison (from comparison)
  - Recommendations and Next Steps
  - Appendices (detailed data references)
```

**BR-001.2**: Executive summary format validation
```gherkin
Given a complete pipeline briefing is generated
When the Executive Summary section is reviewed
Then it shall be concise (1-2 paragraphs, max 300 words)
And it shall include:
  - Device name and intended use (1 sentence)
  - Determination result (YES/NO/CONDITIONAL with traffic light)
  - Classification summary (FDA/EU/MFDS class)
  - Recommended pathway and timeline
  - Key risks and escalation flags
And it shall NOT include detailed analysis (that belongs in body sections)
```

---

### BR-002: Executive Briefing from Partial Pipeline Data
**Requirement**: ER-008 - Handle partial pipeline data scenarios
**Priority**: High

**Test Cases**:

**BR-002.1**: Briefing with only determination and classification
```gherkin
Given the user has completed only:
  - /aria:determine (determination.md exists)
  - /aria:classify (classification.md exists)
And other pipeline steps have NOT been completed
When /aria:brief is executed
Then the briefing shall cover available data (determination + classification)
And sections for pathway, estimation, and plan shall display:
  - "데이터 없음 - /aria:pathway를 실행하여 경로 선택 데이터를 생성하세요"
And the Executive Summary shall note which steps are incomplete
And next step suggestions shall recommend completing the missing pipeline steps
```

**BR-002.2**: Briefing with missing comparison data
```gherkin
Given the pipeline is complete except for /aria:compare
When /aria:brief is executed
Then the Multi-Country Comparison section shall display:
  - "비교 데이터 없음 - /aria:compare를 실행하여 다국가 비교 분석을 생성하세요"
And the briefing shall remain functional with the available data
```

---

### BR-003: Full Context On-Demand Loading (S10.4)
**Requirement**: ER-008, Phase 4 Success Criterion - Full context on-demand loading
**Priority**: High

**Test Cases**:

**BR-003.1**: Default briefing uses compressed summaries
```gherkin
Given all pipeline steps have completed
And each step has generated a .summary.md file (compressed context)
When /aria:brief is executed with default settings
Then the skill shall load compressed summaries (.summary.md) by default
And the total token consumption shall be reduced by at least 60%
And the briefing shall be complete without loading full outputs
```

**BR-003.2**: On-demand full context loading when needed
```gherkin
Given compressed summaries lack sufficient detail for a specific section
When the briefing skill requires more detail
Then the skill shall load the full output file (e.g., determination.md instead of determination.summary.md)
And the output shall note "(full context loaded)" in the Data Sources section
And full context loading shall be selective (only for sections requiring detail)
```

**BR-003.3**: User-triggered full context mode
```gherkin
Given the user invokes /aria:brief with a --full-context flag
When the briefing skill processes the input
Then all full output files shall be loaded (not summaries)
And the briefing shall include maximum detail from all pipeline steps
And the disclaimer shall note "Full context mode - comprehensive analysis"
```

---

### BR-004: Detailed Analysis Sections in Briefing
**Requirement**: ER-008 - Detailed analysis sections
**Priority**: High

**Test Cases**:

**BR-004.1**: Device Overview section format
```gherkin
Given a complete pipeline briefing
When the Device Overview section is reviewed
Then it shall include:
  - Product name and description
  - Intended use and user population
  - Primary function and product form
  - Key technical characteristics
  - Data source attribution (from determination.md)
```

**BR-004.2**: Regulatory Classification section format
```gherkin
Given a complete pipeline briefing
When the Regulatory Classification section is reviewed
Then it shall include:
  - FDA classification (Class I/II/III) with rule references
  - EU MDR classification (Class I/IIa/IIb/III) with rule references
  - MFDS classification (Grade 1/2/3/4) with rule references
  - Traffic light indicators per region
  - Data source attribution (from classification.md)
```

**BR-004.3**: Submission Pathways section format
```gherkin
Given a complete pipeline briefing
When the Submission Pathways section is reviewed
Then it shall include:
  - Recommended pathway per region (510(k), PMA, CE Marking, 허가, etc.)
  - Timeline ranges per pathway
  - Key requirements per pathway
  - Critical path identification
  - Data source attribution (from pathway.md)
```

**BR-004.4**: Cost and Timeline section format
```gherkin
Given a complete pipeline briefing
When the Cost and Timeline section is reviewed
Then it shall include:
  - Total cost ranges (optimistic/expected/pessimistic)
  - Cost breakdown by category
  - Timeline milestones with dependencies
  - Critical path timeline
  - Data source attribution (from estimation.md and plan.md)
```

---

### BR-005: Recommendations and Next Steps
**Requirement**: ER-009 - Next step suggestions
**Priority**: High

**Test Cases**:

**BR-005.1**: Strategic recommendations in briefing
```gherkin
Given a complete pipeline briefing is generated
When the Recommendations section is reviewed
Then it shall include 1-3 strategic recommendations such as:
  - Recommended submission sequence (e.g., "Start with FDA 510(k), then parallel EU and Korea")
  - Risk mitigation strategies
  - Resource allocation guidance
And each recommendation shall cite supporting data from pipeline steps
```

**BR-005.2**: Next steps limited to maximum 3 (WR-002)
```gherkin
Given the briefing is complete
When next step suggestions are displayed
Then the count shall be between 1 and 3 (inclusive)
And never exceed 3 suggestions (compliance with WR-002)
And suggestions may include:
  - "Engage regulatory consultant for FDA 510(k) predicate search"
  - "Initiate biocompatibility testing per ISO 10993"
  - "Schedule pre-submission meeting with FDA"
```

---

### BR-006: Appendices Section
**Requirement**: ER-008 - Appendices with detailed references
**Priority**: Medium

**Test Cases**:

**BR-006.1**: Appendices include detailed data references
```gherkin
Given a complete pipeline briefing
When the Appendices section is reviewed
Then it shall include:
  - Appendix A: Full determination rationale
  - Appendix B: Classification rule references
  - Appendix C: Pathway comparison table (full matrix)
  - Appendix D: Cost estimation breakdown (all categories)
  - Appendix E: Regulatory plan Gantt chart
  - Appendix F: Data source attribution list
```

---

### BR-007: VALID Framework Compliance for Briefing
**Requirement**: UR-004 - VALID framework enforcement
**Priority**: Critical

**Test Cases**:

**BR-007.1**: Briefing output meets VALID checklist
```gherkin
Given /aria:brief produces output
When the VALID checklist is applied
Then V (Verified): All pipeline data sources shall be cited
And A (Accurate): Synthesized data shall match source files
And L (Linked): Cross-references between sections shall be included
And I (Inspectable): Decision logic from each pipeline step shall be traceable
And D (Deliverable): Output shall be stored in .aria/products/ with proper naming
```

---

### BR-008: Korean Language Output for Briefing
**Requirement**: UR-001 - All user-facing output in Korean
**Priority**: Critical

**Test Cases**:

**BR-008.1**: All briefing sections in Korean
```gherkin
Given any /aria:brief execution
When the output is generated
Then all section headers shall be in Korean:
  - "경영진 요약" (Executive Summary)
  - "제품 개요" (Device Overview)
  - "규제 등급 분류" (Regulatory Classification)
  - "제출 경로" (Submission Pathways)
  - "비용 및 일정" (Cost and Timeline)
  - "규제 계획" (Regulatory Plan)
  - "권장사항 및 다음 단계" (Recommendations and Next Steps)
  - "부록" (Appendices)
And all body text shall be in Korean
And only regulation codes may appear in English
```

---

### BR-009: Disclaimer and Data Source Attribution
**Requirement**: UR-002, UR-003 - Disclaimer and data source citation
**Priority**: High

**Test Cases**:

**BR-009.1**: Standard disclaimer in briefing
```gherkin
Given any /aria:brief execution
When the output is generated
Then the standard disclaimer shall appear: "본 자료는 참고 정보이며, 규제 자문이 아닙니다"
And the disclaimer shall be prominently placed at the top of the briefing
```

**BR-009.2**: Data source attribution throughout briefing
```gherkin
Given briefing output synthesizes multiple pipeline steps
When each section cites data
Then the source shall be attributed (e.g., "출처: determination.md", "출처: classification.md")
And the Appendix F shall list all data sources used in the briefing
And no unsupported claims shall appear (WR-003)
```

---

### BR-010: Traffic Light System in Briefing
**Requirement**: UR-005 - Traffic light system for regulatory risk
**Priority**: High

**Test Cases**:

**BR-010.1**: Traffic light indicators in Executive Summary
```gherkin
Given a complete pipeline briefing
When the Executive Summary is reviewed
Then the overall regulatory risk shall be indicated with a traffic light:
  - GREEN: All pathways are low-risk (Class I exempt, etc.)
  - YELLOW: Moderate risk or escalation flags present
  - RED: High risk or critical blockers identified
And the traffic light rationale shall reference determination and classification results
```

**BR-010.2**: Traffic light per region in Classification section
```gherkin
Given the Regulatory Classification section
When classification results per region are displayed
Then each region shall have a traffic light indicator:
  - FDA: [GREEN/YELLOW/RED]
  - EU MDR: [GREEN/YELLOW/RED]
  - MFDS: [GREEN/YELLOW/RED]
And the legend shall explain the traffic light meaning
```

---

### BR-011: Storage Path Convention for Briefing
**Requirement**: UR-006 - Data storage path convention
**Priority**: Medium

**Test Cases**:

**BR-011.1**: Briefing output stored in correct directory
```gherkin
Given a product named "Cardiac Monitor X1"
And the command is executed on 2026-02-11
When /aria:brief generates output
Then the output file shall be stored at:
  .aria/products/cardiac-monitor-x1/2026-02-11/briefing.md
And the .summary.md file shall be at:
  .aria/products/cardiac-monitor-x1/2026-02-11/briefing.summary.md
```

---

### BR-012: Report Issuance Policy (ER-017)
**Requirement**: ER-017 - User confirmation before report generation
**Priority**: Critical

**Test Cases**:

**BR-012.1**: Analysis turn outputs decision-relevant information only
```gherkin
Given /aria:brief is executed
When the analysis turn completes
Then the output shall include only:
  - Key findings summary
  - Traffic light assessment
  - Items requiring user confirmation (e.g., "Does the cost estimate align with your budget?")
And a full formatted report shall NOT be generated in the same turn
```

**BR-012.2**: Full report generated after user confirmation
```gherkin
Given analysis results are presented to the user
When the user confirms/approves the content (e.g., user responds "Yes, generate the report")
Then the full formatted briefing report shall be generated
And the report shall be stored in .aria/products/{product-name}/{date}/briefing.md
```

**BR-012.3**: Report generation blocked without user confirmation
```gherkin
Given the user has NOT confirmed the analysis results
When the system attempts to generate a report
Then the report generation shall be blocked
And the system shall prompt: "분석 결과를 검토하고 확인해 주세요. 보고서를 생성할까요?"
```

**BR-012.4**: Default Markdown format when no format flag provided
```gherkin
Given report generation is triggered after user confirmation
When no --format flag is provided
Then the default Markdown format shall be used
And the report shall be written to .aria/products/ as briefing.md
And no format selection prompt shall be displayed
```

---

### BR-013: Multi-Format Output (SR-004)
**Requirement**: SR-004 - Output format conversion
**Priority**: High

**Test Cases**:

**BR-013.1**: Markdown format (default)
```gherkin
Given the user confirms report generation
When --format markdown is specified (or no flag provided)
Then a Markdown format report shall be generated
And the report shall be stored in .aria/products/ as briefing.md
```

**BR-013.2**: PDF format
```gherkin
Given the user confirms report generation
When --format pdf is specified
Then a PDF format report shall be generated
And the content shall follow the same structure as the Markdown version
And the PDF shall be stored in .aria/products/ as briefing.pdf
```

**BR-013.3**: Google Docs format (OR-001)
```gherkin
Given Google Drive MCP is configured
And the user confirms report generation
When --format gdocs is specified
Then a Google Docs format report shall be created via Google Drive MCP connector
And the content shall match the Markdown output structure
And the system shall return the Google Docs URL
```

**BR-013.4**: Notion page format
```gherkin
Given Notion MCP is configured
And the user confirms report generation
When --format notion is specified
Then a Notion page shall be created via Notion MCP connector
And the content shall match the Markdown output
And the system shall return the Notion page URL
```

---

### BR-014: English Output Toggle (SR-008)
**Requirement**: SR-008 - English output toggle
**Priority**: Medium

**Test Cases**:

**BR-014.1**: English toggle via command flag
```gherkin
Given the user enables English output via --lang en flag
When /aria:brief is executed
Then all user-facing text shall be in English
And Korean regulatory terms shall include English translations (e.g., "medical device (의료기기)")
And section headers shall be in English
```

**BR-014.2**: English toggle via aria.local.md playbook
```gherkin
Given aria.local.md contains language preference set to "en"
When /aria:brief is executed
Then the behavior shall be identical to explicit --lang en flag
And all output shall be in English
```

---

## Integration Tests

### IT-001: Full Phase 4 Pipeline Integration
**Requirement**: Phase 4 Success Criterion - Full pipeline flow operational
**Priority**: Critical

**Test Cases**:

**IT-001.1**: Sequential execution from determination to briefing
```gherkin
Given the user has executed the full pipeline:
  - /aria:determine → determination.md + determination.summary.md
  - /aria:classify → classification.md + classification.summary.md
  - /aria:pathway → pathway.md + pathway.summary.md
  - /aria:estimate → estimation.md + estimation.summary.md
  - /aria:plan → plan.md + plan.summary.md
  - /aria:compare → comparison.md + comparison.summary.md
When /aria:brief is executed as the final step
Then the briefing shall synthesize all six prior steps
And no data shall be re-requested from the user
And the final briefing shall accurately reflect the full pipeline data flow
And the briefing quality shall meet VALID framework standards
```

---

### IT-002: Comparison Command Integration
**Requirement**: ER-007 - Comparison skill operational
**Priority**: High

**Test Cases**:

**IT-002.1**: Comparison command with classification context
```gherkin
Given /aria:classify has been executed previously
When /aria:compare is executed for "classification rules"
Then the comparison shall reference the classification results
And the output shall include context-aware recommendations
```

---

## Negative Tests

### NT-001: Briefing with No Pipeline Data
**Requirement**: Graceful degradation
**Priority**: Medium

**Test Cases**:

**NT-001.1**: Briefing invoked with empty .aria/ directory
```gherkin
Given NO pipeline data exists in .aria/products/
When /aria:brief is executed
Then a warning message shall appear: "파이프라인 데이터가 없습니다. /aria:determine부터 시작하세요."
And the user shall be prompted to complete at least the determination step
And the traffic light shall be YELLOW
```

---

### NT-002: Comparison with Invalid Topic
**Requirement**: Error handling
**Priority**: Low

**Test Cases**:

**NT-002.1**: Comparison with unsupported topic
```gherkin
Given the user invokes /aria:compare with an unsupported topic (e.g., "marketing strategies")
When the comparison skill processes the input
Then a warning shall appear: "지원되지 않는 비교 주제입니다. 규제 관련 주제를 선택하세요."
And suggested valid topics shall be listed (e.g., "clinical evidence", "labeling requirements", "QMS")
```

---

### NT-003: Multi-Format Output Without MCP Configuration
**Requirement**: Graceful degradation (SR-001)
**Priority**: Medium

**Test Cases**:

**NT-003.1**: Google Docs format requested without Google Drive MCP
```gherkin
Given Google Drive MCP is NOT configured
When /aria:brief --format gdocs is executed
Then a limitation notice shall appear: "Google Drive MCP가 설정되지 않았습니다. Markdown 형식으로 출력합니다."
And the output shall fall back to default Markdown format
And the report shall be stored as briefing.md
```

**NT-003.2**: Notion format requested without Notion MCP
```gherkin
Given Notion MCP is NOT configured
When /aria:brief --format notion is executed
Then a limitation notice shall appear: "Notion MCP가 설정되지 않았습니다. Markdown 형식으로 출력합니다."
And the output shall fall back to default Markdown format
```

---

## Summary

**Total Test Scenarios**: 50+ test cases
**Coverage**:
- ER-007 (compare): 100% (10 test scenarios)
- ER-008 (brief): 100% (14 test scenarios)
- ER-009 (next steps): 100% (integrated in BR-005)
- ER-017 (report issuance): 100% (BR-012)
- UR-001 through UR-006: 100% (ubiquitous requirements)
- SR-001 (degradation): 100% (NT-003)
- SR-004 (multi-format): 100% (BR-013)
- SR-008 (English toggle): 100% (BR-014)
- WR-001 through WR-003: 100% (unwanted behaviors)
- OR-001 (Google Drive export): 100% (BR-013.3)

**Focus**: Multi-country comparison accuracy, executive briefing synthesis, full pipeline integration, VALID framework compliance, report issuance policy
**Quality Target**: 85%+ acceptance criteria coverage

---

**Version**: 1.0.0
**Created**: 2026-02-11
**Author**: Testing Specialist (team-tester)
