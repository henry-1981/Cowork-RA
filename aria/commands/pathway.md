---
description: "Regulatory submission pathway analysis - Identifies optimal pathways for FDA, EU MDR, and MFDS submissions based on classification"
argument-hint: "[Target markets] [--lang en|ko]"
---

# /aria:pathway - Regulatory Pathway Analysis

## Purpose

Identify regulatory submission pathways for FDA, EU MDR, and MFDS based on device classification. Provides pathway recommendations, timeline ranges, and multi-region comparison.

## Workflow

### 1. Product Context Loading

- Load active product from `.aria/active_product.json`
- If multiple products exist, prompt for selection
- If no products exist, display error: "제품을 먼저 생성하거나 선택하세요"

### 2. Classification Data Loading

- Check for classification results: `.aria/products/{product-name}/{date}/classification.summary.md`
- If classification data NOT found:
  - Display warning: **"⚠️ 분류 데이터가 없습니다. 먼저 `/aria:classify` 명령을 실행하세요."**
  - Suggest: Run `/aria:classify` first
  - STOP workflow

### 3. Target Market Selection

- Default: All three markets (FDA, EU MDR, MFDS)
- Optional: User can specify subset (e.g., "FDA and EU only")
- Extract device class/grade from classification summary

### 4. Pathway Analysis

- Activate pathway skill with loaded classification data
- Apply pathway selection logic per region:
  - **FDA**: Exempt, 510(k), De Novo, or PMA based on class and exemption status
  - **EU MDR**: Self-declaration, Notified Body Annex IV/IX/X based on class and device type
  - **MFDS**: 신고 (registration) or 허가 (approval) based on grade
- Identify timeline ranges and key requirements
- Assign traffic light indicator

### 5. Multi-Region Comparison

- Generate comparison table: Region | Pathway | Timeline | Key Requirements
- Identify critical path (longest timeline)
- Highlight shared activities (e.g., common testing)
- Recommend parallel vs. sequential submission strategy

### 6. Output Generation

**Full output** (`pathway.md`):
- Header (command, product, date, version)
- Pathway recommendations per region
- Multi-region comparison table
- Timeline estimates
- Traffic light assessment
- Escalation recommendations (if Class III or clinical study required)
- Next steps
- Disclaimer

**Compressed summary** (`pathway.summary.md`):
- Selected pathways per region
- Timeline ranges
- Critical path
- Traffic light status

### 7. Next Steps

- **Primary**: `/aria:estimate` (cost and timeline estimation)
- **Alternative**: Expert consultation (if YELLOW traffic light)

## Flags

- `--lang en|ko`: Output language (default: `ko`)

## Output Location

- `.aria/products/{product-name}/{date}/pathway.md`
- `.aria/products/{product-name}/{date}/pathway.summary.md`

## Data Sources

Built-in regulatory pathway knowledge (2026-01). References FDA guidance documents, EU MDR Annexes, and MFDS regulations. External data connectors are used only when configured.

## Example

```
/aria:pathway
```

Analyzes all three markets (FDA, EU MDR, MFDS) and generates pathway recommendations based on classification results.

```
/aria:pathway FDA EU
```

Analyzes only US and EU markets, excluding MFDS.

## Dependencies

- **Required**: `/aria:classify` must be executed first
- **Input**: Classification results from `.summary.md`
- **Output**: Pathway recommendations for downstream `/aria:estimate`

## Traffic Light Interpretation

- **🟢 GREEN**: Low-risk pathways (Class I/IIa, Grade 1-2, no clinical trials)
- **🟡 YELLOW**: Moderate-high risk pathways (Class IIb/III, Grade 3-4, De Novo, PMA, clinical trials)

## Notes

- All pathways are based on device classification
- Actual submission requirements may vary based on product specifics
- High-risk devices (Class III, Grade 4) always trigger YELLOW + expert consultation recommendation
- Multi-region submissions benefit from shared testing activities
