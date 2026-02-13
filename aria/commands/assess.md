---
description: Regulatory assessment pipeline - Combines determination, classification, and pathway analysis into a single integrated assessment
argument-hint: "[Product description or document] [--lang en|ko] [--format markdown|pdf|notion|gdocs]"
---

# /aria:assess - Regulatory Assessment Orchestrator

## Purpose

Integrated regulatory assessment pipeline that answers: "Where does my product stand in the regulatory landscape?" Combines device determination, classification, and pathway analysis into a single orchestrated workflow with multi-region comparison when 2+ target markets are selected.

**Replaces**: `/aria:determine`, `/aria:classify`, `/aria:pathway`, `/aria:compare` (for assessment context)

## Workflow

### 1. Product Context Loading

Check `.aria/products/` directory structure and `.aria/active_product.json`:

**Case 1: active_product.json exists with valid product reference**
- Load active product from file
- Update last_accessed date
- Skip selection menu

**Case 2: Multiple products exist AND active_product.json does NOT exist**
- Scan `.aria/products/` for all product directories
- Present selection menu with product names and most recent dates
- Allow creation of new product entry
- Persist user selection to `.aria/active_product.json`:
  ```json
  { "product_name": "cardiac-monitor-x1", "last_accessed": "2026-02-12", "path": ".aria/products/cardiac-monitor-x1/2026-02-12/" }
  ```

**Case 3: active_product.json exists but references invalid/deleted product**
- Treat file as stale
- Present product selection menu
- Update active_product.json with new selection

**Case 4: Exactly 1 product exists**
- Auto-select single product
- Persist to active_product.json
- Skip selection menu

**Case 5: No products exist**
- Prompt user to create new product entry
- Apply product naming convention (lowercase, hyphens, alphanumeric only)
- Persist new product to active_product.json

### 2. Input Collection

**If technical document provided** (PDF, text, or structured input):
- Extract device description, intended use, product form, primary function
- Large documents (>100 pages): Analyze TOC first, extract relevant sections
- Gap detection + targeted Q&A for missing fields (max 1-3 rounds)

**If prior profile.json exists** (from `/aria:chat`):
- Load product profile from `.aria/products/{product-name}/{date}/profile.json`
- Verify completeness, ask only for missing critical fields

**If no document and no prior context**:
- Conversational Q&A: device description, intended use, product form, primary function, target markets

**Required fields**:
- Device description and physical characteristics
- Intended use statement (medical purpose)
- Product form (hardware, software, IVD, combination)
- Primary function and mechanism of action
- Target markets (default: FDA, EU MDR, MFDS)

**IMPORTANT**: Once all required fields are collected, proceed directly to Step 3. Do NOT repeat or re-display the Q&A conversation.

### 3. Determination Phase

Invoke the determination skill with collected device information:

- Skill("aria-determination") with all collected fields as context
- Evaluate against FDA, EU MDR, MFDS definitions
- Apply traffic light system and identify escalation scenarios

**Decision Gate**:
- **YES** (device is a medical device): Continue to Step 4
- **CONDITIONAL** (borderline case): Display warning with rationale, recommend expert review, continue to Step 4
- **NO** (not a medical device): Stop workflow with rationale. Output determination-only result. Suggest expert review if user disagrees.

### 4. Classification Phase

Invoke the classification skill with determination context:

- Skill("aria-classification") with device characteristics and determination results
- Apply FDA classification decision rules (Class I/II/III)
- Apply EU MDR Annex VIII classification logic (Rules 1-22) (Class I/IIa/IIb/III)
- Apply MFDS classification evaluation criteria (Grade 1/2/3/4)
- Generate multi-region classification matrix
- Apply traffic light per region

### 5. Pathway Phase

Invoke the pathway skill with classification results:

- Skill("aria-pathway") with classification matrix
- Identify optimal submission routes per target region:
  - **FDA**: Exempt, 510(k), De Novo, PMA
  - **EU MDR**: Self-declaration, Notified Body Annex IV/IX/X
  - **MFDS**: Registration (notification) or Approval (permit)
- Determine timeline ranges and key requirements per pathway
- Identify critical path (longest timeline)

### 6. Multi-Region Comparison (if 2+ target markets)

When the product targets 2 or more markets, apply comparison logic inline:

**Comparison Dimensions**:
- Regulatory basis and classification alignment across regions
- Pathway complexity and timeline comparison
- Shared testing activities and documentation overlap
- Harmonized standards applicability (ISO 13485, ISO 14971, IEC 60601)

**Strategic Recommendation**:
- Harmonized approach (design to most stringent requirement, usually EU MDR)
- Parallel submission strategy (simultaneous multi-region)
- Sequential submission strategy (easiest market first)

**Cost-Benefit Highlights**:
- Common testing reuse potential
- Documentation overlap estimation
- Translation/localization budget consideration

### 7. Output Generation

**Full output** (`assess.md`):

```markdown
# Regulatory Assessment Report

## Product Information
- Product: {product-name}
- Date: {YYYY-MM-DD}
- Target Markets: {FDA, EU MDR, MFDS}

## 1. Device Determination

### Medical Device Status
| Region | Status | Rationale | Traffic Light |
|--------|--------|-----------|---------------|
| FDA | {YES/NO/CONDITIONAL} | {rationale} | {GREEN/YELLOW/RED} |
| EU MDR | {YES/NO/CONDITIONAL} | {rationale} | {GREEN/YELLOW/RED} |
| MFDS | {YES/NO/CONDITIONAL} | {rationale} | {GREEN/YELLOW/RED} |

### Applicable Regulations
- FDA: {applicable sections}
- EU MDR: {applicable articles}
- MFDS: {applicable regulations}

## 2. Classification

### Multi-Region Classification Matrix
| Region | Class | Risk Level | Rationale | Traffic Light |
|--------|-------|------------|-----------|---------------|
| FDA | {I/II/III} | {Low/Moderate/High} | {rationale} | {GREEN/YELLOW/RED} |
| EU MDR | {I/IIa/IIb/III} | {Low/Medium-Low/Medium-High/High} | {rationale} | {GREEN/YELLOW/RED} |
| MFDS | {1/2/3/4} | {risk level} | {rationale} | {GREEN/YELLOW/RED} |

### Key Classification Factors
- Invasiveness: {level}
- Duration: {transient/short-term/long-term}
- Active/Passive: {type}
- Body System: {system}

## 3. Regulatory Pathways

### Pathway Recommendations
| Region | Pathway | Timeline | Key Requirements | Traffic Light |
|--------|---------|----------|-----------------|---------------|
| FDA | {pathway} | {timeline} | {requirements} | {GREEN/YELLOW} |
| EU MDR | {pathway} | {timeline} | {requirements} | {GREEN/YELLOW} |
| MFDS | {pathway} | {timeline} | {requirements} | {GREEN/YELLOW} |

### Critical Path
- Region: {region with longest timeline}
- Duration: {timeline range}
- Key Bottleneck: {bottleneck description}

## 4. Multi-Region Comparison (if applicable)

### Regional Alignment
{Side-by-side comparison of key requirements}

### Harmonization Opportunities
{Shared standards, common testing, documentation overlap}

### Recommended Strategy
{Harmonized / Parallel / Sequential approach with rationale}

## 5. Overall Assessment

### Traffic Light Summary
| Phase | Status |
|-------|--------|
| Determination | {GREEN/YELLOW/RED} |
| Classification | {GREEN/YELLOW/RED} |
| Pathway | {GREEN/YELLOW/RED} |
| **Overall** | **{most conservative}** |

### Escalation Items
{Items requiring expert review, if any}

### Recommended Next Steps
1. {Next step 1}
2. {Next step 2}
3. {Next step 3}

## Disclaimer

**Important Notice**

This assessment is an AI-based regulatory intelligence analysis, not official regulatory advice.

- **No legal effect**: Results are for reference only and have no legal binding force
- **Expert review required**: All regulatory analyses require validation by qualified regulatory affairs professionals
- **Regulatory authority confirmation**: Final regulatory decisions must follow official guidance from FDA, Notified Bodies, MFDS, etc.
- **Limitation of liability**: Users are responsible for regulatory decisions made based on this tool's output

Knowledge Base Date: 2026-01

---

This is reference information for professional review, not regulatory advice.
```

**Compressed summary** (`assess.summary.md`):

