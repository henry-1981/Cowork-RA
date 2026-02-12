# Test Scenarios for SPEC-ARIA-001 Phase 5

**SPEC**: SPEC-ARIA-001 v4.0.0
**Scope**: Phase 5 acceptance criteria validation (Router Command + Workflow Integration)
**Status**: Test scenarios documented
**Coverage Target**: 100% requirement coverage for ER-001, SR-006

---

## Executive Summary

This document defines comprehensive test scenarios for ARIA Cowork Plugin Phase 5, covering:
- **Hybrid Router**: `/aria:chat` command with keyword auto-detect and skill suggestion menu
- **Multi-Product Selection**: File-based persistence via `.aria/active_product.json` for stateless environments
- **Pipeline Integration**: Cross-command context sharing via Context Simplifier
- **Full Workflow Validation**: End-to-end pipeline from determination through briefing

Test design follows TDD methodology with 100% coverage target for all Phase 5 acceptance criteria.

---

## Test Strategy

### Test Categories

1. **Routing Tests** (40%): Hybrid router keyword detection and skill suggestion
2. **Multi-Product Tests** (30%): Active product selection and persistence
3. **Integration Tests** (20%): Full pipeline flow validation
4. **Context Loading Tests** (10%): Context Simplifier and cross-command data flow

### Coverage Mapping

All test scenarios map to acceptance criteria in `acceptance.md`:
- **Event-Driven Requirements**: ER-001 (hybrid routing), ER-011 (auto-load context)
- **State-Driven Requirements**: SR-006 (multi-product selection)
- **Ubiquitous Requirements**: UR-001 through UR-006
- **Quality Target**: Routing accuracy 80%+ on 20+ queries across 7 domains (acceptance.md line 677-679)

---

## Phase 5: Hybrid Router Test Scenarios

### HR-001: Clear Keyword Routing - Determination Skill
**Requirement**: ER-001 - Keyword auto-detect for clear matches
**Priority**: Critical

**Test Cases**:

**HR-001.1**: "의료기기인지 확인해주세요" routes to determination
```gherkin
Given the user invokes /aria:chat with query "의료기기인지 확인해주세요"
When the hybrid router processes the query
Then the keyword "의료기기" shall be detected
And the system shall route directly to the determination skill
And execute /aria:determine without showing a disambiguation menu
And the output shall include determination results
```

**HR-001.2**: "is this a medical device" routes to determination (English)
```gherkin
Given the user invokes /aria:chat with query "is this a medical device"
When the hybrid router processes the query
Then the keyword "medical device" shall be detected
And the system shall route directly to the determination skill
And execute /aria:determine without disambiguation
```

**HR-001.3**: "device determination" routes to determination
```gherkin
Given the user invokes /aria:chat with query "device determination"
When the hybrid router processes the query
Then the keyword "determination" shall be detected
And the system shall route directly to the determination skill
```

---

### HR-002: Clear Keyword Routing - Classification Skill
**Requirement**: ER-001 - Keyword auto-detect for classification
**Priority**: Critical

**Test Cases**:

**HR-002.1**: "제품 등급 분류" routes to classification
```gherkin
Given the user invokes /aria:chat with query "제품 등급 분류"
When the hybrid router processes the query
Then the keyword "등급" or "분류" shall be detected
And the system shall route directly to the classification skill
And execute /aria:classify without disambiguation
```

**HR-002.2**: "classify my device" routes to classification
```gherkin
Given the user invokes /aria:chat with query "classify my device"
When the hybrid router processes the query
Then the keyword "classify" shall be detected
And the system shall route directly to the classification skill
```

**HR-002.3**: "what class is this device" routes to classification
```gherkin
Given the user invokes /aria:chat with query "what class is this device"
When the hybrid router processes the query
Then the keyword "class" shall be detected
And the system shall route directly to the classification skill
```

