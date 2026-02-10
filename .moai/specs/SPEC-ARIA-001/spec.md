# SPEC-ARIA-001: ARIA Cowork Plugin - Full System Refactoring

## TAG BLOCK

```yaml
SPEC_ID: SPEC-ARIA-001
TITLE: ARIA Cowork Plugin - Full System Refactoring
VERSION: 3.1.0
STATUS: Planned
PRIORITY: High
DOMAIN: aria-plugin
CREATED: 2026-02-10
UPDATED: 2026-02-10
AUTHOR: ARIA Architect
ASSIGNED: manager-spec
RELATED_SPECS: []
LIFECYCLE: spec-anchored
TAGS: [aria, cowork, plugin, regulatory, medical-device, refactoring]
```

---

## HISTORY

| Version | Date | Summary |
|---------|------|---------|
| 1.0.0 | 2026-02-10 | Initial SPEC creation |
| 2.0.0 | 2026-02-10 | Review reflection: conversational info extraction, limitation notices, architecture decisions |
| 3.0.0 | 2026-02-10 | Comprehensive review: (A) Built-in knowledge high-density strategy, document-first input workflow, context simplifier, classification tuning; (B) plugin.json manifest fix, command namespacing with `/aria:` prefix, MCP package name correction; (C) plan.md/acceptance.md creation, complete traceability matrix, concurrent product/data versioning, duplicate requirement merging; (D) SKILL.md 500-line constraint, VALID enforcement clarification, agent contingency measurable criteria, security considerations, English toggle, degradation matrix completion; (E) Minor notes for input length, data cleanup, Q&A session handling, glossary, knowledge date stamping, playbook location, data lookup parallelization |
| 3.1.0 | 2026-02-10 | 외부 리뷰 반영: Context Simplifier 생성 주체 명확화, Active Product 상태 관리, 등급 최적화 로직 추상화, 대용량 파일 TOC 분석, 데이터 보존 경고, Acceptance Criteria 정량화, 플래그 형식 표준화 |

---

## Environment

### System Context

**Project**: ARIA (AI Regulatory Intelligence Assistant)
**Type**: Anthropic Cowork Plugin (following knowledge-work-plugins pattern)
**Target Domain**: Medical Device Regulatory Affairs (RA) / Quality Assurance (QA)
**Target Users**: Non-developer business professionals (RA managers, QA engineers, design engineers, clinical specialists)
**Source**: Refactoring of existing ARIA Claude Code agentic system into Cowork plugin format

### Regulatory Scope

**Target Regions**:
- US FDA (Food and Drug Administration)
- EU MDR (Medical Device Regulation 2017/745)
- Korea MFDS (Ministry of Food and Drug Safety)

**Target Device Types**:
- Active medical devices
- Implantable medical devices
- In Vitro Diagnostic (IVD) devices
- Software as a Medical Device (SaMD)
- Non-active medical devices

### Technical Environment

**Platform**: Anthropic Cowork Plugin System
**Plugin Name**: aria
**Language**: Korean (primary user-facing), English (optional toggle via command flag or playbook setting)
**Distribution**: Public GitHub repository, organization internal use first (no marketplace initially)
**Design Benchmark**: Legal plugin from knowledge-work-plugins repository

### Integration Context

**MCP Connectors**:
- Notion (organization regulatory database - primary data source)
- Google Drive (document storage and output)
- Context7 (library and regulatory document supplementation)

**Data Storage**: `.aria/products/{product-name}/{date}/` as Markdown files

---

## Assumptions

### Technical Assumptions

- [A1] Anthropic Cowork Plugin API supports commands and skills as defined in the knowledge-work-plugins pattern
- [A2] Plugin directory structure follows `.claude-plugin/plugin.json` manifest convention
- [A3] Commands use YAML frontmatter with `description` and `argument-hint` fields (minimal frontmatter pattern)
- [A4] Skills use YAML frontmatter with `name` and `description` fields only (minimal frontmatter pattern)
- [A5] MCP servers can be configured via `.mcp.json` at plugin root
- [A6] Each command can operate independently without requiring prior steps
- [A7] Built-in knowledge summaries of approximately 2,000-2,500 tokens per skill, containing decision-making know-how and judgment logic, are sufficient for standalone operation. Regulatory text, law citations, and regulation body text are retrieved from MCP sources (Notion DB, Context7) at runtime.

### Domain Assumptions

- [A8] RA/QA practitioners are comfortable with natural language interfaces but not coding
- [A9] Regulatory workflows follow a sequential pipeline pattern: determine -> classify -> pathway -> estimate -> plan -> compare -> brief
- [A10] VALID quality framework (Verified, Accurate, Linked, Inspectable, Deliverable) is appropriate for regulatory content quality
- [A11] Traffic Light System (GREEN/YELLOW/RED) is universally understood for regulatory risk communication
- [A12] Each organization has custom regulatory strategies, preferred pathways, and decision criteria that should be configurable

### Data Strategy Assumptions

- [A13] Notion DB is the highest-priority data source containing organization-specific regulatory data, precedents, and latest information
- [A14] Built-in knowledge (skill-embedded regulatory summaries) provides sufficient baseline when external sources are unavailable
- [A15] Context7 MCP supplements and verifies information from other sources
- [A16] All three data sources (Notion, built-in, Context7) are mandatory for full operation but the system degrades gracefully

### User Assumptions

- [A17] Users prefer Korean language for all interactions
- [A18] Users require plain language guidance without technical jargon
- [A19] Users expect a disclaimer that all output is reference information, not regulatory advice
- [A20] Users benefit from suggested next steps after each command completes

---

## Requirements (EARS Format)

### Ubiquitous Requirements (Always Active)

**[UR-001] The system shall always provide user-facing responses in Korean.**

- Rationale: Target users are Korean RA/QA practitioners
- Verification: All command output, skill responses, and error messages use Korean
- Acceptance: No English responses exposed to end users unless English mode is explicitly enabled

**[UR-002] The system shall always include a disclaimer stating "This is reference information, not regulatory advice" on all outputs.**

- Rationale: Legal and professional liability protection; regulatory decisions require human expert judgment
- Verification: Every command and skill output contains the disclaimer block
- Acceptance: No output delivered without disclaimer present

**[UR-003] The system shall always attribute data sources in output.**

- Rationale: Regulatory accuracy requires source verification and traceability
- Verification: All regulatory information cites its source (Notion DB, built-in knowledge, Context7, or specific regulation reference)
- Acceptance: No regulatory claims without source attribution
- Note: WR-003 is the negative form of this requirement, retained for explicit prohibition. See WR-003.

**[UR-004] The system shall always enforce the VALID quality framework on all deliverables.**

- Rationale: Regulatory content must meet Verified, Accurate, Linked, Inspectable, Deliverable standards
- Verification: VALID checklist applied before output delivery
- Acceptance: Outputs pass all five VALID pillars

**[UR-005] The system shall always use the Traffic Light System for regulatory risk assessment.**

- Rationale: Universal visual communication of regulatory compliance status
- Verification: Risk assessments use GREEN (compliant), YELLOW (conditional/requires attention), RED (non-compliant/blocked)
- Acceptance: All risk-related output uses the three-color system consistently

**[UR-006] The system shall always store working data in `.aria/products/{product-name}/{date}/` as Markdown files.**

- Rationale: Consistent data persistence enables cross-command context sharing and audit trail
- Verification: Each command reads from and writes to the standardized directory structure
- Acceptance: All product-related data follows the path convention

### Event-Driven Requirements (When-Then)

**[ER-001] WHEN the user invokes `/aria:chat` with a free-form query, THEN the system shall route to the appropriate skill using hybrid detection (keyword auto-detect for clear matches, skill suggestion menu for ambiguous cases).**

- Input: Natural language query in Korean or English
- Processing: Keyword matching against skill domains; if ambiguous, present top 1-3 skill suggestions
- Output: Routed skill execution or disambiguation menu
- Verification: Test with 20+ diverse queries across all 7 skill domains

**[ER-002] WHEN the user invokes `/aria:determine`, THEN the system shall activate the determination skill to evaluate whether the product qualifies as a medical device and determine initial classification.**

- Input: Product description, intended use, user population (via document analysis or conversational Q&A)
- Processing: Medical device determination checklist against FDA, EU MDR, and MFDS criteria
- Output: Determination result with traffic light status, applicable regulations, and rationale
- Verification: Test with 5+ product types (active, implantable, IVD, SaMD, non-active)

