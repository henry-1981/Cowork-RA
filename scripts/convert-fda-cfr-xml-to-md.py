#!/usr/bin/env python3
"""21 CFR Subchapter H XML → Part-level Markdown chunker.

Splits eCFR XML into individual Part .md files (1 file per Part).
Parsing only — no interpretation, summarization, or normalization.

Usage:
    python3 scripts/convert-fda-cfr-xml-to-md.py
"""

import re
import sys
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path

# === Configuration ===

SRC_PATH = Path("/Users/hb/Documents/01.Regulatory/02. FDA/01.Statue/CFR-2025-title21-vol8-chapI-subchapH.xml")
DST_BASE = Path("aria/knowledge/fda/02-regulation/21cfr-subchapter-h")
TODAY = date.today().isoformat()
SOURCE_FILE = SRC_PATH.name


# === XML → Markdown Conversion ===

def get_text(elem):
    """Extract all text from element, including tail text of children."""
    if elem is None:
        return ""
    return "".join(elem.itertext()).strip()


def convert_element_to_md(elem, depth=0):
    """Recursively convert an XML element to Markdown."""
    if elem is None:
        return ""

    tag = elem.tag
    result = []

    # PART heading
    if tag == "HD":
        source = elem.get("SOURCE", "")
        text = get_text(elem).strip()
        if source == "HED":
            # Top-level heading within current context
            if depth == 0:
                result.append(f"# {text}\n\n")
            elif depth == 1:
                result.append(f"## {text}\n\n")
            else:
                result.append(f"### {text}\n\n")
        elif source == "HD1":
            result.append(f"### {text}\n\n")
        elif source == "HD2":
            result.append(f"#### {text}\n\n")
        elif source == "HD3":
            result.append(f"##### {text}\n\n")
        else:
            result.append(f"### {text}\n\n")
        return "".join(result)

    # SECTION: §XXX.XX Title
    if tag == "SECTION":
        sectno = elem.find("SECTNO")
        subject = elem.find("SUBJECT")
        sectno_text = get_text(sectno) if sectno is not None else ""
        subject_text = get_text(subject) if subject is not None else ""
        if sectno_text:
            result.append(f"### {sectno_text} {subject_text}\n\n")
        for child in elem:
            if child.tag not in ("SECTNO", "SUBJECT"):
                result.append(convert_element_to_md(child, depth + 1))
        return "".join(result)

    # RESERVED subpart/section
    if tag == "RESERVED":
        text = get_text(elem).strip()
        if text:
            result.append(f"*{text}*\n\n")
        return "".join(result)

    # Paragraph
    if tag == "P":
        text = convert_inline_text(elem).strip()
        if text:
            result.append(f"{text}\n\n")
        return "".join(result)

    # FP (flush paragraph)
    if tag == "FP":
        text = convert_inline_text(elem).strip()
        if text:
            result.append(f"{text}\n\n")
        return "".join(result)

    # EXTRACT (block quote)
    if tag == "EXTRACT":
        for child in elem:
            md = convert_element_to_md(child, depth + 1)
            if md.strip():
                for line in md.strip().split("\n"):
                    result.append(f"> {line}\n")
                result.append("\n")
        return "".join(result)

    # Citation
    if tag == "CITA":
        text = get_text(elem).strip()
        if text:
            result.append(f"> Citation: {text}\n\n")
        return "".join(result)

    # Authority
    if tag == "AUTH":
        for child in elem:
            result.append(convert_element_to_md(child, depth))
        return "".join(result)

    # SOURCE note
    if tag == "SOURCE":
        for child in elem:
            result.append(convert_element_to_md(child, depth))
        return "".join(result)

    # EFFDNOT (effective date note)
    if tag == "EFFDNOT":
        for child in elem:
            result.append(convert_element_to_md(child, depth))
        return "".join(result)

    # SUBPART container
    if tag == "SUBPART":
        for child in elem:
            result.append(convert_element_to_md(child, depth + 1))
        return "".join(result)

    # GPOTABLE → markdown table
    if tag == "GPOTABLE":
        return convert_gpotable(elem)

    # CONTENTS (table of contents) — skip to avoid duplication
    if tag == "CONTENTS":
        return ""

    # EAR (Part number label) — skip, redundant with HD
    if tag == "EAR":
        return ""

    # Page marker — skip
    if tag == "PRTPAGE":
        return ""

    # SECHD (section heading in contents) — skip
    if tag == "SECHD":
        return ""

    # SECTNO/SUBJECT in CONTENTS — skip
    if tag in ("SECTNO", "SUBJECT") and depth > 0:
        return ""

    # NOTE
    if tag == "NOTE":
        for child in elem:
            result.append(convert_element_to_md(child, depth))
        return "".join(result)

    # Default — recurse into children
    for child in elem:
        result.append(convert_element_to_md(child, depth))

    return "".join(result)