**HR-002.4**: "device grade" routes to classification
```gherkin
Given the user invokes /aria:chat with query "device grade"
When the hybrid router processes the query
Then the keyword "grade" shall be detected
And the system shall route directly to the classification skill
```

---

### HR-003: Clear Keyword Routing - Pathway Skill
**Requirement**: ER-001 - Keyword auto-detect for pathway
**Priority**: Critical

**Test Cases**:

**HR-003.1**: "규제 경로 추천" routes to pathway
```gherkin
Given the user invokes /aria:chat with query "규제 경로 추천"
When the hybrid router processes the query
Then the keyword "경로" shall be detected
And the system shall route directly to the pathway skill
And execute /aria:pathway without disambiguation
```

**HR-003.2**: "submission route" routes to pathway
```gherkin
Given the user invokes /aria:chat with query "submission route"
When the hybrid router processes the query
Then the keyword "submission" or "route" shall be detected
And the system shall route directly to the pathway skill
```

**HR-003.3**: "regulatory pathway for FDA" routes to pathway
```gherkin
Given the user invokes /aria:chat with query "regulatory pathway for FDA"
When the hybrid router processes the query
Then the keyword "pathway" shall be detected
And the system shall route directly to the pathway skill
```

**HR-003.4**: "approval process" routes to pathway
```gherkin
Given the user invokes /aria:chat with query "approval process"
When the hybrid router processes the query
Then the keyword "approval" shall be detected
And the system shall route directly to the pathway skill
```

---

### HR-004: Clear Keyword Routing - Estimation Skill
**Requirement**: ER-001 - Keyword auto-detect for estimation
**Priority**: Critical

**Test Cases**:

**HR-004.1**: "비용 추정" routes to estimation
```gherkin
Given the user invokes /aria:chat with query "비용 추정"
When the hybrid router processes the query
Then the keyword "비용" shall be detected
And the system shall route directly to the estimation skill
And execute /aria:estimate without disambiguation
```

**HR-004.2**: "cost estimate" routes to estimation
```gherkin
Given the user invokes /aria:chat with query "cost estimate"
When the hybrid router processes the query
Then the keyword "cost" or "estimate" shall be detected
And the system shall route directly to the estimation skill
```

**HR-004.3**: "timeline for submission" routes to estimation
```gherkin
Given the user invokes /aria:chat with query "timeline for submission"
When the hybrid router processes the query
Then the keyword "timeline" shall be detected
And the system shall route directly to the estimation skill
```

**HR-004.4**: "how much will it cost" routes to estimation
```gherkin
Given the user invokes /aria:chat with query "how much will it cost"
When the hybrid router processes the query
Then the keyword "cost" shall be detected
And the system shall route directly to the estimation skill
```

---

### HR-005: Clear Keyword Routing - Planning Skill
**Requirement**: ER-001 - Keyword auto-detect for planning
**Priority**: Critical

**Test Cases**:

**HR-005.1**: "규제 계획 수립" routes to planning
```gherkin
Given the user invokes /aria:chat with query "규제 계획 수립"
When the hybrid router processes the query
Then the keyword "계획" shall be detected
And the system shall route directly to the planning skill
And execute /aria:plan without disambiguation
```

**HR-005.2**: "regulatory plan" routes to planning
```gherkin
Given the user invokes /aria:chat with query "regulatory plan"
When the hybrid router processes the query
Then the keyword "plan" shall be detected
And the system shall route directly to the planning skill
```

**HR-005.3**: "milestone schedule" routes to planning
```gherkin
Given the user invokes /aria:chat with query "milestone schedule"
When the hybrid router processes the query
Then the keyword "milestone" shall be detected
And the system shall route directly to the planning skill
```

**HR-005.4**: "project roadmap" routes to planning
```gherkin
Given the user invokes /aria:chat with query "project roadmap"
When the hybrid router processes the query
Then the keyword "roadmap" shall be detected
And the system shall route directly to the planning skill
```

---

### HR-006: Clear Keyword Routing - Comparison Skill
**Requirement**: ER-001 - Keyword auto-detect for comparison
**Priority**: Critical

