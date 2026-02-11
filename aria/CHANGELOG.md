# Changelog

All notable changes to the ARIA plugin will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
