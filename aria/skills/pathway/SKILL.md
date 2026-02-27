---
name: aria-pathway
description: >
  Regulatory submission pathway analysis and recommendation for FDA, EU MDR, and MFDS.
  Evaluates submission routes based on device classification and provides strategic pathway recommendations with timelines.
allowed-tools: Read Grep Glob
user-invocable: false
metadata:
  version: "0.3.2"
  category: "domain"
  status: "active"
  updated: "2026-02-25"
  modularized: "true"
  tags: "pathway, regulatory, FDA, EU-MDR, MFDS, submission, 510(k), PMA, CE-mark"
  knowledge-base-date: "2026-01"

# MoAI Extension: Progressive Disclosure
progressive_disclosure:
  enabled: true
  level1_tokens: 100
  level2_tokens: 2500

# MoAI Extension: Triggers
triggers:
  keywords: ["pathway", "submission route", "regulatory pathway", "510(k)", "PMA", "CE mark"]
  phases: ["run"]
---


# Progressive Disclosure Enforcement

## Level 1 — 간결 응답 (기본)
- 경로 결론 1-2문장 + 예상 기간
- Knowledge DB 로드하지 않음 — 내장 Decision Framework만 사용
- 예시: "510(k) 경로로 약 6-9개월 예상됩니다. 상세 일정/비용 분석이 필요하신가요?"

## Level 2 — 상세 응답 (사용자 요청 시)
- 전체 pathway 비교 (FDA vs EU vs MFDS)
- 타임라인, 비용 견적 포함
- MANDATORY OUTPUT FORMAT 사용
- Knowledge DB + modules/ 로드

# Regulatory Pathway Analysis Skill

## Purpose

Identify regulatory submission pathways for FDA, EU MDR, and MFDS based on device classification.

**Input**: Device classification results (FDA Class I/II/III, EU Class I/IIa/IIb/III, MFDS Grade 1-4)
**Output**: Pathway recommendations, timeline ranges, key requirements, traffic light indicator
**Knowledge Base Date**: 2026-01

---

## Decision Framework

### FDA Pathways

| Classification | Pathway | Timeline | Traffic Light |
|---------------|---------|----------|---------------|
| Class I Exempt | Registration only | 1-2 months | GREEN |
| Class I Non-exempt | 510(k) | 3-6 months | GREEN |
| Class II + predicate | 510(k) | 3-6 months | GREEN |
| Class II no predicate | De Novo | 6-12 months | YELLOW |
| Class III | PMA | 12-18+ months | YELLOW |
| Rare disease (<8K/yr) | HDE | 9-15 months | YELLOW |

> Detail: See `modules/fda-pathways.md` for De Novo vs PMA framework, Special Controls, Material-to-Testing Chain, Clinical Endpoints, 510(k) Resubmission

### EU MDR Pathways

| Classification | Pathway | Timeline | Notified Body |
|---------------|---------|----------|---------------|
| Class I (non-sterile) | Self-declaration (Annex IV) | 2-4 months | Not required |
| Class I (sterile/measuring) | Notified Body Annex IV | 4-6 months | Required |
| Class IIa | Notified Body Annex IX/X | 6-12 months | Required |
| Class IIb | Notified Body Annex IX/X | 8-14 months | Required |
| Class III | Notified Body Annex IX + Clinical | 12-18+ months | Required |

> **CRITICAL**: Always write "Notified Body" in full, never "NB"

### MFDS Pathways (HARDCODED)

| Grade | Pathway | Timeline | Legal Basis |
|-------|---------|----------|-------------|
| 1등급 | 신고 (Notification) | 1-3 months | 의료기기법 제12조 |
| 2등급 | 인증 (Certification) | 3-9 months | 의료기기법 제9조 |
| 3등급 | 허가 (Approval) | 9-15 months | 의료기기법 제6조 |
| 4등급 | 허가 + 임상 (Approval+Clinical) | 12-18+ months | 의료기기법 제6조 |

> **Knowledge DB 참조**: 상세 인허가 경로는 `../../knowledge/mfds/01-법령/01-의료기기법/` (의료기기법 제6조, 제9조, 제12조) 참조

---

## Analysis Workflow

### Step 0 (pre-analysis)

**Level 1 (기본):** Knowledge DB 로드하지 않음. 위 Decision Framework 테이블만으로 판단.
**Level 2:** Knowledge DB + modules/ 로드.

Knowledge DB references (Level 2+):
- FDA: `../../knowledge/regulations/fda-framework.md`
- EU MDR: `../../knowledge/eu/01-regulation/mdr-2017-745/`
- EU IVDR: `../../knowledge/eu/01-regulation/ivdr-2017-746/`
- EU MDCG: `../../knowledge/eu/02-mdcg/`
- EU MEDDEV: `../../knowledge/eu/03-meddev/`
- MFDS 의료기기법: `../../knowledge/mfds/01-법령/01-의료기기법/`
- MFDS 체외진단법: `../../knowledge/mfds/01-법령/02-체외진단의료기기법/`
- MFDS 디지털의료제품법: `../../knowledge/mfds/01-법령/03-디지털의료제품법/`
- MFDS 가이드라인: `../../knowledge/mfds/02-가이드라인/`

### Step 1: Receive Classification Data

Accept classification results. If not provided, return error indicating classification required first.

### Step 2: Select Pathways per Region

Use Decision Framework tables above. For De Novo/PMA decisions, load `modules/fda-pathways.md`.

### Step 3: Multi-Region Comparison

When multiple target regions:
- Generate comparison table: Region | Pathway | Timeline | Key Requirements
- Identify critical path (longest timeline)
- Recommend parallel vs. sequential submission strategy

### Step 4: Assign Overall Traffic Light

- **GREEN**: All pathways low-risk (Class I/IIa, Grade 1-2)
- **YELLOW**: Any pathway requires Notified Body, clinical data, or De Novo/PMA

### Step 5: Return Structured Result

Return pathway analysis with:
- Selected pathway per region with rationale
- Timeline ranges (optimistic/expected/pessimistic)
- Key requirements per pathway
- Multi-region comparison (if applicable)

#### Evidence Requirements

Each pathway MUST include regulatory citations:
- **FDA**: Submission type, 21 CFR reference, guidance document
- **EU MDR**: Annex reference, MDCG guidance
- **MFDS**: 의료기기법 조항

**CRITICAL**: Do NOT fabricate DEN/510(k)/PMA numbers.

**MANDATORY OUTPUT FORMAT (Level 2+ only):**
```
### Regulatory Evidence
- **FDA**: [Submission type] — 21 CFR [section] — Guidance: [document] — Precedent: [number or "requires verification"]
- **EU MDR**: Annex [ref] — MDCG: [guidance ref]
- **MFDS**: 「의료기기법」 [조항]
```

**MANDATORY OUTPUT FORMAT (Level 2+ only):**
```
### Confidence & Escalation
- **Confidence Score**: [0-100]% — [basis]
- **Escalation Level**: [1-4] (1=automated, 2=brief review, 3=expert required, 4=authority consultation)
- **Next Action**: [recommended next step]
```

---

## Escalation Scenarios

Escalate to regulatory expert when:
- FDA Class III (PMA) or EU MDR Class III
- MFDS Grade 4 (clinical trial required)
- De Novo pathway (no predicate)
- Multi-region conflicting timelines

---

## Data Source Strategy

1. **Built-in Knowledge** (Primary): Embedded pathway frameworks
2. **Module Files** (On-demand): Detailed pathway info in `modules/` for Level 2+
3. **MCP Connectors** (Supplementary): Organization-specific precedents

For MCP integration patterns, see `CONNECTORS.md`.