**Test Cases**:

**HR-006.1**: "FDA와 EU MDR 비교" routes to comparison
```gherkin
Given the user invokes /aria:chat with query "FDA와 EU MDR 비교"
When the hybrid router processes the query
Then the keyword "비교" shall be detected
And the system shall route directly to the comparison skill
And execute /aria:compare without disambiguation
```

**HR-006.2**: "compare FDA and EU" routes to comparison
```gherkin
Given the user invokes /aria:chat with query "compare FDA and EU"
When the hybrid router processes the query
Then the keyword "compare" shall be detected
And the system shall route directly to the comparison skill
```

**HR-006.3**: "regulatory differences" routes to comparison
```gherkin
Given the user invokes /aria:chat with query "regulatory differences"
When the hybrid router processes the query
Then the keyword "differences" shall be detected
And the system shall route directly to the comparison skill
```

**HR-006.4**: "multi-country requirements" routes to comparison
```gherkin
Given the user invokes /aria:chat with query "multi-country requirements"
When the hybrid router processes the query
Then the keyword "multi-country" shall be detected
And the system shall route directly to the comparison skill
```

---

### HR-007: Clear Keyword Routing - Briefing Skill
**Requirement**: ER-001 - Keyword auto-detect for briefing
**Priority**: Critical

**Test Cases**:

**HR-007.1**: "종합 보고서 생성" routes to briefing
```gherkin
Given the user invokes /aria:chat with query "종합 보고서 생성"
When the hybrid router processes the query
Then the keyword "보고서" shall be detected
And the system shall route directly to the briefing skill
And execute /aria:report without disambiguation
```

**HR-007.2**: "executive summary" routes to briefing
```gherkin
Given the user invokes /aria:chat with query "executive summary"
When the hybrid router processes the query
Then the keyword "executive" or "summary" shall be detected
And the system shall route directly to the briefing skill
```

**HR-007.3**: "comprehensive report" routes to briefing
```gherkin
Given the user invokes /aria:chat with query "comprehensive report"
When the hybrid router processes the query
Then the keyword "report" shall be detected
And the system shall route directly to the briefing skill
```

**HR-007.4**: "regulatory briefing" routes to briefing
```gherkin
Given the user invokes /aria:chat with query "regulatory briefing"
When the hybrid router processes the query
Then the keyword "briefing" shall be detected
And the system shall route directly to the briefing skill
```

---

### HR-008: Ambiguous Query - Skill Suggestion Menu
**Requirement**: ER-001 - Skill suggestion menu for ambiguous queries
**Priority**: Critical

**Test Cases**:

**HR-008.1**: "help with my product" shows skill suggestions
```gherkin
Given the user invokes /aria:chat with query "help with my product"
When the hybrid router processes the query
Then no single clear keyword shall be detected
And the system shall present a skill suggestion menu
And the menu shall include top 1-3 matching skills
And the user can select a skill to proceed
```

**HR-008.2**: "I need guidance" shows skill suggestions
```gherkin
Given the user invokes /aria:chat with query "I need guidance"
When the hybrid router processes the query
Then the system shall present a skill suggestion menu
And suggested skills may include determination, classification, or pathway
And each suggestion shall include a brief description
```

**HR-008.3**: "regulatory advice" shows skill suggestions
```gherkin
Given the user invokes /aria:chat with query "regulatory advice"
When the hybrid router processes the query
Then the system shall present a skill suggestion menu
And suggested skills may include comparison, briefing, or planning
```

**HR-008.4**: "시작하고 싶어요" shows skill suggestions
```gherkin
Given the user invokes /aria:chat with query "시작하고 싶어요"
When the hybrid router processes the query
Then the system shall present a skill suggestion menu in Korean
And the primary suggestion shall be determination (starting point of pipeline)
```

