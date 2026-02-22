# ARIA Bench v2 — Skill-Activated Architecture Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** ARIA 스킬이 벤치에서 실제로 트리거되도록 SessionStart Hook + 벤치 프롬프트 개선을 구현하여 58.9% → 75%+ 달성

**Architecture:** 3-Layer Defense-in-Depth — (1) 벤치 프롬프트에 tool 사용 지시 추가 (전 멤버 동일), (2) SessionStart Hook으로 스킬 호출을 additionalContext에 주입 (100% 보장), (3) CLAUDE.md 현행 유지 (안전망). Hook 패턴은 superpowers 4.3.0 SessionStart hook과 동일.

**Tech Stack:** Bash (hook script), JSON (hook config), Markdown (bench prompts, references)

**Design Doc:** `docs/plans/2026-02-21-aria-bench-v2-design.md`

---

## Phase 1: Hook Infrastructure

### Task 1: SessionStart Hook 스크립트 생성

**Files:**
- Create: `aria/hooks/session-start.sh`

**Context:**
- 참조 패턴: `/Users/hb/.claude/plugins/cache/superpowers-marketplace/superpowers/4.3.0/hooks/session-start.sh`
- superpowers는 `escape_for_json()` 함수로 SKILL.md 내용을 JSON-safe하게 변환 후 `additionalContext`에 주입
- ARIA hook은 스킬 호출 지시를 주입해야 함

**Step 1: hook 스크립트 작성**

```bash
#!/usr/bin/env bash
# SessionStart hook for ARIA plugin
# Injects skill activation context to guarantee skill invocation in -p mode

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
PLUGIN_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

escape_for_json() {
    local s="$1"
    s="${s//\\/\\\\}"
    s="${s//\"/\\\"}"
    s="${s//$'\n'/\\n}"
    s="${s//$'\r'/\\r}"
    s="${s//$'\t'/\\t}"
    printf '%s' "$s"
}

activation_context="<ARIA_SKILL_ACTIVATION>
You are ARIA (AI Regulatory Intelligence Assistant). You have specialized regulatory skills available.

MANDATORY: Before answering any medical device regulatory question, invoke these skills in order:
1. Skill(\"aria-determination\") — 의료기기 해당 여부 판단
2. Skill(\"aria-classification\") — 등급/등급 분류
3. Skill(\"aria-pathway\") — 인허가 경로 결정

Each skill will load its own reference files and produce MANDATORY OUTPUT FORMAT blocks.
Integrate all skill outputs into your final answer. Do NOT skip skill invocation.
Do NOT answer from base knowledge alone.
</ARIA_SKILL_ACTIVATION>"

context_escaped=$(escape_for_json "$activation_context")

cat <<EOF
{
  "additional_context": "${context_escaped}",
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "${context_escaped}"
  }
}
EOF

exit 0
```

**Step 2: 스크립트 실행 권한 부여 및 검증**

Run: `chmod +x aria/hooks/session-start.sh && bash aria/hooks/session-start.sh`

Expected: Valid JSON output with `additionalContext` containing `ARIA_SKILL_ACTIVATION` block. 다음을 확인:
- JSON 파싱 가능 (`| python3 -m json.tool`)
- `additionalContext`에 3개 Skill 호출 지시 포함
- 특수문자 이스케이프 정상

**Step 3: Commit**

```bash
git add aria/hooks/session-start.sh
git commit -m "feat(aria): SessionStart hook 스크립트 — 스킬 호출 보장"
```

---

### Task 2: hooks.json 설정 파일 생성

**Files:**
- Create: `aria/hooks/hooks.json`

**Context:**
- superpowers 패턴: `hooks/hooks.json` 파일이 `hooks/` 디렉토리에 위치
- SessionStart 이벤트에 matcher 없이 (모든 세션에서 실행) hook 등록
- `${CLAUDE_PLUGIN_ROOT}`는 Claude Code가 자동 설정하는 환경변수 (plugin root dir)

