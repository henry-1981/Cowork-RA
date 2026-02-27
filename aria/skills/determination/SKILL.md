---
name: aria-determination
description: >
  Medical device determination skill for FDA, EU MDR, and MFDS regulations.
  Evaluates whether a product qualifies as a medical device. Use for device
  status evaluation and regulatory scope determination.
allowed-tools: Read Grep Glob
user-invocable: false
metadata:
  version: "0.3.4"
  category: "domain"
  status: "active"
  updated: "2026-02-25"
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


# Progressive Disclosure Enforcement

이 스킬은 응답 깊이를 단계적으로 제공한다:

## Level 1 — 간결 응답 (기본, 첫 질문)
- 결론 1문장 + 핵심 근거 1-2문장
- MANDATORY OUTPUT FORMAT 사용하지 않음
- Knowledge DB 로드하지 않음 — 내장 Decision Framework만으로 판단
- 예시: "FDA 기준으로 의료기기에 해당합니다 (21 CFR 201(h), 진단 목적). 등급 분류도 확인할까요?"

## Level 2 — 상세 응답 (사용자가 요청할 때)
- 전체 multi-region determination 출력
- MANDATORY OUTPUT FORMAT 포함
- Knowledge DB: 전체 jurisdiction 로드
- CONDITIONAL 시 전체 output contract 포함

## Level 3 — 심층 분석 (명시적 요청 시)
- modules/ 파일 로드 (fda-criteria.md, eu-mdr-criteria.md, mfds-criteria.md)
- 4-Gate 분석 (MFDS 디지털)
- Combination Product Detection
- Annex XVI Detection

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

**MANDATORY OUTPUT FORMAT (Level 2+ only, when digital technology is involved):**
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

**Level 1 (기본):** Knowledge DB 로드하지 않음. 위 Decision Framework (21 CFR 201(h), Article 2(1), 의료기기법 정의)만으로 판단.
**Level 2:** 사용자가 명시한 jurisdiction의 Knowledge DB만 로드. 명시 없으면 가장 관련성 높은 1개.
**Level 3:** 전체 jurisdiction 로드 + modules/ 파일 로드.

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

**MFDS 원문 DB 로드 조건**:
- 키워드: AI, SW, 소프트웨어, software, IoT, 로봇, robot, VR, AR, 가상, HPC, 디지털, digital, SaMD, 앱, app, 알고리즘, 딥러닝, 머신러닝
- 또는: 이전 Gate 2 PASS 결과가 context에 있을 때
- 디지털 기기 → `03-디지털의료제품법/` + 가이드라인, 비디지털 → `01-의료기기법/` 또는 `02-체외진단의료기기법/`

**Knowledge DB 로드 실패 시:**
원문 DB 참조 불가 시: modules/ 인라인 규칙만으로 판단하고, 법적 근거 원문 확인이 필요하다고 안내.

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

**Interactive mode** (conversational context):
- ask 1-3 minimum follow-up questions that directly resolve missing inputs

**Batch/JSON-output mode** (when prompt requests strict JSON output):
- do NOT add extra keys to the JSON (e.g., `insufficient`, `missing_fields` are FORBIDDEN)
- express insufficiency within the allowed schema fields only:
  ```
  "determination": "INSUFFICIENT - [reason: e.g., product falls under EU IVDR not EU MDR]",
  "classification": "INSUFFICIENT - see determination",
  "pathway": "INSUFFICIENT - see determination",
  "evidence_urls": []
  ```
- the output must remain schema-valid (no keys beyond those defined in the prompt's output format)

### Step 2: Apply Multi-Region Criteria

For each target region (FDA, EU MDR, MFDS):

1. **(Level 2+)** Load the region-specific module (`modules/fda-criteria.md`, `modules/eu-mdr-criteria.md`, `modules/mfds-criteria.md`). Level 1에서는 위 Decision Framework만 사용.
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

**MANDATORY OUTPUT FORMAT (Level 2+ only):**
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

**MANDATORY OUTPUT FORMAT (Level 2+ only):**
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

Combination product (drug-device, biologic-device) 감지 시 → CONDITIONAL 판정.

> Detail: See `modules/combination-detection.md`

---

## Annex XVI Detection (Non-Medical Purpose Devices)

Non-medical purpose device (Annex XVI) 감지 시 → SPECIAL/IN SCOPE 판정.

> Detail: See `modules/annex-xvi-detection.md`

---

## Data Source Strategy

1. **Built-in Knowledge** (Primary): Embedded decision frameworks from FDA, EU MDR, MFDS regulations
2. **Module Files** (On-demand): Detailed criteria in `modules/` loaded when deep analysis needed
3. **MCP Connectors** (Supplementary): Organization-specific regulatory data and verification

For MCP integration patterns (tool discovery, graceful degradation, source attribution), see `CONNECTORS.md`.
