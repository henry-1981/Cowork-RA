# 공정경쟁규약 Compliance Checklist 개선 구현 계획

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** PR #27의 토픽 기반 KD 위에 Checklist 원문 통합 + Mode 3 대화형 컴플라이언스 체크 + 서류 검토 기능 추가

**Architecture:** 토픽 파일 내부에 4-계층 섹션(규정/내부지침/해설/체크리스트) 태깅, _index.yaml에 메타데이터 확장, SKILL.md에 Mode 3 워크플로 추가. DB=verbatim 원문, Skill=분석 로직 분리 원칙.

**Tech Stack:** Markdown (KD), YAML (_index.yaml), Python (extraction script), Bash (verification)

**Design Doc:** `docs/plans/2026-02-28-compliance-checklist-improvement-design.md`

---

## Prerequisites

PR #27 (`fix/fair-competition-cleanup`)이 GitHub에 머지된 상태. 작업 전:

```bash
git checkout main && git pull origin main
git checkout -b feature/compliance-checklist-improvement
```

main에 PR #27 squash commit이 반영되어 있어야 함. topics/ 디렉토리와 _index.yaml이 존재하는지 확인:

```bash
ls aria/knowledge/mfds/01-법령/04-공정경쟁규약/topics/
# 18개 파일 존재해야 함
```

---

### Task 1: 토픽 파일 섹션 헤더 정규화

**목적:** 기존 토픽 파일의 섹션 헤더를 설계 문서의 4-계층 구조로 통일

**Files:**
- Modify: `aria/knowledge/mfds/01-법령/04-공정경쟁규약/topics/*.md` (18파일)

**Step 1: 현재 토픽 파일 헤더 구조 감사**

각 토픽 파일의 현재 섹션 구조를 확인. PR #27에서 사용된 헤더 패턴:
```
# [토픽명] (규약 제N조)
## 안내서 (2022.04)
## 배포본 해설
## 배포본 FAQ
```

설계 문서의 목표 구조:
```
# Art. N [토픽명]
## 규정 (Regulation)
### 공정경쟁규약 제N조
### 세부운용기준 제N조
## 심의위원회 내부지침 (Committee Guidance)
## 규정 해설 (FAQ/Interpretation)
## Compliance Checklist
```

**Step 2: 섹션 헤더 매핑 스크립트 작성**

```bash
# scripts/normalize-topic-headers.py
```

이 스크립트가 하는 일:
1. 각 토픽 파일을 읽음
2. 기존 섹션 헤더를 새 표준 헤더로 매핑:
   - `## 안내서 (2022.04)` → `## 규정 (Regulation)` 아래 `### 공정경쟁규약 제N조` + `### 세부운용기준 제N조`
   - `## 배포본 해설` 내 심의위 내부지침 내용 → `## 심의위원회 내부지침 (Committee Guidance)`
   - `## 배포본 FAQ` → `## 규정 해설 (FAQ/Interpretation)`
3. 변환 전후 diff 출력 (검증용)
4. `--dry-run` 옵션으로 미리보기 가능

**중요**: 본문 텍스트는 절대 수정하지 않음. 섹션 헤더만 변경.

**Step 3: 스크립트 실행 (dry-run)**

```bash
python3 scripts/normalize-topic-headers.py --dry-run
# Expected: 각 파일별 헤더 변경 사항 미리보기 출력
```

**Step 4: 스크립트 실행 (적용)**

```bash
python3 scripts/normalize-topic-headers.py --apply
```

**Step 5: 원문 변경 없음 검증**

```bash
# 헤더 라인을 제외한 본문 내용이 동일한지 diff로 확인
python3 scripts/normalize-topic-headers.py --verify
# Expected: "All topic files: headers normalized, body content unchanged"
```

**Step 6: 커밋**

```bash
git add scripts/normalize-topic-headers.py aria/knowledge/mfds/01-법령/04-공정경쟁규약/topics/
git commit -m "refactor(knowledge): 토픽 파일 섹션 헤더 4-계층 표준 구조로 정규화"
```

---

### Task 2: Checklist 원문 추출 및 토픽 파일에 삽입

**목적:** 안내서 원문의 Compliance Checklist 표를 해당 토픽 파일 끝에 verbatim 삽입

