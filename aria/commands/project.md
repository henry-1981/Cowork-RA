---
description: Project planning pipeline - Combines cost/timeline estimation and milestone planning into an integrated project plan
argument-hint: "[Options] [--lang en|ko] [--format markdown|pdf|notion|gdocs]"
---

# /aria:project - Project Planning Orchestrator

## Purpose

Integrated project planning pipeline that answers: "When, how much, and in what order?" Combines cost/timeline estimation and milestone planning into a single orchestrated workflow. Leverages assessment results from `/aria:assess` when available.

**Replaces**: `/aria:estimate`, `/aria:plan`, `/aria:compare` (for project context)

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

### 2. Assessment Data Loading

Check for assessment results in `.aria/products/{product-name}/{date}/`:

**Case A: assess.summary.md exists**
- Load assessment summary (classification, pathways, traffic light)
- Extract pathway selections and classification data for estimation input
- Inform user: "Assessment data loaded from {date}."

**Case B: Legacy pipeline data exists** (determination.summary.md, classification.summary.md, pathway.summary.md)
- Load available legacy summaries as fallback
- Extract pathway and classification data
- Inform user: "Legacy pipeline data loaded. Consider running /aria:assess for integrated results."

**Case C: No assessment or legacy data found**
- Inform user: "No assessment data found. For best results, run `/aria:assess` first."
- Allow manual input: Accept pathway and classification information directly from user
- Collect minimum required data:
  - Target markets (FDA, EU MDR, MFDS)
  - Device class per market
  - Expected pathway per market
- Proceed with user-provided data

### 3. Estimation Phase

Invoke the estimation skill with loaded pathway data:

- Skill("aria-estimation") with pathway selections and classification data
- Apply three-point cost estimation per region:
  - **Optimistic**: Best-case scenario (fast approvals, minimal deficiencies)
  - **Expected**: Most likely scenario (industry average)
  - **Pessimistic**: Worst-case scenario (delays, re-testing, extended review)
- Break down by cost categories:
  - Consulting services
  - Testing & validation
  - Regulatory fees
  - Notified Body fees (EU only)
  - Clinical study costs (if applicable)
- Apply milestone-based timeline estimation per pathway
- Identify critical path (longest timeline)

### 4. Planning Phase

Invoke the planning skill with estimation results:

- Skill("aria-planning") with estimation data and pathway selections
- Select appropriate plan template based on pathways:
  - 510(k): 4-phase plan (Preparation, Testing, Documentation, Submission/Review)
  - PMA: 4-phase plan with clinical trial phase
  - De Novo: 4-phase plan with special controls development
  - EU MDR IIa/IIb: 3-phase plan with Notified Body assessment
  - MFDS Grade 1-2: 4-phase plan
  - MFDS Grade 3-4: 5-phase plan with clinical data/trial
- Map timeline estimates to phases with deliverables
- Define dependencies (sequential, parallel, milestone)
- Calculate cumulative timeline per strategy

### 5. Multi-Region Optimization (if 2+ target markets)

When the product targets 2 or more markets, apply comparison logic inline:

**Parallel Execution Analysis**:
- Identify shared phases across regions (common testing, shared documentation)
- Calculate parallel vs. sequential timeline impact
- Estimate cost savings from shared activities (15-30% typical)

**Optimization Recommendations**:
- Common testing reuse (biocompatibility, electrical safety, performance)
- Harmonized documentation strategy (design to most stringent requirement)
- Parallel submission scheduling (offset by preparation time)
- Critical path optimization (focus resources on bottleneck)

**Dependency Mapping**:
```
Common Testing -> FDA Documentation -> FDA Submission
              -> EU Documentation  -> EU Submission
              -> MFDS Documentation -> MFDS Submission
```

### 6. Output Generation

**Full output** (`project.md`):

