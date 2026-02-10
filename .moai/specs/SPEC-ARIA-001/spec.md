# SPEC-ARIA-001: ARIA Cowork Plugin - Full System Refactoring

## TAG BLOCK

```yaml
SPEC_ID: SPEC-ARIA-001
TITLE: ARIA Cowork Plugin - Full System Refactoring
VERSION: 2.0.0
STATUS: Planned
PRIORITY: High
DOMAIN: aria-plugin
CREATED: 2026-02-10
AUTHOR: ARIA Architect
ASSIGNED: manager-spec
RELATED_SPECS: []
LIFECYCLE: spec-anchored
TAGS: [aria, cowork, plugin, regulatory, medical-device, refactoring]
```

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
**Language**: Korean (primary user-facing), English (optional toggle)
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
- [A7] Built-in knowledge summaries of approximately 2,000-2,500 tokens per skill are sufficient for standalone operation

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

**[ER-001] WHEN the user invokes `/aria` with a free-form query, THEN the system shall route to the appropriate skill using hybrid detection (keyword auto-detect for clear matches, skill suggestion menu for ambiguous cases).**

- Input: Natural language query in Korean or English
- Processing: Keyword matching against skill domains; if ambiguous, present top 1-3 skill suggestions
- Output: Routed skill execution or disambiguation menu
- Verification: Test with 20+ diverse queries across all 7 skill domains

**[ER-002] WHEN the user invokes `/determine`, THEN the system shall activate the determination skill to evaluate whether the product qualifies as a medical device and determine initial classification.**

- Input: Product description, intended use, user population
- Processing: Medical device determination checklist against FDA, EU MDR, and MFDS criteria
- Output: Determination result with traffic light status, applicable regulations, and rationale
- Verification: Test with 5+ product types (active, implantable, IVD, SaMD, non-active)

**[ER-003] WHEN the user invokes `/classify`, THEN the system shall activate the classification skill to determine regulatory class across target regions.**

- Input: Device characteristics (from /determine output or manual entry)
- Processing: FDA class (I/II/III) + EU MDR class (I/IIa/IIb/III) + MFDS class (1/2/3/4) matrix
- Output: Classification matrix with rationale, rule references, and traffic light per region
- Verification: Test with devices spanning all classification levels

**[ER-004] WHEN the user invokes `/pathway`, THEN the system shall activate the pathway skill to identify regulatory submission pathways per country.**

- Input: Classification results (from /classify or manual), target markets
- Processing: Country-specific pathway mapping (510(k)/PMA/De Novo for FDA, CE Marking routes for EU, MFDS authorization types)
- Output: Pathway comparison table with timelines, requirements, and recommendations
- Verification: Test multi-market scenarios (US-only, US+EU, US+EU+Korea)

**[ER-005] WHEN the user invokes `/estimate`, THEN the system shall activate the estimation skill to provide cost and timeline frameworks.**

- Input: Pathway selection (from /pathway or manual), device complexity
- Processing: Cost estimation framework (consulting, testing, regulatory fees, notified body) and timeline estimation
- Output: Structured estimate with ranges (optimistic/expected/pessimistic), cost breakdown, and milestone timeline
- Verification: Test with Class I vs Class III device scenarios

**[ER-006] WHEN the user invokes `/plan`, THEN the system shall activate the planning skill to generate a regulatory milestone plan.**

- Input: Pathway and estimate data (from prior steps or manual)
- Processing: Regulatory milestone sequencing, dependency mapping, critical path identification
- Output: Milestone plan with phases, deliverables, dependencies, and checkpoints
- Verification: Test with single-market and multi-market scenarios

**[ER-007] WHEN the user invokes `/compare`, THEN the system shall activate the comparison skill to compare regulations across multiple countries.**

- Input: Regulatory topic or requirement area, target countries
- Processing: Side-by-side comparison of regulatory requirements, key differences, harmonized standards
- Output: Comparison matrix with similarities, differences, and strategic recommendations
- Verification: Test FDA vs EU MDR vs MFDS for 3+ regulatory topics

**[ER-008] WHEN the user invokes `/brief`, THEN the system shall activate the briefing skill to generate a comprehensive regulatory briefing report.**

