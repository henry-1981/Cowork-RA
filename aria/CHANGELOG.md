# Changelog

All notable changes to the ARIA plugin will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