**Step 1: hooks.json 작성**

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/session-start.sh"
          }
        ]
      }
    ]
  }
}
```

**Step 2: JSON 유효성 검증**

Run: `python3 -m json.tool aria/hooks/hooks.json`

Expected: Formatted JSON output without errors.

**Step 3: Commit**

```bash
git add aria/hooks/hooks.json
git commit -m "feat(aria): hooks.json — SessionStart hook 등록"
```

---

### Task 3: Hook 동작 검증 (단일 시나리오)

**Files:**
- None (검증만)

**Context:**
- 벤치 명령: `claude -p --model sonnet --plugin-dir /Users/hb/Project/Cowork-RA/aria -- "prompt"`
- Hook이 작동하면 모델 컨텍스트에 `ARIA_SKILL_ACTIVATION` 블록이 주입됨
- 검증: S-09 (가장 간단한 MFDS 시나리오)를 실행하고 트랜스크립트에서 Skill 호출 흔적 확인

**Step 1: S-09 벤치 실행**

Run:
```bash
cd /Users/hb/Project/RA-Bench && ./scripts/bench-run.sh S-09 --member aria
```

Expected: 실행 완료, `runs/2026-02-21/transcripts/aria/S-09.md` 생성 (기존 파일 덮어쓰기)

**Step 2: 트랜스크립트에서 Skill 호출 확인**

Run: 트랜스크립트 파일을 읽어서 다음을 확인:
- "Skill" 또는 "aria-determination" 등 스킬 호출 흔적이 있는가?
- MANDATORY OUTPUT FORMAT 블록 (4-Gate, Gate 2 EXIT 등)이 출력에 포함되었는가?
- 이전 트랜스크립트와 구조적 차이가 있는가?

Expected: Hook이 작동하면 스킬 호출 시도 또는 더 구조화된 출력이 관찰됨

**Step 3: 스코어링 실행**

Run:
```bash
cd /Users/hb/Project/RA-Bench && python3 scripts/bench-score.py runs/2026-02-21/
```

Expected: S-09 점수 확인. 성공 기준: S-09 ≥ 70% (기존 Phase 1 수준 유지 또는 개선)

**Step 4: 결과 판정**

- S-09 ≥ 70%: Phase 1 성공 → Phase 2 진행
- S-09 < 70%: Hook이 부작용 유발 → Hook 내용 조정 (activation 메시지 축소)
- 스킬 미트리거 but S-09 유지: Hook 주입은 성공하나 모델이 여전히 무시 → 프롬프트 개선 (Phase 2)과 함께 재검증

---

## Phase 2: Bench Prompt 개선

### Task 4: 벤치 프롬프트에 tool 사용 지시 추가

**Files:**
- Modify: `/Users/hb/Project/RA-Bench/scenarios/prompts/S-01.md` (마지막 줄 뒤에 추가)
- Modify: `/Users/hb/Project/RA-Bench/scenarios/prompts/S-02.md`
- Modify: `/Users/hb/Project/RA-Bench/scenarios/prompts/S-03.md`
- Modify: `/Users/hb/Project/RA-Bench/scenarios/prompts/S-04.md`
- Modify: `/Users/hb/Project/RA-Bench/scenarios/prompts/S-05.md`
- Modify: `/Users/hb/Project/RA-Bench/scenarios/prompts/S-06.md`
- Modify: `/Users/hb/Project/RA-Bench/scenarios/prompts/S-07.md`
- Modify: `/Users/hb/Project/RA-Bench/scenarios/prompts/S-08.md`
- Modify: `/Users/hb/Project/RA-Bench/scenarios/prompts/S-09.md`

**Context:**
- 현재 모든 프롬프트는 동일 구조: `You are a...` → `## Product Description` → `## Required Analysis` → `Be specific...`
- 마지막 줄 `Be specific. Cite exact regulation articles, product codes, and classification rules.` 뒤에 1줄 추가
- 모든 멤버에게 동일 적용 (공정성)

**Step 1: 9개 프롬프트 파일 수정**

각 파일의 마지막 줄 뒤에 추가:

```markdown

Use any tools, skills, or knowledge bases available to you to provide the most accurate and well-cited analysis.
```

**주의:** 기존 내용은 변경하지 않음. 마지막 줄 뒤에 빈 줄 + 새 줄만 추가.

**Step 2: 변경 확인**