**HR-008.5**: "what should I do" shows skill suggestions
```gherkin
Given the user invokes /aria:chat with query "what should I do"
When the hybrid router processes the query
Then the system shall present a skill suggestion menu
And the menu shall suggest starting with determination if no prior data exists
And the menu shall suggest next pipeline step if prior data exists
```

---

### HR-009: General Q&A Mode - Conversational Responses
**Requirement**: ER-001 - Conversational mode for general regulatory questions
**Priority**: High

**Test Cases**:

**HR-009.1**: "what is EU MDR?" enters conversational mode
```gherkin
Given the user invokes /aria:chat with query "what is EU MDR?"
When the hybrid router processes the query
Then the system shall enter conversational mode
And provide an informational answer about EU MDR
And NOT execute any specific skill command
```

**HR-009.2**: "what is the difference between 510(k) and PMA?" enters conversational mode
```gherkin
Given the user invokes /aria:chat with query "what is the difference between 510(k) and PMA?"
When the hybrid router processes the query
Then the system shall enter conversational mode
And provide a comparison explanation
And NOT execute the comparison skill (since this is general education, not product-specific comparison)
```

**HR-009.3**: "explain medical device classification" enters conversational mode
```gherkin
Given the user invokes /aria:chat with query "explain medical device classification"
When the hybrid router processes the query
Then the system shall enter conversational mode
And provide general regulatory education about classification
And NOT execute the classification skill (since no specific device is being classified)
```

**HR-009.4**: "FDA 규제란?" enters conversational mode
```gherkin
Given the user invokes /aria:chat with query "FDA 규제란?"
When the hybrid router processes the query
Then the system shall enter conversational mode
And provide an informational answer in Korean
```

**HR-009.5**: "what is ISO 13485?" enters conversational mode
```gherkin
Given the user invokes /aria:chat with query "what is ISO 13485?"
When the hybrid router processes the query
Then the system shall enter conversational mode
And provide a general explanation of ISO 13485
And suggest /aria:compare for comparing QMS requirements across regions if relevant
```

---

### HR-010: Routing Accuracy Quality Target
**Requirement**: Acceptance criteria - 80%+ routing accuracy on 20+ queries (acceptance.md line 677-679)
**Priority**: Critical

**Test Cases**:

**HR-010.1**: Comprehensive routing accuracy test across 7 skill domains
```gherkin
Given at least 20 diverse queries spanning all 7 skill domains:
  - Determination: 3 queries (e.g., "is this a medical device", "check if medical device", "의료기기 판정")
  - Classification: 3 queries (e.g., "classify my device", "what class is this", "등급 분류")
  - Pathway: 3 queries (e.g., "submission route", "regulatory pathway", "경로 추천")
  - Estimation: 3 queries (e.g., "cost estimate", "timeline", "비용 추정")
  - Planning: 3 queries (e.g., "regulatory plan", "milestone", "계획 수립")
  - Comparison: 3 queries (e.g., "compare FDA and EU", "regulatory differences", "다국가 비교")
  - Briefing: 2 queries (e.g., "executive summary", "comprehensive report", "종합 보고서")
When each query is processed by the hybrid router
Then at least 16 out of 20 queries (80%) shall route to the correct skill
And no query shall route to an incorrect skill (false positive)
And ambiguous queries may show skill suggestions (acceptable outcome)
```

---

## Phase 5: Multi-Product Selection Test Scenarios

### MP-001: Multiple Products - Selection Menu
**Requirement**: SR-006 - Multi-product selection with active_product.json persistence
**Priority**: Critical

**Test Cases**:

**MP-001.1**: 3 products exist, active_product.json absent → show menu
```gherkin
Given .aria/products/ contains 3 product directories:
  - cardiac-monitor-x1/2026-02-10/
  - insulin-pump-z2/2026-02-09/
  - glucose-sensor-y3/2026-02-11/
And .aria/active_product.json does NOT exist
When the user invokes any /aria: command
Then the system shall present a selection menu with all 3 products
And each menu item shall show product name and most recent date
And the menu shall include an option to create a new product
And the user's selection shall be persisted to .aria/active_product.json
```

