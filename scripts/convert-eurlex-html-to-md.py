#!/usr/bin/env python3
"""EUR-Lex HTML → Article/Annex Markdown chunker.

Splits CELEX XHTML files into individual Article and Annex .md files.
Parsing only — no interpretation, summarization, or normalization.

Usage:
    python3 scripts/convert-eurlex-html-to-md.py
"""

import os
import re
import sys
from datetime import date
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag

# === Configuration ===

SRC_BASE = Path("/Users/hb/Documents/01.Regulatory/03. EU/01.Regulation")

DST_BASE = Path("aria/knowledge/eu/01-regulation")

INSTRUMENTS = {
    "CELEX_32017R0745_EN_TXT.html": {
        "instrument": "MDR",
        "title": "Regulation (EU) 2017/745",
        "source_url": "https://eur-lex.europa.eu/eli/reg/2017/745/oj/eng",
    },
    "CELEX_32017R0746_EN_TXT.html": {
        "instrument": "IVDR",
        "title": "Regulation (EU) 2017/746",
        "source_url": "https://eur-lex.europa.eu/eli/reg/2017/746/oj/eng",
    },
}

DEST_DIRS = {
    "MDR": "mdr-2017-745",
    "IVDR": "ivdr-2017-746",
}

TODAY = date.today().isoformat()


# === HTML → Markdown Conversion ===

def is_enum_table(table):
    """Check if a table is an enumeration table (4%/96% width pattern)."""
    # Only check direct col children (not nested tables' cols)
    cols = table.find_all("col", recursive=False)
    if len(cols) == 2:
        w1 = cols[0].get("width", "")
        w2 = cols[1].get("width", "")
        if "4%" in w1 and "96%" in w2:
            return True
    return False


def convert_node_to_md(node, depth=0):
    """Recursively convert an HTML node to Markdown text."""
    if isinstance(node, NavigableString):
        text = str(node)
        # Collapse whitespace but preserve meaningful spaces
        text = re.sub(r'\s+', ' ', text)
        return text

    if not isinstance(node, Tag):
        return ""

    tag = node.name

    # Skip script/style
    if tag in ("script", "style", "link", "meta"):
        return ""

    # Bold
    if tag == "span" and "oj-bold" in node.get("class", []):
        inner = children_to_md(node, depth)
        return f"**{inner.strip()}**" if inner.strip() else ""

    # Italic
    if tag == "span" and "oj-italic" in node.get("class", []):
        inner = children_to_md(node, depth)
        return f"*{inner.strip()}*" if inner.strip() else ""

    # Footnote tags
    if tag == "span" and "oj-note-tag" in node.get("class", []):
        inner = children_to_md(node, depth)
        return inner

    # Other spans — pass through
    if tag == "span":
        return children_to_md(node, depth)

    # Anchor tags — just take the text
    if tag == "a":
        return children_to_md(node, depth)

    # Paragraph
    if tag == "p":
        classes = node.get("class", [])
        inner = children_to_md(node, depth).strip()
        if not inner:
            return ""

        # Article title
        if "oj-ti-art" in classes:
            return f"## {inner}\n\n"
        # Article subtitle
        if "oj-sti-art" in classes:
            return f"### {inner}\n\n"
        # Section title in annexes
        if "oj-ti-grseq-1" in classes:
            return f"## {inner}\n\n"
        if "oj-ti-grseq-2" in classes:
            return f"### {inner}\n\n"
        if "oj-ti-section" in classes or "oj-ti-section-1" in classes:
            return f"### {inner}\n\n"
        # Chapter title
        if "oj-ti-grseq-3" in classes:
            return f"#### {inner}\n\n"
        # Document title
        if "oj-doc-ti" in classes:
            return f"# {inner}\n\n"

        return f"{inner}\n\n"

    # Enumeration table (4%/96%)
    if tag == "table" and is_enum_table(node):
        # Only process direct tbody > tr rows, not nested table rows
        tbody = node.find("tbody", recursive=False)
        if tbody:
            rows = tbody.find_all("tr", recursive=False)
        else:
            rows = node.find_all("tr", recursive=False)
        result = []
        for row in rows:
            tds = row.find_all("td", recursive=False)
            if len(tds) >= 2:
                marker = children_to_md(tds[0], depth).strip()
                content = children_to_md(tds[1], depth).strip()
                if marker and content:
                    result.append(f"{marker} {content}\n\n")
                elif content:
                    result.append(f"{content}\n\n")
        return "".join(result)

    # Data table (non-enumeration)
    if tag == "table":
        return convert_data_table(node)

    # Div — recurse
    if tag == "div":
        return children_to_md(node, depth)

    # Lists
    if tag == "ul":
        items = []
        for li in node.find_all("li", recursive=False):
            inner = children_to_md(li, depth).strip()
            items.append(f"- {inner}")
        return "\n".join(items) + "\n\n"

    if tag == "ol":
        items = []
        for i, li in enumerate(node.find_all("li", recursive=False), 1):
            inner = children_to_md(li, depth).strip()
            items.append(f"{i}. {inner}")
        return "\n".join(items) + "\n\n"

    if tag == "li":
        return children_to_md(node, depth)

    # BR
    if tag == "br":
        return "\n"

    # HR
    if tag == "hr":
        return "\n---\n\n"

    # tbody, thead, col, colgroup — pass through
    if tag in ("tbody", "thead", "tfoot", "col", "colgroup", "tr", "td", "th"):
        return children_to_md(node, depth)

    # img — skip
    if tag == "img":
        return ""

    # sup/sub
    if tag == "sup":
        return children_to_md(node, depth)
    if tag == "sub":
        return children_to_md(node, depth)

    # Default — recurse
    return children_to_md(node, depth)


