# EU MDR Annex VIII Classification Logic

## Class I (Low Risk)
- Non-invasive devices
- Transient use (<60 minutes)
- Minimal risk profile

## Class IIa (Medium-Low Risk)
- Short-term invasive devices (<=30 days)
- Transient use with specific body systems
- Examples: Contact lenses, hearing aids

**Decision Rules**:
- Rule 5: Non-invasive devices channeling/storing body substances - IIa
- Rule 6: Short-term invasive surgically devices - IIa

## Class IIb (Medium-High Risk)
- Long-term invasive devices (>30 days)
- Active therapeutic devices delivering potentially dangerous energy
- Examples: Lung ventilators, bone screws

**Decision Rules**:
- Rule 7: Long-term surgically invasive devices - IIb (general), III (heart/CNS/circulatory)
- Rule 8: Active implantable devices - IIb (general), III (heart/CNS/circulatory)
- Rule 9: Active therapeutic devices delivering potentially dangerous energy - IIb
- Rule 11 (SaMD, higher tier): Software intended to drive clinical management of serious/critical conditions - IIb

## Class III (High Risk)
- Devices in direct contact with heart, central circulatory system, CNS
- Implantable/long-term devices affecting vital functions
- Examples: Heart valves, drug-eluting stents

**Decision Rules**:
- Rule 8: Active implantable devices in direct contact with heart/CNS/central circulatory → III
- Rule 11 (SaMD, highest tier): Software intended for diagnosis/treatment of critical conditions → III
- Rule 14: Devices incorporating medicinal substance with ancillary action → III
- Implementing Rule 3.5: When multiple rules apply, the STRICTEST classification prevails

## Rule 11: Software (SaMD) Classification

**Rule 11 is the PRIMARY classification rule for Software as a Medical Device (SaMD).**

### IMDRF SaMD Risk Categorization Integration

| IMDRF Category | SaMD Function | Patient Condition | EU MDR Class |
|---|---|---|---|
| **Category I** (Inform clinical management) | Inform | Non-serious | **Class IIa** |
| **Category I** (Inform clinical management) | Inform | Serious | **Class IIa** |
| **Category II** (Drive clinical management) | Drive | Non-serious | **Class IIa** |
| **Category II** (Drive clinical management) | Drive | Serious | **Class IIb** |
| **Category III** (Treat or diagnose) | Diagnose/Treat | Non-serious | **Class IIa** |
| **Category III** (Treat or diagnose) | Diagnose/Treat | Serious | **Class IIb** |
| **Category IV** (Treat or diagnose) | Diagnose/Treat | Critical | **Class III** |

### Screening vs Diagnosis Distinction (CRITICAL for Rule 11)

```
SaMD function analysis:
├─ Screening/Triage (population-level, non-diagnostic)
│   - Output: "Consider further evaluation" / "Risk flag"
│   - Does NOT provide a diagnosis
│   - IMDRF: "Inform clinical management"
│   → Class IIa (even for serious conditions)
│
├─ Diagnostic (individual-level, specific condition identification)
│   - Output: "Disease X detected" / "Condition Y identified"
│   - Provides actionable diagnostic information
│   - IMDRF: "Treat or diagnose"
│   → Class IIb (serious) or Class III (critical)
│
└─ Treatment/Therapy guidance
    - Output: Dosing, treatment planning, therapy delivery
    - IMDRF: "Treat or diagnose"
    → Class IIb (serious) or Class III (critical)
```

**Example**: AI diabetic retinopathy SCREENING (binary refer/no-refer output):
- Function: Screening (not diagnosis — refers to specialist for confirmation)
- Patient condition: Serious (diabetic retinopathy can cause blindness)
- IMDRF: "Inform clinical management" of serious condition
- **Rule 11 result: Class IIa** (NOT IIb)

**Key principle**: The "serious deterioration" tier in Rule 11 requires the SOFTWARE ITSELF to drive or determine treatment/diagnosis, not merely flag for further evaluation.