- Input: All available product data from .aria/ directory, specific focus areas
- Processing: Synthesize determination, classification, pathway, estimates, and plan into executive briefing
- Output: Formatted briefing report with executive summary, detailed analysis, recommendations, and appendices
- Verification: Test with complete pipeline data and partial data scenarios

**[ER-009] WHEN any command completes execution, THEN the system shall display the top 1-3 most frequent next steps in the pipeline.**

- Rationale: Guide users through the natural regulatory workflow
- Processing: Determine current pipeline position, suggest logical next commands
- Output: Suggested next commands with brief descriptions (e.g., "Next: /classify to determine device class")
- Verification: Each command shows appropriate next step suggestions

**[ER-010] WHEN data lookup is required, THEN the system shall follow the priority order: Notion DB first, built-in knowledge second, Context7 third.**

- Rationale: Organization-specific data takes priority, then skill-embedded summaries, then external supplementation
- Processing: Query Notion DB -> if insufficient, supplement with built-in -> use Context7 for verification/supplementation
- Output: Aggregated response with source attribution for each data element
- Verification: Test data retrieval with all three sources available, and with individual sources disabled

**[ER-011] WHEN prior step data exists in `.aria/products/{product-name}/{date}/`, THEN the system shall auto-load that context for the current command.**

- Rationale: Pipeline continuity without requiring users to re-enter information
- Processing: Scan .aria/ directory for relevant prior step output, load as context
- Output: Pre-populated fields and contextual awareness in current command
- Verification: Test pipeline flow with and without prior step data

**[ER-012] WHEN the user provides input in multiple formats (file upload, URL, pasted text, interactive QA), THEN the system shall accept and process all formats equivalently.**

- Rationale: Flexibility for different user workflows and data sources
- Processing: Detect input format, normalize to internal representation
- Output: Consistent processing regardless of input format
- Verification: Test each input format for at least 2 commands

**[ER-013] WHEN a command is executed without prior pipeline data in `.aria/`, THEN the system shall initiate conversational information extraction to collect the minimum required input for that command.**

- Rationale: Each command must deliver baseline quality independently; pipeline data is supplementary, not mandatory
- Processing: Check .aria/ for prior data; if missing, use interactive Q&A to gather: Intended Use, Product Form, Primary Function, Device Description, plus skill-specific fields
- Output: Collected information used as command input; optionally saved to .aria/ for future pipeline use
- Verification: Test each command with empty .aria/ directory; verify Q&A flow collects sufficient information

### State-Driven Requirements (If-Then)

**[SR-001] IF Notion MCP connection is unavailable, THEN the system shall gracefully degrade to built-in knowledge and Context7.**

- Rationale: System must remain functional without external database connectivity
- Processing: Detect MCP connection failure, fall back to built-in summaries, notify user of degraded mode
- Output: Results with "(built-in data)" attribution, recommendation to connect Notion for full accuracy
- Verification: Test all commands with Notion MCP disabled

**[SR-002] IF `aria.local.md` playbook exists in the project root, THEN the system shall load organization-specific configuration.**

- Rationale: Each organization has preferred pathways, standard positions, and custom criteria
- Content: Preferred regulatory pathways, standard classification positions, cost/timeline benchmarks, preferred consultants/notified bodies, risk tolerance levels, custom escalation criteria
- Processing: Parse aria.local.md and apply overrides to default skill behavior
- Verification: Test with and without aria.local.md present

**[SR-003] IF prior step output exists for the current product in `.aria/`, THEN the system shall pre-populate the current command with relevant context.**

- Rationale: Eliminate redundant data entry in pipeline workflows
- Processing: Read prior step Markdown files, extract relevant fields for current command
- Output: Pre-populated input with option for user override
- Verification: Test complete pipeline flow from /determine through /brief

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

---

## Specifications

### S1: Plugin Structure

**[S1.1] Plugin Manifest**

File: `.claude-plugin/plugin.json`

```json
{
  "name": "aria",
  "description": "AI Regulatory Intelligence Assistant - Medical device regulatory compliance for US FDA, EU MDR, and Korea MFDS",
  "version": "2.0.0",
  "author": {
    "name": "ARIA Team"
  }
}
```

