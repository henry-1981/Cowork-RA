---
name: aria-fair-competition
description: >
  Korean medical device fair-competition review and drafting skill based on
  the KMDIA Fair Competition Code (의료기기 거래에 관한 공정경쟁규약).
  Evaluates activities against the Code, provides traffic-light guidance
  (GREEN/YELLOW/RED), and supports drafting or reviewing internal approval
  documents via Google Workspace MCP integration.
allowed-tools: Read Grep Glob google-workspace:read_document google-workspace:inspect_template google-workspace:copy_template google-workspace:fill_fields google-workspace:get_share_link
user-invocable: false
metadata:
  version: "1.0.0"
  category: "domain"
  status: "active"
  updated: "2026-03-16"
  modularized: "true"
  tags: "fair-competition, KMDIA, marketing, anti-kickback, Korea"
  knowledge-base-date: "2024-07"
---

# Medical Device Fair Competition Skill

## Purpose

Evaluate medical device marketing activities against the KMDIA Fair Competition Code and provide **traffic-light guidance** (GREEN/YELLOW/RED) to help users make informed decisions. This skill operates in two modes:

- **Draft Mode** (사업팀): Q&A guidance and internal approval document drafting via Google Docs
- **Review Mode** (법무정책실/RA팀): Regulation-based compliance review and judgment

**Input**: Marketing activity description, activity type, involved parties, or Google Docs link
**Output**: Traffic-light status (GREEN/YELLOW/RED), applicable articles with source citation, drafted documents or review findings
**Knowledge Base Date**: 2024-07

---

## Knowledge DB

This skill reads from the bundled topic-based 공정경쟁규약 reference set at `aria/skills/fair-competition/references/`.

### Topic File Hierarchy

Each topic file contains ALL relevant content for one article. Sections follow an **authority hierarchy** — upper layers override lower layers:

| Layer | Section Header | Role | Usage |
|-------|---------------|------|-------|
| 규정 | `## 공정경쟁규약` + `## 공정경쟁규약 세부지침` | 법적 근거 | 판정의 1차 근거. 금액·횟수 한도, 요건 |
| 보완 | `## 공정경쟁규약 심의위원회 내부규정 주요 내부지침` | 규정 해석/override | 해당 시 규정보다 우선 적용 |
| 실무 | `## 배포본 해설` | workflow + 실무 요약 | 활동 맥락 파악, 실무 절차 이해 |
| 해석 | `## FAQ` | 규정급 적용 예시 | edge case 판단, 시정 방향 근거 |
| 참고 | `## 의료기기 공정경쟁규약 심의 Compliance Checklist` | 안내서 원문 체크리스트 (해당 활동만) | 최종 출력에 매핑하는 참고 자료 |

> **Checklist 활용 원칙**: Checklist는 대화를 드라이브하는 도구가 아님. 규정/내부지침/FAQ 기반으로 대화를 진행하고, 확인된 내용을 최종 출력 시 체크리스트에 매핑하여 참고로 제공.

### Metadata (`_index.yaml`)

Review 시작 시 1회 Read:
- `has_checklist` — 최종 출력에 체크리스트 참고 표 포함 여부
- `checklist_meta.evidence_required` — 서류 검토 시 보조 참고 (1차 출처는 15-신고)
- `procedure_required` — 해당 활동의 필수 절차

### Cross-cutting Topics (전 활동 공통 참조)

| Topic | File | Role |
|-------|------|------|
| **사전·사후 신고사항** | `topics/15-규약의공정거래위원회신고.md` | 핵심 실무 허브: 활동별 사전신고 여부·기한·서류, 사후신고 여부·기한·서류 |
| 지출보고서 가이드라인 | `topics/공통-지출보고서-가이드라인.md` | 전 활동 공통 지출보고서 작성 기준 (가이드라인 Ⅱ판) |

> **15-신고**: 실무자에게 가장 유용한 토픽. Review Step 5(후속 절차) + Draft 정보 수집에서 반드시 참조. 활동별 필요 서류 목록의 1차 출처.

