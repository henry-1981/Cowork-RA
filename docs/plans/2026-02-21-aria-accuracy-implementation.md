# ARIA 정확도 개선 구현 계획

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** RA-Bench 57.3% → 85% 달성 (252/440 → 374/440)

**Architecture:** 4-Phase 점진적 개선 — 아키텍처 레이어 → 선례 DB → 도메인 규칙 → 루브릭 보정. 매 Phase 후 벤치 검증. 기존 6-스킬 아키텍처와 대화형 UX 보존.

**Tech Stack:** Claude Code Plugin (CLAUDE.md, SKILL.md, knowledge modules), RA-Bench (bench-run.sh, bench-score.py)

**설계 문서:** `docs/plans/2026-02-21-aria-accuracy-improvement-design.md`

**벤치 실행 방법:**
```bash
# 단일 시나리오
cd /Users/hb/Project/RA-Bench && ./scripts/bench-run.sh S-08 --member aria
# 채점
cd /Users/hb/Project/RA-Bench && python scripts/bench-score.py S-08 --member aria
# 전체
cd /Users/hb/Project/RA-Bench && ./scripts/bench-run.sh all --member aria
```

**핵심 원칙:**
- 1 Phase = 1 변경 = 1 벤치 = 1 검증
- 토큰 예산 주의 (CLAUDE.md 200줄 이내)
- 유즈케이스 추가 금지 — 범용 룰/패턴만

---

## Phase 1: 아키텍처 레이어 (스킬 자동 활성화)

**목표:** Generic 프롬프트에서도 ARIA 스킬이 자동 트리거되도록 CLAUDE.md + meta-skill 생성
**예상 효과:** +40~50pt → 66~69%
**검증:** S-08 ≥ 55%, S-09 ≥ 80% 유지

### Task 1: CLAUDE.md 생성

**Files:**
- Create: `aria/CLAUDE.md`

**Step 1: CLAUDE.md 작성**

아래 내용을 `aria/CLAUDE.md`에 작성. ~300 토큰, 간결하게.

```markdown
# ARIA — AI Regulatory Intelligence Assistant

의료기기 규제(FDA, EU MDR, MFDS) 질문에 대해 반드시 ARIA 스킬을 사용한다.

## 스킬 체인 (필수)

규제 평가 질문 → 아래 순서로 Skill tool 호출:
1. `aria-determination` — 의료기기 해당 여부
2. `aria-classification` — 등급 분류 (FDA I/II/III, EU I/IIa/IIb/III, MFDS 1-4)
3. `aria-pathway` — 인허가 경로 (510(k), PMA, De Novo, CE, 신고/인증/허가)

비용/일정: `aria-estimation` → `aria-planning`
마케팅 컴플라이언스: `aria-compliance` (독립 호출)

## 규칙
- base knowledge로만 규제 질문에 답하지 않는다
- 각 스킬의 MANDATORY OUTPUT FORMAT 블록을 반드시 출력에 포함한다
- 정보 부족 시 스킬이 정의한 insufficiency 절차를 따른다
```

**Step 2: 커밋**

```bash
git add -f aria/CLAUDE.md
git commit -m "feat(aria): CLAUDE.md 신설 — 스킬 자동 라우팅 기반"
```

---

### Task 2: using-aria 메타스킬 생성

**Files:**
- Create: `aria/skills/using-aria/SKILL.md`

**Step 1: 디렉터리 생성 및 SKILL.md 작성**

```bash
mkdir -p aria/skills/using-aria
```

아래 내용을 `aria/skills/using-aria/SKILL.md`에 작성:

```yaml
---
name: using-aria
description: >
  MANDATORY: 의료기기, 규제, FDA, EU MDR, MFDS, SaMD, 510(k), PMA,
  CE mark, 등급 분류, 인허가, 컴플라이언스 관련 질문에 반드시 사용.
  RA 질문을 감지하면 ARIA 스킬 체인을 트리거한다.
allowed-tools: Skill Read Grep Glob
user-invocable: false
metadata:
  version: "0.1.0"
  category: "meta"
  status: "active"
---

<EXTREMELY-IMPORTANT>
의료기기 규제 관련 질문이 1%라도 해당되면 반드시 ARIA 스킬을 호출한다.

## 라우팅 규칙

**규제 평가 (assessment):**
1. Skill("aria-determination")
2. Skill("aria-classification")
3. Skill("aria-pathway")

**비용/일정:** + Skill("aria-estimation") → Skill("aria-planning")
**컴플라이언스:** Skill("aria-compliance") 단독

## 금지사항
- base knowledge로만 규제 답변 금지
- 스킬 없이 등급/경로 결론 금지
- MANDATORY OUTPUT FORMAT 누락 금지
</EXTREMELY-IMPORTANT>
```

**Step 2: 커밋**

```bash
git add -f aria/skills/using-aria/SKILL.md
git commit -m "feat(aria): using-aria 메타스킬 — 자동 스킬 체인 라우팅"
```

---

### Task 3: plugin.json 버전 범프

**Files:**
- Modify: `aria/.claude-plugin/plugin.json`

**Step 1: 버전을 0.1.11 → 0.2.0으로 범프**

`plugin.json`의 `"version": "0.1.11"` → `"version": "0.2.0"` 변경

**Step 2: 커밋**

```bash
git add aria/.claude-plugin/plugin.json
git commit -m "chore(aria): 버전 0.2.0 — 아키텍처 레이어 추가"
```

---

### Task 4: Phase 1 벤치 검증

**Step 1: S-08 벤치 실행 (VUNO DeepBrain AD)**

```bash
cd /Users/hb/Project/RA-Bench && ./scripts/bench-run.sh S-08 --member aria
```

**Step 2: S-09 벤치 실행 (수동 겸자)**

```bash
cd /Users/hb/Project/RA-Bench && ./scripts/bench-run.sh S-09 --member aria
```

**Step 3: 채점**

```bash
cd /Users/hb/Project/RA-Bench && python scripts/bench-score.py S-08 --member aria
cd /Users/hb/Project/RA-Bench && python scripts/bench-score.py S-09 --member aria
```

**성공 기준:**
- S-08: ≥ 55% (22/40) — 현재 47.5% (19/40)
- S-09: ≥ 80% 유지 — 현재 80% (28/35)

**회귀 감시:** S-01, S-07도 실행하여 점수 하락 없는지 확인

**실패 시:** CLAUDE.md 토큰이 과다하면 압축. meta-skill description이 트리거되지 않으면 키워드 조정.

---

## Phase 2: 선례 데이터베이스

**목표:** Evidence 점수 평균 1.1/5 → 3.0+/5
**예상 효과:** +25~35pt → 72~77%
**검증:** S-01, S-04, S-08 evidence ≥ 2.5/5

### Task 5: precedent-db.md 생성

**Files:**
- Create: `aria/knowledge/precedent-db.md`

**Step 1: 디렉터리 생성 및 선례 DB 작성**

```bash
mkdir -p aria/knowledge
```

설계 문서의 Section 3.1 "25개 카테고리 선례 DB"를 `aria/knowledge/precedent-db.md`에 작성.

포함 내용:
- 5개 카테고리 그룹 (진단/AI·SaMD/임플란트/치료/특수)
- 각 항목: Category, FDA Product Code, CFR, Landmark Decision, MFDS Code, Grade, 7-Digit, Confidence
- 사용 가이드라인 (✅/⚠️/❓ 신뢰도별 인용 규칙)

**Step 2: 커밋**

```bash
git add -f aria/knowledge/precedent-db.md
git commit -m "feat(aria): 선례 DB 25개 카테고리 — evidence 정확도 향상"
```

---

### Task 6: CLAUDE.md에 선례 DB 참조 추가

**Files:**
- Modify: `aria/CLAUDE.md`

**Step 1: CLAUDE.md에 선례 참조 규칙 추가**

CLAUDE.md 하단에 아래 섹션 추가:

```markdown
## 근거 제시 규칙
- 규제 평가 시 `aria/knowledge/precedent-db.md`의 해당 카테고리 코드를 인용
- ✅ 검증완료 코드: 직접 인용 가능
- ⚠️ 고신뢰 추정 코드: "~로 추정됨" 접두어 사용
- 매칭 불가 시: "규제 당국 데이터베이스 검증 필요" 명시
```

