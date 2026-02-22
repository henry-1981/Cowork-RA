---
name: aria-determination
description: >
  Medical device determination skill for FDA, EU MDR, and MFDS regulations.
  Evaluates whether a product qualifies as a medical device. Use for device
  status evaluation and regulatory scope determination.
allowed-tools: Read Grep Glob
user-invocable: false
metadata:
  version: "0.1.5"
  category: "domain"
  status: "active"
  updated: "2026-02-22"
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

### CONDITIONAL Output Contract

When determination is **CONDITIONAL** for any jurisdiction, the following fields are MANDATORY:

| Field | Description | Example |
|-------|-------------|---------|
| **Uncertainty Basis** | Specific regulatory boundary being straddled | "FDA General Wellness Policy boundary: respiratory monitoring features may exceed wellness scope" |
| **Resolution Conditions** | What information or decision would resolve to YES or NO | "Intended use claims limited to wellness → NO; Any diagnostic/screening claim → YES" |
| **If YES Scenario** | Classification and pathway assuming device status | "Class II, De Novo/510(k)" |
| **If NO Scenario** | Regulatory status assuming non-device | "Not subject to FDA regulation as medical device" |

**CONDITIONAL triggers** (non-exhaustive):
1. Wellness/medical device boundary (FDA General Wellness Policy, MFDS 건강지원제품)
2. Borderline products (EU MDR MDCG 2019-11)
3. Combination products (drug-device, biologic-device) — see Combination Product Detection below
4. Software boundary (CDS exemption, general purpose computing)
5. Intended use ambiguity (claims could be interpreted either way)

**CRITICAL**: Do NOT collapse CONDITIONAL to YES or NO. If uncertainty exists, output CONDITIONAL with all mandatory fields. Each jurisdiction is evaluated independently — one jurisdiction may be YES while another is CONDITIONAL.

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

#### MFDS 4-Gate Analysis (Mandatory for Digital Products)

When the product involves digital technology (SW, AI, IoT, VR/AR, intelligent robot, HPC), the 4-Gate analysis from `modules/mfds-criteria.md` Section "4-Gate Decision Logic" MUST be executed during determination and its result shown in the output.

Execute each gate and output the result explicitly:
1. Gate 1: 의료기기 해당 여부 (Step 1 결과 반영)
2. Gate 2: 디지털 기술 적용 여부 (SW, AI, IoT, VR/AR 등)
3. Gate 3: 핵심 기능 영향 여부
4. Gate 4: 배제 원칙 확인

**MANDATORY OUTPUT FORMAT (must appear in response when digital technology is involved):**
```
### MFDS 4-Gate Analysis
- Gate 1 (의료기기 해당): [PASS/FAIL] — [근거]
- Gate 2 (디지털 기술): [PASS/EXIT] — [기술 유형 또는 "비디지털 기기"]
- Gate 3 (핵심 기능 영향): [PASS/FAIL] — [영향 분석] (Gate 2 EXIT 시 N/A)
- Gate 4 (배제 원칙): [PASS/EXIT] — [배제 해당 여부] (Gate 2 EXIT 시 N/A)
- **Result**: [디지털의료기기 해당 / Gate 2 EXIT (비디지털) / 비해당]
```

- **4-Gate 통과 (디지털의료기기)**: Include in determination output, classification will use for risk grading
- **Gate 2 EXIT (비디지털)**: State explicitly — device is medical device but not digital medical device
- **Gate 1 FAIL**: Device is not a medical device → determination NO

---

## Analysis Workflow

### Step 0 (pre-analysis)
Read("references/evidence-catalog.md") to load jurisdiction-specific evidence keywords.

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

For each target region (FDA, EU MDR, MFDS):

1. Load the region-specific module (`modules/fda-criteria.md`, `modules/eu-mdr-criteria.md`, `modules/mfds-criteria.md`)
2. Execute the module's decision tree
3. At each decision point, evaluate whether the answer is clear (YES/NO) or uncertain (CONDITIONAL)
4. **CONDITIONAL gate**: If any of the following are true, the determination MUST be CONDITIONAL:
   - The product straddles a wellness/medical boundary
   - The intended use could be interpreted as either medical or non-medical
   - The product is a combination product (drug-device, biologic-device)
   - Regulatory guidance explicitly identifies the product type as borderline
   - The product fits a new regulatory category (e.g., MFDS 건강지원제품) that is distinct from both "device" and "non-device"
5. When CONDITIONAL: populate all CONDITIONAL output contract fields (see above)

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

#### Evidence Requirements (per jurisdiction)

Each determination MUST include specific regulatory citations:

- **FDA**: 21 CFR section (e.g., 21 CFR 201(h)), relevant guidance document(s) (e.g., FDA General Wellness Policy), predicate device (if applicable)
- **EU MDR**: Article reference (e.g., Article 2(1)), applicable MDCG guidance (e.g., MDCG 2019-11 for borderline products)
- **MFDS**: 의료기기법 조항 (e.g., 제2조 정의), 품목코드 (Axxxxx.xx if known), 관련 고시/가이드라인 (e.g., 디지털의료제품법 제3조)

