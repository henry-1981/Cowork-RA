---
description: Free-form regulatory Q&A with intelligent skill routing - Automatically routes queries to appropriate skills or provides conversational answers
argument-hint: "[Question or request] [--lang en|ko]"
---

# /aria:chat - Intelligent Regulatory Q&A

## Purpose

Free-form conversation interface for regulatory questions with intelligent skill routing. Automatically detects user intent and routes to the appropriate skill, presents disambiguation menu for ambiguous queries, or provides direct conversational answers for general questions.

## Workflow

### 1. Multi-Product Selection (SR-006)

Check `.aria/products/` directory structure and `.aria/active_product.json`:

**Case 1: Multiple products exist AND active_product.json does NOT exist**
- Scan `.aria/products/` for all product directories
- Present selection menu with product names and most recent dates
- Allow creation of new product entry
- Persist user selection to `.aria/active_product.json` with format:
  ```json
  { "product_name": "cardiac-monitor-x1", "last_accessed": "2026-02-11", "path": ".aria/products/cardiac-monitor-x1/2026-02-11/" }
  ```

**Case 2: active_product.json exists with valid product reference**
- Load active product from file
- Update last_accessed date
- Skip selection menu

**Case 3: active_product.json exists but references invalid/deleted product**
- Treat file as stale
- Present product selection menu
- Update active_product.json with new selection

**Case 4: Exactly 1 product exists**
- Auto-select single product
- Persist to active_product.json
- Skip selection menu

**Case 5: No products exist**
- Prompt user to create new product entry
- Apply product naming convention (lowercase, hyphens, alphanumeric only)
- Persist new product to active_product.json

### 2. Query Analysis (Hybrid Routing Logic)

Analyze user query for routing decision:

**Route 1: Clear Keyword Match → Direct Skill Execution**

Detect explicit skill keywords and route directly without disambiguation:

**Determination keywords**:
- "의료기기인지", "의료기기 해당", "determine", "의료기기 판정", "device determination", "해당 여부"
- Example: "이 제품이 의료기기인지 확인해줘" → `/aria:determine`

**Classification keywords**:
- "등급", "분류", "classify", "classification", "Class", "등급 판정", "FDA class", "EU MDR class", "MFDS 등급"
- Example: "FDA 등급을 알려줘" → `/aria:classify`

**Pathway keywords**:
- "경로", "pathway", "510(k)", "PMA", "De Novo", "CE Marking", "MFDS 인증", "허가 경로", "submission pathway"
- Example: "510(k) 경로로 갈 수 있을까?" → `/aria:pathway`

**Estimation keywords**:
- "비용", "일정", "estimate", "cost", "timeline", "예산", "기간", "소요 시간"
- Example: "인허가 비용이 얼마나 들까?" → `/aria:estimate`

**Planning keywords**:
- "계획", "plan", "milestone", "일정표", "로드맵", "프로젝트 계획"
- Example: "인허가 계획을 세워줘" → `/aria:plan`

**Comparison keywords**:
- "비교", "compare", "차이", "difference", "FDA vs EU", "국가별 비교", "다국가 규제"
- Example: "FDA와 EU MDR 차이점을 비교해줘" → `/aria:compare`

**Briefing keywords**:
- "보고서", "brief", "briefing", "요약 보고", "종합 분석", "executive summary"
- Example: "종합 보고서를 작성해줘" → `/aria:brief`

**Route 2: Ambiguous Query → Skill Suggestion Menu**

Present top 1-3 skill suggestions when query intent is unclear:

**Ambiguous query examples**:
- "내 제품 도와줘" → Could be determination, classification, or pathway
- "규제 관련 질문이 있어" → Could be any skill
- "이것 좀 봐줘" → Requires context to determine skill

**Suggestion menu format**:
- Top 1-3 most relevant skills based on context
- Brief description per skill (1 line)
- Allow user selection or query refinement

**Route 3: General Regulatory Question → Conversational Q&A**

Provide direct informational answer for general knowledge questions:

**General question examples**:
- "EU MDR이 뭐야?" → Direct answer about EU MDR regulation
- "의료기기 인허가가 왜 필요해?" → Explain regulatory requirements
- "ISO 13485는 무슨 규격이야?" → Define quality management standard
- "Clinical evidence가 뭔지 설명해줘" → Explain clinical evidence concept

**Conversational mode behavior**:
- Direct answer without skill invocation
- Include source attribution where applicable
- Provide disclaimer for regulatory interpretations
- Suggest related skills if user wants deeper analysis

### 3. Context Integration

Load prior pipeline data from `.aria/products/{product-name}/{date}/` when available:

**Available context**:
- Determination results inform classification-related queries
- Classification results inform pathway-related queries
- Pathway selection informs estimation and planning queries
- All prior data available for briefing requests

**Context usage**:
- Auto-populate skill inputs from prior step data
- Reduce redundant Q&A by reusing collected information
- Compress context using `.summary.md` files when available