### Templates (`templates.yaml`)

Draft Mode에서 Google Docs 기안 작성 시 참조:
- `templates` — 사전심의요청서, 지출보고서 등 템플릿 정의 (doc_id, fields)
- `topic_templates` — 토픽별 사용 가능 템플릿 매핑

### Precedents

`공정경쟁규약-주요-위반유형-및-사례23-5-2-1.md` — 위반유형별 실제 경고조치 사례

### KD Base Path

`aria/skills/fair-competition/references/`

---

## Mode Selection

Two operating modes based on user intent:

| Mode | Trigger | User | Use Case |
|------|---------|------|----------|
| **Draft** | "이거 해도 돼?", 기안, 작성, 사전심의 준비, 활동 기획 | 사업팀 | Q&A + 기안 작성 → Google Docs 자동 생성 |
| **Review** | 검토, 리뷰, 적합성 확인, 체크, Google Docs 링크 | 법무정책실/RA팀 | 규정 기반 검토 → 판정 |

---

## Draft Mode (기안)

사업팀이 활동 기획 단계에서 사용. 경량 Q&A부터 기안 문서 작성까지 하나의 모드에서 처리.

### Lightweight Q&A (경량)

For quick regulatory questions ("이 활동 가능한가요?"):

**Step 1: Article Mapping**
1. Classify the subject: HCP / institution / non-HCP / foreign HCP
2. Map the activity to a specific article using the Article Index
3. If the activity doesn't map to Articles 6-17, default to Article 5
4. **If information is insufficient**: List what's missing and ask. Do NOT proceed.

**Step 2: Rule Lookup**
1. Read the topic file (Article Index → file path). The file contains 5 layers.
   - **Authority chain**: 내부지침 > 규정 > 배포본 해설 > FAQ
   - FAQ는 예시 형식이지만 규정급 해석 권위를 가짐
2. Extract applicable rules: monetary limits, frequency limits, prior approval, documentation

**Step 3: Precedent Reinforcement + Traffic-Light**
1. Grep the precedents file for the relevant article or activity pattern
2. Determine traffic-light status using the Decision Framework
3. Generate output using Draft Q&A Response Format

**Step 4: Draft Offer**
> "기안 문서를 작성해 드릴까요? (사전심의 요청서 / 지출보고서)"

### Full Draft (기안 작성)

When the user requests document drafting or accepts the draft offer:

**Step 1: Activity Classification**
- Same as Q&A Step 1 (if not already done)

**Step 2: Knowledge Load**
1. **Topic file** — 규정 요건 추출
2. **`topics/15-규약의공정거래위원회신고.md`** — 사전/사후 신고 요건
3. **`topics/공통-지출보고서-가이드라인.md`** — 지출보고서 기준
4. **`templates.yaml`** — 해당 토픽의 템플릿 목록 확인

**Step 3: Template Inspection**
- Call `inspect_template` on the relevant template doc_id from `templates.yaml`
- Extract the actual `{{placeholder}}` field list from the Google Docs template

**Step 4: Interactive Information Gathering**
- Combine regulation requirements + template fields into a unified question list
- Ask 1-2 questions at a time, conversationally
- For each answer, validate against regulatory requirements immediately
- Flag potential issues early (e.g., amount exceeding limits)

**Step 5: Preview**
Present a pre-generation preview:
- Filled values (채워질 핵심 값)
- Empty values requiring manual input (비어있는 값)
- RA review points and cautions (주의사항)
- Traffic-light assessment

**Step 6: Document Generation**
After user confirmation ("진행해 주세요"):
1. `copy_template` — create new document from template
2. `fill_fields` — fill placeholders with gathered information
3. `get_share_link` — set sharing and return link

**Step 7: Completion Summary**
- Document link
- Unfilled fields list (from `fill_fields` response)
- Traffic-light judgment
- Required follow-up procedures (신고, 지출보고서)