**CRITICAL**: Do NOT fabricate regulatory citations. If a specific citation is uncertain, state "requires regulatory database verification."

**MANDATORY OUTPUT FORMAT (must appear in response):**
```
### Regulatory Evidence
- **FDA Legal Basis**: 21 CFR [section] (e.g., 21 CFR 201(h)) — Guidance: [document name if applicable]
- **EU MDR Legal Basis**: [Article reference] (e.g., Article 2(1)) — MDCG: [guidance number if applicable]
- **MFDS Legal Basis**: [법률 조항] (e.g., 「의료기기법」 제2조) — 고시/가이드라인: [명칭 if applicable]
- **Citations**:
  - [FDA] 21 CFR § [specific section]
  - [EU MDR] Article/Annex [reference]
  - [MFDS] [법률/고시 reference]
```

**MANDATORY OUTPUT FORMAT (must appear in response):**
```
### Confidence & Escalation
- **Confidence Score**: [0-100]% — [basis: e.g., "clear medical purpose, well-established device category"]
- **Escalation Level**: [1-4]
  - 1 = Automated processing sufficient
  - 2 = Brief expert review recommended
  - 3 = Expert review required (borderline/CONDITIONAL)
  - 4 = Regulatory authority consultation required
- **Next Action**: [recommended next step]
```

---

## Combination Product Detection (P5)

### Trigger Conditions

When ANY of the following are detected in the product description:
- Drug-device combination (drug coating, drug-eluting, drug reservoir)
- Biologic-device combination (tissue-derived component, cell therapy + device)
- Device constituent + drug constituent identified separately

### Mandatory Output

Determination MUST be **CONDITIONAL** with additional required fields:

| Field | Description |
|-------|-------------|
| **Combination Type** | Drug-device / Biologic-device / Drug-biologic-device |
| **Device Constituent** | Physical/mechanical component description and function |
| **Drug/Biologic Constituent** | Pharmacological/biological component and its action |
| **PMOA (Primary Mode of Action)** | Which constituent provides the primary therapeutic effect |
| **Lead Center** | CDRH (device PMOA) / CDER (drug PMOA) / CBER (biologic PMOA) |
| **Consultation** | Which other center(s) must be consulted |

### PMOA Determination Logic

```
Device PMOA indicators:
  - Mechanical/physical action is primary therapeutic effect
  - Drug/biologic action is ancillary (prevents side effects, enhances device function)
  → Lead: CDRH, Consult: CDER or CBER

Drug PMOA indicators:
  - Pharmacological action is primary therapeutic effect
  - Device is delivery mechanism
  → Lead: CDER, Consult: CDRH

Biologic PMOA indicators:
  - Biological action is primary therapeutic effect
  → Lead: CBER, Consult: CDRH
```

---

## Annex XVI Detection (Non-Medical Purpose Devices)

### Trigger Conditions

When ANY of the following are detected in the product description:
- Device without intended medical purpose (cosmetic, aesthetic, wellness with no medical claim)
- Product listed in Annex XVI categories: contact lenses (non-corrective), laser equipment (skin treatment), dermal fillers, liposuction/lipoplasty/lipectomy equipment, intense pulsed light equipment, brain stimulation equipment

### Mandatory Output

When Annex XVI device detected, EU MDR determination MUST include:

```
### EU MDR Determination — Annex XVI (Non-Medical Purpose)
- **Determination**: SPECIAL — IN SCOPE via Annex XVI (not a medical device per Article 2(1), but regulated under MDR)
- **MDR Article 2(1) Medical Device?**: NO — [reason: no intended medical purpose]
- **MDR Annex XVI Listed?**: YES — [specific Annex XVI category]
- **Result**: IN SCOPE (SPECIAL) — Device falls under MDR scope via Annex XVI, not Article 2(1)
- **Common Specifications**: Implementing Regulation (EU) 2022/2346 (IR 2022/2346)
- **MDCG Guidance**: MDCG 2023-5 (Annex XVI application guidance)
- **Classification**: Apply MDR Annex VIII rules as if medical device → [resulting Class]
- **Conformity Assessment**: Notified Body involvement mandatory per Article 52
```

### Key Principle

Annex XVI devices require **dual determination**:
1. Article 2(1) assessment → typically NO (no medical purpose)
2. Annex XVI assessment → YES (listed non-medical purpose device)
3. Result: Device IS within MDR scope despite not being a "medical device" per Article 2(1) → use **SPECIAL** or **IN SCOPE** determination status (NOT "YES")

---

## Data Source Strategy

1. **Built-in Knowledge** (Primary): Embedded decision frameworks from FDA, EU MDR, MFDS regulations
2. **Module Files** (On-demand): Detailed criteria in `modules/` loaded when deep analysis needed
3. **MCP Connectors** (Supplementary): Organization-specific regulatory data and verification

For MCP integration patterns (tool discovery, graceful degradation, source attribution), see `CONNECTORS.md`.
