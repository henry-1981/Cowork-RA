---
name: aria-briefing
description: >
  Comprehensive regulatory briefing report generation skill.
  Synthesizes all pipeline data into executive-ready documents.
  Use for comprehensive reports integrating determination, classification, pathway, estimates, and plan.
allowed-tools: Read Grep Glob ToolSearch
user-invocable: false
metadata:
  version: "1.0.1"
  category: "domain"
  status: "active"
  updated: "2026-02-11"
  modularized: "false"
  tags: "briefing, executive-summary, comprehensive-report, pipeline-integration"
  knowledge-base-date: "2026-01"

# MoAI Extension: Progressive Disclosure
progressive_disclosure:
  enabled: true
  level1_tokens: 100
  level2_tokens: 2500

# MoAI Extension: Triggers
triggers:
  keywords: ["briefing", "brief", "executive summary", "comprehensive report", "regulatory summary"]
  phases: ["run"]
---

# Regulatory Briefing Report Generation Skill

## Quick Reference

**Purpose**: Generate comprehensive regulatory briefing reports synthesizing all available pipeline data into executive-ready documents.

**Input**: All .aria/ pipeline data (determination, classification, pathway, estimation, plan, comparison), optional focus area
**Output**: Executive briefing with summary, detailed analysis, recommendations, and appendices
**Knowledge Base Date**: 2026-01

---

## Decision Framework

### Briefing Report Structure

#### Executive Summary (1-2 pages)
- **Product Overview**: Device name, intended use, regulatory scope
- **Regulatory Status**: Device determination, classification across regions
- **Recommended Pathway**: FDA, EU MDR, MFDS submission routes
- **Timeline & Cost**: Overall project estimate (expected timeline, budget range)
- **Key Risks**: Critical regulatory challenges with traffic light assessment
- **Strategic Recommendations**: Top 3 action items for leadership

#### Detailed Analysis (per pipeline step)
1. **Device Determination**: Medical device status per region, applicable regulations
2. **Classification**: Class/Grade assignment per region with rationale
3. **Regulatory Pathways**: Submission routes, timelines, requirements
4. **Cost & Timeline Estimates**: Budget breakdown, milestone schedule
5. **Regulatory Plan**: Phase-by-phase implementation roadmap
6. **Multi-Country Comparison**: Regional requirement differences (if available)

#### Recommendations Section
- **Immediate Actions**: Tasks for next 30 days
- **Critical Dependencies**: Key decision points and blockers
- **Resource Requirements**: Personnel, consultants, testing facilities
- **Risk Mitigation**: Strategies for identified regulatory challenges

#### Appendices
- **Regulatory Citations**: All referenced regulations (FDA CFR, EU MDR Articles, MFDS 의료기기법)
- **Data Sources**: Attribution for all information used
- **Escalation Items**: Items requiring expert review with rationale
- **Glossary**: Regulatory terms and acronyms

---

## Workflow

### Step 1: Load All Available Pipeline Data

Scan `.aria/products/<product-name>/<date>/` for:
- `determination.summary.md` (device status)
- `classification.summary.md` (class/grade)
- `pathway.summary.md` (submission routes)
- `estimation.summary.md` (cost/timeline)
- `plan.summary.md` (milestone roadmap)
- `comparison.summary.md` (multi-country analysis, optional)

**Priority for Briefing**:
- Use `.summary.md` files for executive summary (compressed context)
- Use full `.md` files for detailed analysis section (complete information)

### Step 2: Assess Data Completeness

Categorize pipeline completeness:

**Full Pipeline** (all 5 core steps available):
- determination → classification → pathway → estimation → plan
- Generate comprehensive briefing with all sections

**Partial Pipeline** (some steps available):
- Generate briefing covering available data
- Indicate missing steps with recommendations to complete

**Minimal Data** (only determination or classification):
- Generate focused briefing on available analysis
- Strong recommendations to execute remaining pipeline steps

### Step 3: Identify Focus Area (Optional)

If user specifies focus area:
- **Clinical Strategy**: Emphasize clinical evidence requirements, trial planning
- **Cost Control**: Emphasize budget optimization, cost reduction opportunities
- **Timeline Acceleration**: Emphasize parallel submission, expedited pathways
- **Multi-Market Entry**: Emphasize comparison analysis, harmonization strategy

Apply focus area weighting in recommendations and executive summary.

### Step 4: Synthesize Executive Summary

Extract key information from all loaded summaries:

**From Determination Summary**:
- Medical device status (YES/NO/CONDITIONAL)
- Applicable regions (FDA, EU MDR, MFDS)

