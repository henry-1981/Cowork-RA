---
name: aria-connectors
description: >
  MCP connector integration patterns for ARIA domain skills.
  Provides centralized connector logic for Notion (database), Context7 (documentation),
  and Google Drive (storage). Use for MCP tool discovery, graceful degradation, and source attribution.
allowed-tools: Read Grep Glob ToolSearch
user-invocable: false
metadata:
  version: "0.0.1"
  category: "connector"
  status: "active"
  updated: "2026-02-11"
  modularized: "false"
  tags: "mcp, notion, context7, google-drive, connector, integration"
---

# ARIA MCP Connector Skill

## Quick Reference

**Purpose**: Centralized MCP connector integration patterns for ARIA domain skills.

**Connector Categories**:
- **Database Connectors**: Notion (organization-specific regulatory data)
- **Documentation Connectors**: Context7 (external regulatory document verification)
- **Storage Connectors**: Google Drive (document export and storage)

**Key Patterns**:
- Tool discovery via ToolSearch
- Graceful degradation when MCP unavailable
- Source attribution in outputs

---

## Data Priority Framework

ARIA uses a built-in-first data priority model across all domain skills:

1. **Built-in Knowledge** (Priority 1): Embedded decision frameworks from FDA, EU MDR, MFDS regulations
2. **Module Files** (Priority 2): Detailed criteria in `modules/` loaded when deep analysis needed
3. **Notion MCP** (Priority 3): Organization-specific regulatory data (supplementary)
4. **Context7 MCP** (Priority 4): External regulatory document verification (supplementary)

**Critical Rule**: External MCP sources are supplementary, not required. All ARIA skills remain fully functional using built-in knowledge only.

---

## Database Connector (Notion)

**Purpose**: Retrieve organization-specific regulatory data to supplement built-in knowledge.

### Tool Discovery

Use ToolSearch to load Notion MCP tools:

```
ToolSearch("notion")
```

Expected tools: `mcp__notion__*` (e.g., `mcp__notion__search`, `mcp__notion__fetch`)

### Workflow Pattern

1. **Tool Discovery**:
   - Call `ToolSearch("notion")` at skill start
   - Check if Notion tools are available

2. **If Notion tools available**:
   - Query organization database for region-specific regulatory data
   - Cross-reference with built-in knowledge
   - Attribute Notion as source in output

3. **If Notion tools unavailable or query fails**:
   - Gracefully degrade to built-in knowledge
   - Continue without interruption
   - No error shown to user

### Data Attribution

Always include "Sources:" section in output:

**When Notion used**:
```
Sources: Built-in Knowledge (FDA/EU MDR/MFDS regulations) + Notion DB (organization-specific data)
```

**When Notion unavailable**:
```
Sources: Built-in Knowledge (FDA/EU MDR/MFDS regulations)
```

### Graceful Degradation

- Notion MCP is supplementary, not required
- If unavailable: Use built-in knowledge without notification
- If query fails: Log internally, proceed with built-in data
- Domain skill output remains fully functional

---

## Documentation Connector (Context7)

**Purpose**: Verify and supplement regulatory document references (FDA 21 CFR, EU MDR, MFDS regulations).

### Tool Discovery

Use ToolSearch to load Context7 MCP tools:

```
ToolSearch("context7")
```

Expected tools: `mcp__context7__resolve-library-id`, `mcp__context7__get-library-docs`

### Workflow Pattern

1. **Tool Discovery**:
   - Call `ToolSearch("context7")` when regulatory citations are referenced
   - Check if Context7 tools are available

2. **If Context7 tools available**:
   - Resolve regulatory library IDs for FDA/EU MDR/MFDS regulations
   - Retrieve latest regulatory document versions
   - Cross-reference determination/classification/pathway criteria with latest regulations
   - Verify regulatory citations are current
   - Attribute Context7 as supplementary source in output

3. **If Context7 unavailable or query fails**:
   - Gracefully degrade to built-in knowledge
   - Continue without interruption
   - Include "(Context7 unavailable)" in Sources section

### Data Attribution

**When Context7 used**:
```
Sources: Built-in Knowledge + Context7 (regulatory verification)
```

**When Context7 unavailable**:
```
Sources: Built-in Knowledge (Context7 unavailable)
```

### Graceful Degradation

- Context7 is supplementary, not required
- If unavailable: Use built-in knowledge without error message
- If query fails: Log internally, proceed with built-in data
- Domain skill output remains fully functional

---

## Storage Connector (Google Drive)

**Purpose**: Export regulatory reports to Google Docs format when `--format gdocs` flag is specified.