**[ER-003] WHEN the user invokes `/aria:classify`, THEN the system shall activate the classification skill to determine regulatory class across target regions.**

- Input: Device characteristics (from `/aria:determine` output or manual entry)
- Processing: FDA class (I/II/III) + EU MDR class (I/IIa/IIb/III) + MFDS class (1/2/3/4) matrix
- Output: Classification matrix with rationale, rule references, and traffic light per region
- Verification: Test with devices spanning all classification levels

**[ER-004] WHEN the user invokes `/aria:pathway`, THEN the system shall activate the pathway skill to identify regulatory submission pathways per country.**

- Input: Classification results (from `/aria:classify` or manual), target markets
- Processing: Country-specific pathway mapping (510(k)/PMA/De Novo for FDA, CE Marking routes for EU, MFDS authorization types)
- Output: Pathway comparison table with timelines, requirements, and recommendations
- Verification: Test multi-market scenarios (US-only, US+EU, US+EU+Korea)

**[ER-005] WHEN the user invokes `/aria:estimate`, THEN the system shall activate the estimation skill to provide cost and timeline frameworks.**

- Input: Pathway selection (from `/aria:pathway` or manual), device complexity
- Processing: Cost estimation framework (consulting, testing, regulatory fees, notified body) and timeline estimation
- Output: Structured estimate with ranges (optimistic/expected/pessimistic), cost breakdown, and milestone timeline
- Verification: Test with Class I vs Class III device scenarios

**[ER-006] WHEN the user invokes `/aria:plan`, THEN the system shall activate the planning skill to generate a regulatory milestone plan.**

- Input: Pathway and estimate data (from prior steps or manual)
- Processing: Regulatory milestone sequencing, dependency mapping, critical path identification
- Output: Milestone plan with phases, deliverables, dependencies, and checkpoints
- Verification: Test with single-market and multi-market scenarios

**[ER-007] WHEN the user invokes `/aria:compare`, THEN the system shall activate the comparison skill to compare regulations across multiple countries.**

- Input: Regulatory topic or requirement area, target countries
- Processing: Side-by-side comparison of regulatory requirements, key differences, harmonized standards
- Output: Comparison matrix with similarities, differences, and strategic recommendations
- Verification: Test FDA vs EU MDR vs MFDS for 3+ regulatory topics

**[ER-008] WHEN the user invokes `/aria:brief`, THEN the system shall activate the briefing skill to generate a comprehensive regulatory briefing report.**

- Input: All available product data from .aria/ directory, specific focus areas
- Processing: Synthesize determination, classification, pathway, estimates, and plan into executive briefing
- Output: Formatted briefing report with executive summary, detailed analysis, recommendations, and appendices
- Verification: Test with complete pipeline data and partial data scenarios

**[ER-009] WHEN any command completes execution, THEN the system shall display the top 1-3 most frequent next steps in the pipeline.**

- Rationale: Guide users through the natural regulatory workflow
- Processing: Determine current pipeline position, suggest logical next commands
- Output: Suggested next commands with brief descriptions (e.g., "Next: `/aria:classify` to determine device class")
- Verification: Each command shows appropriate next step suggestions

**[ER-010] WHEN data lookup is required, THEN the system shall follow the priority order: Notion DB first, built-in knowledge second, Context7 third.**

- Rationale: Organization-specific data takes priority, then skill-embedded summaries, then external supplementation
- Processing: Query Notion DB -> if insufficient, supplement with built-in -> use Context7 for verification/supplementation
- Output: Aggregated response with source attribution for each data element
- Verification: Test data retrieval with all three sources available, and with individual sources disabled
- Implementation Note: Notion and Context7 queries can run in parallel when both are available, with Notion results taking priority in final aggregation

**[ER-011] WHEN prior step data exists in `.aria/products/{product-name}/{date}/`, THEN the system shall auto-load that context for the current command.**

- Rationale: Pipeline continuity without requiring users to re-enter information
- Processing: Scan .aria/ directory for relevant prior step output, load as context. Context is loaded in compressed form (via Context Simplifier, S10) unless the command requires full prior step detail.
- Output: Pre-populated fields and contextual awareness in current command
- Verification: Test pipeline flow with and without prior step data
- Note: This requirement subsumes the pre-population behavior previously described in SR-003. See SR-003.

**[ER-012] WHEN the user provides input in multiple formats (file upload, URL, pasted text, interactive QA), THEN the system shall accept and process all formats equivalently.**

- Rationale: Flexibility for different user workflows and data sources
- Processing: Detect input format, normalize to internal representation
- Output: Consistent processing regardless of input format
- Verification: Test each input format for at least 2 commands

**[ER-013] IF a command is executed without prior pipeline data AND the user provides a technical document, THEN the system shall extract required information from the document first, then use conversational Q&A only for missing fields.**

- Rationale: Document-first workflow reduces user effort; technical documentation contains most required information
- Processing: Accept technical documentation (product specification, user manual, design document) as primary input. Extract device description, intended use, product form, primary function, and skill-specific fields via document analysis. Identify missing fields not extractable from document. Initiate targeted conversational Q&A only for genuinely missing fields. Optionally save collected data to .aria/ for future pipeline use.
- Output: Complete input data assembled from document extraction + targeted Q&A
- Verification: Test each command with a sample technical document; verify document extraction coverage and Q&A brevity

**[ER-014] WHEN the user provides a technical document (product specification, user manual, design document), THEN the system shall extract device description, intended use, product form, primary function, and all skill-specific fields automatically.**

- Rationale: Automated extraction from structured documents reduces manual input burden and improves data completeness
- Processing: Parse document structure, identify key sections (intended use, device description, specifications), extract relevant fields using document analysis
- Output: Structured data extracted from document, with confidence indicators for each field
- Verification: Test with 3+ document formats (product specification, user manual, IFU); verify extraction accuracy for core fields

**[ER-015] WHEN passing context from a completed pipeline step to the next step, THEN the system shall compress the previous step's output to key conclusions only, preserving decision outcomes, classification results, and critical data points while discarding verbose analysis text.**

- Rationale: Prevent token overconsumption from accumulated pipeline results; maintain context efficiency across multi-step workflows
- Processing: Apply Context Simplifier (S10) compression rules to completed step output before passing to next step
- Output: Compressed summary (~500 tokens max) containing decision outcome, key data points, traffic light status, source attribution summary, and escalation flags
- Verification: Compare token usage between compressed and uncompressed pipeline runs; verify no critical information loss

**[ER-016] WHEN a command is executed AND data older than the configured retention period exists in `.aria/products/`, THEN the system shall display a warning message about stale data without automatically deleting it.**

- Rationale: 보존기간 초과 데이터에 대해 사용자에게 인지시키되, 자동 삭제로 인한 데이터 손실을 방지한다
- Processing: 커맨드 실행 시 `.aria/products/` 내 날짜 디렉토리를 스캔하여 `aria.local.md`의 `data_retention_days` 설정과 비교. 초과 데이터가 있으면 경고 표시.
- Output: Warning message listing stale data directories with their ages
- Verification: Test with data directories older/newer than configured retention period
- Configuration: `aria.local.md`의 `data_retention_days` (default: 365일), `warn_on_stale_data` (default: true)

### State-Driven Requirements (If-Then)

**[SR-001] IF Notion MCP connection is unavailable, THEN the system shall gracefully degrade to built-in knowledge and Context7.**

- Rationale: System must remain functional without external database connectivity
- Processing: Detect MCP connection failure, fall back to built-in summaries, notify user of degraded mode
- Output: Results with "(built-in data)" attribution, recommendation to connect Notion for full accuracy
- Verification: Test all commands with Notion MCP disabled

**[SR-002] IF `aria.local.md` playbook exists in the user's project root, THEN the system shall load organization-specific configuration.**

- Rationale: Each organization has preferred pathways, standard positions, and custom criteria
- Content: Preferred regulatory pathways, standard classification positions, cost/timeline benchmarks, preferred consultants/notified bodies, risk tolerance levels, custom escalation criteria
- Processing: Parse aria.local.md and apply overrides to default skill behavior
- Verification: Test with and without aria.local.md present
- Clarification: `aria.local.md` is placed in the user's project root directory, not in the plugin directory

**[SR-003] See ER-011. (Pre-population of context from prior step data is handled by ER-011.)**

- Note: Previously a standalone requirement for pre-populating context. Merged into ER-011 to eliminate duplication.

**[SR-004] IF the user requests output in a specific format (Notion page, Google Docs, .docx), THEN the system shall generate the requested format via appropriate MCP connector.**