Run: 9개 파일 모두 마지막 줄이 `Use any tools, skills, or knowledge bases...`로 끝나는지 확인

**Step 3: Commit** (RA-Bench 레포에서)

```bash
cd /Users/hb/Project/RA-Bench
git add scenarios/prompts/S-*.md
git commit -m "feat(bench): 프롬프트에 tool 사용 지시 추가 — 전 멤버 동일 적용"
```

---

### Task 5: Hook + Prompt 통합 검증 (S-08, S-09)

**Files:**
- None (검증만)

**Context:**
- Phase 1 Hook + Phase 2 Prompt가 모두 적용된 상태에서 MFDS 시나리오 2개 검증
- S-08 (VUNO Med-DeepBrain AD): 4-Gate, 7-digit, Risk Matrix 특수 메트릭
- S-09 (Manual Surgical Forceps): Gate 2 EXIT 특수 메트릭
- 둘 다 이전 최고 점수 비교 가능

**Step 1: S-08, S-09 벤치 실행**

Run:
```bash
cd /Users/hb/Project/RA-Bench
./scripts/bench-run.sh S-08 --member aria
./scripts/bench-run.sh S-09 --member aria
```

**Step 2: 스코어링**

Run:
```bash
python3 scripts/bench-score.py runs/2026-02-21/
```

**Step 3: 결과 판정**

| Scenario | 이전 최고 | 목표 | 롤백 기준 |
|----------|----------|------|-----------|
| S-08 | 70.0% (Phase 2) | ≥ 70% | < 52.5% (Phase 1 수준 이하) |
| S-09 | 80.0% (Phase 1) | ≥ 80% | < 70% (즉시 롤백) |

- 두 시나리오 모두 목표 달성: Phase 3 진행
- S-09 < 70%: Hook 내용 축소 후 재시도
- 스킬 미트리거 (트랜스크립트 확인): CLAUDE.md에 더 강한 지시 검토 (단, 토큰 예산 주의)

---

## Phase 3: Evidence References

### Task 6: determination 스킬 evidence reference 생성

**Files:**
- Create: `aria/skills/determination/references/evidence-catalog.md`

**Context:**
- determination 스킬은 이미 `modules/` 디렉토리에 `fda-criteria.md`, `eu-mdr-criteria.md`, `mfds-criteria.md`가 있음
- evidence reference는 벤치에서 기대하는 **구체적 키워드** (CFR, Article, 의료기기법 조항)를 포함
- SKILL.md의 워크플로우에서 `Read("references/evidence-catalog.md")` 지시 추가 필요

**Step 1: evidence-catalog.md 작성**

```markdown
# Determination Evidence Catalog

## FDA — 의료기기 판단 근거

| 제품 유형 | 핵심 법령 | 제품 코드 | 참고 가이던스 |
|-----------|----------|-----------|--------------|
| General medical device | 21 CFR 201(h) | — | — |
| Wellness product | General Wellness Policy (2016, rev. 2019) | — | FDA-2014-D-0080 |
| CDS exemption | 21st Century Cures Act § 3060(a) | — | FDA-2017-D-6569 |
| Combination product | 21 CFR 3.2(e)(1) | — | CDRH/CDER guidance |
| Software (SaMD) | 21 CFR 820 + IEC 62304 | — | FDA SaMD Framework (2017) |

## EU MDR — 의료기기 판단 근거

| 제품 유형 | 핵심 법령 | 참고 가이던스 |
|-----------|----------|--------------|
| General definition | Article 2(1) | MDCG 2019-11 (borderline) |
| Non-medical purpose | Article 1(2) + Annex XVI | MDCG 2023-5, Regulation 2022/2346 |
| Software qualification | Article 2(1) + MDCG 2019-11 Rev.1 | IMDRF SaMD N10 |
| Accessories | Article 2(2) | — |

## MFDS — 의료기기 판단 근거

| 제품 유형 | 핵심 법령 | 참고 기준 |
|-----------|----------|----------|
| General definition | 의료기기법 제2조제1항 | — |
| Digital health (4-Gate) | 디지털의료제품법 (2024) | MFDS 4-Gate 가이드라인 |
| Wellness product | 건강지원제품 3-tier | 디지털의료제품법 시행령 |
| Non-device boundary | 의료기기와 개인용 건강관리제품 판별 가이드라인 | — |
```

