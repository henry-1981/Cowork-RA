---
last_updated: "2026-02-23"
sources:
  - "Regulation (EU) 2017/745 of the European Parliament and of the Council"
  - "MDCG 2019-11 Rev.1 — Qualification and Classification of Software (June 2025)"
  - "MDCG 2021-24 — Guidance on Classification of Medical Devices"
  - "MDCG 2025-6 / AIB 2025-1 — Interplay between MDR/IVDR and AI Act"
  - "MDCG 2025-9 — Guidance on Breakthrough Devices (BtX)"
  - "Regulation (EU) 2023/607 — Transitional Provisions Amendment"
  - "Regulation (EU) 2024/1860 — AI Act (Artificial Intelligence Act)"
  - "COM(2025) 1023 — Proposal to Simplify MDR/IVDR (December 2025)"
next_review: "2026-03-23"
---

# EU MDR Regulatory Framework for SaMD

## 1. Classification Rules — Annex VIII of Regulation (EU) 2017/745

The EU Medical Devices Regulation (MDR) 2017/745, which became fully applicable on 26 May 2021,
establishes 22 classification rules in Annex VIII that determine whether a device falls into
Class I, Class IIa, Class IIb, or Class III. These rules replaced the 18 rules from the
previous Medical Device Directive (MDD) 93/42/EEC.

> **Source**: Regulation (EU) 2017/745, Annex VIII, Chapters I–III
> ([EUR-Lex CELEX:32017R0745](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32017R0745))

### 1.1 Chapter I — Definitions Specific to Classification Rules

**Duration of Use** (Section 1):

| Term | Definition | Reference |
|------|-----------|-----------|
| **Transient** | Normally intended for continuous use for less than 60 minutes | Annex VIII, §1.1 |
| **Short-term** | Normally intended for continuous use for between 60 minutes and 30 days | Annex VIII, §1.2 |
| **Long-term** | Normally intended for continuous use for more than 30 days | Annex VIII, §1.3 |

**Invasive and Active Device Definitions** (Section 2):

- **Body orifice** (§2.1): Any natural opening in the body, as well as the external surface of
  the eyeball, or any permanent artificial opening such as a stoma.
  *(Annex VIII, §2.1)*

- **Surgically invasive device** (§2.2): A device that penetrates the body surface through or in
  the context of a surgical operation, or produces penetration other than through a body orifice.
  *(Annex VIII, §2.2)*

- **Reusable surgical instrument** (§2.3): An instrument intended for cutting, drilling, sawing,
  scratching, scraping, clamping, retracting, clipping, or similar procedures, without connection
  to any active device, intended to be reused after appropriate cleaning and reprocessing.
  *(Annex VIII, §2.3)*

- **Active therapeutic device** (§2.4): Any active device used to support, modify, replace, or
  restore biological functions or structures for the purpose of treatment or alleviation of an
  illness, injury, or disability.
  *(Annex VIII, §2.4)*

- **Active device intended for diagnosis and monitoring** (§2.5): Any active device used to
  supply information for detecting, diagnosing, monitoring, or treating physiological conditions,
  states of health, illnesses, or congenital deformities.
  *(Annex VIII, §2.5)*

- **Central circulatory system** (§2.6): The following blood vessels — arteriae pulmonales,
  aorta ascendens, arcus aortae, aorta descendens to the bifurcatio aortae, arteriae coronariae,
  arteria carotis communis, arteria carotis externa, arteria carotis interna, arteriae cerebrales,
  truncus brachiocephalicus, venae cordis, venae pulmonales, vena cava superior, vena cava
  inferior.
  *(Annex VIII, §2.6)*

- **Central nervous system** (§2.7): The brain, meninges, and spinal cord.
  *(Annex VIII, §2.7)*

### 1.2 Chapter II — Implementing Rules

These rules govern how the 22 classification rules are applied. They resolve ambiguity
when multiple rules could apply.

> **Source**: Regulation (EU) 2017/745, Annex VIII, Chapter II, Sections 3.1–3.7

**Rule 3.1 — Intended Purpose Governs Classification**
Application of the classification rules shall be governed by the intended purpose of the
devices.
*(Annex VIII, §3.1)*

**Rule 3.2 — Separate Classification for Combinations**
If the device is intended to be used in combination with another device, the classification
rules shall apply separately to each of the devices. Accessories for a medical device and
for a product listed in Annex XVI shall be classified in their own right separately from the
device with which they are used.
*(Annex VIII, §3.2)*

**Rule 3.3 — Software Classification**
Software which drives a device or influences the use of a device shall fall within the same
class as the device. If the software is independent of any other device, it shall be classified
in its own right.
*(Annex VIII, §3.3)*

**Rule 3.4 — Most Critical Use Applies**
If the device is not intended to be used solely or principally in a specific part of the body,
it shall be considered and classified on the basis of the most critical specified use.
*(Annex VIII, §3.4)*