**[S1.2] Directory Structure**

```
aria/
├── .claude-plugin/plugin.json        # Plugin manifest (S1.1)
├── .mcp.json                         # MCP connector configuration (S1.3)
├── CONNECTORS.md                     # Tool category documentation (S1.4)
├── README.md                         # Installation/usage guide + aria.local.md template (S1.5)
├── commands/                         # 8 slash commands (S2)
│   ├── aria.md                       # Free conversation (hybrid router)
│   ├── determine.md                  # Medical device determination
│   ├── classify.md                   # Device classification
│   ├── pathway.md                    # Regulatory pathway
│   ├── estimate.md                   # Cost/timeline estimation
│   ├── plan.md                       # Regulatory planning
│   ├── compare.md                    # Multi-country comparison
│   └── brief.md                      # Regulatory briefing
└── skills/                           # 7 domain skills (S3)
    ├── determination/SKILL.md        # Device determination logic
    ├── classification/SKILL.md       # Classification matrix
    ├── pathway/SKILL.md              # Pathway selection
    ├── estimation/SKILL.md           # Cost/timeline framework
    ├── planning/SKILL.md             # Milestone planning
    ├── comparison/SKILL.md           # Multi-country comparison
    └── briefing/SKILL.md             # Briefing report generation
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
      "args": ["-y", "@context7/mcp"]
    }
  }
}
```

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
- Command reference with examples
- aria.local.md playbook template and configuration guide
- Troubleshooting and FAQ

### S2: Command System (8 Commands)

**[S2.1] Command Design Pattern (Legal Plugin Benchmark)**

All commands follow the minimal frontmatter pattern:
- `description`: Brief purpose description
- `argument-hint`: Expected input format

No `tools`, `model`, or `skills` fields in command frontmatter. Commands reference skills through declarative workflow steps, not direct tool invocations.

**[S2.2] Command-Skill Mapping**

| Command | Skill | Function | Legal Benchmark Pattern |
|---------|-------|----------|------------------------|
| /aria | (all skills routing) | Free conversation + auto skill selection | (ARIA-unique hybrid router) |
| /determine | determination | Device determination checklist + classification | nda-triage pattern |
| /classify | classification | FDA/EU/MFDS grade classification matrix | legal-risk-assessment |
| /pathway | pathway | Country-specific regulatory pathway comparison | compliance pattern |
| /estimate | estimation | Cost/timeline estimation framework | contract-review pattern |
| /plan | planning | Regulatory milestone planning | meeting-briefing pattern |
| /compare | comparison | Multi-country regulation comparison | compliance pattern |
| /brief | briefing | Regulatory briefing report generation | meeting-briefing pattern |

**[S2.3] Pipeline Flow**

```
/determine --> /classify --> /pathway --> /estimate --> /plan --> /compare --> /brief
```

- Each step is freely skippable; every command can run independently
- Each command reads from `.aria/` if prior step data exists
- Upon completion, each command suggests top 1-3 most relevant next steps

Note: Each command operates independently. When prior step data is absent, the command initiates conversational information extraction (interactive Q&A) to collect minimum required input. Common required fields: Intended Use, Product Form, Primary Function, Device Description. Skill-specific fields are defined per skill implementation.

**[S2.4] /aria Command (Hybrid Router)**

The `/aria` command serves as the single entry point for free-form conversation:
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
- Escalation path definition ("when expert confirmation is needed")
- Disclaimer block

**[S3.2] Skill Definitions**

**determination** (determination/SKILL.md)
- Purpose: Evaluate whether a product qualifies as a medical device under target regulations
- Knowledge: FDA device definition (21 CFR 201(h)), EU MDR Article 2(1), MFDS device criteria
- Output: Determination checklist, YES/NO/CONDITIONAL result with traffic light, applicable regulations
- Escalation: When product is borderline (e.g., wellness vs medical device, combination products)