**Files:**
- Read: `aria/knowledge/mfds/01-법령/04-공정경쟁규약/의료기기-리베이트-예방-및-공정경쟁을-위한-안내서2022-04.md` (lines 1425+)
- Modify: `aria/knowledge/mfds/01-법령/04-공정경쟁규약/topics/03-견본품.md`
- Modify: `aria/knowledge/mfds/01-법령/04-공정경쟁규약/topics/04-기부행위.md`
- Modify: `aria/knowledge/mfds/01-법령/04-공정경쟁규약/topics/05-학술대회개최지원.md`
- Modify: `aria/knowledge/mfds/01-법령/04-공정경쟁규약/topics/06-학술대회참가지원.md`
- Modify: `aria/knowledge/mfds/01-법령/04-공정경쟁규약/topics/07-자사제품설명회.md`
- Modify: `aria/knowledge/mfds/01-법령/04-공정경쟁규약/topics/08-교육훈련.md`
- Modify: `aria/knowledge/mfds/01-법령/04-공정경쟁규약/topics/09-강연및자문.md`
- Modify: `aria/knowledge/mfds/01-법령/04-공정경쟁규약/topics/10-임상시험지원.md`
- Modify (추가): `aria/knowledge/mfds/01-법령/04-공정경쟁규약/topics/12-시판후조사.md`

**Step 1: Checklist 라인 범위 매핑 작성**

`scripts/fair-competition-checklist-map.yaml` 생성:

```yaml
# 안내서 원문에서 Checklist 표의 라인 범위 매핑
source: "aria/knowledge/mfds/01-법령/04-공정경쟁규약/의료기기-리베이트-예방-및-공정경쟁을-위한-안내서2022-04.md"

checklists:
  - topic_file: "topics/04-기부행위.md"
    article: 7
    source_lines: [1427, 1435]
    questions: 8
  - topic_file: "topics/03-견본품.md"
    article: 6
    source_lines: [1436, 1450]
    questions: 11
  - topic_file: "topics/05-학술대회개최지원.md"
    article: 8
    source_lines: [1451, 1458]
    questions: 7
  - topic_file: "topics/06-학술대회참가지원.md"
    article: 9
    source_lines: [1459, 1482]
    questions: 10
  - topic_file: "topics/07-자사제품설명회.md"
    article: 10
    source_lines: [1483, 1508]
    questions: 16
  - topic_file: "topics/08-교육훈련.md"
    article: 11
    source_lines: [1509, 1539]
    questions: 14
  - topic_file: "topics/09-강연및자문.md"
    article: 12
    source_lines: [1540, 1548]
    questions: 7
  - topic_file: "topics/10-임상시험지원.md"
    article: 13
    source_lines: [1549, 1566]
    questions: 8
  - topic_file: "topics/12-시판후조사.md"
    article: 15
    source_lines: [1567, 1597]
    questions: 13
```

> **주의**: 라인 번호는 근사치. 실제 추출 시 안내서 원문을 직접 확인하여 정확한 범위를 조정해야 함.

**Step 2: 추출 스크립트 작성**

```bash
# scripts/extract-checklists.py
```

이 스크립트가 하는 일:
1. `fair-competition-checklist-map.yaml` 읽음
2. 안내서 원문에서 해당 라인 범위의 Checklist 표를 추출
3. 각 토픽 파일 끝에 `## Compliance Checklist` 헤더와 함께 verbatim 삽입
4. `--dry-run` 옵션으로 미리보기

**Step 3: 라인 범위 검증 (dry-run)**

```bash
python3 scripts/extract-checklists.py --dry-run
# Expected: 각 토픽 파일에 삽입될 Checklist 내용 미리보기
# 수동으로 원문 대조하여 정확성 확인
```

**Step 4: 스크립트 실행 (적용)**

```bash
python3 scripts/extract-checklists.py --apply
```

**Step 5: Verbatim 검증**

```bash
python3 scripts/extract-checklists.py --verify
# Expected: 삽입된 내용이 원문 해당 라인과 byte-for-byte 동일
```

**Step 6: 커밋**

```bash
git add scripts/fair-competition-checklist-map.yaml scripts/extract-checklists.py
git add aria/knowledge/mfds/01-법령/04-공정경쟁규약/topics/
git commit -m "feat(knowledge): 토픽 파일에 Compliance Checklist 원문 verbatim 삽입 (9개 활동유형)"
```

---

### Task 3: 지출보고서 가이드라인 추출

