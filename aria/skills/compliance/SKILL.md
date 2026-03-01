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
  version: "0.4.0"
  category: "domain"
  status: "active"
  updated: "2026-02-28"
  modularized: "true"
  tags: "compliance, fair-competition, KMDIA, marketing, anti-kickback, Korea"
  knowledge-base-date: "2024-07"

# MoAI Extension: Progressive Disclosure
progressive_disclosure:
  enabled: true
  level1_tokens: 100
  level2_tokens: 4000

# MoAI Extension: Triggers
triggers:
  keywords: ["compliance", "fair competition", "KMDIA", "리베이트", "공정경쟁규약",
             "마케팅 컴플라이언스", "심의 체크", "컴플라이언스 체크", "사전심의",
             "사후신고 준비", "활동 검토", "compliance check"]
  phases: ["run"]
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

**Topic files** (`topics/`): Each topic file contains ALL relevant content for one article, with standardized section structure:

| Section Header | Content |
|---------------|---------|
| `## 공정경쟁규약` | 공정경쟁규약 본문 조항 (verbatim) |
| `## 공정경쟁규약 세부지침` | 세부운용기준 조항 (verbatim) |
| `## 공정경쟁규약 심의위원회 내부규정 주요 내부지침` | 심의위 override 규칙 (해당 시) |
| `## FAQ` | 토픽별 FAQ (verbatim) |
| `## 배포본 해설` | 안내서 배포본의 해설 요약 (해당 시) |
| `## 의료기기 공정경쟁규약 심의 Compliance Checklist` | 안내서 원문 체크리스트 표 (해당 활동만) |

**Metadata** (`_index.yaml`): Topic-level metadata including `has_checklist`, `checklist_meta` (critical questions, evidence required), `procedure_required`, `common_procedures`.

**Precedents** (별도 파일): `공정경쟁규약-주요-위반유형-및-사례23-5-2-1.md` — 위반유형별 실제 경고조치 사례

**Common Procedures**: `topics/공통-지출보고서-가이드라인.md` — 경제적 이익 제공에 따른 지출보고서 작성 가이드라인 Ⅱ판

**KD Base Path**: `aria/knowledge/mfds/01-법령/04-공정경쟁규약/`

---

## Mode Selection

Three operating modes based on user intent:

| Mode | Trigger | Use Case |
|------|---------|----------|
| **Mode 1: Q&A** | 규정 질문, 특정 활동 허용 여부 | 단일 질문 → 즉시 답변 |
| **Mode 2: Activity Review Report** | "검토해줘", "보고서", 복수 항목 종합 평가 | 복수 항목 테이블 형식 보고서 |
| **Mode 3: Interactive Compliance Check** | "심의 체크", "컴플라이언스 체크", "사전심의 준비", "활동 검토" | 대화형 체크리스트 순차 진행 → 판정 → 서류 검토 |

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
   - The file contains regulation, committee guidance, FAQ/interpretation, and checklist in one document.
   - When 심의위원회 내부지침 section exists for the same article, its content takes precedence.

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

4. **Offer Mode 3 transition**: "정확한 판단을 위해 체크리스트를 진행하시겠습니까?"

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

The context determines judgment meaning (see Decision Matrix).

### Step 3: Topic File Read (토픽 파일 조회)

Read the matching topic file(s) from Knowledge DB:
- Path: `aria/knowledge/mfds/01-법령/04-공정경쟁규약/topics/{topic-file}.md`
- Focus on the `## 의료기기 공정경쟁규약 심의 Compliance Checklist` section for checklist questions
- Also extract key rules from `## 공정경쟁규약` and `## 공정경쟁규약 세부지침` for citation during the checklist

If multi-mapping: Read each topic file sequentially before proceeding to its checklist.

### Step 4: Sequential Checklist (체크리스트 순차 진행)

Walk through the Compliance Checklist questions from the topic file:

1. Present **1-2 questions at a time**
2. For each question, provide the regulation citation (Article number + section reference)
3. Answer options for each question:
   - **Yes**: Requirement met
   - **No**: Requirement not met
   - **확인필요** (needs confirmation): User is unsure, will verify later
4. On **No** answer: Immediately flag the violation risk and suggest correction direction
   - Cite the specific regulation clause
   - Indicate severity: whether this is a critical violation or a correctable issue
5. On **확인필요**: Note it and continue. This affects the final judgment (auto-YELLOW)
6. Continue until all checklist questions are answered

### Step 5: Judgment Determination (판정)

After all checklist questions are answered, apply the Decision Matrix:

1. Count Yes / No / 확인필요 answers
2. Check if any No answers are on critical questions (from `_index.yaml` `checklist_meta.critical_questions`)
3. Verify evidence requirements (from `_index.yaml` `checklist_meta.evidence_required`)
4. Determine GREEN / YELLOW / RED using the Decision Matrix conditions
5. Apply context-specific meaning based on the user's context (A/B/C from Step 2)

### Step 6: Follow-up Procedures (후속 절차 안내)

Present required follow-up procedures:

1. **Common procedure** (all activities): 지출보고서 작성
   - Reference: `topics/공통-지출보고서-가이드라인.md`
   - Read this file and summarize key requirements

2. **Activity-specific procedures** (from `_index.yaml` `procedure_required`):
   - 사전심의 신청 (if listed)
   - 사후신고 (if applicable)
   - Activity-specific documents (evidence_required from checklist_meta)

### Step 7: Document Review (서류 검토) — Optional

Offer to review relevant documents:

1. **Search current folder** using Glob for relevant document patterns:
   - Filenames containing: 심의, 신청서, 보고서, 계획서, 명단, 내역서, 계약서
   - Common extensions: .xlsx, .docx, .pdf, .hwp

2. **If documents found**: Present the filename(s) to the user
   - "이 파일이 맞나요? [filename]"
   - **User confirmation is mandatory** — never auto-review without explicit confirmation

3. **If user confirms**: Read the file and perform basic review:
   - Required field completeness (필수 항목 누락 여부)
   - Amount limits compliance (금액 한도 초과 여부)
   - Form completion (양식 완성도 — 주요 필드 기입 확인)

4. **If no documents found**: "해당 서류를 업로드해 주세요" or user can skip ("나중에")

5. **If user declines**: Mark as "미검토" in the final summary

### Step 8: Final Summary (최종 요약)

Generate the complete compliance check result using Mode 3 Response Format:
- Judgment with context-specific meaning
- Checklist results table
- Required improvements (if any)
- Follow-up procedures with completion status
- Document review status

### Step 9: Mode 2 Transition Offer

After the final summary:

> "내부 보고용 문서를 생성해 드릴까요?"

If the user accepts, transition to Mode 2 to generate a formal Activity Review Report incorporating all findings from the compliance check.

---

## Decision Framework

### Traffic-Light Conditions

Apply these conditions to determine the judgment in Mode 1, 2, and 3:

**GREEN** 🟢 — 체크리스트상 명백한 위반 사항 없음

All of the following must be true:
- All required checklist questions answered **Yes**
- All required evidence confirmed (by user report)
- Activity classification confidence **HIGH**
- Zero **확인필요** answers

**YELLOW** 🟡 — 조건부: 추가 확인 또는 보완 조치 필요

Any of the following:
- One or more **확인필요** answers
- OR unconfirmed required evidence
- OR activity classification confidence **MED** (multi-mapping)
- OR **No** answers with severity: warning (correctable, non-critical)

**RED** 🔴 — 위반 가능성: 진행 전 재검토 필요

Any of the following:
- **No** answer on a critical question (per `_index.yaml` `checklist_meta.critical_questions`)
- OR 3+ **No** answers total
- OR activity classification confidence **LOW** and unresolved

### Context-Specific Judgment Meaning (Mode 3)

| Judgment | (A) 기획 검토 | (B) 신고 준비 | (C) 사후 확인 |
|----------|-------------|-------------|-------------|
| GREEN 🟢 | 규정 요건 부합. 후속 절차 안내 | 제출 요건 충족. 진행 가능 | 적정. 기록 보관 안내 |
| YELLOW 🟡 | 조건부. 보완 사항 목록 제공 | 보완 후 제출 권장. 미비 항목 명시 | 일부 미비. 보완 조치 안내 |
| RED 🔴 | 현재 구성으로는 불가. 재설계 필요 | 제출 불가. 근본적 재검토 필요 | 위반 가능. 시정 조치 검토 |

---

## Mode Interconnection

- **Mode 1 → Mode 3**: "정확한 판단을 위해 체크리스트를 진행하시겠습니까?"
- **Mode 3 → Mode 2**: "내부 보고용 문서를 생성해 드릴까요?"

Common judgment engine (Decision Framework) + mode-specific UX. Mode 3 collects facts through interactive dialogue, Mode 1 provides quick answers, Mode 2 generates formal reports.

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
| Penalties | Art. 19-20 | Art. 18 | topics/16-위반시제재사항.md |

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

### 체크 결과
| # | 항목 | 답변 | 상태 |
|---|------|------|------|
| 1 | [질문] | Yes/No/확인필요 | OK/위반/주의 |
| ... | ... | ... | ... |

### 보완 사항 (YELLOW/RED인 경우)
1. [보완 필요 항목] (Art.N §M)
   → [시정 방향 또는 안내]

### 후속 절차
- [ ] / [x] [절차명] — [상태/안내]

### 서류 상태
| 서류 | 상태 | 비고 |
|------|------|------|
| [서류명] | 확인완료/미검토/미제출 | [비고] |

### Disclaimer
본 결과는 정보 제공 목적이며, 법적 효력이 없습니다.
GREEN 판정은 "체크리스트상 명백한 위반 사항 없음"을 의미하며, 법적 승인이 아닙니다.
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

This skill provides AI-generated reference information only and does not constitute regulatory advice, legal guidance, or official regulatory determination. All compliance decisions must be validated by qualified regulatory affairs professionals. GREEN judgment means "no apparent violation found on the checklist" — it is NOT legal approval.
