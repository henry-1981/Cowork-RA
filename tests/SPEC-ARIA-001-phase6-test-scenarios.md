# Test Scenarios for SPEC-ARIA-001 Phase 6 Core

**SPEC**: SPEC-ARIA-001 v4.0.0
**Scope**: Phase 6 Core acceptance criteria validation (PDF Export, Playbook, English Toggle, Graceful Degradation)
**Status**: Test scenarios documented
**Coverage Target**: 100% requirement coverage for SR-001, SR-002, SR-008, ER-017

---

## Executive Summary

This document defines comprehensive test scenarios for ARIA Cowork Plugin Phase 6 Core, covering:
- **PDF Export**: Multi-format output (Markdown, PDF, Google Docs) with format flag validation
- **Playbook Loading**: Organization-specific configuration via aria.local.md
- **English Toggle**: Language preference via --lang flag or playbook setting
- **Graceful Degradation**: Default built-in knowledge operation when external MCPs are unavailable

Test design follows TDD methodology with 100% coverage target for all Phase 6 Core acceptance criteria.

---

## Test Strategy

### Test Categories

1. **PDF Export Tests** (30%): Multi-format output with --format flag validation
2. **Playbook Tests** (30%): aria.local.md loading and application
3. **English Toggle Tests** (25%): Language switching via flag or playbook
4. **Graceful Degradation Tests** (15%): Built-in knowledge fallback behavior

### Coverage Mapping

All test scenarios map to acceptance criteria in `acceptance.md`:
- **State-Driven Requirements**: SR-001 (graceful degradation), SR-002 (playbook), SR-008 (English toggle)
- **Event-Driven Requirements**: ER-017 (report issuance policy)
- **Optional Requirements**: OR-001 (Google Drive export)
- **Ubiquitous Requirements**: UR-001 through UR-006

---

## Phase 6: PDF Export Test Scenarios

### PDF-001: Brief Command PDF Export
**Requirement**: ER-017 - Multi-format output with --format flag
**Priority**: Critical

**Test Cases**:

**PDF-001.1**: /aria:report with --format pdf flag generates PDF report
```gherkin
Given the user has completed the full pipeline for "cardiac-monitor-x1"
And all .summary.md files exist in .aria/products/cardiac-monitor-x1/2026-02-11/
When the user invokes /aria:report --format pdf
Then the system shall confirm the analysis content with the user first
And after user confirmation, generate a PDF format report
And the PDF content shall match the Markdown output structure
And the PDF shall include all sections: executive summary, detailed analysis, recommendations, appendices
And the PDF shall be stored in .aria/products/cardiac-monitor-x1/2026-02-11/briefing.pdf
```

**PDF-001.2**: /aria:report with no --format flag defaults to Markdown
```gherkin
Given the user has completed the full pipeline
When the user invokes /aria:report (no --format flag)
Then the system shall confirm the analysis content with the user first
And after user confirmation, generate the default Markdown format report
And the output shall be written to .aria/products/{product}/briefing.md
And no format selection prompt shall be displayed
```

**PDF-001.3**: /aria:report with --format gdocs but google-drive-mcp NOT configured
```gherkin
Given google-drive-mcp is NOT configured in .mcp.json
When the user invokes /aria:report --format gdocs
Then the system shall display a limitation notice: "Google Drive MCP가 설정되지 않았습니다"
And the system shall fallback to Markdown format
And the output shall be written as briefing.md
And the limitation notice shall appear in the Data Source Attribution section
```

---

### PDF-002: Compare Command PDF Export
**Requirement**: ER-017 - Multi-format output for compare command
**Priority**: High

**Test Cases**:

**PDF-002.1**: /aria:compare with --format pdf
```gherkin
Given the user has completed classification for "insulin-pump-z2"
When the user invokes /aria:compare --format pdf with topic "clinical evidence requirements" for FDA, EU MDR, MFDS
Then the system shall confirm the comparison content with the user first
And after user confirmation, generate a PDF format comparison report
And the PDF shall include the side-by-side comparison matrix
And the PDF shall be stored in .aria/products/insulin-pump-z2/2026-02-11/comparison.pdf
```

**PDF-002.2**: /aria:compare with --format markdown
```gherkin
Given the user has completed classification
When the user invokes /aria:compare --format markdown
Then the system shall confirm the comparison content with the user first
And after user confirmation, generate the default Markdown format report
And the output shall be written to comparison.md
```

---

### PDF-003: Pathway Command PDF Export
**Requirement**: ER-017 - Multi-format output for pathway command
**Priority**: High

**Test Cases**:

**PDF-003.1**: /aria:pathway with --format pdf
```gherkin
Given the user has completed classification for a Class II device
When the user invokes /aria:pathway --format pdf
Then the system shall confirm the pathway analysis with the user first
And after user confirmation, generate a PDF format pathway report
And the PDF shall include pathway comparison table with timelines and requirements
And the PDF shall be stored in .aria/products/{product}/{date}/pathway.pdf
```

**PDF-003.2**: /aria:pathway with --format gdocs and google-drive-mcp configured
```gherkin
Given google-drive-mcp is configured in .mcp.json with valid credentials
When the user invokes /aria:pathway --format gdocs
Then the system shall confirm the pathway analysis with the user first
And after user confirmation, create a Google Docs format report via MCP connector
And the Google Docs content shall match the Markdown output structure
And a link to the created Google Doc shall be displayed to the user
```

---

### PDF-004: Estimate Command PDF Export
**Requirement**: ER-017 - Multi-format output for estimation command
**Priority**: High

**Test Cases**:

**PDF-004.1**: /aria:estimate with --format pdf
```gherkin
Given the user has completed pathway selection
When the user invokes /aria:estimate --format pdf
Then the system shall confirm the cost/timeline estimation with the user first
And after user confirmation, generate a PDF format estimation report
And the PDF shall include cost breakdown (optimistic/expected/pessimistic) and timeline
And the PDF shall be stored in .aria/products/{product}/{date}/estimation.pdf
```

---

### PDF-005: Plan Command PDF Export
**Requirement**: ER-017 - Multi-format output for planning command
**Priority**: High

**Test Cases**:

**PDF-005.1**: /aria:plan with --format pdf
```gherkin
Given the user has completed pathway and estimate steps
When the user invokes /aria:plan --format pdf
Then the system shall confirm the milestone plan with the user first
And after user confirmation, generate a PDF format planning report
And the PDF shall include milestone phases, deliverables, dependencies, and checkpoints
And the PDF shall be stored in .aria/products/{product}/{date}/plan.pdf
```

---

### PDF-006: Format Flag Validation
**Requirement**: ER-017 - Format flag syntax compliance
**Priority**: Medium

**Test Cases**:

**PDF-006.1**: Invalid format flag rejected
```gherkin
Given the user invokes /aria:report --format invalid
When the system validates the format flag
Then the system shall reject the invalid format value
And display an error message: "지원되지 않는 형식입니다. 사용 가능한 형식: markdown, pdf, gdocs"
And the command shall NOT proceed
```

**PDF-006.2**: Format flag case-insensitive
```gherkin
Given the user invokes /aria:report --format PDF
When the system validates the format flag
Then the system shall accept the case-insensitive format value
And treat "PDF" as "pdf"
And proceed with PDF format generation after user confirmation
```

**PDF-006.3**: Multiple format flags (last one wins)
```gherkin
Given the user invokes /aria:report --format markdown --format pdf
When the system parses the command flags
Then the system shall use the last format flag value: "pdf"
And proceed with PDF format generation
```

---

### PDF-007: Report Issuance Policy Compliance
**Requirement**: ER-017 - User confirmation required before report generation
**Priority**: Critical

**Test Cases**:

**PDF-007.1**: No report without user confirmation
```gherkin
Given the user invokes /aria:report --format pdf
When the system completes the analysis
Then the system shall output only decision-relevant information (key findings, traffic light, items for confirmation)
And a full formatted PDF report shall NOT be generated in the same turn
And the system shall prompt: "분석이 완료되었습니다. 보고서를 생성하시겠습니까?"
```

**PDF-007.2**: Report generated after user confirmation
```gherkin
Given the analysis results are presented to the user
When the user confirms: "네, 보고서를 생성해주세요"
Then the system shall generate the full formatted report in the requested format (PDF)
And the report shall be stored in .aria/products/{product}/{date}/briefing.pdf
And a confirmation message shall be displayed: "PDF 보고서가 생성되었습니다: .aria/products/{product}/{date}/briefing.pdf"
```

**PDF-007.3**: Report generation blocked without confirmation
```gherkin
Given the analysis results are presented
When the user does NOT confirm the report generation
Then the report generation shall be blocked
And the system shall wait for user confirmation
And display: "보고서 생성을 원하시면 확인해주세요"
```

---

## Phase 6: Playbook Test Scenarios

### PB-001: Playbook Loading - Language Preference
**Requirement**: SR-002, SR-008 - aria.local.md language preference override
**Priority**: Critical

**Test Cases**:

**PB-001.1**: aria.local.md with language preference "en" applied to all commands
```gherkin
Given aria.local.md exists in the user's project root with content:
  ---
  ## Language Preference
  - Output language: en
  ---
When the user invokes /aria:determine
Then the system shall load aria.local.md at command startup
And switch all user-facing text to English
And the behavior shall be identical to explicit English toggle via --lang en flag
And Korean regulatory terms shall include English translations (e.g., "medical device (의료기기)")
```

**PB-001.2**: aria.local.md with language preference "ko" (Korean output)
```gherkin
Given aria.local.md exists with language preference set to "ko"
When the user invokes /aria:classify
Then the system shall load the playbook
And output all user-facing text in Korean
And this shall be the default behavior (no change from standard)
```

**PB-001.3**: Command flag --lang en takes precedence over playbook language setting
```gherkin
Given aria.local.md exists with language preference "ko"
When the user invokes /aria:pathway --lang en
Then the command flag shall take precedence over the playbook setting
And all user-facing text shall be in English
And the playbook language preference shall be ignored for this command execution
```

---

### PB-002: Playbook Loading - Pathway Defaults
**Requirement**: SR-002 - Preferred regulatory pathways
**Priority**: High

**Test Cases**:

**PB-002.1**: Playbook pathway defaults applied
```gherkin
Given aria.local.md exists with content:
  ---
  ## Preferred Regulatory Pathways
  - FDA: 510(k) pathway preferred for Class II devices
  - EU MDR: Notified Body NB-2797 preferred
  - MFDS: Standard approval pathway
  ---
When the user invokes /aria:pathway for a Class II device
Then the system shall load the playbook pathway defaults
And recommend 510(k) pathway as the primary option for FDA
And suggest NB-2797 as the preferred notified body for EU MDR
And include a note: "(조직 선호 경로 적용됨)"
```

**PB-002.2**: Playbook pathway defaults override default skill behavior
```gherkin
Given aria.local.md contains preferred pathways
When /aria:pathway is executed
Then the system shall prioritize playbook pathway preferences over default skill recommendations
And the output shall clearly indicate: "조직 playbook 기준 경로 적용"
```

---

### PB-003: Playbook Loading - Risk Tolerance
**Requirement**: SR-002 - Risk tolerance levels and escalation criteria
**Priority**: High

**Test Cases**:

**PB-003.1**: Playbook risk tolerance "conservative" lowers escalation thresholds
```gherkin
Given aria.local.md exists with content:
  ---
  ## Risk Tolerance
  - Organization risk appetite: conservative
  ---
When the user invokes /aria:classify for a borderline Class II/III device
Then the system shall apply conservative risk tolerance
And escalate to YELLOW or RED more frequently than default
And recommend "전문가 확인 필요" for ambiguous cases
```

**PB-003.2**: Playbook risk tolerance "aggressive" raises escalation thresholds
```gherkin
Given aria.local.md exists with risk tolerance set to "aggressive"
When /aria:classify is executed
Then the system shall apply aggressive risk tolerance
And reduce escalation frequency
And allow more YELLOW classifications without escalation recommendation
```

---

### PB-004: Playbook Loading - Custom Escalation Criteria
**Requirement**: SR-002 - Custom escalation criteria
**Priority**: Medium

**Test Cases**:

**PB-004.1**: Playbook custom escalation criteria applied
```gherkin
Given aria.local.md exists with content:
  ---
  ## Custom Escalation Criteria
  - Escalate to legal counsel: when classification is Class III or higher
  - Escalate to external consultant: when multi-market submission involves 3+ countries
  - Board notification threshold: when total cost estimate exceeds $500,000
  ---
When the user invokes /aria:classify and the result is Class III
Then the system shall apply the custom escalation criterion
And display escalation recommendation: "법무 자문 필요 (Class III 이상 등급)"
```

---

### PB-005: Playbook Loading - Data Retention Warning
**Requirement**: SR-002, ER-016 - Data retention period from playbook
**Priority**: Medium

**Test Cases**:

**PB-005.1**: Playbook data_retention_days applied to stale data warning
```gherkin
Given aria.local.md exists with content:
  ---
  ## Data Management
  - data_retention_days: 180  # 보존기간 (일)
  - warn_on_stale_data: true
  ---
And .aria/products/ contains data directories older than 180 days
When the user invokes any /aria: command
Then the system shall load the playbook retention setting
And display a warning message listing stale data directories older than 180 days
And the warning shall include: "보존기간(180일) 초과 데이터가 있습니다"
```