**목적:** 안내서 Part 2의 지출보고서 작성 가이드라인을 별도 파일로 추출 (전 활동 공통 참조)

**Files:**
- Read: `aria/knowledge/mfds/01-법령/04-공정경쟁규약/의료기기-리베이트-예방-및-공정경쟁을-위한-안내서2022-04.md` (Part 2 영역)
- Create: `aria/knowledge/mfds/01-법령/04-공정경쟁규약/topics/공통-지출보고서-가이드라인.md`

**Step 1: Part 2 영역 확인**

안내서에서 "경제적 이익 제공에 따른 지출보고서 작성 가이드라인 Ⅱ판" 섹션의 시작/끝 라인 확인.

**Step 2: 추출 및 파일 생성**

```markdown
---
topic: "공통-지출보고서-가이드라인"
title: "경제적 이익 제공에 따른 지출보고서 작성 가이드라인 Ⅱ판"
type: COMMON_PROCEDURE
sources: [framework]
---

# 경제적 이익 제공에 따른 지출보고서 작성 가이드라인 Ⅱ판

[안내서 Part 2 해당 섹션 verbatim]
```

**Step 3: 커밋**

```bash
git add aria/knowledge/mfds/01-법령/04-공정경쟁규약/topics/공통-지출보고서-가이드라인.md
git commit -m "feat(knowledge): 지출보고서 가이드라인 Ⅱ판 공통 참조 파일 추출"
```

---

### Task 4: 중복 제거 — 배포본 삭제

**목적:** 배포본(요약판)은 원본 안내서와 중복이므로 삭제

**Files:**
- Delete: `aria/knowledge/mfds/01-법령/04-공정경쟁규약/의료기기-리베이트-예방-및-공정거래를-위한-안내서-배포본.md`

**Step 1: 배포본이 토픽 파일에서 참조되는지 확인**

```bash
grep -r "배포본" aria/knowledge/mfds/01-법령/04-공정경쟁규약/topics/ || echo "No references found"
grep -r "배포본" aria/skills/compliance/ || echo "No references found"
```

배포본 해설 내용이 이미 토픽 파일에 통합되어 있으면 삭제 안전.

**Step 2: 토픽 파일 내 "배포본 해설" 섹션 처리**

Task 1의 헤더 정규화에서 `## 배포본 해설` 내용이 적절한 섹션(규정/내부지침)으로 이동되었는지 확인. 중복 내용은 제거하되, 고유 내용(예: 심의위 해석)은 보존.

**Step 3: 삭제 및 커밋**

```bash
git rm aria/knowledge/mfds/01-법령/04-공정경쟁규약/의료기기-리베이트-예방-및-공정거래를-위한-안내서-배포본.md
git commit -m "refactor(knowledge): 배포본(요약판) 삭제 — 원본 안내서 + 토픽 파일로 대체"
```

---

### Task 5: _index.yaml 확장

**목적:** checklist_meta, procedure_required, common_procedures 메타데이터 추가

**Files:**
- Modify: `aria/knowledge/mfds/01-법령/04-공정경쟁규약/_index.yaml`

**Step 1: 현재 _index.yaml 확인**

PR #27의 기존 구조를 읽고, 설계 문서 Section 2.2의 목표 구조와 비교.

**Step 2: 메타데이터 확장**

설계 문서의 `_index.yaml` 구조를 그대로 적용:
- `sections`: 섹션 헤딩 패턴 정의
- 각 토픽에 `has_checklist`, `faq_range`, `procedure_required`, `checklist_meta` 추가
- `common_procedures`: 지출보고서, 사전심의, 사후신고

**Step 3: YAML 구문 검증**

```bash
python3 -c "import yaml; yaml.safe_load(open('aria/knowledge/mfds/01-법령/04-공정경쟁규약/_index.yaml'))"
# Expected: No errors
```

**Step 4: 커밋**

```bash
git add aria/knowledge/mfds/01-법령/04-공정경쟁규약/_index.yaml
git commit -m "feat(knowledge): _index.yaml에 checklist 메타데이터 + 절차 정보 확장"
```

---

### Task 6: references/ 디렉토리 제거

**목적:** LLM 요약된 참조 파일 제거 — 토픽 파일이 완전 대체

