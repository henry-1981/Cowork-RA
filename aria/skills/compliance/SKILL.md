---
name: aria-compliance
description: >
  Korean medical device marketing compliance advisor based on KMDIA Fair
  Competition Code (의료기기 거래에 관한 공정경쟁규약). Evaluates marketing
  activities against the Code and provides traffic-light guidance (GREEN/YELLOW/RED)
  to help users make informed compliance decisions. Supports Q&A (Mode 1),
  Report generation (Mode 2), and Interactive Compliance Check (Mode 3).
allowed-tools: Read Grep Glob
user-invocable: false
metadata:
  version: "0.5.0"
  category: "domain"
  status: "active"
  updated: "2026-03-02"
  modularized: "true"
  tags: "compliance, fair-competition, KMDIA, marketing, anti-kickback, Korea"
  knowledge-base-date: "2024-07"
---

# Medical Device Marketing Compliance Skill

## Purpose

Evaluate medical device marketing activities against the KMDIA Fair Competition Code and provide **traffic-light guidance** (GREEN/YELLOW/RED) to help users make informed compliance decisions. This skill does NOT make final regulatory determinations — it organizes applicable rules, precedents, and conditions so the user can judge.

**Input**: Marketing activity description, activity type, involved parties
**Output**: Traffic-light status (GREEN/YELLOW/RED), applicable articles with source citation, related precedents, action items for user
**Knowledge Base Date**: 2024-07

---

## Knowledge DB

This skill reads from the topic-based 공정경쟁규약 Knowledge DB at `aria/knowledge/mfds/01-법령/04-공정경쟁규약/`.

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

Mode 3 시작 시 1회 Read:
- `has_checklist` — 최종 출력에 체크리스트 참고 표 포함 여부
- `checklist_meta.evidence_required` — 서류 검토 시 보조 참고 (1차 출처는 15-신고)
- `procedure_required` — 해당 활동의 필수 절차

### Cross-cutting Topics (전 활동 공통 참조)

| Topic | File | Role |
|-------|------|------|
| **사전·사후 신고사항** | `topics/15-규약의공정거래위원회신고.md` | 핵심 실무 허브: 활동별 사전신고 여부·기한·서류, 사후신고 여부·기한·서류 |
| 지출보고서 가이드라인 | `topics/공통-지출보고서-가이드라인.md` | 전 활동 공통 지출보고서 작성 기준 (가이드라인 Ⅱ판) |

> **15-신고**: 실무자에게 가장 유용한 토픽. Mode 3 Step 5(후속 절차) + Step 6(서류 검토)에서 반드시 참조. 활동별 필요 서류 목록의 1차 출처.

### Precedents

`공정경쟁규약-주요-위반유형-및-사례23-5-2-1.md` — 위반유형별 실제 경고조치 사례

### KD Base Path

`aria/knowledge/mfds/01-법령/04-공정경쟁규약/`

---

## Mode Selection

Three operating modes based on user intent:

| Mode | Trigger | Use Case |
|------|---------|----------|
| **Mode 1: Q&A** | 규정 질문, 특정 활동 허용 여부 | 단일 질문 → 즉시 답변 |
| **Mode 2: Activity Review Report** | "검토해줘", "보고서", 복수 항목 종합 평가 | 복수 항목 테이블 형식 보고서 |
| **Mode 3: Interactive Compliance Check** | "심의 체크", "컴플라이언스 체크", "사전심의 준비", "활동 검토" | 규정 기반 대화형 검토 → 판정 → 서류 검토 |

---

## Mode 1: Q&A Assessment

### Step 1: Article Mapping (조항 식별)

Identify the relevant Code article(s) from the user's question or activity description.

1. Classify the subject: HCP (보건의료인) / institution (의료기관) / non-HCP / foreign HCP
2. Map the activity to a specific article using the Article Index below
3. If the activity doesn't map to Articles 6-17, default to Article 5 (general prohibition)
4. **If information is insufficient**: List what's missing and ask the user. Do NOT proceed to Step 2.

### Step 2: Rule Lookup (규칙 조회)

1. **Read the topic file**: Use the Article Index below to find the file path. Read the entire topic file.
   - The file contains 5 layers: 규정(규약+세부지침), 내부지침, 배포본 해설, FAQ, Checklist.
   - **Authority chain**: 내부지침 > 규정 > 배포본 해설 > FAQ (해당 섹션 존재 시)
   - FAQ는 예시 형식이지만 규정급 해석 권위를 가짐 — edge case 판단 시 적극 활용

