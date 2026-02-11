---
name: aria-connectors
description: >
  MCP connector integration patterns for ARIA domain skills.
  Provides centralized connector logic with category placeholders for tool-agnostic workflows.
  Use for MCP tool discovery, graceful degradation, and source attribution.
allowed-tools: Read Grep Glob ToolSearch
user-invocable: false
metadata:
  version: "0.0.4"
  category: "connector"
  status: "active"
  updated: "2026-02-11"
  modularized: "false"
  tags: "mcp, connector, integration, category-placeholders"
---

# ARIA MCP Connector Skill

## Quick Reference

**Purpose**: Centralized MCP connector integration patterns for ARIA domain skills with tool-agnostic category placeholders.

**Connector Categories**:
- `~~knowledge base`: Organization-specific regulatory data (Notion, Confluence)
- `~~regulatory docs`: External regulatory document verification (Context7)
- `~~cloud storage`: Document export and storage (Microsoft 365, Google Drive)
- `~~project tracker`: Regulatory project milestone tracking (Jira, Linear)
- `~~chat`: Team communication and regulatory update notifications (Slack, Teams)

**Key Patterns**:
- Tool discovery via ToolSearch
- Graceful degradation when MCP unavailable
- Source attribution in outputs
- Category-based tool-agnostic design

---

## Data Priority Framework

ARIA uses a built-in-first data priority model across all domain skills:

1. **Built-in Knowledge** (Priority 1): Embedded decision frameworks from FDA, EU MDR, MFDS regulations
2. **Module Files** (Priority 2): Detailed criteria in `modules/` loaded when deep analysis needed
3. **~~knowledge base** (Priority 3): Organization-specific regulatory data (supplementary)
4. **~~regulatory docs** (Priority 4): External regulatory document verification (supplementary)

**Critical Rule**: External MCP sources are supplementary, not required. All ARIA skills remain fully functional using built-in knowledge only.

---

## Knowledge Base Connector (`~~knowledge base`)

**Purpose**: Retrieve organization-specific regulatory data to supplement built-in knowledge.

### Tool Discovery

Use ToolSearch to load knowledge base MCP tools:

```
ToolSearch("notion")  # or "atlassian", "confluence"
```

Expected tools: `mcp__notion__*` (e.g., `mcp__notion__search`, `mcp__notion__fetch`)

### Workflow Pattern

1. **Tool Discovery**:
   - Call `ToolSearch("notion")` at skill start
   - Check if `~~knowledge base` tools are available

2. **If `~~knowledge base` tools available**:
   - Query organization database for region-specific regulatory data
   - Cross-reference with built-in knowledge
   - Attribute `~~knowledge base` as source in output

3. **If `~~knowledge base` tools unavailable or query fails**:
   - Gracefully degrade to built-in knowledge
   - Continue without interruption
   - No error shown to user

### Data Attribution

Always include "Sources:" section in output:

**When `~~knowledge base` used**:
```
Sources: Built-in Knowledge (FDA/EU MDR/MFDS regulations) + ~~knowledge base (organization-specific data)
```

**When `~~knowledge base` unavailable**:
```
Sources: Built-in Knowledge (FDA/EU MDR/MFDS regulations)
```

### Graceful Degradation

- `~~knowledge base` MCP is supplementary, not required
- If unavailable: Use built-in knowledge without notification
- If query fails: Log internally, proceed with built-in data
- Domain skill output remains fully functional

---

## Regulatory Docs Connector (`~~regulatory docs`)

**Purpose**: Verify and supplement regulatory document references (FDA 21 CFR, EU MDR, MFDS regulations).

### Tool Discovery

Use ToolSearch to load regulatory docs MCP tools:

```
ToolSearch("context7")
```

Expected tools: `mcp__context7__resolve-library-id`, `mcp__context7__get-library-docs`

### Workflow Pattern

1. **Tool Discovery**:
   - Call `ToolSearch("context7")` when regulatory citations are referenced
   - Check if `~~regulatory docs` tools are available

2. **If `~~regulatory docs` tools available**:
   - Resolve regulatory library IDs for FDA/EU MDR/MFDS regulations
   - Retrieve latest regulatory document versions
   - Cross-reference determination/classification/pathway criteria with latest regulations
   - Verify regulatory citations are current
   - Attribute `~~regulatory docs` as supplementary source in output

3. **If `~~regulatory docs` unavailable or query fails**:
   - Gracefully degrade to built-in knowledge
   - Continue without interruption
   - Include "(~~regulatory docs unavailable)" in Sources section