**주의:** CLAUDE.md 전체가 200줄을 넘지 않도록 관리

**Step 2: 커밋**

```bash
git add -f aria/CLAUDE.md
git commit -m "feat(aria): CLAUDE.md에 선례 DB 참조 규칙 추가"
```

---

### Task 7: Phase 2 벤치 검증

**Step 1: 대상 시나리오 벤치 실행**

```bash
cd /Users/hb/Project/RA-Bench
./scripts/bench-run.sh S-01 --member aria
./scripts/bench-run.sh S-04 --member aria
./scripts/bench-run.sh S-08 --member aria
```

**Step 2: 채점**

```bash
python scripts/bench-score.py S-01 --member aria
python scripts/bench-score.py S-04 --member aria
python scripts/bench-score.py S-08 --member aria
```

**성공 기준:**
- Evidence 평균 ≥ 2.5/5 (현재 1.1/5)
- S-04 de_novo_identification ≥ 2/5 (현재 0/5)

**회귀 감시:** S-09 점수 유지 확인

---

## Phase 3: 도메인 규칙 강화

**목표:** CONDITIONAL/SPECIAL 판정 정확도 + De Novo 경로 + 디지털의료제품법 + 4-Gate 승격
**예상 효과:** +33~47pt → 80~87%
**검증:** S-03 ≥ 50%, S-05 det ≥ 3

**중요:** Phase 3는 변경이 많으므로 3a/3b/3c로 세분화. 각 서브Phase 후 벤치 검증.

### Task 8 (Phase 3a): Classification — 4-Gate를 분석 전제조건으로 승격

**Files:**
- Modify: `aria/skills/classification/SKILL.md`
- Modify: `aria/skills/determination/SKILL.md`

**Step 1: classification/SKILL.md에서 4-Gate를 Phase 0 Prerequisite로 재구조화**

현재 Step 4A의 4-Gate 출력 형식을 다음 구조로 변경:

```
### MFDS 분류 워크플로우

Phase 0: 4-Gate 디지털의료기기 판정 (PREREQUISITE)
  - Gate 1~4 순차 실행
  - 결과가 Phase 1의 분류 경로를 결정

Phase 1: 등급 분류 (4-Gate 결과에 따라 분기)
  - IF 디지털의료기기 → Risk Matrix → 7-Digit Code
  - IF 비디지털 / Gate 2 EXIT → 전통 품목분류표

Phase 2: 검증
```

**Step 2: 6개 MANDATORY 블록을 2개 통합 블록으로 간소화**

- 통합 블록 1: "MFDS 분류 분석 결과" (4-Gate + Risk Matrix + 7-Digit + Consistency)
- 통합 블록 2: "근거 및 신뢰도" (Evidence + Confidence)

**Step 3: determination/SKILL.md에서 4-Gate 중복 정의 제거**

4-Gate 출력 형식 블록을 제거하고, "디지털 제품 감지 플래그" 설정만 유지.

**Step 4: 커밋**

```bash
git add aria/skills/classification/SKILL.md aria/skills/determination/SKILL.md
git commit -m "refactor(aria): 4-Gate를 분류 전제조건으로 승격, MANDATORY 블록 통합"
```

**Step 5: S-08, S-09 벤치 검증**

S-08 special metrics (4gate, 7digit, risk_matrix) 향상 확인, S-09 회귀 없음 확인.

---

### Task 9 (Phase 3b): Determination — CONDITIONAL 유형별 분기 + 디지털의료제품법

**Files:**
- Modify: `aria/skills/determination/SKILL.md`
- Modify: `aria/skills/determination/modules/mfds-criteria.md`
- Modify: `aria/skills/determination/modules/eu-mdr-criteria.md`

**Step 1: CONDITIONAL 유형별 분기 트리 추가**