2. **Extract applicable rules**:
   - Monetary limits (금액 한도)
   - Frequency limits (횟수 제한)
   - Prior approval requirements (사전심의/신고)
   - Documentation requirements (증빙서류)

### Step 3: Precedent Reinforcement + Traffic-Light Guidance (사례 보강 + 신호등 안내)

1. **Check precedents**: Grep the precedents file for the relevant article or activity pattern.
   - If matching case exists: cite it with the outcome (경고/경징계/중징계)

2. **Determine traffic-light status** using the Decision Framework below.

3. **Generate output** using Mode 1 Response Format.

4. **Offer Mode 3 transition**: "상세 검토를 위해 대화형 컴플라이언스 체크를 진행하시겠습니까?"

---

## Mode 2: Activity Review Report

For comprehensive review requests with multiple items, generate a table-format report.

### Workflow

1. Identify all activities mentioned by the user
2. Map each to the corresponding Article using the Article Index
3. Read the relevant topic files for each activity
4. Check precedents for each activity
5. Determine traffic-light status per item using the Decision Framework
6. Generate the report using Mode 2 Response Format

---

## Mode 3: Interactive Compliance Check (대화형 컴플라이언스 심의)

When a user requests a compliance check or wants to prepare for review/filing.

### Step 1: Activity Classification (활동유형 분류)

From the user's activity description, identify the applicable article(s):

- **Single mapping (confidence HIGH)**: Proceed directly to Step 2
- **Multi-mapping (confidence MED)**: Announce all applicable types — "이 활동은 [A]와 [B] 성격을 모두 가집니다. 순차적으로 진행하겠습니다." → Process each topic sequentially
- **Uncertain (confidence LOW)**: Present 2-3 candidate types with distinguishing criteria, ask user to select

Use the Article Index below for mapping. If borderline between articles, present the distinguishing criteria and let the user choose.

### Step 2: Context Confirmation (맥락 확인)

Ask the user:

> 현재 어떤 단계인가요?
> (A) 활동 기획 중 — 사전 검토
> (B) 신고/심의 준비 중 — 제출 전 최종 점검
> (C) 이미 진행한 활동 — 사후 적정성 확인

The context determines judgment meaning (see Decision Framework).

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

Based on the loaded knowledge, conduct an interactive review:

1. **Extract key requirements** from 규정 + 세부지침 + 내부지침:
   - 금액 한도 (monetary limits)
   - 횟수/기간 제한 (frequency/duration limits)
   - 대상 제한 (eligible recipients)
   - 사전 승인/심의 요건 (prior approval requirements)
   - 서류/증빙 요건 (documentation requirements)

2. **Verify each requirement conversationally**:
   - Present 1-2 key requirements at a time
   - For each, cite the regulation source (Article number + section)
   - User answers: Yes (충족) / No (미충족) / 확인필요 (미확인)

3. **On No answer**: Flag the risk immediately
   - Cite the specific regulation clause
   - Reference FAQ if a similar case exists — suggest correction direction
   - Indicate severity: critical violation vs correctable issue

4. **On 확인필요**: Note it and continue. Affects final judgment (auto-YELLOW)

5. **Use 배포본 해설** for workflow context when guiding the user through practical steps

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

### Step 6: Document Review (서류 검토) — Optional

Derive required document list from Step 3 knowledge load:
- **Primary source**: `15-신고` topic — 사전/사후 신고 서류 목록
- **Secondary source**: `_index.yaml` `checklist_meta.evidence_required` (if exists)
- **Common**: 지출보고서

For each required document:

1. **Search current folder** using Glob:
   - Match against the derived document list
   - Common extensions: .xlsx, .docx, .pdf, .hwp

2. **If found**: "이 파일이 맞나요? [filename]"
   - **User confirmation is mandatory** — never auto-review without explicit confirmation

3. **If confirmed**: Read and perform basic review:
   - Required field completeness (필수 항목 누락 여부)
   - Amount limits compliance (금액 한도 초과 여부)
   - Form completion (양식 완성도 — 주요 필드 기입 확인)

4. **If not found**: "해당 서류를 업로드해 주세요" or user can skip ("나중에")

5. **If declined**: Mark as "미검토" in the final summary

### Step 7: Judgment Determination (판정)

After the interactive review and procedure check:

1. Assess confirmed requirements vs violations from Step 4
2. Factor in unresolved items (확인필요)
3. Factor in 신고/서류 준비 상태 from Steps 5-6
4. Determine GREEN / YELLOW / RED using the Decision Framework
5. Apply context-specific meaning based on the user's context (A/B/C from Step 2)