**classification** (classification/SKILL.md)
- Purpose: Determine regulatory class across all target regions
- Knowledge: FDA classification rules, EU MDR Annex VIII rules, MFDS classification criteria
- Output: Multi-region classification matrix (FDA I/II/III, EU I/IIa/IIb/III, MFDS 1/2/3/4)
- Escalation: When classification is ambiguous or spans multiple rules

**pathway** (pathway/SKILL.md)
- Purpose: Identify and compare regulatory submission pathways per country
- Knowledge: FDA pathways (510(k), PMA, De Novo, Exempt), EU MDR routes, MFDS authorization types
- Output: Pathway comparison table with requirements, timelines, and recommendations
- Escalation: When novel device type lacks clear predicate or pathway precedent

**estimation** (estimation/SKILL.md)
- Purpose: Provide cost and timeline estimation framework for regulatory submissions
- Knowledge: Standard fee ranges, typical timelines by device class, cost categories
- Output: Cost breakdown (optimistic/expected/pessimistic), timeline with milestones
- Escalation: When estimate requires organization-specific pricing or non-standard testing

**planning** (planning/SKILL.md)
- Purpose: Generate a regulatory milestone plan with phases and dependencies
- Knowledge: Standard regulatory milestones, critical path patterns, common bottlenecks
- Output: Phase-based plan with deliverables, dependencies, checkpoints, and responsible parties
- Escalation: When plan involves parallel multi-market submissions with complex dependencies

**comparison** (comparison/SKILL.md)
- Purpose: Compare regulatory requirements across multiple countries for specific topics
- Knowledge: Key regulatory differences across FDA, EU MDR, MFDS for major compliance areas
- Output: Side-by-side comparison matrix with similarities, differences, harmonized standards, and strategy
- Escalation: When comparison involves recently amended regulations or conflicting interpretations

**briefing** (briefing/SKILL.md)
- Purpose: Generate comprehensive regulatory briefing reports synthesizing all available data
- Knowledge: Briefing report structure, executive summary patterns, regulatory strategy presentation
- Output: Formatted briefing with executive summary, detailed analysis, recommendations, and appendices
- Escalation: When briefing is for external stakeholders (board, investors, regulatory authorities)

### S4: Data Strategy

**[S4.1] Data Source Priority Order**

1. **Notion DB** (highest priority): Organization-specific detailed regulatory data, precedents, latest information
2. **Built-in Knowledge** (second): Skill-embedded regulatory summaries (~2,000-2,500 tokens per skill)
3. **Context7** (third): Library/regulatory document supplementation and verification

**[S4.2] Data Lookup Flow**

```
Query received
  |
  v
[1] Search Notion DB
  |-- Found: Use as primary source, attribute "Notion DB"
  |-- Not found: Continue to step 2
  |
  v
[2] Use Built-in Knowledge
  |-- Available: Use as baseline, attribute "Built-in"
  |-- Insufficient: Continue to step 3
  |
  v
[3] Query Context7
  |-- Found: Supplement/verify, attribute "Context7"
  |-- Not found: Use available data, note limitations
  |
  v
[4] Aggregate results with source attribution
```

**[S4.3] Graceful Degradation Matrix**

| Notion DB | Built-in | Context7 | System Status | User Notification |
|-----------|----------|----------|---------------|-------------------|
| Available | Available | Available | Full operation | None |
| Unavailable | Available | Available | Degraded (no org data) | "Organization database unavailable. Using general knowledge." |
| Available | Available | Unavailable | Degraded (no supplementation) | "External document verification unavailable." |
| Unavailable | Available | Unavailable | Minimal operation | "Operating with built-in knowledge only. Results may be less specific." |
| Unavailable | Unavailable | Unavailable | Error state | "Unable to access data sources. Please check connections." |

Note: When operating in degraded modes (rows 2-4), each output must include a visible limitation notice indicating which data sources are unavailable and how this affects result reliability. The limitation notice is distinct from the standard disclaimer (S7.2) and appears in the Data Source Attribution section of the output.

### S5: Output System

**[S5.1] Local Data Storage**

Path: `.aria/products/{product-name}/{date}/`