---

## Review Mode (리뷰)

법무정책실/RA팀이 활동 또는 기안 문서의 규정 적합성을 검토할 때 사용.

### Step 1: Input Reception (입력 수신)

Determine input type:
- **Google Docs link/ID** → Call `read_document` to load document content
- **Text / activity description** → Process directly

Both types follow the same review process from Step 2 onward.

### Step 2: Activity Classification (활동유형 분류)

From the document content or description, identify applicable article(s):
- **Single mapping (confidence HIGH)**: Proceed directly
- **Multi-mapping (confidence MED)**: Announce all applicable types — "이 활동은 [A]와 [B] 성격을 모두 가집니다. 순차적으로 진행하겠습니다." → Process each topic sequentially
- **Uncertain (confidence LOW)**: Present 2-3 candidate types with distinguishing criteria, ask user to select

For document input: infer activity type from document content. Confirm with user if uncertain.

### Step 3: Knowledge Load (지식 로드)

Read the following in order:

1. **`_index.yaml`** — 해당 토픽의 메타데이터 추출:
   - `has_checklist`, `procedure_required`, `checklist_meta`

2. **Topic file** — Article Index로 경로 확인 후 전체 Read:
   - 규정 + 세부지침 → 핵심 요건 추출
   - 내부지침 → override 규칙 확인
   - 배포본 해설 → workflow 맥락 파악
   - FAQ → 적용 예시 참조

3. **`topics/15-규약의공정거래위원회신고.md`** — 해당 활동의:
   - 사전신고 여부 + 기한 + 필요 서류
   - 사후신고 여부 + 기한 + 필요 서류

4. **`topics/공통-지출보고서-가이드라인.md`** — 전 활동 공통 지출보고서 작성 기준

If multi-mapping: `_index.yaml`, `15-신고`, `지출보고서 가이드라인`은 세션 1회만 Read. Topic file만 매핑별 반복 Read.

### Step 4: Regulation-Based Review (규정 기반 핵심 요건 확인)

Conduct an interactive review based on loaded knowledge:

1. **Extract key requirements** from 규정 + 세부지침 + 내부지침:
   - 금액 한도 (monetary limits)
   - 횟수/기간 제한 (frequency/duration limits)
   - 대상 제한 (eligible recipients)
   - 사전 승인/심의 요건 (prior approval requirements)
   - 서류/증빙 요건 (documentation requirements)

2. **Verify each requirement conversationally**:
   - Present 1-2 key requirements at a time
   - Cite the regulation source (Article number + section)
   - For document input: cross-reference document field values against requirements directly
   - User answers: Yes (충족) / No (미충족) / 확인필요 (미확인)

3. **On No answer**: Flag the risk immediately
   - Cite the specific regulation clause
   - Reference FAQ if a similar case exists — suggest correction direction
   - Indicate severity: critical violation vs correctable issue

4. **On 확인필요**: Note it and continue. Affects final judgment (auto-YELLOW)

5. **Use 배포본 해설** for workflow context when guiding through practical steps

### Step 5: Follow-up Procedures (후속 절차 안내)

Present required follow-up procedures:

1. **사전/사후 신고** (from `topics/15-규약의공정거래위원회신고.md`):
   - 사전신고 필요 여부, 기한, 필요 서류
   - 사후신고 필요 여부, 기한, 필요 서류

2. **지출보고서** (all activities):
   - Reference: `topics/공통-지출보고서-가이드라인.md`
   - Summarize key requirements

3. **Activity-specific procedures** (from `_index.yaml` `procedure_required`):
   - Additional procedures beyond 신고 and 지출보고서

### Step 6: Judgment Determination (판정)

After the interactive review and procedure check:

1. Assess confirmed requirements vs violations from Step 4
2. Factor in unresolved items (확인필요)
3. Factor in 신고/서류 준비 상태 from Step 5
4. Determine GREEN / YELLOW / RED using the Decision Framework

