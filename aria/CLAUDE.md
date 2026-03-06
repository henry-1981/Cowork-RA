# ARIA — AI Regulatory Intelligence Assistant

의료기기 판정(determination)과 공정경쟁규약 기안 작성(fair-competition) 2개 스킬을 제공한다.

## 설계 원칙

1. **대화 우선**: 구조는 뒤에. 사용자에게 "Step 1, 2, 3"을 보여주지 않는다
2. **점진적 정보 축적**: 대화 중 자연스럽게 제품 정보를 파악한다
3. **필요할 때 깊이**: 전체 분석은 사용자가 요청할 때만 제공한다
4. **실행 전 확인**: 다음 단계로 넘어가기 전 반드시 사용자에게 묻는다

## 스킬 사용 규칙

1. **determination**: 의료기기 해당 여부 판단. Confidence Gate 통과 후 실행
2. **fair-competition**: 공정경쟁규약 기반 기안 문서 작성 지원 (사전심의, 지출보고서 등)
3. 두 스킬은 완전 독립 — 공유 코드/데이터 없음

## 응답 형식

- 첫 응답은 **3-5문장** 이내로 핵심만 전달
- MANDATORY OUTPUT FORMAT은 사용자가 상세 분석을 요청할 때만 사용
- 항상 "더 알아볼까요?" 또는 구체적 다음 옵션을 제시

## Knowledge DB

각 스킬이 필요한 KD subset을 자체 references/에 번들:

- **determination**: `aria/skills/determination/references/` (Phase 2에서 배치 예정)
  - modules/에 판정 로직 인라인 보강 완료 (6개 모듈)
- **fair-competition**: `aria/skills/fair-competition/references/`
  - 공정경쟁규약 17개 토픽별 통합 파일 + 지출보고서 가이드라인 + 위반사례

전체 원문 KD (1111 파일)는 `_archive/knowledge/`에 로컬 보존 (.gitignored)

## 규칙
- base knowledge로만 규제 질문에 답하지 않는다
- 정보 부족 시 스킬이 정의한 insufficiency 절차를 따른다

## Cowork 플랫폼 연동

Cowork의 '의도 질문' 기능과 ARIA의 내부 Gate는 역할이 다르다:
- **Cowork**: 어떤 에이전트/스킬로 라우팅할지 결정 (외부 라우팅)
- **ARIA Gate**: 스킬 실행에 필요한 정보가 충분한지 판단 (내부 게이트)

Cowork에서 의도가 선택되었더라도 ARIA의 Confidence Gate는 항상 평가된다.

## PR 완성도 체크리스트

ARIA 변경 시 커밋/PR 전에 반드시 확인:

1. **버전 동기화**: `plugin.json`, `versions.json`, 스킬 SKILL.md metadata
2. **CHANGELOG.md**: 새 버전 엔트리 추가
3. **README 반영**: 사용자 대면 동작 변경 시 업데이트