```
.aria/
└── products/
    └── cardiac-monitor-x1/
        └── 2026-02-10/
            ├── determination.md       # /determine output
            ├── classification.md      # /classify output
            ├── pathway.md             # /pathway output
            ├── estimation.md          # /estimate output
            ├── plan.md                # /plan output
            ├── comparison.md          # /compare output
            └── briefing.md            # /brief output
```

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
```

**[S6.3] Loading Behavior**

- ARIA checks for `aria.local.md` in the project root at command startup
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

**[S7.3] Traffic Light System**

| Color | Meaning | Usage |
|-------|---------|-------|
| GREEN | Compliant / Clear pathway / Low risk | Device clearly meets criteria, straightforward pathway |
| YELLOW | Conditional / Requires attention / Medium risk | Ambiguous classification, additional testing may be needed |
| RED | Non-compliant / Blocked / High risk | Device does not meet criteria, significant regulatory barriers |

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

**[S8.2] Architecture Decision: Commands + Skills Only**

ARIA intentionally uses no agent definitions, following the Legal plugin benchmark pattern. All domain logic resides in skills, invoked through commands.

- Rationale: Simplicity and alignment with Cowork plugin conventions; skills handle domain logic declaratively
- Contingency: If commands + skills alone cannot deliver sufficient interaction quality after Phase 2 implementation, the following agents may be introduced:
  - Device Description Extraction Agent: Interactive Q&A specialist for building complete device profiles
  - Planning Agent: Complex multi-market regulatory strategy coordination
- Decision Point: Evaluate after Phase 2 (Foundation Skills) implementation

---

## Implementation Phases

### Phase 1: Plugin Scaffold + Core Infrastructure (Priority: Primary)

**Objective**: Establish plugin foundation recognized by Cowork platform

**Deliverables**:
- `.claude-plugin/plugin.json` (plugin manifest)
- `.mcp.json` (MCP connector configuration)
- `CONNECTORS.md` (tool category documentation)
- `README.md` (installation/usage guide with aria.local.md template)
- `aria.local.md` template

**Success Criteria**:
- Plugin recognized by Cowork platform
- MCP configuration validates without errors
- README provides complete setup instructions

### Phase 2: Foundation Skills + Commands (Priority: Primary)

**Objective**: Implement determination and classification capabilities

**Deliverables**:
- `skills/determination/SKILL.md` (device determination skill)
- `skills/classification/SKILL.md` (device classification skill)
- `commands/determine.md` (/determine command)
- `commands/classify.md` (/classify command)
- `.aria/` directory structure for local data storage

**Dependencies**: Phase 1 complete

**Success Criteria**:
- /determine correctly evaluates medical device status for 5+ product types
- /classify generates multi-region classification matrix (FDA, EU MDR, MFDS)
- Traffic light system operational on both commands
- Output stored in .aria/products/ structure
- Graceful degradation functional when Notion unavailable

### Phase 3: Pathway Skills + Commands (Priority: Secondary)

**Objective**: Implement regulatory pathway, estimation, and planning capabilities

**Deliverables**:
- `skills/pathway/SKILL.md` (regulatory pathway skill)
- `skills/estimation/SKILL.md` (cost/timeline estimation skill)
- `skills/planning/SKILL.md` (regulatory planning skill)
- `commands/pathway.md` (/pathway command)
- `commands/estimate.md` (/estimate command)
- `commands/plan.md` (/plan command)

**Dependencies**: Phase 2 complete (classification data informs pathways)

**Success Criteria**:
- /pathway identifies correct pathways for all target regions
- /estimate provides structured cost/timeline frameworks
- /plan generates milestone plans with dependencies
- Pipeline data flow from Phase 2 commands works correctly
- Next step suggestions display after each command

### Phase 4: Analysis Skills + Commands (Priority: Secondary)

**Objective**: Implement comparison and briefing capabilities

**Deliverables**:
- `skills/comparison/SKILL.md` (multi-country comparison skill)
- `skills/briefing/SKILL.md` (regulatory briefing skill)
- `commands/compare.md` (/compare command)
- `commands/brief.md` (/brief command)

**Dependencies**: Phase 3 complete (plan data informs briefings)

**Success Criteria**:
- /compare generates accurate multi-country comparison matrices
- /brief synthesizes all pipeline data into executive briefing
- Full pipeline flow from /determine through /brief operational
- Briefing quality meets VALID framework standards

### Phase 5: Router Command + Workflow Integration (Priority: Secondary)

**Objective**: Implement the /aria hybrid router and full pipeline integration

**Deliverables**:
- `commands/aria.md` (/aria free conversation command with hybrid routing)
- Pipeline integration testing and optimization
- Cross-command context sharing validation

**Dependencies**: Phase 4 complete (all skills available for routing)

**Success Criteria**:
- /aria correctly routes clear queries to appropriate skills
- /aria presents skill suggestions for ambiguous queries
- Full pipeline flow seamless with auto-context loading
- All 8 commands operational and independently executable

### Phase 6: Data Pipeline + Output Options (Priority: Final)

**Objective**: Complete Notion DB integration, Context7 supplementation, and multi-format output

**Deliverables**:
- Notion DB data lookup integration (primary data source)
- Context7 supplementation integration
- Google Drive output connector
- aria.local.md playbook parsing and application
- Multi-format output (Markdown default, Notion page, Google Docs)

**Dependencies**: Phase 5 complete

**Success Criteria**:
- Notion DB lookup operational as primary data source
- Context7 supplementation and verification functional
- Data source priority order (Notion -> built-in -> Context7) enforced
- Graceful degradation matrix fully operational (S4.3)
- aria.local.md customization applied correctly
- At least Markdown and Notion page output formats working

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
Phase 1 (scaffold) ─── mandatory ──> Phase 2 (foundation)
Phase 2 (foundation) ── mandatory ──> Phase 3 (pathway)
Phase 3 (pathway) ──── mandatory ──> Phase 4 (analysis)
Phase 4 (analysis) ──── mandatory ──> Phase 5 (router)
Phase 5 (router) ────── mandatory ──> Phase 6 (data pipeline)
```