`determination/SKILL.md` Step 2에 5개 유형 분기 추가:
- TYPE-W (Wellness/Medical) → 3-Tier 필수 호출
- TYPE-C (Combination) → PMOA 분석
- TYPE-X (Annex XVI) → SPECIAL 출력
- TYPE-S (Software/CDS) → CDS 4기준
- TYPE-A (Ambiguity) → 양방향 분석

**Step 2: mfds-criteria.md에 디지털의료제품법 3-Tier 보강**

설계 문서 Section 3.2의 내용 추가:
- 법적 근거 (제2조, 제3조, 제7조)
- 3-Tier 판단 워크플로우
- 경계 제품 필수 키워드 체크리스트 ("디지털의료제품법", "3-tier", "웰니스", "건강지원제품")

**Step 3: eu-mdr-criteria.md에 Annex XVI 감지 조건 보완**

Step 2 워크플로우에서 Annex XVI 해당 시 SPECIAL 상태로 분기하는 조건 명시.

**Step 4: 커밋**

```bash
git add aria/skills/determination/SKILL.md aria/skills/determination/modules/mfds-criteria.md aria/skills/determination/modules/eu-mdr-criteria.md
git commit -m "feat(aria): CONDITIONAL 유형별 분기 + 디지털의료제품법 3-Tier 통합"
```

**Step 5: S-03, S-06 벤치 검증**

- S-03: MFDS determination/classification/pathway ≥ 1 (현재 전부 0)
- S-06: determination ≥ 3 (현재 1)

---

### Task 10 (Phase 3c): Classification/Pathway — 이중 트랙 + 근거 체크리스트 + 일관성 검증

**Files:**
- Modify: `aria/skills/classification/SKILL.md`
- Modify: `aria/skills/pathway/SKILL.md`
- Modify: `aria/skills/determination/SKILL.md`

**Step 1: Classification에 Dual-Track Conditional Mode 추가**

Step 1 이후에 Step 1.5 삽입:
- determination=YES → 기존 워크플로우
- determination=CONDITIONAL → Scenario A (IF device) + Scenario B (IF NOT device) 이중 출력

**Step 2: Pathway에 Conditional 입력 처리 추가**

Step 1에서 Dual-Track 입력 인식, "IF device:" 접두사 유지.

De Novo 우선 로직 추가:
- "선례(predicate) 부재 + low-moderate risk → De Novo를 PRIMARY 경로로 추천"

**Step 3: 3개 스킬에 관할권별 근거 체크리스트 추가**

각 스킬의 Evidence Requirements를 통합 체크리스트로 교체:
```
FDA: □ CFR § □ Product Code □ 선례 [DEN/K/P] □ Guidance
EU MDR: □ Article □ Rule □ MDCG □ IR
MFDS: □ 법률 조항 □ 품목코드 □ 등급 근거 □ 가이드라인
```

**Step 4: 3차원 일관성 검증을 Classification 최종 단계에 배치**

Determination ↔ Classification ↔ Pathway 일관성 3차원 검증.

**Step 5: 커밋**

```bash
git add aria/skills/classification/SKILL.md aria/skills/pathway/SKILL.md aria/skills/determination/SKILL.md
git commit -m "feat(aria): 이중 트랙 분류 + De Novo 우선 + 근거 체크리스트 + 3차원 일관성 검증"
```

**Step 6: S-03, S-04, S-05 벤치 검증**

- S-03: total ≥ 50/80 (현재 33/80)
- S-04: pathway ≥ 4/5, de_novo ≥ 3/5
- S-05: determination ≥ 3/5 (현재 0/5)

---

## Phase 4: 루브릭 & 품질 보정

**목표:** 채점 공정성 확보 + 잔여 점수
**예상 효과:** +12~15pt → 82~91%
**검증:** 전체 9개 시나리오 ≥ 85%

### Task 11: 루브릭 별칭 수정

**Files:**
- Modify: `/Users/hb/Project/RA-Bench/rubric/catalog.json` (또는 scoring-rubric.json)

**Step 1: "(if YES)" 별칭 추가**

S-03의 expected classification values에 별칭 추가:
- `"Class II (if YES)"` → aliases에 `"class ii"`, `"class 2"` 추가
- `"등급 2 (if device)"` → aliases에 `"등급 2"`, `"2등급"` 추가