- Default: Markdown report
- Alternatives: Notion page (via Notion MCP), Google Docs (via Google Drive MCP), .docx (via conversion)
- Processing: Generate base Markdown, convert to requested format
- Verification: Test Markdown default and at least one alternative format

**[SR-005] IF a skill identifies a situation requiring expert human confirmation, THEN the system shall explicitly state the escalation recommendation.**

- Rationale: AI should not make final regulatory decisions in ambiguous cases
- Processing: Detect ambiguity, conflicting requirements, or high-risk scenarios
- Output: Clear escalation message with reasoning and suggested expert type
- Verification: Test with deliberately ambiguous regulatory scenarios

**[SR-006] IF multiple products exist in `.aria/products/`, THEN the system shall check `.aria/active_product.json` for the current active product. If the file does not exist or is stale, the system shall prompt the user to select the active product and persist the selection to `.aria/active_product.json`.**

- Rationale: Multi-product workflows require explicit product selection to prevent data crossover. File-based persistence (`active_product.json`)을 통해 Stateless 환경에서도 active product 상태를 유지한다.
- Processing: 커맨드 실행 시 `.aria/active_product.json`을 읽어 active product를 확인한다. 파일이 없거나 참조 경로가 유효하지 않으면, `.aria/products/`를 스캔하여 선택 메뉴를 표시하고 선택 결과를 `active_product.json`에 기록한다. 제품이 1개이면 자동 선택한다.
- Format: `active_product.json` 구조:
  ```json
  { "product_name": "cardiac-monitor-x1", "last_accessed": "2026-02-10", "path": ".aria/products/cardiac-monitor-x1/2026-02-10/" }
  ```
- Output: Active product context set for current and subsequent commands via file-based persistence
- Verification: Test with 0, 1, and 3+ products in `.aria/products/`; test `active_product.json` presence/absence/stale scenarios

**[SR-007] IF a command is executed for a product on a date where output already exists, THEN the system shall create a versioned output (e.g., `determination-v2.md`) rather than overwriting.**

- Rationale: Preserve audit trail and prevent accidental data loss from re-execution
- Processing: Check for existing output file; if present, increment version suffix
- Output: Versioned file (e.g., `determination-v2.md`, `classification-v3.md`)
- Verification: Test re-execution of same command for same product/date; verify versioning

**[SR-008] IF the user explicitly requests English output (via `--lang en` command flag or playbook setting), THEN the system shall switch all user-facing text to English while maintaining Korean regulatory term translations.**

- Rationale: Support international team collaboration while preserving regulatory term accuracy
- Processing: Detect English toggle from `--lang en` command flag or `aria.local.md` language preference field. Switch output language to English. Maintain Korean equivalents for regulatory terms where relevant (e.g., "의료기기 (medical device)").
- Flag format: `--lang en` (GNU 스타일 더블 하이픈, value flag)
- Output: English-language output with bilingual regulatory terms
- Verification: Test with `--lang en` flag enabled; verify language switch and term preservation

### Unwanted Behavior Requirements (Shall Not)

**[WR-001] The system shall not present any output as regulatory advice or legal guidance.**

- Prohibited: Phrases like "you should", "you must", "this is required" without disclaimer context
- Required: All outputs framed as "reference information for professional review"
- Verification: Content review of all command output templates

**[WR-002] The system shall not display more than 3 next step suggestions after command completion.**

- Prohibited: Overwhelming users with too many options
- Required: Curated top 1-3 most relevant next steps
- Verification: Post-completion suggestion count check across all commands

**[WR-003] The system shall not provide regulatory information without data source attribution.**

- Prohibited: Unsupported regulatory claims, uncited standards
- Required: Source name (Notion DB, built-in, Context7) and specific regulation reference where applicable
- Verification: Source attribution presence check on all outputs
- Note: Negative form of UR-003, retained for explicit prohibition

**[WR-004] The system shall not include tool call instructions or technical implementation details in skill definitions.**

- Prohibited: Direct MCP tool invocation syntax, API calls, function signatures in user-facing content
- Required: Declarative workflow steps only (Legal plugin pattern)
- Verification: Skill content review for technical implementation leakage

**[WR-005] The system shall not expose technical error messages to users.**

- Prohibited: Raw exception messages, stack traces, MCP error codes
- Required: Plain language explanation with suggested recovery action
- Verification: Error scenario testing with forced failures

### Optional Feature Requirements (Where Feature Exists)

**[OR-001] WHERE Google Drive MCP is configured, the system shall provide Google Docs export option.**

- Feature: Export regulatory reports as Google Docs
- Benefit: Integration with organization document management workflows
- Priority: Medium

**[OR-002] WHERE .docx conversion capability exists, the system shall provide Word document export option.**

- Feature: Export reports in .docx format for regulatory submission packages
- Benefit: Compatibility with regulatory authority submission requirements
- Priority: Medium

**[OR-003] WHERE additional MCP connectors become available, the system shall support future expansion through the CONNECTORS.md tool category documentation pattern.**

- Feature: Extensible MCP integration without core code changes
- Benefit: Future-proofing for new data sources and output targets
- Priority: Low

**[OR-004] WHERE the user explicitly requests classification optimization, the classification skill shall provide strategic suggestions on which product specifications or intended use modifications could potentially lower the regulatory class, with clear disclaimers that such modifications must be validated by regulatory professionals.**

- Feature: Opt-in classification optimization analysis
- Benefit: Strategic guidance on regulatory class reduction through product design modifications
- Processing: When invoked with `--optimize` flag, the classification skill shall:
  1. 등급 결정에 결정적 영향을 미친 핵심 결정 인자(Key Decision Factors)를 추출 (예: Invasiveness, Duration of Contact, Active/Passive, Intended Use Scope)
  2. 각 핵심 인자에 대한 변경 시나리오를 가이드 (예: "침습 등급을 낮추면 -> Class가 변경될 수 있음")
  3. 전체 역추론 로직을 빌트인에 포함하지 않고, 핵심 인자 기반 추상화된 가이드만 제공
- Traffic Light: All optimization suggestions are tagged with YELLOW (requires professional review)
- Escalation: Mandatory escalation recommendation for any suggested product modification
- Priority: Low
- Note: See S7.2 supplementary disclaimer for classification optimization

---

## Specifications

### S1: Plugin Structure

**[S1.1] Plugin Manifest**

File: `.claude-plugin/plugin.json`

```json
{
  "name": "aria",
  "version": "2.0.0",
  "description": "AI Regulatory Intelligence Assistant - Medical device regulatory compliance for US FDA, EU MDR, and Korea MFDS",
  "author": { "name": "ARIA Team" },
  "commands": ["./commands/"],
  "skills": ["./skills/"],
  "mcpServers": "./.mcp.json"
}
```

**[S1.2] Directory Structure**

```
aria/
+-- .claude-plugin/plugin.json        # Plugin manifest (S1.1)
+-- .mcp.json                         # MCP connector configuration (S1.3)
+-- CONNECTORS.md                     # Tool category documentation (S1.4)
+-- README.md                         # Installation/usage guide + aria.local.md template (S1.5)
+-- commands/                         # 8 slash commands (S2)
|   +-- chat.md                      # Free conversation (hybrid router) -> /aria:chat
|   +-- determine.md                  # Medical device determination -> /aria:determine
|   +-- classify.md                   # Device classification -> /aria:classify
|   +-- pathway.md                    # Regulatory pathway -> /aria:pathway
|   +-- estimate.md                   # Cost/timeline estimation -> /aria:estimate
|   +-- plan.md                       # Regulatory planning -> /aria:plan
|   +-- compare.md                    # Multi-country comparison -> /aria:compare
|   +-- brief.md                      # Regulatory briefing -> /aria:brief
+-- skills/                           # 7 domain skills (S3)
    +-- determination/SKILL.md        # Device determination logic
    +-- classification/SKILL.md       # Classification matrix
    +-- pathway/SKILL.md              # Pathway selection
    +-- estimation/SKILL.md           # Cost/timeline framework
    +-- planning/SKILL.md             # Milestone planning
    +-- comparison/SKILL.md           # Multi-country comparison
    +-- briefing/SKILL.md             # Briefing report generation
```

**[S1.3] MCP Configuration**

File: `.mcp.json`

```json
{
  "mcpServers": {
    "notion": {
      "command": "npx",
      "args": ["-y", "@notionhq/notion-mcp-server"],
      "env": {
        "NOTION_API_KEY": ""
      }
    },
    "gdrive": {
      "command": "npx",
      "args": ["-y", "@anthropic/google-drive-mcp"],
      "env": {
        "GOOGLE_CREDENTIALS": ""
      }
    },
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    }
  }
}
```