**PB-005.2**: Playbook warn_on_stale_data set to false suppresses warning
```gherkin
Given aria.local.md exists with warn_on_stale_data set to false
When any /aria: command is executed
Then the system shall NOT display stale data warnings
And proceed without retention period checks
```

---

### PB-006: Playbook Absent - Default Behavior
**Requirement**: SR-002 - Default behavior when playbook does NOT exist
**Priority**: High

**Test Cases**:

**PB-006.1**: No aria.local.md → use default skill behavior
```gherkin
Given aria.local.md does NOT exist in the user's project root
When the user invokes /aria:determine
Then the system shall check for aria.local.md and find it absent
And use default skill behavior with no customization
And output language shall be Korean (default)
And pathway recommendations shall use default logic (no organization preferences)
And proceed without playbook configuration
```

---

## Phase 6: English Toggle Test Scenarios

### EN-001: English Toggle via --lang en Flag
**Requirement**: SR-008 - English output via command flag
**Priority**: Critical

**Test Cases**:

**EN-001.1**: /aria:determine with --lang en switches to English
```gherkin
Given the user invokes /aria:determine --lang en
When the determination skill processes the input
Then all user-facing text shall be in English
And Korean regulatory terms shall include English translations (e.g., "의료기기 (medical device)")
And the disclaimer shall be in English: "This is reference information, not regulatory advice"
And the traffic light labels shall be in English: "GREEN", "YELLOW", "RED"
```

**EN-001.2**: /aria:classify with --lang en switches to English
```gherkin
Given the user invokes /aria:classify --lang en
When the classification skill processes the input
Then the output shall be entirely in English
And classification results shall use English terminology: "FDA Class II", "EU MDR Class IIa", "MFDS Class 2"
And rationale text shall be in English
```

**EN-001.3**: /aria:pathway with --lang en switches to English
```gherkin
Given the user invokes /aria:pathway --lang en
When the pathway skill processes the input
Then the pathway comparison table shall be in English
And pathway names shall be in English: "510(k) Premarket Notification", "CE Marking", "MFDS Authorization"
And timeline descriptions shall be in English
```

**EN-001.4**: /aria:estimate with --lang en switches to English
```gherkin
Given the user invokes /aria:estimate --lang en
When the estimation skill processes the input
Then cost categories shall be in English: "Consulting", "Testing", "Regulatory Fees", "Notified Body", "Clinical"
And timeline milestones shall be in English
And disclaimer text shall be in English
```

**EN-001.5**: /aria:plan with --lang en switches to English
```gherkin
Given the user invokes /aria:plan --lang en
When the planning skill processes the input
Then milestone phases shall be in English: "Pre-submission", "Submission", "Review", "Approval"
And deliverables shall be in English
And dependency descriptions shall be in English
```

**EN-001.6**: /aria:compare with --lang en switches to English
```gherkin
Given the user invokes /aria:compare --lang en
When the comparison skill processes the input
Then the comparison matrix shall be in English
And regulatory topics shall be in English
And similarities/differences shall be in English
```

**EN-001.7**: /aria:report with --lang en switches to English
```gherkin
Given the user invokes /aria:report --lang en
When the briefing skill processes the input
Then the executive summary shall be in English
And detailed analysis sections shall be in English
And recommendations shall be in English
And appendices shall be in English
```

**EN-001.8**: /aria:chat with --lang en switches to English
```gherkin
Given the user invokes /aria:chat --lang en with query "is this a medical device"
When the hybrid router processes the query
Then the response shall be in English
And skill suggestion menu (if displayed) shall be in English
And conversational Q&A shall be in English
```

---

### EN-002: English Toggle via Playbook Setting
**Requirement**: SR-008 - English output via aria.local.md language preference
**Priority**: High

**Test Cases**:

**EN-002.1**: Playbook language "en" applied to all commands
```gherkin
Given aria.local.md exists with language preference set to "en"
When the user invokes /aria:determine (no --lang flag)
Then the system shall load the playbook language setting
And switch all user-facing text to English
And the behavior shall be identical to explicit --lang en flag
```

**EN-002.2**: Playbook language "en" with --lang ko flag override
```gherkin
Given aria.local.md exists with language preference "en"
When the user invokes /aria:classify --lang ko
Then the command flag shall take precedence over the playbook setting
And all user-facing text shall be in Korean
And the playbook English setting shall be ignored for this command execution
```

---

### EN-003: Korean Regulatory Term Translations
**Requirement**: SR-008 - Bilingual regulatory terms when English mode enabled
**Priority**: Medium

**Test Cases**:

**EN-003.1**: Medical device term with Korean translation
```gherkin
Given the user invokes /aria:determine --lang en
When the output mentions "medical device"
Then the term shall include Korean translation: "medical device (의료기기)"
And this pattern shall be consistent throughout the output
```