**Rule 3.5 — Highest Class Wins**
If several rules, or if, within the same rule, several sub-rules, apply to the same device
based on the device's intended purpose, the strictest rule and sub-rule resulting in the
higher classification shall apply.
*(Annex VIII, §3.5)*

**Rule 3.6 — Duration Calculation**
In calculating the duration referred to in Section 1, continuous use shall mean: (a) the
entire duration of use of the same device without regard to temporary interruption of use
during a procedure or temporary removal for purposes such as cleaning or disinfection of
the device. Whether the interruption of use or the removal is temporary shall be established
in relation to the duration of the use prior to and after the period when the use is
interrupted or the device removed; and (b) the accumulated use of a device that is intended
by the manufacturer to be replaced immediately with another of the same type.
*(Annex VIII, §3.6)*

**Rule 3.7 — Direct Diagnosis**
A device is considered to allow direct diagnosis when it provides the diagnosis of the
disease or condition in question by itself, or when it provides decisive information for the
diagnosis.
*(Annex VIII, §3.7)*

### 1.3 Chapter III — Classification Rules

#### Non-Invasive Devices (Rules 1–4)

**Rule 1 — Default Non-Invasive (Class I)**
All non-invasive devices are classified as Class I, unless one of the rules set out
hereinafter applies.
*(Annex VIII, Chapter III, Rule 1)*

**Rule 2 — Channelling or Storing Body Fluids/Tissues (Class I–IIb)**

| Condition | Class |
|-----------|-------|
| Intended for channelling or storing blood, body liquids, cells, or tissues, liquids or gases for infusion, administration, or introduction into the body, **if connectable to a Class IIa or higher active device** | **IIa** |
| Intended for storing or channelling **blood or other body liquids or for storing organs, parts of organs, or body cells/tissues** (except blood bags) | **IIa** |
| **Blood bags** | **IIb** |
| All other such devices | **I** |

*(Annex VIII, Chapter III, Rule 2)*

**Rule 3 — Modifying Biological or Chemical Composition (Class IIa–III)**

| Condition | Class |
|-----------|-------|
| Intended for modifying biological or chemical composition of human tissues, cells, blood, other body liquids, or other liquids intended for implantation — **by means of filtration, centrifugation, or exchanges of gas/heat** | **IIa** |
| All other such modification (e.g., non-viable human tissue treatment) | **IIb** |
| **In vitro contact** with human cells, tissues, or embryos that are subsequently implanted or administered | **III** |

*(Annex VIII, Chapter III, Rule 3)*

**Rule 4 — Contact with Injured Skin or Mucous Membrane (Class I–IIb)**

| Condition | Class |
|-----------|-------|
| Mechanical barrier, compression, or absorption of exudates | **I** |
| Intended for use with wounds breaching the dermis that can only heal by secondary intent | **IIb** |
| Principally intended to manage micro-environment of wounds | **IIa** |
| All other cases | **IIa** |

*(Annex VIII, Chapter III, Rule 4)*

#### Invasive Devices (Rules 5–8)

**Rule 5 — Invasive via Body Orifice (Class I–IIb)**

| Duration | General | Exceptions |
|----------|---------|------------|
| Transient | **I** | Connected to active devices in IIa or higher → IIa |
| Short-term | **IIa** | Oral cavity to pharynx, ear canal up to ear drum, nasal cavity → **I** |
| Long-term | **IIb** | Oral/ear/nasal (non-absorbable) → **IIa** |

*(Annex VIII, Chapter III, Rule 5)*

**Rule 6 — Surgically Invasive, Transient Use (Class IIa–III)**

| Condition | Class |
|-----------|-------|
| Default transient surgically invasive | **IIa** |
| Reusable surgical instruments | **I** |
| In direct contact with heart, central circulatory, or central nervous system | **III** |
| Supplies energy as ionizing radiation | **IIb** |
| Has a biological effect or is wholly or mainly absorbed | **IIb** |
| Intended to administer medicinal products by means potentially hazardous given the mode of application | **IIb** |

*(Annex VIII, Chapter III, Rule 6)*

**Rule 7 — Surgically Invasive, Short-term Use (Class IIa–III)**

| Condition | Class |
|-----------|-------|
| Default short-term surgically invasive | **IIa** |
| In direct contact with heart, central circulatory, or central nervous system | **III** |
| Intended to supply energy as ionizing radiation | **IIb** |
| Has a biological effect or is wholly or mainly absorbed | **III** |
| Undergoes chemical change in the body (except teeth) | **IIb** |
| Intended to administer medicinal products | **IIb** |

*(Annex VIII, Chapter III, Rule 7)*

**Rule 8 — Implantable and Long-term Surgically Invasive Devices (Class IIb–III)**

