---
name: aria-classification
description: >
  Multi-region device classification skill for FDA, EU MDR, and MFDS.
  Determines regulatory class (FDA I/II/III, EU I/IIa/IIb/III, MFDS 1/2/3/4)
  based on device characteristics. Use for regulatory class determination.
allowed-tools: Read Grep Glob
user-invocable: false
metadata:
  version: "0.3.2"
  category: "domain"
  status: "active"
  updated: "2026-02-25"
  modularized: "true"
  tags: "medical-device, classification, FDA, EU-MDR, MFDS, regulatory"
  knowledge-base-date: "2026-01"

# MoAI Extension: Progressive Disclosure
progressive_disclosure:
  enabled: true
  level1_tokens: 100
  level2_tokens: 3000

# MoAI Extension: Triggers
triggers:
  keywords: ["classification", "device class", "risk level", "FDA class", "EU MDR class", "MFDS grade"]
  phases: ["run"]
---


# Progressive Disclosure Enforcement

## Level 1 — 간결 응답 (기본)
- 등급 결론 1-2문장 + 핵심 규칙 근거
- Risk Matrix, 4-Gate 등 MANDATORY 포맷 생략
- Knowledge DB 로드하지 않음 — 내장 Decision Framework만 사용
- 예시: "FDA Class II (510(k) 대상), MFDS 2등급입니다. 상세 분류 근거가 필요하신가요?"

## Level 2 — 상세 응답 (사용자 요청 시)
- MANDATORY OUTPUT FORMAT 포함
- Risk Matrix Grid, 4-Gate Analysis 포함
- 전체 jurisdiction 비교 테이블
- Knowledge DB + modules/ 로드

# Medical Device Classification Skill

## Purpose

Determine regulatory class across FDA, EU MDR, and MFDS jurisdictions. This is a pure analysis unit that receives device characteristics and returns a structured classification result.

**Input**: Device characteristics (invasiveness, duration, active/passive, body system, anatomical location)
**Output**: Multi-region classification matrix, rationale, traffic light per region
**Knowledge Base Date**: 2026-01

**Multi-Region Classification Matrix**:
| Region | Classes | Risk Levels |
|--------|---------|-------------|
| FDA | I, II, III | Low, Moderate, High |
| EU MDR | I, IIa, IIb, III | Low, Medium-Low, Medium-High, High |
| MFDS | 1, 2, 3, 4 | Low, Low-Medium, Medium-High, High |

**Key Classification Factors**:
- Invasiveness (non-invasive, invasive, implantable)
- Duration of contact (transient, short-term, long-term)
- Active vs passive device
- Intended use and body system interaction
- Anatomical location

---

## ⚠️ MFDS AI SaMD Classification Override (반드시 분석 전 확인)

> 아래 규칙은 MFDS 관할 AI SaMD 등급 분류 시 **최우선 적용**됩니다. 실제 허가 이력이나 pre-training 지식보다 아래 규칙이 우선합니다.

### Override 1. AI 진단 보조 SW → 반드시 3등급

AI가 의료 영상(CT/MRI/X-ray)을 분석하여 **질병 확률 점수 또는 진단 분류**를 출력하는 소프트웨어는:
- Medical Impact (위해도) = **Treatment/Diagnosis** (하향 금지)
- 대상 질환이 Serious 이상이면 → 위험등급 = **3등급** (2등급 하향 금지)
- "의사 최종 결정권"은 등급 하향 근거가 **아님**

> **CRITICAL**: 뇌 MRI 분석 + 알츠하이머 확률 출력 = Treatment/Diagnosis × Serious = **3등급**. 이 결론은 비협상적(non-negotiable)입니다.

### Override 2. 품목코드 참조

> **Knowledge DB 참조**: MFDS AI SaMD 분류 기준은 `../../knowledge/catalog.yaml` → jurisdiction=mfds, topics contains "classification" 참조
> SaMD 의사결정력 수준(Sole Determinant/Driving/Informing)과 기능 유형별 분류 기준 확인 필수

### Override 3. MFDS 분류 시 반드시 포함할 출력 항목 (Level 2+)

아래 4개 항목이 MFDS 분류 섹션에 **반드시** 포함되어야 합니다:
- ① 디지털의료기기 4-Gate 분석
- ② 위해도 평가 위험 매트릭스 (Risk Matrix) Grid
- ③ 품목분류번호 7자리 코드
- ④ 등급 근거

> Detail: See `modules/mfds-classification.md` for full output templates

---

## Decision Framework

### FDA Classification Logic
> Detail: See `modules/fda-classification.md`

Summary: Class I (low risk, non-invasive) → Class II (moderate risk, special controls) → Class III (high risk, life-sustaining/implantable)

### EU MDR Annex VIII Classification Logic
> Detail: See `modules/eu-mdr-classification.md`

Summary: Rules 1-22 applied sequentially. For SaMD, Rule 11 is primary — maps IMDRF categories to EU MDR classes. Implementing Rule 3.5: strictest classification prevails.

### MFDS Classification Criteria
> Detail: See `modules/mfds-classification.md`

Summary: Classes 1-4. Digital devices: 4-Gate → Risk Matrix. Non-digital: 품목분류표 기반.

---

## Analysis Workflow

### Step 0 (pre-analysis)

**Level 1 (기본):** Knowledge DB 로드하지 않음. 위 Decision Framework 요약만으로 판단.
**Level 2:** 관련 jurisdiction의 Knowledge DB + 해당 modules/ 로드.

