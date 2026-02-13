# SPEC-ARIA-005: Output Contract Unification + Humanized Writing Layer

**Date**: 2026-02-13  
**Status**: Design Approved (Single Document, Dual Gates)  
**Scope**: `aria/commands/*`, `aria/skills/*`

---

## 1. Background

ARIA must prevent bad decisions from incomplete or unclear information.  
At the same time, outputs should be easier to read and act on for both operators and executives.

Current state has two separate concerns:
1. Output contract is inconsistent by surface (commands expose format options, skills mainly define analytical outputs).
2. Writing style quality is not centralized as one reusable internal layer.

This design keeps one document for operational convenience, but splits approval into two independent gates.

---

## 2. Decision Summary

### 2.1 Single document + dual gate model

- **Part A (Gate A)**: Output Contract Unification
- **Part B (Gate B)**: Humanized Writing Layer
- **Rule**: Gate A must be approved before Part B implementation starts.

### 2.2 Core principle

ARIA’s root flow is fixed and must not be weakened:
1. Check information sufficiency
2. Provide analysis/judgment
3. Ask for user-approved next action

### 2.3 Internal-only shared writing skill

- Introduce `aria-humanized-writing` as a shared internal capability.
- Keep it **non-user-invocable** (`user-invocable: false`).
- Users continue to use only existing command surface (`/aria:chat`, `/aria:assess`, `/aria:project`, `/aria:report`).

### 2.4 Efficiency requirement

Apply depth control to avoid latency inflation:
- Presets: `express | standard | deep`
- Default: automatic by context/output type
- User override: supported via `--depth express|standard|deep`

---

## 3. Guardrails (Top Priority)

These guardrails apply to Part A and Part B.

1. Do not provide deterministic conclusions when information is insufficient.
2. Do not finalize class/pathway from weak assumptions.
3. Do not auto-run next pipeline commands without explicit user approval.
4. Always show confidence state: `sufficient | partial | insufficient`.
5. Always provide minimum missing inputs (1-3 items) when confidence is not sufficient.

---

## 4. Part A (Gate A): Output Contract Unification

## 4.1 Goal

Unify output control across commands and skills with one canonical contract while preserving current command UX.

## 4.2 Canonical output contract

```json
{
  "output_type": "user_response_body | summary_md | full_report_md",
  "response_mode": "skill_invoked | general_qa",
  "format": "markdown | pdf | notion | gdocs",
  "language": "ko | en",
  "audience": "operator | executive | mixed",
  "safety_flags": {
    "preserve_regulatory_facts": true,
    "preserve_numeric_values": true,
    "preserve_disclaimer_strength": true
  },
  "actionability_level": "low | medium | high",
  "depth": "express | standard | deep"
}
```

## 4.3 Responsibility split

- **Skills** (`determination`, `classification`, `pathway`, `estimation`, `planning`, `compliance`)
  - Produce structured analytical results only.
  - No command-level format orchestration responsibility.
- **Commands** (`chat`, `assess`, `project`, `report`)
  - Resolve output contract.
  - Render/export to target format.
  - Persist files and expose final output to users.

## 4.4 Chat-specific alignment

- `chat` keeps current command surface (`--lang` only).
- Internal contract still sets `format=markdown`.
- `response_mode` is explicit:
  - `skill_invoked`: analysis results naturally embedded in conversation
  - `general_qa`: direct explanatory answer

This reflects current `chat` behavior without forcing immediate CLI-level `--format` expansion.

## 4.5 ARIA examples for non-technical stakeholders

### Example A: `/aria:chat` (conversation turn)

- Input: “부정맥 감지 웨어러블, 미국/한국 진출”
- Contract:
  - `output_type=user_response_body`
  - `response_mode=skill_invoked`
  - `format=markdown`
  - `language=ko`
  - `audience=operator`
- User-visible pattern:
  - 필요한 추가정보 확인
  - 현재 정보 기준 판단 제시
  - 다음 액션 질문 1개

### Example B: `/aria:assess` summary

- Contract:
  - `output_type=summary_md`
  - `format=markdown`
  - `language=ko`
  - `audience=executive`
- User-visible pattern:
  - 결론 우선
  - 핵심 근거 3줄
  - 권장 액션 3개

### Example C: `/aria:report --format pdf --lang en`

- Contract:
  - `output_type=full_report_md` (source)
  - `format=pdf` (delivery)
  - `language=en`
  - `audience=mixed`
- User-visible pattern:
  - Executive summary first
  - Detailed analysis next
  - Facts and numbers preserved

## 4.6 Error handling (Part A)

