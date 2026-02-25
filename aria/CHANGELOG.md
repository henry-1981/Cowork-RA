# Changelog

All notable changes to the ARIA plugin will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.1] - 2026-02-25

### Fixed
- depth hint("상세 분석", "심화 수준")가 스킬 체이닝을 트리거하지 않도록 분리
- Gate 2(Mandatory Confidence Gate) 무조건 평가 규칙 명시 — depth와 무관
- "전체 분석" 요청 시 assess 리다이렉트 대신 chat 내 확인 후 순차 실행으로 변경

### Added
- chat.md: Depth Hint Keywords 매핑 섹션 (Level 1/2/3 + 전체 분석 분리)
- chat.md: Full Analysis Request in Chat 규칙 (확인 → 순차 → 중단 가능)
- CLAUDE.md: Cowork 플랫폼 연동 섹션 (외부 라우팅 ≠ 내부 게이트)
- using-aria: depth≠chaining 금지 규칙
- 테스트: CH-010/011/012 시나리오 7개 추가

### Changed
- chat.md Output Contract default depth: `standard` → `express`
- using-aria version: 0.2.0 → 0.3.1
- chat command version: 0.1.2 → 0.1.3

## [0.3.0] - 2026-02-25

### Fixed
- SPEC-ARIA-003 설계 원칙 복원 — RA-Bench 최적화로 소실된 UX 원칙 재적용
- 자동 스킬 체인 제거 (determination → classification → pathway 자동 실행 금지)
- Progressive disclosure 실행 규칙 추가 (Level 1/2/3 단계적 깊이)

### Changed
- SKILL.md 모듈화 — 입력 토큰 53% 절감
  - determination: Combination/Annex XVI → modules/
  - classification: Decision Framework/4-Gate → modules/
  - pathway: De Novo/Clinical Endpoints → modules/
- using-aria: 점진적 스킬 호출로 변경 (한 번에 하나, 사용자 확인 후 진행)
- Level 1 응답에서 Knowledge DB 로드 제거 — 내장 Decision Framework만 사용

## [0.2.0] - 2026-02-24

### Added
- `aria/knowledge/` — 규제 프레임워크 레퍼런스 DB (FDA, EU MDR, MFDS, IMDRF)
- `knowledge-refresh` 스킬 — 월간 Knowledge DB 갱신
- session-start hook — Knowledge DB 갱신 알림

### Changed
- classification/SKILL.md — 품목코드/Override 테이블 → Knowledge DB 참조
- pathway/SKILL.md — Grade→Pathway 테이블 → Knowledge DB 참조

### Removed
- evidence-catalog.md (3개) — Knowledge DB로 대체
- aria-reference.md — Knowledge DB로 대체

### Deprecated
- aria-bench-wrapper.sh — Knowledge DB + 스킬 체인으로 대체

## [0.1.5] - 2026-02-13

### Changed
- Updated docs tracking policy so `docs/plans/**` stays local-only while `docs/development/**` remains tracked
- Synchronized plugin version between:
  - `aria/.claude-plugin/plugin.json`
  - `.claude-plugin/marketplace.json`
  - Version updated to `0.1.5`

## [0.1.4] - 2026-02-13

### Added
- Reorganized root onboarding docs into bilingual single-file `README.md` (Korean + English)
- Rewrote `aria/README.md` as a power-user guide focused on command/skill usage patterns
- Moved version policy document to developer docs: `docs/development/versioning.md`

### Changed
- Removed version-policy references from user-facing READMEs
- Synchronized plugin version between:
  - `aria/.claude-plugin/plugin.json`
  - `.claude-plugin/marketplace.json`
  - Version updated to `0.1.4`

## [0.1.3] - 2026-02-13

### Added
- Version policy document: `aria/VERSIONING.md`
- Command-level version registry: `aria/commands/versions.json`
- Version guard script: `scripts/versioning/check_version_policy.py`
- GitHub Actions validation workflow: `.github/workflows/version-policy.yml`

### Changed
- Synchronized plugin version between:
  - `aria/.claude-plugin/plugin.json`
  - `.claude-plugin/marketplace.json`

## [0.1.2] - 2026-02-12

### Added
- New `aria-compliance` skill: Korean medical device marketing compliance advisor based on KMDIA Fair Competition Code (공정경쟁규약)
- Compliance skill references: regulation.md (Code full text), activity-guide.md (checklist + Committee Guidance 2024), faq.md (70+ FAQs + violation cases)
- Compliance keyword routing in `/aria:chat` for transparent skill invocation

### Changed
- Updated `/aria:chat` Conversational Skill Routing with Compliance Triggers block
- Updated Keyword Reference table with compliance routing context
- Updated plugin.json keywords with compliance, fair-competition, KMDIA
- Updated README.md with 6th skill documentation and directory structure

## [0.0.4] - 2026-02-11

### Added
- Plugin-level `.mcp.json` with HTTP MCP servers (Notion, Atlassian, Slack, Microsoft 365)
- Category-based connector design with `~~category` placeholders
- Standard Cowork plugin connector architecture

### Changed
- Rewrote CONNECTORS.md in official Cowork plugin format
- Updated connector skill to use tool-agnostic category placeholders
- Unified all versions to 0.0.4 across plugin.json, marketplace.json, and 8 skills
- Updated README.md with connector architecture documentation

### Removed
- "ARIA Plugin Version: 2.0.0" inline text from 7 skill files (duplicate metadata)

## [0.0.2] - 2026-02-XX

### Changed
- Centralized MCP connector configuration
- Version alignment to release tag 0.0.2

## [0.0.1] - 2026-01-XX

### Added
- Initial ARIA plugin release
- 8 core cognitive skills (briefing, classification, comparison, connectors, determination, estimation, pathway, planning)
- Basic MCP server integration