### 4. Skill Routing Execution

**For clear keyword matches**:
- Route directly to identified skill
- Pass user query and context to skill
- Execute skill workflow (determination, classification, pathway, etc.)
- Return skill output to user

**For ambiguous queries**:
- Present suggestion menu
- Wait for user selection
- Route to selected skill

**For general questions**:
- Generate conversational answer
- Include disclaimer if regulatory interpretation
- Suggest next step skills if relevant

### 5. Output Handling

**Skill-routed output**:
- Follow routed skill's output format and storage rules
- Store results in `.aria/products/{product-name}/{date}/`
- Generate compressed summary via Context Simplifier

**Conversational output**:
- Direct answer in chat interface
- No file storage for general Q&A
- Include source attribution for regulatory facts

### 6. Next Steps

**After skill execution**:
- Display skill-specific next step suggestions
- Follow skill's pipeline progression logic

**After conversational answer**:
- Suggest relevant skills for deeper analysis
- Example: "EU MDR 설명" answer → Suggest `/aria:determine` or `/aria:classify` for device-specific analysis

## Routing Accuracy Target

Target routing accuracy: 80% or higher on diverse test queries (20+ queries across 7 skill domains).

**Accuracy definition**:
- Clear keyword queries route correctly without disambiguation
- Ambiguous queries present relevant suggestions (top 1-3)
- General questions receive direct answers without unnecessary skill invocation

## Flags

- `--lang en|ko`: Output language (default: `ko`)

## Multi-Product Workflow

Multi-product selection (SR-006) executes BEFORE query routing to ensure all skill invocations operate in correct product context.

**Product context persistence**:
- `.aria/active_product.json` maintains active product across sessions
- File-based persistence supports stateless environment
- Selection survives application restart

## Data Sources

Built-in knowledge for general Q&A, keyword routing logic, and skill descriptions. Prior pipeline data from `.aria/` directory supplements context. External data connectors (Notion, Context7) are invoked only if skills are routed.

## Example Interactions

**Example 1: Clear keyword match**
```
User: /aria:chat 이 제품이 의료기기인지 판정해줘
System: [Detects "의료기기인지" keyword]
System: [Routes directly to determination skill]
System: [Executes /aria:determine workflow]
```

**Example 2: Ambiguous query**
```
User: /aria:chat 내 제품 규제 관련 도와줘
System: [Multiple skills applicable]
System: [Presents menu]
  1. /aria:determine - 의료기기 해당 여부 판정
  2. /aria:classify - 규제 등급 분류
  3. /aria:pathway - 인허가 경로 선택
User: [Selects option 1]
System: [Routes to determination skill]
```

**Example 3: General question**
```
User: /aria:chat EU MDR이 뭐야?
System: [Detects general knowledge question]
System: [Generates conversational answer]
Response: EU MDR(Medical Device Regulation 2017/745)은 유럽연합의 의료기기 규제로...
[Includes source attribution and disclaimer]
[Suggests /aria:compare for detailed FDA vs EU MDR comparison]
```

**Example 4: Multi-turn dialogue**
```
User: /aria:chat 인허가 비용이 궁금해
System: [Detects "비용" keyword → estimation skill]
System: [Routes to /aria:estimate]
[After estimation completes]
System: Next steps:
  - /aria:plan to create regulatory milestone plan
  - /aria:brief to generate comprehensive report
```

## Keyword Mapping Reference

Quick reference for skill routing:

| Skill | Primary Keywords (Korean) | Primary Keywords (English) | Example Queries |
|-------|---------------------------|----------------------------|-----------------|
| determination | 의료기기인지, 해당 여부, 판정 | determine, medical device qualification | "의료기기 해당하나요?" |
| classification | 등급, 분류, Class | classify, class, grade | "FDA 등급이 뭐죠?" |
| pathway | 경로, 510(k), PMA, CE Marking | pathway, submission route | "510(k) 가능한가요?" |
| estimation | 비용, 일정, 예산 | cost, timeline, budget | "비용이 얼마나 들까요?" |
| planning | 계획, 로드맵, 마일스톤 | plan, milestone, roadmap | "인허가 계획 세워줘" |
| comparison | 비교, 차이, 국가별 | compare, difference, multi-country | "FDA vs EU 차이점" |
| briefing | 보고서, 종합, 요약 | brief, report, summary | "종합 보고서 작성" |

## Disclaimer

**Important Notice**

This chat interface is an AI-powered regulatory intelligence router, not a substitute for regulatory expertise.

- **No legal effect**: Responses are for reference only and have no legal binding force
- **Expert review required**: All regulatory analyses require validation by qualified regulatory affairs professionals
- **Routing accuracy**: Keyword-based routing may misinterpret complex queries; users can manually invoke specific commands if needed
- **Limitation of liability**: Users are responsible for regulatory decisions made based on this tool's output

Knowledge Base Date: 2026-01

---

This is reference information for professional review, not regulatory advice.
