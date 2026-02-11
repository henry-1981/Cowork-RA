# Changelog

All notable changes to ARIA Cowork Plugin will be documented in this file.

## [Phase 3] - 2026-02-11

### Added

- **Pathway Skill**: FDA/EU MDR/MFDS 규제 경로 선택 로직
  - `/aria:pathway` 명령 추가
  - Traffic light system 통합 (GREEN/YELLOW 위험 평가)
  - Context Simplifier로 pipeline 연결 지원
  - 국가별 규제 제출 경로 비교 및 추천 기능

- **Estimation Skill**: 비용 및 일정 추정 프레임워크
  - `/aria:estimate` 명령 추가
  - 3-point 추정 (optimistic/expected/pessimistic)
  - 5가지 비용 카테고리 (컨설팅, 시험, 수수료, NB, 임상)
  - 경로별 비용 범위 및 마일스톤 타임라인 제공

- **Planning Skill**: 규제 이정표 계획 생성
  - `/aria:plan` 명령 추가
  - 4-6 단계 마일스톤 구조
  - Dependency mapping 및 critical path 식별
  - 체크포인트 및 책임 주체 정의

- **Test Coverage**: 45+ Gherkin 테스트 시나리오 추가
  - 긍정/부정/통합 테스트 커버리지
  - Phase 3 acceptance criteria 100% 검증
  - ER-004, ER-005, ER-006 요구사항 완전 검증

### Quality

- **TRUST 5 Score**: 4.5/5.0 (Excellent)
- **Requirements Coverage**: 15/15 (100%)
- **Total Implementation**: 8 files, 2,713 lines
- **Zero Critical Issues**

---

## [Phase 2] - 2026-02-10

### Added

- **Determination Skill**: FDA/EU MDR/MFDS 의료기기 판정 로직
  - `/aria:determine` 명령 추가
  - 4단계 통합 워크플로우 (SPEC v4.0.0 반영)
  - 반복 출력 방지 지시문 (anti-loop directive)

- **Classification Skill**: 다지역 등급 분류 매트릭스
  - `/aria:classify` 명령 추가
  - FDA/EU MDR/MFDS 분류 로직
  - `--optimize` 플래그 지원 (등급 최적화 제안)

- **Plugin Scaffold**: 플러그인 기본 구조
  - `.claude-plugin/plugin.json` (minimal metadata)
  - `.mcp.json` (Notion, Context7, Google Drive)
  - `CONNECTORS.md` (MCP 커넥터 카테고리 문서)
  - `README.md` (설치 가이드 및 커맨드 참조)
  - `aria.local.md` (조직별 설정 템플릿)

### Quality

- **TRUST 5 Score**: 4.6/5.0 (Excellent)
- **VALID Score**: 4.7/5.0 (Excellent)
- **Overall Quality**: 94/100

---

## [Phase 1] - 2026-02-10

### Added

- Plugin infrastructure and foundation
- MCP connector configuration
- Installation documentation
- Security guidelines for .aria/ directory

---

**버전 정책**: Semantic Versioning (MAJOR.MINOR.PATCH)
**라이선스**: Apache-2.0
**지원**: GitHub Issues에서 문제 보고 및 기능 요청