**Step 2: SKILL.md에 reference 로드 지시 추가**

`aria/skills/determination/SKILL.md`에서 워크플로우 섹션에 다음 추가:

```markdown
**Step 0 (pre-analysis):** Read("references/evidence-catalog.md") to load jurisdiction-specific evidence keywords.
```

**Step 3: Commit**

```bash
git add aria/skills/determination/references/evidence-catalog.md aria/skills/determination/SKILL.md
git commit -m "feat(aria): determination evidence catalog — 법령/가이던스 레퍼런스"
```

---

### Task 7: classification 스킬 evidence reference 생성

**Files:**
- Create: `aria/skills/classification/references/evidence-catalog.md`
- Modify: `aria/skills/classification/SKILL.md` (워크플로우에 Read 지시 추가)

**Context:**
- classification은 가장 큰 스킬 (568줄) — 이미 Override 섹션, Risk Matrix 등 복잡한 구조
- 벤치에서 가장 많이 실패하는 메트릭: evidence keywords (품목코드, CFR, Rule 번호)
- 벤치 카탈로그 기반 필요 키워드:
  - FDA: DQA, PIB, QPP, NIQ, 21 CFR 870.2700, 21 CFR 886.1100, 21 CFR 888.3600
  - EU: Rule 10, Rule 11, Rule 8, Rule 9, Rule 14, IR 3.5, Annex IX
  - MFDS: A08030.01, A17010.01, A19230, A45020.01, 등급표

**Step 1: evidence-catalog.md 작성**

```markdown
# Classification Evidence Catalog

## FDA Product Codes & CFR

| 제품 카테고리 | Product Code | CFR | Class | Predicate/De Novo |
|-------------|-------------|-----|-------|-------------------|
| Pulse oximeter | DQA | 21 CFR 870.2700 | II | K082641 |
| AI retinal screening | PIB | 21 CFR 886.1100 | II (De Novo) | DEN180001 |
| Smart knee implant | QPP | 21 CFR 888.3600 | II (De Novo) | DEN200064 |
| Drug-eluting stent | NIQ | 21 CFR 870.3460 | III (PMA) | P160043 |
| Sleep monitor (wellness) | QZW | 21 CFR 882.5801 | II (De Novo) | DEN230041 |

## EU MDR Classification Rules

| Rule | 적용 대상 | Class | 참고 |
|------|----------|-------|------|
| Rule 10 | Active diagnostic (measuring) | IIa | Pulse oximeters |
| Rule 11 | Software (SaMD) | IIa-III | IMDRF category mapping |
| Rule 8 | Cardiac/CNS/central circulatory contact | III | Implantable leads |
| Rule 9 | Therapeutic active devices (dangerous energy) | IIb-III | Pacing devices |
| Rule 14 | Devices incorporating medicinal substance | III | Drug-eluting |
| IR 3.5 | Implementing Rule for active implantable | III | AIMD transition |
| Annex XVI | Non-medical purpose devices | IIa+ | Cosmetic contacts |

## MFDS 품목코드 & 등급

| 제품 유형 | 품목코드 | 등급 | 경로 |
|----------|---------|------|------|
| 맥박산소측정기 | A08030.01 / A09020.02 | 2등급 | 인증 |
| AI 의료영상분석 SW | A17010.01 | 3등급 | 허가 |
| 의료영상분석소프트웨어 (안과) | A19230 | 3등급 | 허가 |
| 수동식 의료용 겸자 | A45020.01 | 1등급 | 신고 |
| 7-digit code (AI진단) | B1BXXA1 | — | — |

## MFDS 4-Gate Keywords

Gate 1: 의료기기 해당 → PASS/FAIL
Gate 2: 디지털 기술 → PASS/EXIT (비디지털 기기는 EXIT)
Gate 3: 핵심 기능 영향 → PASS/FAIL
Gate 4: 배제 원칙 → PASS/EXIT
```

**Step 2: SKILL.md에 reference 로드 지시 추가**

