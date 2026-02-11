---
name: aria-determination
description: >
  Medical device determination skill for FDA, EU MDR, and MFDS regulations.
  Evaluates whether a product qualifies as a medical device. Use for device
  status evaluation and regulatory scope determination.
allowed-tools: Read Grep Glob
user-invocable: false
metadata:
  version: "1.0.0"
  category: "domain"
  status: "active"
  updated: "2026-02-11"
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
3. **External Tools** (Supplementary): Only when explicitly configured and available
