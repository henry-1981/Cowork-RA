---
description: Comprehensive regulatory briefing report - Synthesizes all pipeline data (assess + project) into a single executive-ready document
argument-hint: "[Focus area] [--format markdown|pdf|notion|gdocs] [--lang ko|en] [--depth express|standard|deep]"
---

# /aria:report - Comprehensive Report Generator

## Purpose

Generate comprehensive regulatory briefing reports synthesizing all available pipeline data into executive-ready documents. Collects assessment and project plan results from `.aria/products/` and produces an integrated briefing with executive summary, detailed analysis, recommendations, and appendices.

**Absorbs**: briefing skill logic (no separate briefing skill needed)

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
- Warn that briefing requires pipeline data
- Suggest running `/aria:assess` first

### 2. Pipeline Data Loading

Scan `.aria/products/{product-name}/{date}/` for all available pipeline data:

**New format** (from restructured commands):
- `profile.json` (product profile from /aria:chat)
- `assess.md` + `assess.summary.md` (from /aria:assess)
- `project.md` + `project.summary.md` (from /aria:project)

**Legacy format** (backward compatibility):
- `determination.summary.md` + `determination.md`
- `classification.summary.md` + `classification.md`
- `pathway.summary.md` + `pathway.md`
- `estimation.summary.md` + `estimation.md`
- `plan.summary.md` + `plan.md`
- `comparison.summary.md` + `comparison.md`

**Loading Priority**:
- Use `.summary.md` files for executive summary (compressed context)
- Use full `.md` files for detailed analysis sections (complete information)
- Prefer new format files over legacy format when both exist

### 3. Data Completeness Assessment

**Full Pipeline** (assess + project data available):
- Generate comprehensive briefing with all sections
- Executive summary + detailed analysis + recommendations + appendices

**Assessment Only** (assess data available, no project data):
- Generate focused briefing covering regulatory assessment
- Include: device status, classification, pathways, multi-region comparison
- Indicate missing project data with recommendation to run `/aria:project`

**Project Only** (project data available, no assess data):
- Generate focused briefing covering project plan
- Include: cost/timeline estimates, milestone plan
- Indicate missing assessment data with recommendation to run `/aria:assess`

**No Pipeline Data**:
- Warn user that briefing requires pipeline data
- Suggest: "Run `/aria:assess` first, then `/aria:project` for a complete briefing."
- STOP workflow

### 4. Focus Area Identification (Optional)

User can specify focus area for emphasis in recommendations:
- **Clinical Strategy**: Clinical evidence requirements, trial planning
- **Cost Control**: Budget optimization, cost reduction opportunities
- **Timeline Acceleration**: Parallel submission, expedited pathways
- **Multi-Market Entry**: Comparison analysis, harmonization strategy

Default: Balanced coverage of all aspects

### 5. Two-Phase Output (ER-017 Report Issuance Policy)

**Phase A - Analysis Turn** (Present key findings for user confirmation):

Display concise analysis summary:

```markdown
# Regulatory Briefing Analysis (Summary)

## Product Overview
- **Product**: {product-name}
- **Device Status**: {YES/NO/CONDITIONAL}
- **Classification**: FDA Class {X}, EU MDR Class {X}, MFDS Grade {X}

## Key Findings
1. **Regulatory Pathways**: {FDA pathway} / {EU pathway} / {MFDS pathway}
2. **Critical Path Timeline**: {region} - {timeline}
3. **Budget Range**: {optimistic} ~ {expected} ~ {pessimistic}
4. **Key Risks**: {top risks with traffic light}

## Top 3 Recommendations
1. {Recommendation 1}
2. {Recommendation 2}
3. {Recommendation 3}

## Overall Traffic Light
- **Assessment**: {GREEN/YELLOW/RED}

---
**User confirmation required**: Please review the above analysis. Proceed with full report generation?
```

Ask user to confirm before generating full report.

**Phase B - Full Report Generation** (After user confirmation):

Generate complete briefing report (see Output Template below).

### 6. Output Template