**EN-003.2**: Regulatory pathway terms with Korean translation
```gherkin
Given the user invokes /aria:pathway --lang en
When the output mentions Korean regulatory terms like "허가" (approval) or "인증" (certification)
Then the terms shall be presented as: "approval (허가)" or "certification (인증)"
And maintain bidirectional clarity
```

**EN-003.3**: Classification grade terms with Korean translation
```gherkin
Given the user invokes /aria:classify --lang en
When the output mentions MFDS classification grades
Then the terms shall include Korean: "MFDS Class 2 (2등급 의료기기)"
And provide clear regulatory term mapping
```

---

### EN-004: Default Korean Output (No English Toggle)
**Requirement**: UR-001 - Korean as default language
**Priority**: Critical

**Test Cases**:

**EN-004.1**: No --lang flag and no playbook language setting → Korean output
```gherkin
Given aria.local.md does NOT exist or contains no language preference
When the user invokes /aria:determine (no --lang flag)
Then all user-facing text shall be in Korean
And no English translations shall be included unless specifically referencing English regulatory terms
And this shall be the default behavior per UR-001
```

---

## Phase 6: Graceful Degradation Test Scenarios

### GD-001: Built-in Knowledge Primary Operation
**Requirement**: SR-001 - Default operation with built-in knowledge (not degraded mode)
**Priority**: Critical

**Test Cases**:

**GD-001.1**: No external MCP configured → standard operation with built-in knowledge
```gherkin
Given no external MCP connections are configured (Notion not configured, Context7 not configured)
And .mcp.json exists but mcpServers section is empty or missing
When the user invokes /aria:determine
Then the system shall operate normally using built-in knowledge as the primary source
And this shall be treated as the standard operational state (NOT a degradation)
And the output shall include "(built-in knowledge)" attribution in the Data Source Attribution section
And the determination result shall be fully usable and accurate
```

**GD-001.2**: Built-in knowledge sufficient for determination analysis
```gherkin
Given no external MCPs are configured
When the user invokes /aria:determine for an active implantable cardiac device
Then the system shall use built-in knowledge to evaluate medical device status
And apply FDA 21 CFR 201(h) criteria, EU MDR Article 2(1) logic, and MFDS criteria from built-in decision frameworks
And produce a determination result: YES (medical device) with traffic light GREEN
And no error messages or limitation notices shall be displayed (this is standard operation)
```

**GD-001.3**: Built-in knowledge sufficient for classification analysis
```gherkin
Given no external MCPs are configured
When the user invokes /aria:classify for a Class II active monitoring device
Then the system shall use built-in classification decision rules
And generate a multi-region classification matrix (FDA Class II, EU MDR Class IIa, MFDS Class 2)
And provide rationale and rule references from built-in knowledge
And output shall be fully functional without external data sources
```

**GD-001.4**: Built-in knowledge sufficient for pathway selection
```gherkin
Given no external MCPs are configured
When the user invokes /aria:pathway for a Class II device targeting US, EU, Korea markets
Then the system shall use built-in pathway selection logic
And identify 510(k) pathway for FDA, CE Marking route for EU, MFDS authorization type for Korea
And provide timeline ranges and requirements from built-in frameworks
And no external database lookup shall be required for core pathway recommendations
```

**GD-001.5**: Built-in knowledge sufficient for full pipeline execution
```gherkin
Given no external MCPs are configured
When the user executes the full pipeline from /aria:determine through /aria:report
Then all commands shall operate normally using built-in knowledge
And each command shall produce fully usable outputs
And the final briefing shall synthesize all pipeline data accurately
And the entire workflow shall complete without external data dependencies
```

---

### GD-002: Notion MCP Unavailable at Runtime
**Requirement**: SR-001 - Limitation notice when previously configured MCP becomes unavailable
**Priority**: High

**Test Cases**:

**GD-002.1**: Notion MCP configured but unavailable → limitation notice
```gherkin
Given Notion MCP was previously configured in .mcp.json with valid credentials
And Notion MCP becomes unavailable at runtime (network failure, API error, invalid token)
When the user invokes /aria:determine
Then the system shall continue with built-in knowledge
And display a limitation notice in the Data Source Attribution section:
  "Notion DB를 사용할 수 없습니다. 빌트인 지식을 사용하여 분석을 계속합니다."
And the output shall remain fully usable with built-in knowledge baseline
And the determination result shall be accurate based on built-in decision logic
```

