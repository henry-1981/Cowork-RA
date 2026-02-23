---
last_updated: "2026-02-23"
sources:
  - "IMDRF/SaMD WG/N10 FINAL:2013 — Key Definitions"
  - "IMDRF/SaMD WG/N12 FINAL:2014 — Risk Categorization Framework"
  - "IMDRF/SaMD WG/N41 FINAL:2017 — Clinical Evaluation"
  - "IMDRF/SaMD WG/N81 FINAL:2025 — Software-Specific Risk Characterization"
  - "IMDRF/AIML WG/N88 FINAL:2025 — Good Machine Learning Practice (GMLP)"
  - "FDA 21 CFR Parts 860, 880–892"
  - "Regulation (EU) 2017/745, Annex VIII, Rule 11"
  - "MDCG 2019-11 Rev.1 (June 2025)"
  - "MFDS Notification No. 2020-76 (Medical Device Classification)"
  - "Korean Digital Medical Products Act (January 2025)"
next_review: "2026-03-23"
---

# IMDRF SaMD Classification Framework

## 1. IMDRF Document System — Evolution of SaMD Guidance

The International Medical Device Regulators Forum (IMDRF) SaMD Working Group has produced
a progressive series of guidance documents since 2013. Each document builds on its predecessors
to create a comprehensive global framework for software-based medical devices.