def children_to_md(node, depth=0):
    """Convert all children of a node to markdown."""
    parts = []
    for child in node.children:
        parts.append(convert_node_to_md(child, depth))
    return "".join(parts)


def convert_data_table(table):
    """Convert a real data table to markdown table format."""
    rows = table.find_all("tr")
    if not rows:
        return ""

    # Extract all rows
    all_rows = []
    for row in rows:
        cells = row.find_all(["td", "th"])
        row_data = []
        for cell in cells:
            text = children_to_md(cell).strip()
            # Replace pipes and newlines for table cell compatibility
            text = text.replace("|", "\\|").replace("\n", " ")
            row_data.append(text)
        if row_data:
            all_rows.append(row_data)

    if not all_rows:
        return ""

    # Normalize column count
    max_cols = max(len(r) for r in all_rows)
    for r in all_rows:
        while len(r) < max_cols:
            r.append("")

    # Build markdown table
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
    # Remove excessive blank lines (more than 2 consecutive)
    text = re.sub(r'\n{4,}', '\n\n\n', text)
    # Remove trailing whitespace on lines
    text = re.sub(r'[ \t]+\n', '\n', text)
    # Ensure file ends with single newline
    text = text.rstrip() + "\n"
    return text


# === YAML Frontmatter ===

def make_frontmatter(instrument_info, chunk_type, chunk_id, chunk_title, source_file):
    """Generate YAML frontmatter."""
    lines = [
        "---",
        "source:",
        '  family: "REGULATION"',
        f'  instrument: "{instrument_info["instrument"]}"',
        f'  title: "{instrument_info["title"]}"',
        f'  chunk_type: "{chunk_type}"',
        f'  chunk_id: "{chunk_id}"',
    ]
    if chunk_title:
        # Escape quotes in title
        safe_title = chunk_title.replace('"', '\\"')
        lines.append(f'  chunk_title: "{safe_title}"')
    lines.extend([
        f'  source_file: "{source_file}"',
        f'  converted: "{TODAY}"',
        '  method: "beautifulsoup (eli-subdivision parsing)"',
        "---",
        "",
    ])
    return "\n".join(lines)


# === Main Processing ===

def extract_article_title(art_div):
    """Extract article number and subtitle from an article div."""
    ti = art_div.find("p", class_="oj-ti-art")
    sti = art_div.find("p", class_="oj-sti-art")

    art_id = ti.get_text(strip=True) if ti else f"Article {art_div['id'].replace('art_', '')}"
    art_title = sti.get_text(strip=True) if sti else ""

    return art_id, art_title


def extract_annex_title(anx_div):
    """Extract annex number and title."""
    anx_id_raw = anx_div["id"].replace("anx_", "")

    # Map raw IDs to Roman numerals
    ti = anx_div.find("p", class_="oj-ti-grseq-1")
    if ti:
        title_text = ti.get_text(strip=True)
        return f"Annex {anx_id_raw}", title_text

    ti = anx_div.find("p", class_="oj-doc-ti")
    if ti:
        title_text = ti.get_text(strip=True)
        return f"Annex {anx_id_raw}", title_text

    return f"Annex {anx_id_raw}", ""