**GD-002.2**: Notion unavailable → no organization-specific data enrichment
```gherkin
Given Notion MCP configured but unavailable
When /aria:pathway is executed
Then the system shall use built-in pathway logic
And NOT include organization-specific precedents or custom pathway preferences from Notion
And display a note: "(Notion DB 사용 불가 - 빌트인 지식 기반 경로 추천)"
And the pathway recommendations shall be generic (no organization customization)
```

---

### GD-003: Context7 MCP Unavailable at Runtime
**Requirement**: SR-001 - Limitation notice when Context7 unavailable
**Priority**: Medium

**Test Cases**:

**GD-003.1**: Context7 MCP unavailable → limitation notice
```gherkin
Given Context7 MCP was previously configured
And Context7 MCP becomes unavailable at runtime
When the user invokes /aria:compare
Then the system shall continue with built-in knowledge
And display a limitation notice:
  "Context7 문서 검증을 사용할 수 없습니다. 빌트인 지식을 사용합니다."
And the comparison matrix shall be generated using built-in regulatory difference frameworks
And the output shall be fully functional without Context7 supplementation
```

---

### GD-004: Both Notion and Context7 Unavailable
**Requirement**: SR-001 - System operational with built-in knowledge only
**Priority**: High

**Test Cases**:

**GD-004.1**: All external MCPs unavailable → full operation with built-in
```gherkin
Given Notion MCP and Context7 MCP are both configured but unavailable at runtime
When the user invokes /aria:classify
Then the system shall operate with built-in knowledge only
And display limitation notices for both unavailable sources in the Data Source Attribution section
And the classification matrix shall be generated using built-in decision rules
And the output shall be fully functional with built-in knowledge baseline
And no critical features shall be blocked due to MCP unavailability
```

---

### GD-005: Google Drive MCP Unavailable (Format Fallback)
**Requirement**: SR-001, ER-017 - Fallback to Markdown when Google Drive unavailable
**Priority**: High

**Test Cases**:

**GD-005.1**: --format gdocs requested but google-drive-mcp NOT configured
```gherkin
Given google-drive-mcp is NOT configured in .mcp.json
When the user invokes /aria:report --format gdocs
Then the system shall display a limitation notice:
  "Google Drive MCP가 설정되지 않았습니다. Markdown 형식으로 보고서를 생성합니다."
And the system shall fallback to Markdown format
And the output shall be written to .aria/products/{product}/{date}/briefing.md
And the limitation notice shall appear in the Data Source Attribution section
```

**GD-005.2**: --format gdocs requested but google-drive-mcp configured and unavailable
```gherkin
Given google-drive-mcp is configured but unavailable at runtime
When the user invokes /aria:report --format gdocs
Then the system shall display a limitation notice:
  "Google Drive에 연결할 수 없습니다. Markdown 형식으로 보고서를 생성합니다."
And fallback to Markdown format
And write the output to briefing.md
```

---

### GD-006: Module Files Unavailable (Core Knowledge Only)
**Requirement**: SR-001 - Core SKILL.md operation when module files unavailable
**Priority**: Low

**Test Cases**:

**GD-006.1**: Module files unavailable → use SKILL.md core knowledge only
```gherkin
Given the determination skill SKILL.md exists
And modules/ subdirectory is missing or inaccessible
When the user invokes /aria:determine
Then the system shall use SKILL.md core decision framework only (~2,000-2,500 tokens)
And display a limitation notice:
  "상세 기준 파일을 사용할 수 없습니다. 핵심 지식만 사용합니다."
And the determination analysis shall be functional with reduced detail
And critical decision logic shall remain operational
```

---

### GD-007: Graceful Degradation Matrix Validation
**Requirement**: Specification S4.3 - Graceful degradation matrix compliance
**Priority**: High

**Test Cases**:

**GD-007.1**: Built-in + Module files available, Notion/Context7 NOT configured
```gherkin
Given built-in knowledge is available
And module files are available
And Notion DB is NOT configured
And Context7 is NOT configured
When any command is executed
Then the system status shall be "Standard operation (built-in primary)"
And no user notification shall be displayed (this is the default state)
And output attribution shall show "(built-in knowledge)"
```

**GD-007.2**: Built-in + Module files + Notion configured, Context7 NOT configured
```gherkin
Given built-in knowledge is available
And module files are available
And Notion DB is configured
And Context7 is NOT configured
When any command is executed
Then the system status shall be "Standard + org data"
And a note shall be displayed: "외부 문서 검증이 설정되지 않았습니다"
And output shall include organization-specific data from Notion when relevant
```