Note: Notion and Google Drive MCP package names must be verified against npm registry before Phase 1 implementation. The `@upstash/context7-mcp` is the verified package name for Context7.

**[S1.4] CONNECTORS.md**

Tool-agnostic category documentation for MCP connectors. Documents connector categories without prescribing specific tool calls:
- Database connectors (Notion)
- Storage connectors (Google Drive)
- Documentation connectors (Context7)
- Expandability guidelines for future connectors

**[S1.5] README.md**

Contents:
- ARIA overview and capabilities
- Installation instructions for Cowork plugin
- MCP connector setup guide (Notion API key, Google credentials)
- Command reference with examples (all commands use `/aria:` prefix)
- aria.local.md playbook template and configuration guide
- Troubleshooting and FAQ

### S2: Command System (8 Commands)

**[S2.1] Command Design Pattern (Legal Plugin Benchmark)**

All commands follow the minimal frontmatter pattern:
- `description`: Brief purpose description
- `argument-hint`: Expected input format

No `tools`, `model`, or `skills` fields in command frontmatter. Commands reference skills through declarative workflow steps, not direct tool invocations.

All commands are namespaced under the `aria` plugin prefix and invoked as `/aria:{command-name}`.

**Command Flag Standards**:
- 형식: `--flag-name` (GNU 스타일 더블 하이픈)
- 예시: `/aria:classify --optimize`, `/aria:classify --lang en`, `/aria:brief --format notion`
- `argument-hint`에 플래그 형식 포함: `argument-hint: "제품 설명 [--optimize] [--lang en|ko]"`
- Boolean 플래그: `--optimize` (값 없이 존재 여부로 판단)
- Value 플래그: `--lang en`, `--format notion` (키-값 쌍)

**[S2.2] Command-Skill Mapping**

| Command | Skill | Function | Flags | Legal Benchmark Pattern |
|---------|-------|----------|-------|------------------------|
| `/aria:chat` | (all skills routing) | Free conversation + auto skill selection | `--lang [ko\|en]` (SR-008) | (ARIA-unique hybrid router) |
| `/aria:determine` | determination | Device determination checklist + classification | `--lang [ko\|en]` (SR-008) | nda-triage pattern |
| `/aria:classify` | classification | FDA/EU/MFDS grade classification matrix | `--optimize` (OR-004), `--lang [ko\|en]` (SR-008) | legal-risk-assessment |
| `/aria:pathway` | pathway | Country-specific regulatory pathway comparison | `--lang [ko\|en]` (SR-008) | compliance pattern |
| `/aria:estimate` | estimation | Cost/timeline estimation framework | `--lang [ko\|en]` (SR-008) | contract-review pattern |
| `/aria:plan` | planning | Regulatory milestone planning | `--lang [ko\|en]` (SR-008) | meeting-briefing pattern |
| `/aria:compare` | comparison | Multi-country regulation comparison | `--lang [ko\|en]` (SR-008) | compliance pattern |
| `/aria:brief` | briefing | Regulatory briefing report generation | `--format [markdown\|notion\|gdocs]`, `--lang [ko\|en]` (SR-008) | meeting-briefing pattern |

**[S2.3] Pipeline Flow**

```
/aria:determine --> /aria:classify --> /aria:pathway --> /aria:estimate --> /aria:plan --> /aria:compare --> /aria:brief
```

- Each step is freely skippable; every command can run independently
- Each command reads from `.aria/` if prior step data exists
- Upon completion, each command suggests top 1-3 most relevant next steps

모든 커맨드는 실행 시작 시 `.aria/active_product.json`을 읽어 컨텍스트를 로드한다. 파일이 없으면 사용자에게 제품 선택을 요청한다 (SR-006 참조).

Note: Each command operates independently. When prior step data is absent, the command uses document analysis as the primary input method (if a document is provided), supplemented by targeted Q&A for missing information. Common required fields: Intended Use, Product Form, Primary Function, Device Description. Skill-specific fields are defined per skill implementation.

**[S2.4] /aria:chat Command (Hybrid Router)**

The `/aria:chat` command serves as the single entry point for free-form conversation:
- Keyword auto-detect for clear skill matches (e.g., "determine", "classify", "510(k)")
- Skill suggestion menu for ambiguous queries (present top 1-3 matching skills)
- Direct skill invocation when match confidence is high
- Conversational mode for general regulatory questions

### S3: Skill System (7 Skills)

**[S3.1] Skill Design Pattern (Legal Plugin Benchmark)**

All skills follow the minimal frontmatter pattern:
- `name`: Skill identifier
- `description`: Purpose description

Skill body contains:
- Built-in regulatory knowledge summary (~2,000-2,500 tokens)
- Declarative workflow steps (no tool call instructions)
- Structured output template
- Summary Generation 단계 (Context Simplifier용 압축 요약 출력)
- Escalation path definition ("when expert confirmation is needed")
- Disclaimer block

Built-in knowledge focuses on decision frameworks, classification logic, evaluation criteria, and judgment heuristics. Regulatory text (law articles, regulation body text, standard references) is NOT embedded in skills but retrieved via MCP connectors at runtime.

Each skill should declare its knowledge base date (e.g., "Knowledge base: 2026-01 기준") to indicate the currency of embedded decision logic.

Each SKILL.md must not exceed 500 lines (see C12).

**[S3.2] Skill Definitions**

**determination** (determination/SKILL.md)
- Purpose: Evaluate whether a product qualifies as a medical device under target regulations
- Knowledge: FDA device definition decision tree (21 CFR 201(h) criteria), EU MDR Article 2(1) classification logic, MFDS device criteria evaluation matrix
- Output: Determination checklist, YES/NO/CONDITIONAL result with traffic light, applicable regulations
- Escalation: When product is borderline (e.g., wellness vs medical device, combination products)

**classification** (classification/SKILL.md)
- Purpose: Determine regulatory class across all target regions
- Knowledge: FDA classification decision rules, EU MDR Annex VIII classification logic tree, MFDS classification evaluation criteria
- Output: Multi-region classification matrix (FDA I/II/III, EU I/IIa/IIb/III, MFDS 1/2/3/4)
- Escalation: When classification is ambiguous or spans multiple rules
- Opt-in Capability (OR-004): `--optimize` 플래그로 호출 시, 등급 결정의 핵심 결정 인자(Key Decision Factors: invasiveness, duration, active/passive, intended use scope)를 추출하고, 각 인자별 변경 시나리오를 가이드하는 방식으로 추상화한다. 전체 역추론 로직은 빌트인 토큰 예산(2,500 tokens) 내 구현이 비현실적이므로, 핵심 인자 기반 추상 가이드로 대체한다. Suggestions are framed as "if the intended use were narrowed to X, the classification might change to Y" with mandatory escalation recommendation.

**pathway** (pathway/SKILL.md)
- Purpose: Identify and compare regulatory submission pathways per country
- Knowledge: FDA pathway selection decision tree (510(k), PMA, De Novo, Exempt), EU MDR route evaluation criteria, MFDS authorization type selection logic
- Output: Pathway comparison table with requirements, timelines, and recommendations
- Escalation: When novel device type lacks clear predicate or pathway precedent

**estimation** (estimation/SKILL.md)
- Purpose: Provide cost and timeline estimation framework for regulatory submissions
- Knowledge: Standard fee range frameworks, typical timeline patterns by device class, cost category classification rules
- Output: Cost breakdown (optimistic/expected/pessimistic), timeline with milestones
- Escalation: When estimate requires organization-specific pricing or non-standard testing

**planning** (planning/SKILL.md)
- Purpose: Generate a regulatory milestone plan with phases and dependencies
- Knowledge: Standard regulatory milestone sequencing logic, critical path identification patterns, common bottleneck detection criteria
- Output: Phase-based plan with deliverables, dependencies, checkpoints, and responsible parties
- Escalation: When plan involves parallel multi-market submissions with complex dependencies

**comparison** (comparison/SKILL.md)
- Purpose: Compare regulatory requirements across multiple countries for specific topics
- Knowledge: Key regulatory difference evaluation framework across FDA, EU MDR, MFDS for major compliance areas
- Output: Side-by-side comparison matrix with similarities, differences, harmonized standards, and strategy
- Escalation: When comparison involves recently amended regulations or conflicting interpretations

