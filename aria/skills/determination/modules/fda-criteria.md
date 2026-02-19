# FDA Device Determination Criteria (21 CFR 201(h))

## Definition

A medical device is an instrument, apparatus, implement, machine, contrivance, implant, in vitro reagent, or other similar or related article intended for use in the diagnosis, cure, mitigation, treatment, or prevention of disease, or to affect the structure or any function of the body — that does NOT achieve its primary intended purpose through chemical action or metabolism.

**Legal basis**: 21 USC §321(h), 21 CFR 201(h)

## Gate 1: Medical Device Definition Check

### Decision Tree

```
Product intended for:
├─ Diagnosis of disease or conditions? → Proceed to Gate 1B
├─ Cure, mitigation, treatment, prevention of disease? → Proceed to Gate 1B
├─ Affecting structure or function of the body? → Proceed to Gate 1B
└─ None of the above → CHECK wellness/CDS exclusions below
```

### Gate 1B: Exclusion Assessment

```
Primary mechanism of action:
├─ Chemical action or metabolism → NOT a device (likely drug) → EXIT NO
├─ Mechanical, physical, electrical, or computational → CONTINUE
└─ Both chemical AND mechanical → CONDITIONAL (combination product → see SKILL.md P5)
```

### Gate 1C: Wellness & CDS Exclusions

**General Wellness Policy** (FDA-2014-N-1039, revised Jan 2026):
- Product makes ONLY general wellness claims (e.g., "manage weight," "improve sleep quality," "promote relaxation")
- Product is low risk (non-invasive, does not involve testing for specific diseases)
- Product does NOT monitor, measure, or analyze biomarkers for medical conditions

```
Wellness assessment:
├─ Makes ONLY wellness claims + low risk + no biomarker analysis → NO (general wellness)
├─ Makes wellness claims BUT ALSO:
│   ├─ Monitors SpO2, heart rhythm, respiratory patterns → CONDITIONAL
│   │   Reason: Biomarker monitoring may exceed wellness scope
│   │   Resolution: If monitoring is purely informational with no alerts/flags → may remain wellness
│   │                If monitoring triggers alerts or suggests medical action → YES (device)
│   ├─ Provides disease-specific insights or screening → YES (device)
│   └─ Suggests user "consult a healthcare professional" based on data → CONDITIONAL
│       Reason: CDS exemption boundary (21st Century Cures Act §3060)
│       Resolution: If meets all 4 CDS criteria → NO (exempt CDS)
│                    If fails any CDS criterion → YES (device)
└─ Makes explicit medical/diagnostic claims → YES (device)
```

**CDS Exemption Criteria** (21st Century Cures Act §3060, all 4 must be met):
1. Not intended to acquire, process, or analyze a medical image/signal/specimen
2. Intended for displaying, analyzing, or printing medical information
3. Intended for HCPs to independently review the basis for recommendations
4. Not intended to replace clinical judgment

### Gate 1 Output

| Result | Meaning | Next Step |
|--------|---------|-----------|
| **YES** | Product is a medical device | Proceed to classification |
| **NO** | Product is NOT a medical device | EXIT — not subject to FDA regulation |
| **CONDITIONAL** | Boundary case | Output uncertainty basis + resolution conditions + both scenarios |

## Predicate & Pathway Pre-Assessment

**Purpose**: Inform classification and pathway skills with predicate availability data.

```
Predicate search:
├─ Predicate device exists (substantially equivalent) → Note: 510(k) pathway likely
├─ Predicate absent + product is low-to-moderate risk →
│   ├─ De Novo (PRIMARY) — creates new regulatory classification
│   │   Note: De Novo results in Class I or Class II with special controls
│   │   Note: Specific DEN numbers require FDA database verification (do NOT fabricate)
│   └─ PMA (FALLBACK — only if risk assessment indicates high risk)
└─ Predicate absent + product is high risk → PMA (PRIMARY)
```

**Key indicators for De Novo vs PMA**:
- Novel device with no predicate BUT low-moderate risk profile → **De Novo**
- Device type has never been classified → **De Novo** (creates new classification)
- Implantable but not life-sustaining, with mitigable risks → **De Novo possible**
- Life-sustaining, life-supporting, or high risk of illness/injury → **PMA**

**CRITICAL**: Do NOT default to "no predicate → automatic Class III → PMA." The De Novo pathway exists specifically for novel devices that are NOT high risk. Always evaluate De Novo as the primary option when predicate is absent and risk is low-to-moderate.

## Common Boundary Examples

| Product Type | Likely Status | Rationale |
|---|---|---|
| Surgical instrument | YES | Direct medical use, non-chemical |
| Fitness tracker (no medical claims) | NO | General wellness, no medical purpose |
| Software with diagnostic claims | YES (SaMD) | Intended for diagnosis |
| Sleep monitor with SpO2 + wellness claims | CONDITIONAL | Wellness/device boundary — depends on claims and alert logic |
| Topical with drug component | CONDITIONAL | May be combination product |
| AI screening tool (no predicate) | YES, De Novo likely | Novel SaMD, low-moderate risk |
