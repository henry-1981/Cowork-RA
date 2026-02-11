# Connectors

ARIA plugin connector documentation in standard Cowork plugin format.

## How tool references work

ARIA plugin uses **tool-agnostic design** with category placeholders. Instead of hardcoding specific product names (like "Notion" or "Slack"), workflows are described in terms of **categories** (like `~~knowledge base` or `~~chat`).

This approach allows users to choose their preferred tools within each category. The plugin's `.mcp.json` file pre-configures HTTP MCP servers for each category, but users can substitute alternative tools with similar capabilities.

### Category Placeholder Syntax

Throughout ARIA skills and documentation, you'll see references like:

- `~~knowledge base` → Refers to any knowledge base tool (e.g., Notion, Confluence, Guru)
- `~~project tracker` → Refers to any project management tool (e.g., Jira, Linear, Asana)
- `~~chat` → Refers to any chat platform (e.g., Slack, Microsoft Teams)
- `~~cloud storage` → Refers to any cloud storage service (e.g., Microsoft 365, Google Drive)
- `~~regulatory docs` → Refers to regulatory documentation sources (e.g., Context7, FDA APIs)

These placeholders make workflows portable across different toolsets while maintaining clear semantic meaning.

---

## Connectors for this plugin

ARIA provides the following connector categories:

| Category | Placeholder | Included servers | Other options |
|----------|-------------|-----------------|---------------|
| Knowledge base | `~~knowledge base` | Notion, Atlassian (Confluence) | Guru, Coda |
| Project tracker | `~~project tracker` | Atlassian (Jira) | Linear, Asana |
| Chat | `~~chat` | Slack | Microsoft Teams |
| Cloud storage | `~~cloud storage` | Microsoft 365 | Google Drive |
| Regulatory docs | `~~regulatory docs` | Context7* | -- |

**Note**: Context7 is a local MCP server (npx-based) and is NOT included in the plugin's `.mcp.json`. Configure Context7 separately in your system-level `.mcp.json` file.

---

## Knowledge base (`~~knowledge base`)

**Purpose**: Access organization-specific regulatory data, past classification decisions, and internal precedents.

**Included servers**:
- **Notion**: Primary knowledge base connector for regulatory databases
- **Atlassian Confluence**: Alternative knowledge base option

**ARIA-specific usage**:
- Query organization regulatory database
- Search historical classification decisions
- Reference internal regulatory standards
- Cross-reference with built-in regulatory knowledge

**Data priority**: Knowledge base sources are **supplementary** (Priority 3). ARIA uses built-in knowledge first and supplements with organization-specific data from `~~knowledge base`.

**Graceful degradation**: If `~~knowledge base` is unavailable, ARIA continues using built-in regulatory knowledge (FDA, EU MDR, MFDS regulations) without interruption.

---

## Project tracker (`~~project tracker`)

**Purpose**: Track regulatory project milestones, submission deadlines, and compliance activities.

**Included servers**:
- **Atlassian Jira**: Primary project tracking connector

**ARIA-specific usage**:
- Track regulatory submission milestones
- Monitor compliance activities
- Link regulatory decisions to project tasks
- Export regulatory plans to project tracking systems

**Data priority**: Project tracker integration is optional. ARIA generates regulatory plans in Markdown format by default, with optional export to `~~project tracker`.

**Graceful degradation**: ARIA regulatory planning works fully without `~~project tracker` integration. Plans are output as structured Markdown.

---

## Chat (`~~chat`)

**Purpose**: Notify stakeholders about regulatory updates and share regulatory intelligence.

**Included servers**:
- **Slack**: Primary chat platform connector

**ARIA-specific usage**:
- Share regulatory briefings with team channels
- Notify stakeholders of classification decisions
- Distribute regulatory pathway recommendations
- Collaborate on multi-regional regulatory strategies

**Data priority**: Chat integration is optional. ARIA generates all outputs in Markdown format first, with optional sharing to `~~chat`.

**Graceful degradation**: All ARIA outputs work independently of `~~chat` availability. Chat integration only adds distribution capabilities.

---

## Cloud storage (`~~cloud storage`)

**Purpose**: Export regulatory reports and documentation to cloud storage platforms.

**Included servers**:
- **Microsoft 365**: Primary cloud storage connector (OneDrive, SharePoint)

**ARIA-specific usage**:
- Export regulatory briefings as Google Docs or Word documents
- Store regulatory reports in organization document repositories
- Integrate with existing document management workflows
- Share regulatory deliverables with external auditors

**Supported formats**:
- Google Docs (regulatory reports)
- Microsoft Word (regulatory briefings)
- PDF (via conversion - future enhancement)