**briefing** (briefing/SKILL.md)
- Purpose: Generate comprehensive regulatory briefing reports synthesizing all available data
- Knowledge: Briefing report structuring rules, executive summary generation criteria, regulatory strategy presentation framework
- Output: Formatted briefing with executive summary, detailed analysis, recommendations, and appendices
- Escalation: When briefing is for external stakeholders (board, investors, regulatory authorities)

### S4: Data Strategy

**[S4.1] Data Source Priority Order**

1. **Notion DB** (highest priority): Organization-specific detailed regulatory data, precedents, latest information
2. **Built-in Knowledge** (second): Skill-embedded decision frameworks and judgment logic (~2,000-2,500 tokens per skill)
3. **Context7** (third): Library/regulatory document supplementation and verification

**[S4.2] Data Lookup Flow**

```
Query received
  |
  v
[1] Search Notion DB          [3] Query Context7
  |-- Found: Use as primary       |-- Found: Supplement/verify
  |-- Not found: Continue          |-- Not found: Note limitations
  |                                |
  v                                v
[2] Use Built-in Knowledge    [4] Aggregate results with source attribution
  |-- Available: Use as baseline
  |-- Insufficient: Continue
```

Implementation Note: Notion and Context7 queries can run in parallel when both sources are available, with Notion results taking priority in final aggregation. Built-in knowledge is always available as the synchronous fallback.

**[S4.3] Graceful Degradation Matrix**

| Notion DB | Built-in | Context7 | System Status | User Notification |
|-----------|----------|----------|---------------|-------------------|
| Available | Available | Available | Full operation | None |
| Unavailable | Available | Available | Degraded (no org data) | "Organization database unavailable. Using general knowledge." |
| Available | Available | Unavailable | Degraded (no supplementation) | "External document verification unavailable." |
| Unavailable | Available | Unavailable | Minimal operation | "Operating with built-in knowledge only. Results may be less specific." |
| Unavailable | Unavailable | Unavailable | Error state | "Unable to access data sources. Please check connections." |

Note: When operating in degraded modes (rows 2-4), each output must include a visible limitation notice indicating which data sources are unavailable and how this affects result reliability. The limitation notice is distinct from the standard disclaimer (S7.2) and appears in the Data Source Attribution section of the output.

Explicit Assumption: Built-in knowledge is always available as it is embedded in skill definitions. Therefore, scenarios with "Built-in unavailable" are N/A (only possible if the skill file itself is corrupted, which is an installation error, not a runtime degradation scenario).

**[S4.4] Knowledge Architecture**

The system separates knowledge into two categories based on volatility and token efficiency:

**Built-in (embedded in skills)**:
- Decision trees and classification logic
- Classification rules and evaluation matrices
- Judgment criteria and heuristics
- Workflow logic and procedural steps
- Evaluation frameworks and scoring rubrics

**MCP-sourced (Notion/Context7 at runtime)**:
- Regulatory text and law citations (e.g., 21 CFR 201(h) full text)
- Standard references and regulation body text
- Current fee schedules and updated timelines
- Organization-specific precedents and decisions
- Recently amended regulations and interpretations

Rationale: Decision logic changes infrequently and benefits from being immediately available without network latency. Regulatory text changes more frequently, may be voluminous, and benefits from always-current retrieval from authoritative sources.

### S5: Output System

**[S5.1] Local Data Storage**

Path: `.aria/products/{product-name}/{date}/`

Product naming convention: lowercase, hyphens, alphanumeric only. Example: "Cardiac Monitor X1" -> `cardiac-monitor-x1`

```
.aria/
+-- active_product.json              # 현재 활성 제품 (Stateless 대응, SR-006)
+-- products/
    +-- cardiac-monitor-x1/
        +-- 2026-02-10/
            +-- determination.md              # /aria:determine output
            +-- determination.summary.md      # Compressed summary (Context Simplifier)
            +-- classification.md             # /aria:classify output
            +-- classification.summary.md     # Compressed summary
            +-- pathway.md                    # /aria:pathway output
            +-- pathway.summary.md            # Compressed summary
            +-- estimation.md                 # /aria:estimate output
            +-- estimation.summary.md         # Compressed summary
            +-- plan.md                       # /aria:plan output
            +-- plan.summary.md              # Compressed summary
            +-- comparison.md                 # /aria:compare output
            +-- comparison.summary.md         # Compressed summary
            +-- briefing.md                   # /aria:brief output
            +-- briefing.summary.md          # Compressed summary
```

Note: `.aria/` directory contents are user-managed. Manual deletion of product directories or date directories is the primary cleanup mechanism. No automated cleanup is provided to prevent accidental data loss.

**[S5.2] Output Format Options**

| Format | Method | Priority |
|--------|--------|----------|
| Markdown Report (default) | Direct file write to .aria/ | Primary |
| Notion Page | Notion MCP connector | Secondary |
| Google Docs | Google Drive MCP connector | Optional |
| .docx | Conversion from Markdown | Optional |

**[S5.3] Output Template Structure**

Every command output includes:
1. Header with command name, product, date, and version
2. Input summary (what was provided)
3. Analysis body (command-specific content)
4. Traffic light assessment (where applicable)
5. Data source attribution section
6. Escalation recommendations (if applicable)
7. Suggested next steps (top 1-3)
8. Disclaimer block

### S6: Playbook (aria.local.md)

**[S6.1] Purpose**

Organization-specific configuration file that customizes ARIA behavior based on organizational preferences, historical data, and strategic decisions.

**[S6.2] Content Structure**

```markdown
# ARIA Local Playbook

## Organization Profile
- Company name and regulatory department
- Primary device types manufactured
- Active markets

## Language Preference
- Output language: ko (default) | en

## Preferred Regulatory Pathways
- FDA: Default pathway preferences by device class
- EU MDR: Preferred notified bodies, certification approach
- MFDS: Standard authorization pathway

## Classification Positions
- Standard positions for recurring device types
- Historical classification decisions

## Cost/Timeline Benchmarks
- Historical project costs by device class
- Typical timeline actuals vs estimates
- Preferred testing laboratories

## Consultant/Notified Body Preferences
- Preferred regulatory consultants
- Preferred notified bodies (EU)
- Preferred testing/certification bodies

## Risk Tolerance
- Organization risk appetite (conservative/moderate/aggressive)
- Escalation triggers and thresholds

## Custom Escalation Criteria
- When to involve legal counsel
- When to engage external consultants
- Board notification thresholds

## Data Management
- data_retention_days: 365  # 보존기간 (일)
- warn_on_stale_data: true  # 보존기간 초과 데이터 경고
```

**[S6.3] Loading Behavior**

- ARIA checks for `aria.local.md` in the user's project root at command startup (not the plugin directory)
- If present: Load and apply configuration overrides to default skill behavior
- If absent: Use default skill behavior with no customization
- Template provided in README.md for easy initialization

### S7: Quality Framework

**[S7.1] VALID Framework**

| Pillar | Description | Implementation |
|--------|-------------|----------------|
| **V**erified | All claims verified against source regulations | Citation required for every regulatory assertion |
| **A**ccurate | Information matches current regulatory state | Notion DB for latest data, Context7 for supplementation |
| **L**inked | Traceability across all outputs | Cross-references between pipeline step outputs |
| **I**nspectable | Decision rationale is transparent | Audit trail in .aria/ output files |
| **D**eliverable | Output meets professional standards | Structured templates with consistent formatting |

Note: VALID framework is enforced through skill prompt instructions and output template structure. Enforcement is declarative (prompt-level), not programmatic. Each skill's SKILL.md includes the VALID checklist as part of its output generation workflow.

**[S7.2] Disclaimer**

Standard disclaimer text (included in every output):

```
---
Disclaimer: This output is AI-generated reference information for professional review.
It does not constitute regulatory advice, legal guidance, or official regulatory determination.
All regulatory decisions must be validated by qualified regulatory affairs professionals
and verified against current applicable regulations.
---
```

Supplementary disclaimer for classification optimization (OR-004):

```
---
Classification Optimization Disclaimer: Classification optimization suggestions are
exploratory scenarios only. Any product modification for regulatory classification purposes
must be validated by qualified regulatory affairs professionals and must not compromise
patient safety or device efficacy.
---
```

**[S7.3] Traffic Light System**

| Color | Meaning | Usage |
|-------|---------|-------|
| GREEN | Compliant / Clear pathway / Low risk | Device clearly meets criteria, straightforward pathway |
| YELLOW | Conditional / Requires attention / Medium risk | Ambiguous classification, additional testing may be needed |
| RED | Non-compliant / Blocked / High risk | Device does not meet criteria, significant regulatory barriers |

