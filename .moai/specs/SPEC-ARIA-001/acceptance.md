# SPEC-ARIA-001: Acceptance Criteria

```yaml
SPEC_ID: SPEC-ARIA-001
TITLE: ARIA Cowork Plugin - Acceptance Criteria
VERSION: 3.1.0
```

---

## Ubiquitous Requirements

### UR-001: Korean Language Responses

```gherkin
Given the ARIA plugin is installed and active
When any command is executed
Then all user-facing output shall be in Korean
And no English text shall appear in responses unless English mode is explicitly enabled (SR-008)

Given the English toggle is NOT enabled
When the user invokes any /aria: command
Then error messages, disclaimers, next step suggestions, and analysis text are all in Korean
```

### UR-002: Disclaimer Presence

```gherkin
Given any /aria: command is executed
When the command produces output
Then the output shall include the standard disclaimer block
And the disclaimer shall state "This is reference information, not regulatory advice" (in Korean)

Given the /aria:classify command is executed with optimization flag
When classification optimization suggestions are generated
Then BOTH the standard disclaimer AND the supplementary classification optimization disclaimer shall appear
```

### UR-003: Data Source Attribution

```gherkin
Given any command produces regulatory information
When the output is generated
Then each regulatory claim shall cite its data source (Notion DB, built-in, Context7, or specific regulation)
And no regulatory assertion shall appear without source attribution

Given WR-003 (negative form of UR-003)
When regulatory information is presented
Then unsupported claims or uncited standards shall NOT appear
```

### UR-004: VALID Framework Enforcement

```gherkin
Given any command produces a deliverable
When the VALID checklist is applied
Then all five pillars (Verified, Accurate, Linked, Inspectable, Deliverable) shall pass
And the output shall meet the criteria defined in S7.1
```

### UR-005: Traffic Light System

```gherkin
Given any command includes a regulatory risk assessment
When the assessment is generated
Then the output shall use GREEN, YELLOW, or RED indicators
And exactly three levels shall be used consistently across all commands
```

### UR-006: Data Storage Path Convention

```gherkin
Given the user executes a command for product "Cardiac Monitor X1" on 2026-02-10
When the command output is generated
Then the output shall be stored at .aria/products/cardiac-monitor-x1/2026-02-10/
And the product name shall be lowercase, hyphens, alphanumeric only
```

---

## Event-Driven Requirements

### ER-001: /aria:chat Hybrid Router

```gherkin
Given the user invokes /aria:chat with a clear keyword query like "classify my device"
When the system processes the query
Then the system shall route directly to the matching skill (classification)
And execute the skill without showing a disambiguation menu

Given the user invokes /aria:chat with an ambiguous query like "help with my product"
When the system processes the query
Then the system shall present top 1-3 skill suggestions
And the user can select one to proceed

Given the user invokes /aria:chat with a general question like "what is EU MDR?"
When the system processes the query
Then the system shall enter conversational mode for general regulatory Q&A
```

### ER-002: /aria:determine

```gherkin
Given the user invokes /aria:determine with a product description
When the determination skill processes the input
Then the system shall evaluate the product against FDA, EU MDR, and MFDS criteria
And produce a determination result (YES/NO/CONDITIONAL) with traffic light status
And cite applicable regulations for each region

Given the user provides a technical document as input to /aria:determine
When the document is processed
Then the system shall extract device description, intended use, product form, and primary function
And initiate targeted Q&A only for fields not extractable from the document

Given an active medical device (e.g., cardiac defibrillator)
When /aria:determine is executed
Then the result shall be YES (medical device) with GREEN traffic light

Given a wellness device (e.g., fitness tracker with no medical claims)
When /aria:determine is executed
Then the result shall include YELLOW traffic light with escalation recommendation for borderline case

Given a non-medical product (e.g., general furniture, office equipment)
When the user uploads a product technical document to /aria:determine
Then the result shall be NO (not a medical device) with RED or YELLOW traffic light
And the output shall clearly state "의료기기 해당 없음" with rationale
And the system shall suggest the user verify with a regulatory professional if uncertain
```