Knowledge DB references (Level 2+, 해당 jurisdiction만):
1. Read `../../knowledge/catalog.yaml`
2. Filter: jurisdiction={target} AND topics contains "classification"
3. Read matched chunk paths

레거시 참조 (catalog 미전환 jurisdiction):
- FDA: `../../knowledge/regulations/fda-framework.md`
- EU MDR: `../../knowledge/regulations/eu-mdr-framework.md`
- MFDS 일반: `../../knowledge/regulations/mfds-framework.md`
- SaMD: `../../knowledge/shared/samd-classification.md` → SaMD 해당 시

MFDS 디지털 (catalog 전환 완료):
- catalog.yaml에서 jurisdiction=mfds 필터 → 해당 청크 로드

**MFDS Digital Knowledge 로드 조건**:
- 키워드: AI, SW, 소프트웨어, software, IoT, 로봇, robot, VR, AR, 가상, HPC, 디지털, digital, SaMD, 앱, app, 알고리즘, 딥러닝, 머신러닝
- 또는: 이전 Gate 2 PASS 결과가 context에 있을 때
- 로드 대상: catalog.yaml → jurisdiction=mfds, topics contains "classification"

**Knowledge DB 로드 실패 시:**
catalog.yaml 또는 청크 파일 참조 불가 시: 기본 등급분류 체계(mfds-framework.md)만으로 판단하고, 정확한 4-Gate/Risk Matrix/7-digit 코드 분석은 Knowledge DB 확인 후 가능하다고 안내.

### Step 1: Extract Device Characteristics
- Device type and intended use
- Invasiveness level (non-invasive, invasive, implantable)
- Duration of contact (transient <60min, short-term <=30 days, long-term >30 days)
- Active vs passive classification
- Body system interaction
- Anatomical location

### Step 2: Apply FDA Classification Rules
> **(Level 2+)** Load `modules/fda-classification.md`
1. Assess device type and intended use
2. Determine if predicate device exists (510(k) pathway)
3. Evaluate risk factors (invasiveness, duration, active/passive)
4. Check for life-supporting/life-sustaining characteristics
5. Assign FDA Class (I, II, or III)

### Step 3: Apply EU MDR Annex VIII Rules
> **(Level 2+)** Load `modules/eu-mdr-classification.md`
1. Apply classification rules 1-22 in sequence
2. Evaluate invasiveness and duration
3. Check for special rules (implantable, CNS, cardiovascular)
4. Resolve conflicts (higher class takes precedence)
5. Assign EU MDR Class (I, IIa, IIb, or III)

### Step 4: Apply MFDS Classification Criteria
> **(Level 2+)** Load `modules/mfds-classification.md`

Step 4A (4-Gate) → Step 4B (Risk Matrix) or Step 4C (Traditional). See module for details.

### Step 5: Generate Classification Matrix
- Consolidate multi-region classifications
- Identify classification rationale per region
- Reference applicable rules and regulations
- Flag any discrepancies between regions

#### Evidence Requirements (per classification)

Each classification MUST include specific regulatory citations:

- **FDA**: Product code (e.g., QAS), CFR reference (e.g., 21 CFR 892.2050), predicate class basis
- **EU MDR**: Annex VIII Rule number(s), Implementing Rule 3.5 application
- **MFDS**: 품목분류번호, 등급 근거 — Risk Matrix (디지털) or 품목분류표 (비디지털)

**CRITICAL**: Do NOT fabricate product codes or CFR references. If uncertain, state "requires regulatory database verification."

**MANDATORY OUTPUT FORMAT (Level 2+ only):**
```
### Regulatory Evidence
- **FDA**: Product Code [XXX] — 21 CFR § [section] — Predicate basis: [class basis or "N/A"]
- **EU MDR**: Rule [N] (Annex VIII) — MDCG: [guidance ref if applicable]
- **MFDS**: 품목분류번호 [Axxxxx.xx] or 7-Digit Code [XXXXXXX] — 등급 근거: [detail]
```

**MANDATORY OUTPUT FORMAT (Level 2+ only):**
```
### Confidence & Escalation
- **Confidence Score**: [0-100]% — [basis]
- **Escalation Level**: [1-4] (1=automated, 2=brief review, 3=expert required, 4=authority consultation)
- **Next Action**: [recommended next step]
```

**MANDATORY OUTPUT FORMAT — Consistency Validation (Level 2+ only):**
```
### Consistency Validation
- Determination Traffic Light: [GREEN/YELLOW/RED]
- Stated Risk Level: [level]
- Assigned Grade: [N]등급
- **Consistency**: [PASS — aligned / FAIL — [mismatch description]]
```

### Step 6: (Optional) Classification Optimization Analysis
> Detail: See `modules/classification-optimization.md`

---

## Traffic Light Criteria

- **GREEN**: All regions definitive, no borderline, standard pathway
- **YELLOW**: Borderline/conditional, cross-region discrepancy, novel device → mandatory escalation
- **RED**: Insufficient info, conflicting rules, outside known framework

---

## Data Source Strategy

1. **Built-in Knowledge** (Primary): Embedded classification rules
2. **Module Files** (On-demand): Detailed rules in `modules/` loaded for Level 2+
3. **MCP Connectors** (Supplementary): Organization-specific verification

For MCP integration patterns, see `CONNECTORS.md`.
