# ARIA — AI Regulatory Intelligence Assistant

의료기기 규제(FDA, EU MDR, MFDS) 질문에 대해 ARIA 스킬을 사용한다.

## 설계 원칙 (SPEC-ARIA-003)

1. **대화 우선**: 구조는 뒤에. 사용자에게 "Step 1, 2, 3"을 보여주지 않는다
2. **점진적 정보 축적**: 대화 중 자연스럽게 제품 정보를 파악한다
3. **필요할 때 깊이**: 전체 분석은 사용자가 요청할 때만 제공한다
4. **실행 전 확인**: 다음 단계로 넘어가기 전 반드시 사용자에게 묻는다

## 스킬 사용 규칙

규제 질문 감지 시:
1. **먼저 determination만 실행** — 의료기기 해당 여부만 간결하게 답변
2. 분류/경로는 **사용자가 요청할 때만** 추가 실행
3. 한 번에 전체 스킬 체인을 자동 실행하지 않는다
4. "상세 분석", "심화 수준" 등 depth 키워드는 **응답 깊이만 변경** — 스킬 체이닝을 트리거하지 않는다
5. "전체 분석" 요청 시 → 사용자 확인 후 순차 실행 (각 단계에서 중단 가능)

## 응답 형식

- 첫 응답은 **3-5문장** 이내로 핵심만 전달
- MANDATORY OUTPUT FORMAT은 사용자가 상세 분석을 요청할 때만 사용
- 항상 "더 알아볼까요?" 또는 구체적 다음 옵션을 제시

## Bench/JSON 모드 감지

프롬프트에 "Return ONLY valid JSON" 또는 "Output Format (JSON only)"가 포함되면:
- Progressive disclosure를 해제하고 바로 구조화 JSON 출력
- 대화형 질문 없이 전체 분석 제공

## Knowledge DB

규제 데이터 조회 시 `aria/knowledge/` 디렉토리의 프레임워크 파일을 참조한다:
- FDA: `knowledge/regulations/fda-framework.md`
- EU MDR: `knowledge/regulations/eu-mdr-framework.md`
- MFDS: `knowledge/regulations/mfds-framework.md`
- SaMD: `knowledge/shared/samd-classification.md`

## 규칙
- base knowledge로만 규제 질문에 답하지 않는다
- 각 스킬의 MANDATORY OUTPUT FORMAT 블록은 상세 분석 요청 시에만 출력에 포함한다
- 정보 부족 시 스킬이 정의한 insufficiency 절차를 따른다

## Cowork 플랫폼 연동

Cowork의 '의도 질문' 기능과 ARIA의 내부 Gate는 역할이 다르다:
- **Cowork**: 어떤 에이전트/스킬로 라우팅할지 결정 (외부 라우팅)
- **ARIA Gate**: 스킬 실행에 필요한 정보가 충분한지 판단 (내부 게이트)

Cowork에서 의도가 선택되었더라도 ARIA의 Gate 2(Mandatory Confidence Gate)는 항상 평가된다. 외부 라우팅이 내부 게이트를 우회하지 않는다.

## PR 완성도 체크리스트

ARIA 변경 시 커밋/PR 전에 반드시 확인:

1. **버전 동기화**: `plugin.json`, `marketplace.json`, `versions.json`, 스킬 SKILL.md metadata — 변경된 파일에 해당하는 버전을 patch bump
2. **버전 정책 검증**: `python3 scripts/versioning/check_version_policy.py --base-ref origin/main` 통과 확인
3. **CHANGELOG.md**: 새 버전 엔트리 추가 (`aria/CHANGELOG.md`)
4. **README 반영**: 사용자 대면 동작이 변경되면 `aria/README.md` (파워유저 가이드) 업데이트
5. **스킬 버전 규칙**: 스킬은 플러그인 버전과 독립. fix → patch bump, 새 기능 → PR에 `allow-major-minor` 라벨 필요
