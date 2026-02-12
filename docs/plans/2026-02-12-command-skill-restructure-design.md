# SPEC-ARIA-003: Command & Skill Architecture Restructure

**Date**: 2026-02-12
**Status**: Design Approved
**Branch**: feature/SPEC-ARIA-003

---

## Problem Statement

Current ARIA architecture has significant redundancy between commands (8) and skills (8). Commands are essentially 1:1 wrappers around skills with duplicated workflow logic (product loading, flag handling, file storage, pipeline connections). This makes maintenance difficult and creates confusion about where logic should live.

---

## Design Decision

**Approach**: Functional Group Commands (Approach A)

- **Commands** = complex orchestrators that combine multiple skills for meaningful business workflows
- **Skills** = atomic, pure analysis logic units (no I/O, no file management)
- **Chat** = conversational advisor entry point with organic skill integration

---

## Architecture Overview

### Commands (4 - Complex Orchestrators)

| Command | Purpose | Skills Used |
|---------|---------|-------------|
| `/aria:chat` | Conversational entry, product profile builder, skill router | Any (on-demand) |
| `/aria:assess` | Regulatory assessment pipeline | determination + classification + pathway + comparison logic |
| `/aria:project` | Project planning pipeline | estimation + planning + comparison logic |
| `/aria:brief` | Comprehensive integrated report | All results synthesis (absorbs briefing skill) |

### Skills (5 - Pure Analysis Logic)

| Skill | Purpose | Produces |
|-------|---------|----------|
| determination | Medical device qualification evaluation | YES/NO/CONDITIONAL + traffic light |
| classification | Multi-region class determination | FDA I/II/III, EU I/IIa/IIb/III, MFDS 1/2/3/4 |
| pathway | Regulatory submission route selection | Route recommendations per region |
| estimation | Cost/timeline 3-point estimation | Optimistic/Expected/Pessimistic ranges |
| planning | Milestone plan generation | 4-6 milestone regulatory plan |

### Infrastructure

| Component | Location | Purpose |
|-----------|----------|---------|
| Connectors | `CONNECTORS.md` (existing) | MCP integration patterns |
| Product context | `.aria/active_product.json`, `.aria/products/` | Product data management |
| Playbook | `aria.local.md` | Organization settings |

---

## Command Designs

### /aria:chat - Conversational Regulatory Advisor

**Core Concept**: Natural conversation with a regulatory expert. Product information accumulates organically. Skills are woven into the conversation transparently.

**Design Principles**:

1. **Conversation first, structure behind**: No "Step 1, 2, 3" shown to users. Skills operate transparently within natural dialogue
2. **Progressive information accumulation**: Product info saved to `.aria/` automatically during conversation. No explicit "profile complete" step
3. **Skills as tools, conversation as interface**: Skill invocation may be invisible to users. ARIA delivers results naturally within dialogue
4. **Depth on demand**: Full reports generated only when user requests deeper analysis

**Input Modes**:
- Conversational Q&A: ARIA asks questions to build product understanding
- Document upload: Auto-extract product info from technical documents/PDFs, gap analysis + minimal Q&A (1-3 rounds)
- Both modes supported, flexible based on situation

**Product Profile Schema**:
```json
{
  "name": "string",
  "description": "string",
  "intended_use": "string",
  "product_form": "hardware | software | IVD | combination",
  "primary_function": "string",
  "target_markets": ["US", "EU", "Korea"],
  "completeness": 0-100
}
```

**Auto-suggestion Logic**:
- Profile sufficient + no assess data -> Suggest `/aria:assess`
- Assess data exists -> Suggest `/aria:project`
- All data exists -> Suggest `/aria:brief`
- User approval required before execution

**Conversation Example**:
```
User: We're developing a wearable that measures heart rate.
      Not sure where to start with regulatory.

ARIA: Heart rate monitoring wearable. Does this device also detect
      arrhythmias or is it purely heart rate measurement?

User: It detects arrhythmia and alerts the doctor.

ARIA: With arrhythmia detection and physician alerting, this device
      likely qualifies as a medical device across all regions:
      [determination skill runs internally]

      - FDA: Medical device (diagnostic purpose)
      - EU MDR: Medical device (Article 2(1))
      - MFDS: Medical device (disease diagnosis purpose)

      Want me to check the classification? Or shall we decide
      target markets first?

User: US and Korea. What class would it be?

ARIA: [classification skill runs]

      Expected classification:
      - FDA: Class II (arrhythmia detection -> 510(k))
      - MFDS: Class 2 (ECG-based -> certification)

      Both mid-risk. 510(k) + MFDS certification path available.
      Let me know if you'd like cost/timeline estimates.
```

### /aria:assess - Regulatory Assessment Orchestrator

**Purpose**: "Where does my product stand in the regulatory landscape?"

**Execution Flow**:
1. Load product context (existing profile or new input)
2. Run determination skill -> YES/NO/CONDITIONAL
   - NO -> Stop with rationale
   - CONDITIONAL -> Warning, continue
   - YES -> Continue
3. Run classification skill -> Multi-region class matrix
   - Pass results as pathway input
4. Run pathway skill -> Optimal submission routes
   - Uses classification results
5. Apply comparison logic (if 2+ markets)
6. Generate integrated output

**Output**: `assess.md` + `assess.summary.md`

**Flags**: `--lang en|ko`, `--format markdown|pdf|notion|gdocs`

### /aria:project - Project Planning Orchestrator

**Purpose**: "When, how much, and in what order?"