> **Source**: [IMDRF SaMD Working Group page](https://www.imdrf.org/working-groups/software-medical-device-samd)

### 1.1 Document Progression

| Document | Year | Title | Key Contribution |
|----------|------|-------|------------------|
| **N10** | 2013 | Key Definitions | Established foundational SaMD/SiMD definitions |
| **N12** | 2014 | Framework for Risk Categorization and Corresponding Considerations | Two-axis risk matrix (Significance × Severity) → Categories I–IV |
| **N23** | 2015 | Application of Quality Management System | QMS principles for SaMD lifecycle |
| **N41** | 2017 | Clinical Evaluation | Three-pillar clinical evidence framework (VCA, AV, CV) |
| **N81** | 2025 | Characterization Considerations for Medical Device Software and Software-Specific Risk | Expanded scope to all MDSW (SaMD + SiMD), comprehensive risk characterization |
| **N88** | 2025 | Good Machine Learning Practice: Guiding Principles | 10 GMLP principles for AI/ML-enabled medical devices |

> **Source**: IMDRF document library; [IMDRF releases N81 and N88 (Jan 2025)](https://www.emergobyul.com/news/imdrf-releases-key-guidance-documents-medical-device-software)

### 1.2 Key Definitions from N10

| Term | Definition | Source |
|------|-----------|--------|
| **SaMD** | Software intended to be used for one or more medical purposes that perform these purposes without being part of a hardware medical device | IMDRF/SaMD WG/N10 FINAL:2013, §3 |
| **SiMD** | Software that is an integral part of a medical device (i.e., part of hardware medical device) | IMDRF/SaMD WG/N10 FINAL:2013, §3 |
| **Medical purpose** | Diagnosis, prevention, monitoring, prediction, prognosis, treatment, or alleviation of disease; or investigation, replacement, or modification of anatomy or physiological/pathological process or state | IMDRF/SaMD WG/N10 FINAL:2013, §3 |

**Boundary clarifications (N10)**:
- SaMD **is**: Stand-alone software performing medical functions independently
- SaMD **is not**: Software that drives or controls a hardware medical device (that is SiMD)
- SaMD **is not**: Software used in the manufacturing or maintenance of a medical device
- SaMD **may run on**: General-purpose computing platforms (PCs, smartphones, cloud servers)

> **Source**: IMDRF/SaMD WG/N10 FINAL:2013

---

## 2. Risk Categorization Matrix — N12 (2014)

The N12 document establishes the central risk categorization framework that has been adopted
or adapted by regulators worldwide. It uses a two-axis matrix to assign SaMD to one of four
risk categories (I–IV).

> **Source**: [IMDRF/SaMD WG/N12 FINAL:2014](https://www.imdrf.org/sites/default/files/docs/imdrf/final/technical/imdrf-tech-140918-samd-framework-risk-categorization-141013.pdf)

### 2.1 Axis Definitions

**Axis 1 — Significance of Information Provided by SaMD**:

| Level | Definition | Examples |
|-------|-----------|----------|
| **Treat or Diagnose** | SaMD provides information used to take an immediate or near-term action — to treat, diagnose, or screen for a disease or condition | AI diagnostic imaging, automated therapy dosing, diagnostic screening algorithms |
| **Drive Clinical Management** | SaMD provides information to aid in determining treatment, diagnosis, triage, or identifying early stages of a disease — aids clinical management but is not the sole basis for decision | Clinical decision support, risk scoring tools, drug interaction checkers |
| **Inform Clinical Management** | SaMD provides information that is not intended to trigger immediate clinical action; it may aggregate, trend, or make recommendations that clinicians consider alongside other data | Data trending dashboards, population health analytics, general wellness indicators |

**Axis 2 — Severity of Healthcare Situation or Condition**:

| Level | Definition | Examples |
|-------|-----------|----------|
| **Critical** | Situations or conditions where inaccurate information could lead to death or irreversible deterioration of health; or where interventions to mitigate such outcomes are time-critical | Acute stroke, cardiac arrest, cancer diagnosis, sepsis |
| **Serious** | Situations or conditions where inaccurate information could lead to serious deterioration of health (potentially reversible) or where a surgical intervention may be needed | Fracture diagnosis, moderate infections, chronic disease exacerbation |
| **Non-serious** | Situations or conditions where inaccurate information would not lead to significant harm; conditions that are self-limiting or easily manageable | Minor skin conditions, general fitness tracking, mild symptom tracking |

> **Source**: IMDRF/SaMD WG/N12 FINAL:2014, Section 7

### 2.2 Risk Categorization Matrix

| Significance \ Severity | **Critical** | **Serious** | **Non-serious** |
|------------------------|-------------|------------|----------------|
| **Treat or Diagnose** | **IV** | **III** | **II** |
| **Drive Clinical Management** | **III** | **II** | **II** |
| **Inform Clinical Management** | **II** | **II** | **I** |

> **Source**: IMDRF/SaMD WG/N12 FINAL:2014, Table 1

**Category descriptions**:

| Category | Risk Level | Regulatory Intensity |
|----------|-----------|---------------------|
| **I** | Lowest risk | Minimal regulatory oversight |
| **II** | Low-moderate risk | Moderate regulatory controls |
| **III** | Moderate-high risk | Significant regulatory controls |
| **IV** | Highest risk | Most stringent regulatory controls |

### 2.3 Highest Category Rule

When a SaMD can be used across multiple clinical contexts (significance levels or severity
levels), it must be categorized based on the **most severe applicable combination**. This
mirrors the "highest class wins" principle in EU MDR Implementing Rule 3.5.

> *"When a SaMD can be used across multiple intended use environments, the SaMD should be
> categorized based on the most critical intended use."*
> — IMDRF/SaMD WG/N12 FINAL:2014, Section 7.3

### 2.4 Special Considerations

- **Lay user escalation**: When SaMD is used by lay users (non-healthcare professionals) in
  serious or critical situations without immediate access to specialist support, the severity
  should be escalated to the next higher level.
  *(IMDRF/SaMD WG/N12 FINAL:2014, Section 7.2)*

- **Professional context**: The intended user (specialist physician, general practitioner,
  nurse, patient) affects how the information is interpreted and therefore influences risk.

---

## 3. Three-Jurisdiction Mapping — IMDRF ↔ FDA ↔ EU MDR ↔ MFDS

Each major jurisdiction has adopted its own regulatory classification system for SaMD, but
all are influenced by the IMDRF N12 framework. The mappings below show the approximate
correspondence between systems.

> **Sources**:
> - IMDRF/SaMD WG/N12 FINAL:2014
> - FDA 21 CFR §860.3; FDA Guidance "Policy for Device Software Functions" (2019)
> - Regulation (EU) 2017/745, Annex VIII, Rule 11; MDCG 2019-11 Rev.1
> - MFDS Medical Device Act, Article 2; Notification No. 2020-76
> - Korean Digital Medical Products Act (effective Jan 2025)

### 3.1 Classification Mapping Table

| IMDRF Category | FDA Class | EU MDR Class | MFDS Grade | NB/Review Required |
|---------------|-----------|-------------|------------|-------------------|
| **I** | Class I (exempt) | Class I | Grade 1 | FDA: No 510(k); EU: Self-declaration; MFDS: Notification |
| **II** | Class I or II | Class IIa | Grade 2 | FDA: 510(k) or exempt; EU: NB required; MFDS: MDITAC/NIDS review |
| **III** | Class II | Class IIb | Grade 3 | FDA: 510(k) or De Novo; EU: NB required; MFDS: MFDS review |
| **IV** | Class III | Class III | Grade 4 | FDA: PMA or De Novo; EU: NB full assessment; MFDS: MFDS review (clinical trial may be required) |

### 3.2 Key Mapping Notes

**FDA (United States)**:
- The FDA does not formally adopt IMDRF categories but recognizes the N12 framework in its
  guidance documents. The FDA policy document "Policy for Device Software Functions and
  Mobile Medical Applications" (2019) uses risk-based thinking consistent with IMDRF.
- FDA classification is product-code-based (21 CFR Parts 880–892), not purely rule-based.
- IMDRF Categories I–II generally map to FDA Class I–II (510(k) exempt or cleared).
- IMDRF Categories III–IV map to FDA Class II (510(k)/De Novo) or Class III (PMA).
- The FDA's Digital Health Center of Excellence manages SaMD regulatory pathways.

> **Source**: FDA Guidance "Policy for Device Software Functions" (September 2019);
> 21 CFR §860.3 (device classification)

**EU MDR (European Union)**:
- Rule 11 of Annex VIII is the primary classification rule for MDSW/SaMD.
- MDCG 2019-11 Rev.1 explicitly aligns the Rule 11 classification matrix with the IMDRF
  N12 framework. The alignment is:
  - IMDRF "Inform × Non-serious" (Cat I) → EU Class I
  - IMDRF "Drive/Inform × Serious/Non-serious" (Cat II) → EU Class IIa
  - IMDRF "Treat/Diagnose × Serious" or "Drive × Critical" (Cat III) → EU Class IIb
  - IMDRF "Treat/Diagnose × Critical" (Cat IV) → EU Class III
- EU tends to classify SaMD at a **higher** level than other jurisdictions — Class I software
  is rare under the current Rule 11 interpretation.

> **Source**: Regulation (EU) 2017/745, Annex VIII, Rule 11; MDCG 2019-11 Rev.1, Table 2

**MFDS (South Korea)**:
- South Korea's classification follows the GHTF (predecessor to IMDRF) four-tier system:
  Grade 1 (lowest) through Grade 4 (highest).
- The MFDS adopted IMDRF-aligned SaMD definitions through its "Guidelines for Approval and
  Examination of Machine Learning-enabled Medical Devices."
- As of 24 January 2025, the Digital Medical Products Act regulates digital-only medical
  devices (including SaMD) under a streamlined pathway.
- The AI Basic Act (effective 22 January 2026) classifies healthcare AI as "High-Impact,"
  introducing additional oversight requirements.
- Grade 1–2 devices are certified by MDITAC (Medical Device Information and Technology
  Assistance Center) or NIDS. Grade 3–4 devices require direct MFDS approval.

> **Source**: MFDS Medical Device Act; Korean Digital Medical Products Act (2025);
> [MFDS approval process](https://www.mfds.go.kr/eng/wpge/m_39/denofile.do);
> [Korea SaMD guidelines overview](https://www.freyrsolutions.com/blog/an-overview-of-south-koreas-samd-approval-guidelines)

### 3.3 Regulatory Pathway Comparison

| Aspect | FDA | EU MDR | MFDS |
|--------|-----|--------|------|
| **Primary SaMD pathway** | 510(k), De Novo, PMA | CE marking via NB (Class IIa+) | Technical review + approval |
| **AI/ML-specific pathway** | Predetermined Change Control Plan (PCCP) | AI Act (Reg 2024/1860) overlay | Digital Medical Products Act + AI Basic Act |
| **Clinical evidence** | Per submission type (510(k) may use predicate) | CER + PMCF for all classes | Clinical trial for Grade 3–4; clinical literature for Grade 1–2 |
| **Post-market** | 510(k) Annual Report, MDR (device) reporting | PMS Plan, PSUR (IIa+), PMCF | GMP periodic audit, adverse event reporting |
| **Software change management** | Predetermination of modifications (PCCP for AI/ML) | Significant change → NB re-assessment | Change notification to MFDS |
| **Expedited pathway** | Breakthrough Device Designation | BtX (MDCG 2025-9, pilot Q2 2026) | Priority review for innovative devices |
| **Average review timeline** | 510(k): ~130 days; De Novo: ~260 days; PMA: ~180 days | NB assessment: 13–18 months | Grade 2: ~40 days; Grade 3: ~80 days; Grade 4: ~120 days |

---

## 4. Clinical Evaluation Framework — N41 (2017)

The N41 document establishes a globally harmonized clinical evaluation framework for SaMD
based on three pillars of clinical evidence.

> **Source**: [IMDRF/SaMD WG/N41 FINAL:2017](https://www.imdrf.org/sites/default/files/docs/imdrf/final/technical/imdrf-tech-170921-samd-n41-clinical-evaluation_1.pdf)

### 4.1 Three Pillars of Clinical Evidence

```
            ┌─────────────────────────────────────────────┐
            │         SaMD Clinical Evidence               │
            │                                             │
            │  ┌───────────┐  ┌──────────┐  ┌──────────┐ │
            │  │   Valid    │  │Analytical│  │ Clinical │ │
            │  │  Clinical  │  │Validation│  │Validation│ │
            │  │Association │  │   (AV)   │  │   (CV)   │ │
            │  │   (VCA)   │  │          │  │          │ │
            │  └───────────┘  └──────────┘  └──────────┘ │
            └─────────────────────────────────────────────┘
```

**Pillar 1 — Valid Clinical Association (VCA)**:
Establishes that the SaMD output (e.g., a biomarker, clinical metric, or diagnostic conclusion)
has a well-founded, clinically meaningful association with the target clinical condition.

| Aspect | Description |
|--------|------------|
| **Purpose** | Demonstrate that the input/output relationship is clinically meaningful |
| **Evidence sources** | Published literature, clinical guidelines, established clinical practice |
| **Question answered** | "Is there a valid scientific basis connecting the SaMD output to the clinical condition?" |
| **Example** | HbA1c levels are validly associated with diabetes management status |

> **Source**: IMDRF/SaMD WG/N41 FINAL:2017, Section 7

**Pillar 2 — Analytical Validation (AV)**:
Demonstrates that the SaMD accurately, reliably, and precisely generates the intended output
from the input data.

| Aspect | Description |
|--------|------------|
| **Purpose** | Verify that the software correctly processes inputs to produce intended outputs |
| **Evidence sources** | Bench testing, algorithm verification, reference dataset comparison |
| **Question answered** | "Does the SaMD reliably produce the correct technical output?" |
| **Example** | An AI algorithm correctly identifies pulmonary nodules in CT scans with sensitivity ≥95% and specificity ≥90% on a reference dataset |

> **Source**: IMDRF/SaMD WG/N41 FINAL:2017, Section 8

**Pillar 3 — Clinical Validation (CV)**:
Demonstrates that the SaMD achieves a clinically meaningful output in the target population
under intended conditions of use.

| Aspect | Description |
|--------|------------|
| **Purpose** | Confirm that the SaMD output leads to the intended clinical benefit in real use |
| **Evidence sources** | Clinical studies, real-world evidence, user studies, outcome data |
| **Question answered** | "Does the SaMD deliver the claimed clinical benefit when used as intended?" |
| **Example** | Use of the AI diagnostic tool results in improved detection rates and patient outcomes compared to standard of care |

> **Source**: IMDRF/SaMD WG/N41 FINAL:2017, Section 9

### 4.2 Evidence Level Expectations by IMDRF Category

| Category | VCA | AV | CV |
|----------|-----|----|----|
| **I** | Published literature sufficient | Testing per software lifecycle | May rely on literature/real-world evidence |
| **II** | Published literature or guidelines | Testing with reference datasets | Clinical study or substantial real-world evidence |
| **III** | Well-established clinical association required | Rigorous testing with independent reference standard | Prospective clinical study recommended |
| **IV** | Strong, independently validated clinical association | Comprehensive analytical testing with external validation | Prospective clinical study generally required |

> **Source**: IMDRF/SaMD WG/N41 FINAL:2017, Section 10, Table 2

### 4.3 Jurisdictional Adoption

- **FDA**: Adopted N41 framework through the December 2017 Federal Register notice
  (FDA-2016-D-2483). The FDA uses these principles within its 510(k), De Novo, and PMA
  review processes for SaMD.
- **EU**: MDCG 2020-1 "Guidance on Clinical Evaluation (MDR) / Performance Evaluation (IVDR)
  of Medical Device Software" directly references and builds upon N41.
- **MFDS**: Guidelines for ML-enabled medical devices reference IMDRF clinical evaluation
  principles.

> **Source**: FDA Federal Register Vol. 82, No. 235 (8 Dec 2017); MDCG 2020-1

---

## 5. GMLP — 10 Guiding Principles (N88, January 2025)

The IMDRF AI/ML Working Group published N88 on 27 January 2025, establishing 10 guiding
principles for Good Machine Learning Practice (GMLP) in medical device development.

> **Source**: [IMDRF/AIML WG/N88 FINAL:2025](https://www.imdrf.org/sites/default/files/2025-01/IMDRF_AIML%20WG_GMLP_N88%20Final_0.pdf);
> [UK GOV.UK GMLP Principles](https://www.gov.uk/government/publications/good-machine-learning-practice-for-medical-device-development-guiding-principles/good-machine-learning-practice-for-medical-device-development-guiding-principles)

These principles are aligned with the jointly identified principles of the FDA, Health Canada,
and MHRA (originally published October 2021), with minor refinements in wording for the IMDRF
final version.

### 5.1 The 10 Principles

**Principle 1 — Well-Defined Intended Use**
AI-enabled medical devices must be designed to address clinically meaningful needs. An
in-depth understanding of the model's intended integration into clinical workflow, including
a thorough assessment of potential benefits and risks, should be maintained throughout the
total product lifecycle.
*(IMDRF/AIML WG/N88, Principle 1)*

**Principle 2 — Good Software Engineering, Device Design, and Security Practices**
Model development, including data management, feature selection, training, evaluation, and
deployment, should follow validated quality management system practices. Robust cybersecurity
practices and structured risk management (consistent with ISO 14971) must be implemented
throughout the device lifecycle.
*(IMDRF/AIML WG/N88, Principle 2)*

**Principle 3 — Representative Clinical Data**
Data collection protocols must ensure that datasets used for training, testing, and monitoring
sufficiently represent the intended patient population. This includes adequate representation
across relevant demographics, clinical characteristics, and use environments to minimize bias
and ensure generalizable performance.
*(IMDRF/AIML WG/N88, Principle 3)*

**Principle 4 — Independent Training and Test Datasets**
Training and testing datasets must maintain appropriate independence to ensure valid performance
evaluation. All potential dependencies — related to patients, sites, data acquisition methods,
and timing — must be identified and managed to prevent data leakage and overly optimistic
performance estimates.
*(IMDRF/AIML WG/N88, Principle 4)*

**Principle 5 — Fit-for-Purpose Reference Standards**
Reference datasets should be based upon accepted, best-available methods ensuring clinically
relevant and well-characterized data. The rationale for reference standard selection and its
known limitations must be documented.
*(IMDRF/AIML WG/N88, Principle 5)*

**Principle 6 — Model Design Tailored to Data and Intended Use**
The choice and design of the AI/ML model must be appropriate for the available data and the
intended clinical use. Risks such as overfitting, underfitting, and performance degradation
over time must be evaluated and mitigated.
*(IMDRF/AIML WG/N88, Principle 6)*

**Principle 7 — Assessment of Human-AI Interaction**
The focus should be placed on the performance of the **Human-AI team** rather than just the
model in isolation. Evaluation must consider the user's skills and training, potential for
overreliance on or undertrust of the AI system, and foreseeable misuse scenarios within the
intended clinical workflow.
*(IMDRF/AIML WG/N88, Principle 7)*

**Principle 8 — Performance Testing in Clinically Relevant Conditions**
Statistically sound test plans must be developed to generate clinically relevant device
performance information independently of the training dataset. Testing must cover intended
populations and realistic clinical environments, including edge cases and failure modes.
*(IMDRF/AIML WG/N88, Principle 8)*

**Principle 9 — Clear and Essential Information for Users**
Users must be provided with accessible and comprehensive details about the device's intended
use, performance across relevant subgroups, training data characteristics, known limitations,
and integration into the clinical workflow.
*(IMDRF/AIML WG/N88, Principle 9)*

**Principle 10 — Monitoring of Deployed Models and Management of Re-training Risks**
Deployed models must be continuously monitored for real-world performance. Risks associated
with model retraining — including dataset drift, concept drift, and unintended bias
introduction — must be proactively managed through a structured change management process.
*(IMDRF/AIML WG/N88, Principle 10)*

### 5.2 Regulatory Adoption of GMLP

| Jurisdiction | Adoption Status | Reference |
|-------------|----------------|-----------|
| **FDA (US)** | Co-authored original 10 principles (Oct 2021); endorses N88 | FDA AI/ML Action Plan (2021) |
| **Health Canada** | Co-authored original 10 principles; endorses N88 | Health Canada GMLP guidance (2021) |
| **MHRA (UK)** | Co-authored original 10 principles; endorses N88 | GOV.UK GMLP publication |
| **EU (MDCG)** | Referenced in MDCG 2025-6 / AIB 2025-1 | MDCG 2025-6, Section 4 |
| **MFDS (Korea)** | Incorporated through Guidelines for ML-enabled Medical Devices | MFDS AI device guidance (2022, updated 2024) |
| **TGA (Australia)** | Endorses IMDRF principles; participates in SaMD WG | TGA AI/ML regulatory guidance |
| **PMDA (Japan)** | Endorses IMDRF principles; participates in AIML WG | PMDA AMED AI guidance |

---

## 6. Software-Specific Risk Characterization — N81 (January 2025)

The N81 document, published 27 January 2025, represents a major expansion of the IMDRF
software risk framework beyond SaMD to encompass **all medical device software** (MDSW).

> **Source**: [IMDRF/SaMD WG/N81 FINAL:2025](https://www.imdrf.org/sites/default/files/docs/imdrf/final/technical/imdrf-tech-140918-samd-framework-risk-categorization-141013.pdf);
> [IMDRF N81 overview](https://www.imdrf.org/documents/characterization-considerations-medical-device-software-and-software-specific-risk)

### 6.1 Expanded Scope — SaMD + SiMD

Unlike the N12 framework (which focused exclusively on SaMD), N81 applies to **all medical
device software** irrespective of:
- Software technology (traditional algorithms, AI/ML, rule-based, hybrid)
- Platform (mobile application, cloud, server, embedded hardware)
- Relationship to hardware (SaMD = standalone, SiMD = embedded)

> *"This document focuses on medical device software irrespective of the software technology
> and/or the platform."*
> — IMDRF/SaMD WG/N81 FINAL:2025, Section 1

### 6.2 Software Characterization Considerations

N81 establishes a structured approach to characterize medical device software through:

**Intended Use / Intended Purpose Statement**:
- Clear definition of the medical purpose
- Target population and clinical context
- User type (healthcare professional, lay user, or both)
- Operating environment and platform constraints

**Medical Device Software Description**:
- Functional description of the software
- Input/output specifications
- Data sources and data flow
- Interfaces with other systems (interoperability)
- AI/ML model description (if applicable)

> **Source**: IMDRF/SaMD WG/N81 FINAL:2025, Section 4

### 6.3 Risk Characterization Framework

N81 provides a comprehensive risk characterization process:

**Step 1 — Risk Identification and Analysis**:
- Identify hazardous situations related to software function
- Consider software-specific failure modes (data integrity, algorithm errors, latency,
  interoperability failures, cybersecurity vulnerabilities)
- Analyze the chain: Software failure → Hazardous situation → Harm

**Step 2 — Risk Estimation**:
- Probability of occurrence (considering software reliability, use environment, user factors)
- Severity of harm (consistent with N12 severity axis: Critical, Serious, Non-serious)
- Combination to estimate overall risk

**Step 3 — Approaches for Risk Categorization**:
- Apply the N12 matrix for SaMD
- For SiMD, consider the overall device risk classification and the software's contribution
- Consider the software's autonomy level (decision-support vs. autonomous decision-making)

> **Source**: IMDRF/SaMD WG/N81 FINAL:2025, Section 5

### 6.4 Software-Specific Risk Factors

N81 identifies risk factors unique to software-based medical devices:

| Risk Factor | Description |
|------------|------------|
| **Data integrity** | Errors in input data (corrupted, incomplete, out-of-range) propagating through the software |
| **Algorithm performance** | Model accuracy degradation, edge cases, out-of-distribution inputs |
| **Interoperability** | Failures in data exchange with EHR systems, other devices, or networks |
| **Cybersecurity** | Unauthorized access, data breach, malicious modification of software behavior |
| **Update/change management** | Unintended consequences of software updates, version incompatibility |
| **Platform dependency** | Operating system updates, cloud service changes, hardware obsolescence |
| **User interface** | Misinterpretation of outputs, alert fatigue, workflow integration failures |
| **Autonomy level** | Higher risk when software makes autonomous decisions vs. advisory role |
| **Dataset drift** | For AI/ML: change in input data distribution over time degrading performance |
| **Concept drift** | For AI/ML: change in the underlying clinical relationship the model learned |

> **Source**: IMDRF/SaMD WG/N81 FINAL:2025, Section 5.2

### 6.5 Relationship to N12

N81 does **not replace** N12 but builds upon it:
- N12 remains the primary risk categorization framework for SaMD classification
- N81 adds depth to risk characterization by providing software-specific risk analysis guidance
- N81 extends the framework to SiMD, which was outside N12's scope
- Together, N12 + N81 provide a comprehensive "what category" (N12) + "how to analyze risks"
  (N81) framework

> **Source**: IMDRF/SaMD WG/N81 FINAL:2025, Section 1.2

---

## 7. Summary — SaMD Classification Decision Framework

```
Step 1: Determine if software is SaMD (N10 definitions)
├── Does software perform a medical purpose? → If No → Not SaMD
├── Is software independent of hardware device? → If No → SiMD (use N81)
└── Yes to both → SaMD

Step 2: Apply N12 Risk Categorization Matrix
├── Determine Significance: Treat/Diagnose, Drive, or Inform
├── Determine Severity: Critical, Serious, or Non-serious
├── Map to Category I, II, III, or IV
└── Apply "highest category" rule if multiple uses

Step 3: Map to Jurisdiction-Specific Classification
├── FDA → Class I, II, or III (product-code-based)
├── EU MDR → Rule 11 → Class I, IIa, IIb, or III
└── MFDS → Grade 1, 2, 3, or 4

Step 4: Determine Clinical Evidence Requirements (N41)
├── Establish Valid Clinical Association
├── Perform Analytical Validation
└── Perform Clinical Validation (rigor scales with category)

Step 5: For AI/ML-based SaMD, apply GMLP (N88)
├── Follow 10 guiding principles throughout lifecycle
├── Address training data representativeness
├── Plan for continuous monitoring and drift management
└── Design for human-AI team performance

Step 6: Characterize Software-Specific Risks (N81)
├── Document intended use and software description
├── Identify software-specific hazards and failure modes
└── Estimate and mitigate risks per established framework
```
