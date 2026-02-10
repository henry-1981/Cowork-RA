# SPEC-ARIA-001: Implementation Plan

```yaml
SPEC_ID: SPEC-ARIA-001
TITLE: ARIA Cowork Plugin - Implementation Plan
VERSION: 3.1.0
```

---

## Overview

ARIA Cowork Plugin의 전체 구현 계획. 6개 Phase로 나뉘며, 각 Phase는 이전 Phase에 의존한다.

### Technical Approach

- **Architecture**: Anthropic Cowork Plugin (commands + skills, no agents)
- **Knowledge Strategy**: Decision logic embedded in skills (~2,000-2,500 tokens), regulatory text retrieved via MCP at runtime
- **Input Strategy**: Document-first workflow (S9) with targeted Q&A fallback
- **Context Strategy**: Context Simplifier (S10) for pipeline context compression (~500 tokens per step)
- **Data Strategy**: Three-tier priority (Notion DB > Built-in > Context7) with graceful degradation
- **Output Strategy**: Markdown primary, compressed summaries for pipeline, versioned outputs for audit trail

---

## Milestone 1: Plugin Scaffold (Priority: Primary)

### Phase 1: Plugin Scaffold + Core Infrastructure

**Goal**: Cowork platform에서 인식되는 plugin 기반 구조 확립

**Deliverables**:

| Deliverable | File | Description |
|-------------|------|-------------|
| Plugin Manifest | `.claude-plugin/plugin.json` | Plugin metadata + component path declarations (commands, skills, mcpServers) |
| MCP Configuration | `.mcp.json` | Notion, Google Drive, Context7 connector definitions |
| Connector Docs | `CONNECTORS.md` | Tool-agnostic MCP connector category documentation |
| User Guide | `README.md` | Installation, setup, command reference, aria.local.md template |
| Playbook Template | `aria.local.md` | Organization-specific configuration template |

**Technical Approach**:
1. knowledge-work-plugins (Legal plugin) 구조를 benchmark으로 사용
2. `plugin.json`에 `commands`, `skills`, `mcpServers` path 선언 포함 (AR-1 fix)
3. MCP package names npm registry 확인 (`@upstash/context7-mcp` verified, Notion/Google Drive TBD)
4. 모든 command reference에 `/aria:` prefix 사용 (AR-2 fix)

**Success Criteria**:
- Plugin이 Cowork platform에서 인식됨
- MCP configuration이 에러 없이 검증됨
- 모든 MCP package names이 npm registry에서 확인됨
- README가 `/aria:` namespaced commands로 완전한 setup 안내 제공

**Risks**:
- Cowork Plugin API가 예상 패턴과 다를 수 있음 -> 조기 Phase 1 검증으로 대응
- MCP package names 미확인 -> Phase 1 success criteria에 검증 포함

---

## Milestone 2: Foundation Skills (Priority: Primary)

### Phase 2: Foundation Skills + Commands

**Goal**: Determination 및 Classification 핵심 기능 구현

**Deliverables**:

| Deliverable | File | Description |
|-------------|------|-------------|
| Determination Skill | `skills/determination/SKILL.md` | FDA/EU MDR/MFDS device determination decision logic |
| Classification Skill | `skills/classification/SKILL.md` | Multi-region classification matrix with opt-in optimization (OR-004) |
| Determine Command | `commands/determine.md` | `/aria:determine` command definition |
| Classify Command | `commands/classify.md` | `/aria:classify` command definition |
| Data Storage | `.aria/products/` | Local data storage directory structure |
| Document Analysis | (integrated in commands) | Document-first input workflow (S9) |
| Context Simplifier | (integrated in commands) | Compressed summary generation (S10) |

**Technical Approach**:
1. Skills에 decision tree/classification logic 내장 (~2,500 tokens), regulatory text는 MCP에서 runtime retrieval
2. Document Analysis Pipeline (S9): 기술 문서 입력 -> 필드 추출 -> gap detection -> targeted Q&A
3. Context Simplifier (S10): 각 command output에 `.summary.md` 압축 파일 동시 생성. 각 스킬 구현 시 SKILL.md 출력 템플릿에 Summary Generation 단계를 반드시 포함해야 한다 (요약 생성 책임은 각 개별 스킬에 있음).
4. Output versioning (SR-007): 기존 파일 존재 시 `-v2.md` suffix 자동 부여
5. Knowledge base date를 각 skill에 명시

**Implementation Steps**:
1. `.aria/products/` directory structure 및 naming convention 구현
2. `determination/SKILL.md` 작성 - FDA/EU MDR/MFDS determination decision tree 내장
3. `classification/SKILL.md` 작성 - Classification logic tree + OR-004 optimization flag 지원
4. `commands/determine.md` 작성 - document-first input, targeted Q&A, output + summary 생성
5. `commands/classify.md` 작성 - pipeline context loading, classification optimization opt-in
6. Graceful degradation 테스트 (Notion unavailable 시나리오)
7. S8.2 measurable criteria baseline 수집 시작