**MP-001.2**: User selects product from menu → persisted to active_product.json
```gherkin
Given the product selection menu is displayed
When the user selects "cardiac-monitor-x1"
Then .aria/active_product.json shall be created with content:
  {
    "product_name": "cardiac-monitor-x1",
    "last_accessed": "2026-02-11",
    "path": ".aria/products/cardiac-monitor-x1/2026-02-10/"
  }
And the command shall proceed with cardiac-monitor-x1 as the active product
```

**MP-001.3**: Active product context loaded for subsequent commands
```gherkin
Given .aria/active_product.json exists with product_name "cardiac-monitor-x1"
When the user invokes /aria:classify
Then the system shall load context for cardiac-monitor-x1
And NOT present a product selection menu
And update last_accessed in active_product.json to current date
```

---

### MP-002: Single Product - Auto-Select
**Requirement**: SR-006 - Automatically select single product
**Priority**: High

**Test Cases**:

**MP-002.1**: Exactly 1 product exists → auto-select without menu
```gherkin
Given .aria/products/ contains exactly 1 product directory:
  - cardiac-monitor-x1/2026-02-10/
When the user invokes any /aria: command
Then the system shall automatically select cardiac-monitor-x1
And persist the selection to .aria/active_product.json
And NOT present a product selection menu
And the command shall proceed immediately
```

---

### MP-003: Active Product Exists - Load Without Menu
**Requirement**: SR-006 - Load active product from active_product.json
**Priority**: Critical

**Test Cases**:

**MP-003.1**: active_product.json exists with valid reference → load without menu
```gherkin
Given .aria/active_product.json exists with valid product reference:
  {
    "product_name": "insulin-pump-z2",
    "last_accessed": "2026-02-10",
    "path": ".aria/products/insulin-pump-z2/2026-02-09/"
  }
And the path .aria/products/insulin-pump-z2/2026-02-09/ exists
When the user invokes any /aria: command
Then the system shall load insulin-pump-z2 as the active product
And NOT present a product selection menu
And update last_accessed to current date
```

---

### MP-004: Stale Active Product - Re-Prompt
**Requirement**: SR-006 - Stale active_product.json handling
**Priority**: High

**Test Cases**:

**MP-004.1**: active_product.json references non-existent product → re-prompt
```gherkin
Given .aria/active_product.json exists with product reference:
  {
    "product_name": "deleted-product",
    "last_accessed": "2026-01-15",
    "path": ".aria/products/deleted-product/2026-01-15/"
  }
And the path .aria/products/deleted-product/2026-01-15/ does NOT exist
When the user invokes any /aria: command
Then the system shall treat active_product.json as stale
And present a product selection menu with available products
And update active_product.json with the new selection
```

**MP-004.2**: active_product.json with malformed JSON → re-prompt
```gherkin
Given .aria/active_product.json exists but contains malformed JSON
When the user invokes any /aria: command
Then the system shall treat the file as invalid
And present a product selection menu
And create a new valid active_product.json after selection
```

---

### MP-005: Empty Products Directory - Prompt for New Product
**Requirement**: SR-006 - Create new product when directory is empty
**Priority**: High

**Test Cases**:

**MP-005.1**: .aria/products/ is empty → prompt for new product
```gherkin
Given .aria/products/ is empty (no product directories exist)
When the user invokes any /aria: command
Then the system shall prompt the user to create a new product entry
And display the product naming convention: "lowercase, hyphens, alphanumeric only"
And provide an example: "Cardiac Monitor X1" → "cardiac-monitor-x1"
```

**MP-005.2**: User creates new product → persisted to active_product.json
```gherkin
Given the new product prompt is displayed
When the user enters product name "Cardiac Monitor X1"
Then the system shall apply the naming convention to create "cardiac-monitor-x1"
And create directory .aria/products/cardiac-monitor-x1/2026-02-11/
And persist the new product to .aria/active_product.json:
  {
    "product_name": "cardiac-monitor-x1",
    "last_accessed": "2026-02-11",
    "path": ".aria/products/cardiac-monitor-x1/2026-02-11/"
  }
And the command shall proceed with the new product as the active product
```

