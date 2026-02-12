---
name: aria-planning
description: >
  Regulatory milestone planning with phase management, deliverables, and dependencies.
  Creates structured regulatory project plans based on pathway and estimation data.
allowed-tools: Read Grep Glob
user-invocable: false
metadata:
  version: "0.1.0"
  category: "domain"
  status: "active"
  updated: "2026-02-12"
  modularized: "false"
  tags: "planning, milestones, phases, dependencies, project-management"
  knowledge-base-date: "2026-01"

# MoAI Extension: Progressive Disclosure
progressive_disclosure:
  enabled: true
  level1_tokens: 100
  level2_tokens: 2000

# MoAI Extension: Triggers
triggers:
  keywords: ["plan", "milestone", "schedule", "roadmap", "project plan"]
  phases: ["run"]
---

# Regulatory Milestone Planning Skill

## Purpose

Generate phase-based regulatory project plans with milestones, dependencies, and critical path analysis. This is a pure analysis unit that receives pathway and estimation data and returns a structured project plan.

**Input**: Pathway and estimation results (selected pathways, cost/timeline estimates per region)
**Output**: Milestone plan with phases, deliverables, dependencies, critical path, traffic light indicator
**Knowledge Base Date**: 2026-01

---

## Planning Framework

### Phase Structure

All regulatory plans follow a standard 4-6 phase structure:

1. **Preparation**
   - Gap analysis
   - Resource allocation
   - Strategy finalization

2. **Testing & Validation**
   - Biocompatibility testing
   - Performance testing
   - Electrical safety testing
   - Software validation (if applicable)

3. **Documentation**
   - Technical file creation
   - Submission package assembly
   - Clinical evaluation report (if applicable)

4. **Submission & Review**
   - Regulatory submission
   - Deficiency response
   - Approval/certification

5. **Clinical Study** (if applicable)
   - Protocol development
   - IRB approval
   - Patient enrollment
   - Data collection and analysis

6. **Post-Market** (optional in initial plan)
   - Post-market surveillance setup
   - Vigilance system implementation

---

## Dependency Types

### Sequential Dependencies
- **Hard Dependency**: Task B cannot start until Task A completes
  - Example: "Documentation" depends on "Testing completion"
  - Notation: A -> B

### Parallel Dependencies
- **Shared Resource**: Tasks can run in parallel but share common inputs
  - Example: FDA and EU submissions both depend on "Common Testing"
  - Notation: C => A, C => B

### Milestone Dependencies
- **Checkpoint**: Multiple tasks must complete before next phase begins
  - Example: All testing must finish before documentation starts
  - Notation: [A, B, C] => D

---

## Plan Templates by Pathway

| Pathway | Phase 1 | Phase 2 | Phase 3 | Phase 4 | Critical Path |
|---------|---------|---------|---------|---------|---------------|
| **510(k)** | Preparation (1-2mo): Predicate search, Gap analysis | Testing (2-4mo): Biocomp, Electrical, Performance | Documentation (1-2mo): 510(k) package, SE report | Review (3-6mo): Submission, Deficiency response | Phase 4 (FDA review) |
| **PMA** | IDE Preparation (2-4mo): IDE app, IRB approval | Clinical Study (12-24mo): Patient enrollment, Data collection | PMA Documentation (3-6mo): PMA package, QMS docs | FDA Review (6-12mo): Panel meeting, Approval | Phase 2 (Clinical study) |
| **EU IIa** | Preparation (1-3mo): NB selection, Tech file structure | Testing/CER (3-6mo): Testing, CER, PMSP | NB Assessment (2-4mo): NB audit, CE cert | - | Phase 2 (Testing/CER) |
| **MFDS G2** | Preparation (1-2mo): Protocol, Doc plan | Testing (2-4mo): Non-clinical tests, Validation | Documentation (1-2mo): Approval package | Review (2-4mo): MFDS submission | Phase 2 (Testing) |

---

## Multi-Region Planning

### Parallel Submission Strategy

When submitting to multiple regions simultaneously:

**Shared Phases** (run once, benefit all):
- Common Testing (biocompatibility, electrical safety, performance)
- Clinical data collection (if shared across regions)

**Region-Specific Phases** (run in parallel):
- FDA 510(k) documentation
- EU MDR technical file
- MFDS approval application

**Dependency Map**:
```
Common Testing -> FDA Documentation -> FDA Submission
              -> EU Documentation -> EU Submission
              -> MFDS Documentation -> MFDS Submission
```

**Critical Path**: Region with longest review time

---

### Sequential Submission Strategy

When staggering submissions (e.g., US first, then EU/Korea):

**Phase Order**:
1. Common Testing
2. FDA Submission -> FDA Approval
3. EU Submission (using FDA approval data)
4. MFDS Submission (using FDA/EU data)

**Advantage**: Later submissions can reference earlier approvals
**Disadvantage**: Longer total timeline

---

## Analysis Workflow

### Step 1: Receive Input Data

Accept pathway and estimation results as input:
- Selected pathways per region
- Cost/timeline estimates per region
- Target regions

If input data is not provided, return an error indicating pathway and estimation analysis are required first.

### Step 2: Select Plan Template

Based on pathway data, select appropriate template:
- 510(k) -> 4-phase plan
- PMA -> 4-phase plan with clinical trial
- De Novo -> 4-phase plan with special controls
- EU MDR IIa/IIb -> 3-phase plan with Notified Body
- MFDS Grade 1-2 -> 4-phase plan
- MFDS Grade 3-4 -> 5-phase plan with clinical data/trial

### Step 3: Map Milestones to Timeline

Using timeline estimates:
- Assign duration to each phase (optimistic, expected, pessimistic)
- Calculate cumulative timeline
- Identify phase dependencies

### Step 4: Multi-Region Integration

If multiple target regions:
- Identify shared phases (common testing)
- Determine parallel vs. sequential strategy
- Map dependencies across regions
- Calculate critical path

### Step 5: Assign Traffic Light

- **GREEN**: Total timeline < 12 months, no clinical study, low complexity
- **YELLOW**: Timeline 12-24 months or clinical study required or multi-region complex dependencies

### Step 6: Return Structured Result

Return the project plan containing:
- Phase-by-phase breakdown with durations
- Deliverables per phase
- Dependencies map (sequential, parallel, milestone)
- Multi-region integration plan (if applicable)
- Critical path identification
- Key milestones with estimated dates
- Risk factors and mitigation strategies
- Traffic light assessment

---

## Traffic Light Definitions

- **GREEN**: Total timeline < 12 months, no clinical study, single or dual-market, low complexity
- **YELLOW**: Timeline 12-24 months, clinical study required, or multi-region with complex dependencies
- **RED**: Not used (all plans are feasible with appropriate resources)

---

## Data Source Strategy

1. **Built-in Knowledge** (Primary): Phase templates and dependency frameworks
2. **Pathway Data** (Input): Pathway selection results from pathway skill
3. **Estimation Data** (Input): Cost/timeline estimates from estimation skill

For MCP integration patterns (tool discovery, graceful degradation, source attribution), see `CONNECTORS.md`.