**Files:**
- Delete: `aria/skills/compliance/references/regulation.md`
- Delete: `aria/skills/compliance/references/activity-guide.md`
- Delete: `aria/skills/compliance/references/faq.md`
- Delete: `aria/skills/compliance/references/` (디렉토리)

**Step 1: SKILL.md에서 references/ 참조 확인**

```bash
grep -n "references/" aria/skills/compliance/SKILL.md
```

Mode 1/2에서 references/ 파일을 참조하는 부분이 있으면 Task 7에서 함께 수정.

**Step 2: 삭제 및 커밋**

```bash
git rm -r aria/skills/compliance/references/
git commit -m "refactor(compliance): references/ 제거 — 토픽 KD 직접 참조로 전환"
```

---

### Task 7: SKILL.md 재작성 — Mode 3 추가

**목적:** Interactive Compliance Check 워크플로, 판정 매트릭스, 서류 검토 흐름 추가

**Files:**
- Modify: `aria/skills/compliance/SKILL.md`

**Step 1: 현재 SKILL.md 전체 읽기**

현재 구조 파악 (Mode 1, Mode 2, Article Index, Decision Framework, Response Format).

**Step 2: SKILL.md 수정 — 핵심 변경사항**

**(a) metadata 업데이트**
```yaml
metadata:
  version: "0.4.0"  # Mode 3 추가 = minor bump
  updated: "2026-02-28"
```

**(b) triggers 확장**
```yaml
triggers:
  keywords: ["compliance", "fair competition", "KMDIA", "리베이트", "공정경쟁규약",
             "마케팅 컴플라이언스", "심의 체크", "컴플라이언스 체크", "사전심의",
             "사후신고 준비", "활동 검토", "compliance check"]
```

**(c) Assessment Workflow에 Mode 3 추가**

```markdown
### Mode 3: Interactive Compliance Check (대화형 컴플라이언스 심의)

When a user requests a compliance check or wants to prepare for review:

1. Identify the activity type from user description
   - Map to Article 5-17 using Article Index
   - If borderline: present 2-3 candidates with distinguishing criteria, ask user to select
   - If multi-type: announce both, process sequentially

2. Confirm user context:
   - (A) Planning phase — pre-activity review
   - (B) Filing preparation — pre-submission final check
   - (C) Post-activity — compliance verification

3. Read the matching topic file(s) from Knowledge DB
   - Read: `aria/knowledge/mfds/01-법령/04-공정경쟁규약/topics/{topic}.md`
   - Focus on: ## Compliance Checklist section

4. Walk through Checklist questions sequentially:
   - Present 1-2 questions at a time
   - For each question, provide regulation citation (Article + section)
   - Answer options: Yes / No / 확인필요 (needs confirmation)
   - On No: immediately flag violation risk + suggest correction
   - On 확인필요: note and continue, affects final judgment

5. After Checklist completion, determine judgment:
   - Apply Decision Matrix (see below)
   - Provide context-appropriate judgment meaning

6. Present required follow-up procedures:
   - Common: 지출보고서 (refer to 공통-지출보고서-가이드라인.md)
   - Activity-specific: from _index.yaml procedure_required

7. Offer document review (optional):
   - Search current folder for relevant documents (Glob)
   - If found: present filename, ask user to confirm before reviewing
   - If not found: offer upload option
   - Review scope: required field completeness, amount limits, form completion
   - If user declines: mark as "unreviewed"

8. Provide final summary: judgment + procedures + document status

9. Offer Mode 2 transition: "내부 보고용 문서를 생성해 드릴까요?"
```

**(d) Decision Matrix 추가**

```markdown
## Decision Matrix (Mode 3)

### Judgment Conditions

GREEN (체크리스트상 명백한 위반 사항 없음) — all of:
  - All required questions answered Yes
  - All required evidence confirmed (by user report)
  - Classification confidence HIGH
  - Zero "확인필요" answers

YELLOW (조건부 — 추가 확인/조치 필요) — any of:
  - One or more "확인필요" answers
  - OR unconfirmed required evidence
  - OR classification confidence MED (multi-mapping)
  - OR No answers with severity: warning (correctable)

RED (위반 가능성 — 진행 전 재검토 필요) — any of:
  - No answer on critical question (per _index.yaml checklist_meta.critical_questions)
  - OR 3+ No answers total
  - OR classification confidence LOW + unresolved

### Context-Specific Judgment Meaning

| Judgment | (A) Planning | (B) Filing Prep | (C) Post-Activity |
|----------|-------------|----------------|-------------------|
| GREEN | Requirements met. Proceed to filing procedures | Submission ready. Go ahead | Compliant. Maintain records |
| YELLOW | Conditional. Fix items listed | Fix before filing. Items listed | Partially compliant. Remediate |
| RED | Not viable as designed. Redesign needed | Cannot file. Fundamental review needed | Potential violation. Corrective action needed |
```