**Multi-mapping 판정 통합**: 토픽별로 개별 판정 후, 전체 판정은 가장 심각한 결과를 따름 (RED > YELLOW > GREEN). 각 토픽별 판정도 최종 요약에 표시.

### Step 7: Final Summary (최종 요약)

Generate the Review Summary using the Review Response Format:
- Judgment with rationale
- Key findings from the review
- Required improvements (if any)
- Follow-up procedures with 신고 기한
- If `has_checklist: true`: Compliance Checklist reference table

---

## Decision Framework

### Traffic-Light Conditions

Apply these conditions based on review findings (both Draft and Review modes):

**GREEN** — 확인된 범위 내 명백한 위반 사항 없음

All of the following must be true:
- All key regulatory requirements confirmed as met
- Required evidence confirmed (by user report)
- Activity classification confidence **HIGH**
- Zero **확인필요** answers
- 필수 신고 절차 확인됨 (사전신고 완료 또는 기한 내)

**YELLOW** — 조건부: 추가 확인 또는 보완 조치 필요

Any of the following:
- One or more **확인필요** answers
- OR unconfirmed required evidence
- OR activity classification confidence **MED** (multi-mapping)
- OR requirement violations that are correctable (non-critical)
- OR 필수 서류 미확보 (준비 가능한 상태)
- OR 신고기한 임박 (보완 후 제출 가능)

**RED** — 위반 가능성: 진행 전 재검토 필요

Any of the following:
- Critical regulatory requirement violated (금액 한도 초과, 대상 제한 위반 등)
- OR 3+ requirement violations total
- OR activity classification confidence **LOW** and unresolved
- OR 신고기한 경과 (사전신고 필수 활동에서 미신고 상태로 진행)

### Context-Specific Judgment Meaning

| Judgment | 기획 검토 (Draft) | 신고/제출 준비 | 사후 확인 |
|----------|----------------|-------------|----------|
| GREEN | 규정 요건 부합. 후속 절차 안내 | 제출 요건 충족. 진행 가능 | 적정. 기록 보관 안내 |
| YELLOW | 조건부. 보완 사항 목록 제공 | 보완 후 제출 권장. 미비 항목 명시 | 일부 미비. 보완 조치 안내 |
| RED | 현재 구성으로는 불가. 재설계 필요 | 제출 불가. 근본적 재검토 필요 | 위반 가능. 시정 조치 검토 |

---

## Article Index

| Activity | Code Article | Operating Standard | File |
|----------|-------------|-------------------|------|
| Gifts/Benefits restriction | Art. 5 | Art. 2 | topics/02-금품류제공제한.md |
| Samples | Art. 6 | Art. 3 | topics/03-견본품.md |
| Donations | Art. 7 | Art. 4 | topics/04-기부행위.md |
| Conference hosting support | Art. 8 | Art. 5 | topics/05-학술대회개최지원.md |
| Conference attendance support | Art. 9 | Art. 6 | topics/06-학술대회참가지원.md |
| Product presentations | Art. 10 | Art. 7 | topics/07-자사제품설명회.md |
| Education/Training | Art. 11 | Art. 8 | topics/08-교육훈련.md |
| Lectures/Consulting | Art. 12 | Art. 9 | topics/09-강연및자문.md |
| Clinical device provision | Art. 13 | — | topics/10-임상시험지원.md |
| Market research | Art. 14 | Art. 10 | topics/11-시장조사.md |
| Post-market surveillance | Art. 15 | Art. 11 | topics/12-시판후조사.md |
| Clinical activities (non-PMS) | Art. 16 | Art. 12 | topics/13-시판후외임상활동.md |
| Exhibition/Advertising | Art. 17 | Art. 13 | topics/14-전시및광고.md |
| Prior/post filing requirements | Art. 18 | — | topics/15-규약의공정거래위원회신고.md |
| Penalties + Committee | Art. 19-20 | Art. 18 | topics/16-위반시제재사항.md |