def process_file(src_path, instrument_info):
    """Process a single EUR-Lex HTML file."""
    src_file = src_path.name
    instrument = instrument_info["instrument"]
    dest_dir = DST_BASE / DEST_DIRS[instrument]
    dest_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n=== Processing {instrument}: {src_file} ===")

    with open(src_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    chunks = []  # For _index.yaml
    stats = {"articles": 0, "annexes": 0, "preamble": 0, "recitals": 0}

    # --- 1. Preamble (citations + introductory text) ---
    preamble_parts = []

    # Main title
    main_title_div = soup.find("div", class_="eli-main-title")
    if main_title_div:
        preamble_parts.append(children_to_md(main_title_div))

    # Citations
    cits = soup.find_all("div", class_="eli-subdivision", id=re.compile(r"^cit_\d+$"))
    if cits:
        for cit in cits:
            preamble_parts.append(children_to_md(cit))

    # "Whereas:" text (between citations and recitals)
    pbl = soup.find("div", class_="eli-subdivision", id="pbl_1")
    if pbl:
        # Get direct paragraph children that aren't in subdivisions
        for child in pbl.children:
            if isinstance(child, Tag) and child.name == "p":
                text = child.get_text(strip=True)
                if text and not text.startswith("(") and "Whereas" not in text:
                    continue
                if text == "Whereas:":
                    preamble_parts.append(f"{text}\n\n")

    if preamble_parts:
        frontmatter = make_frontmatter(
            instrument_info, "PREAMBLE", "Preamble", "Preamble", src_file
        )
        content = clean_markdown(frontmatter + "".join(preamble_parts))
        (dest_dir / "preamble.md").write_text(content, encoding="utf-8")
        chunks.append({"file": "preamble.md", "type": "PREAMBLE"})
        stats["preamble"] = 1
        print(f"  OK: preamble.md")

    # --- 2. Recitals (single file) ---
    rcts = soup.find_all("div", class_="eli-subdivision", id=re.compile(r"^rct_\d+$"))
    if rcts:
        recital_parts = []
        for rct in rcts:
            recital_parts.append(children_to_md(rct))

        frontmatter = make_frontmatter(
            instrument_info, "RECITALS", "Recitals",
            f"Recitals (1-{len(rcts)})", src_file
        )
        content = clean_markdown(frontmatter + "".join(recital_parts))
        (dest_dir / "recitals.md").write_text(content, encoding="utf-8")
        chunks.append({"file": "recitals.md", "type": "RECITALS"})
        stats["recitals"] = len(rcts)
        print(f"  OK: recitals.md ({len(rcts)} recitals)")

    # --- 3. Articles (individual files) ---
    articles = soup.find_all("div", class_="eli-subdivision", id=re.compile(r"^art_\d+$"))
    for art in articles:
        art_num = int(art["id"].replace("art_", ""))
        art_id, art_title = extract_article_title(art)

        filename = f"article-{art_num:03d}.md"
        frontmatter = make_frontmatter(
            instrument_info, "ARTICLE", art_id, art_title, src_file
        )
        body = children_to_md(art)
        content = clean_markdown(frontmatter + body)

        (dest_dir / filename).write_text(content, encoding="utf-8")

        chunk_entry = {"file": filename, "type": "ARTICLE", "id": art_id}
        if art_title:
            chunk_entry["title"] = art_title
        chunks.append(chunk_entry)
        stats["articles"] += 1

    print(f"  OK: {stats['articles']} article files")

    # --- 4. Annexes (individual files) ---
    annexes = soup.find_all("div", class_="eli-container", id=re.compile(r"^anx_"))
    for anx in annexes:
        anx_id_raw = anx["id"].replace("anx_", "")

        # Skip the wrapper "ANNEXES" section
        if anx_id_raw == "ES":
            continue

        anx_id, anx_title = extract_annex_title(anx)
        filename = f"annex-{anx_id_raw}.md"

        frontmatter = make_frontmatter(
            instrument_info, "ANNEX", anx_id, anx_title, src_file
        )
        body = children_to_md(anx)
        content = clean_markdown(frontmatter + body)

        (dest_dir / filename).write_text(content, encoding="utf-8")

        chunk_entry = {"file": filename, "type": "ANNEX", "id": anx_id}
        if anx_title:
            chunk_entry["title"] = anx_title
        chunks.append(chunk_entry)
        stats["annexes"] += 1

    print(f"  OK: {stats['annexes']} annex files")

    # --- 5. Generate _index.yaml ---
    index_lines = [
        f'instrument: {instrument}',
        f'title: "{instrument_info["title"]}"',
        f'source_file: {src_file}',
        f'source_url: "{instrument_info["source_url"]}"',
        f'converted: "{TODAY}"',
        f'total_chunks: {len(chunks)}',
        "chunks:",
    ]
    for c in chunks:
        index_lines.append(f'  - file: {c["file"]}')
        index_lines.append(f'    type: {c["type"]}')
        if "id" in c:
            index_lines.append(f'    id: "{c["id"]}"')
        if "title" in c:
            safe = c["title"].replace('"', '\\"')
            index_lines.append(f'    title: "{safe}"')

    (dest_dir / "_index.yaml").write_text("\n".join(index_lines) + "\n", encoding="utf-8")
    print(f"  OK: _index.yaml ({len(chunks)} chunks)")

    # Summary
    total = stats["preamble"] + (1 if stats["recitals"] else 0) + stats["articles"] + stats["annexes"] + 1  # +1 for _index.yaml
    print(f"\n  Summary for {instrument}:")
    print(f"    Articles: {stats['articles']}")
    print(f"    Annexes:  {stats['annexes']}")
    print(f"    Recitals: {stats['recitals']} (1 file)")
    print(f"    Preamble: {stats['preamble']} file")
    print(f"    _index:   1 file")
    print(f"    Total:    {total} files")

    return total


def main():
    total_files = 0

    print("=== EUR-Lex HTML → Markdown Conversion ===")
    print(f"Source: {SRC_BASE}")
    print(f"Destination: {DST_BASE}")
    print(f"Date: {TODAY}")

    for src_filename, info in INSTRUMENTS.items():
        src_path = SRC_BASE / src_filename
        if not src_path.exists():
            print(f"\nERROR: Source file not found: {src_path}")
            sys.exit(1)

        total_files += process_file(src_path, info)

    print(f"\n=== Grand Total: {total_files} files generated ===")


if __name__ == "__main__":
    main()