### ER-003: /aria:classify

```gherkin
Given the user invokes /aria:classify with device characteristics
When the classification skill processes the input
Then the system shall generate a multi-region classification matrix
And include FDA class (I/II/III), EU MDR class (I/IIa/IIb/III), and MFDS class (1/2/3/4)
And provide rationale and rule references for each classification

Given a Class II active monitoring device
When /aria:classify is executed
Then the output shall show FDA Class II, EU MDR Class IIa, and MFDS Class 2 (or equivalent)
And each classification shall reference the applicable classification rule

Given the optimization flag is set (OR-004)
When /aria:classify is executed
Then the system shall additionally analyze which device characteristics could lower the class
And all optimization suggestions shall be tagged YELLOW
And a mandatory escalation recommendation shall be included
And the supplementary classification optimization disclaimer shall appear
```

### ER-004: /aria:pathway

```gherkin
Given the user invokes /aria:pathway with classification results
When the pathway skill processes the input
Then the system shall identify regulatory submission pathways for each target region
And produce a comparison table with timelines, requirements, and recommendations

Given a Class II device targeting US + EU + Korea markets
When /aria:pathway is executed
Then the output shall include 510(k) pathway for FDA
And CE Marking route for EU MDR
And MFDS authorization type for Korea
And each pathway shall include timeline ranges and key requirements
```

### ER-005: /aria:estimate

```gherkin
Given the user invokes /aria:estimate with pathway selection
When the estimation skill processes the input
Then the system shall provide a cost breakdown with optimistic/expected/pessimistic ranges
And a timeline with milestones
And cost categories (consulting, testing, regulatory fees, notified body)

Given a Class III device with PMA pathway
When /aria:estimate is executed
Then the cost ranges shall reflect higher Class III costs
And the timeline shall be longer than Class I/II estimates
And the disclaimer shall emphasize estimate uncertainty
```

### ER-006: /aria:plan

```gherkin
Given the user invokes /aria:plan with pathway and estimate data
When the planning skill processes the input
Then the system shall generate a milestone plan with phases
And include deliverables, dependencies, and checkpoints for each phase

Given a multi-market scenario (US + EU + Korea)
When /aria:plan is executed
Then the plan shall show parallel submission tracks per market
And identify the critical path
And highlight common dependencies
```

### ER-007: /aria:compare

```gherkin
Given the user invokes /aria:compare with a regulatory topic and target countries
When the comparison skill processes the input
Then the system shall generate a side-by-side comparison matrix
And highlight similarities, differences, and harmonized standards

Given the topic "clinical evidence requirements" for FDA vs EU MDR vs MFDS
When /aria:compare is executed
Then the matrix shall show specific requirements per region
And include strategic recommendations
```

### ER-008: /aria:brief

```gherkin
Given the user invokes /aria:brief with complete pipeline data in .aria/
When the briefing skill processes the input
Then the system shall synthesize all prior step data into an executive briefing
And include executive summary, detailed analysis, recommendations, and appendices

Given partial pipeline data (only determination and classification)
When /aria:brief is executed
Then the briefing shall cover available data
And indicate which sections lack data
And suggest completing missing pipeline steps
```

### ER-009: Next Step Suggestions

```gherkin
Given any command completes execution
When the output is displayed
Then the system shall show 1-3 next step suggestions (not more than 3, per WR-002)
And each suggestion shall include the command name and brief description

Given /aria:determine completes
When next steps are suggested
Then the primary suggestion shall be "/aria:classify to determine device class"
```

### ER-010: Data Lookup Priority

```gherkin
Given all three data sources are available
When a data lookup is required
Then the system shall query Notion DB first, built-in knowledge second, Context7 third
And the final output shall attribute each data element to its source

Given Notion DB returns partial results
When the lookup continues
Then built-in knowledge shall supplement the gap
And Context7 shall verify and supplement further
And the output shall show mixed attribution
```

### ER-011: Auto-Load Pipeline Context