def convert_inline_text(elem):
    """Convert element text including inline markup (E tags, etc.)."""
    parts = []
    if elem.text:
        parts.append(elem.text)
    for child in elem:
        if child.tag == "E":
            # Emphasis types: T="03" = italic, T="01" = bold, T="04" = bold
            etype = child.get("T", "")
            inner = get_text(child)
            if etype == "03":
                parts.append(f"*{inner}*")
            elif etype in ("01", "04"):
                parts.append(f"**{inner}**")
            else:
                parts.append(inner)
        elif child.tag == "SU":
            # Superscript (footnote ref)
            parts.append(get_text(child))
        elif child.tag == "FTNT":
            # Footnote
            parts.append(f" [{get_text(child).strip()}]")
        elif child.tag == "PRTPAGE":
            pass  # Skip page markers
        elif child.tag == "AC":
            # Accounting format
            parts.append(get_text(child))
        else:
            parts.append(convert_inline_text(child))
        if child.tail:
            parts.append(child.tail)
    return "".join(parts)


def convert_gpotable(table_elem):
    """Convert GPOTABLE XML to markdown table."""
    rows_elems = table_elem.findall(".//ROW")
    if not rows_elems:
        return ""

    all_rows = []
    for row in rows_elems:
        cells = row.findall("ENT")
        row_data = [convert_inline_text(cell).strip().replace("|", "\\|").replace("\n", " ")
                     for cell in cells]
        if row_data:
            all_rows.append(row_data)

    if not all_rows:
        return ""

    # Check for BOXHD (header)
    boxhd = table_elem.find("BOXHD")
    header_row = None
    if boxhd is not None:
        hed_elems = boxhd.findall("CHED")
        if hed_elems:
            header_row = [get_text(h).strip().replace("|", "\\|") for h in hed_elems]

    max_cols = max(len(r) for r in all_rows)
    if header_row:
        max_cols = max(max_cols, len(header_row))

    # Pad rows
    for r in all_rows:
        while len(r) < max_cols:
            r.append("")
    if header_row:
        while len(header_row) < max_cols:
            header_row.append("")

    result = []
    if header_row:
        result.append("| " + " | ".join(header_row) + " |")
        result.append("| " + " | ".join(["---"] * max_cols) + " |")
        for row in all_rows:
            result.append("| " + " | ".join(row) + " |")
    else:
        # Use first row as header
        result.append("| " + " | ".join(all_rows[0]) + " |")
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

def make_frontmatter(part_num, part_title, section_count):
    """Generate YAML frontmatter for a Part."""
    safe_title = part_title.replace('"', '\\"')
    lines = [
        "---",
        "source:",
        '  family: "REGULATION"',
        '  instrument: "21 CFR"',
        '  title: "Title 21 — Food and Drugs, Chapter I, Subchapter H — Medical Devices"',
        '  chunk_type: "PART"',
        f'  chunk_id: "Part {part_num}"',
        f'  chunk_title: "{safe_title}"',
        f'  sections: {section_count}',
        f'  source_file: "{SOURCE_FILE}"',
        f'  converted: "{TODAY}"',
        '  method: "xml.etree.ElementTree (PART-level chunking)"',
        "---",
        "",
    ]
    return "\n".join(lines)


# === Main Processing ===

def extract_part_info(part_elem):
    """Extract Part number and title from a PART element."""
    ear = part_elem.find("EAR")
    hd = part_elem.find("HD")

    if ear is not None:
        ear_text = get_text(ear)
        # "Pt. 800" → "800"
        m = re.search(r'Pt\.\s*(\d+)', ear_text)
        part_num = m.group(1) if m else ear_text
    else:
        part_num = None

    if hd is not None:
        hd_text = get_text(hd)
        # "PART 800—GENERAL" → "GENERAL"
        m = re.match(r'PART\s+\d+\s*[—–-]\s*(.*)', hd_text)
        part_title = m.group(1) if m else hd_text
        full_title = hd_text
    else:
        part_title = ""
        full_title = ""

    return part_num, part_title, full_title