Note: Classification optimization suggestions (OR-004) are always tagged with YELLOW (requires professional review).

### S8: Design Patterns (from Legal Plugin Benchmarking)

**[S8.1] Pattern Catalog**

| Pattern | Description | Application in ARIA |
|---------|-------------|---------------------|
| Minimal Frontmatter | Skills: name+description only. Commands: description+argument-hint only | All 7 skills and 8 commands |
| Traffic Light System | GREEN/YELLOW/RED risk indicators | Regulatory risk assessment in all applicable commands |
| Disclaimer | Standard disclaimer on all outputs | VALID framework integration |
| Playbook | Local configuration for organization-specific behavior | aria.local.md |
| Graceful Degradation | Works without external connections | Built-in knowledge fallback |
| Declarative Workflows | No tool call instructions in skills, only procedural steps | All skill definitions |
| Escalation Paths | Each step defines when expert confirmation is needed | All 7 skills |
| Structured Output Templates | Consistent report format across all commands | Output template (S5.3) |
| Multi-format Input | File upload, URL, pasted text, interactive QA | All commands accept multiple input formats |
| Tool-agnostic Connectors | Category documentation, not tool-specific | CONNECTORS.md |
| Document-First Input | Technical documents as primary input source | Document analysis before Q&A (S9) |
| Context Compression | Compressed summaries for pipeline context passing | Context Simplifier (S10) |

**[S8.2] Architecture Decision: Commands + Skills Only**

ARIA intentionally uses no agent definitions, following the Legal plugin benchmark pattern. All domain logic resides in skills, invoked through commands.

- Rationale: Simplicity and alignment with Cowork plugin conventions; skills handle domain logic declaratively
- Contingency: If commands + skills alone cannot deliver sufficient interaction quality after Phase 2 implementation, the following agents may be introduced:
  - Device Description Extraction Agent: Interactive Q&A specialist for building complete device profiles
  - Planning Agent: Complex multi-market regulatory strategy coordination
- Measurable Criteria for Agent Introduction Decision:
  - If document analysis + targeted Q&A requires more than 5 rounds to collect minimum input for any single command
  - If hybrid routing accuracy falls below 80% on diverse test queries (20+ queries across 7 domains)
  - If user testing reveals consistent confusion about pipeline progression (3+ users report same issue)
- Decision Point: Evaluate after Phase 2 (Foundation Skills) implementation

### S9: Input Processing System

**[S9.1] Document Analysis Pipeline**

The system accepts technical documents as the primary input method for all commands:
- Supported document types: Product specifications, user manuals, design documents, IFU (Instructions for Use), technical files
- Input methods: File upload, pasted text, URL reference
- Extraction targets: Device description, intended use, product form, primary function, and all skill-specific fields (e.g., invasiveness level, duration of contact, active/passive status)
- Processing: Parse document structure, identify key sections, extract relevant fields with confidence indicators

대용량 문서(의료기기 기술문서 등 수백 페이지 규모) 처리 시:
1단계: 목차(Table of Contents) 우선 분석
2단계: 의도된 용도(Intended Use), 제품 사양(Specification), 제품 설명(Device Description) 섹션 식별
3단계: 식별된 핵심 섹션만 선택적 추출하여 분석
4단계: 추출 불가 시 사용자에게 해당 섹션 직접 입력 요청

이 접근은 전체 문서를 컨텍스트 윈도우에 로드하는 것보다 토큰 효율적이며, 의료기기 기술문서의 표준 구조(IEC 62366, ISO 14971 등)를 활용한다.

**[S9.2] Gap Detection**

After document analysis, the system identifies which required fields were not extractable:
- Compare extracted fields against the active command's required field list
- Generate a gap report listing missing fields with their importance level
- Prioritize gaps by criticality (required for output vs. optional enhancement)

**[S9.3] Targeted Q&A**

For fields not extractable from the document, initiate focused conversational Q&A:
- Ask only about genuinely missing fields (not fields already extracted)
- Group related questions to minimize interaction rounds
- Provide context from document analysis to help users answer quickly
- Target: 1-3 Q&A rounds maximum for any single command

Note: If the Q&A session times out or the user provides partial data, the system should persist the partially collected data to `.aria/` and indicate which fields are still missing in the output.

**[S9.4] Input Data Persistence**

All collected input data (from document analysis + Q&A) is saved to `.aria/`:
- Extracted data saved alongside command output
- Enables reuse by subsequent pipeline commands
- Format: Structured Markdown with field labels and confidence indicators

### S10: Context Simplifier

**[S10.1] Purpose**

Prevent token overconsumption from accumulated pipeline results when passing context between commands. Each pipeline step may generate 2,000-5,000 tokens of output; without compression, a full pipeline would consume 14,000-35,000 tokens of prior context.

각 스킬은 자신의 출력 템플릿 마지막 단계에 'Summary Generation' 단계를 포함한다. 각 스킬이 정규 출력(full output)과 압축 요약(summary)을 동시에 생성한다.

**[S10.2] Compression Rules**

Each step output is compressed to a structured summary (max ~500 tokens) containing:
- **Decision outcome**: Primary result (e.g., "Medical device: YES", "FDA Class II")
- **Key data points**: Critical facts that downstream commands need
- **Traffic light status**: GREEN/YELLOW/RED assessment
- **Source attribution summary**: Which sources informed the decision
- **Escalation flags**: Any escalation recommendations carried forward

요약 생성 책임은 각 개별 스킬에 있으며, 별도의 요약 전용 에이전트나 스킬은 사용하지 않는다. 스킬의 SKILL.md 출력 템플릿에 Summary Generation 섹션이 반드시 포함되어야 한다.

Discarded in compression:
- Verbose analysis text and reasoning chains
- Detailed regulatory citations (available in full output)
- Formatting and template boilerplate

**[S10.3] Storage**

Compressed summaries stored alongside full outputs in `.aria/`:
- Naming: `{step}.summary.md` alongside `{step}.md`
- Example: `determination.summary.md` alongside `determination.md`
- Full output always preserved for audit trail and on-demand access

**[S10.4] Loading Priority**

- Next step loads compressed summary by default
- Full output available on-demand if deeper context is needed (e.g., briefing command synthesizing all data)
- Commands can specify whether they need summary or full context per prior step

### S11: Security Considerations

**[S11.1] Data Classification**

`.aria/` contents may contain trade secrets and proprietary device designs:
- Recommend adding `.aria/` to `.gitignore` in project setup instructions
- Include warning in README.md about sensitive data in `.aria/` directory
- Each command output header notes data classification level

**[S11.2] MCP Credential Management**

- All MCP credentials (Notion API key, Google credentials) stored as environment variables
- Never stored in committed files or plugin configuration
- `.mcp.json` references environment variable placeholders, not actual values
- README.md provides secure credential setup instructions

**[S11.3] Audit Trail**

- `.aria/` Markdown files serve as audit trail for regulatory decision support
- Recommend treating as confidential organizational records
- Versioned outputs (SR-007) preserve decision history

**[S11.4] Data Retention**

Note: Regulatory data retention requirements vary by jurisdiction:
- FDA: Minimum 2 years after device discontinuation
- EU MDR: 10 years (15 years for implantable devices) after last device placed on market
- MFDS: Per Korean Medical Devices Act retention requirements
- Users are responsible for implementing appropriate retention policies for `.aria/` data

각 커맨드 실행 시 `.aria/products/` 내 보존기간(`aria.local.md`의 `data_retention_days` 설정) 초과 데이터가 있으면 경고 메시지를 표시한다. 자동 삭제는 수행하지 않으며, 전용 데이터 관리 커맨드는 Phase 6 이후 사용자 피드백에 따라 도입을 검토한다.

---

## Implementation Phases

### Phase 1: Plugin Scaffold + Core Infrastructure (Priority: Primary)

**Objective**: Establish plugin foundation recognized by Cowork platform

**Deliverables**:
- `.claude-plugin/plugin.json` (plugin manifest with component path declarations)
- `.mcp.json` (MCP connector configuration with verified package names)
- `CONNECTORS.md` (tool category documentation)
- `README.md` (installation/usage guide with aria.local.md template, `/aria:` command references)
- `aria.local.md` template

**Success Criteria**:
- Plugin recognized by Cowork platform
- MCP configuration validates without errors
- All MCP package names verified against npm registry
- README provides complete setup instructions with `/aria:` namespaced commands

### Phase 2: Foundation Skills + Commands (Priority: Primary)