```gherkin
Given prior step output exists at .aria/products/cardiac-monitor-x1/2026-02-10/determination.md
When the user invokes /aria:classify for the same product
Then the system shall auto-load determination context
And the context shall be loaded in compressed form (determination.summary.md)

Given prior step output does NOT exist
When a command is invoked
Then the system shall proceed without prior context
And use document analysis or Q&A to collect required input
```

### ER-012: Multi-Format Input

```gherkin
Given the user provides input via file upload
When the command processes the input
Then the result shall be equivalent to pasted text input

Given the user provides input via URL reference
When the command processes the input
Then the result shall be equivalent to direct text input
```

### ER-013: Document-First Input

```gherkin
Given a command is executed without prior pipeline data
And the user provides a technical document
When the system processes the input
Then the system shall extract required information from the document FIRST
And identify missing fields via gap detection
And initiate targeted Q&A ONLY for genuinely missing fields
And NOT ask about fields already extracted from the document

Given a product specification document is provided to /aria:determine
When document analysis is complete
Then device description, intended use, and product form shall be extracted
And only skill-specific fields not found in the document shall be asked via Q&A
```

### ER-014: Document Extraction

```gherkin
Given the user provides a product specification document
When the system analyzes the document
Then the system shall extract device description, intended use, product form, primary function
And all skill-specific fields (invasiveness, duration of contact, active/passive, etc.)
And each extracted field shall have a confidence indicator

Given the user provides an IFU (Instructions for Use) document
When the system analyzes the document
Then intended use and product form shall be extracted with high confidence
And device-specific technical parameters shall be extracted where available
```

### ER-015: Context Compression

```gherkin
Given /aria:determine produces a 3,000-token output
When Context Simplifier processes the output
Then a compressed summary of approximately 500 tokens shall be generated
And the summary shall contain: decision outcome, key data points, traffic light status, source attribution, escalation flags
And the full output shall be preserved in .aria/

Given a full pipeline run from /aria:determine through /aria:brief
When comparing compressed vs uncompressed pipeline context
Then total pipeline context shall be reduced by at least 60%
And no critical decision information shall be lost in compression
```

### ER-016: Stale Data Warning

```gherkin
Given .aria/products/ contains data directories older than the configured retention period (data_retention_days in aria.local.md)
When any /aria: command is executed
Then the system shall display a warning message listing stale data directories
And the warning shall include the age of each stale directory
And the system shall NOT automatically delete any data

Given .aria/products/ contains no data older than the configured retention period
When any /aria: command is executed
Then no stale data warning shall be displayed

Given aria.local.md does not specify data_retention_days
When stale data check is performed
Then the system shall use the default retention period of 365 days
```

---

## State-Driven Requirements

### SR-001: Graceful Degradation

```gherkin
Given Notion MCP connection is unavailable
When any command is executed
Then the system shall fall back to built-in knowledge and Context7
And display "Organization database unavailable. Using general knowledge."
And output shall include "(built-in data)" attribution

Given all external sources are unavailable (Notion + Context7)
When any command is executed
Then the system shall operate with built-in knowledge only
And display "Operating with built-in knowledge only. Results may be less specific."
And output shall be usable (degraded but functional)
```

### SR-002: Playbook Loading

```gherkin
Given aria.local.md exists in the user's project root
When a command is executed
Then the system shall load and apply organization-specific configuration
And override default behavior per playbook settings

Given aria.local.md does NOT exist
When a command is executed
Then the system shall use default skill behavior
And proceed without customization
```

### SR-003: See ER-011

```gherkin
Note: SR-003 is merged into ER-011. Pre-population of context from prior step data
is tested through ER-011 acceptance criteria.
```

### SR-004: Output Format Conversion

```gherkin
Given the user requests Notion page output
When the command generates results
Then the system shall create a Notion page via MCP connector
And the content shall match the Markdown output

Given no specific format is requested
When the command generates results
Then the default Markdown report shall be written to .aria/
```

### SR-005: Escalation Recommendations