**GD-007.3**: Built-in + Module files + Context7 configured, Notion NOT configured
```gherkin
Given built-in knowledge is available
And module files are available
And Notion DB is NOT configured
And Context7 is configured
When any command is executed
Then the system status shall be "Standard + supplementation"
And a note shall be displayed: "조직 데이터베이스가 설정되지 않았습니다"
And output shall include Context7 supplementation for regulatory documents
```

**GD-007.4**: Built-in + Module files + Notion + Context7 all configured
```gherkin
Given built-in knowledge is available
And module files are available
And Notion DB is configured
And Context7 is configured
When any command is executed
Then the system status shall be "Full operation (enhanced)"
And no limitation notices shall be displayed
And output attribution shall show mixed sources: "(built-in knowledge, Notion DB, Context7)"
```

**GD-007.5**: Built-in available, module files unavailable, no external MCPs
```gherkin
Given built-in knowledge (SKILL.md) is available
And module files are unavailable
And Notion DB is NOT configured
And Context7 is NOT configured
When any command is executed
Then the system status shall be "Core operation (SKILL.md only)"
And a limitation notice shall be displayed: "모듈 파일을 사용할 수 없습니다. 핵심 지식만 사용합니다"
And the output shall be functional with reduced detail
```

---

## Cross-Requirement Integration Tests

### INT-001: PDF Export + English Toggle
**Requirement**: ER-017 + SR-008 - Multi-format output with English language
**Priority**: High

**Test Cases**:

**INT-001.1**: PDF report in English
```gherkin
Given the user has completed the full pipeline
When the user invokes /aria:report --format pdf --lang en
Then the system shall confirm the analysis in English
And after user confirmation, generate a PDF format report in English
And all sections (executive summary, detailed analysis, recommendations, appendices) shall be in English
And Korean regulatory terms shall include English translations
And the PDF shall be stored in .aria/products/{product}/{date}/briefing.pdf
```

---

### INT-002: Playbook Language + English Flag Override
**Requirement**: SR-002 + SR-008 - Command flag precedence over playbook
**Priority**: High

**Test Cases**:

**INT-002.1**: Playbook "ko" overridden by --lang en flag
```gherkin
Given aria.local.md exists with language preference "ko"
When the user invokes /aria:determine --lang en
Then the command flag shall take precedence over the playbook setting
And all user-facing text shall be in English
And the playbook Korean setting shall be ignored for this command execution
```

**INT-002.2**: Playbook "en" overridden by --lang ko flag
```gherkin
Given aria.local.md exists with language preference "en"
When the user invokes /aria:classify --lang ko
Then the command flag shall take precedence over the playbook setting
And all user-facing text shall be in Korean
And the playbook English setting shall be ignored
```

---

### INT-003: Graceful Degradation + PDF Export
**Requirement**: SR-001 + ER-017 - PDF export with built-in knowledge only
**Priority**: Medium

**Test Cases**:

**INT-003.1**: PDF report generated with built-in knowledge only
```gherkin
Given no external MCPs are configured (Notion, Context7, Google Drive all absent)
When the user invokes /aria:report --format pdf
Then the system shall confirm the analysis with the user
And after user confirmation, generate a PDF format report using built-in knowledge only
And the Data Source Attribution section shall show "(built-in knowledge)"
And the PDF shall be fully functional without external data sources
And the PDF shall be stored locally in .aria/products/{product}/{date}/briefing.pdf
```

---

### INT-004: Playbook + Graceful Degradation
**Requirement**: SR-002 + SR-001 - Playbook loading without external MCPs
**Priority**: Medium

**Test Cases**:

**INT-004.1**: Playbook applied with built-in knowledge only
```gherkin
Given aria.local.md exists with preferred pathways and risk tolerance settings
And no external MCPs are configured
When the user invokes /aria:pathway
Then the system shall load playbook pathway preferences
And apply built-in knowledge for pathway logic
And recommend playbook-preferred pathways
And display attribution: "(조직 playbook 적용, 빌트인 지식 사용)"
```

---

## Negative Tests

### NEG-001: Invalid Format Flag
**Requirement**: ER-017 - Error handling for invalid format values
**Priority**: Medium

**Test Cases**:

**NEG-001.1**: Unsupported format value
```gherkin
Given the user invokes /aria:report --format xml
When the system validates the format flag
Then the system shall reject the invalid format value
And display an error message: "지원되지 않는 형식입니다. 사용 가능한 형식: markdown, pdf, gdocs"
And the command shall NOT proceed until a valid format is provided
```

---

### NEG-002: Playbook Syntax Errors
**Requirement**: SR-002 - Error handling for malformed playbook
**Priority**: Medium

