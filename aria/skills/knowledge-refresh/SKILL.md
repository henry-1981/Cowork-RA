---
name: aria-knowledge-refresh
description: "ARIA Knowledge DB 월간 갱신 — 최신 규제 변경사항 반영"
allowed-tools:
  - WebSearch
  - WebFetch
  - Read
  - Edit
  - Bash
user-invocable: true
metadata:
  version: "0.2.0"
  category: "maintenance"
  status: "active"
  updated: "2026-02-24"
  tags: "knowledge, refresh, regulatory-update"
---

# Knowledge DB Refresh Skill

## Purpose

ARIA Knowledge DB의 규제 데이터를 월간 주기로 갱신한다. 각 knowledge 파일의 YAML frontmatter에 기록된 `next_review` 날짜를 기준으로 갱신 대상을 판별하고, 최신 규제 변경사항을 반영한다.

**Input**: None (자동 스캔)
**Output**: Change summary report

---

## Analysis Workflow

### Step 1: Review Date Check

각 knowledge 파일의 YAML frontmatter에서 `next_review` 날짜를 확인한다:

```
knowledge/regulations/fda-framework.md
knowledge/regulations/eu-mdr-framework.md
knowledge/regulations/mfds-framework.md
knowledge/shared/samd-classification.md
knowledge/shared/combination-products.md
```

- `next_review` < today → 갱신 대상
- `next_review` >= today → SKIP

### Step 2: Regulatory Update Search

갱신 대상 파일별로 관할권에 맞는 웹 검색 수행:

**FDA**:
- "FDA guidance documents [current year]"
- "FDA 510(k) policy update"
- "FDA AI/ML SaMD framework update"
- Source: fda.gov/regulatory-information/search-fda-guidance-documents

**EU MDR**:
- "MDCG guidance [current year]"
- "EU MDR implementing acts update"
- "EU AI Act medical device update"
- Source: health.ec.europa.eu/medical-devices-sector

**MFDS**:
- "식약처 의료기기 고시 개정"
- "디지털의료제품법 시행령 개정"
- "MFDS SaMD guidance update"
- Source: mfds.go.kr

**IMDRF/Shared**:
- "IMDRF SaMD guidance update"
- "IMDRF work items [current year]"

### Step 3: Update Changed Sections

변경사항이 확인된 섹션만 업데이트한다:

1. 변경된 내용을 해당 섹션에 반영
2. 인라인 소스 인용 추가: `(Source: [document name], [date])`
3. 기존 내용과 충돌 시 최신 공식 문서 우선
4. 변경 이력을 `## Revision History` 섹션에 기록

### Step 4: Metadata Update

각 갱신된 파일의 YAML frontmatter 업데이트:

```yaml
last_updated: "[today's date]"
next_review: "[today + 30 days]"
knowledge_base_date: "[current year-month]"
```

### Step 5: Change Summary Report

갱신 결과를 구조화된 리포트로 출력:

```
### Knowledge DB Refresh Report — [date]

| File | Status | Changes | Sources |
|------|--------|---------|---------|
| fda-framework.md | UPDATED / NO CHANGE | [summary] | [source list] |
| eu-mdr-framework.md | UPDATED / NO CHANGE | [summary] | [source list] |
| mfds-framework.md | UPDATED / NO CHANGE | [summary] | [source list] |
| samd-classification.md | UPDATED / NO CHANGE | [summary] | [source list] |
| combination-products.md | UPDATED / NO CHANGE | [summary] | [source list] |

**Next Review**: [today + 30 days]
```

---

## Benchmark Contamination Prevention

Knowledge DB에 아래 항목을 포함하지 않는다:

- 벤치마크 시나리오 식별자 (S-01 ~ S-09)
- 특정 제품명 (VUNO DeepBrain, IDx-DR 등)을 GROUND TRUTH 데이터로 사용 금지
- 제품 코드 매핑에 특정 회사명 포함 금지

Knowledge DB는 **규제 프레임워크와 규칙**만 포함하며, 특정 제품 사례는 스킬의 예시로만 사용한다.
