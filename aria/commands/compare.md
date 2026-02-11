---
description: Multi-country regulation comparison - Compares regulatory requirements across FDA, EU MDR, and MFDS
argument-hint: "규제 주제 또는 요구사항 영역, 대상 국가 [--lang ko|en]"
---

# /aria:compare - Multi-Country Regulatory Comparison

## Purpose

Compare regulatory requirements across multiple countries (FDA/US, EU MDR/Europe, MFDS/Korea) for specific regulatory topics. Identify similarities, differences, harmonized standards, and develop multi-market strategies.

## Workflow

### 1. Product Context Loading

- Load active product from `.aria/active_product.json`
- If multiple products exist, prompt for selection
- If no products exist, create new product entry

### 2. Prior Context Check (Optional)

- Check `.aria/products/{product-name}/{date}/` for prior pipeline data
- Classification results inform comparison focus areas
- Pathway selection informs regional submission context
- Use prior context when available, proceed without it otherwise

### 3. Input Collection

**Comparison Topic Examples**:
- "임상 증거 요구사항" (Clinical evidence requirements)
- "품질 시스템 규제" (Quality system requirements)
- "시판 후 조사" (Post-market surveillance)
- "라벨링 및 IFU" (Labeling and IFU)
- "기술 문서" (Technical documentation)
- "위해성 관리" (Risk management)

**Target Countries** (default: FDA, EU MDR, MFDS):
- User can specify subset or additional regions
- Default covers all three primary regions

### 4. Comparison Analysis

- Activate comparison skill with specified topic and countries
- Apply multi-region comparison framework
- Generate side-by-side comparison matrix
- Identify harmonized standards (ISO 13485, ISO 14971, IEC standards)
- Highlight key regulatory differences
- Formulate strategic recommendations (harmonized/sequential/parallel approach)

### 5. Output Generation

**Full output** (`comparison.md`):
- Header (command, product, topic, date, version)
- Comparison matrix (per dimension: regulatory basis, requirements, timing, verification)
- Harmonized standards section
- Key differences section
- Strategic recommendations
- Traffic light assessment
- Next steps
- Disclaimer

**Compressed summary** (`comparison.summary.md`):
- Topic, countries, traffic light, key differences, recommended strategy

### 6. Next Steps

- **Primary**: `/aria:brief` (if ready to generate comprehensive briefing)
- **Alternative**: Additional comparison topics (if multi-topic analysis needed)
- **Optional**: Expert review (if YELLOW or RED traffic light)

## Flags

- `--lang en|ko`: Output language (default: `ko`)

## Output Location

- `.aria/products/{product-name}/{date}/comparison.md`
- `.aria/products/{product-name}/{date}/comparison.summary.md`

## Data Sources

Built-in regulatory comparison frameworks for FDA, EU MDR, MFDS are the primary source. Prior pipeline data (classification, pathway) supplements the analysis when available. External data connectors (Notion, Context7) are used only when configured.

## Example

```
/aria:compare 임상 증거 요구사항
```
> System loads comparison topic: Clinical evidence requirements
> System generates multi-country comparison matrix for FDA, EU MDR, MFDS
> System outputs comparison with harmonized standards and strategic recommendations

```
/aria:compare --lang en Post-market surveillance requirements
```
> English output for post-market surveillance comparison across three regions

## Disclaimer

**Important Notice**

This comparison is an AI-based regulatory intelligence analysis, not official regulatory advice.

- **No legal effect**: Results are for reference only and have no legal binding force
- **Expert review required**: Regulatory affairs professional review is mandatory before actual regulatory strategy implementation
- **Regulatory authority confirmation**: Each region's specific requirements must be verified with current regulations
- **Limitation of liability**: Users are responsible for regulatory non-compliance resulting from use of this tool

Knowledge Base Date: 2026-01

---

This is reference information for professional review, not regulatory advice.
