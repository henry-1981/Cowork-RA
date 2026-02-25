# Combination Product Detection (P5)

## Trigger Conditions

When ANY of the following are detected in the product description:
- Drug-device combination (drug coating, drug-eluting, drug reservoir)
- Biologic-device combination (tissue-derived component, cell therapy + device)
- Device constituent + drug constituent identified separately

## Mandatory Output

Determination MUST be **CONDITIONAL** with additional required fields:

| Field | Description |
|-------|-------------|
| **Combination Type** | Drug-device / Biologic-device / Drug-biologic-device |
| **Device Constituent** | Physical/mechanical component description and function |
| **Drug/Biologic Constituent** | Pharmacological/biological component and its action |
| **PMOA (Primary Mode of Action)** | Which constituent provides the primary therapeutic effect |
| **Lead Center** | CDRH (device PMOA) / CDER (drug PMOA) / CBER (biologic PMOA) |
| **Consultation** | Which other center(s) must be consulted |

## PMOA Determination Logic

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