def process_part(part_elem, dest_dir, part_num_override=None, filename_suffix=""):
    """Process a PART element into a markdown file."""
    part_num, part_title, full_title = extract_part_info(part_elem)

    if part_num is None and part_num_override is None:
        # Part 820 QMSR variant (no EAR element)
        return None

    actual_num = part_num_override or part_num
    section_count = len(part_elem.findall(".//SECTION"))

    # Convert to markdown
    body = convert_element_to_md(part_elem, depth=0)
    frontmatter = make_frontmatter(actual_num, part_title, section_count)
    content = clean_markdown(frontmatter + body)

    filename = f"part-{actual_num}{filename_suffix}.md"
    filepath = dest_dir / filename
    filepath.write_text(content, encoding="utf-8")

    return {
        "file": filename,
        "type": "PART",
        "id": f"Part {actual_num}",
        "title": part_title,
        "sections": section_count,
    }


def generate_index(chunks, dest_dir):
    """Generate _index.yaml."""
    total_sections = sum(c.get("sections", 0) for c in chunks)
    lines = [
        'instrument: "21 CFR"',
        'title: "Title 21 — Food and Drugs, Chapter I, Subchapter H — Medical Devices"',
        f'source_file: "{SOURCE_FILE}"',
        'source_url: "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-H"',
        f'converted: "{TODAY}"',
        f'total_chunks: {len(chunks)}',
        f'total_sections: {total_sections}',
        "chunks:",
    ]
    for c in chunks:
        lines.append(f'  - file: {c["file"]}')
        lines.append(f'    type: {c["type"]}')
        lines.append(f'    id: "{c["id"]}"')
        if c.get("title"):
            safe = c["title"].replace('"', '\\"')
            lines.append(f'    title: "{safe}"')
        if c.get("sections"):
            lines.append(f'    sections: {c["sections"]}')

    (dest_dir / "_index.yaml").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    print("=== FDA Regulation (21 CFR) XML → Markdown Conversion ===")
    print(f"Source: {SRC_PATH}")
    print(f"Destination: {DST_BASE}")
    print(f"Date: {TODAY}")

    if not SRC_PATH.exists():
        print(f"\nERROR: Source file not found: {SRC_PATH}")
        sys.exit(1)

    DST_BASE.mkdir(parents=True, exist_ok=True)

    # Parse XML
    tree = ET.parse(SRC_PATH)
    root = tree.getroot()

    # Find all PART elements
    parts = root.findall(".//PART")
    print(f"\nFound {len(parts)} PART elements")

    chunks = []
    seen_part_nums = set()

    for part_elem in parts:
        part_num, part_title, full_title = extract_part_info(part_elem)

        # Handle Part 820 duplicate (current QSR + new QMSR eff.2-2-26)
        if part_num and part_num in seen_part_nums:
            # Second occurrence — append "-qmsr" suffix
            suffix = "-qmsr"
            print(f"  NOTE: Duplicate Part {part_num} detected — saving as part-{part_num}{suffix}.md")
            result = process_part(part_elem, DST_BASE, part_num_override=part_num, filename_suffix=suffix)
        elif part_num is None:
            # No EAR → Part 820 QMSR variant
            # Extract number from HD
            hd = part_elem.find("HD")
            if hd is not None:
                m = re.search(r'PART\s+(\d+)', get_text(hd))
                if m:
                    pnum = m.group(1)
                    if pnum in seen_part_nums:
                        suffix = "-qmsr"
                        print(f"  NOTE: Part {pnum} QMSR variant — saving as part-{pnum}{suffix}.md")
                        result = process_part(part_elem, DST_BASE, part_num_override=pnum, filename_suffix=suffix)
                    else:
                        seen_part_nums.add(pnum)
                        result = process_part(part_elem, DST_BASE, part_num_override=pnum)
                else:
                    continue
            else:
                continue
        else:
            seen_part_nums.add(part_num)
            result = process_part(part_elem, DST_BASE)

        if result:
            chunks.append(result)
            print(f"  OK: {result['file']} — {result['title'][:50]} ({result['sections']} sections)")

    # Generate index
    generate_index(chunks, DST_BASE)
    print(f"\n  OK: _index.yaml ({len(chunks)} chunks)")

    total_sections = sum(c.get("sections", 0) for c in chunks)
    print(f"\n=== Summary ===")
    print(f"  Parts: {len(chunks)}")
    print(f"  Total sections: {total_sections}")
    print(f"  Total files: {len(chunks) + 1}")


if __name__ == "__main__":
    main()
