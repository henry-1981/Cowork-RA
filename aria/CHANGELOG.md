# Changelog

All notable changes to the ARIA plugin will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.4] - 2026-02-27

### Added
- `scripts/verify-knowledge-db.sh` — 3-Agent Knowledge DB 검증 파이프라인
  - Stage 1 (Extractor): YAML frontmatter + 본문 통계 + 핵심 식별자 추출
  - Stage 2 (Verifier): 원본 PDF 독립 재추출 diff 대조
  - Stage 3 (Structural Checker): frontmatter 완결성, 디렉토리-내용 일치, 인코딩 검증
- 질의응답집 OCR 변환 (벡터 PDF → 600 DPI tesseract kor+eng)

### Changed
- 스킬 Knowledge 참조를 MFDS 원문 DB 경로로 갱신 (determination, classification, pathway, knowledge-refresh)
- `mfds-criteria.md` 운영 규칙 인라인 보강 (4-Gate, Risk Matrix, 7-Digit Code)
- modules/ `Loaded Knowledge` 참조 → `법적 근거` 원문 법률 참조로 변경

### Skill Versions
- determination: 0.3.1 → 0.3.3
- classification: 0.3.1 → 0.3.3
- pathway: 0.3.0 → 0.3.1
- knowledge-refresh: 0.2.1 → 0.2.2

## [0.3.3] - 2026-02-26

### Added
- `aria/knowledge/mfds/` — MFDS 원문 DB 50개 파일 (pdftotext 기계적 변환)
  - `01-법령/01-의료기기법/` — 의료기기법, 시행령, 별표 6종, 고시 8종 (18 파일)
  - `01-법령/02-체외진단의료기기법/` — 체외진단법, 시행령, 시행규칙, 별표, 고시 (9 파일)
  - `01-법령/03-디지털의료제품법/` — 디지털의료제품법, 시행령, 시행규칙, 고시 5종 (8 파일)
  - `02-가이드라인/` — SaMD 허가심사 가이드라인 15종
- `scripts/convert-pdfs-to-md.sh` — PDF→Markdown 배치 변환 스크립트

### Changed
- CLAUDE.md Knowledge DB 섹션: 원문 DB + 레거시 참조 2계층 구조로 개편
- 원칙 명시: PDF 원문을 그대로 markdown으로 변환. 요약/재구성/선택적 추출 금지

## [0.3.2] - 2026-02-26

### Added
- `knowledge/shared/mfds-digital-classification.md` — 디지털의료제품법 분류 운영 규칙 SSOT
  - 4-Gate, 7-digit 코드 생성, Risk Matrix, Medical Impact 매핑, Malfunction Adjustment

### Fixed
- MFDS 분류 규칙 소실 복원 — cross-skill 참조 → 공유 Knowledge DB 참조로 전환
  - classification 모듈: `determination/modules/` 참조 제거, Knowledge DB 참조로 교체
  - determination 모듈: 인라인 규칙 → Knowledge DB 참조로 일원화

### Changed
- classification Step 0 로딩 최적화: 전체 로드 → 관련 jurisdiction만 선택 로드
- classification version: 0.3.0 → 0.3.1
- determination version: 0.3.0 → 0.3.1

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
- using-aria version: 0.2.0 → 0.2.1
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