**Objective**: Implement determination and classification capabilities

**Deliverables**:
- `skills/determination/SKILL.md` (device determination skill)
- `skills/classification/SKILL.md` (device classification skill)
- `commands/determine.md` (`/aria:determine` command)
- `commands/classify.md` (`/aria:classify` command)
- `.aria/` directory structure for local data storage
- Document analysis pipeline (S9) for determination and classification inputs

**Dependencies**: Phase 1 complete

**Success Criteria**:
- `/aria:determine` correctly evaluates medical device status for 5+ product types
- `/aria:classify` generates multi-region classification matrix (FDA, EU MDR, MFDS)
- Traffic light system operational on both commands
- Output stored in .aria/products/ structure with compressed summaries
- Graceful degradation functional when Notion unavailable
- Document-first input workflow operational for both commands

### Phase 3: Pathway Skills + Commands (Priority: Secondary)

**Objective**: Implement regulatory pathway, estimation, and planning capabilities

**Deliverables**:
- `skills/pathway/SKILL.md` (regulatory pathway skill)
- `skills/estimation/SKILL.md` (cost/timeline estimation skill)
- `skills/planning/SKILL.md` (regulatory planning skill)
- `commands/pathway.md` (`/aria:pathway` command)
- `commands/estimate.md` (`/aria:estimate` command)
- `commands/plan.md` (`/aria:plan` command)

**Dependencies**: Phase 2 complete (classification data informs pathways)

**Success Criteria**:
- `/aria:pathway` identifies correct pathways for all target regions
- `/aria:estimate` provides structured cost/timeline frameworks
- `/aria:plan` generates milestone plans with dependencies
- Pipeline data flow from Phase 2 commands works correctly via Context Simplifier
- Next step suggestions display after each command

### Phase 4: Analysis Skills + Commands (Priority: Secondary)

**Objective**: Implement comparison and briefing capabilities

**Deliverables**:
- `skills/comparison/SKILL.md` (multi-country comparison skill)
- `skills/briefing/SKILL.md` (regulatory briefing skill)
- `commands/compare.md` (`/aria:compare` command)
- `commands/brief.md` (`/aria:brief` command)

**Dependencies**: Phase 3 complete (plan data informs briefings)

**Success Criteria**:
- `/aria:compare` generates accurate multi-country comparison matrices
- `/aria:brief` synthesizes all pipeline data into executive briefing
- Full pipeline flow from `/aria:determine` through `/aria:brief` operational
- Briefing quality meets VALID framework standards

### Phase 5: Router Command + Workflow Integration (Priority: Secondary)

**Objective**: Implement the `/aria:chat` hybrid router and full pipeline integration

**Deliverables**:
- `commands/chat.md` (`/aria:chat` free conversation command with hybrid routing)
- Pipeline integration testing and optimization
- Cross-command context sharing validation via Context Simplifier
- Multi-product selection workflow (SR-006)

**Dependencies**: Phase 4 complete (all skills available for routing)

**Success Criteria**:
- `/aria:chat` correctly routes clear queries to appropriate skills
- `/aria:chat` presents skill suggestions for ambiguous queries
- Full pipeline flow seamless with auto-context loading
- All 8 commands operational and independently executable
- Multi-product selection functional

### Phase 6: Data Pipeline + Output Options (Priority: Final)

**Objective**: Complete Notion DB integration, Context7 supplementation, and multi-format output

**Deliverables**:
- Notion DB data lookup integration (primary data source)
- Context7 supplementation integration
- Google Drive output connector
- aria.local.md playbook parsing and application (including language preference)
- Multi-format output (Markdown default, Notion page, Google Docs)
- English output toggle (SR-008)

**Dependencies**: Phase 5 complete

**Success Criteria**:
- Notion DB lookup operational as primary data source
- Context7 supplementation and verification functional
- Data source priority order (Notion -> built-in -> Context7) enforced
- Graceful degradation matrix fully operational (S4.3)
- aria.local.md customization applied correctly
- At least Markdown and Notion page output formats working
- English toggle functional when enabled

---

## Dependencies

### External Dependencies

- **Anthropic Cowork Platform**: Plugin hosting and API
- **Notion MCP**: Organization regulatory database connectivity
- **Google Drive MCP**: Document storage and export
- **Context7 MCP**: Library and regulatory document lookup

### Internal Dependencies

- **Existing ARIA System**: Source material for 7 skills (9 existing skills with 22 modules merging into 7 skills)
- **Legal Plugin Reference**: Design pattern benchmark from knowledge-work-plugins
- **VALID Quality Framework**: Quality gate definitions

### Phase Dependencies

```
Phase 1 (scaffold) --- mandatory --> Phase 2 (foundation)
Phase 2 (foundation) -- mandatory --> Phase 3 (pathway)
Phase 3 (pathway) ---- mandatory --> Phase 4 (analysis)
Phase 4 (analysis) ---- mandatory --> Phase 5 (router)
Phase 5 (router) ------ mandatory --> Phase 6 (data pipeline)
```

---

## Constraints

### Technical Constraints

- [C1] Plugin structure must comply with Anthropic Cowork Plugin specification
- [C2] Commands must use minimal frontmatter (description + argument-hint only)
- [C3] Skills must use minimal frontmatter (name + description only)
- [C4] Skill body must not contain tool call instructions (declarative workflows only)
- [C5] Built-in knowledge per skill limited to approximately 2,000-2,500 tokens, focused on decision logic and judgment frameworks. Regulatory text retrieved from MCP sources.
- [C6] All user-facing output must be Korean (with optional English toggle via SR-008)

### Domain Constraints

- [C7] All regulatory information must include source attribution
- [C8] Disclaimer must appear on every output
- [C9] Traffic light system must use exactly three levels (GREEN/YELLOW/RED)
- [C10] Escalation paths must be defined for every skill

### Distribution Constraints

- [C11] Public GitHub repository distribution
- [C12] Each SKILL.md must not exceed 500 lines
- [C13] Organization internal use first, no marketplace initially
- [C14] README must provide complete self-service installation guide

---

## Risks and Mitigation

### Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Cowork Plugin API differs from expected pattern | Medium | High | Early Phase 1 validation; follow knowledge-work-plugins reference closely |
| MCP connector configuration incompatible | Low | High | Test each connector independently in Phase 6; verify npm package names in Phase 1 |
| Built-in knowledge token budget insufficient for decision logic | Medium | Medium | Aggressive summarization of decision frameworks; prioritize most-used classification rules |
| Pipeline context passing between commands unreliable | Medium | Medium | Robust .aria/ file reading with fallback to manual input; Context Simplifier (S10) for efficient context passing |
| Document analysis extraction accuracy insufficient | Medium | Medium | Targeted Q&A as fallback; iterative improvement of extraction patterns |

### Domain Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Regulatory information becomes outdated | Medium | High | Notion DB as primary source; Context7 supplementation; date-stamped outputs; knowledge base dates in skills |
| Classification logic incorrect for edge cases | Medium | High | Conservative approach with YELLOW traffic light; mandatory escalation path |
| Multi-country comparison inaccurate | Low | High | Source attribution per data point; built-in knowledge reviewed by domain expert |
| Cost estimates wildly inaccurate | High | Medium | Always present as ranges; disclaimer emphasis; playbook overrides |

### User Experience Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Users treat AI output as definitive regulatory advice | High | Critical | Prominent disclaimer; YELLOW/RED escalation paths; playbook for org governance |
| Pipeline too rigid for experienced users | Medium | Low | All commands independently executable; steps freely skippable |
| Hybrid router misroutes queries | Medium | Medium | Suggestion menu for ambiguous cases; always allow direct command access |
| Document analysis fails to extract key fields | Medium | Medium | Targeted Q&A fallback; confidence indicators on extracted fields |
| Token overconsumption in long pipelines | Medium | Medium | Context Simplifier (S10) compression; summary-first loading |

---

## Success Criteria

### Functional Success

- [FS-01] All 8 commands (`/aria:chat`, `/aria:determine`, `/aria:classify`, `/aria:pathway`, `/aria:estimate`, `/aria:plan`, `/aria:compare`, `/aria:brief`) operational
- [FS-02] All 7 skills (determination, classification, pathway, estimation, planning, comparison, briefing) produce accurate output
- [FS-03] Pipeline flow from `/aria:determine` through `/aria:brief` works with auto-context loading via Context Simplifier
- [FS-04] Each command works independently without prior steps
- [FS-05] `/aria:chat` hybrid router correctly handles clear matches and ambiguous queries
- [FS-06] Document-first input workflow operational for all commands (S9)
- [FS-07] Context Simplifier compresses pipeline context within ~500 token budget (S10)
- [FS-08] Multi-product selection functional when multiple products exist (SR-006)
- [FS-09] Output versioning prevents overwriting of existing outputs (SR-007)

