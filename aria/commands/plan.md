---
description: "Regulatory milestone planning - Generates phase-based project plans with deliverables, dependencies, and critical path analysis"
argument-hint: "[Options] [--lang en|ko]"
---

# /aria:plan - Regulatory Milestone Planning

## Purpose

Generate phase-based regulatory project plans with milestones, deliverables, dependencies, and critical path analysis. Creates actionable execution roadmap for regulatory submissions.

## Workflow

### 1. Product Context Loading

- Load active product from `.aria/active_product.json`
- If multiple products exist, prompt for selection
- If no products exist, display error: "제품을 먼저 생성하거나 선택하세요"

### 2. Input Data Loading

- Check for pathway results: `.aria/products/{product-name}/{date}/pathway.summary.md`
- Check for estimation results: `.aria/products/{product-name}/{date}/estimate.summary.md`
- If either NOT found:
  - Display warning: **"⚠️ 경로 및 비용 추정 데이터가 필요합니다. 먼저 `/aria:pathway` 및 `/aria:estimate` 명령을 실행하세요."**
  - Suggest: Run `/aria:pathway` and `/aria:estimate` first
  - STOP workflow

### 3. Plan Template Selection

- Activate planning skill with loaded pathway and estimation data
- Select appropriate plan template based on pathways:
  - 510(k): 4-phase plan (Preparation, Testing, Documentation, Submission/Review)
  - PMA: 4-phase plan with clinical trial phase
  - De Novo: 4-phase plan with special controls development
  - EU MDR IIa/IIb: 3-phase plan with Notified Body assessment
  - MFDS Grade 1-2: 4-phase plan (Preparation, Testing, Documentation, Review)
  - MFDS Grade 3-4: 5-phase plan with clinical data/trial

### 4. Milestone Mapping

- Map timeline estimates from `/aria:estimate` to phases
- Assign duration to each phase (optimistic/expected/pessimistic)
- Define deliverables per phase
- Identify dependencies (sequential, parallel, milestone)

### 5. Multi-Region Integration

- If multiple target regions:
  - Identify shared phases (common testing)
  - Determine parallel vs. sequential submission strategy
  - Map cross-region dependencies
  - Calculate critical path (longest timeline)
  - Highlight cost-saving opportunities from parallel execution

### 6. Dependency Mapping

- **Sequential Dependencies**: Task B starts after Task A completes (A → B)
- **Parallel Dependencies**: Tasks share common inputs (C ⇒ A, C ⇒ B)
- **Milestone Dependencies**: Multiple tasks must complete before next phase ([A, B, C] ⟹ D)

### 7. Output Generation

**Full output** (`plan.md`):
- Header (command, product, date, version)
- Project overview (goals, strategy, timeline)
- Phase-by-phase execution plan:
  - Phase objective
  - Activities
  - Deliverables
  - Dependencies
  - Cost allocation
  - Responsible organization
- Multi-region parallel submission plan
- Dependency map (visual diagram)
- Key milestones table
- Risk factors and mitigation strategies
- Next steps
- Traffic light assessment
- Disclaimer

**Compressed summary** (`plan.summary.md`):
- Total timeline
- Critical path
- Phase list with durations
- Key milestones
- Traffic light status

### 8. Next Steps

- **Primary**: Internal budget approval and resource allocation
- **Secondary**: Vendor contract negotiations (consulting, testing labs)
- **Ongoing**: Weekly progress monitoring

## Flags

- `--lang en|ko`: Output language (default: `ko`)

## Output Location

- `.aria/products/{product-name}/{date}/plan.md`
- `.aria/products/{product-name}/{date}/plan.summary.md`

## Data Sources

Regulatory project management best practices (2026-01). Phase templates based on industry standards for FDA 510(k)/PMA, EU MDR, and MFDS submissions.

## Example

```
/aria:plan
```

Generates milestone plan based on pathway and estimation results from prior commands.

## Dependencies

- **Required**: `/aria:pathway` and `/aria:estimate` must be executed first
- **Input**: Pathway selections and timeline estimates from `.summary.md` files
- **Output**: Actionable execution plan for regulatory submissions

## Traffic Light Interpretation

- **🟢 GREEN**: Total timeline < 12 months, no clinical study, low complexity
- **🟡 YELLOW**: Timeline 12-24 months, clinical study required, or multi-region complex dependencies

## Notes

- Plans are reference frameworks, not confirmed schedules
- Actual project timelines depend on testing results, regulatory feedback, and resource availability
- High-risk devices (Class III, Grade 4) always receive YELLOW traffic light
- Multi-region plans identify opportunities for parallel execution
- Plans should be reviewed and updated regularly during project execution
- Critical path is the longest sequence of dependent activities determining minimum project duration