### Tool Discovery

Use ToolSearch to load Google Drive MCP tools:

```
ToolSearch("google drive")
```

Expected tools: `mcp__gdrive__create_file`, `mcp__gdrive__upload_content`

### Workflow Pattern (when `--format gdocs` specified)

1. **Tool Discovery**:
   - Call `ToolSearch("google drive")` when `--format gdocs` flag present
   - Check if Google Drive tools are available

2. **If Google Drive tools unavailable**:
   - Fallback to Markdown format
   - Display: "Google Drive MCP가 설정되지 않았습니다. Markdown 형식으로 보고서를 생성합니다."
   - Save to `.aria/products/{product-name}/{date}/briefing.md`
   - Include limitation notice in Data Source Attribution

3. **If Google Drive tools available**:
   - Generate briefing content in Markdown format first
   - Convert Markdown to Google Docs-compatible format
   - Create document via `mcp__gdrive__create_file`:
     - Title: "{Product Name} - Regulatory Briefing Report ({YYYY-MM-DD})"
     - MimeType: `application/vnd.google-apps.document`
     - Content: Converted briefing content
   - Display Google Docs link to user
   - Save Markdown backup to `.aria/products/{product-name}/{date}/briefing.md`

4. **If MCP tool call fails**:
   - Fallback to Markdown with error message
   - Error: "Google Drive에 연결할 수 없습니다. Markdown 형식으로 보고서를 생성합니다."

### Graceful Degradation

- Google Drive connector is optional
- Default output format is always Markdown (works without any MCP)
- Google Docs export is a convenience feature, not a requirement

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
3. **Notion MCP** (Supplementary): Organization-specific regulatory data
4. **Context7 MCP** (Verification): External regulatory document verification

For MCP integration patterns (tool discovery, graceful degradation, source attribution), see `skills/connectors/SKILL.md`.
```

### Benefits

- **Single Source of Truth**: MCP patterns defined once, referenced by all domain skills
- **Consistency**: All domain skills follow identical MCP integration behavior
- **Maintainability**: Update MCP patterns in one location
- **Reduced Duplication**: Eliminates ~300 lines of duplicate MCP workflow from 4 domain skills

---

## Unified Graceful Degradation Matrix

| Connector | Available | Action | User Notification |
|-----------|-----------|--------|-------------------|
| Notion | Yes | Use organization data + built-in knowledge | Attribution in Sources |
| Notion | No | Use built-in knowledge only | None (silent degradation) |
| Context7 | Yes | Use regulatory verification + built-in knowledge | Attribution in Sources |
| Context7 | No | Use built-in knowledge only | "(Context7 unavailable)" in Sources |
| Google Drive | Yes | Export to Google Docs + Markdown backup | Google Docs link displayed |
| Google Drive | No | Export to Markdown only | "Markdown 형식으로 보고서를 생성합니다." |

---

## Source Attribution Templates

### Determination Skill Attribution

**Full Attribution** (all sources used):
```
Sources: Built-in Knowledge (FDA 21 CFR 201(h), EU MDR Article 2(1), MFDS 의료기기법) + Notion DB (organization precedents) + Context7 (regulatory verification)
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
- Notion DB: Used (organization classification precedents)
- Context7: Used (regulatory rule verification)
```

**Partial Attribution** (Context7 unavailable):
```
Data Source Attribution:
- Built-in Knowledge: Used (FDA CFR, EU MDR Annex VIII, MFDS classification criteria)
- Notion DB: Used (organization classification precedents)
- Context7: Not available
```

### Pathway Skill Attribution

**Full Attribution**:
```
Sources: Built-in Knowledge (FDA Guidance, EU MDR Annex IV/IX/X, MFDS 의료기기법) + Notion DB (organization pathway histories) + Context7 (regulatory verification)
```

### Briefing Skill Attribution

**Appendix B: Data Sources**:
```
- Built-in knowledge: FDA, EU MDR, MFDS decision frameworks (2026-01 knowledge base)
- Notion DB: Organization-specific regulatory data (if used)
- Context7: External regulatory document verification (if used)
- Google Drive: Document export (if --format gdocs used)
```

---

## Version History

**v0.0.1** (2026-02-11):
- Initial connector skill creation
- Centralized MCP integration patterns for Notion, Context7, Google Drive
- Data priority framework (built-in-first)
- Graceful degradation matrix
- Source attribution templates
- Domain skill integration pattern

---

**Knowledge Base Cutoff**: 2026-01
**Maintained by**: ARIA Plugin Team