```gherkin
Given an ambiguous classification scenario (e.g., borderline Class II/III)
When the skill processes the input
Then the system shall explicitly state an escalation recommendation
And specify the type of expert needed (e.g., "Consult a regulatory affairs specialist")
And the escalation reason shall be documented

Given a high-risk scenario (RED traffic light)
When the output is generated
Then the escalation recommendation shall be prominently displayed
And the suggested expert type shall be specific to the risk area
```

### SR-006: Multi-Product Selection (File-Based Persistence)

```gherkin
Given .aria/products/ contains 3 product directories AND .aria/active_product.json does NOT exist
When the user invokes any /aria: command
Then the system shall present a selection menu with all 3 products and most recent dates
And persist the selection to .aria/active_product.json
And allow creation of a new product entry

Given .aria/active_product.json exists with valid product reference
When the user invokes any /aria: command
Then the system shall load the active product from active_product.json
And NOT present a selection menu
And update last_accessed date in active_product.json

Given .aria/active_product.json exists but references a product that no longer exists
When the user invokes any /aria: command
Then the system shall treat active_product.json as stale
And present a product selection menu
And update active_product.json with the new selection

Given .aria/products/ contains exactly 1 product directory
When the user invokes any /aria: command
Then the system shall automatically select the single product
And persist the selection to .aria/active_product.json
And NOT present a selection menu

Given .aria/products/ is empty
When the user invokes any /aria: command
Then the system shall prompt the user to create a new product entry
And apply the product naming convention (lowercase, hyphens, alphanumeric)
And persist the new product to .aria/active_product.json
```

### SR-007: Output Versioning

```gherkin
Given .aria/products/cardiac-monitor-x1/2026-02-10/determination.md already exists
When the user re-executes /aria:determine for the same product and date
Then the system shall create determination-v2.md (NOT overwrite determination.md)
And both files shall be preserved for audit trail

Given determination-v2.md already exists
When the user executes /aria:determine again
Then the system shall create determination-v3.md
And all versions (determination.md, determination-v2.md, determination-v3.md) shall be preserved
```

### SR-008: English Output Toggle

```gherkin
Given the user enables English output via command flag
When any command is executed
Then all user-facing text shall be in English
And Korean regulatory terms shall include English translations (e.g., "medical device (의료기기)")

Given aria.local.md contains language preference set to "en"
When any command is executed
Then the behavior shall be identical to explicit English toggle via command flag
```

---

## Unwanted Behavior Requirements

### WR-001: No Regulatory Advice

```gherkin
Given any command output is generated
When reviewing the content
Then phrases like "you should", "you must", "this is required" shall NOT appear without disclaimer context
And all regulatory statements shall be framed as "reference information for professional review"
```

### WR-002: Max 3 Next Steps

```gherkin
Given any command completes execution
When next step suggestions are displayed
Then the count shall be between 1 and 3 (inclusive)
And never exceed 3 suggestions
```

### WR-003: No Unsourced Regulatory Claims

```gherkin
Given any regulatory information is presented
When reviewing the output
Then every regulatory claim shall have a source citation
And unsupported claims or uncited standards shall NOT appear
```

### WR-004: No Tool Calls in Skills

```gherkin
Given any SKILL.md file is reviewed
When checking for technical implementation leakage
Then NO MCP tool invocation syntax, API calls, or function signatures shall be present
And only declarative workflow steps shall be used
```

### WR-005: No Technical Error Messages

```gherkin
Given an MCP connection failure occurs during command execution
When the error is communicated to the user
Then raw exception messages, stack traces, or MCP error codes shall NOT be displayed
And a plain language explanation with suggested recovery action shall be shown
```

---

## Optional Feature Requirements

### OR-001: Google Drive Export

```gherkin
Given Google Drive MCP is configured
When the user requests Google Docs export
Then the system shall create a Google Doc via MCP connector
And the content shall match the Markdown output
```

### OR-002: .docx Export

```gherkin
Given .docx conversion capability exists
When the user requests Word document export
Then the system shall generate a .docx file from Markdown
And the formatting shall be preserved
```

### OR-003: Extensible Connectors

```gherkin
Given a new MCP connector becomes available
When it is added to .mcp.json and documented in CONNECTORS.md
Then the system shall support the new connector without core code changes
```