---

### MP-006: Multi-Product Naming Convention Validation
**Requirement**: SR-006 - Product naming convention enforcement
**Priority**: Medium

**Test Cases**:

**MP-006.1**: Valid product naming convention accepted
```gherkin
Given the user is creating a new product
When the user enters "cardiac-monitor-x1" (lowercase, hyphens, alphanumeric)
Then the product name shall be accepted
And the directory .aria/products/cardiac-monitor-x1/ shall be created
```

**MP-006.2**: Invalid product naming convention rejected
```gherkin
Given the user is creating a new product
When the user enters "Cardiac Monitor X1" (uppercase, spaces)
Then the system shall convert to "cardiac-monitor-x1" automatically
And notify the user: "제품명이 'cardiac-monitor-x1'로 변환되었습니다"
```

**MP-006.3**: Special characters removed from product name
```gherkin
Given the user is creating a new product
When the user enters "Cardiac Monitor (X1) #2" (special characters)
Then the system shall convert to "cardiac-monitor-x1-2"
And remove special characters: (, ), #
And retain only lowercase, hyphens, and alphanumeric
```

---

### MP-007: Active Product Security Warning
**Requirement**: Specification S11.1 - active_product.json security warning
**Priority**: Medium

**Test Cases**:

**MP-007.1**: README.md includes active_product.json security warning
```gherkin
Given the ARIA plugin README.md is reviewed
When the security section is read
Then it shall include a warning: "active_product.json은 개인 로컬 상태 파일이므로 Git에 커밋하거나 공유하지 마세요"
And recommend adding .aria/ to .gitignore
```

---

## Phase 5: Pipeline Integration Test Scenarios

### PI-001: Full Pipeline Auto-Context Loading
**Requirement**: ER-011 - Auto-load context from prior steps via Context Simplifier
**Priority**: Critical

**Test Cases**:

**PI-001.1**: Sequential pipeline execution with context loading
```gherkin
Given the user executes the full pipeline for product "cardiac-monitor-x1":
  - /aria:determine → determination.md + determination.summary.md
  - /aria:classify (loads determination.summary.md automatically) → classification.md + classification.summary.md
  - /aria:pathway (loads classification.summary.md automatically) → pathway.md + pathway.summary.md
  - /aria:estimate (loads pathway.summary.md automatically) → estimation.md + estimation.summary.md
  - /aria:plan (loads estimation.summary.md automatically) → plan.md + plan.summary.md
  - /aria:compare (loads classification.summary.md for context) → comparison.md + comparison.summary.md
  - /aria:report (loads all .summary.md files) → briefing.md + briefing.summary.md
When each command is executed
Then the system shall auto-load prior step context from .summary.md files
And no data shall be re-requested from the user
And each command shall display "(prior context loaded from {step}.summary.md)"
```

**PI-001.2**: Context loading failure graceful fallback
```gherkin
Given /aria:classify is executed
And determination.summary.md is missing (corrupted or deleted)
When the classification skill attempts to load prior context
Then the system shall fall back to manual input mode
And prompt the user for required classification fields
And display a warning: "이전 단계 데이터를 찾을 수 없습니다. 수동 입력을 시작합니다."
```

---

### PI-002: Context Simplifier Token Efficiency Validation
**Requirement**: ER-015 - Context compression reduces token usage by 60%+
**Priority**: High

**Test Cases**:

**PI-002.1**: Full pipeline with compression vs without compression
```gherkin
Given a full pipeline run from /aria:determine through /aria:report
When comparing token usage with compressed summaries vs full outputs
Then total pipeline context token usage shall be reduced by at least 60%
And no critical decision information shall be lost in compression
```