| Condition | Class |
|-----------|-------|
| Default long-term surgically invasive / implantable | **IIb** |
| Placed in teeth (default) | **IIa** |
| In direct contact with heart, central circulatory, or central nervous system | **III** |
| Has biological effect or is wholly or mainly absorbed | **III** |
| Undergoes chemical change in body (except teeth) | **III** |
| Intended to administer medicinal products | **III** |
| Active implantable devices or accessories | **III** |
| Breast implants, surgical meshes, total/partial joint replacements (except ancillary components) | **III** |
| Spinal disc replacement and devices in contact with spinal column (except components) | **III** |

*(Annex VIII, Chapter III, Rule 8)*

#### Active Devices (Rules 9–13)

**Rule 9 — Active Therapeutic Devices (Class IIa–III)**

| Condition | Class |
|-----------|-------|
| Default active therapeutic device intended to exchange or administer energy | **IIa** |
| Energy administration or exchange is potentially hazardous (nature, density, site) | **IIb** |
| Intended to control, monitor, or directly influence performance of Class IIb active therapeutic devices | **IIb** |
| Intended to administer ionizing radiation for therapeutic purposes (incl. control/monitoring) | **IIb** |
| Intended to control, monitor, or directly influence performance of active implantable devices | **III** |

*(Annex VIII, Chapter III, Rule 9)*

**Rule 10 — Active Devices for Diagnosis and Monitoring (Class I–IIb)**

| Condition | Class |
|-----------|-------|
| Intended to supply energy to be absorbed by human body (except illumination with visible light) | **IIa** |
| Intended to image in-vivo distribution of radiopharmaceuticals | **IIa** |
| Intended to allow direct diagnosis or monitoring of vital physiological processes | **IIa** |
| Specifically intended for monitoring of vital physiological parameters where variations could result in **immediate danger** to the patient | **IIb** |
| Intended for use in direct diagnosis of clinical conditions, taken in clinical emergency settings | **IIb** |
| Active device to emit ionizing radiation for diagnostic or therapeutic interventional radiology | **IIb** |
| All other active diagnostic/monitoring devices | **I** |

*(Annex VIII, Chapter III, Rule 10)*

**Rule 11 — Software (Class I–III)** *(see Section 2 for detailed analysis)*

Software intended to provide information which is used to take decisions with diagnosis or
therapeutic purposes is classified as:

| Condition | Class |
|-----------|-------|
| Decisions may cause **death or irreversible deterioration** of health | **III** |
| Decisions may cause **serious deterioration of health or a surgical intervention** | **IIb** |
| All other diagnostic/therapeutic decision-support software | **IIa** |
| Intended for **monitoring of physiological processes** | **IIa** |
| Monitoring **vital physiological parameters** where variations could result in **immediate danger** | **IIb** |
| **All other software** | **I** |

*(Annex VIII, Chapter III, Rule 11)*

**Rule 12 — Active Devices for Substance Administration/Removal (Class IIa–IIb)**

| Condition | Class |
|-----------|-------|
| Default active device for administering or removing medicinal products, body liquids, or substances | **IIa** |
| Potentially hazardous given the nature of substance, body part, and mode of application | **IIb** |

*(Annex VIII, Chapter III, Rule 12)*

**Rule 13 — All Other Active Devices (Class I)**
All other active devices are classified as Class I.
*(Annex VIII, Chapter III, Rule 13)*

#### Special Rules (Rules 14–22)

**Rule 14 — Incorporating Medicinal Substance (Class III)**
Devices incorporating as integral part a substance which, if used separately, would be
considered a medicinal product (including human blood or plasma derivatives) with ancillary
action to that of the device are classified as Class III.
*(Annex VIII, Chapter III, Rule 14)*

**Rule 15 — Contraception and STD Prevention (Class IIb–III)**

| Condition | Class |
|-----------|-------|
| Contraception or prevention of sexually transmitted diseases (default) | **IIb** |
| Implantable or long-term invasive contraceptive/STD devices | **III** |

*(Annex VIII, Chapter III, Rule 15)*

**Rule 16 — Disinfection of Medical Devices (Class IIa–IIb)**

| Condition | Class |
|-----------|-------|
| Specifically intended for disinfecting, cleaning, rinsing, or hydrating **contact lenses** | **IIb** |
| Specifically for disinfecting or sterilizing **medical devices** | **IIa** |
| Disinfecting solutions/washer-disinfectors specifically for **invasive** medical devices (end point of processing) | **IIb** |

*(Annex VIII, Chapter III, Rule 16)*

**Rule 17 — X-ray Diagnostic Image Recording (Class IIa)**
Devices specifically intended for recording of diagnostic images generated by X-ray
radiation are classified as Class IIa.
*(Annex VIII, Chapter III, Rule 17)*

**Rule 18 — Human or Animal Tissue Utilizing Devices (Class III)**
All devices utilizing or incorporating non-viable tissues or cells of human origin, or
their derivatives, or non-viable tissues or cells of animal origin or their derivatives, are
classified as Class III, unless such devices are manufactured utilizing tissues or cells of
animal origin or their derivatives which are non-viable and are intended to come into contact
only with intact skin.
*(Annex VIII, Chapter III, Rule 18)*