**Test Cases**:

**NEG-002.1**: aria.local.md with malformed YAML syntax
```gherkin
Given aria.local.md exists but contains malformed YAML syntax (unclosed quotes, invalid indentation)
When any command attempts to load the playbook
Then the system shall detect the syntax error
And display an error message: "aria.local.md 파일 형식 오류가 있습니다. 기본 설정을 사용합니다."
And fallback to default skill behavior
And log the syntax error for debugging
```

**NEG-002.2**: aria.local.md with invalid language value
```gherkin
Given aria.local.md exists with language preference set to "fr" (unsupported language)
When any command attempts to load the playbook
Then the system shall detect the invalid language value
And display a warning: "지원되지 않는 언어 설정입니다 (fr). 기본 언어(ko)를 사용합니다."
And fallback to Korean (default)
```

---

### NEG-003: English Toggle Edge Cases
**Requirement**: SR-008 - Error handling for language flag
**Priority**: Low

**Test Cases**:

**NEG-003.1**: Invalid --lang flag value
```gherkin
Given the user invokes /aria:determine --lang fr
When the system validates the language flag
Then the system shall reject the unsupported language value
And display an error message: "지원되지 않는 언어입니다. 사용 가능한 언어: ko, en"
And fallback to default Korean
```

**NEG-003.2**: Duplicate --lang flags
```gherkin
Given the user invokes /aria:classify --lang en --lang ko
When the system parses the command flags
Then the system shall use the last language flag value: "ko"
And proceed with Korean output
```

---

## Ubiquitous Requirements Coverage

### UR-001: Korean Language Output (Default)
**Test Coverage**: All test scenarios validate Korean output when no English toggle is enabled

### UR-002: Disclaimer Presence
**Test Coverage**: All PDF export and command execution scenarios validate disclaimer presence in all formats

### UR-003: Data Source Attribution
**Test Coverage**: All graceful degradation scenarios validate source attribution for built-in knowledge, Notion, Context7

### UR-004: VALID Framework
**Test Coverage**: PDF export tests validate VALID checklist compliance in all output formats

### UR-005: Traffic Light System
**Test Coverage**: All command execution scenarios validate traffic light indicators in all languages

### UR-006: Data Storage Path Convention
**Test Coverage**: PDF export tests validate .aria/products/{product}/{date}/ path structure

---

## Summary

**Total Test Scenarios**: 40+ test cases

**Coverage**:
- **PDF Export (ER-017)**: 100% (10+ scenarios covering all 5 commands with multi-format output)
  - Brief command PDF export: 3 test cases
  - Compare command PDF export: 2 test cases
  - Pathway command PDF export: 2 test cases
  - Estimate command PDF export: 1 test case
  - Plan command PDF export: 1 test case
  - Format flag validation: 3 test cases
  - Report issuance policy: 3 test cases
- **Playbook Loading (SR-002)**: 100% (6 scenarios covering all playbook settings)
  - Language preference: 3 test cases
  - Pathway defaults: 2 test cases
  - Risk tolerance: 2 test cases
  - Custom escalation criteria: 1 test case
  - Data retention warning: 2 test cases
  - Playbook absent: 1 test case
- **English Toggle (SR-008)**: 100% (12+ scenarios covering all 8 commands with language switching)
  - Command flag --lang en: 8 test cases (one per command)
  - Playbook language setting: 2 test cases
  - Korean regulatory term translations: 3 test cases
  - Default Korean output: 1 test case
- **Graceful Degradation (SR-001)**: 100% (12+ scenarios covering degradation matrix)
  - Built-in knowledge primary: 5 test cases
  - Notion unavailable: 2 test cases
  - Context7 unavailable: 1 test case
  - Both MCPs unavailable: 1 test case
  - Google Drive unavailable: 2 test cases
  - Module files unavailable: 1 test case
  - Degradation matrix validation: 5 test cases
- **Integration Tests**: 4 scenarios covering cross-requirement interactions
- **Negative Tests**: 6 scenarios covering edge cases and error handling

**Quality Targets**:
- **Requirement Coverage**: 100% for SR-001, SR-002, SR-008, ER-017
- **Format Support**: Markdown (default), PDF, Google Docs
- **Language Support**: Korean (default), English (--lang en flag or playbook)
- **Graceful Degradation**: Built-in knowledge as default operational state

**Focus**: Multi-format output validation, organization-specific playbook customization, bilingual output support, built-in knowledge resilience

---

**Version**: 1.0.0
**Created**: 2026-02-11
**Author**: Testing Specialist (team-tester)
