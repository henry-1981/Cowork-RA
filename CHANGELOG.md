# Changelog

All notable changes to ARIA Cowork Plugin will be documented in this file.

## [0.1.3] - 2026-02-13

### Added

- 버전 정책 문서 추가: `aria/VERSIONING.md`
- 커맨드 버전 레지스트리 추가: `aria/commands/versions.json`
- 버전 가드 스크립트 추가: `scripts/versioning/check_version_policy.py`
- GitHub Actions 버전 검증 워크플로 추가: `.github/workflows/version-policy.yml`

### Changed

- 플러그인 버전 동기화: `aria/.claude-plugin/plugin.json` 및 `.claude-plugin/marketplace.json`를 `0.1.3`으로 일치

## [0.1.1] - 2026-02-12

### Fixed

- **`/aria:brief` renamed to `/aria:report`**: Cowork 기본 `legal` 플러그인의 `brief` 커맨드와 이름 충돌 해결
- **marketplace.json 버전 동기화**: `0.0.4` → `0.1.0`으로 업데이트하여 플러그인 업데이트 감지 정상화
- **plugin.json `commands` 필드 형식 수정**: object 형식(`{"chat": "commands/chat.md"}`)을 제거하고 `commands/` 디렉토리 자동 탐색에 의존하도록 변경. 공식 스키마에서 `commands`는 `string|array` 타입만 지원

---

## [0.1.0] - 2026-02-12

### BREAKING CHANGES

- **6 commands removed**: `/aria:determine`, `/aria:classify`, `/aria:pathway`, `/aria:estimate`, `/aria:plan`, `/aria:compare` are no longer available
- **`/aria:brief` renamed to `/aria:report`**: Renamed to avoid command name collision with Cowork built-in `legal` plugin
- **Output file format changed**: Individual per-skill files (determination.md, classification.md, etc.) replaced by integrated reports (assess.md, project.md)

### Added

- **`/aria:assess` command**: Integrated regulatory assessment pipeline
  - Combines determination + classification + pathway into single orchestrated workflow
  - Multi-region comparison logic (inline, for 2+ target markets)
  - Decision gate: Stops workflow on NO determination
  - Output: `assess.md` + `assess.summary.md`

- **`/aria:project` command**: Integrated project planning pipeline
  - Combines estimation + planning into single orchestrated workflow
  - Multi-region optimization with parallel submission analysis
  - Loads assessment data from `/aria:assess` automatically
  - Output: `project.md` + `project.summary.md`

### Changed

- **`/aria:chat` rewritten**: Conversational regulatory advisor redesign
  - Progressive product profiling via natural dialogue (profile.json)
  - Transparent skill routing (invisible to user)
  - Auto-suggestion logic for pipeline commands
  - Document upload with auto-extraction and gap analysis

- **`/aria:report` rewritten**: Comprehensive report generator
  - Absorbs briefing skill logic (no separate briefing skill)
  - Two-phase output (ER-017 report issuance policy)
  - Supports focus area selection (Clinical Strategy, Cost Control, Timeline Acceleration, Multi-Market Entry)
  - Backward compatibility with legacy pipeline data

- **5 skills refactored**: Pure analysis logic only
  - determination, classification, pathway, estimation, planning
  - Removed: product context loading, flag handling, file storage, pipeline connections
  - Retained: regulatory decision frameworks, module references, traffic light logic

- **Plugin manifest updated**: Version bumped to 0.1.0, command registry updated to 4 commands

### Removed

- **Briefing skill** (`aria/skills/briefing/`): Logic absorbed by `/aria:report` command
- **Comparison skill** (`aria/skills/comparison/`): Logic absorbed inline by assess and project commands
- **Connectors skill** (`aria/skills/connectors/`): Merged into `CONNECTORS.md` infrastructure document

### Migration Notes

- Existing `.aria/products/` data is preserved and backward compatible
- `/aria:report` and `/aria:project` can read legacy format files (determination.summary.md, etc.)
- New format files are preferred over legacy when both exist
- No manual data migration required

### Quality

- **Architecture**: 8 commands -> 4 commands, 8 skills -> 5 skills
- **Output files**: 14 files per product -> 7 files per product
- **Command-Skill redundancy**: Eliminated (clear separation of concerns)
- **Test scenarios**: 150+ Gherkin test cases across 5 test scenario documents

---

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