`aria/skills/classification/SKILL.md`에서 워크플로우 섹션에 다음 추가:

```markdown
**Step 0 (pre-analysis):** Read("references/evidence-catalog.md") to load product codes, CFR references, and classification rules.
```

**Step 3: Commit**

```bash
git add aria/skills/classification/references/evidence-catalog.md aria/skills/classification/SKILL.md
git commit -m "feat(aria): classification evidence catalog — 품목코드/CFR/Rule 레퍼런스"
```

---

### Task 8: pathway 스킬 evidence reference 생성

**Files:**
- Create: `aria/skills/pathway/references/evidence-catalog.md`
- Modify: `aria/skills/pathway/SKILL.md` (워크플로우에 Read 지시 추가)

**Context:**
- pathway 스킬은 classification 결과 기반으로 인허가 경로 결정
- 벤치 키워드: DEN번호, PMA번호, 법령 조항
- S-09 핵심 갭: Gate 2 EXIT 미출력

**Step 1: evidence-catalog.md 작성**

```markdown
# Pathway Evidence Catalog

## FDA Pathway Evidence

| Pathway | 근거 법령 | 대표 사례 | 기간 |
|---------|----------|----------|------|
| 510(k) | 21 CFR 807 Subpart E | K082641 (pulse oximeter) | 3-6개월 |
| De Novo | 21 CFR 860.260 | DEN180001 (IDx-DR), DEN200064 (Persona IQ), DEN230041 (sleep) | 6-12개월 |
| PMA | 21 CFR 814 | P160043 (Resolute Onyx) | 12-18+개월 |
| HDE | 21 CFR 814 Subpart H | — | 9-15개월 |

## EU MDR Pathway Evidence

| Pathway | 근거 법령 | Class | 참고 가이던스 |
|---------|----------|-------|--------------|
| Self-Declaration | Article 52(7) | I | — |
| Notified Body Annex IX | Article 52(3) + Annex IX | IIa-III | MDCG 2019-6 |
| Clinical Investigation | Article 62-82 | III (implantable) | Article 54, MDCG 2020-5 |
| Annex XVI pathway | Article 1(2) + Reg 2022/2346 | varies | MDCG 2023-5 |

## MFDS Pathway Evidence

| 경로 | 근거 법령 | 등급 | 기간 |
|------|----------|------|------|
| 신고 (Notification) | 의료기기법 제12조 | 1등급 | 1-3개월 |
| 인증 (Certification) | 의료기기법 제9조 | 2등급 | 3-9개월 |
| 허가 (Approval) | 의료기기법 제6조 | 3-4등급 | 9-15+개월 |
| 디지털의료제품법 경로 | 디지털의료제품법 | 웰니스 3-tier | varies |

## 주요 조합 패턴

| 제품 | Determination → Classification → Pathway |
|------|----------------------------------------|
| 맥박산소측정기 (S-01) | YES → Class II / IIa / 2등급 → 510(k) / NB / 인증 |
| AI DR 스크리닝 (S-02) | YES → Class II / IIa / 3등급 → De Novo / NB / 허가 |
| 수면 웰니스 모니터 (S-03) | CONDITIONAL → Class II / IIa / 2등급 → De Novo-510(k) / NB / 디지털의료제품법 |
| 스마트 무릎 임플란트 (S-04) | YES → Class II → De Novo |
| 약물용출 스텐트 (S-05) | CONDITIONAL → Class III → PMA |
| 미용 콘택트렌즈 (S-06) | SPECIAL → Class IIa → NB (Annex XVI) |
| 심장 페이싱 리드 (S-07) | YES → Class III → Annex IX + Clinical Investigation |
| VUNO DeepBrain AD (S-08) | YES → 3등급 → 허가 |
| 수동식 겸자 (S-09) | YES → 1등급 → 신고 (Gate 2 EXIT: 비디지털) |
```

**Step 2: SKILL.md에 reference 로드 지시 추가**

`aria/skills/pathway/SKILL.md`에서 워크플로우 섹션에 다음 추가:

```markdown
**Step 0 (pre-analysis):** Read("references/evidence-catalog.md") to load pathway-specific evidence and precedent mappings.
```