```markdown
# Assessment Summary

**Product**: {product-name}
**Date**: {YYYY-MM-DD}
**Target Markets**: {markets}

## Determination
- **Status**: {YES/NO/CONDITIONAL}
- **Traffic Light**: {GREEN/YELLOW/RED}

## Classification
- **FDA Class**: {I/II/III}
- **EU MDR Class**: {I/IIa/IIb/III}
- **MFDS Grade**: {1/2/3/4}

## Pathways
- **FDA**: {pathway} ({timeline})
- **EU MDR**: {pathway} ({timeline})
- **MFDS**: {pathway} ({timeline})

## Critical Path
- **Region**: {region}
- **Duration**: {timeline}

## Overall Traffic Light
- **Assessment**: {GREEN/YELLOW/RED}

## Recommended Strategy
- **Approach**: {harmonized/parallel/sequential}

---
This summary is consumed by `/aria:project` command.
```

### 8. File Storage

Save results to `.aria/products/{product-name}/{date}/`:
- `assess.md` - Full integrated assessment report
- `assess.summary.md` - Compressed summary for downstream commands

### 9. Next Steps

- **Primary**: `/aria:project` to generate cost/timeline estimation and milestone plan
- **Alternative**: Expert review consultation (if YELLOW or RED traffic light)
- **Optional**: `/aria:chat` for follow-up questions about the assessment

## Output Contract

Before rendering output, `/aria:assess` resolves:

- `output_type`: `full_report_md` (`assess.md`) and `summary_md` (`assess.summary.md`)
- `format`: `markdown | pdf | notion | gdocs`
- `language`: `ko | en`
- `audience`: `mixed` (`summary_md` leans executive; `full_report_md` supports operator + executive)
- `safety_flags`:
  - `preserve_regulatory_facts=true`
  - `preserve_numeric_values=true`
  - `preserve_disclaimer_strength=true`
- `graceful fallback`: if requested export is unavailable, fall back to `markdown` with an explicit notice.

## Format Output

**Format Selection** (via `--format` flag):
- `markdown` (default): Markdown report to `.aria/products/`
- `notion`: Notion page via Notion MCP connector (requires notion-mcp configuration)
- `gdocs`: Google Docs via Google Drive MCP connector (requires google-drive-mcp configuration)
- `pdf`: PDF conversion from Markdown (requires pdf-converter tool, e.g., pandoc)

**Graceful Degradation**: If selected format's MCP connector is unavailable, fall back to Markdown format with a notice.

## Flags

- `--lang en|ko`: Output language (default: `ko`)
- `--format markdown|pdf|notion|gdocs`: Output format (default: `markdown`)

## Output Location

- `.aria/products/{product-name}/{date}/assess.md`
- `.aria/products/{product-name}/{date}/assess.summary.md`

## Data Sources

Built-in regulatory knowledge is the primary source. Detailed criteria are available in skill modules for deep analysis. External data connectors (Notion, Context7) are used only when configured.

## Skills Used

- `aria-determination`: Medical device qualification evaluation
- `aria-classification`: Multi-region device classification
- `aria-pathway`: Regulatory submission pathway analysis
- Comparison logic: Inline multi-region comparison (no separate skill)

## Traffic Light Interpretation

- **GREEN**: Clear determination, definitive classification, low-risk pathways
- **YELLOW**: Borderline determination, ambiguous classification, moderate-high risk pathways, or escalation items
- **RED**: Unable to determine/classify due to insufficient information or conflicting criteria

The overall traffic light is the most conservative (highest caution) across all phases.

## Example

```
/aria:assess
```
> System loads product context or starts Q&A
> Runs determination -> classification -> pathway pipeline
> Generates integrated assessment report

```
/aria:assess --lang en --format pdf
```
> English output, PDF format
> Same pipeline execution
> PDF conversion after Markdown generation

```
/aria:assess [Upload technical specification PDF]
```
> Extracts product info from document
> Runs full assessment pipeline
> Generates integrated report

## Disclaimer

**Important Notice**

This assessment is an AI-based regulatory intelligence analysis, not official regulatory advice.

- **No legal effect**: Results are for reference only and have no legal binding force
- **Expert review required**: All regulatory analyses require validation by qualified regulatory affairs professionals
- **Regulatory authority confirmation**: Final regulatory decisions must follow official guidance from FDA, Notified Bodies, MFDS, etc.
- **Limitation of liability**: Users are responsible for regulatory decisions made based on this tool's output

Knowledge Base Date: 2026-01

---

This is reference information for professional review, not regulatory advice.