**(e) Article Index 업데이트**

references/ 대신 topics/ 파일 참조로 변경:

```markdown
| Activity | Regulation | Operating Standard | Reference |
|----------|-----------|-------------------|-----------|
| Gifts/Benefits restriction | Art. 5 | Art. 2 | topics/02-금품류제공제한.md |
| Samples | Art. 6 | Art. 3 | topics/03-견본품.md |
...
```

**(f) Mode 간 연계 섹션 추가**

```markdown
## Mode Interconnection

- Mode 1 → Mode 3: "정확한 판단을 위해 체크리스트를 진행하시겠습니까?"
- Mode 3 → Mode 2: "내부 보고용 문서를 생성해 드릴까요?"

Common judgment engine + mode-specific UX. Mode 3 collects facts, Mode 1/2 present results.
```

**(g) Disclaimer 강화**

기존 Disclaimer에 추가:
```markdown
GREEN 판정은 "체크리스트상 명백한 위반 사항 없음"을 의미하며, 법적 승인이 아닙니다.
```

**Step 3: SKILL.md 저장 후 문법 검증**

```bash
# YAML frontmatter 파싱 확인
python3 -c "
import yaml
with open('aria/skills/compliance/SKILL.md') as f:
    content = f.read()
    fm = content.split('---')[1]
    yaml.safe_load(fm)
    print('Frontmatter OK')
"
```

**Step 4: 커밋**

```bash
git add aria/skills/compliance/SKILL.md
git commit -m "feat(compliance): SKILL.md 0.4.0 — Mode 3 대화형 체크리스트 + 판정 매트릭스 + 서류 검토"
```

---

### Task 8: 버전 + CHANGELOG + README 업데이트

**Files:**
- Modify: `aria/.claude-plugin/plugin.json` — version bump
- Modify: `.claude-plugin/marketplace.json` — version sync
- Modify: `aria/CHANGELOG.md` — 새 엔트리
- Modify: `aria/README.md` — Mode 3 기능 설명 추가
- Modify: `aria/CLAUDE.md` — Knowledge DB 섹션 현행화

**Step 1: 버전 bump**

`plugin.json`과 `marketplace.json` 모두 `0.3.8` → `0.4.0` (또는 현재 최신 + minor)

**Step 2: CHANGELOG 엔트리**

```markdown
## 0.4.0 (2026-02-28)

### Added
- **Mode 3: Interactive Compliance Check** — 대화형 체크리스트 기반 컴플라이언스 심의
  - 활동유형 자동 분류 (다중 매핑 지원)
  - 맥락별 판정 (기획검토/신고준비/사후확인)
  - GREEN/YELLOW/RED 신호등 판정 매트릭스
  - Cowork 폴더 연동 서류 검토
- **Compliance Checklist** — 안내서 원문 9개 활동유형 체크리스트 DB 통합
- **지출보고서 가이드라인** — 전 활동 공통 절차 참조 파일
- **_index.yaml 확장** — checklist_meta, procedure_required, common_procedures

### Changed
- 토픽 파일 섹션 헤더 4-계층 표준화 (규정/내부지침/해설/체크리스트)
- Mode 1→3→2 자연스러운 전환 흐름

### Removed
- `references/` 디렉토리 (regulation.md, activity-guide.md, faq.md) — 토픽 KD로 완전 대체
- 배포본(요약판) 파일 — 원본과 중복
```

**Step 3: CLAUDE.md 현행화**

`aria/CLAUDE.md`의 Knowledge DB 섹션에서 04-공정경쟁규약 설명 업데이트:
```
- `01-법령/04-공정경쟁규약/` — 토픽별 18파일 (4-계층: 규정/내부지침/해설/체크리스트) + 지출보고서 가이드라인 + 위반사례
```

**Step 4: 커밋**