### Data Attribution

**When `~~regulatory docs` used**:
```
Sources: Built-in Knowledge + ~~regulatory docs (regulatory verification)
```

**When `~~regulatory docs` unavailable**:
```
Sources: Built-in Knowledge (~~regulatory docs unavailable)
```

### Graceful Degradation

- `~~regulatory docs` is supplementary, not required
- If unavailable: Use built-in knowledge without error message
- If query fails: Log internally, proceed with built-in data
- Domain skill output remains fully functional

---

## Cloud Storage Connector (`~~cloud storage`)

**Purpose**: Export regulatory reports to cloud storage format when `--format` flag is specified.

### Tool Discovery

Use ToolSearch to load cloud storage MCP tools:

```
ToolSearch("microsoft 365")  # or "google drive"
```

Expected tools: `mcp__ms365__create_file`, `mcp__ms365__upload_content`

### Workflow Pattern (when `--format` specified)

1. **Tool Discovery**:
   - Call `ToolSearch("microsoft 365")` when `--format` flag present
   - Check if `~~cloud storage` tools are available

2. **If `~~cloud storage` tools unavailable**:
   - Fallback to Markdown format
   - Display: "~~cloud storage MCP가 설정되지 않았습니다. Markdown 형식으로 보고서를 생성합니다."
   - Save to `.aria/products/{product-name}/{date}/briefing.md`
   - Include limitation notice in Data Source Attribution

3. **If `~~cloud storage` tools available**:
   - Generate briefing content in Markdown format first
   - Convert Markdown to cloud document-compatible format
   - Create document via `~~cloud storage` tools:
     - Title: "{Product Name} - Regulatory Briefing Report ({YYYY-MM-DD})"
     - Content: Converted briefing content
   - Display document link to user
   - Save Markdown backup to `.aria/products/{product-name}/{date}/briefing.md`

4. **If MCP tool call fails**:
   - Fallback to Markdown with error message
   - Error: "~~cloud storage에 연결할 수 없습니다. Markdown 형식으로 보고서를 생성합니다."

### Graceful Degradation

- `~~cloud storage` connector is optional
- Default output format is always Markdown (works without any MCP)
- Cloud document export is a convenience feature, not a requirement

---

## Project Tracker Connector (`~~project tracker`)

**Purpose**: Export regulatory plans to project tracking systems when integration is configured.

### Tool Discovery

Use ToolSearch to load project tracker MCP tools:

```
ToolSearch("atlassian")  # or "linear", "asana"
```

Expected tools: `mcp__atlassian__create_issue`, `mcp__atlassian__create_milestone`

### Workflow Pattern

1. **Tool Discovery**:
   - Call `ToolSearch("atlassian")` when project export is requested
   - Check if `~~project tracker` tools are available

2. **If `~~project tracker` tools available**:
   - Convert regulatory plan milestones to project tasks
   - Create issues/milestones via `~~project tracker` tools
   - Display project tracking link to user
   - Save Markdown backup to `.aria/products/{product-name}/{date}/plan.md`

3. **If `~~project tracker` tools unavailable**:
   - Output structured Markdown plan
   - Display: "~~project tracker MCP가 설정되지 않았습니다. Markdown 형식으로 계획을 생성합니다."

### Graceful Degradation

- `~~project tracker` integration is optional
- Regulatory plans work fully as structured Markdown without MCP integration

---

## Chat Connector (`~~chat`)

**Purpose**: Share regulatory intelligence with team communication platforms.

### Tool Discovery

Use ToolSearch to load chat MCP tools:

```
ToolSearch("slack")  # or "microsoft teams"
```

Expected tools: `mcp__slack__send_message`, `mcp__slack__create_channel`

### Workflow Pattern

1. **Tool Discovery**:
   - Call `ToolSearch("slack")` when sharing is requested
   - Check if `~~chat` tools are available

2. **If `~~chat` tools available**:
   - Format regulatory briefing for chat display
   - Send via `~~chat` tools to specified channel
   - Confirm delivery to user

3. **If `~~chat` tools unavailable**:
   - Output to local Markdown
   - Display: "~~chat MCP가 설정되지 않았습니다. 로컬 파일로 저장되었습니다."

### Graceful Degradation

- `~~chat` integration is optional
- All regulatory outputs work as local Markdown files without chat integration

---

## Domain Skill Integration Pattern

Domain skills reference this connector skill instead of duplicating MCP integration logic.

### How Domain Skills Use This Connector Skill

