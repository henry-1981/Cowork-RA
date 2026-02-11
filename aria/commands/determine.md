---
description: Medical device determination - Evaluates whether a product qualifies as a medical device under FDA, EU MDR, and MFDS regulations
argument-hint: "Product description or technical document [--lang en|ko]"
---

# /aria:determine - Medical Device Determination

## Purpose

This command evaluates whether your product qualifies as a medical device under target regulations (US FDA, EU MDR, Korea MFDS).

Use this command to:
- Determine if your product falls under medical device regulatory scope
- Understand which regulations apply to your product
- Identify borderline cases requiring expert review
- Prepare for classification and regulatory pathway decisions

## Workflow

### 1. Product Context Loading
- Load active product from `.aria/active_product.json`
- If multiple products exist, prompt for selection
- If no products exist, create new product entry

### 2. Input Collection (Document-First Workflow)

**If technical document provided**:
- Extract device description, intended use, product form, primary function
- If large document (>100 pages): Analyze Table of Contents first, extract relevant sections
- If no TOC: Analyze first/last 2000 tokens, search for key sections
- Gap detection: Identify missing required fields
- Targeted Q&A: Ask only for genuinely missing fields (max 1-3 rounds)

**If no document provided**:
- Conversational Q&A to collect:
  - Device description (what is it?)
  - Intended use statement (medical purpose?)
  - Product form (hardware, software, IVD, combination?)
  - Primary function (how does it work?)

### 3. Prior Context Check
- Check `.aria/products/{product-name}/{date}/` for existing determination data
- If exists: Load and offer to create versioned output (`determination-v2.md`)

### 4. Determination Analysis
- Activate determination skill (references `skills/determination/SKILL.md`)
- Evaluate against FDA 21 CFR 201(h) criteria
- Evaluate against EU MDR Article 2(1) criteria
- Evaluate against MFDS device criteria
- Apply traffic light system (GREEN/YELLOW/RED)
- Identify escalation scenarios (borderline cases)

### 5. Output Generation
- **Full output**: `determination.md`
  - Header (command, product, date, version)
  - Input summary
  - Determination checklist (FDA, EU MDR, MFDS status)
  - Traffic light assessment
  - Data source attribution
  - Escalation recommendations (if applicable)
  - Next steps (1-3 suggestions)
  - Disclaimer block

- **Compressed summary**: `determination.summary.md` (Key-Value Markdown format, ~500 tokens)
  ```markdown
  - **Decision**: [YES/NO/CONDITIONAL]
  - **Traffic Light**: [GREEN/YELLOW/RED]
  - **FDA Status**: [Device/Non-device/Conditional]
  - **EU MDR Status**: [Device/Non-device/Conditional]
  - **MFDS Status**: [Device/Non-device/Conditional]
  - **Key Factors**: [Primary factors affecting determination]
  - **Escalation**: [Yes/No + reason]
  - **Sources**: [Data sources: Notion/Built-in/Context7]
  ```

### 6. Next Steps
Suggest 1-3 next commands based on determination result:
- **Primary**: `/aria:classify` (if device status = YES)
- **Alternative**: Expert review consultation (if status = CONDITIONAL)
- **Optional**: Document review and amendment (if missing information)

## Flags

- `--lang en|ko`: Output language (default: `ko` from aria.local.md or system default)

## Output Location

- **Full output**: `.aria/products/{product-name}/{date}/determination.md`
- **Compressed summary**: `.aria/products/{product-name}/{date}/determination.summary.md`

## Data Sources

The determination analysis uses a three-tier data priority system:

1. **Notion DB** (Priority 1): Organization-specific regulatory precedents and device determinations
2. **Built-in Knowledge** (Priority 2): Embedded decision frameworks from FDA, EU MDR, MFDS regulations
3. **Context7** (Priority 3): Supplementation and verification from regulatory documentation libraries

If Notion DB is unavailable, the system gracefully degrades to built-in knowledge with Context7 supplementation.

## Traffic Light System

- **GREEN**: Clear medical device status across all three regions (FDA, EU MDR, MFDS agree)
- **YELLOW**: Borderline/conditional status; requires regulatory specialist review before proceeding
- **RED**: Not a medical device; product outside regulatory scope

## Escalation Scenarios

YELLOW or RED traffic lights trigger escalation recommendations:
- **Wellness vs Medical Device**: Borderline products with both wellness and medical claims
- **Combination Products**: Products combining device and drug/biologic components
- **Novel Device Types**: New technologies without clear regulatory precedent

## Example Usage

### Example 1: Document-First Input
```
/aria:determine [Upload technical specification PDF]
```
→ System extracts device description, intended use, product form from document
→ Asks targeted questions only for missing fields
→ Generates determination result

### Example 2: Conversational Input
```
/aria:determine
```
→ System: "What is the device description?"
→ User: "Wearable heart rate monitor with arrhythmia detection"
→ System: "What is the intended use?"
→ User: "Detect and alert users to irregular heart rhythms"
→ System: [Continues Q&A for missing fields]
→ Generates determination result

### Example 3: Korean Output
```
/aria:determine --lang ko
```
→ All output generated in Korean language

## Disclaimer

⚠️ **중요 고지사항**

본 판정 결과는 AI 기반 regulatory intelligence tool의 분석이며, 공식적인 규제 자문이 아닙니다.

- **법적 효력 없음**: 본 결과는 참고용이며 법적 구속력이 없습니다
- **전문가 검토 필수**: 실제 규제 제출 전 regulatory affairs 전문가 검토가 반드시 필요합니다
- **규제 기관 확인**: 최종 판정은 FDA, Notified Body, MFDS 등 규제 기관의 공식 결정을 따릅니다
- **책임 한계**: 본 도구 사용으로 인한 규제 미준수 책임은 사용자에게 있습니다

Knowledge Base Date: 2026-01 기준

---

This is reference information for professional review, not regulatory advice. All regulatory decisions must be validated by qualified regulatory affairs professionals.
