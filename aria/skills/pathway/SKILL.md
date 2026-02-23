---
name: aria-pathway
description: >
  Regulatory submission pathway analysis and recommendation for FDA, EU MDR, and MFDS.
  Evaluates submission routes based on device classification and provides strategic pathway recommendations with timelines.
allowed-tools: Read Grep Glob
user-invocable: false
metadata:
  version: "0.1.4"
  category: "domain"
  status: "active"
  updated: "2026-02-22"
  modularized: "false"
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

# Regulatory Pathway Analysis Skill

## Purpose

Identify regulatory submission pathways for FDA, EU MDR, and MFDS based on device classification. This is a pure analysis unit that receives classification results and returns pathway recommendations.

**Input**: Device classification results (FDA Class I/II/III, EU Class I/IIa/IIb/III, MFDS Grade 1-4)
**Output**: Pathway recommendations, timeline ranges, key requirements, traffic light indicator
**Knowledge Base Date**: 2026-01

---

## Decision Framework

### FDA Pathways

#### Class I Devices
- **510(k) Exempt**: Devices listed in exempt categories (21 CFR 862-892)
  - Pathway: Registration only
  - Timeline: 1-2 months
  - Requirements: Establishment registration, Device listing
  - Traffic Light: GREEN

- **510(k) Required**: Class I devices not in exempt categories
  - Pathway: 510(k) Premarket Notification
  - Timeline: 3-6 months (standard) or 1-3 months (expedited)
  - Requirements: Substantial equivalence to predicate device
  - Traffic Light: GREEN

#### Class II Devices
- **510(k) Premarket Notification** (most common)
  - Pathway: 510(k) submission with predicate device
  - Timeline: 3-6 months (standard) or 1-3 months (expedited)
  - Requirements: Predicate search, substantial equivalence demonstration, performance testing
  - Traffic Light: GREEN

- **De Novo Classification Request**
  - When: No valid predicate exists AND device is low-moderate risk
  - Key principle: De Novo creates a NEW classification (Class I or II with Special Controls)
  - After De Novo grant: the device becomes a predicate for future 510(k) submissions
  - Timeline: 6-12 months (FDA target: 150 review days)
  - Requirements:
    - Risk-benefit analysis (not SE demonstration)
    - Proposed Special Controls (performance criteria, labeling, post-market)
    - Non-clinical and/or clinical data supporting safety and effectiveness
    - Product Code assignment request
  - Distinguishing from PMA:
    - De Novo: novel but LOW-MODERATE risk, mitigable with Special Controls
    - PMA: novel AND HIGH risk (life-sustaining, implantable vital organ, high mortality)
  - Traffic Light: YELLOW (escalate to expert)
  - NOTE: Specific DEN numbers require FDA database verification. Do NOT fabricate.

#### De Novo vs PMA Decision Framework

**Decision Criteria**:

| Factor | De Novo | PMA |
|--------|---------|-----|
| Risk Level | Low-to-moderate | High |
| Predicate Exists? | No | No (or insufficient predicate) |
| Life-sustaining? | No | Often yes |
| Implantable (vital organ)? | No | Often yes |
| Special Controls sufficient? | Yes — risk mitigable | No — requires full clinical evidence |
| Clinical Data | Non-clinical + limited clinical | Comprehensive clinical trials |
| Review Timeline | 6-12 months (150-day target) | 12-18+ months |
| Post-Grant | Becomes predicate for future 510(k) | PMA supplement for changes |

**Decision Logic**:
- Novel device + LOW-MODERATE risk + Special Controls can mitigate → **De Novo**
- Novel device + HIGH risk + life-sustaining/implantable vital organ → **PMA**
- If uncertain between De Novo and PMA → recommend Pre-Submission (Q-Sub) meeting with FDA

#### Special Controls (De Novo pathway)

When recommending De Novo, MUST specify proposed Special Controls:
- **Performance Testing**: [specific test standards, e.g., ASTM F2129 for corrosion, IEC 62304 for software]
- **Biocompatibility**: [ISO 10993 series if applicable]
- **Clinical Performance**: [endpoint metrics, e.g., sensitivity/specificity for diagnostic SaMD]
- **Labeling Requirements**: [specific warnings, contraindications]
- **Post-Market Surveillance**: [mandatory reporting, registry participation]

**Material-to-Testing Chain** (link device materials to required test standards):