### Quality Success

- [QS-01] VALID framework enforced on all outputs
- [QS-02] Disclaimer present on every output
- [QS-03] Traffic light system applied consistently
- [QS-04] Data source attribution on all regulatory information
- [QS-05] All escalation paths defined and triggered appropriately
- [QS-06] All SKILL.md files within 500-line limit (C12)

### Data Success

- [DS-01] Notion DB lookup operational as primary data source
- [DS-02] Graceful degradation matrix (S4.3) fully functional
- [DS-03] Data priority order (Notion -> built-in -> Context7) enforced
- [DS-04] .aria/ local storage working for all commands with compressed summaries
- [DS-05] Built-in knowledge correctly separated: decision logic embedded, regulatory text retrieved at runtime

### Integration Success

- [IS-01] Plugin recognized by Cowork platform
- [IS-02] Notion MCP connector functional
- [IS-03] Context7 MCP connector functional
- [IS-04] Google Drive MCP connector functional (for output)
- [IS-05] aria.local.md playbook parsing operational (including language preference)
- [IS-06] English output toggle functional (SR-008)

---

## Traceability

### Requirement-to-Specification Mapping

| Requirement | Specification | Phase | Verification |
|-------------|---------------|-------|--------------|
| UR-001 (Korean responses) | S2.1, S3.1, S5.3 | 1-6 | Language check on all outputs |
| UR-002 (Disclaimer) | S5.3, S7.2 | 1-6 | Disclaimer presence check |
| UR-003 (Source attribution) | S4.1, S4.2, S5.3 | 2-6 | Attribution presence check |
| UR-004 (VALID framework) | S7.1 | 2-6 | VALID checklist validation |
| UR-005 (Traffic light) | S7.3 | 2-6 | Color system consistency check |
| UR-006 (Data storage path) | S5.1 | 2-6 | Path convention validation |
| ER-001 (/aria:chat routing) | S2.4 | 5 | Routing accuracy test |
| ER-002 (/aria:determine) | S2.2, S3.2 | 2 | Determination accuracy test |
| ER-003 (/aria:classify) | S2.2, S3.2 | 2 | Classification matrix test |
| ER-004 (/aria:pathway) | S2.2, S3.2 | 3 | Pathway identification test |
| ER-005 (/aria:estimate) | S2.2, S3.2 | 3 | Estimation framework test |
| ER-006 (/aria:plan) | S2.2, S3.2 | 3 | Planning output test |
| ER-007 (/aria:compare) | S2.2, S3.2 | 4 | Comparison matrix test |
| ER-008 (/aria:brief) | S2.2, S3.2 | 4 | Briefing report test |
| ER-009 (Next steps) | S2.3, S5.3 | 2-6 | Post-completion suggestion test |
| ER-010 (Data priority) | S4.1, S4.2 | 6 | Data source order test |
| ER-011 (Auto-load context) | S5.1, S10 | 2-6 | Pipeline context test |
| ER-012 (Multi-format input) | S2.1, S9 | 2-6 | Input format test |
| ER-013 (Document-first input) | S9.1, S9.2, S9.3 | 2-6 | Document extraction + Q&A test |
| ER-014 (Document extraction) | S9.1, S9.4 | 2-6 | Extraction accuracy test |
| ER-015 (Context compression) | S10.1, S10.2, S10.3 | 2-6 | Token reduction test |
| ER-016 (Stale data warning) | S6.2, S11.4 | 2-6 | Retention period warning test |
| SR-001 (Graceful degradation) | S4.3 | 6 | Degradation matrix test |
| SR-002 (Playbook loading) | S6 | 6 | Playbook configuration test |
| SR-003 (See ER-011) | S5.1, S10 | 2-6 | See ER-011 |
| SR-004 (Output formats) | S5.2 | 6 | Format conversion test |
| SR-005 (Escalation) | S3.2 | 2-6 | Escalation trigger test |
| SR-006 (Multi-product) | S5.1 | 5 | Product selection test |
| SR-007 (Output versioning) | S5.1 | 2-6 | Version file creation test |
| SR-008 (English toggle) | S6.2, S2.1 | 6 | Language switch test |
| WR-001 (No regulatory advice) | S7.2 | 1-6 | Content review |
| WR-002 (Max 3 next steps) | S2.3 | 2-6 | Suggestion count check |
| WR-003 (Source attribution) | S4.1 | 2-6 | Attribution presence check |
| WR-004 (No tool calls in skills) | S3.1 | 2-6 | Skill content review |
| WR-005 (No technical errors) | S8.1 | 1-6 | Error handling test |
| OR-001 (Google Drive export) | S5.2 | 6 | Export format test |
| OR-002 (.docx export) | S5.2 | 6 | Export format test |
| OR-003 (Extensible connectors) | S1.4 | 6 | Connector expansion test |
| OR-004 (Classification optimization) | S3.2, S7.2, S7.3 | 2-6 | Optimization scenario test |

### Specification-to-Requirement Reverse Mapping

| Specification | Requirements Served |
|---------------|-------------------|
| S1 (Plugin Structure) | C1, IS-01 |
| S2 (Command System) | ER-001 through ER-009, WR-002 |
| S3 (Skill System) | ER-002 through ER-008, SR-005, WR-004, OR-004, C12 |
| S4 (Data Strategy) | ER-010, SR-001, UR-003 |
| S5 (Output System) | UR-006, SR-004, SR-006, SR-007 |
| S6 (Playbook) | SR-002, SR-008 |
| S7 (Quality Framework) | UR-002, UR-004, UR-005, OR-004 |
| S8 (Design Patterns) | WR-004, WR-005, ER-012 |
| S9 (Input Processing) | ER-012, ER-013, ER-014 |
| S10 (Context Simplifier) | ER-011, ER-015 |
| S11 (Security) | S11.1-S11.4 (security best practices) |

### VALID Quality Framework Traceability

**V**erified:
- Regulatory citations verified via data source priority (UR-003, S4.1, S4.2)
- Traffic light system validated per assessment (UR-005, S7.3)

**A**ccurate:
- Notion DB as primary source for latest data (S4.1)
- Context7 for supplementation and verification (S4.1)
- Graceful degradation when sources unavailable (SR-001, S4.3)
- Knowledge base dates declared in skills (S3.1)

**L**inked:
- Pipeline data flow across commands (ER-011, S5.1)
- Cross-references between step outputs (S5.3)
- Context Simplifier preserves traceability (S10)
- Traceability matrix above

**I**nspectable:
- Audit trail via .aria/ Markdown files (UR-006, S5.1)
- Data source attribution on every output (UR-003)
- Escalation reasoning documented (SR-005)
- Versioned outputs for decision history (SR-007)

**D**eliverable:
- Structured output templates (S5.3)
- Multi-format export (S5.2)
- VALID checklist enforcement (S7.1)
- Document-first input reduces user burden (S9)

---

## References

### Design References

- **Knowledge-Work-Plugins (Legal Plugin)**: Design pattern benchmark for Cowork plugin architecture
- **Existing ARIA System**: Source for domain knowledge, agent logic, and skill content

### Regulatory References

- FDA 21 CFR Part 820: Quality System Regulation
- FDA 21 CFR Part 807: Establishment Registration and Device Listing
- FDA 21 CFR Part 860: Medical Device Classification Procedures
- EU MDR 2017/745: Medical Device Regulation
- EU IVDR 2017/746: In Vitro Diagnostic Regulation
- Korea MFDS Medical Devices Act
- ISO 13485:2016: Medical devices - Quality management systems
- ISO 14971:2019: Medical devices - Application of risk management
- IEC 62304:2006+A1:2015: Medical device software - Software life cycle processes
- IEC 62366-1:2015: Medical devices - Usability engineering

### Existing System References (Source for Refactoring)

- 8 domain expert agents converting to 7 skills (no separate agents)
- 9 domain skills with 22 modules merging by function into 7 skills
- VALID quality framework maintained
- Notion DB integration maintained as primary data source

### Future Considerations

- **OR-005 (Regulatory Term Glossary)**: WHERE a regulatory term glossary feature is implemented, the system shall provide inline term definitions and cross-regional term mapping. Priority: Low. Deferred to post-Phase 6.