1. Missing required contract fields -> block render and return explicit schema error.
2. Unsupported format (connector unavailable) -> graceful fallback to `markdown` with notice.
3. Invalid `response_mode` for context -> normalize to default and log warning.

## 4.7 Testing and acceptance (Part A)

1. Contract schema validation tests (required field coverage).
2. Command mapping tests (`chat/assess/project/report` -> expected contract).
3. Format fallback tests (pdf/notion/gdocs unavailable cases).
4. Snapshot tests for `summary_md` and `full_report_md` structure.

**Gate A Acceptance**:
- All commands resolve valid contract objects.
- Skills return structure-first outputs.
- Existing command UX remains backward-compatible.

---

## 5. Part B (Gate B): Humanized Writing Layer

## 5.1 Goal

Improve readability and actionability without changing regulatory meaning.

## 5.2 Design

Introduce shared internal layer `aria-humanized-writing`:
- `user-invocable: false`
- Always on for user-visible content
- Used in both layers:
  - Skill layer (when user-visible text is produced)
  - Command final layer (final consistency pass)
- De-duplication via metadata flag (`humanized=true`), so repeated heavy rewriting is avoided.

## 5.3 Efficiency model (depth presets)

### Presets

1. `express`: short, question-forward, minimal explanation
2. `standard`: default balance of clarity + evidence + next action
3. `deep`: full narrative for detailed reports

### Default resolution

1. `user_response_body`: `standard`  
   Exception: information insufficient -> force `express`
2. `summary_md`: `express`
3. `full_report_md`: `deep`

### User override

Allow optional override:
- `--depth express|standard|deep`

Override never bypasses safety guardrails.

## 5.4 Hard-fact invariants

Never alter semantic meaning of:
1. Regulatory citations/articles
2. Class/pathway decisions
3. Numeric values and timelines
4. Escalation status
5. Disclaimer strength

Humanization can rephrase, structure, and clarify only.

## 5.5 Insufficient-information behavior

When confidence is `insufficient`:
1. Do not expand deep analysis.
2. Provide short rationale for why more data is needed.
3. Ask 1-3 minimum questions to unlock valid judgment.
4. Keep tone supportive but conservative.

## 5.6 ARIA wording example (same fact, better readability)

- Raw style: “FDA Class II. 510(k) pathway.”
- Humanized style: “현재 주신 정보 기준으로 FDA Class II 가능성이 높습니다. 일반적으로 510(k) 경로를 검토합니다. 다음으로 intended use 문장을 확정하면 판단 정확도를 높일 수 있습니다.”

## 5.7 Error handling (Part B)

1. Humanizer failure -> return original content with safety notice and log incident.
2. Fact-preservation check failure -> block rewritten output and fallback to original.
3. Latency threshold breach -> downgrade from `deep` to `standard` when allowed by output context.

## 5.8 Testing and acceptance (Part B)

### Heuristic checks

1. Sentence-length threshold
2. First-use terminology gloss rate
3. Presence of next action line
4. Confidence-state disclosure rate

### Golden-set checks

Representative scenarios:
- chat: insufficient info turn
- chat: skill-invoked determination turn
- assess: summary output
- project: summary output
- report: full report output

Pass criteria:
1. No semantic drift in protected facts
2. Readability/actionability metrics improved from baseline
3. Latency budget respected per preset class

**Gate B Acceptance**:
- Humanization is always on for user-visible outputs.
- Protected facts are unchanged.
- Efficiency controls prevent blanket deep rewriting.

---

## 6. Data Flow Overview

1. User request enters command.
2. Command gathers/loads context.
3. Skills produce structured analytical results.
4. Command builds output contract.
5. Humanization layer applies by contract + depth.
6. Safety/fact-preservation checks run.
7. Render/export (markdown/pdf/notion/gdocs).
8. Save output files and return response.

---

## 7. Rollout Strategy

1. Implement Gate A baseline contract and validators.
2. Stabilize command mappings and backward compatibility.
3. Enable Gate B in shadow mode (compare-only, no output replacement).
4. Promote Gate B to production mode after golden-set pass.

---

## 8. Non-Goals

1. Introducing a new user-facing command for humanization.
2. Weakening or softening legal/regulatory disclaimers.
3. Auto-executing next pipeline command without user approval.

---

## 9. Approvals

- Design direction approved by user on 2026-02-13.
- Gate model approved: single doc with dual independent gates.
- Core ARIA flow reaffirmed as non-negotiable.
- Part B efficiency update approved: insufficiency-short mode + depth presets + user override.