**From Classification Summary**:
- FDA Class (I/II/III)
- EU MDR Class (I/IIa/IIb/III)
- MFDS Grade (1/2/3/4)
- Overall risk profile

**From Pathway Summary**:
- Recommended pathways per region
- Critical path (longest timeline)

**From Estimation Summary**:
- Total budget range (optimistic/expected/pessimistic)
- Total timeline (end-to-end)

**From Plan Summary**:
- Number of phases
- Key milestones and dependencies

**From Comparison Summary** (if available):
- Harmonization strategy
- Key regulatory differences

### Step 5: Generate Detailed Analysis

For each pipeline step with full data available:
- Load full `.md` file content
- Extract: Input, Analysis, Traffic Light, Escalation, Sources
- Present in structured format with subsections

### Step 6: Formulate Recommendations

Based on synthesized data:

**Immediate Actions** (next 30 days):
1. [Action based on current pipeline stage]
2. [Critical dependency resolution]
3. [Expert consultation if escalation flagged]

**Critical Dependencies**:
- [Key decision points from plan]
- [Data gaps requiring resolution]
- [External dependencies (testing, clinical, notified body)]

**Resource Requirements**:
- Regulatory consultants (FDA/EU/MFDS expertise)
- Testing facilities (per pathway requirements)
- Clinical trial sites (if PMA or Class III pathway)
- Notified Body (if EU Class IIa+)

**Risk Mitigation**:
- [Strategies for YELLOW/RED traffic light items]
- [Contingency plans for identified risks]

### Step 7: Assign Overall Traffic Light

Aggregate traffic lights from all pipeline steps:

- **🟢 GREEN**: All steps GREEN, low-risk regulatory path
- **🟡 YELLOW**: Any step YELLOW or RED, moderate-high risk, expert review recommended
- **🔴 RED**: Multiple RED flags, significant regulatory barriers, fundamental approach change needed

### Step 8: Generate Output (ER-017 Two-Phase Approach)

**Phase A - Analysis Turn** (Present key findings for user confirmation):

```markdown
# 규제 브리핑 분석 결과 (요약)

## 제품 개요
- **제품명**: [Product Name]
- **의료기기 해당 여부**: [YES/NO/CONDITIONAL]
- **분류**: FDA Class [I/II/III], EU MDR Class [I/IIa/IIb/III], MFDS Grade [1/2/3/4]

## 핵심 발견사항
1. **규제 경로**: [FDA Pathway] / [EU Pathway] / [MFDS Pathway]
2. **예상 소요 기간**: [Critical Path Timeline]
3. **예상 비용**: [Budget Range]
4. **주요 위험**: [Key risks with traffic light]

## 권장사항 (Top 3)
1. [Immediate action 1]
2. [Immediate action 2]
3. [Immediate action 3]

## 전체 위험도 평가
- **Traffic Light**: [🟢 GREEN / 🟡 YELLOW / 🔴 RED]

[If YELLOW or RED]: **⚠️ 전문가 검토 권장**: 복잡도가 높은 규제 경로이므로 규제 전문가와 상담을 권장합니다.

---
**사용자 확인 필요**: 위 분석 내용을 검토하신 후, 전체 보고서 생성을 진행하시겠습니까?
```

**Phase B - Full Report Generation** (After user confirmation, generate complete briefing):