**Multi-mapping 판정 통합**: 토픽별로 개별 판정 후, 전체 판정은 가장 심각한 결과를 따름 (RED > YELLOW > GREEN). 각 토픽별 판정도 최종 요약에 표시.

### Step 8: Final Summary (최종 요약)

Generate the complete compliance check result using Mode 3 Response Format:
- Judgment with context-specific meaning
- Key findings from the review
- Required improvements (if any)
- Follow-up procedures with 신고 기한
- Document status
- If `has_checklist: true`: Compliance Checklist reference table — map confirmed items from the conversation to checklist questions (참고용)

### Step 9: Mode 2 Transition Offer

After the final summary:

> "내부 보고용 문서를 생성해 드릴까요?"

If the user accepts, transition to Mode 2 to generate a formal Activity Review Report incorporating all findings from the compliance check.

---

## Decision Framework

### Traffic-Light Conditions

Apply these conditions based on the interactive review findings (Mode 1, 2, and 3):

**GREEN** 🟢 — 확인된 범위 내 명백한 위반 사항 없음

All of the following must be true:
- All key regulatory requirements confirmed as met
- Required evidence confirmed (by user report)
- Activity classification confidence **HIGH**
- Zero **확인필요** answers
- 필수 신고 절차 확인됨 (사전신고 완료 또는 기한 내)

**YELLOW** 🟡 — 조건부: 추가 확인 또는 보완 조치 필요

Any of the following:
- One or more **확인필요** answers
- OR unconfirmed required evidence
- OR activity classification confidence **MED** (multi-mapping)
- OR requirement violations that are correctable (non-critical)
- OR 필수 서류 미확보 (준비 가능한 상태)
- OR 신고기한 임박 (보완 후 제출 가능)

**RED** 🔴 — 위반 가능성: 진행 전 재검토 필요

Any of the following:
- Critical regulatory requirement violated (금액 한도 초과, 대상 제한 위반 등)
- OR 3+ requirement violations total
- OR activity classification confidence **LOW** and unresolved
- OR 신고기한 경과 (사전신고 필수 활동에서 미신고 상태로 진행)

### Context-Specific Judgment Meaning (Mode 3)

| Judgment | (A) 기획 검토 | (B) 신고 준비 | (C) 사후 확인 |
|----------|-------------|-------------|-------------|
| GREEN 🟢 | 규정 요건 부합. 후속 절차 안내 | 제출 요건 충족. 진행 가능 | 적정. 기록 보관 안내 |
| YELLOW 🟡 | 조건부. 보완 사항 목록 제공 | 보완 후 제출 권장. 미비 항목 명시 | 일부 미비. 보완 조치 안내 |
| RED 🔴 | 현재 구성으로는 불가. 재설계 필요 | 제출 불가. 근본적 재검토 필요 | 위반 가능. 시정 조치 검토 |

---

## Mode Interconnection

- **Mode 1 → Mode 3**: "상세 검토를 위해 대화형 컴플라이언스 체크를 진행하시겠습니까?"
- **Mode 3 → Mode 2**: "내부 보고용 문서를 생성해 드릴까요?"

Common judgment engine (Decision Framework) + mode-specific UX. Mode 3 collects facts through regulation-based interactive dialogue, Mode 1 provides quick answers, Mode 2 generates formal reports.

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

### Mode 1: Q&A Response

The response should be structured as follows, but delivered conversationally (not as raw template):

**1. Traffic-Light Status**
- Status: GREEN 🟢 / YELLOW 🟡 / RED 🔴
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
- Required documents, approvals, or procedures

### Mode 2: Activity Review Report

For comprehensive review requests, use a table format:

| Item | Article | Status | Source | Notes |
|------|---------|--------|--------|-------|
| [item] | Art. X | 🟢/🟡/🔴 | 안내서/내부지침 | [detail] |

Followed by:
- Risk areas with precedent references
- Required procedures checklist
- Overall recommendation

### Mode 3: Interactive Compliance Check Result

```
## 컴플라이언스 체크 결과

### 활동 유형: [활동명] (Art. N)
### 맥락: [기획 검토 / 신고 준비 / 사후 확인]

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

### 서류 상태
| 서류 | 상태 | 비고 |
|------|------|------|
| [서류명] | 확인완료/미검토/미제출 | [비고] |

### Compliance Checklist 참고 (해당 시)
> 아래는 안내서 원문 체크리스트에 대화 확인 내용을 매핑한 참고 자료입니다.

| # | 체크리스트 항목 | 확인 결과 |
|---|---------------|----------|
| 1 | [질문] | ✓/✗/— |

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
