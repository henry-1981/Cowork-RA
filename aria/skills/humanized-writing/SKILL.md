---
name: aria-humanized-writing
description: >
  Internal writing layer for ARIA outputs. Improves readability and actionability
  while preserving regulatory meaning and safety disclaimers.
allowed-tools: Read Grep Glob
user-invocable: false
metadata:
  version: "0.1.0"
  category: "infrastructure"
  status: "active"
  updated: "2026-02-13"
  tags: "writing, readability, actionability, safety"
  knowledge-base-date: "2026-01"

progressive_disclosure:
  enabled: true
  level1_tokens: 120
  level2_tokens: 2500
---

# Humanized Writing Skill (Internal)

## Purpose

Apply readability-focused rewriting to user-visible outputs while keeping regulatory facts unchanged.

## Contract

Inputs:
- raw content
- output type (`user_response_body | summary_md | full_report_md`)
- depth (`express | standard | deep`)
- confidence state (`sufficient | partial | insufficient`)

Outputs:
- humanized content
- applied profile metadata
- validation markers

## Safety Invariants

Do not alter:
- `preserve_regulatory_facts`
- `preserve_numeric_values`
- `preserve_disclaimer_strength`

This skill may improve flow, sentence structure, and glossary clarity only.

## Depth Presets

- `express`: short answer, 1-3 next questions, minimal narrative
- `standard`: balanced clarity + rationale + next action
- `deep`: full explanation for report-grade output

## Insufficient Information Behavior

When confidence is `insufficient`:
1. Keep response concise.
2. Explain why additional information is required.
3. Ask only 1-3 minimum questions to unlock valid assessment.
4. Do not present deterministic classification/pathway decisions.

## Integration Note

This skill is internal-only. Command surface remains `/aria:chat`, `/aria:assess`, `/aria:project`, `/aria:report`.