**Reference Pattern in Domain Skills**:

Replace detailed MCP workflow sections with:

```markdown
## Data Source Strategy

1. **Built-in Knowledge** (Primary): Embedded decision frameworks from FDA, EU MDR, MFDS regulations
2. **Module Files** (On-demand): Detailed criteria in `modules/` loaded when deep analysis needed
3. **~~knowledge base** (Supplementary): Organization-specific regulatory data
4. **~~regulatory docs** (Verification): External regulatory document verification

For MCP integration patterns (tool discovery, graceful degradation, source attribution), see `skills/connectors/SKILL.md`.
```

### Benefits

- **Single Source of Truth**: MCP patterns defined once, referenced by all domain skills
- **Consistency**: All domain skills follow identical MCP integration behavior
- **Tool-Agnostic**: Category placeholders allow user choice of tools
- **Maintainability**: Update MCP patterns in one location
- **Reduced Duplication**: Eliminates ~300 lines of duplicate MCP workflow from 4 domain skills

---

## Unified Graceful Degradation Matrix

| Connector | Available | Action | User Notification |
|-----------|-----------|--------|-------------------|
| ~~knowledge base | Yes | Use organization data + built-in knowledge | Attribution in Sources |
| ~~knowledge base | No | Use built-in knowledge only | None (silent degradation) |
| ~~regulatory docs | Yes | Use regulatory verification + built-in knowledge | Attribution in Sources |
| ~~regulatory docs | No | Use built-in knowledge only | "(~~regulatory docs unavailable)" in Sources |
| ~~cloud storage | Yes | Export to cloud storage + Markdown backup | Document link displayed |
| ~~cloud storage | No | Export to Markdown only | "Markdown 형식으로 보고서를 생성합니다." |
| ~~project tracker | Yes | Export to project tracker + Markdown | Project link displayed |
| ~~project tracker | No | Export to Markdown only | "Markdown 형식으로 계획을 생성합니다." |
| ~~chat | Yes | Share to chat channel | Delivery confirmation |
| ~~chat | No | Save to local file | "로컬 파일로 저장되었습니다." |

---

## Source Attribution Templates

### Determination Skill Attribution

**Full Attribution** (all sources used):
```
Sources: Built-in Knowledge (FDA 21 CFR 201(h), EU MDR Article 2(1), MFDS 의료기기법) + ~~knowledge base (organization precedents) + ~~regulatory docs (regulatory verification)
```

**Built-in Only**:
```
Sources: Built-in Knowledge (FDA 21 CFR 201(h), EU MDR Article 2(1), MFDS 의료기기법)
```

### Classification Skill Attribution

**Full Attribution**:
```
Data Source Attribution:
- Built-in Knowledge: Used (FDA CFR, EU MDR Annex VIII, MFDS classification criteria)
- ~~knowledge base: Used (organization classification precedents)
- ~~regulatory docs: Used (regulatory rule verification)
```

**Partial Attribution** (~~regulatory docs unavailable):
```
Data Source Attribution:
- Built-in Knowledge: Used (FDA CFR, EU MDR Annex VIII, MFDS classification criteria)
- ~~knowledge base: Used (organization classification precedents)
- ~~regulatory docs: Not available
```

### Pathway Skill Attribution

**Full Attribution**:
```
Sources: Built-in Knowledge (FDA Guidance, EU MDR Annex IV/IX/X, MFDS 의료기기법) + ~~knowledge base (organization pathway histories) + ~~regulatory docs (regulatory verification)
```

### Briefing Skill Attribution

**Appendix B: Data Sources**:
```
- Built-in knowledge: FDA, EU MDR, MFDS decision frameworks (2026-01 knowledge base)
- ~~knowledge base: Organization-specific regulatory data (if used)
- ~~regulatory docs: External regulatory document verification (if used)
- ~~cloud storage: Document export (if --format flag used)
```

---

## Version History

**v0.0.4** (2026-02-11):
- Updated to category placeholder syntax (`~~category`)
- Aligned with official Cowork plugin connector pattern
- Added `~~project tracker` and `~~chat` connectors
- Updated metadata version to 0.0.4

**v0.0.1** (2026-02-11):
- Initial connector skill creation
- Centralized MCP integration patterns for specific tools
- Data priority framework (built-in-first)
- Graceful degradation matrix
- Source attribution templates
- Domain skill integration pattern

---

**Knowledge Base Cutoff**: 2026-01
**Maintained by**: ARIA Plugin Team
