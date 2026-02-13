---
name: aria-determination
description: >
  Medical device determination skill for FDA, EU MDR, and MFDS regulations.
  Evaluates whether a product qualifies as a medical device. Use for device
  status evaluation and regulatory scope determination.
allowed-tools: Read Grep Glob
user-invocable: false
metadata:
  version: "0.1.1"
  category: "domain"
  status: "active"
  updated: "2026-02-12"
  modularized: "true"
  tags: "medical-device, determination, FDA, EU-MDR, MFDS, regulatory"
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

## Purpose

Evaluate whether a product qualifies as a medical device under FDA, EU MDR, and MFDS regulations. This is a pure analysis unit that receives device information and returns a structured determination result.

**Input**: Device description, intended use, product form, primary function
**Output**: Determination (YES/NO/CONDITIONAL), traffic light (GREEN/YELLOW/RED), applicable regulations
**Knowledge Base Date**: 2026-01

---

## Decision Framework

### FDA (21 CFR 201(h))

Core question: Is the product intended for diagnosis, treatment, cure, mitigation, or prevention of disease -- without achieving its primary purpose through chemical action or metabolism?

> Detail: See `modules/fda-criteria.md`

### EU MDR (Article 2(1))

Core question: Is the product intended for a specific medical purpose as defined by EU MDR, including diagnosis, treatment, monitoring, or investigation?

> Detail: See `modules/eu-mdr-criteria.md`

### MFDS

Core question: Is the product used for disease diagnosis/treatment/prevention or structure/function examination/replacement/modification, without chemical action as primary effect?

> Detail: See `modules/mfds-criteria.md`

---

## Analysis Workflow

### Step 1: Use Provided Device Information

Use the device information provided as input. Required fields:
- Device description and physical characteristics
- Intended use statement (medical purpose)
- Product form (hardware, software, IVD, combination)
- Primary function and mechanism of action

## Minimum Determination Input Contract

Before issuing deterministic multi-region determination output (YES/NO/CONDITIONAL), the following minimum inputs must be explicit:

1. Intended medical claim (what disease/condition is being diagnosed, treated, monitored, or prevented)
2. Product mechanism and software role (display-only vs analysis/decision logic vs hardware control)
3. Measured parameters and data source (e.g., FEV1/FVC/PEF and how those values are derived)
4. Target patient condition and care context (including target patient condition: critical/serious/non-serious where applicable)
5. Target market scope (FDA / EU MDR / MFDS, or subset)

If any critical input above is missing or contradictory:
- do not output deterministic determination/classification/pathway conclusions
- return an insufficiency rationale
- ask 1-3 minimum follow-up questions that directly resolve missing inputs

### Step 2: Apply Multi-Region Criteria

- Evaluate against FDA, EU MDR, and MFDS definitions
- For each region: determine YES/NO/CONDITIONAL
- Reference `modules/` for detailed criteria when deep analysis needed

### Step 3: Assign Traffic Light & Escalation

- GREEN: All regions agree on device status
- YELLOW: Borderline or conditional -- escalate to expert
- RED: Not a medical device in any region

> Detail: See `modules/escalation-traffic-light.md`

### Step 4: Return Structured Result

Return the determination result containing:
- Multi-region determination (YES/NO/CONDITIONAL per region)
- Applicable regulations per region
- Traffic light assessment
- Escalation flags if borderline

---

## Data Source Strategy

1. **Built-in Knowledge** (Primary): Embedded decision frameworks from FDA, EU MDR, MFDS regulations
2. **Module Files** (On-demand): Detailed criteria in `modules/` loaded when deep analysis needed
3. **MCP Connectors** (Supplementary): Organization-specific regulatory data and verification

For MCP integration patterns (tool discovery, graceful degradation, source attribution), see `CONNECTORS.md`.