---

## Constraints

### Technical Constraints

- [C1] Plugin structure must comply with Anthropic Cowork Plugin specification
- [C2] Commands must use minimal frontmatter (description + argument-hint only)
- [C3] Skills must use minimal frontmatter (name + description only)
- [C4] Skill body must not contain tool call instructions (declarative workflows only)
- [C5] Built-in knowledge per skill limited to approximately 2,000-2,500 tokens
- [C6] All user-facing output must be Korean (with optional English toggle)

### Domain Constraints

- [C7] All regulatory information must include source attribution
- [C8] Disclaimer must appear on every output
- [C9] Traffic light system must use exactly three levels (GREEN/YELLOW/RED)
- [C10] Escalation paths must be defined for every skill

### Distribution Constraints

- [C11] Public GitHub repository distribution
- [C12] Organization internal use first, no marketplace initially
- [C13] README must provide complete self-service installation guide

---

## Risks and Mitigation

### Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Cowork Plugin API differs from expected pattern | Medium | High | Early Phase 1 validation; follow knowledge-work-plugins reference closely |
| MCP connector configuration incompatible | Low | High | Test each connector independently in Phase 6 |
| Built-in knowledge token budget insufficient | Medium | Medium | Aggressive summarization; prioritize most-used regulations |
| Pipeline context passing between commands unreliable | Medium | Medium | Robust .aria/ file reading with fallback to manual input |

### Domain Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Regulatory information becomes outdated | Medium | High | Notion DB as primary source; Context7 supplementation; date-stamped outputs |
| Classification logic incorrect for edge cases | Medium | High | Conservative approach with YELLOW traffic light; mandatory escalation path |
| Multi-country comparison inaccurate | Low | High | Source attribution per data point; built-in knowledge reviewed by domain expert |
| Cost estimates wildly inaccurate | High | Medium | Always present as ranges; disclaimer emphasis; playbook overrides |

### User Experience Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Users treat AI output as definitive regulatory advice | High | Critical | Prominent disclaimer; YELLOW/RED escalation paths; playbook for org governance |
| Pipeline too rigid for experienced users | Medium | Low | All commands independently executable; steps freely skippable |
| Hybrid router misroutes queries | Medium | Medium | Suggestion menu for ambiguous cases; always allow direct command access |

---

## Success Criteria