**Success Criteria**:
- `/aria:determine`가 5+ product types에 대해 정확한 의료기기 판정
- `/aria:classify`가 multi-region classification matrix (FDA, EU MDR, MFDS) 생성
- Traffic light system 양 command에서 정상 작동
- `.aria/products/` 구조에 output + compressed summary 저장
- Notion unavailable 시 graceful degradation 정상 작동
- Document-first input workflow 양 command에서 작동

**Agent Contingency Evaluation** (Phase 2 완료 후):
- Document analysis + Q&A가 5 rounds 초과하는 command가 있는지 확인
- Hybrid routing 정확도 80% 이상인지 확인 (20+ queries)
- User confusion 패턴 확인

---

## Milestone 3: Pathway Skills (Priority: Secondary)

### Phase 3: Pathway Skills + Commands

**Goal**: Regulatory pathway, estimation, planning 기능 구현

**Deliverables**:

| Deliverable | File | Description |
|-------------|------|-------------|
| Pathway Skill | `skills/pathway/SKILL.md` | FDA/EU/MFDS pathway selection decision tree |
| Estimation Skill | `skills/estimation/SKILL.md` | Cost/timeline estimation framework |
| Planning Skill | `skills/planning/SKILL.md` | Regulatory milestone planning logic |
| Pathway Command | `commands/pathway.md` | `/aria:pathway` command definition |
| Estimate Command | `commands/estimate.md` | `/aria:estimate` command definition |
| Plan Command | `commands/plan.md` | `/aria:plan` command definition |

**Technical Approach**:
1. Context Simplifier를 통해 Phase 2 output의 compressed summary를 pipeline context로 로드
2. Estimation skill에서 cost ranges (optimistic/expected/pessimistic) 구조 사용
3. Planning skill에서 milestone dependency mapping 및 critical path identification
4. 각 command의 next step suggestions (ER-009) 구현

**Dependencies**: Phase 2 완료 (classification data가 pathway 선택에 필요)

**Success Criteria**:
- `/aria:pathway`가 모든 target regions에 대해 올바른 pathway 식별
- `/aria:estimate`가 구조화된 cost/timeline framework 제공
- `/aria:plan`이 dependency가 포함된 milestone plan 생성
- Phase 2 commands와의 pipeline data flow가 Context Simplifier를 통해 정상 작동
- 각 command 완료 후 next step suggestions 표시

---

## Milestone 4: Analysis Skills (Priority: Secondary)

### Phase 4: Analysis Skills + Commands

**Goal**: Comparison 및 Briefing 기능 구현

**Deliverables**:

| Deliverable | File | Description |
|-------------|------|-------------|
| Comparison Skill | `skills/comparison/SKILL.md` | Multi-country regulation comparison framework |
| Briefing Skill | `skills/briefing/SKILL.md` | Executive briefing report generation |
| Compare Command | `commands/compare.md` | `/aria:compare` command definition |
| Brief Command | `commands/brief.md` | `/aria:brief` command definition |

**Technical Approach**:
1. Comparison skill: FDA vs EU MDR vs MFDS side-by-side evaluation framework
2. Briefing skill: 전체 pipeline data synthesis (summary + full context on-demand)
3. `/aria:brief`는 S10.4에 따라 full context를 on-demand로 로드할 수 있음

**Dependencies**: Phase 3 완료

**Success Criteria**:
- `/aria:compare`가 정확한 multi-country comparison matrices 생성
- `/aria:brief`가 전체 pipeline data를 executive briefing으로 synthesis
- `/aria:determine`부터 `/aria:brief`까지 full pipeline flow 작동
- Briefing quality가 VALID framework 기준 충족

---

## Milestone 5: Router + Integration (Priority: Secondary)

### Phase 5: Router Command + Workflow Integration

**Goal**: `/aria:chat` hybrid router 및 전체 pipeline 통합

**Deliverables**:

| Deliverable | File | Description |
|-------------|------|-------------|
| Chat Command | `commands/chat.md` | `/aria:chat` hybrid router command |
| Pipeline Integration | (testing) | Cross-command context sharing validation |
| Multi-product Selection | (integrated) | SR-006 multi-product workflow |

**Technical Approach**:
1. Hybrid router: keyword auto-detect + skill suggestion menu for ambiguous queries
2. Cross-command context sharing: Context Simplifier summary loading validation
3. Multi-product selection (SR-006): `.aria/products/` scan, selection menu, active product context

**Dependencies**: Phase 4 완료 (모든 skills가 routing에 필요)

**Success Criteria**:
- `/aria:chat`가 clear queries를 올바른 skills로 routing
- `/aria:chat`가 ambiguous queries에 대해 skill suggestions 표시
- Full pipeline flow가 auto-context loading으로 seamless 작동
- 8개 전체 commands가 독립 실행 가능
- Multi-product selection 기능 작동

---

## Milestone 6: Data Pipeline + Output (Priority: Final)

### Phase 6: Data Pipeline + Output Options

**Goal**: Notion DB integration, Context7 supplementation, multi-format output 완성

**Deliverables**:

| Deliverable | Description |
|-------------|-------------|
| Notion DB Integration | Primary data source lookup |
| Context7 Integration | Supplementation and verification |
| Google Drive Connector | Output export to Google Docs |
| Playbook Parsing | aria.local.md configuration (including language preference) |
| Multi-format Output | Markdown + Notion page output formats |
| English Toggle | SR-008 language switch |

**Technical Approach**:
1. Notion DB: Organization-specific regulatory data lookup (priority 1)
2. Context7: Regulatory document supplementation/verification (priority 3, parallel with Notion)
3. Data priority order enforcement: Notion -> built-in -> Context7
4. Graceful degradation matrix (S4.3) 전체 구현
5. aria.local.md playbook parsing: language preference, pathway defaults, risk tolerance 등
6. English output toggle (SR-008): command flag 또는 playbook setting

**Dependencies**: Phase 5 완료

**Success Criteria**:
- Notion DB lookup이 primary data source로 작동
- Context7 supplementation/verification 기능 작동
- Data source priority order (Notion -> built-in -> Context7) 강제
- Graceful degradation matrix (S4.3) 전체 작동
- aria.local.md customization 올바르게 적용
- Markdown + Notion page output formats 최소 2개 작동
- English toggle 활성화 시 정상 작동

---

## Risk Mitigation Plan

### Technical Risks

| Risk | Phase | Mitigation Strategy |
|------|-------|-------------------|
| Cowork Plugin API mismatch | 1 | knowledge-work-plugins 참조, 조기 validation |
| MCP package names 미확인 | 1 | npm registry 확인을 Phase 1 success criteria에 포함 |
| Built-in knowledge token budget 부족 | 2 | Decision framework 중심 aggressive summarization |
| Document extraction 정확도 부족 | 2 | Targeted Q&A fallback, confidence indicators |
| Pipeline context 비효율 | 2-6 | Context Simplifier (~500 token compression) |

### Domain Risks

| Risk | Phase | Mitigation Strategy |
|------|-------|-------------------|
| Regulatory info 구식화 | 6 | Notion DB primary, knowledge base date stamping |
| Classification edge cases | 2 | YELLOW traffic light + mandatory escalation |
| Cost estimate 부정확 | 3 | Range presentation, disclaimer, playbook overrides |

### UX Risks

| Risk | Phase | Mitigation Strategy |
|------|-------|-------------------|
| AI output을 regulatory advice로 인식 | 2-6 | Prominent disclaimer, escalation paths |
| Pipeline rigidity | 2-6 | 모든 commands 독립 실행 가능 |
| Hybrid router misrouting | 5 | Suggestion menu for ambiguous, direct command access |

---

## Architecture Design Direction

### Plugin Structure (Commands + Skills Only)

```
User -> /aria:{command} -> Command (workflow orchestration) -> Skill (domain logic)
                                     |                              |
                                     v                              v
                               .aria/ (data)              MCP (Notion/Context7)
```

- No agents: Domain logic resides entirely in skills
- Commands: Thin orchestration layer (frontmatter + workflow steps)
- Skills: Decision logic + output templates (~2,000-2,500 tokens each, max 500 lines)
- Data: .aria/ for local persistence, MCP for external data

### Input Processing Architecture

```
User Input -> [Document?] --yes--> Document Analysis (S9.1)
                  |                       |
                  no                 Gap Detection (S9.2)
                  |                       |
                  v                  Missing fields?
          Conversational Q&A              |
          (collect all fields)       yes: Targeted Q&A (S9.3)
                  |                  no:  Proceed
                  v                       |
          Input Data Persistence (S9.4)   v
                  |              Input Data Persistence
                  v                       |
          Command Execution <-------------+
```

### Pipeline Context Architecture

```
Step N Output (2,000-5,000 tokens)
       |
       v
Context Simplifier (S10.2)
       |
       v
Compressed Summary (~500 tokens)  +  Full Output (preserved in .aria/)
       |
       v
Step N+1 loads summary by default
(full output available on-demand)
```

---

## Quality Gates Per Phase

| Phase | Quality Gate |
|-------|-------------|
| 1 | Plugin 인식, MCP validation, package name 확인 |
| 2 | 5+ product types determination, multi-region classification, traffic light, graceful degradation, document-first input |
| 3 | Correct pathways, cost/timeline framework, milestone plan, pipeline data flow, next step suggestions |
| 4 | Comparison matrices, executive briefing, full pipeline flow, VALID framework |
| 5 | Routing accuracy (80%+), full pipeline seamless, 8 commands operational, multi-product selection |
| 6 | Notion/Context7 integration, graceful degradation matrix, playbook parsing, multi-format output, English toggle |

---

## Dependency Graph

```
Phase 1 (scaffold)
  |
  v
Phase 2 (foundation: determination + classification)
  |
  +-- Agent contingency evaluation (S8.2 measurable criteria)
  |
  v
Phase 3 (pathway + estimation + planning)
  |
  v
Phase 4 (comparison + briefing)
  |
  v
Phase 5 (router + integration + multi-product)
  |
  v
Phase 6 (data pipeline + output options + English toggle)
```

All phase transitions are mandatory sequential dependencies.