**Step 2: 커밋 (RA-Bench repo)**

```bash
cd /Users/hb/Project/RA-Bench
git add rubric/
git commit -m "fix(rubric): classification 조건부 수식어 별칭 추가 (공정성)"
```

---

### Task 12: 전체 벤치 실행 및 최종 검증

**Step 1: 전체 9개 시나리오 벤치 실행**

```bash
cd /Users/hb/Project/RA-Bench && ./scripts/bench-run.sh all --member aria
```

**Step 2: 전체 채점**

```bash
cd /Users/hb/Project/RA-Bench && python scripts/bench-score.py all --member aria
```

**Step 3: 결과 분석**

각 시나리오별 점수를 이전 결과(Phase 4, 2026-02-21)와 비교:

| Scenario | Before | After | Delta | Target |
|----------|--------|-------|-------|--------|
| S-01 | 51/75 (68%) | ? | ? | ≥ 75% |
| S-02 | 48/90 (53%) | ? | ? | ≥ 70% |
| S-03 | 33/80 (41%) | ? | ? | ≥ 60% |
| S-04 | 14/30 (47%) | ? | ? | ≥ 75% |
| S-05 | 18/30 (60%) | ? | ? | ≥ 75% |
| S-06 | 19/30 (63%) | ? | ? | ≥ 80% |
| S-07 | 22/30 (73%) | ? | ? | ≥ 80% |
| S-08 | 19/40 (48%) | ? | ? | ≥ 70% |
| S-09 | 28/35 (80%) | ? | ? | ≥ 80% |
| **Total** | **252/440 (57%)** | **?** | **?** | **≥ 374/440 (85%)** |

**최종 성공 기준:** 전체 ≥ 85% (374/440)

**목표 미달 시 조치:**
- 70~80%: Phase 3 서브Phase 재분할 후 추가 검증
- 80~85%: Analysis 점수 (Stage 2 LLM judge) 향상을 위한 추론 깊이 개선
- <70%: 아키텍처 레이어 재검토 (meta-skill이 실제로 트리거되는지 확인)

---

### Task 13: 버전 범프 및 CHANGELOG 업데이트

**Files:**
- Modify: `aria/.claude-plugin/plugin.json`
- Modify: `aria/CHANGELOG.md`

**Step 1: 최종 버전 범프**

85% 달성 시 `plugin.json` 버전을 `0.3.0`으로 범프.

**Step 2: CHANGELOG 업데이트**

```markdown
## [0.3.0] - 2026-02-XX

### Added
- CLAUDE.md 신설 — 스킬 자동 라우팅 기반
- using-aria 메타스킬 — RA 질문 자동 감지 및 스킬 체인 트리거
- 선례 DB (25개 카테고리) — evidence 정확도 향상
- 디지털의료제품법 3-Tier 프레임워크 통합
- CONDITIONAL 유형별 분기 트리 (TYPE-W/C/X/S/A)
- Dual-Track Conditional Classification Mode
- De Novo 경로 우선 로직
- 관할권별 근거 체크리스트
- 3차원 일관성 검증 (Determination ↔ Classification ↔ Pathway)

### Changed
- 4-Gate를 출력 형식에서 분류 전제조건으로 승격
- MANDATORY OUTPUT FORMAT 6개 → 2개 통합 블록
- 4-Gate 중복 정의 제거 (determination → classification 단일 소스)

### Performance
- RA-Bench: 57.3% → XX% (Phase 1-4 적용)
```

**Step 3: 커밋**

```bash
git add aria/.claude-plugin/plugin.json aria/CHANGELOG.md
git commit -m "chore(aria): v0.3.0 — 정확도 개선 Phase 1-4 완료"
```

---

## 메모리 업데이트 (최종)

모든 Phase 완료 후, 크로스 세션 메모리 업데이트:

```
/Users/hb/.claude/projects/-Users-hb-Project-Cowork-RA/memory/aria-bench.md
```

- 새로운 벤치 결과 추가
- Phase별 효과 기록
- 실패/성공 교훈 기록