**PI-002.2**: Each .summary.md file within 500 token budget
```gherkin
Given any /aria: command completes and generates a .summary.md file
When the summary token count is measured
Then the summary shall be within approximately 500 tokens
And the summary shall follow the Key-Value Markdown format:
  - **Decision**: [primary result]
  - **Class**: [classification if applicable]
  - **Traffic Light**: [GREEN/YELLOW/RED]
  - **Key Factors**: [critical data points]
  - **Escalation**: [escalation flags]
  - **Sources**: [data source attribution]
```

---

### PI-003: Cross-Command Context Sharing
**Requirement**: ER-011 - Pipeline continuity via .aria/ data storage
**Priority**: High

**Test Cases**:

**PI-003.1**: Classification loads determination context
```gherkin
Given /aria:determine completed for "insulin-pump-z2"
And determination.summary.md exists with decision "YES (medical device)" and intended use extracted
When /aria:classify is executed
Then the classification skill shall load determination.summary.md
And pre-populate fields: intended use, device description, product form
And NOT re-ask for information already in determination.summary.md
```

**PI-003.2**: Pathway loads classification context
```gherkin
Given /aria:classify completed for "insulin-pump-z2"
And classification.summary.md exists with FDA Class II, EU MDR Class IIa, MFDS Class 2
When /aria:pathway is executed
Then the pathway skill shall load classification.summary.md
And suggest pathways based on classification results
And NOT re-ask for classification information
```

**PI-003.3**: Briefing loads all pipeline context
```gherkin
Given all 6 prior pipeline steps completed for "insulin-pump-z2"
And all .summary.md files exist
When /aria:report is executed
Then the briefing skill shall load all 6 .summary.md files
And synthesize all data into a comprehensive briefing
And NOT re-request any information from the user
```

---

## Integration Tests

### IT-001: Full Phase 5 Workflow - Hybrid Router to Briefing
**Requirement**: Phase 5 Success Criterion - Full pipeline flow seamless
**Priority**: Critical

**Test Cases**:

**IT-001.1**: User journey from /aria:chat to final briefing
```gherkin
Given the user is new to ARIA and has no prior data
When the user invokes /aria:chat with query "의료기기 규제 시작하고 싶어요"
Then the hybrid router shall suggest starting with /aria:determine
And the user proceeds through the full pipeline:
  - /aria:chat → suggests determination
  - /aria:determine → determination.md created
  - /aria:chat → suggests classification (next step)
  - /aria:classify → classification.md created (auto-loads determination context)
  - /aria:chat → suggests pathway
  - /aria:pathway → pathway.md created (auto-loads classification context)
  - /aria:chat → suggests estimation
  - /aria:estimate → estimation.md created (auto-loads pathway context)
  - /aria:chat → suggests planning
  - /aria:plan → plan.md created (auto-loads estimation context)
  - /aria:chat → suggests comparison or briefing
  - /aria:report → briefing.md created (auto-loads all context)
And the entire workflow completes without re-requesting user data
And the final briefing synthesizes all pipeline data accurately
```

---

### IT-002: Multi-Product Pipeline Isolation
**Requirement**: SR-006 - Multi-product workflows prevent data crossover
**Priority**: High

**Test Cases**:

**IT-002.1**: Context isolation between products
```gherkin
Given the user has completed /aria:determine for "cardiac-monitor-x1"
And the user switches to "insulin-pump-z2" via product selection menu
When /aria:classify is executed for "insulin-pump-z2"
Then the system shall NOT load determination.summary.md from "cardiac-monitor-x1"
And the system shall prompt for new determination data for "insulin-pump-z2"
And all context shall remain isolated per product
```

---

## Negative Tests

### NT-001: Routing Edge Cases
**Requirement**: Error handling for ambiguous routing
**Priority**: Medium

**Test Cases**:

**NT-001.1**: Completely unrelated query to regulatory domain
```gherkin
Given the user invokes /aria:chat with query "what is the weather today"
When the hybrid router processes the query
Then the system shall enter conversational mode
And respond: "죄송합니다. 저는 의료기기 규제 전문 AI입니다. 의료기기 규제 관련 질문을 해주세요."
And suggest example queries: "의료기기인지 확인", "등급 분류", "규제 경로"
```

**NT-001.2**: Query with multiple skill keywords
```gherkin
Given the user invokes /aria:chat with query "classify and estimate cost for my device"
When the hybrid router processes the query
Then the system shall detect multiple keywords: "classify" and "cost"
And present a skill suggestion menu with both classification and estimation skills
And the user can select which skill to execute first
```

---

### NT-002: Multi-Product Edge Cases
**Requirement**: Error handling for multi-product scenarios
**Priority**: Medium

**Test Cases**:

**NT-002.1**: active_product.json references a future date (invalid)
```gherkin
Given .aria/active_product.json exists with last_accessed "2027-01-01" (future date)
When the user invokes any /aria: command
Then the system shall treat the file as suspicious
And display a warning: "active_product.json의 날짜가 유효하지 않습니다. 제품을 다시 선택하세요."
And present a product selection menu
```

**NT-002.2**: Two products with identical names (rare collision)
```gherkin
Given .aria/products/ contains two directories with the same name but different dates:
  - cardiac-monitor-x1/2026-02-10/
  - cardiac-monitor-x1/2026-02-11/
When the product selection menu is displayed
Then the system shall list both entries with unique identifiers:
  - "cardiac-monitor-x1 (2026-02-10)"
  - "cardiac-monitor-x1 (2026-02-11)"
And the user can select which date version to use
```

---

## Ubiquitous Requirements Coverage

### UR-001: Korean Language Output
**Test Coverage**: All HR, MP, PI test scenarios validate Korean output

**UR-002: Disclaimer Presence
**Test Coverage**: All command executions include disclaimer validation

**UR-003: Data Source Attribution
**Test Coverage**: All routing, pipeline, and context loading scenarios validate source attribution

**UR-004: VALID Framework
**Test Coverage**: Full pipeline integration tests validate VALID checklist

**UR-005: Traffic Light System
**Test Coverage**: Routing and pipeline tests validate traffic light indicators

**UR-006: Data Storage Path Convention
**Test Coverage**: Multi-product and pipeline tests validate .aria/ path structure

---

## Summary

**Total Test Scenarios**: 35+ test cases

**Coverage**:
- **ER-001 (hybrid routing)**: 100% (10+ scenarios covering all 7 skills + ambiguous queries + Q&A mode)
  - Determination routing: 3 test cases
  - Classification routing: 4 test cases
  - Pathway routing: 4 test cases
  - Estimation routing: 4 test cases
  - Planning routing: 4 test cases
  - Comparison routing: 4 test cases
  - Briefing routing: 4 test cases
  - Ambiguous queries: 5 test cases
  - General Q&A: 5 test cases
  - Routing accuracy target: 80%+ on 20+ queries
- **SR-006 (multi-product selection)**: 100% (7 scenarios covering all product selection flows)
  - Multiple products → menu
  - Single product → auto-select
  - Active product exists → load without menu
  - Stale active_product.json → re-prompt
  - Empty directory → create new product
  - Naming convention validation
  - Security warning compliance
- **ER-011 (auto-load context)**: 100% (validated via pipeline integration tests)
- **ER-015 (context compression)**: 100% (validated via token efficiency tests)
- **Ubiquitous Requirements (UR-001 through UR-006)**: 100%
- **Negative Tests**: 4 scenarios covering edge cases

**Quality Target**:
- **Routing Accuracy**: 80%+ on 20+ queries across 7 skill domains (acceptance.md line 677-679)
- **Requirement Coverage**: 100% for ER-001, SR-006, ER-011

**Focus**: Hybrid routing accuracy, multi-product file-based persistence, full pipeline integration, context compression efficiency

---

**Version**: 1.0.0
**Created**: 2026-02-11
**Author**: Testing Specialist (team-tester)