**Execution Flow**:
1. Load assess results (auto if available, collect if not)
2. Run estimation skill -> Cost/timeline 3-point estimates
3. Run planning skill -> Milestone plan based on estimates
4. Apply comparison logic (if 2+ markets, optimize parallel execution)
5. Generate integrated output

**Output**: `project.md` + `project.summary.md`

**Flags**: `--lang en|ko`, `--format markdown|pdf|notion|gdocs`

### /aria:brief - Comprehensive Report Generator

**Purpose**: All pipeline data into single executive-ready document

**Execution Flow**:
1. Collect all existing data from `.aria/products/{product}/{date}/`
2. Analyze data completeness
   - Sufficient -> Generate report
   - Insufficient -> Guide user to run assess/project first
3. Generate integrated briefing (absorbs briefing skill logic)
   - Executive Summary
   - Regulatory Assessment Summary (assess data)
   - Project Plan Summary (project data)
   - Recommendations & Risks
   - Appendix (data sources, disclaimer)
4. Output in requested format

**Output**: `briefing.md` (+ pdf/notion/gdocs variants)

**Flags**: `--lang en|ko`, `--format markdown|pdf|notion|gdocs`

---

## Skill Refactoring

### What to REMOVE from each skill (moves to command responsibility):
- Product context loading logic
- Flag handling (`--lang`, `--format`)
- File storage logic (`.aria/products/`)
- Pipeline connections ("Next step: /aria:XXX")
- Input collection workflows

### What to KEEP in each skill:
- Pure analysis frameworks (FDA/EU MDR/MFDS criteria)
- Module references (`modules/` directory)
- Decision frameworks and classification rules
- Traffic light / escalation logic
- Knowledge base date references

---

## Data Flow

```
User
  |
  +-- /aria:chat ---- natural conversation --+
  |   (accumulates product info,              |
  |    invokes skills transparently)          |
  |                                           |
  +-- /aria:assess --+-- determination --+    |
  |                  +-- classification --+ -> assess.md
  |                  +-- pathway --------+    |
  |                  (+ comparison logic)     |
  |                                           |
  +-- /aria:project -+-- estimation -----+    |
  |                  +-- planning -------+ -> project.md
  |                  (+ comparison logic)     |
  |                                           |
  +-- /aria:brief -- all results --------- -> briefing.md
                                              |
  Product Context (.aria/) <------------------+
```

### Context Passing:
- **chat -> assess**: `profile.json` product info
- **assess -> project**: `assess.summary.md` routes/classes
- **all -> brief**: `.summary.md` files collected and synthesized

---

## File Structure

### Before (Current - 7 individual files per analysis):
```
.aria/products/{product}/{date}/
+-- determination.md + determination.summary.md
+-- classification.md + classification.summary.md
+-- pathway.md + pathway.summary.md
+-- estimation.md + estimation.summary.md
+-- plan.md + plan.summary.md
+-- comparison.md + comparison.summary.md
+-- briefing.md + briefing.summary.md
```

### After (New - 3 integrated reports + 1 profile):
```
.aria/products/{product}/{date}/
+-- profile.json          # Product profile (managed by chat)
+-- assess.md             # Integrated regulatory assessment
+-- assess.summary.md     # Compressed summary
+-- project.md            # Integrated project plan
+-- project.summary.md    # Compressed summary
+-- briefing.md           # Comprehensive briefing report
```

---

## Migration Plan

### Files to DELETE (6 commands):
- `aria/commands/determine.md`
- `aria/commands/classify.md`
- `aria/commands/pathway.md`
- `aria/commands/estimate.md`
- `aria/commands/plan.md`
- `aria/commands/compare.md`

### Files to CREATE (2 commands):
- `aria/commands/assess.md` (regulatory assessment orchestrator)
- `aria/commands/project.md` (project planning orchestrator)

### Files to REWRITE (2 commands):
- `aria/commands/chat.md` (conversational advisor redesign)
- `aria/commands/brief.md` (absorb briefing skill, new file structure)

### Skills to REFACTOR (5 - remove I/O, keep pure logic):
- `aria/skills/determination/SKILL.md`
- `aria/skills/classification/SKILL.md`
- `aria/skills/pathway/SKILL.md`
- `aria/skills/estimation/SKILL.md`
- `aria/skills/planning/SKILL.md`

### Skills to DELETE (2):
- `aria/skills/briefing/SKILL.md` -> absorbed by `/aria:brief` command
- `aria/skills/comparison/SKILL.md` -> absorbed by assess/project commands

### Skills to MOVE (1):
- `aria/skills/connectors/SKILL.md` -> merge into `CONNECTORS.md` infrastructure doc

### Documentation to UPDATE:
- `aria/README.md` - New command system
- `aria/.claude-plugin/plugin.json` - Version bump
- `CHANGELOG.md` - Record changes
- `tests/` - New test scenarios for restructured commands

---

## Test Strategy

1. **Chat conversation flow**: Multiple scenarios (no info, partial info, document upload, skill routing)
2. **Assess pipeline**: End-to-end determination -> classification -> pathway context passing
3. **Project pipeline**: End-to-end estimation -> planning with assess data
4. **Brief integration**: Report generation with various data completeness levels
5. **Backward compatibility**: Existing `.aria/` data handling
6. **MCP connector graceful degradation**: All connectors unavailable scenarios

---

## Summary

| Metric | Before | After |
|--------|--------|-------|
| Commands | 8 | 4 |
| Skills | 8 (incl. connectors) | 5 |
| Output files per product | 14 (7 pairs) | 6 (3 reports + 3 summaries) |
| Command-Skill redundancy | High (1:1 mapping) | None (clear separation) |
| Pipeline orchestration | Manual (user chains commands) | Automatic (commands chain skills) |