```bash
git add aria/.claude-plugin/plugin.json .claude-plugin/marketplace.json
git add aria/CHANGELOG.md aria/README.md aria/CLAUDE.md
git commit -m "chore(aria): 버전 0.4.0 — Mode 3 Compliance Checklist + 서류 검토"
```

---

### Task 9: 검증

**Step 1: Knowledge DB 구조 검증**

```bash
./scripts/verify-knowledge-db.sh --scope mfds --stage 3
# Expected: Stage 3 (Structural Checker) 통과
# 체크: frontmatter 완전성, 빈 파일 없음, 인코딩 정상
```

**Step 2: 버전 정책 검증**

```bash
python3 scripts/versioning/check_version_policy.py --base-ref origin/main
# Expected: 통과 (allow-major-minor 라벨 필요할 수 있음)
```

**Step 3: _index.yaml 무결성**

```bash
python3 -c "
import yaml, os
idx = yaml.safe_load(open('aria/knowledge/mfds/01-법령/04-공정경쟁규약/_index.yaml'))
topics = idx['topics']
for t in topics:
    path = os.path.join('aria/knowledge/mfds/01-법령/04-공정경쟁규약', t['file'])
    assert os.path.exists(path), f'Missing: {path}'
    if t.get('has_checklist'):
        with open(path) as f:
            assert '## Compliance Checklist' in f.read(), f'Missing checklist in {path}'
print(f'All {len(topics)} topics verified')
"
```

**Step 4: Checklist verbatim 대조**

```bash
python3 scripts/extract-checklists.py --verify
# Expected: 각 토픽 파일의 Checklist 섹션이 원문과 동일
```

**Step 5: SKILL.md frontmatter 유효성**

```bash
python3 -c "
import yaml
with open('aria/skills/compliance/SKILL.md') as f:
    content = f.read()
    fm = content.split('---')[1]
    d = yaml.safe_load(fm)
    assert d['metadata']['version'] == '0.4.0'
    print('SKILL.md metadata OK')
"
```

**Step 6: 검증 결과 기록 및 커밋**

모든 검증 통과 후:

```bash
git add -A
git commit -m "chore: 전체 검증 통과 확인"
```

---

### Task 10: E2E 테스트 — Mode 3 시나리오

**목적:** Mode 3 흐름이 실제로 동작하는지 수동 E2E 테스트

**시나리오 1: 단일 활동 (자사제품설명회)**

프롬프트: "다음 주에 병원에서 자사 의료기기 제품설명회를 개최하려고 합니다. 컴플라이언스 체크를 해주세요."

기대 결과:
1. Art. 10 자사제품설명회로 분류
2. 맥락 확인 질문 (기획검토)
3. topics/07-자사제품설명회.md Read
4. 16개 Checklist 질문 순차 진행
5. 판정 + 후속 절차 (사전심의 + 지출보고서) 안내
6. 서류 검토 제안

**시나리오 2: 복합 활동 (학술대회 + 제품설명회)**

프롬프트: "학술대회에서 부스를 설치하고 제품 시연도 하면서 참석자에게 점심도 제공하려 합니다."

기대 결과:
1. 다중 매핑: Art. 8 (학술대회) + Art. 10 (제품설명회) + Art. 5 (금품류)
2. 사용자 확인 후 순차 진행
3. 각 토픽 Checklist 순차 실행
4. 종합 판정

---

## Task 의존성 그래프

```
Task 1 (헤더 정규화)
  ↓
Task 2 (Checklist 삽입) ← Task 1 완료 후 진행
  ↓
Task 3 (지출보고서) ← 독립, Task 2와 병렬 가능
  ↓
Task 4 (배포본 삭제) ← Task 1, 2 완료 후 (배포본 내용이 이전됨 확인)
  ↓
Task 5 (_index.yaml) ← Task 2, 3 완료 후 (checklist 존재 확인)
  ↓
Task 6 (references/ 제거) ← Task 7과 함께 (SKILL.md에서 참조 제거)
  ↓
Task 7 (SKILL.md Mode 3) ← Task 5 완료 후 (_index.yaml 구조 확정)
  ↓
Task 8 (버전 + 문서) ← Task 7 완료 후
  ↓
Task 9 (검증) ← 모든 Task 완료 후
  ↓
Task 10 (E2E 테스트) ← Task 9 통과 후
```

**병렬 실행 가능**: Task 2 + Task 3 (독립 추출 작업)