**Rule 19 — Nanomaterial (Class IIa–III)**

| Internal Exposure Potential | Class |
|----------------------------|-------|
| High or medium | **III** |
| Low | **IIb** |
| Negligible | **IIa** |

*(Annex VIII, Chapter III, Rule 19)*

**Rule 20 — Invasive Inhalation Drug Delivery (Class IIa–IIb)**

| Condition | Class |
|-----------|-------|
| Invasive device via body orifice for administering medicinal products by inhalation (default) | **IIa** |
| Mode of action has essential impact on efficacy/safety, or treats life-threatening conditions | **IIb** |

*(Annex VIII, Chapter III, Rule 20)*

**Rule 21 — Absorbed Substances via Body Orifice or Skin (Class IIa–III)**

| Condition | Class |
|-----------|-------|
| Absorbed by or locally dispersed in the human body systemically | **III** |
| Absorbed by stomach or lower gastrointestinal tract | **III** |
| Applied to skin or in nasal or oral cavity — achieving purpose locally | **IIa** |
| All other cases | **IIb** |

*(Annex VIII, Chapter III, Rule 21)*

**Rule 22 — Active Therapeutic with Integrated Diagnostic (Class III)**
Active therapeutic devices with an integrated or incorporated diagnostic function which
significantly determines the patient management by the device (e.g., closed-loop systems or
automated external defibrillators) are classified as Class III.
*(Annex VIII, Chapter III, Rule 22)*

---

## 2. Rule 11 (SaMD) — Detailed Analysis

Rule 11 is the primary classification rule for **Medical Device Software (MDSW)**,
including Software as a Medical Device (SaMD). It was newly introduced in the MDR (no
equivalent existed in the MDD) and has been one of the most debated and complex rules
due to its broad applicability.

> **Source**: Regulation (EU) 2017/745, Annex VIII, Chapter III, Rule 11;
> MDCG 2019-11 Rev.1 (June 2025)

### 2.1 Exact Rule Text

> *"Software intended to provide information which is used to take decisions with diagnosis or
> therapeutic purposes is classified as class IIa, except if such decisions have an impact that
> may cause:*
>
> *— death or an irreversible deterioration of a person's state of health, in which case it is
> in class III; or*
>
> *— a serious deterioration of a person's state of health or a surgical intervention, in which
> case it is classified as class IIb.*
>
> *Software intended to monitor physiological processes is classified as class IIa, except if it
> is intended for monitoring of vital physiological parameters, where the nature of variations of
> those parameters is such that it could result in immediate danger to the patient, in which case
> it is classified as class IIb.*
>
> *All other software is classified as class I."*
>
> — Regulation (EU) 2017/745, Annex VIII, Rule 11

### 2.2 IMDRF-Aligned Classification Matrix (MDCG 2019-11)

MDCG 2019-11 (original 2019; Rev.1 June 2025) maps the IMDRF N12 risk categorization
framework onto Rule 11 using a two-axis matrix:

- **Axis 1 — Significance of Information**: What does the SaMD do with the clinical information?
  - **Treat or Diagnose**: Information is used to take action (treatment/diagnosis decisions)
  - **Drive Clinical Management**: Information drives clinical management but does not directly
    diagnose or treat
  - **Inform Clinical Management**: Information informs but does not determine clinical
    management decisions

- **Axis 2 — Severity of Patient Condition**: What is the severity if the information is
  incorrect or the software malfunctions?
  - **Critical**: Death or irreversible deterioration of health
  - **Serious**: Serious deterioration of health or surgical intervention
  - **Non-serious**: Non-serious deterioration of health

**Classification Matrix**:

| Significance \ Severity | Critical | Serious | Non-serious |
|------------------------|----------|---------|-------------|
| **Treat or Diagnose** | **III** | **IIb** | **IIa** |
| **Drive Clinical Management** | **IIb** | **IIa** | **IIa** |
| **Inform Clinical Management** | **IIa** | **IIa** | **I** |

> **Source**: MDCG 2019-11 Rev.1, Section 4.2, Table 2; aligned with IMDRF/SaMD WG/N12 FINAL:2014

**Monitoring Branch** (Rule 11, second paragraph):

| Function | Class |
|----------|-------|
| Monitor physiological processes (general) | **IIa** |
| Monitor vital physiological parameters with variations posing immediate danger | **IIb** |

**All Other Software**: Class **I**

### 2.3 Practical Classification Examples