| Material/Component | Primary Test Standard | Test Purpose | Pathway Impact |
|--------------------|-----------------------|--------------|----------------|
| CoCr (Cobalt-Chromium) alloy | ASTM F2129 (corrosion), ASTM F1537 (wrought alloy) | Corrosion resistance, mechanical properties | PMA — implant-grade material requires comprehensive testing |
| PtIr (Platinum-Iridium) alloy | ASTM F2229 (wire), ASTM F2129 (corrosion) | Electrical performance, corrosion resistance | PMA — active implantable electrode material |
| Titanium / Ti alloy | ASTM F136 (wrought), ASTM F2129 (corrosion) | Biocompatibility, fatigue resistance | PMA or 510(k) depending on implant classification |
| Polymers (PEEK, UHMWPE) | ASTM F2026 (PEEK), ASTM F648 (UHMWPE) | Wear resistance, mechanical properties | 510(k) if predicate exists |
| Software / AI algorithm | IEC 62304 (SW lifecycle), IEC 82304-1 (health SW) | Software safety classification | De Novo for novel SaMD without predicate |
| Biological tissue | ISO 22442 (animal tissue), ASTM F2150 (characterization) | Tissue safety, sterility | PMA — biological device typically high risk |

> **Usage**: When a device contains specific materials, cross-reference this table to identify mandatory test standards and anticipate pathway complexity.

#### Class III Devices
- **PMA (Premarket Approval)**
  - Pathway: Full clinical study and PMA submission
  - Timeline: 12-18+ months
  - Requirements: Clinical data, manufacturing quality system, risk analysis
  - Traffic Light: YELLOW (escalate to expert)

- **HDE (Humanitarian Device Exemption)**
  - When: Rare disease (<8,000 patients/year in US)
  - Timeline: 9-15 months
  - Requirements: IRB approval, probable benefit demonstration
  - Traffic Light: YELLOW (escalate to expert)

#### 510(k) Resubmission Process

When a 510(k) receives Additional Information (AI) request or Not Substantially Equivalent (NSE) determination:

**AI Request Response**:
1. Review FDA letter for specific deficiencies
2. Prepare point-by-point response with additional data
3. Resubmit within FDA-specified timeframe (typically 180 days)
4. Timeline impact: adds 3-6 months to original timeline

**After NSE Determination — Options**:

| Option | When to Use | Timeline | Outcome |
|--------|-------------|----------|---------|
| **New 510(k)** with different predicate | Original predicate was wrong; better predicate exists | 3-6 months | New SE determination |
| **New 510(k)** with additional data | Same predicate viable; data gap was the issue | 3-6 months | Strengthened SE argument |
| **De Novo petition** | No suitable predicate exists; device is low-moderate risk | 6-12 months | New classification + becomes predicate |
| **PMA submission** | Device is high risk; De Novo not appropriate | 12-18+ months | Full approval pathway |
| **Pre-Submission (Q-Sub)** meeting | Unclear path forward; need FDA feedback | 2-3 months for meeting | Clarified strategy before resubmission |

> **Key Rule**: NSE does NOT mean the device cannot be marketed — it means the chosen regulatory strategy needs revision. Always evaluate all options before selecting the resubmission path.

#### Clinical Endpoint Standards (PMA and High-Risk Devices)

When recommending PMA or clinical trial-dependent pathways, specify applicable clinical endpoint standards:

**Cardiovascular Devices**:
- **MACE** (Major Adverse Cardiac Events): composite of cardiac death, MI, TVR — primary safety endpoint
- **TLF** (Target Lesion Failure): composite of cardiac death, target vessel MI, ischemia-driven TLR — per ARC-2 definitions
- **VLST** (Very Late Stent Thrombosis): definite/probable stent thrombosis >1 year — per ARC definitions
- Follow-up: minimum 12 months; 24-60 months for long-term safety

**Diagnostic SaMD (AI/ML)**:
- **Sensitivity/Specificity**: primary performance endpoints with confidence intervals
- **AUC-ROC**: discriminative ability — per FDA guidance on Clinical Performance Assessment
- **PPV/NPV**: clinical utility in target prevalence population

**Orthopedic Implants**:
- **Revision rate**: primary endpoint — Kaplan-Meier survivorship analysis
- **Patient-reported outcomes**: validated instruments (e.g., WOMAC, Harris Hip Score, Knee Society Score)
- Follow-up: minimum 24 months; 5-10 years for joint replacement

**Neurological Devices**:
- **Responder rate**: percentage achieving clinically meaningful improvement
- **Adverse event rate**: device-related serious adverse events
- **Functional outcome**: validated scales (e.g., mRS, NIHSS, Barthel Index)

> **Usage**: When a device falls into one of these categories, include the relevant clinical endpoints in the pathway recommendation to set expectations for clinical study design.

---

### EU MDR Pathways

