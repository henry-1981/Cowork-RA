---
name: aria-determination
description: >
  Medical device determination skill for FDA, EU MDR, and MFDS regulations.
  Evaluates whether a product qualifies as a medical device. Use for device
  status evaluation and regulatory scope determination.
allowed-tools: Read Grep Glob ToolSearch
user-invocable: false
metadata:
  version: "0.0.2"
  category: "domain"
  status: "active"
  updated: "2026-02-11"
  modularized: "true"
  tags: "medical-device, determination, FDA, EU-MDR, MFDS, regulatory, notion-mcp"
  knowledge-base-date: "2026-01"

# MoAI Extension: Progressive Disclosure
progressive_disclosure:
  enabled: true
  level1_tokens: 100
  level2_tokens: 3000

# MoAI Extension: Triggers
triggers:
  keywords: ["determination", "medical device", "device status", "regulatory scope"]
  phases: ["run"]
---

# Medical Device Determination Skill

## Quick Reference

**Purpose**: Evaluate whether a product qualifies as a medical device under FDA, EU MDR, and MFDS regulations.

**Input**: Device description, intended use, product form, primary function
**Output**: Determination (YES/NO/CONDITIONAL), traffic light (GREEN/YELLOW/RED), applicable regulations
**Knowledge Base Date**: 2026-01

---

## Decision Framework

### FDA (21 CFR 201(h))

Core question: Is the product intended for diagnosis, treatment, cure, mitigation, or prevention of disease — without achieving its primary purpose through chemical action or metabolism?

> Detail: See `modules/fda-criteria.md`

### EU MDR (Article 2(1))

Core question: Is the product intended for a specific medical purpose as defined by EU MDR, including diagnosis, treatment, monitoring, or investigation?

> Detail: See `modules/eu-mdr-criteria.md`

### MFDS

Core question: Is the product used for disease diagnosis/treatment/prevention or structure/function examination/replacement/modification, without chemical action as primary effect?

> Detail: See `modules/mfds-criteria.md`

---

## Workflow

### Step 1: Use Provided Device Information

Use the device information already collected by the command. Do NOT re-ask or re-display previously collected answers.

Required fields (already provided):
- Device description and physical characteristics
- Intended use statement (medical purpose)
- Product form (hardware, software, IVD, combination)
- Primary function and mechanism of action

### Step 2: Apply Multi-Region Criteria

- Evaluate against FDA, EU MDR, and MFDS definitions
- For each region: determine YES/NO/CONDITIONAL
- Reference `modules/` for detailed criteria when deep analysis needed

### Step 3: Assign Traffic Light & Escalation

- GREEN: All regions agree on device status
- YELLOW: Borderline or conditional — escalate to expert
- RED: Not a medical device in any region

> Detail: See `modules/escalation-traffic-light.md`

### Step 4: Generate Result

- Consolidate multi-region determination
- Identify applicable regulations
- Flag escalation scenarios if borderline
- Output the determination result ONLY — do NOT repeat the original question or user input
- After output, STOP. Do not loop back to Step 1

---

## Data Source Strategy

1. **Built-in Knowledge** (Primary): Embedded decision frameworks from FDA, EU MDR, MFDS regulations
2. **Module Files** (On-demand): Detailed criteria in `modules/` loaded when deep analysis needed
3. **Notion MCP** (Supplementary): Organization-specific regulatory data from Notion database
4. **Context7 MCP** (Verification): External regulatory document verification and supplementation

### Notion MCP Integration

**Purpose**: Retrieve organization-specific regulatory data to supplement built-in knowledge.

**Workflow**:
1. Use ToolSearch to load Notion MCP tools (mcp__notion__*)
2. If Notion tools available:
   - Query organization database for region-specific determination criteria
   - Cross-reference with built-in knowledge
   - Attribute sources in output
3. If Notion tools unavailable or query fails:
   - Gracefully degrade to built-in knowledge
   - Continue without interruption
   - No error shown to user

**Data Attribution**:
- Always include "Sources:" section in output
- Format: "Built-in Knowledge (FDA/EU MDR/MFDS regulations)" + "Notion DB (organization-specific data)" if used

**Graceful Degradation**:
- Notion MCP is supplementary, not required
- If unavailable: Use built-in knowledge without notification
- If query fails: Log internally, proceed with built-in data

### Context7 MCP Integration

**Purpose**: Verify and supplement regulatory document references (FDA 21 CFR 201(h), EU MDR Article 2(1), MFDS 의료기기법).

**Workflow**:
1. Use ToolSearch to load Context7 MCP tools: `ToolSearch("context7")`
2. Expected tools: `mcp__context7__resolve-library-id`, `mcp__context7__get-library-docs`
3. If Context7 tools available:
   - Resolve regulatory library IDs for FDA/EU MDR/MFDS regulations
   - Retrieve latest regulatory document versions
   - Cross-reference determination criteria with latest regulations
   - Verify regulatory citations are current
   - Attribute Context7 as supplementary source in output
4. If Context7 unavailable or query fails:
   - Gracefully degrade to built-in knowledge
   - Continue without interruption
   - Include "(Context7 unavailable)" in Sources section

**Data Priority**:
- Notion DB (Priority 1): Organization-specific precedents
- Built-in Knowledge (Priority 2): Embedded regulatory frameworks
- Context7 (Priority 3): External regulatory document verification

**Source Attribution**:
- When Context7 used: "Sources: Built-in Knowledge + Context7 (regulatory verification)"
- When Context7 unavailable: "Sources: Built-in Knowledge (Context7 unavailable)"

**Graceful Degradation**:
- Context7 is supplementary, not required
- If unavailable: Use built-in knowledge without error message
- If query fails: Log internally, proceed with built-in data