| Software Type | Class | Rationale |
|--------------|-------|-----------|
| AI diagnosing malignant tumours | III | Treat/Diagnose × Critical (death possible) |
| Software predicting sepsis risk in ICU | III | Treat/Diagnose × Critical |
| Triage algorithm directing ER patient flow | IIb | Treat/Diagnose × Serious (surgical intervention possible) |
| Decision-support for drug dosing (non-life-threatening) | IIa | Treat/Diagnose × Non-serious |
| ECG analysis detecting arrhythmias (not life-threatening) | IIa | Drive × Serious |
| Continuous vital-sign monitor (ICU, immediate danger) | IIb | Monitoring branch — vital parameters |
| Activity tracker providing general wellness info | I | All other software |
| Hospital workflow management software | Not MDSW | Not a medical device |

> **Source**: MDCG 2019-11 Rev.1, Section 5, Examples; MDCG 2021-24, Section 3.3

### 2.4 Key Interpretive Issues

1. **Implementing Rule 3.5 applies**: When multiple sub-rules of Rule 11 could apply, the
   strictest classification wins. *(Annex VIII, §3.5)*

2. **Implementing Rule 3.3 — SiMD vs. SaMD**: Software driving a device inherits the device
   classification. Only independent software is classified under Rule 11 in its own right.
   *(Annex VIII, §3.3)*

3. **"Intended purpose" is decisive**: The manufacturer's stated intended purpose (not just
   technical capability) determines classification. Overly broad claims can inadvertently
   increase classification. *(MDCG 2019-11 Rev.1, Section 3)*

4. **Prognosis and prediction**: MDCG 2019-11 Rev.1 clarifies that software providing clinical
   prognosis or prediction falls under the "Treat or Diagnose" significance level, which
   tends toward Class IIb or III. *(MDCG 2019-11 Rev.1, Section 4.2)*

---

## 3. MDCG Guidance Documents

### 3.1 MDCG 2019-11 Rev.1 — Qualification and Classification of Software (June 2025)

Published 17 June 2025, this revision of the original 2019 guidance provides the primary
framework for determining whether software qualifies as MDSW and how to classify it.