#### Class I Devices
- **Self-Declaration (Annex IV)**
  - When: Non-sterile, non-measuring function
  - Pathway: Technical documentation + DoC
  - Timeline: 2-4 months
  - Requirements: Technical file, risk management, clinical evaluation
  - Notified Body: Not required
  - Traffic Light: GREEN

- **Notified Body Certification (Annex IV for sterile/measuring)**
  - When: Sterile or with measuring function
  - Pathway: Technical documentation + Notified Body review
  - Timeline: 4-6 months
  - Requirements: Technical file, sterility validation (if sterile)
  - Traffic Light: GREEN

#### Class IIa Devices
- **Notified Body Certification (Annex IX or X)**
  - Pathway: Notified Body QMS certification (Annex IX) or Type Examination (Annex X)
  - Timeline: 6-12 months
  - Requirements: Technical documentation, Clinical Evaluation Report, Post-Market Surveillance Plan
  - Notified Body: Mandatory involvement required
  - Traffic Light: YELLOW (moderate complexity)

> **CRITICAL OUTPUT RULE**: When describing EU MDR pathways, ALWAYS write out "Notified Body" in full (not abbreviate as "NB") to ensure regulatory terminology precision.

#### Class IIb Devices
- **Notified Body Certification (Annex IX or X)**
  - Pathway: Full QMS certification (Annex IX) or Type Examination + Product QMS (Annex X)
  - Timeline: 8-14 months
  - Requirements: Technical documentation, Clinical Evaluation Report, PMCF plan
  - Traffic Light: YELLOW (moderate-high complexity)

#### Class III Devices
- **Notified Body Full QMS Certification (Annex IX)**
  - Pathway: Full QMS review + clinical investigation
  - Timeline: 12-18+ months
  - Requirements: Clinical investigation data, comprehensive technical documentation
  - Traffic Light: YELLOW (escalate to expert)

---

### MFDS Pathways

#### MFDS Grade→Pathway Mapping

> **Knowledge DB 참조**: 상세 인허가 경로는 `../../knowledge/regulations/mfds-framework.md` Section 3 참조

**GROUND TRUTH (절대 변경 불가):**
1. 1등급 → 신고
2. 2등급 → 인증
3. 3등급 → 허가
4. 4등급 → 허가

#### Grade 1 Detail
- **Pathway**: 신고 (Notification) — 제조/수입 신고
- Requirements: Product specifications, labeling, manufacturing documentation
- Clinical Data: Not required
- MFDS Technical Review: Not required

#### Grade 2 Detail
- **Pathway**: 인증 (Certification/TPR) — 지정된 인증기관 심사
- Requirements: Non-clinical test data, risk analysis, labeling, 기술문서
- Clinical Data: Non-clinical testing sufficient for most devices
- MFDS Direct Review: Not required (인증기관이 심사)

#### Grade 3 Detail
- **Pathway**: 허가 (Approval) — MFDS 직접 심사
- Requirements: Clinical or comprehensive non-clinical data, risk management
- Clinical Data: Required for most Grade 3 devices

#### Grade 4 Detail
- **Pathway**: 허가 (Approval) — MFDS 직접 심사 + 임상시험
- Requirements: IRB-approved clinical trial, comprehensive clinical data
- Clinical Data: Mandatory clinical trial

---

## Analysis Workflow

### Step 0 (pre-analysis)
Read("references/evidence-catalog.md") to load pathway-specific evidence and precedent mappings.

### Step 1: Receive Classification Data

Accept classification results as input:
- FDA Class (I/II/III)
- EU MDR Class (I/IIa/IIb/III)
- MFDS Grade (1/2/3/4)
- Target regions

If classification data is not provided, return an error indicating classification is required first.

### Step 2: Select Pathways per Region

**FDA Pathway Selection Logic**:
- Class I + Exempt -> Registration only (GREEN, 1-2 months)
- Class I + Non-exempt -> 510(k) (GREEN, 3-6 months)
- Class II + Valid predicate -> 510(k) (GREEN, 3-6 months)
- Class II + No predicate -> De Novo (YELLOW, 6-12 months)
- Class III -> PMA (YELLOW, 12-18+ months)

**EU MDR Pathway Selection Logic**:
- Class I (non-sterile, non-measuring) -> Self-declaration (GREEN, 2-4 months)
- Class I (sterile or measuring) -> Notified Body Annex IV (GREEN, 4-6 months)
- Class IIa -> Notified Body Annex IX/X (YELLOW, 6-12 months)
- Class IIb -> Notified Body Annex IX/X (YELLOW, 8-14 months)
- Class III -> Notified Body Annex IX + Clinical Investigation (YELLOW, 12-18+ months)

