#!/usr/bin/env python3
"""GPO U.S. Code HTML → Section Markdown chunker.

Splits FD&C Act (21 U.S.C. Chapter 9, Subchapter V) into individual Section .md files.
Parsing only — no interpretation, summarization, or normalization.

Usage:
    python3 scripts/convert-fda-uscode-to-md.py
"""

import os
import re
import sys
from datetime import date
from pathlib import Path

from bs4 import BeautifulSoup, Comment, NavigableString, Tag

# === Configuration ===

SRC_PATH = Path("/Users/hb/Documents/01.Regulatory/02. FDA/02.Regulation/USCODE-2024-title21-chap9-subchapV.htm")
DST_BASE = Path("aria/knowledge/fda/01-statute/fdc-act-title21-chap9-subchapV")
TODAY = date.today().isoformat()
SOURCE_FILE = SRC_PATH.name

# Regex to identify section-level documentid comments (numeric section IDs only)
SECTION_DOCID_RE = re.compile(r"documentid:21_(\d+[a-z]*(?:[-–]\d+)?)\s")


# === HTML → Markdown Conversion ===

def convert_node_to_md(node):
    """Recursively convert an HTML node to Markdown text."""
    if isinstance(node, Comment):
        return ""
    if isinstance(node, NavigableString):
        text = str(node)
        text = re.sub(r'\s+', ' ', text)
        return text
    if not isinstance(node, Tag):
        return ""

    tag = node.name
    if tag in ("script", "style", "link", "meta"):
        return ""

    # Section head
    if tag == "h3" and "section-head" in node.get("class", []):
        inner = children_to_md(node).strip()
        return f"# {inner}\n\n"

    # Part head
    if tag == "h3" and "part-head" in node.get("class", []):
        inner = children_to_md(node).strip()
        return f"# {inner}\n\n"

    # Subchapter head
    if tag == "h3" and "subchapter-head" in node.get("class", []):
        inner = children_to_md(node).strip()
        return f"# {inner}\n\n"

    # Subsection head
    if tag == "h4":
        classes = node.get("class", [])
        inner = children_to_md(node).strip()
        if "subsection-head" in classes:
            return f"## {inner}\n\n"
        if "paragraph-head" in classes:
            return f"### {inner}\n\n"
        if "note-head" in classes:
            return f"### {inner}\n\n"
        return f"## {inner}\n\n"

    # Paragraph variants
    if tag == "p":
        classes = node.get("class", [])
        inner = children_to_md(node).strip()
        if not inner:
            return ""

        # Source credit
        if "source-credit" in classes:
            return f"> Source: {inner}\n\n"

        # Note body
        if "note-body" in classes:
            return f"  {inner}\n\n"

        # Statutory body with indentation levels
        indent = ""
        for cls in classes:
            if cls.startswith("statutory-body-") and cls.endswith("em"):
                try:
                    level = int(cls.replace("statutory-body-", "").replace("em", ""))
                    indent = "  " * level
                except ValueError:
                    pass
            elif cls == "statutory-body-block":
                pass  # No indent, just a block continuation

        # Footnote
        if "footnote" in classes:
            return f"  {inner}\n\n"

        return f"{indent}{inner}\n\n"

    # cap-smallcap → pass through text
    if tag == "cap-smallcap":
        return children_to_md(node)

    # Bold
    if tag == "b" or tag == "strong":
        inner = children_to_md(node).strip()
        return f"**{inner}**" if inner else ""

    # Italic
    if tag == "i" or tag == "em":
        inner = children_to_md(node).strip()
        return f"*{inner}*" if inner else ""

    # Sup/sub — just pass text
    if tag in ("sup", "sub"):
        return children_to_md(node)

    # Anchor — just text
    if tag == "a":
        return children_to_md(node)

    # BR
    if tag == "br":
        return "\n"

    # Span — pass through
    if tag == "span":
        return children_to_md(node)

    # Table
    if tag == "table":
        return convert_table(node)

    # Default — recurse
    return children_to_md(node)


def children_to_md(node):
    """Convert all children of a node to markdown."""
    parts = []
    for child in node.children:
        parts.append(convert_node_to_md(child))
    return "".join(parts)


def convert_table(table):
    """Convert an HTML table to markdown table."""
    rows = table.find_all("tr")
    if not rows:
        return ""

    all_rows = []
    for row in rows:
        cells = row.find_all(["td", "th"])
        row_data = []
        for cell in cells:
            text = children_to_md(cell).strip()
            text = text.replace("|", "\\|").replace("\n", " ")
            row_data.append(text)
        if row_data:
            all_rows.append(row_data)

    if not all_rows:
        return ""

    max_cols = max(len(r) for r in all_rows)
    for r in all_rows:
        while len(r) < max_cols:
            r.append("")

    result = []
    header = all_rows[0]
    result.append("| " + " | ".join(header) + " |")
    result.append("| " + " | ".join(["---"] * max_cols) + " |")
    for row in all_rows[1:]:
        result.append("| " + " | ".join(row) + " |")
    result.append("")
    return "\n".join(result) + "\n"