```markdown
# 규제 브리핑 보고서

## 목차
1. [경영진 요약 (Executive Summary)](#경영진-요약)
2. [상세 분석 (Detailed Analysis)](#상세-분석)
3. [권장사항 (Recommendations)](#권장사항)
4. [부록 (Appendices)](#부록)

---

## 경영진 요약

### 제품 개요
- **제품명**: [Product Name]
- **의도된 용도**: [Intended Use]
- **규제 범위**: FDA (미국), EU MDR (유럽), MFDS (한국)

### 규제 현황
- **의료기기 해당 여부**: [YES/NO/CONDITIONAL] ([Traffic Light])
- **분류 등급**:
  - FDA: Class [I/II/III]
  - EU MDR: Class [I/IIa/IIb/III]
  - MFDS: Grade [1/2/3/4]

### 권장 경로
- **FDA**: [Pathway] (예상 소요 기간: [Timeline])
- **EU MDR**: [Pathway] (예상 소요 기간: [Timeline])
- **MFDS**: [Pathway] (예상 소요 기간: [Timeline])
- **Critical Path**: [Region] ([Longest Timeline])

### 비용 및 일정
- **총 예상 비용**: [Optimistic] ~ [Expected] ~ [Pessimistic]
- **총 예상 기간**: [End-to-end Timeline]
- **주요 마일스톤**: [Key milestones from plan]

### 주요 위험
1. [Risk 1 with traffic light]
2. [Risk 2 with traffic light]
3. [Risk 3 with traffic light]

### 전략 권장사항
1. [Top recommendation 1]
2. [Top recommendation 2]
3. [Top recommendation 3]

---

## 상세 분석

### 1. 의료기기 판정 (Device Determination)
[Full determination analysis from determination.md]

### 2. 등급 분류 (Classification)
[Full classification analysis from classification.md]

### 3. 규제 경로 (Regulatory Pathways)
[Full pathway analysis from pathway.md]

### 4. 비용 및 일정 추정 (Cost & Timeline Estimation)
[Full estimation analysis from estimation.md]

### 5. 규제 계획 (Regulatory Plan)
[Full plan analysis from plan.md]

### 6. 다국가 규제 비교 (Multi-Country Comparison)
[Full comparison analysis from comparison.md if available]
[If not available: "다국가 비교 분석은 수행되지 않았습니다. `/aria:compare` 명령으로 수행 가능합니다."]

---

## 권장사항

### 즉시 실행 항목 (30일 이내)
1. [Immediate action 1 with rationale]
2. [Immediate action 2 with rationale]
3. [Immediate action 3 with rationale]

### 핵심 의존성
- [Critical dependency 1]
- [Critical dependency 2]
- [Critical dependency 3]

### 필요 리소스
- **규제 전문가**: FDA/EU MDR/MFDS 전문 컨설턴트
- **시험 기관**: [Testing requirements per pathway]
- **임상 시험**: [Clinical trial requirements if applicable]
- **인증 기관**: [Notified Body if EU Class IIa+]

### 위험 완화 전략
- [Risk mitigation strategy 1]
- [Risk mitigation strategy 2]
- [Risk mitigation strategy 3]

---

## 부록

### A. 규제 근거 (Regulatory Citations)
- **FDA**: [FDA CFR citations from all steps]
- **EU MDR**: [EU MDR Article citations from all steps]
- **MFDS**: [MFDS 의료기기법 citations from all steps]

### B. 데이터 출처 (Data Sources)
- [Attribution summary from all pipeline steps]
- Built-in knowledge: FDA, EU MDR, MFDS decision frameworks (2026-01 knowledge base)
- External sources: [Notion DB / Context7 if used]

### C. 전문가 검토 필요 항목 (Escalation Items)
[All escalation items from pipeline steps with rationale]

### D. 용어집 (Glossary)
- **510(k)**: FDA Premarket Notification
- **PMA**: FDA Premarket Approval
- **CE Marking**: EU conformity marking
- **Notified Body**: EU conformity assessment body
- **PMCF**: Post-Market Clinical Follow-up
- **QMS**: Quality Management System
- [Additional regulatory terms as needed]

---

## 면책 조항
⚠️ **본 브리핑 보고서는 참고 정보이며, 규제 자문이 아닙니다.** 모든 규제 결정은 규제 전문가의 검토와 검증이 필요하며, 최종 규제 제출 전 최신 규제 요구사항을 확인하시기 바랍니다.

---
**생성 일시**: [Timestamp]
**ARIA Plugin Version**: 2.0.0
**보고서 버전**: [Version if re-generated]
```

### Step 9: Generate Context Simplifier Summary

Create `.summary.md` file:

```markdown
# Briefing Summary

**Product**: [Product Name]
**Date**: [YYYY-MM-DD]

- **Decision**: Comprehensive briefing report generated
- **Pipeline Steps Covered**: [List of available steps]
- **Traffic Light**: [GREEN/YELLOW/RED]
- **Critical Path**: [Region] ([Timeline])
- **Total Budget**: [Expected Range]
- **Key Risks**: [Top 3 risks]
- **Top Recommendations**: [Top 3 actions]
- **Escalation**: [Yes/No with items if yes]
- **Sources**: FDA, EU MDR, MFDS regulations + all pipeline data

---
This summary captures the briefing report for audit trail.
```

---

## Data Source Strategy

1. **Pipeline Data** (Primary): `.summary.md` for executive summary, full `.md` for detailed analysis
2. **Built-in Knowledge** (Supplementary): Briefing structure rules, executive summary framework
3. **External Tools** (Optional): Only when explicitly configured

### Context7 Integration for Regulatory Document Supplementation

**Purpose**: Supplement regulatory citations and verify latest regulatory requirements

**Workflow**:

1. **Tool Discovery**:
   - Use ToolSearch to load Context7 MCP tools: `ToolSearch("context7")`
   - Expected tools: `mcp__context7__resolve-library-id`, `mcp__context7__get-library-docs`

2. **Regulatory Document Supplementation**:
   - When regulatory citations are referenced (FDA CFR, EU MDR, MFDS):
     - Resolve library ID via `mcp__context7__resolve-library-id`
     - Retrieve latest documentation via `mcp__context7__get-library-docs`
     - Cross-reference with built-in knowledge to verify accuracy
     - Attribute Context7 as supplementary source in Appendix B (Data Sources)

3. **Graceful Degradation**:
   - If Context7 unavailable → Use built-in knowledge only
   - Display in Data Source Attribution: "(built-in knowledge, Context7 unavailable)"
   - Briefing remains fully functional without Context7

4. **Source Attribution**:
   - When Context7 used successfully:
     - Appendix B: "External sources: Context7 (regulatory document verification)"
     - Each citation: Add "(verified via Context7 YYYY-MM-DD)" when applicable
   - When Context7 unavailable:
     - Appendix B: "External sources: Context7 (unavailable, built-in knowledge used)"

---

## Traffic Light Definitions

- **🟢 GREEN**: All pipeline steps GREEN, low-risk regulatory path
- **🟡 YELLOW**: Any step YELLOW or RED, moderate-high risk path
- **🔴 RED**: Multiple RED flags, significant regulatory barriers

---

## Escalation Scenarios

Escalate to regulatory expert when:
- Overall traffic light is YELLOW or RED
- Briefing is for external stakeholders (board, investors, regulatory authorities)
- Critical decision points require executive approval
- Budget or timeline exceeds organizational thresholds

---

## VALID Framework Compliance

- **Verified**: All claims sourced from pipeline data or built-in regulatory knowledge
- **Accurate**: Briefing reflects current pipeline state, all sources attributed
- **Linked**: Cross-references between briefing sections and source pipeline steps
- **Inspectable**: Decision rationale transparent, audit trail via .aria/ files
- **Deliverable**: Output stored in `.aria/products/<product-name>/<date>/briefing.md`

---

## Report Issuance Policy (ER-017)

**Two-Phase Approach**:
1. **Analysis Phase**: Present key findings, traffic light, recommendations for user review
2. **Report Phase**: After user confirmation, generate full formatted report

**Format Options** (via `--format` flag):
- `markdown` (default): Markdown report to `.aria/products/`
- `notion`: Notion page via Notion MCP (requires notion-mcp)
- `gdocs`: Google Docs via Google Drive MCP (requires google-drive-mcp)
- `pdf`: PDF conversion from Markdown (requires pandoc/wkhtmltopdf/weasyprint)

**Google Docs Export Workflow**:

When `--format gdocs` is specified:

1. **Tool Discovery**:
   - Use ToolSearch to load Google Drive MCP tools: `ToolSearch("google drive")`
   - Expected tools: `mcp__gdrive__create_file`, `mcp__gdrive__upload_content`

2. **Graceful Degradation**:
   - If ToolSearch returns no Google Drive tools → Fallback to Markdown
   - Display: "Google Drive MCP가 설정되지 않았습니다. Markdown 형식으로 보고서를 생성합니다."
   - Save to `.aria/products/{product-name}/{date}/briefing.md`
   - Include limitation notice in Data Source Attribution

3. **Google Docs Creation** (if tools available):
   - Generate briefing content in Markdown format first
   - Convert Markdown to Google Docs-compatible format
   - Create document via `mcp__gdrive__create_file`:
     - Title: "{Product Name} - Regulatory Briefing Report ({YYYY-MM-DD})"
     - MimeType: `application/vnd.google-apps.document`
     - Content: Converted briefing content
   - Display Google Docs link to user
   - Save Markdown backup to `.aria/products/{product-name}/{date}/briefing.md`

4. **Error Recovery**:
   - If MCP tool call fails → Fallback to Markdown with error message
   - Error: "Google Drive에 연결할 수 없습니다. Markdown 형식으로 보고서를 생성합니다."

**User confirmation required before full report generation** (ER-017).

---

## Version History

**v1.0.0** (2026-02-11):
- Initial implementation for Phase 4
- Full pipeline data synthesis
- Executive summary generation
- Detailed analysis per step
- Recommendations and escalation
- Two-phase report issuance (ER-017)
- Multi-format output support
- Context Simplifier integration
- Korean language output
- Traffic light aggregation
- VALID framework compliance

---

**Knowledge Base Cutoff**: 2026-01
**Next Update**: Quarterly regulatory updates
