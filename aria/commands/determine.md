---
description: Medical device determination - Evaluates whether a product qualifies as a medical device under FDA, EU MDR, and MFDS regulations
argument-hint: "Product description or technical document [--lang en|ko]"
---

# /aria:determine - Medical Device Determination

## Purpose

Evaluate whether your product qualifies as a medical device under US FDA, EU MDR, and Korea MFDS regulations. Identifies borderline cases and prepares for classification.

## Workflow

### 1. Product Context Loading

- Load active product from `.aria/active_product.json`
- If multiple products exist, prompt for selection
- If no products exist, create new product entry

### 2. Input Collection

**If technical document provided**:
- Extract device description, intended use, product form, primary function
- Large documents (>100 pages): Analyze TOC first, extract relevant sections
- Gap detection + targeted Q&A for missing fields (max 1-3 rounds)

**If no document provided**:
- Conversational Q&A: device description, intended use, product form, primary function

### 3. Prior Context Check

- Check `.aria/products/{product-name}/{date}/` for existing data
- If exists: Offer versioned output (`determination-v2.md`)

### 4. Determination Analysis

- Activate determination skill
- Evaluate against FDA, EU MDR, MFDS criteria
- Apply traffic light system and identify escalation scenarios

### 5. Output Generation

**Full output** (`determination.md`):
- Header (command, product, date, version)
- Input summary
- Determination checklist (FDA, EU MDR, MFDS status)
- Traffic light assessment with rationale
- Escalation recommendations (if applicable)
- Next steps
- Disclaimer

**Compressed summary** (`determination.summary.md`):
- Decision, Traffic Light, per-region status, key factors, escalation status

### 6. Next Steps

- **Primary**: `/aria:classify` (if device = YES)
- **Alternative**: Expert review (if CONDITIONAL)
- **Optional**: Document amendment (if missing info)

## Flags

- `--lang en|ko`: Output language (default: `ko`)

## Output Location

- `.aria/products/{product-name}/{date}/determination.md`
- `.aria/products/{product-name}/{date}/determination.summary.md`

## Data Sources

Built-in regulatory knowledge is the primary source. Detailed criteria are available in skill modules for deep analysis. External data connectors (Notion, etc.) are used only when configured — see plugin documentation for setup.

## Example

```
/aria:determine
```
> System asks for device description, intended use, product form
> User provides details conversationally
> System generates determination result with traffic light assessment

## Disclaimer

**Important Notice**

This determination is an AI-based regulatory intelligence analysis, not official regulatory advice.

- **No legal effect**: Results are for reference only and have no legal binding force
- **Expert review required**: Regulatory affairs professional review is mandatory before actual regulatory submission
- **Regulatory authority confirmation**: Final determination follows official decisions by FDA, Notified Body, MFDS, etc.
- **Limitation of liability**: Users are responsible for regulatory non-compliance resulting from use of this tool

Knowledge Base Date: 2026-01

---

This is reference information for professional review, not regulatory advice.