```markdown
# Regulatory Briefing Report

## Table of Contents
1. Executive Summary
2. Detailed Analysis
3. Recommendations
4. Appendices

---

## 1. Executive Summary

### Product Overview
- **Product**: {product-name}
- **Intended Use**: {intended use}
- **Regulatory Scope**: FDA (US), EU MDR (Europe), MFDS (Korea)

### Regulatory Status
- **Medical Device Status**: {YES/NO/CONDITIONAL} ({traffic light})
- **Classification**:
  - FDA: Class {I/II/III}
  - EU MDR: Class {I/IIa/IIb/III}
  - MFDS: Grade {1/2/3/4}

### Recommended Pathways
- **FDA**: {pathway} (timeline: {range})
- **EU MDR**: {pathway} (timeline: {range})
- **MFDS**: {pathway} (timeline: {range})
- **Critical Path**: {region} ({longest timeline})

### Cost & Timeline
- **Total Budget**: {optimistic} ~ {expected} ~ {pessimistic}
- **Total Timeline**: {end-to-end timeline}
- **Key Milestones**: {milestone summary}

### Key Risks
1. {Risk 1 with traffic light}
2. {Risk 2 with traffic light}
3. {Risk 3 with traffic light}

### Strategic Recommendations
1. {Top recommendation 1}
2. {Top recommendation 2}
3. {Top recommendation 3}

---

## 2. Detailed Analysis

### 2.1 Device Determination
{Full determination analysis from assess.md}

### 2.2 Classification
{Full classification analysis from assess.md}

### 2.3 Regulatory Pathways
{Full pathway analysis from assess.md}

### 2.4 Multi-Region Comparison
{Comparison analysis from assess.md, if available}

### 2.5 Cost & Timeline Estimation
{Full estimation analysis from project.md}

### 2.6 Milestone Plan
{Full planning analysis from project.md}

---

## 3. Recommendations

### Immediate Actions (30 Days)
1. {Action with rationale}
2. {Action with rationale}
3. {Action with rationale}

### Critical Dependencies
- {Dependency 1}
- {Dependency 2}
- {Dependency 3}

### Resource Requirements
- **Regulatory Consultants**: FDA/EU MDR/MFDS expertise
- **Testing Facilities**: {per pathway requirements}
- **Clinical Trial Sites**: {if applicable}
- **Notified Body**: {if EU Class IIa+}

### Risk Mitigation Strategies
- {Strategy 1}
- {Strategy 2}
- {Strategy 3}

---

## 4. Appendices

### A. Regulatory Citations
- **FDA**: {citations from all analysis steps}
- **EU MDR**: {article citations from all steps}
- **MFDS**: {regulation citations from all steps}

### B. Data Sources
- {Attribution summary from all pipeline steps}
- Built-in knowledge: FDA, EU MDR, MFDS decision frameworks (2026-01)
- External sources: {Notion DB / Context7 if used}

### C. Escalation Items
{All escalation items from pipeline steps with rationale}

### D. Glossary
- **510(k)**: FDA Premarket Notification
- **PMA**: FDA Premarket Approval
- **CE Marking**: EU conformity marking
- **Notified Body**: EU conformity assessment body
- **PMCF**: Post-Market Clinical Follow-up
- **QMS**: Quality Management System
{Additional terms as needed}

---

## Disclaimer

**Important Notice**

This briefing is an AI-based regulatory intelligence synthesis, not official regulatory advice.

- **No legal effect**: Briefing is for reference only and has no legal binding force
- **Expert review required**: All findings and recommendations require validation by qualified regulatory affairs professionals
- **Regulatory authority confirmation**: Final regulatory decisions must follow official guidance from FDA, Notified Bodies, MFDS, etc.
- **Limitation of liability**: Users are responsible for regulatory non-compliance resulting from use of this tool

Knowledge Base Date: 2026-01

---

This is reference information for professional review, not regulatory advice.
```

### 7. Summary Generation

**Compressed summary** (`briefing.summary.md`):

```markdown
# Briefing Summary

**Product**: {product-name}
**Date**: {YYYY-MM-DD}

- **Pipeline Steps Covered**: {list of available data}
- **Traffic Light**: {GREEN/YELLOW/RED}
- **Critical Path**: {region} ({timeline})
- **Total Budget**: {expected range}
- **Key Risks**: {top 3 risks}
- **Top Recommendations**: {top 3 actions}
- **Escalation Items**: {yes/no with count}
- **Sources**: FDA, EU MDR, MFDS regulations + all pipeline data

---
This summary captures the briefing report for audit trail.
```

### 8. File Storage

Save results to `.aria/products/{product-name}/{date}/`:
- `briefing.md` - Full comprehensive briefing report
- `briefing.summary.md` - Compressed summary for audit trail

### 9. Next Steps

- **Primary**: Review report with stakeholders (executive team, regulatory experts)
- **Alternative**: Execute immediate actions from recommendations
- **Optional**: Complete missing pipeline steps if partial data

## Output Contract

Before rendering output, `/aria:report` resolves:

- `output_type`: `full_report_md` (`briefing.md`) and `summary_md` (`briefing.summary.md`)
- `format`: `markdown | pdf | notion | gdocs`
- `language`: `ko | en`
- `audience`: `mixed` (executive + operator consumption)
- `depth`: `express | standard | deep` (default: `summary_md=express`, `full_report_md=deep`)
- `safety_flags`:
  - `preserve_regulatory_facts=true`
  - `preserve_numeric_values=true`
  - `preserve_disclaimer_strength=true`
- `graceful fallback`: if requested export is unavailable, fall back to `markdown` with an explicit notice.

## Format Output

**Format Selection** (via `--format` flag):

- `markdown` (default): Markdown report to `.aria/products/`

- `notion`: Notion page via Notion MCP connector (requires notion-mcp configuration)
  - Use `ToolSearch("notion mcp")` to find MCP tools
  - Graceful degradation: Fall back to Markdown if unavailable

- `gdocs`: Google Docs via Google Drive MCP connector (requires google-drive-mcp configuration)
  - Use `ToolSearch("google drive mcp")` to find MCP tools
  - Create document with title: "{Product Name} - Regulatory Briefing Report ({date})"
  - Also save Markdown backup to `.aria/products/`
  - Graceful degradation: Fall back to Markdown if unavailable

- `pdf`: PDF conversion from Markdown
  - Check for tools in order: `pandoc`, `wkhtmltopdf`, Python `weasyprint`
  - Generate Markdown first, then convert
  - Pandoc command: `pandoc briefing.md -o briefing.pdf --pdf-engine=xelatex --variable=geometry:margin=1in --toc`
  - Graceful degradation: Keep Markdown if no PDF tool available, display installation guidance

**Graceful Degradation**: If selected format's tool/MCP connector is unavailable, fall back to Markdown format with a notice explaining the limitation and how to install the required tool.

## Flags

- `--format markdown|notion|gdocs|pdf`: Output format (default: `markdown`)
- `--lang en|ko`: Output language (default: `ko`)
- `--depth express|standard|deep`: Narrative depth override (optional)

## Output Location

- `.aria/products/{product-name}/{date}/briefing.md` (always generated)
- `.aria/products/{product-name}/{date}/briefing.summary.md` (always generated)
- `.aria/products/{product-name}/{date}/briefing.pdf` (when `--format pdf`)
- Notion page or Google Docs (when alternative format selected, link provided to user)

## Data Sources

All pipeline data from `.aria/` directory is the primary source. Built-in knowledge supplements briefing structure and executive summary framework. External data connectors (Notion, Context7) are reflected via pipeline data already generated.

## Report Issuance Policy (ER-017)

**Critical Rule**: Full formatted report is NOT generated in the same turn as initial analysis.

**Two-Phase Approach**:
1. **Analysis Phase**: Output only key findings, traffic light, items for confirmation
2. **Report Phase**: After user reviews and confirms, generate full formatted report

**User confirmation required before full report generation.**

## Traffic Light Interpretation

- **GREEN**: All pipeline steps GREEN, low-risk regulatory path
- **YELLOW**: Any step YELLOW, moderate-high risk, expert review recommended
- **RED**: Multiple RED flags, significant regulatory barriers, fundamental approach change needed

The overall traffic light is the most conservative (highest caution) across all pipeline steps.

## Example

```
/aria:report
```
> System loads all available pipeline data
> Presents analysis summary (Phase A)
> User confirms
> Generates comprehensive briefing report (Phase B, Markdown format)

```
/aria:report --format gdocs --lang en
```
> English output, Google Docs format
> Loads all pipeline data
> Presents analysis summary
> User confirms
> Generates Google Docs briefing via Google Drive MCP

```
/aria:report Clinical Strategy
```
> Focus area: Clinical Strategy
> Emphasizes clinical evidence requirements and trial planning in recommendations

```
/aria:report --format pdf
```
> Loads all pipeline data
> Presents analysis summary (Phase A)
> User confirms
> Generates Markdown briefing
> Converts to PDF using available tool (pandoc/wkhtmltopdf/weasyprint)

## Disclaimer

**Important Notice**

This briefing is an AI-based regulatory intelligence synthesis, not official regulatory advice.

- **No legal effect**: Briefing is for reference only and has no legal binding force
- **Expert review required**: All findings and recommendations require validation by qualified regulatory affairs professionals
- **Regulatory authority confirmation**: Final regulatory decisions must follow official guidance from FDA, Notified Bodies, MFDS, etc.
- **Limitation of liability**: Users are responsible for regulatory non-compliance resulting from use of this tool

Knowledge Base Date: 2026-01

---

This is reference information for professional review, not regulatory advice.
