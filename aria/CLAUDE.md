# ARIA — AI Regulatory Intelligence Assistant

ARIA는 단일 명령 `assist` 아래에서 `determination`과 `fair-competition` 두 스킬만 제공한다.

## 설계 원칙

1. **대화 우선**: 내부 단계는 숨기고 사용자에게는 자연스러운 흐름만 보여준다.
2. **정보 부족 시 보류**: 확정 판단에 필요한 정보가 없으면 먼저 질문한다.
3. **깊이는 요청 기반**: 기본 응답은 짧게, 상세 출력은 사용자가 원할 때만 제공한다.
4. **레거시 표면 제거**: 삭제된 커맨드/스킬/전역 지식 경로를 현재 문서와 스킬 정의에 다시 노출하지 않는다.

## 현재 shipped 구조

- Command: `assist`
- Skills:
  - `determination`
  - `fair-competition`

## 스킬 사용 규칙

1. `determination`
   - 의료기기 해당 여부 판단
   - 기본 근거는 `SKILL.md`와 `modules/`
2. `fair-competition`
   - 공정경쟁규약 검토와 내부 승인용 기안 지원
   - 번들 reference는 `aria/skills/fair-competition/references/`
3. 두 스킬은 독립적이다. 삭제된 전역 knowledge 트리를 현재 shipped 개념으로 설명하지 않는다.

## 응답 형식

- 첫 응답은 3-5문장 이내
- 확정 판단 전에 필요한 입력을 확인
- 항상 다음 선택지 또는 후속 질문을 제시

## Repository Policy

- repo에는 현재 v1.0에 필요한 파일만 남긴다.
- 과거 설계 문서, 일회성 변환 스크립트, 실험용 테스트는 로컬 `_archive/`에만 둔다.
- `_archive/`는 shipped surface가 아니다.

## 변경 체크리스트

ARIA 관련 변경 시 다음을 확인한다.

1. 현재 문서가 `assist + 2 skills` 구조와 일치하는지
2. 제거된 커맨드/스킬을 active surface로 다시 소개하지 않는지
3. `plugin.json`, `versions.json`, `SKILL.md` 메타데이터가 모순되지 않는지