**Data priority**: Cloud storage is optional. ARIA outputs to `.aria/` local Markdown directory by default, with optional export to `~~cloud storage`.

**Graceful degradation**: ARIA works fully without `~~cloud storage`. All features remain functional with local Markdown outputs.

---

## Regulatory docs (`~~regulatory docs`)

**Purpose**: Verify and supplement built-in regulatory knowledge with latest external regulatory documents.

**Included servers**:
- **Context7***: External regulatory document verification

**ARIA-specific usage**:
- Reference latest FDA guidance documents
- Verify EU MDR regulation updates
- Check Korea MFDS regulatory changes
- Supplement built-in knowledge with current regulatory sources

**Data priority**: Regulatory docs sources are **supplementary** (Priority 4). Used only to verify and supplement Notion and built-in knowledge.

**Graceful degradation**: ARIA remains fully functional without `~~regulatory docs`. Built-in regulatory knowledge (FDA, EU MDR, MFDS) is comprehensive and kept up-to-date.

**Special note**: Context7 is a local npx-based MCP server and is NOT included in `aria/.mcp.json`. Configure Context7 separately in your system-level `.mcp.json` file (`~/.claude/settings.json`).

---

## Connector Extension Guide

### Adding New Connectors

To add a new connector to ARIA:

1. **Identify the category**: Determine which category the connector belongs to (Knowledge base, Project tracker, Chat, Cloud storage, Regulatory docs)

2. **Configure HTTP MCP server**: If the connector is an HTTP MCP server, add it to `aria/.mcp.json`:

```json
{
  "mcpServers": {
    "your-connector": {
      "type": "http",
      "url": "https://your-connector.com/mcp"
    }
  }
}
```

3. **Configure local MCP server**: If the connector is a local npx-based server (like Context7), add it to your system-level `.mcp.json` (`~/.claude/settings.json`):

```json
{
  "mcpServers": {
    "your-connector": {
      "command": "npx",
      "args": ["-y", "your-mcp-package"],
      "env": {
        "YOUR_API_KEY": ""
      }
    }
  }
}
```

4. **Update CONNECTORS.md**: Document the new connector in the appropriate category section

5. **Update skills**: Use `~~category` placeholders in skills to reference the new connector capability

### Connector Category Classification

**Knowledge base connectors**:
- Organization-internal data repositories
- Read-focused (regulatory data queries)
- Structured data (databases, wikis)

**Project tracker connectors**:
- Project management platforms
- Read/write (milestone tracking)
- Task and timeline oriented

**Chat connectors**:
- Team communication platforms
- Write-focused (notifications, sharing)
- Real-time collaboration

**Cloud storage connectors**:
- Document storage and sharing platforms
- Write-focused (report export)
- File-based repositories

**Regulatory docs connectors**:
- External reference document sources
- Read-only
- Public or subscription-based information

---

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        ARIA Skills                           │
└─────────────────────────────────────────────────────────────┘
                            │
                            ├─────────────────┬──────────────┐
                            ▼                 ▼              ▼
                ┌──────────────────┐  ┌─────────────┐ ┌────────────────┐
                │ ~~knowledge base │  │   Built-in  │ │ ~~regulatory   │
                │   (Priority 3)   │  │  Knowledge  │ │     docs       │
                │                  │  │ (Priority 1)│ │  (Priority 4)  │
                │ Notion/Confluence│  │  FDA/MDR/   │ │   Context7     │
                │                  │  │    MFDS     │ │                │
                └──────────────────┘  └─────────────┘ └────────────────┘
                            │
                            ▼
                    ┌──────────────┐
                    │  .aria/ Local│
                    │   Markdown   │
                    └──────────────┘
                            │
                            ├─────────────────┬──────────────┬─────────────┐
                            ▼                 ▼              ▼             ▼
                    ┌──────────────┐  ┌─────────────┐ ┌──────────┐ ┌──────────────┐
                    │   Markdown   │  │ ~~cloud     │ │ ~~chat   │ │ ~~project    │
                    │   (default)  │  │  storage    │ │          │ │   tracker    │
                    │              │  │             │ │  Slack   │ │              │
                    │              │  │   MS365     │ │          │ │ Jira/Linear  │
                    └──────────────┘  └─────────────┘ └──────────┘ └──────────────┘
```

---

## Reference

- **README.md**: Complete installation guide and MCP setup instructions
- **aria/.mcp.json**: HTTP MCP server configuration for this plugin
- **System .mcp.json**: `~/.claude/settings.json` for local MCP servers (Context7)
- **aria/skills/connectors/SKILL.md**: Centralized connector integration patterns

---

**Version**: 0.0.4
**Last Updated**: 2026-02-11
**Maintained by**: ARIA Team
