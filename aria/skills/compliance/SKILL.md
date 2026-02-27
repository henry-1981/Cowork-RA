---
name: aria-compliance
description: >
  Korean medical device marketing compliance advisor based on KMDIA Fair
  Competition Code (의료기기 거래에 관한 공정경쟁규약). Evaluates marketing
  activities against the Code and provides traffic-light guidance (GREEN/YELLOW/RED)
  to help users make informed compliance decisions. Triggers: medical device
  compliance, 공정경쟁규약, 리베이트, 보건의료인, 마케팅 활동 검토, KMDIA
allowed-tools: Read Grep Glob
user-invocable: false
metadata:
  version: "0.3.0"
  category: "domain"
  status: "active"
  updated: "2026-02-27"
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
  keywords: ["compliance", "fair competition", "KMDIA", "리베이트", "공정경쟁규약", "마케팅 컴플라이언스"]
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

This skill reads from the topic-based 공정경쟁규약 Knowledge DB at `aria/knowledge/mfds/01-법령/04-공정경쟁규약/topics/`.

Each topic file contains ALL relevant content from 3 sources (안내서, 배포본, 내부지침) merged by article:

| Source Section | Content |
|---------------|---------|
| `## 안내서 (2022.04)` | 규약 본문 + 세부운용기준 + 조항별 해설 |
| `## 배포본 해설` | 용어 정의 + 개념 설명 + 실무 체크리스트 + FAQ |
| `## 내부지침 (24.07.12 개정)` | 심의위원회 override 규칙 (해당 시) |

**Precedents** (별도 파일): `공정경쟁규약-주요-위반유형-및-사례23-5-2-1.md` — 위반유형별 실제 경고조치 사례

**KD Base Path**: `aria/knowledge/mfds/01-법령/04-공정경쟁규약/`

---

## Assessment Workflow

### Step 1: Article Mapping (조항 식별)

Identify the relevant Code article(s) from the user's question or activity description.

1. Classify the subject: HCP (보건의료인) / institution (의료기관) / non-HCP / foreign HCP
2. Map the activity to a specific article using the Article Index below
3. If the activity doesn't map to Articles 6-17, default to Article 5 (general prohibition)
4. **If information is insufficient**: List what's missing and ask the user. Do NOT proceed to Step 2.

### Step 2: Rule Lookup (규칙 조회)

1. **Read the topic file**: Use the Article Index below to find the file path. Read the entire topic file.
   - The file contains 안내서 규칙, 배포본 해설, and 내부지침 override (if applicable) in one document.
   - When 내부지침 section exists for the same article, its content takes precedence.

2. **Extract applicable rules**:
   - Monetary limits (금액 한도)
   - Frequency limits (횟수 제한)
   - Prior approval requirements (사전심의/신고)
   - Documentation requirements (증빙서류)

### Step 3: Precedent Reinforcement + Traffic-Light Guidance (사례 보강 + 신호등 안내)

1. **Check precedents**: Grep the `precedents` file for the relevant article or activity pattern.
   - If matching case exists: cite it with the outcome (경고/경징계/중징계)

2. **Determine traffic-light status**:

   - **GREEN** 🟢: Activity is clearly permitted under the Code. Standard requirements only.
     - Example: "제10조에 따라 숙박 미제공 제품설명회는 사전심의 불요"

   - **YELLOW** 🟡: Conditionally permitted OR requires additional verification. Must specify WHAT the user needs to confirm.
     - Example: "내부지침(24.07.12)상 1등급 기기 국외 교육은 추가 필요성 심사 대상. 학회 의견조회 필요."

   - **RED** 🔴: Clearly prohibited OR matches a known violation pattern. Must cite the prohibition or precedent.
     - Example: "내부지침에 따라 택시비는 대중교통 미간주. 3만원 초과 지급은 위반 사례 있음(23.05.02 마항)"

3. **Generate output** using the Response Format below.

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
| Clinical device provision | Art. 13 | - | topics/10-임상시험지원.md |
| Market research | Art. 14 | Art. 10 | topics/11-시장조사.md |
| Post-market surveillance | Art. 15 | Art. 11 | topics/12-시판후조사.md |
| Clinical activities (non-PMS) | Art. 16 | Art. 12 | topics/13-시판후외임상활동.md |
| Exhibition/Advertising | Art. 17 | Art. 13 | topics/14-전시및광고.md |
| Penalties | Art. 20 | Art. 18 | topics/17-위반시제재사항.md |

---

## Response Format

### Q&A Response

The response should be structured as follows, but delivered conversationally (not as raw template):

**1. Traffic-Light Status**
- Status: GREEN 🟢 / YELLOW 🟡 / RED 🔴
- Applicable article(s) and source

**2. Applicable Rules**
- Rule summary from framework
- Override notation if applicable: "내부지침(24.07.12 개정) 적용: ..."
- Key thresholds and conditions

**3. Related Precedents** (if any)
- Case summary from precedents file
- Outcome (경고/경징계/중징계)

**4. Action Items** (for YELLOW/RED)
- What the user needs to verify or prepare
- Required documents, approvals, or procedures

### Activity Review Report

For comprehensive review requests, use a table format:

| Item | Article | Status | Source | Notes |
|------|---------|--------|--------|-------|
| [item] | Art. X | 🟢/🟡/🔴 | 안내서/내부지침 | [detail] |

Followed by:
- Risk areas with precedent references
- Required procedures checklist
- Overall recommendation

---

## Key Principles

From Article 2 (Basic Principles), applicable to ALL activities:

1. Marketing activities must be within fair trade law and accepted business customs
2. Scientific/educational information delivery must NOT compromise HCP independence
3. Activities must take place at appropriate venues matching their purpose
4. All financial records must be accurate, transparent, and properly documented

---

## Disclaimer

This skill provides AI-generated reference information only and does not constitute regulatory advice, legal guidance, or official regulatory determination. All compliance decisions must be validated by qualified regulatory affairs professionals.