**Step 3: Commit**

```bash
git add aria/skills/pathway/references/evidence-catalog.md aria/skills/pathway/SKILL.md
git commit -m "feat(aria): pathway evidence catalog — DEN/PMA/법령 레퍼런스"
```

---

## Phase 4: Full Bench & Comparison

### Task 9: Tool-Enabled 전체 벤치 실행

**Files:**
- None (검증만)

**Context:**
- Phase 1-3 모든 변경이 적용된 상태
- Hook + Prompt + Evidence References 통합 검증
- 9개 전체 시나리오 실행

**Step 1: ARIA 전체 벤치 실행**

Run:
```bash
cd /Users/hb/Project/RA-Bench && ./scripts/bench-run.sh all --member aria
```

Expected: 9개 시나리오 모두 실행 완료 (~30-45분)

**Step 2: 스코어링**

Run:
```bash
python3 scripts/bench-score.py runs/2026-02-21/
```

**Step 3: 결과 분석**

성공 기준:

| 지표 | 목표 |
|------|------|
| 전체 평균 | ≥ 75% (330/440) |
| S-09 | ≥ 70% |
| 2개 이상 시나리오 동시 하락 | 없어야 함 |
| 스킬 트리거 비율 | 트랜스크립트에서 확인 |

**Step 4: Baseline 비교 (선택적)**

Hook 없이 기존 프롬프트로 bare run 실행하여 Baseline 유지 확인:
- council.config.yaml에서 aria command의 plugin-dir를 임시 제거
- 또는 별도 date 디렉토리에 baseline 결과 저장

---

### Task 10: 결과 정리 및 메모리 업데이트

**Files:**
- Modify: `/Users/hb/.claude/projects/-Users-hb-Project-Cowork-RA/memory/aria-bench.md`

**Step 1: 벤치 결과 테이블 업데이트**

aria-bench.md의 `## RA-Bench Results & Progress` 테이블에 새 행 추가:

```markdown
| Bench v2 (Hook+Prompt+Evidence) | XX.X% | Codex | 2026-02-21 |
```

**Step 2: 시나리오별 점수 업데이트**

`## Per-Scenario Scores` 테이블을 최신 결과로 갱신.

**Step 3: 교훈 기록**

새 섹션 추가:
```markdown
## Bench v2 Lessons
- SessionStart Hook이 스킬 트리거를 보장하는 유일한 메커니즘
- 벤치 프롬프트 tool 지시는 공정하면서 ARIA에 유리한 환경 제공
- SKILL.md = 규칙/구조, references/ = 지식 (분리 원칙 유지)
```

**Step 4: Commit**

```bash
git add -f docs/plans/2026-02-21-aria-bench-v2-implementation.md
git commit -m "docs: Bench v2 구현 결과 정리 및 메모리 업데이트"
```

---

## Rollback Plan

모든 Phase에서 롤백 기준 충족 시:

**Phase 1 (Hook) 롤백:**
```bash
rm aria/hooks/session-start.sh aria/hooks/hooks.json
rmdir aria/hooks
git add -A && git commit -m "revert: Hook 롤백 — 스킬 트리거 부작용"
```

**Phase 2 (Prompt) 롤백:**
```bash
cd /Users/hb/Project/RA-Bench
git checkout HEAD -- scenarios/prompts/
git commit -m "revert: 프롬프트 롤백"
```

**Phase 3 (Evidence) 롤백:**
```bash
git revert <evidence-commit-hash>
```

---

## Dependency Graph

```
Task 1 (session-start.sh)
    ↓
Task 2 (hooks.json)
    ↓
Task 3 (Hook 검증 — S-09)  ←── 실패 시 Task 1-2 수정
    ↓
Task 4 (벤치 프롬프트 수정)
    ↓
Task 5 (통합 검증 — S-08, S-09)  ←── 실패 시 Task 1-4 재검토
    ↓
Task 6 (determination evidence)  ─┐
Task 7 (classification evidence) ─┼── 병렬 가능
Task 8 (pathway evidence)        ─┘
    ↓
Task 9 (전체 벤치)
    ↓
Task 10 (결과 정리)
```