> **Source**: [MDCG 2019-11 Rev.1](https://health.ec.europa.eu/latest-updates/update-mdcg-2019-11-rev1-qualification-and-classification-software-regulation-eu-2017745-and-2025-06-17_en)

**Key updates in Rev.1**:

- **Medical Device AI (MDAI)**: First formal introduction of the term "Medical Device Artificial
  Intelligence" (MDAI) as a defined subset of MDSW, acknowledging AI-specific regulatory
  considerations under both MDR and AI Act.

- **Modular software**: Reinforced that each module's intended purpose must be clearly defined
  and documented independently. Each module may have a different classification.

- **Rule 11 enhanced interpretation**: Expanded examples of MDSW classifications, including
  references to software that informs clinical prognosis or prediction. This subtly broadens
  the types of MDSW falling under higher risk classes.

- **European Health Data Space (EHDS)**: Clarifications on Annex XVI devices and interoperability
  with Electronic Health Record (EHR) systems under the EHDS Regulation.

- **Intended purpose emphasis**: Heightened emphasis on clear, unambiguous intended purpose
  statements to prevent misqualification or misclassification.

### 3.2 MDCG 2021-24 — Guidance on Classification of Medical Devices (October 2021)

This guidance provides comprehensive Rule-by-Rule interpretation across all 22 classification
rules, including worked examples.

> **Source**: [MDCG 2021-24](https://health.ec.europa.eu/document/download/b45335c5-1679-4c71-a91c-fc7a4d37f12b_en)

**Key contributions**:

- Software explicitly defined as an "Active Device" under the MDR framework
- Expanded definitions of "Active Therapeutic" and "Active Diagnostic and Monitoring" devices
- Expanded definition of "Devices with a Measuring Function"
- Rule 11 classification must consider intended purpose, intended population (including diseases),
  context of use (ICU, emergency, home), and the nature of decisions enabled by the software
- Companion document to MDCG 2019-11 for software-specific classification

### 3.3 MDCG 2025-6 / AIB 2025-1 — Interplay between MDR/IVDR and AI Act (June 2025)

The first-ever **joint guidance** issued by the Medical Device Coordination Group (MDCG) and
the newly established European Artificial Intelligence Board (AIB).

> **Source**: [AIB 2025-1 / MDCG 2025-6](https://health.ec.europa.eu/document/download/b78a17d7-e3cd-4943-851d-e02a2f22bbb4_en?filename=mdcg_2025-6_en.pdf)

**Key topics**:

- **High-risk MDAI definition**: Clarifies what qualifies as high-risk Medical Device AI under
  the AI Act — specifically AI systems that are intended to be used as safety components of
  medical devices or that are themselves medical devices requiring third-party conformity
  assessment (per AI Act Article 6(1)).

- **Dual compliance framework**: Manufacturers must satisfy both MDR QMS requirements (Annex IX/XI)
  and AI Act requirements (risk management, data governance, transparency, human oversight,
  robustness, cybersecurity) simultaneously.

- **Clinical evaluation for MDAI**: Clinical and performance evaluations must account for the
  dynamic nature of AI — not just initial performance, but real-world variability across diverse
  patient populations, limitations under specific conditions, and adaptation over time.

- **Bias mitigation**: Specific requirements for identifying and mitigating algorithmic bias in
  training data, validation data, and real-world deployment.

- **Notified Body role**: NBs assessing MDAI under MDR also cover AI Act requirements through
  the conformity assessment process, avoiding duplicative audits where possible.

### 3.4 MDCG 2025-9 — Guidance on Breakthrough Devices (BtX) (December 2025)

Introduces a structured EU framework for accelerated access to breakthrough medical devices
and IVDs.

> **Source**: [MDCG 2025-9](https://health.ec.europa.eu/document/download/edca94c7-62ab-4dd5-8539-2b347bd14809_en?filename=mdcg_2025-9.pdf)

**Key elements**:

- **Definition**: Breakthrough devices must demonstrate both (a) a high degree of innovation and
  (b) an expected significant positive clinical impact on life-threatening or irreversibly
  debilitating conditions, or address unmet medical needs. Criteria are cumulative.

- **Scope**: Applies across all technologies and risk classifications. Excludes custom-made
  devices, in-house devices, and Annex XVI products without an intended medical purpose.

- **Benefits**: Priority scientific advice from EMA expert panels, structured dialogue with
  Notified Bodies, and possibility of certification with specific post-market conditions.

- **Clinical evidence**: Rebalancing between pre-market and post-market data — sufficient base of
  clinical evidence for safety and expected benefit, supplemented by reinforced PMS/PMCF designed
  from the start.

- **Pilot timeline**: Implementation pilot project scheduled for Q2 2026.

---

## 4. Conformity Assessment — Article 52

Article 52 of the MDR prescribes the conformity assessment routes by device class. The routes
determine the extent of Notified Body (NB) involvement.

> **Source**: Regulation (EU) 2017/745, Article 52;
> [MDR Article 52 text](https://www.medical-device-regulation.eu/2019/07/11/mdr-article-52-conformity-assessment-procedures/)

### 4.1 Routes by Device Class

| Device Class | NB Involvement | Primary Route | Alternative Route |
|-------------|---------------|---------------|-------------------|
| **Class I** (non-sterile, non-measuring, non-reusable surgical) | **None** — self-declaration | Technical documentation (Annexes II + III) → EU Declaration of Conformity | N/A |
| **Class I** (sterile, measuring function, or reusable surgical instruments) | **Limited** — NB for specific aspects only | Annex IX, Chapters I + III (QMS + specific aspects) | Annex XI, Part A (production quality assurance) |
| **Class IIa** | **Required** — NB assessment of representative device | Annex IX, Chapters I + III (QMS) + at least one representative device from each category assessed per Section 4 | Annexes II + III + Annex XI Part A §10 (production QA) or Part B §18 (product verification) |
| **Class IIb** | **Required** — NB assessment per generic device group | Annex IX, Chapters I + III + Section 4 assessment of at least one representative device per **generic device group** | Annexes II + III + Annex XI Part A §10 or Part B §18 |
| **Class IIb implantable** (except sutures, staples, dental fillings, braces, crowns, screws, wedges, plates, wires, pins, clips, connectors) | **Required** — NB assessment of **every** device | Annex IX, with Section 4 assessment for **every** device | Same as Class IIb |
| **Class III** | **Full** — NB comprehensive assessment | Annex IX (full QMS + technical documentation assessment) | Annex X (type-examination) + Annex XI (production quality assurance) |

*(Article 52, paragraphs 1–7)*

### 4.2 Annex Reference Summary

| Annex | Title | Applies to |
|-------|-------|-----------|
| **Annex I** | General Safety and Performance Requirements (GSPR) | All classes |
| **Annex II** | Technical Documentation | All classes |
| **Annex III** | Technical Documentation on Post-Market Surveillance | All classes |
| **Annex IX** | Conformity Assessment Based on a Quality Management System and Assessment of Technical Documentation | Class IIa, IIb, III (primary route) |
| **Annex X** | Conformity Assessment Based on Type-Examination | Class III (alternative) |
| **Annex XI** | Conformity Assessment Based on Product Conformity Verification | Class IIa, IIb, III (alternative); Class I sterile/measuring |
| **Annex XIV** | Clinical Evaluation and Post-Market Clinical Follow-Up | All classes |

### 4.3 Article 54 — Clinical Evaluation Consultation Procedure (CECP)

For certain high-risk devices, the Notified Body must consult an independent expert panel
before issuing a certificate.

> **Source**: Regulation (EU) 2017/745, Article 54;
> [Second Report on CECP (2024)](https://www.emergobyul.com/news/second-report-european-clinical-evaluation-consultation-procedure-cecp)

**Scope of CECP (mandatory consultation)**:
- **Class III implantable devices**
- **Class IIb active devices** intended to administer and/or remove a medicinal product
  (ARMP devices)

**Process**:
1. NB prepares a Clinical Evaluation Assessment Report (CEAR)
2. NB submits CEAR to the relevant expert panel via EUDAMED
3. Screening panel reviews within **21 days** and decides if full consultation is needed
4. If yes, expert panel delivers scientific opinion within **60 days**
5. NB must give "due consideration" to the opinion; if deviating, must provide justification

**Exemptions**: The most common exemption (99.1% of cases in the 2024 report) is modification
of a device already marketed by the same manufacturer for the same intended purpose, where
modifications do not adversely affect the benefit-risk ratio.

---

## 5. AI Act Intersection

The EU Artificial Intelligence Act (Regulation (EU) 2024/1860), which entered into force on
1 August 2024, creates a parallel regulatory layer for AI systems used in medical devices.

> **Source**: Regulation (EU) 2024/1860, Articles 6, 9–15, Annex I;
> MDCG 2025-6 / AIB 2025-1

### 5.1 Automatic High-Risk Classification — Article 6(1)

Under Article 6(1), an AI system is automatically classified as **high-risk** if:
1. It is intended to be used as a **safety component** of a product, OR is itself a product, AND
2. The product is covered by EU harmonisation legislation listed in Annex I (which includes
   the MDR 2017/745 and IVDR 2017/746), AND
3. It is required to undergo a **third-party conformity assessment** under that legislation.

**Practical implication**: Any AI-enabled MDSW classified as Class IIa or higher under the MDR
automatically qualifies as high-risk under the AI Act, because these classes require NB
involvement (third-party conformity assessment).

**Exception**: Class I software (including sterile/measuring) that does not require NB involvement
for its AI component would not automatically be high-risk under Article 6(1).

### 5.2 Additional Requirements for High-Risk MDAI

High-risk AI systems under the AI Act must satisfy requirements in Articles 9–15:

| AI Act Requirement | Article | MDR Alignment |
|-------------------|---------|--------------|
| Risk management system | Art. 9 | Aligns with Annex I GSPR §3 (risk management per ISO 14971) |
| Data governance | Art. 10 | Partially new — training/validation/test dataset requirements |
| Technical documentation | Art. 11 | Aligns with Annex II, plus AI-specific additions |
| Record-keeping (logging) | Art. 12 | Partially new — automatic event logging |
| Transparency and information | Art. 13 | Aligns with labelling (Annex I GSPR §23), plus AI-specific disclosure |
| Human oversight | Art. 14 | Partially new — human-in-the-loop requirements |
| Accuracy, robustness, cybersecurity | Art. 15 | Aligns with Annex I GSPR §17 (cyber), plus new robustness requirements |

> **Source**: MDCG 2025-6, Sections 3–5

### 5.3 Timeline

| Date | Milestone |
|------|-----------|
| 1 August 2024 | AI Act enters into force |
| 2 February 2025 | Prohibited AI practices apply |
| 2 August 2025 | GPAI model obligations and governance provisions apply |
| **2 August 2027** | **High-risk AI system requirements fully applicable** — all AI-enabled medical devices must demonstrate simultaneous MDR + AI Act compliance |

> **Source**: AI Act, Article 113 (entry into force and application dates)

### 5.4 December 2025 Simplification Proposal Impact on AI Classification

The European Commission's December 2025 proposal (COM(2025) 1023) to amend the MDR includes
a proposed revision of Rule 11 that would allow more MDSW to be classified as Class I. If
enacted, this could **reduce the number of AI-enabled MDSW classified as high-risk** under the
AI Act, because Class I devices generally do not require third-party conformity assessment and
thus would not trigger Article 6(1).

> **Source**: [COM(2025) 1023](https://health.ec.europa.eu/document/download/25e7ea7c-cab3-40cf-86d9-d11f5e7744d8_en?filename=md_com_2025-1023_act_en.pdf)

---

## 6. Transition Timeline & Recent Regulatory Changes

### 6.1 Regulation (EU) 2023/607 — Extended Transition Deadlines

Regulation 2023/607, adopted on 20 March 2023, amended Article 120 of the MDR to extend the
transition period for legacy MDD/AIMDD devices.

> **Source**: Regulation (EU) 2023/607;
> [EC MDR transition page](https://health.ec.europa.eu/medical-devices-sector/new-regulations_en)

**Extended deadlines**:

| Device Category | New Deadline | Condition |
|----------------|-------------|-----------|
| Class III and Class IIb implantable devices | **31 December 2027** | Application filed with NB by 26 May 2024; QMS + NB agreement by 26 Sep 2024 |
| All other Class IIb, IIa, and Is/Im devices | **31 December 2028** | Same conditions as above |
| Class I devices not requiring NB under MDD | **31 December 2028** | Must comply with MDR Annex I GSPR + PMS/vigilance |
| Custom-made Class III devices | **26 May 2026** | Cannot rely on extended deadlines |

**Sell-off clause**: The previous MDD requirement to sell off stock by a fixed deadline has been
removed by Regulation 2023/607.

### 6.2 EUDAMED Mandatory Modules — 28 May 2026

On 27 November 2025, the European Commission confirmed via the Official Journal (OJEU) that
four EUDAMED modules are technically functional and will become mandatory.

> **Source**: [EC EUDAMED Notice (Nov 2025)](https://health.ec.europa.eu/latest-updates/eudamed-four-first-modules-will-be-mandatory-use-28-may-2026-2025-11-27_en)

**Mandatory modules from 28 May 2026**:
1. **Actor Registration** — all economic operators (manufacturers, ARs, importers, sponsors)
2. **UDI/Device Registration** — all MDR/IVDR devices (except custom-made, investigational)
3. **Notified Bodies and Certificates** — NB and certificate data
4. **Market Surveillance** — coordination between competent authorities

**Key deadlines**:

| Action | Deadline |
|--------|----------|
| Actor registration | 28 May 2026 |
| New device registration (devices placed on market from 28 May 2026) | Before first unit placed on EU market |
| Legacy device registration (placed on market before 28 May 2026) | 28 November 2026 |
| Certificate upload (certificates issued before 28 May 2026) | 28 May 2027 |

### 6.3 December 2025 Proposal to Simplify MDR/IVDR — COM(2025) 1023

On 16 December 2025, the European Commission published a legislative proposal to amend the MDR
and IVDR. This is a **proposal** — not yet adopted — that must go through ordinary legislative
procedure in the European Parliament and Council.

> **Source**: [COM(2025) 1023](https://health.ec.europa.eu/publications/proposal-regulation-simplify-rules-medical-and-vitro-diagnostic-devices_en);
> [EC announcement (Dec 2025)](https://www.insideeulifesciences.com/2025/12/16/european-commission-announces-long-awaited-proposal-to-simplify-eu-medical-device-regulations/)

**Key proposed changes**:

- **Rule 11 amendment**: Allow a broader range of MDSW to be classified as **Class I**, including
  many patient self-management apps currently classified as IIa. New criteria: "serious" or
  "critical" situations as triggers for higher classification (IIa/IIb/III).

- **Software cybersecurity**: New specific provisions reinforcing Annex I GSPR §17 for connected
  MDSW cybersecurity requirements.

- **Streamlined conformity assessment**: Simplification of NB procedures for certain device
  categories.

- **AI Act alignment**: Explicit cross-references to harmonize MDR and AI Act requirements for
  MDAI.

### 6.4 Notified Body Capacity

The limited number of designated Notified Bodies remains a significant implementation challenge
for the MDR ecosystem.

> **Source**: [EU NB Survey 2025](https://www.pureglobal.com/news/eu-notified-bodies-survey-2025-on-mdr-and-ivdr-certifications-and-applications);
> [20th NB designated under MDR](https://www.emergobyul.com/news/20th-notified-body-designated-under-eu-mdr-while-ivdr-designations-lag)

**Current status (as of February 2025)**:

| Metric | Value |
|--------|-------|
| Designated NBs under MDR | **51** |
| Total certification applications | ~28,500 |
| Certificates granted | ~12,000 (43% of applications) |
| Average certification timeline | **13–18 months** per application |
| Projected NBs by end of 2027 | ~85 |
| Projected NBs by end of 2028 | 100+ |

**Implications for SaMD manufacturers**: The NB capacity shortage means that manufacturers
should file applications well in advance of transition deadlines. The December 2025 proposal
to allow more software into Class I (no NB needed) would partially alleviate this bottleneck.

---

## 7. Summary — EU MDR Classification Decision Path for SaMD

```
Is the software a medical device (MDSW)?
├── No → Not regulated under MDR
└── Yes → Apply Rule 11
    ├── Provides diagnostic/therapeutic decision information?
    │   ├── Decisions may cause death / irreversible health deterioration → CLASS III
    │   ├── Decisions may cause serious health deterioration / surgical intervention → CLASS IIb
    │   └── Other diagnostic/therapeutic decisions → CLASS IIa
    ├── Monitors physiological processes?
    │   ├── Vital parameters with immediate danger risk → CLASS IIb
    │   └── Other physiological monitoring → CLASS IIa
    └── All other software → CLASS I

Apply Implementing Rule 3.5: If multiple sub-rules apply → highest class wins
Apply Implementing Rule 3.3: If software drives another device → inherits device class
```

**Post-classification steps**:

1. Determine conformity assessment route (Article 52) based on class
2. Check if CECP applies (Article 54) — Class III implantable or Class IIb ARMP
3. Assess AI Act high-risk status (Article 6(1)) — Class IIa+ with AI = high-risk
4. Prepare for EUDAMED registration (mandatory 28 May 2026)
5. Monitor proposed Rule 11 amendments (COM(2025) 1023)
