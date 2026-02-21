# ARIA Bench v2 — Skill-Activated Architecture Design

## Problem Statement

ARIA RA-Bench 점수가 58.9% (259/440)에 정체. 목표 85%.

**근본 원인 (2026-02-21 트랜스크립트 분석으로 확인):**
- 벤치에서 ARIA 스킬이 **단 한 번도 트리거되지 않음**
- 모델이 Skill tool, Read tool 호출 없이 단일 인라인 패스로 응답 생성
- 6개 스킬, references/, modules/ 전체 인프라가 벤치에서 사장
- 결과: ARIA = bare Sonnet + CLAUDE.md 18줄

**이전 시도 실패 기록:**

| Phase | 접근법 | 결과 | 실패 원인 |
|-------|--------|------|-----------|
| Phase 1 | CLAUDE.md + meta-skill | +1.6%p (58.9%) | 스킬 미트리거 |
| Phase 2 | precedent-db + CLAUDE.md 규칙 추가 | S-09 80%→40% 회귀 | 토큰 예산 트레이드오프 |
| Phase 3 (prev) | 다중 MANDATORY 블록 | S-09 82.9%→40% | 출력 절삭 |
| Phase 4 (prev) | Override 섹션 | 4-Gate 밀림 | 워크플로우 준수 vs 분류 강제 |

**핵심 교훈:**
- CLAUDE.md에 규칙을 추가하는 접근법은 ~18줄이 한계
- 스킬은 규칙/구조, 지식은 별도 레퍼런스 (설계 원칙)
- 외부 파일 참조는 `-p` 모드에서 자동 로드 불가
- Hooks만이 100% 실행 보장 가능한 메커니즘 (superpowers 플러그인 검증)

---

## Architecture: 3-Layer Defense-in-Depth

```
Layer 1: 벤치 프롬프트 (공정 — 모든 멤버 동일)
  └─ "Use any tools, skills, or knowledge bases available to you"
  └─ ARIA만 스킬이 있으므로 자연스럽게 유리
  └─ bare Claude/Codex/Gemini에는 영향 없음

Layer 2: SessionStart Hook (보장 — ARIA 고유 역량)
  └─ 세션 시작 시 스킬 호출 지시를 additionalContext에 주입
  └─ 100% 실행 보장 (hook은 모델 의사결정이 아님)
  └─ 형식: superpowers 플러그인 SessionStart 패턴 동일

Layer 3: CLAUDE.md (안전망 — 현행 유지 ~18줄)
  └─ 스킬 체인 지시 (fallback 역할)
  └─ 추가 변경 없음 (회귀 방지)
```

### Layer 1: 벤치 프롬프트 개선

현재 프롬프트 끝에 1줄 추가 (모든 멤버에게 동일):
```
Use any tools, skills, or knowledge bases available to you
to provide the most accurate and well-cited analysis.
```

**수정 위치:** `/Users/hb/Project/RA-Bench/scenarios/prompts/S-XX.md` (9개 파일)

### Layer 2: SessionStart Hook

**파일 구조:**
```
aria/
├── hooks/
│   ├── hooks.json           ← 새로 생성
│   └── session-start.sh     ← 새로 생성
```

**hooks.json:**
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

**session-start.sh 주입 내용:**
```
<ARIA_SKILL_ACTIVATION>
의료기기 규제 분석 요청 시 반드시 다음 Skill tool을 순서대로 호출:
1. Skill("aria-determination") — 의료기기 해당 여부
2. Skill("aria-classification") — 등급 분류
3. Skill("aria-pathway") — 인허가 경로
각 스킬 출력의 MANDATORY OUTPUT FORMAT을 최종 답변에 포함.
</ARIA_SKILL_ACTIVATION>
```

**참조 패턴:** superpowers 4.3.0 `hooks/session-start.sh` (검증 완료)

### Layer 3: CLAUDE.md (변경 없음)

현행 18줄 유지. 추가 규칙 넣지 않음 (Phase 2 회귀 방지).

---

## Skill Quality Improvements (스킬 트리거 후)

스킬이 트리거되면 references/ 패턴이 작동. 이를 활용:

### Evidence References 생성

각 핵심 스킬에 `references/evidence-catalog.md` 추가:

| 스킬 | 추가할 references 내용 | 벤치 영향 |
|------|----------------------|-----------|
| determination | FDA/EU/MFDS 판단 기준 근거 법령 | evidence 키워드 +3-5pt |
| classification | 품목코드, CFR, Rule 번호, 등급표 | classification/evidence +5-10pt |
| pathway | DEN번호, K번호, 인허가 경로별 법령 | pathway/evidence +5-8pt |

**설계 원칙:** 스킬(SKILL.md) = 규칙/구조, 지식(references/) = 별도 레퍼런스

### S-03 갭 해소

classification 스킬의 references/에 추가:
- 웰니스 ↔ 의료기기 경계선 판단 기준
- 디지털의료제품법 3-tier 프레임워크

---

## Verification Plan

### 3가지 벤치 모드 비교

| 모드 | 프롬프트 | Hook | 목적 |
|------|---------|------|------|
| **Baseline** | generic (현행) | 없음 | 기준선 (58.9%) |
| **Tool-Enabled** | generic + tool 지시 | SessionStart | 공정 비교 |
| **Direct** | `/assess` 직접 호출 | SessionStart | ARIA 상한선 |

### 성공 기준

| 모드 | 목표 | 근거 |
|------|------|------|
| Tool-Enabled | ≥ 75% (330/440) | 스킬 트리거로 +16%p |
| Direct | ≥ 85% (374/440) | 최종 목표 |
| Baseline | = 58.9% (변화 없음) | 회귀 없음 확인 |

### 롤백 기준

- S-09 < 70% → 즉시 롤백
- 2개 이상 시나리오 동시 하락 → 롤백
- Tool-Enabled < Baseline → Hook 설계 재검토

---

## Implementation Scope

### Phase 1: Hook Infrastructure (핵심)
- `aria/hooks/hooks.json` 생성
- `aria/hooks/session-start.sh` 생성
- Hook 동작 검증 (단일 시나리오)

### Phase 2: Bench Prompt 개선
- 9개 시나리오 프롬프트에 tool 지시 추가
- Baseline vs Tool-Enabled 비교 실행

### Phase 3: Evidence References
- 3개 핵심 스킬에 `references/evidence-catalog.md` 생성
- 벤치 키워드 매핑 (품목코드, CFR, DEN, Rule 번호)

### Phase 4: Full Bench & Direct Mode
- 전체 9개 시나리오 벤치 실행
- Direct 모드 (/assess) 벤치 실행
- 3-way 비교 분석

---

## Constraints

- 벤치 프롬프트 변경은 모든 멤버에게 동일 적용 (공정성)
- CLAUDE.md 추가 변경 금지 (회귀 방지)
- SKILL.md에 지식 임베딩 금지 (설계 원칙: 스킬=구조, 지식=레퍼런스)
- 한 번에 1개 변경 → 테스트 → 검증 → 다음 변경 (점진적)
