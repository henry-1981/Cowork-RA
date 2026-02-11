---
description: "Regulatory project cost and timeline estimation - Three-point estimates with optimistic/expected/pessimistic ranges"
argument-hint: "[Options] [--lang en|ko]"
---

# /aria:estimate - Cost & Timeline Estimation

## Purpose

Provide regulatory project cost and timeline estimation with three-point ranges (optimistic/expected/pessimistic) based on pathway selections. Includes cost breakdown by category and milestone-based timeline.

## Workflow

### 1. Product Context Loading

- Load active product from `.aria/active_product.json`
- If multiple products exist, prompt for selection
- If no products exist, display error: "제품을 먼저 생성하거나 선택하세요"

### 2. Pathway Data Loading

- Check for pathway results: `.aria/products/{product-name}/{date}/pathway.summary.md`
- If pathway data NOT found:
  - Display warning: **"⚠️ 경로 선택 데이터가 필요합니다. 먼저 `/aria:pathway` 명령을 실행하세요."**
  - Suggest: Run `/aria:pathway` first
  - STOP workflow

### 3. Cost Estimation

- Activate estimation skill with loaded pathway data
- Apply three-point cost estimation per region:
  - **Optimistic**: Best-case scenario (fast approvals, minimal deficiencies)
  - **Expected**: Most likely scenario (industry average)
  - **Pessimistic**: Worst-case scenario (delays, re-testing, extended review)
- Break down by cost categories:
  - Consulting services (컨설팅 비용)
  - Testing & validation (시험 비용)
  - Regulatory fees (규제 수수료)
  - Notified Body fees (인증 기관 비용, EU only)
  - Clinical study costs (임상시험 비용, if applicable)
- Calculate multi-region total with shared cost savings

### 4. Timeline Estimation

- Apply milestone-based timeline per pathway:
  - Phase 1: Preparation
  - Phase 2: Testing
  - Phase 3: Documentation
  - Phase 4: Submission & Review
  - Phase 5: Clinical Study (if applicable)
- Assign duration ranges (optimistic/expected/pessimistic)
- Identify critical path (longest timeline)

### 5. Multi-Region Analysis

- Identify shared costs (common testing, consulting overlap)
- Calculate parallel vs. sequential submission timelines
- Highlight cost-saving opportunities

### 6. Output Generation

**Full output** (`estimate.md`):
- Header (command, product, date, version)
- Cost estimation summary table (optimistic/expected/pessimistic)
- Cost breakdown by region and category
- Timeline estimation with milestones
- Multi-region cost savings analysis
- Traffic light assessment
- Disclaimer emphasizing estimate uncertainty

**Compressed summary** (`estimate.summary.md`):
- Cost ranges
- Timeline ranges
- Critical path
- Traffic light status

### 7. Next Steps

- **Primary**: `/aria:plan` (milestone planning)
- **Alternative**: Detailed budget approval and vendor quotes

## Flags

- `--lang en|ko`: Output language (default: `ko`)

## Output Location

- `.aria/products/{product-name}/{date}/estimate.md`
- `.aria/products/{product-name}/{date}/estimate.summary.md`

## Data Sources

Industry average costs and timelines (2026-01) from Korean regulatory consulting market. Actual costs vary by project complexity, testing requirements, and market conditions. External cost databases are used only when configured.

## Example

```
/aria:estimate
```

Generates cost and timeline estimates for all pathways identified in `/aria:pathway`.

## Dependencies

- **Required**: `/aria:pathway` must be executed first
- **Input**: Pathway selections from `.summary.md`
- **Output**: Cost/timeline estimates for downstream `/aria:plan`

## Traffic Light Interpretation

- **🟢 GREEN**: Low cost/short timeline (< ₩150M, < 12 months)
- **🟡 YELLOW**: Moderate-high cost/long timeline (₩150-500M, 12-24 months, clinical study)

## Notes

- Cost ranges are based on Korean market averages (2026-01)
- Clinical trial costs have high uncertainty (±50% cost, ±100% timeline)
- Class III devices (PMA, EU Class III, MFDS Grade 4) have inherently high estimate variability
- Multi-region submissions achieve 15-30% cost savings through shared testing
- Estimates are NOT confirmed quotes - actual project costs require vendor quotes
