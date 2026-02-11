---
description: Device classification - Determines regulatory class across US FDA, EU MDR, and Korea MFDS
argument-hint: "Device characteristics [--optimize] [--lang en|ko]"
---

# /aria:classify - Device Classification

## Purpose

This command determines the regulatory classification of your medical device across target regions:
- **FDA**: Class I (Low), II (Moderate), III (High)
- **EU MDR**: Class I (Low), IIa (Medium-Low), IIb (Medium-High), III (High)
- **MFDS**: Class 1 (낮음), 2 (낮음-중간), 3 (중간-높음), 4 (높음)

Use this command to:
- Determine regulatory class for pathway planning
- Understand classification differences across regions
- Identify classification optimization opportunities (with `--optimize` flag)
- Prepare for regulatory submission strategy

## Workflow

### 1. Product Context Loading
- Load active product from `.aria/active_product.json`
- If multiple products exist, prompt for selection

### 2. Prior Context Loading (Context Simplifier Integration)
- Auto-load `determination.summary.md` if exists
- If loaded: Pre-populate device characteristics from determination context
- If not loaded: Proceed to input collection

### 3. Input Collection (Document-First Workflow)

**If technical document provided**:
- Extract classification-relevant fields:
  - Invasiveness level (non-invasive, invasive, implantable)
  - Duration of contact (transient <60min, short-term ≤30 days, long-term >30 days)
  - Active vs passive classification
  - Intended use scope
  - Body system interaction
  - Anatomical location
- Gap detection: Identify missing classification fields
- Targeted Q&A: Ask only for genuinely missing fields (max 1-3 rounds)

**If no document and no prior context**:
- Conversational Q&A to collect classification characteristics

### 4. Classification Analysis
- Activate classification skill (references `skills/classification/SKILL.md`)
- Apply FDA classification decision rules
- Apply EU MDR Annex VIII classification logic (Rules 1-22)
- Apply MFDS classification evaluation criteria
- Generate multi-region classification matrix
- Apply traffic light system per region
- Identify escalation scenarios (ambiguous classifications, cross-region discrepancies)

### 5. Optimization Analysis (Optional, OR-004)

**If `--optimize` flag present**:
- Extract key decision factors (invasiveness, duration, active/passive, intended use, anatomical location)
- Provide strategic guidance on potential class reduction pathways:
  - **Invasiveness**: Abstract guidance on reducing invasiveness level
  - **Duration**: Considerations for shortening contact duration
  - **Active/Passive**: Feasibility of passive design alternatives
  - **Anatomical Location**: Strategies to avoid high-risk body systems
- Tag all optimization suggestions as YELLOW
- Include mandatory escalation recommendation
- Add supplementary classification optimization disclaimer

**Important**: Optimization analysis provides abstract strategic guidance only, NOT specific design recommendations.

### 6. Output Generation
- **Full output**: `classification.md`
  - Header (command, product, date, version, optimization enabled/disabled)
  - Input summary
  - Multi-region classification matrix
  - Rationale and rule references per region
  - Traffic light per region
  - Data source attribution
  - Escalation recommendations (if applicable)
  - Optimization analysis (if `--optimize` flag used)
  - Next steps (1-3 suggestions)
  - Standard disclaimer
  - Optimization disclaimer (if applicable)

- **Compressed summary**: `classification.summary.md` (Key-Value Markdown format, ~500 tokens)
  ```markdown
  - **FDA Class**: [I/II/III]
  - **EU MDR Class**: [I/IIa/IIb/III]
  - **MFDS Class**: [1/2/3/4]
  - **Traffic Light**: [GREEN/YELLOW/RED per region]
  - **Key Factors**: [Invasiveness, Duration, Active/Passive]
  - **Optimization Analyzed**: [Yes/No]
  - **Escalation**: [Yes/No + reason]
  - **Sources**: [Data sources: Notion/Built-in/Context7]
  ```

### 7. Next Steps
Suggest 1-3 next commands based on classification result:
- **Primary**: `/aria:pathway` (select regulatory pathway per class)
- **Alternative**: `/aria:compare` (compare multi-region requirements)
- **Optional**: Classification optimization consultation (if `--optimize` flag used)

## Flags

- `--optimize`: Enable classification optimization analysis (OR-004). Analyzes key decision factors for potential class reduction. **Always generates YELLOW traffic light and mandatory escalation.**
- `--lang en|ko`: Output language (default: `ko` from aria.local.md or system default)

## Output Location

- **Full output**: `.aria/products/{product-name}/{date}/classification.md`
- **Compressed summary**: `.aria/products/{product-name}/{date}/classification.summary.md`

## Data Sources

The classification analysis uses a three-tier data priority system:

1. **Notion DB** (Priority 1): Organization-specific classification precedents and device class assignments
2. **Built-in Knowledge** (Priority 2): Embedded classification logic from FDA, EU MDR Annex VIII, MFDS regulations
3. **Context7** (Priority 3): Supplementation and verification from regulatory classification guidelines

If Notion DB is unavailable, the system gracefully degrades to built-in knowledge with Context7 supplementation.

## Traffic Light System

### Per-Region Traffic Lights
Each region (FDA, EU MDR, MFDS) receives independent traffic light assessment:

- **GREEN**: Clear classification with definitive class assignment
- **YELLOW**: Borderline classification or optimization analysis requested (requires regulatory specialist review)
- **RED**: Unable to classify due to insufficient information or conflicting rules

### Overall Traffic Light
The most conservative (highest caution) traffic light across all regions determines overall status.

## Escalation Scenarios

YELLOW or RED traffic lights trigger escalation recommendations:
- **Cross-Region Discrepancies**: Different classes assigned across FDA, EU MDR, MFDS
- **Borderline Classifications**: Device characteristics straddle two classes
- **Novel Device Types**: No clear classification precedent
- **Optimization Analysis**: All `--optimize` flag invocations trigger mandatory escalation

## Classification Optimization (OR-004)

### When to Use `--optimize` Flag

Use classification optimization analysis when:
- Exploring design trade-offs for regulatory strategy
- Early-stage development with flexibility in design choices
- Comparing multiple design concepts for optimal regulatory pathway
- Strategic planning for global market access

**Do NOT use** for:
- Finalized designs submitted for regulatory approval
- Legacy devices with established market presence
- Situations requiring specific design recommendations (consult R&D + Regulatory affairs instead)

### Optimization Output

The analysis provides:
- Abstract guidance on key classification factors (invasiveness, duration, active/passive, anatomical location)
- Potential pathways for class reduction through design modifications
- Strategic considerations for regulatory impact assessment

**What optimization does NOT provide**:
- Specific design changes or technical specifications
- Guarantees of classification reduction approval
- Substitute for R&D feasibility assessment
- Substitute for regulatory affairs strategy consultation

### Mandatory Constraints
- **YELLOW Traffic Light**: All optimization analyses show YELLOW (caution)
- **Mandatory Escalation**: Always escalate to R&D + Regulatory affairs collaboration
- **Abstract Only**: No concrete design recommendations provided

## Example Usage

### Example 1: Pipeline Context Auto-Load
```
/aria:classify
```
→ System auto-loads `determination.summary.md` from prior step
→ Pre-populates device characteristics
→ Asks targeted questions only for missing classification fields
→ Generates classification matrix

### Example 2: With Optimization Analysis
```
/aria:classify --optimize
```
→ System performs standard classification
→ Adds optimization analysis section
→ Provides strategic guidance on key decision factors
→ Tags result as YELLOW with mandatory escalation
→ Includes supplementary optimization disclaimer

### Example 3: Korean Output with Optimization
```
/aria:classify --optimize --lang ko
```
→ All output generated in Korean language
→ Includes optimization analysis

### Example 4: Standalone Classification (No Prior Context)
```
/aria:classify [Upload technical specification PDF]
```
→ System extracts classification characteristics from document
→ Performs classification analysis without determination context
→ Generates classification matrix

## Multi-Region Classification Example

**Sample Output Matrix**:

| Region | Class | Risk Level | Rationale | Traffic Light |
|--------|-------|------------|-----------|---------------|
| FDA | II | Moderate | Invasive surgical device, short-term use | GREEN |
| EU MDR | IIa | Medium-Low | Rule 6: Short-term invasive surgically device | GREEN |
| MFDS | 3 | 중간-높음 | 침습적 사용, 중기 접촉 | GREEN |

**Cross-Region Analysis**: FDA Class II (moderate regulatory pathway), EU MDR Class IIa (Notified Body review), MFDS Class 3 (Ministry review). Consistent moderate-risk classification across all regions.

## Disclaimer

⚠️ **중요 고지사항**

본 분류 결과는 AI 기반 regulatory intelligence tool의 분석이며, 공식적인 규제 분류가 아닙니다.

- **법적 효력 없음**: 본 결과는 참고용이며 법적 구속력이 없습니다
- **전문가 검토 필수**: 실제 규제 제출 전 regulatory affairs 전문가 검토가 반드시 필요합니다
- **규제 기관 확인**: 최종 분류는 FDA, Notified Body, MFDS 등 규제 기관의 공식 결정을 따릅니다
- **책임 한계**: 본 도구 사용으로 인한 규제 미준수 책임은 사용자에게 있습니다

Knowledge Base Date: 2026-01 기준

### Classification Optimization Disclaimer (when `--optimize` used)

⚠️ **분류 최적화 분석 추가 고지사항**

본 분류 최적화 분석은 잠재적 설계 변경 방향에 대한 추상적 가이드이며, 구체적인 설계 권고가 아닙니다.

- **YELLOW 트래픽 라이트 필수**: 최적화 분석은 항상 YELLOW 상태로 표시됩니다
- **필수 에스컬레이션**: Regulatory affairs + R&D 전문가 협의 필수
- **규제 전략 영향**: 설계 변경이 규제 전략에 미치는 영향 사전 평가 필요
- **임상 데이터**: 설계 변경 시 추가 임상 시험 필요 여부 검토 필수
- **성능 검증**: 모든 설계 변경은 임상 성능 유지/개선 검증 필수

Classification optimization suggestions are exploratory scenarios only. Any product modification for regulatory classification purposes must be validated by qualified regulatory affairs professionals and must not compromise patient safety or device efficacy.

---

This is reference information for professional review, not regulatory advice. All regulatory decisions must be validated by qualified regulatory affairs professionals.
