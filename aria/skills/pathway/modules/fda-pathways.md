# FDA Pathway Details

## De Novo vs PMA Decision Framework

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

## Special Controls (De Novo pathway)

When recommending De Novo, MUST specify proposed Special Controls:
- **Performance Testing**: [specific test standards, e.g., ASTM F2129 for corrosion, IEC 62304 for software]
- **Biocompatibility**: [ISO 10993 series if applicable]
- **Clinical Performance**: [endpoint metrics, e.g., sensitivity/specificity for diagnostic SaMD]
- **Labeling Requirements**: [specific warnings, contraindications]
- **Post-Market Surveillance**: [mandatory reporting, registry participation]

## Material-to-Testing Chain

| Material/Component | Primary Test Standard | Test Purpose | Pathway Impact |
|--------------------|-----------------------|--------------|----------------|
| CoCr (Cobalt-Chromium) alloy | ASTM F2129 (corrosion), ASTM F1537 (wrought alloy) | Corrosion resistance, mechanical properties | PMA — implant-grade material requires comprehensive testing |
| PtIr (Platinum-Iridium) alloy | ASTM F2229 (wire), ASTM F2129 (corrosion) | Electrical performance, corrosion resistance | PMA — active implantable electrode material |
| Titanium / Ti alloy | ASTM F136 (wrought), ASTM F2129 (corrosion) | Biocompatibility, fatigue resistance | PMA or 510(k) depending on implant classification |
| Polymers (PEEK, UHMWPE) | ASTM F2026 (PEEK), ASTM F648 (UHMWPE) | Wear resistance, mechanical properties | 510(k) if predicate exists |
| Software / AI algorithm | IEC 62304 (SW lifecycle), IEC 82304-1 (health SW) | Software safety classification | De Novo for novel SaMD without predicate |
| Biological tissue | ISO 22442 (animal tissue), ASTM F2150 (characterization) | Tissue safety, sterility | PMA — biological device typically high risk |

> **Usage**: When a device contains specific materials, cross-reference this table to identify mandatory test standards and anticipate pathway complexity.

## 510(k) Resubmission Process

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

## Clinical Endpoint Standards (PMA and High-Risk Devices)

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