### OR-004: Classification Optimization

```gherkin
Given the user invokes /aria:classify with the optimization flag
When the classification skill processes the input
Then the system shall analyze which device characteristics could lower the regulatory class
And frame suggestions as conditional scenarios (e.g., "if intended use were narrowed to X, classification might change to Y")
And all suggestions shall be tagged YELLOW
And a mandatory escalation recommendation shall be included
And the supplementary classification optimization disclaimer shall appear

Given a Class III device where narrowing intended use could reduce to Class II
When classification optimization is invoked
Then the system shall suggest the specific intended use modification
And clearly state that modification must be validated by regulatory professionals
And note that patient safety must not be compromised
```

---

## Quality Gates

### VALID Framework Checklist

```gherkin
Given any command output is finalized
When the VALID checklist is evaluated:

Then Verified: Every regulatory assertion shall have a source citation
And Accurate: Data shall come from Notion DB (primary), built-in (secondary), or Context7 (tertiary)
And Linked: Pipeline outputs shall cross-reference prior step results
And Inspectable: Decision rationale shall be documented in .aria/ output files
And Deliverable: Output shall follow the structured template (S5.3)
```

### Quantitative Quality Targets

```gherkin
Given /aria:determine is tested with diverse product types
When results are evaluated
Then accurate determination results shall be produced for at least 5 product types (active, implantable, IVD, SaMD, non-active)

Given /aria:chat hybrid routing is tested with diverse queries
When at least 20 queries across all 7 skill domains are tested
Then routing accuracy shall be 80% or higher

Given any SKILL.md file is reviewed for token budget compliance
When built-in knowledge token count is measured
Then each skill's built-in knowledge shall be within 500 lines and approximately 2,500 tokens

Given Context Simplifier generates a compressed summary
When summary token count is measured
Then the summary shall be within approximately 500 tokens

Given Notion MCP is NOT connected
When any /aria: command is executed
Then all commands shall provide basic functionality (graceful degradation)
And output shall clearly indicate degraded mode

Given a document without a Table of Contents (e.g., OCR scanned PDF, draft document)
When the document is processed by S9.1 Document Analysis Pipeline
Then the system shall fall back to analyzing the first 2,000 tokens and last 2,000 tokens
And search for key terms (Intended Use, Device Description, Specification) to locate relevant content

Given a Context Simplifier summary is generated by any skill
When the summary format is validated
Then the summary shall follow the standardized Key-Value Markdown list format
And contain Decision, Traffic Light, Key Factors, Escalation, and Sources fields
```

### SKILL.md Compliance

```gherkin
Given any SKILL.md file in the skills/ directory
When the file is reviewed
Then the file shall not exceed 500 lines (C12)
And the frontmatter shall contain only name and description fields (C3)
And the body shall not contain tool call instructions (C4)
And built-in knowledge shall focus on decision logic (not regulatory text) (C5)
And a knowledge base date shall be declared (S3.1)
```

### Security Compliance

```gherkin
Given the plugin is installed in a user's project
When reviewing data handling practices
Then .aria/ should be in .gitignore recommendations
And MCP credentials should be stored as environment variables only
And no secrets should appear in committed files
And the README should include sensitive data warnings
```

---

## Definition of Done

A requirement is considered DONE when:

1. The feature implements the behavior described in the EARS requirement
2. All Gherkin acceptance scenarios for the requirement PASS
3. The output includes Korean language (or English if SR-008 is enabled)
4. The standard disclaimer is present in all outputs
5. Data source attribution is present for all regulatory claims
6. Traffic light system is applied where applicable
7. Output is stored in `.aria/products/{product-name}/{date}/` structure
8. Compressed summary is generated alongside full output (Context Simplifier)
9. Graceful degradation behavior is verified for the feature
10. VALID framework checklist passes for the output

A Phase is considered DONE when:
1. All deliverables listed for the Phase are complete
2. All success criteria for the Phase are met
3. Quality gates for the Phase pass
4. No regressions in previously completed Phase features
