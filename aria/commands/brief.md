---
description: Comprehensive regulatory briefing report generation - Synthesizes all pipeline data into executive-ready documents
argument-hint: "특정 포커스 영역 (선택 사항) [--format markdown|notion|gdocs|pdf] [--lang ko|en]"
---

# /aria:brief - Comprehensive Regulatory Briefing

## Purpose

Generate comprehensive regulatory briefing reports synthesizing all available pipeline data. Integrates determination, classification, pathway, estimates, plan, and comparison into executive-ready documents with recommendations.

## Workflow

### 1. Product Context Loading

- Load active product from `.aria/active_product.json`
- If multiple products exist, prompt for selection
- If no products exist, warn that briefing requires pipeline data

### 2. Pipeline Data Loading

Scan `.aria/products/{product-name}/{date}/` for all available pipeline data:

**Core Pipeline Steps** (5 required for full briefing):
- `determination.summary.md` + `determination.md`
- `classification.summary.md` + `classification.md`
- `pathway.summary.md` + `pathway.md`
- `estimation.summary.md` + `estimation.md`
- `plan.summary.md` + `plan.md`

**Optional Steps**:
- `comparison.summary.md` + `comparison.md`

**Loading Priority**:
- Use `.summary.md` files for executive summary (compressed context)
- Use full `.md` files for detailed analysis sections (complete information)

### 3. Data Completeness Assessment

**Full Pipeline** (all 5 core steps available):
- Generate comprehensive briefing with all sections
- Executive summary + detailed analysis + recommendations + appendices

**Partial Pipeline** (some steps available):
- Generate briefing covering available data
- Indicate missing steps with strong recommendations to complete
- Example: Only determination + classification → focused briefing on device status and class

**Minimal Data** (only 1-2 steps):
- Warn user that comprehensive briefing requires more pipeline data
- Suggest completing `/aria:determine` → `/aria:classify` → `/aria:pathway` → `/aria:estimate` → `/aria:plan` pipeline

### 4. Focus Area Identification (Optional)

User can specify focus area for emphasis in recommendations:
- **Clinical Strategy**: Clinical evidence requirements, trial planning
- **Cost Control**: Budget optimization, cost reduction opportunities
- **Timeline Acceleration**: Parallel submission, expedited pathways
- **Multi-Market Entry**: Comparison analysis, harmonization strategy

Default: Balanced coverage of all aspects

### 5. Two-Phase Output (ER-017 Report Issuance Policy)

**Phase A - Analysis Turn** (Present key findings for user confirmation):

Display concise analysis summary:
- Product overview (name, device status, classification)
- Key findings (regulatory pathways, timeline, budget, risks)
- Top 3 recommendations
- Overall traffic light assessment

Ask user to confirm before generating full report.

**Phase B - Full Report Generation** (After user confirmation):

Generate complete briefing report:
- **Executive Summary** (1-2 pages): Product overview, regulatory status, pathways, timeline/cost, key risks, recommendations
- **Detailed Analysis** (per pipeline step): Full analysis from each `.md` file
- **Recommendations**: Immediate actions (30 days), critical dependencies, resource requirements, risk mitigation
- **Appendices**: Regulatory citations, data sources, escalation items, glossary

**Format Selection** (via `--format` flag):
- `markdown` (default): Markdown report to `.aria/products/`
- `notion`: Notion page via Notion MCP connector (requires notion-mcp configuration)
- `gdocs`: Google Docs via Google Drive MCP connector (requires google-drive-mcp configuration)
- `pdf`: PDF conversion from Markdown (requires pdf-converter tool)

**Google Docs Format Implementation**:

When `--format gdocs` is specified:

1. **MCP Tool Loading**:
   - Use ToolSearch to load Google Drive MCP tools: `ToolSearch("google drive mcp")`
   - Expected tools: `mcp__gdrive__*` (e.g., `mcp__gdrive__create_file`, `mcp__gdrive__upload_content`)

2. **Graceful Degradation** (if Google Drive MCP unavailable):
   - Display limitation notice: "Google Drive MCP가 설정되지 않았습니다. Markdown 형식으로 보고서를 생성합니다."
   - Fallback to Markdown format
   - Save to `.aria/products/{product-name}/{date}/briefing.md`
   - Include limitation notice in Data Source Attribution section

3. **Google Docs Creation** (if MCP available):
   - Generate full briefing report content in Markdown format first
   - Convert Markdown to Google Docs-compatible rich text format
   - Create Google Doc via `mcp__gdrive__create_file` with:
     - Title: "{Product Name} - Regulatory Briefing Report ({date})"
     - Content: Converted briefing content
     - MimeType: `application/vnd.google-apps.document`
   - Display success message with Google Docs link to user
   - Also save Markdown backup to `.aria/products/{product-name}/{date}/briefing.md`

4. **Output Files**:
   - Google Docs document (via MCP, link provided to user)
   - `.aria/products/{product-name}/{date}/briefing.md` (Markdown backup)
   - `.aria/products/{product-name}/{date}/briefing.summary.md` (summary)

5. **Error Handling**:
   - If MCP tools not found: Fallback to Markdown with limitation notice
   - If Google Docs creation fails: Display error, save Markdown version
   - Specific error: "Google Drive에 연결할 수 없습니다. Markdown 형식으로 보고서를 생성합니다."

**PDF Format Implementation**:

When `--format pdf` is specified:

1. **Tool Availability Check** (in priority order):
   - Check for `pandoc` (recommended): `which pandoc`
   - Check for `wkhtmltopdf`: `which wkhtmltopdf`
   - Check for Python with `markdown` + `weasyprint`: `python3 -c "import markdown, weasyprint"`

2. **Markdown Generation**:
   - Generate full briefing report in Markdown format first
   - Save to `.aria/products/{product-name}/{date}/briefing.md`

3. **PDF Conversion** (based on available tool):

   **Option A - Pandoc (recommended)**:
   ```bash
   pandoc briefing.md -o briefing.pdf \
     --pdf-engine=xelatex \
     --variable=geometry:margin=1in \
     --variable=fontsize:11pt \
     --toc \
     --highlight-style=tango
   ```

   **Option B - wkhtmltopdf**:
   ```bash
   # First convert MD to HTML with basic styling
   python3 -c "import markdown; open('briefing.html', 'w').write(markdown.markdown(open('briefing.md').read()))"

   # Then convert HTML to PDF
   wkhtmltopdf --page-size A4 --margin-top 20mm --margin-bottom 20mm briefing.html briefing.pdf
   ```

   **Option C - Python weasyprint**:
   ```bash
   python3 -c "
   import markdown
   from weasyprint import HTML

   # Convert MD to HTML
   md_content = open('briefing.md', 'r').read()
   html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])

   # Add basic styling
   styled_html = f'''
   <html>
   <head>
       <style>
           body {{ font-family: Arial, sans-serif; margin: 2cm; }}
           h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; }}
           h2 {{ color: #34495e; margin-top: 1.5em; }}
           table {{ border-collapse: collapse; width: 100%; }}
           th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
           th {{ background-color: #f2f2f2; }}
           code {{ background-color: #f5f5f5; padding: 2px 4px; border-radius: 3px; }}
       </style>
   </head>
   <body>{html_content}</body>
   </html>
   '''

   # Generate PDF
   HTML(string=styled_html).write_pdf('briefing.pdf')
   "
   ```

4. **Tool Installation Guidance** (if no tool available):
   - Display error message with installation instructions
   - Recommend installing pandoc via Homebrew: `brew install pandoc`
   - Fallback to Markdown format with warning

5. **Output Files**:
   - `.aria/products/{product-name}/{date}/briefing.pdf` (PDF output)
   - `.aria/products/{product-name}/{date}/briefing.md` (Markdown source)
   - `.aria/products/{product-name}/{date}/briefing.summary.md` (summary)

6. **Error Handling**:
   - If PDF conversion fails, report error but keep Markdown file
   - Provide specific error message about missing dependencies
   - Suggest alternative: "PDF conversion requires pandoc. Install with: brew install pandoc"

### 6. Summary Generation

**Compressed summary** (`briefing.summary.md`):
- Product, date, pipeline steps covered, traffic light, critical path, budget, key risks, top recommendations

### 7. Next Steps

- **Primary**: Review report with stakeholders (executive team, regulatory experts)
- **Alternative**: Execute immediate actions from recommendations
- **Optional**: Complete missing pipeline steps if partial data

## Flags

- `--format markdown|notion|gdocs|pdf`: Output format (default: `markdown`)
- `--lang en|ko`: Output language (default: `ko`)

## Output Location

- `.aria/products/{product-name}/{date}/briefing.md` (Markdown format or PDF source)
- `.aria/products/{product-name}/{date}/briefing.pdf` (when `--format pdf`)
- `.aria/products/{product-name}/{date}/briefing.summary.md` (always generated)
- Notion page or Google Docs if alternative format selected

## Data Sources

All pipeline data from `.aria/` directory is the primary source. Built-in knowledge supplements briefing structure and executive summary framework. External data connectors (Notion, Context7) are reflected via pipeline data already generated.

## Example

```
/aria:brief
```
> System loads all available pipeline data
> System presents analysis summary (Phase A)
> User confirms
> System generates comprehensive briefing report (Phase B, Markdown format)

```
/aria:brief --format gdocs --lang en
```
> English output, Google Docs format
> System loads all pipeline data
> System presents analysis summary
> User confirms
> System generates Google Docs briefing via Google Drive MCP

```
/aria:brief Clinical Strategy
```
> Focus area: Clinical Strategy
> Emphasizes clinical evidence requirements and trial planning in recommendations

```
/aria:brief --format pdf
```
> System loads all pipeline data
> System presents analysis summary (Phase A)
> User confirms
> System generates Markdown briefing
> System converts to PDF using available tool (pandoc/wkhtmltopdf/weasyprint)
> Output: briefing.pdf + briefing.md + briefing.summary.md

## Report Issuance Policy (ER-017)

**Critical Rule**: Full formatted report is NOT generated in the same turn as initial analysis.

**Two-Phase Approach**:
1. **Analysis Phase**: Output only key findings, traffic light, items for confirmation
2. **Report Phase**: After user reviews and confirms, generate full formatted report

**User confirmation required before full report generation.**

## Disclaimer

**Important Notice**

This briefing is an AI-based regulatory intelligence synthesis, not official regulatory advice.

- **No legal effect**: Briefing is for reference only and has no legal binding force
- **Expert review required**: All findings and recommendations require validation by qualified regulatory affairs professionals
- **Regulatory authority confirmation**: Final regulatory decisions must follow official guidance from FDA, Notified Bodies, MFDS, etc.
- **Limitation of liability**: Users are responsible for regulatory non-compliance resulting from use of this tool

Knowledge Base Date: 2026-01

---

This is reference information for professional review, not regulatory advice.