```markdown
# Regulatory Project Plan

## Product Information
- Product: {product-name}
- Date: {YYYY-MM-DD}
- Target Markets: {FDA, EU MDR, MFDS}
- Assessment Reference: {assess.summary.md date, if available}

## 1. Cost Estimation

### Total Cost Range

| Scenario | Cost Range |
|----------|-----------|
| Optimistic | {range} |
| Expected | {range} |
| Pessimistic | {range} |

### Cost Breakdown by Region

#### FDA ({pathway})
| Category | Percentage | Optimistic | Expected | Pessimistic |
|----------|-----------|------------|----------|-------------|
| Consulting | {%} | {amount} | {amount} | {amount} |
| Testing | {%} | {amount} | {amount} | {amount} |
| Regulatory Fees | {%} | {amount} | {amount} | {amount} |
| Clinical (if applicable) | {%} | {amount} | {amount} | {amount} |

#### EU MDR ({pathway})
{Same structure}

#### MFDS ({pathway})
{Same structure}

### Multi-Region Cost Savings
- Shared testing: {savings estimate}
- Consulting overlap: {savings estimate}
- Parallel submission benefits: {savings estimate}

## 2. Timeline Estimation

### Total Timeline Range

| Scenario | Duration |
|----------|----------|
| Optimistic | {months} |
| Expected | {months} |
| Pessimistic | {months} |

### Milestone Timeline per Region

#### FDA ({pathway})
| Phase | Duration | Deliverables |
|-------|----------|-------------|
| Preparation | {months} | {deliverables} |
| Testing | {months} | {deliverables} |
| Documentation | {months} | {deliverables} |
| Submission & Review | {months} | {deliverables} |

#### EU MDR ({pathway})
{Same structure}

#### MFDS ({pathway})
{Same structure}

### Critical Path
- Region: {region with longest timeline}
- Duration: {timeline range}
- Bottleneck Phase: {phase description}

## 3. Milestone Plan

### Project Overview
- Strategy: {parallel/sequential submission}
- Total Phases: {number}
- Key Dependencies: {dependency summary}

### Phase-by-Phase Execution

#### Phase 1: Preparation ({duration})
- **Objective**: {phase goal}
- **Activities**: {activity list}
- **Deliverables**: {deliverable list}
- **Dependencies**: {dependencies or "None"}
- **Cost Allocation**: {amount} ({percentage})
- **Responsible**: {organization type}

{Repeat for all phases}

### Multi-Region Parallel Submission Plan

#### Common Phases (shared across markets)
- Testing: {duration, cost savings}

#### Region-Specific Parallel Tracks
| Region | Documentation | Submission | Review | Total |
|--------|--------------|------------|--------|-------|
| FDA | {duration} | {duration} | {duration} | {total} |
| EU MDR | {duration} | {duration} | {duration} | {total} |
| MFDS | {duration} | {duration} | {duration} | {total} |

### Dependency Map
{Visual dependency diagram}

### Key Milestones Table

| Milestone | Expected Date | Dependencies | Priority |
|-----------|--------------|-------------|----------|
| {milestone} | {date} | {deps} | {priority} |

## 4. Risk Assessment

### Traffic Light Summary
| Component | Status |
|-----------|--------|
| Cost | {GREEN/YELLOW} |
| Timeline | {GREEN/YELLOW} |
| Complexity | {GREEN/YELLOW} |
| **Overall** | **{most conservative}** |

### Key Risks and Mitigation
1. {Risk}: {Mitigation strategy}
2. {Risk}: {Mitigation strategy}
3. {Risk}: {Mitigation strategy}

### Contingency Plan
- Buffer time: {duration}
- Alternative strategies: {alternatives}

## 5. Recommended Next Steps
1. Internal budget approval and resource allocation
2. Vendor/consultant contract negotiations
3. Project team formation and kickoff
4. Weekly progress monitoring setup

## Disclaimer

**Important Notice**

This project plan is an AI-based estimate, not a confirmed schedule or budget.

- **No legal effect**: Estimates are for reference only and have no legal binding force
- **Not confirmed quotes**: Actual costs require vendor quotes and detailed scoping
- **Timeline variability**: Actual timelines depend on testing results, regulatory feedback, and resource availability
- **Expert review required**: Project plans require validation by regulatory affairs and project management professionals
- **Limitation of liability**: Users are responsible for project decisions made based on this tool's output

Knowledge Base Date: 2026-01

---

This is reference information for professional review, not regulatory advice.
```

**Compressed summary** (`project.summary.md`):

```markdown
# Project Summary

**Product**: {product-name}
**Date**: {YYYY-MM-DD}
**Target Markets**: {markets}

## Cost Ranges
- **Optimistic**: {amount}
- **Expected**: {amount}
- **Pessimistic**: {amount}

## Timeline Ranges
- **Optimistic**: {months}
- **Expected**: {months}
- **Pessimistic**: {months}

## Critical Path
- **Region**: {region}
- **Duration**: {timeline}
- **Bottleneck**: {phase}

## Submission Strategy
- **Approach**: {parallel/sequential}
- **Phases**: {number of phases}
- **Key Milestones**: {count}

## Overall Traffic Light
- **Assessment**: {GREEN/YELLOW}

---
This summary is consumed by `/aria:report` command.
```

### 7. File Storage

Save results to `.aria/products/{product-name}/{date}/`:
- `project.md` - Full integrated project plan
- `project.summary.md` - Compressed summary for downstream commands

### 8. Next Steps

- **Primary**: `/aria:report` to generate comprehensive executive briefing
- **Alternative**: Internal budget approval and resource allocation
- **Optional**: Vendor contract negotiations and testing lab engagement

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

- `.aria/products/{product-name}/{date}/project.md`
- `.aria/products/{product-name}/{date}/project.summary.md`

## Data Sources

Assessment results from `/aria:assess` are the primary input. Built-in cost/timeline frameworks (2026-01 Korean market averages) provide estimation baselines. External data connectors (Notion, Context7) are used only when configured.

## Skills Used

- `aria-estimation`: Cost/timeline three-point estimation
- `aria-planning`: Milestone plan generation with dependencies
- Comparison logic: Inline multi-region optimization (no separate skill)

## Traffic Light Interpretation

- **GREEN**: Total cost < W150M, timeline < 12 months, no clinical study
- **YELLOW**: Cost W150-500M or timeline 12-24 months or clinical study required

The overall traffic light is the most conservative across cost, timeline, and complexity.

## Example

```
/aria:project
```
> System loads assessment data (or prompts for /aria:assess)
> Runs estimation -> planning pipeline
> Generates integrated project plan

```
/aria:project --lang en --format gdocs
```
> English output, Google Docs format
> Same pipeline execution
> Google Docs creation via Google Drive MCP

```
/aria:project --format pdf
```
> System loads assessment data
> Runs estimation -> planning pipeline
> Generates Markdown then converts to PDF

## Disclaimer

**Important Notice**

This project plan is an AI-based estimate, not a confirmed schedule or budget.

- **No legal effect**: Estimates are for reference only and have no legal binding force
- **Not confirmed quotes**: Actual costs require vendor quotes and detailed scoping
- **Timeline variability**: Actual timelines depend on testing results, regulatory feedback, and resource availability
- **Expert review required**: Project plans require validation by regulatory affairs and project management professionals
- **Limitation of liability**: Users are responsible for project decisions made based on this tool's output

Knowledge Base Date: 2026-01

---

This is reference information for professional review, not regulatory advice.