---

## Response Format

### Draft Q&A Response

The response should be structured as follows, but delivered conversationally:

**1. Traffic-Light Status**
- Status: GREEN / YELLOW / RED
- Applicable article(s) and source

**2. Applicable Rules**
- Rule summary from the topic file
- Override notation if applicable: "내부지침(24.07.12 개정) 적용: ..."
- Key thresholds and conditions

**3. Related Precedents** (if any)
- Case summary from precedents file
- Outcome (경고/경징계/중징계)

**4. Action Items** (for YELLOW/RED)
- What the user needs to verify or prepare

**5. Draft Offer**
- "기안 문서를 작성해 드릴까요?"

### Draft Preview Response

```
## 기안 미리보기

### 활동 유형: [활동명] (Art. N)
### 템플릿: [사전심의요청서 / 지출보고서]

### 채워질 값
| 필드 | 값 |
|------|-----|
| [field] | [value] |

### 비어있는 값 (수동 기입 필요)
- [field]: [reason or guidance]

### 주의사항
- [RA review point or regulatory caution]

### 판정: [GREEN/YELLOW/RED]

진행하시겠습니까?
```

### Draft Completion Response

```
## 기안 완료

### 문서 링크
[title](link)

### 미치환 필드
- [unfilled field list, if any]

### 판정: [GREEN/YELLOW/RED]

### 후속 절차
| 절차 | 기한 | 서류 |
|------|------|------|
| 사전신고 | [기한] | [서류] |
| 지출보고서 | — | 가이드라인 Ⅱ판 기준 |

### Disclaimer
본 기안은 AI가 작성한 초안이며, 최종 제출 전 사내 컴플라이언스 담당자의 검토가 필요합니다.
```

### Review Summary Response

```
## 컴플라이언스 검토 결과

### 활동 유형: [활동명] (Art. N)

### 판정: [GREEN/YELLOW/RED] — [맥락별 의미]

### 핵심 확인 사항
| # | 요건 | 근거 | 확인 결과 | 비고 |
|---|------|------|----------|------|
| 1 | [규정 요건] | Art.N §M | 충족/미충족/확인필요 | [상세] |

### 보완 사항 (YELLOW/RED인 경우)
1. [보완 필요 항목] (Art.N §M)
   → [시정 방향 또는 안내]

### 후속 절차 + 신고
| 절차 | 기한 | 서류 | 상태 |
|------|------|------|------|
| 사전신고 | [기한] | [서류 목록] | 완료/미완료/미해당 |
| 사후신고 | [기한] | [서류 목록] | 해당/미해당 |
| 지출보고서 | — | 가이드라인 Ⅱ판 기준 | 완료/미완료 |

### Compliance Checklist 참고 (해당 시)
> 아래는 안내서 원문 체크리스트에 대화 확인 내용을 매핑한 참고 자료입니다.

| # | 체크리스트 항목 | 확인 결과 |
|---|---------------|----------|
| 1 | [질문] | O/X/— |

### Disclaimer
본 결과는 정보 제공 목적이며, 법적 효력이 없습니다.
GREEN 판정은 "확인된 범위 내 명백한 위반 사항 없음"을 의미하며, 법적 승인이 아닙니다.
최종 결정은 사내 컴플라이언스 책임자의 검토를 거쳐야 합니다.
```

---

## Key Principles

From Article 2 (Basic Principles), applicable to ALL activities:

1. Marketing activities must be within fair trade law and accepted business customs
2. Scientific/educational information delivery must NOT compromise HCP independence
3. Activities must take place at appropriate venues matching their purpose
4. All financial records must be accurate, transparent, and properly documented

---

## Disclaimer

This skill provides AI-generated reference information only and does not constitute regulatory advice, legal guidance, or official regulatory determination. All compliance decisions must be validated by qualified regulatory affairs professionals. GREEN judgment means "no apparent violation found within confirmed scope" — it is NOT legal approval.