def clean_markdown(text):
    """Clean up generated markdown."""
    text = re.sub(r'\n{4,}', '\n\n\n', text)
    text = re.sub(r'[ \t]+\n', '\n', text)
    text = text.rstrip() + "\n"
    return text


# === YAML Frontmatter ===

def make_frontmatter(chunk_id, chunk_title):
    """Generate YAML frontmatter for a section."""
    lines = [
        "---",
        "source:",
        '  family: "STATUTE"',
        '  instrument: "FD&C Act"',
        '  title: "Federal Food, Drug, and Cosmetic Act"',
        '  chunk_type: "SECTION"',
        f'  chunk_id: "21 U.S.C. § {chunk_id}"',
    ]
    if chunk_title:
        safe_title = chunk_title.replace('"', '\\"')
        lines.append(f'  chunk_title: "{safe_title}"')
    lines.extend([
        f'  source_file: "{SOURCE_FILE}"',
        f'  converted: "{TODAY}"',
        '  method: "beautifulsoup (documentid comment parsing)"',
        "---",
        "",
    ])
    return "\n".join(lines)


# === Main Processing ===

def extract_sections(html_text):
    """Split HTML by section documentid comments, return list of (section_id, html_chunk)."""
    # Find all section-level documentid comment positions
    pattern = re.compile(
        r'(<!-- documentid:21_(\d+[a-z]*(?:[-–]\d+)?)\s.*?-->)',
        re.DOTALL
    )
    matches = list(pattern.finditer(html_text))

    sections = []
    for i, m in enumerate(matches):
        sec_id = m.group(2)
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(html_text)
        chunk_html = html_text[start:end]
        sections.append((sec_id, chunk_html))

    return sections


def process_section(sec_id, chunk_html, dest_dir):
    """Process one section HTML chunk into a markdown file."""
    soup = BeautifulSoup(chunk_html, "html.parser")

    # Extract section title from h3.section-head
    h3 = soup.find("h3", class_="section-head")
    if not h3:
        return None  # Structural entry (part/subchapter), skip

    title_text = h3.get_text(strip=True)
    # Parse section title: "§351. Adulterated drugs and devices"
    title_match = re.match(r'§\d+[a-z]*(?:[-–]\d+)?\.\s*(.*)', title_text)
    chunk_title = title_match.group(1) if title_match else title_text

    # Convert entire chunk to markdown
    body = children_to_md(soup)
    frontmatter = make_frontmatter(sec_id, chunk_title)
    content = clean_markdown(frontmatter + body)

    filename = f"section-{sec_id}.md"
    filepath = dest_dir / filename
    filepath.write_text(content, encoding="utf-8")

    return {
        "file": filename,
        "type": "SECTION",
        "id": f"21 U.S.C. § {sec_id}",
        "title": chunk_title,
    }


def generate_index(chunks, dest_dir):
    """Generate _index.yaml."""
    lines = [
        'instrument: "FD&C Act"',
        'title: "Federal Food, Drug, and Cosmetic Act — Subchapter V (Drugs and Devices)"',
        f'source_file: "{SOURCE_FILE}"',
        'source_url: "https://uscode.house.gov/view.xhtml?path=/prelim@title21/chapter9/subchapter5&edition=prelim"',
        f'converted: "{TODAY}"',
        f'total_chunks: {len(chunks)}',
        "chunks:",
    ]
    for c in chunks:
        lines.append(f'  - file: {c["file"]}')
        lines.append(f'    type: {c["type"]}')
        lines.append(f'    id: "{c["id"]}"')
        if c.get("title"):
            safe = c["title"].replace('"', '\\"')
            lines.append(f'    title: "{safe}"')

    (dest_dir / "_index.yaml").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    print("=== FDA Statute (U.S. Code) HTML → Markdown Conversion ===")
    print(f"Source: {SRC_PATH}")
    print(f"Destination: {DST_BASE}")
    print(f"Date: {TODAY}")

    if not SRC_PATH.exists():
        print(f"\nERROR: Source file not found: {SRC_PATH}")
        sys.exit(1)

    DST_BASE.mkdir(parents=True, exist_ok=True)

    # Read HTML
    html_text = SRC_PATH.read_text(encoding="utf-8")

    # Split into sections
    raw_sections = extract_sections(html_text)
    print(f"\nFound {len(raw_sections)} documentid entries")

    # Process each section
    chunks = []
    skipped = 0
    for sec_id, chunk_html in raw_sections:
        result = process_section(sec_id, chunk_html, DST_BASE)
        if result:
            chunks.append(result)
            print(f"  OK: section-{sec_id}.md — {result['title'][:60]}")
        else:
            skipped += 1

    # Generate index
    generate_index(chunks, DST_BASE)
    print(f"\n  OK: _index.yaml ({len(chunks)} chunks)")

    print(f"\n=== Summary ===")
    print(f"  Sections: {len(chunks)}")
    print(f"  Skipped (structural): {skipped}")
    print(f"  Total files: {len(chunks) + 1}")


if __name__ == "__main__":
    main()
