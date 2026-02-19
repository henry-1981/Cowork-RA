# EU MDR Device Determination Criteria (Article 2(1))

## Definition

"Medical device" means any instrument, apparatus, appliance, software, implant, reagent, material or other article intended by the manufacturer to be used, alone or in combination, for human beings for one or more of the following specific medical purposes:

- Diagnosis, prevention, monitoring, prediction, prognosis, treatment or alleviation of disease
- Diagnosis, monitoring, treatment, alleviation of, or compensation for, an injury or disability
- Investigation, replacement or modification of the anatomy or of a physiological or pathological process or state
- Providing information by means of in vitro examination of specimens derived from the human body, including organ, blood and tissue donations

**Legal basis**: Regulation (EU) 2017/745, Article 2(1)

## Gate 1A: Medical Purpose Check (Article 2(1))

### Decision Tree

```
Does the manufacturer intend the product for a specific medical purpose listed in Art. 2(1)?
├─ YES (clear medical purpose) → YES — medical device → Proceed to classification
├─ NO (no medical purpose) → Check Gate 1B (Annex XVI)
└─ UNCERTAIN → CONDITIONAL assessment below
```

### CONDITIONAL Assessment (Borderline Products)

**Reference**: MDCG 2019-11 rev.1 "Guidance on Qualification and Classification of Software"

When the product's medical purpose is uncertain, evaluate:

```
Borderline assessment:
├─ Product makes wellness/lifestyle claims BUT:
│   ├─ Functions could foreseeably be used for medical purpose → CONDITIONAL (likely YES)
│   │   EU MDR Art. 2(1) considers "foreseeable use" not just intended use
│   ├─ Monitors physiological parameters that indicate disease → CONDITIONAL (likely YES)
│   │   E.g., SpO2 trends, respiratory patterns, heart rhythm irregularities
│   ├─ Suggests user seek medical advice based on data analysis → CONDITIONAL (likely YES)
│   │   Software providing risk assessment or flagging abnormalities
│   └─ Provides only general information without individual assessment → NO
│
├─ Software boundary (MDCG 2019-11):
│   ├─ Performs action on data beyond storage/retrieval/display/communication → likely MDSW
│   ├─ Intended for individual patient benefit → likely MDSW
│   └─ Only provides general reference information → NOT MDSW
│
└─ Key EU-specific principle: EU MDR is STRICTER than FDA on wellness boundary
    - FDA focuses on manufacturer's intended use claims
    - EU MDR also considers "foreseeable use" by users
    - Products that are "wellness" under FDA may be "CONDITIONAL (likely YES)" under EU MDR
```

### CONDITIONAL Output for EU MDR

When determination is CONDITIONAL:
- **Uncertainty basis**: Cite specific MDCG guidance and Art. 2(1) criteria
- **Resolution conditions**: What intended use clarification would resolve
- **If YES scenario**: Classify under Annex VIII rules (likely Rule 11 for software)
- **If NO scenario**: Not subject to EU MDR (unless Annex XVI applies)

## Gate 1B: Annex XVI Check (Non-Medical Purpose)

**When Gate 1A = NO** (no medical purpose):

```
Is the product listed in Annex XVI categories?
├─ Group 1: Contact lenses (non-corrective)
├─ Group 2: Implants for aesthetic modification
├─ Group 3: Substances for facial/dermal filling
├─ Group 4: Equipment for reducing/removing adipose tissue
├─ Group 5: Equipment for brain stimulation (non-medical)
├─ Group 6: Equipment emitting high-intensity radiation for skin treatment
│
├─ YES (matches Annex XVI group) → IN SCOPE
│   Apply: Art. 1(2), Common Specifications (Reg. (EU) 2022/2346)
│   Classification: Apply Annex VIII rules as if medical device
│   Pathway: Notified Body required
│
└─ NO (not in Annex XVI) → EXIT — not subject to EU MDR
```

## Borderline Products Reference

| Product Type | Determination | Key Assessment |
|---|---|---|
| AI diagnostic software | YES | Clear medical purpose (diagnosis) |
| Wellness app (general tips) | NO | No individual patient assessment |
| Sleep monitor with SpO2 alerts | CONDITIONAL (likely YES) | Physiological monitoring with flagging = foreseeable medical use |
| Cosmetic contact lenses | IN SCOPE (Annex XVI) | Non-medical but Annex XVI Group 1 |
| Fitness tracker (steps only) | NO | General wellness, no physiological analysis |
