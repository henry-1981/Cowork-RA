# Annex XVI Detection (Non-Medical Purpose Devices)

## Trigger Conditions

When ANY of the following are detected in the product description:
- Device without intended medical purpose (cosmetic, aesthetic, wellness with no medical claim)
- Product listed in Annex XVI categories: contact lenses (non-corrective), laser equipment (skin treatment), dermal fillers, liposuction/lipoplasty/lipectomy equipment, intense pulsed light equipment, brain stimulation equipment

## Mandatory Output

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

## Key Principle

Annex XVI devices require **dual determination**:
1. Article 2(1) assessment → typically NO (no medical purpose)
2. Annex XVI assessment → YES (listed non-medical purpose device)
3. Result: Device IS within MDR scope despite not being a "medical device" per Article 2(1) → use **SPECIAL** or **IN SCOPE** determination status (NOT "YES")