**MFDS Pathway Selection Logic** (HARDCODED):
- Grade 1 -> 신고/Notification (GREEN, 1-3 months) — 「의료기기법」 제12조
- Grade 2 -> 인증/Certification (GREEN-YELLOW, 3-9 months) — 「의료기기법」 제9조
- Grade 3 -> 허가/Approval (YELLOW, 9-15 months) — 「의료기기법」 제6조
- Grade 4 -> 허가/Approval + Clinical Trial (YELLOW, 12-18+ months) — 「의료기기법」 제6조

### Step 3: Multi-Region Comparison

When multiple target regions selected:
- Generate comparison table: Region | Pathway | Timeline | Key Requirements
- Identify critical path (longest timeline)
- Highlight common dependencies (e.g., shared testing data)
- Recommend parallel vs. sequential submission strategy

### Step 4: Assign Overall Traffic Light

- **GREEN**: All pathways are low-risk (Class I/IIa, Grade 1-2, no clinical trials)
- **YELLOW**: Any pathway requires Notified Body, clinical data, or De Novo/PMA

### Step 5: Return Structured Result

Return the pathway analysis containing:
- Selected pathway per region with rationale
- Timeline ranges (optimistic/expected/pessimistic)
- Key requirements per pathway
- Multi-region comparison (if applicable)
- Critical path identification
- Traffic light assessment

#### Evidence Requirements (per pathway)

Each pathway recommendation MUST include specific regulatory citations:

- **FDA**: Submission type reference (e.g., 21 CFR 807 Subpart E for 510(k)), relevant guidance document(s), DEN/510(k)/PMA precedent (if known)
  - **CRITICAL**: Do NOT fabricate DEN/510(k)/PMA numbers. These are FDA-assigned identifiers.
  - If a specific precedent is recalled, prefix with "Believed to be" + recommend verification
  - If unknown: "Specific precedent number requires FDA database verification"
- **EU MDR**: Annex reference (IV, IX, X), applicable MDCG guidance (e.g., MDCG 2020-5 for clinical evaluation)
- **MFDS**: 의료기기법 조항 (제6조 허가/제9조 인증/제12조 신고), 인증기관 요건 (if applicable)

**MANDATORY OUTPUT FORMAT (must appear in response):**
```
### Regulatory Evidence
- **FDA**: [Submission type] — 21 CFR [section] (e.g., 21 CFR 807 Subpart E for 510(k)) — Guidance: [document name] — Precedent: [DEN/K/P number or "requires FDA database verification"]
- **EU MDR**: Annex [reference] (e.g., Annex IX) — MDCG: [guidance ref] (e.g., MDCG 2020-5)
- **MFDS**: 「의료기기법」 [조항] (e.g., 제9조 인증) — [추가 요건 if applicable]
- **Citations**:
  - [FDA] 21 CFR § [section], [guidance document]
  - [EU MDR] Annex [ref], MDCG [number]
  - [MFDS] [법률/조항 reference]
```

**MANDATORY OUTPUT FORMAT (must appear in response):**
```
### Confidence & Escalation
- **Confidence Score**: [0-100]% — [basis: e.g., "clear predicate exists, standard 510(k) pathway"]
- **Escalation Level**: [1-4]
  - 1 = Automated processing sufficient
  - 2 = Brief expert review recommended
  - 3 = Expert review required (De Novo/PMA or multi-region conflict)
  - 4 = Regulatory authority consultation required
- **Next Action**: [recommended next step]
```

---

## Traffic Light Definitions

- **GREEN**: Low-risk pathways (Class I/IIa, Grade 1-2, no clinical trials, no Notified Body for complex reviews)
- **YELLOW**: Moderate-high risk (Class IIb/III, Grade 3-4, De Novo, PMA, clinical trials required, Notified Body for Class IIb/III)
- **RED**: Not used in pathway skill (all valid classifications have a pathway)

---

## Escalation Scenarios

Escalate to regulatory expert when:
- FDA Class III device (PMA pathway)
- EU MDR Class III device (clinical investigation required)
- MFDS Grade 4 device (clinical trial required)
- De Novo pathway (no predicate device)
- Multi-region submission with conflicting timelines

---

## Data Source Strategy

1. **Built-in Knowledge** (Primary): Embedded pathway frameworks from FDA, EU MDR, MFDS regulations
2. **Classification Data** (Input): Classification results from determination/classification skills
3. **MCP Connectors** (Supplementary): Organization-specific pathway precedents and timeline data

For MCP integration patterns (tool discovery, graceful degradation, source attribution), see `CONNECTORS.md`.