### Functional Success

- [FS-01] All 8 commands (/aria, /determine, /classify, /pathway, /estimate, /plan, /compare, /brief) operational
- [FS-02] All 7 skills (determination, classification, pathway, estimation, planning, comparison, briefing) produce accurate output
- [FS-03] Pipeline flow from /determine through /brief works with auto-context loading
- [FS-04] Each command works independently without prior steps
- [FS-05] /aria hybrid router correctly handles clear matches and ambiguous queries

### Quality Success

- [QS-01] VALID framework enforced on all outputs
- [QS-02] Disclaimer present on every output
- [QS-03] Traffic light system applied consistently
- [QS-04] Data source attribution on all regulatory information
- [QS-05] All escalation paths defined and triggered appropriately

### Data Success

- [DS-01] Notion DB lookup operational as primary data source
- [DS-02] Graceful degradation matrix (S4.3) fully functional
- [DS-03] Data priority order (Notion -> built-in -> Context7) enforced
- [DS-04] .aria/ local storage working for all commands

### Integration Success

- [IS-01] Plugin recognized by Cowork platform
- [IS-02] Notion MCP connector functional
- [IS-03] Context7 MCP connector functional
- [IS-04] Google Drive MCP connector functional (for output)
- [IS-05] aria.local.md playbook parsing operational

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
| ER-001 (/aria routing) | S2.4 | 5 | Routing accuracy test |
| ER-002 (/determine) | S2.2, S3.2 | 2 | Determination accuracy test |
| ER-003 (/classify) | S2.2, S3.2 | 2 | Classification matrix test |
| ER-004 (/pathway) | S2.2, S3.2 | 3 | Pathway identification test |
| ER-005 (/estimate) | S2.2, S3.2 | 3 | Estimation framework test |
| ER-006 (/plan) | S2.2, S3.2 | 3 | Planning output test |
| ER-007 (/compare) | S2.2, S3.2 | 4 | Comparison matrix test |
| ER-008 (/brief) | S2.2, S3.2 | 4 | Briefing report test |
| ER-009 (Next steps) | S2.3, S5.3 | 2-6 | Post-completion suggestion test |
| ER-010 (Data priority) | S4.1, S4.2 | 6 | Data source order test |
| ER-011 (Auto-load context) | S5.1 | 2-6 | Pipeline context test |
| ER-012 (Multi-format input) | S2.1 | 2-6 | Input format test |
| SR-001 (Graceful degradation) | S4.3 | 6 | Degradation matrix test |
| SR-002 (Playbook loading) | S6 | 6 | Playbook configuration test |
| SR-003 (Pre-populate context) | S5.1 | 2-6 | Context pre-population test |
| SR-004 (Output formats) | S5.2 | 6 | Format conversion test |
| SR-005 (Escalation) | S3.2 | 2-6 | Escalation trigger test |
| WR-001 (No regulatory advice) | S7.2 | 1-6 | Content review |
| WR-002 (Max 3 next steps) | S2.3 | 2-6 | Suggestion count check |
| WR-003 (Source attribution) | S4.1 | 2-6 | Attribution presence check |
| WR-004 (No tool calls in skills) | S3.1 | 2-6 | Skill content review |
| WR-005 (No technical errors) | S8.1 | 1-6 | Error handling test |

### VALID Quality Framework Traceability

**V**erified:
- Regulatory citations verified via data source priority (UR-003, S4.1, S4.2)
- Traffic light system validated per assessment (UR-005, S7.3)

**A**ccurate:
- Notion DB as primary source for latest data (S4.1)
- Context7 for supplementation and verification (S4.1)
- Graceful degradation when sources unavailable (SR-001, S4.3)

**L**inked:
- Pipeline data flow across commands (ER-011, S5.1)
- Cross-references between step outputs (S5.3)
- Traceability matrix above

**I**nspectable:
- Audit trail via .aria/ Markdown files (UR-006, S5.1)
- Data source attribution on every output (UR-003)
- Escalation reasoning documented (SR-005)

**D**eliverable:
- Structured output templates (S5.3)
- Multi-format export (S5.2)
- VALID checklist enforcement (S7.1)

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
