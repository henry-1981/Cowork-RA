#!/usr/bin/env python3
"""
pymupdf 기반 Knowledge DB 재추출.
- 테이블 감지 → markdown 테이블로 변환
- OCR 폴백 → pymupdf의 내장 OCR (tesseract 활용)
- 기존 frontmatter 보존, method 필드만 업데이트
"""
import sys, yaml, argparse
from pathlib import Path

try:
    import pymupdf
except ImportError:
    print("ERROR: pymupdf not installed. Run: pip install pymupdf")
    sys.exit(1)


def extract_frontmatter(text):
    """Parse and return (frontmatter_dict, raw_frontmatter_str, body)."""
    if not text.startswith("---"):
        return {}, "", text
    end = text.find("---", 3)
    if end == -1:
        return {}, "", text
    raw = text[3:end]
    try:
        meta = yaml.safe_load(raw) or {}
    except Exception:
        meta = {}
    return meta, raw, text[end + 3 :].strip()


def table_to_markdown(table):
    """Convert pymupdf Table object to markdown table string."""
    rows = table.extract()
    if not rows:
        return ""
    # Clean cells
    clean_rows = []
    for row in rows:
        clean_rows.append(
            [
                (cell or "").replace("\n", " ").replace("|", "\\|").strip()
                for cell in row
            ]
        )
    if not clean_rows:
        return ""
    # Build markdown table
    lines = []
    lines.append("| " + " | ".join(clean_rows[0]) + " |")
    lines.append("| " + " | ".join(["---"] * len(clean_rows[0])) + " |")
    for row in clean_rows[1:]:
        # Pad row if shorter than header
        while len(row) < len(clean_rows[0]):
            row.append("")
        lines.append("| " + " | ".join(row[: len(clean_rows[0])]) + " |")
    return "\n".join(lines)


def extract_page_with_tables(page):
    """Extract page content, replacing table regions with markdown tables."""
    tables = page.find_tables()
    if not tables.tables:
        # No tables — use layout-preserving text extraction
        return page.get_text("text")

    # Get full page text blocks with positions
    blocks = page.get_text("dict")["blocks"]
    table_rects = [t.bbox for t in tables.tables]

    # Build output: text blocks outside tables + markdown tables
    used_table_indices = set()

    # Sort blocks by vertical position
    text_blocks = []
    for b in blocks:
        if b["type"] == 0:  # text block
            for line in b.get("lines", []):
                for span in line.get("spans", []):
                    text_blocks.append(
                        {
                            "y": line["bbox"][1],
                            "x": line["bbox"][0],
                            "text": span["text"],
                            "bbox": line["bbox"],
                        }
                    )
    text_blocks.sort(key=lambda b: (b["y"], b["x"]))

    output_parts = []

    # Check each text block against table regions
    for tb in text_blocks:
        in_table = False
        for ti, tr in enumerate(table_rects):
            if (
                tb["bbox"][1] >= tr[1] - 2
                and tb["bbox"][3] <= tr[3] + 2
                and tb["bbox"][0] >= tr[0] - 2
                and tb["bbox"][2] <= tr[2] + 2
            ):
                in_table = True
                if ti not in used_table_indices:
                    used_table_indices.add(ti)
                    md_table = table_to_markdown(tables.tables[ti])
                    if md_table:
                        output_parts.append("\n" + md_table + "\n")
                break
        if not in_table:
            output_parts.append(tb["text"])

    # Fallback: add any tables not yet inserted
    for ti, t in enumerate(tables.tables):
        if ti not in used_table_indices:
            md_table = table_to_markdown(t)
            if md_table:
                output_parts.append("\n" + md_table + "\n")

    return "\n".join(output_parts)


def extract_page_ocr(page):
    """Extract page via OCR for image-based PDFs."""
    # Try text extraction first
    text = page.get_text("text")
    if len(text.strip()) > 50:
        return text
    # Fall back to OCR via pymupdf
    try:
        tp = page.get_textpage_ocr(language="eng", dpi=300)
        return page.get_text("text", textpage=tp)
    except Exception:
        # pymupdf OCR not available, fall back to raw text
        return text


def reextract_file(md_path, source_base, mode="auto", dry_run=False):
    """Re-extract a single MD file from its source PDF.

    Args:
        md_path: Path to existing MD file
        source_base: Base directory for source PDFs
        mode: "table" (layout+table), "ocr" (OCR), "auto" (detect)
        dry_run: If True, only report what would be done

    Returns: (success, info_message, new_body)
    """
    text = md_path.read_text(encoding="utf-8", errors="replace")
    meta, _, _ = extract_frontmatter(text)
    source = meta.get("source", {})
    src_path_rel = source.get("path", "")
    old_method = source.get("method", "unknown")

    if not src_path_rel:
        return None, "no source path in frontmatter", None

    # Find source PDF
    src_pdf = source_base / src_path_rel
    if not src_pdf.exists():
        return None, f"source PDF not found: {src_pdf}", None

    if dry_run:
        return True, f"would re-extract: {mode}", None

    # Open PDF
    doc = pymupdf.open(str(src_pdf))

    # Detect mode if auto
    if mode == "auto":
        # Check first page for text
        first_text = doc[0].get_text("text").strip()
        if len(first_text) < 50:
            mode = "ocr"
        else:
            mode = "table"

    # Extract all pages
    new_parts = []
    for page in doc:
        if mode == "ocr":
            new_parts.append(extract_page_ocr(page))
        else:
            new_parts.append(extract_page_with_tables(page))
    doc.close()

    new_body = "\n\n".join(new_parts)

    # Update method in frontmatter
    new_method = f"pymupdf-{mode}"
    source["method"] = new_method
    meta["source"] = source

    # Rebuild file
    new_fm = yaml.dump(meta, default_flow_style=False, allow_unicode=True)
    new_content = f"---\n{new_fm}---\n\n{new_body}\n"

    # Write
    md_path.write_text(new_content, encoding="utf-8")

    return True, f"{old_method} → {new_method}", new_body


def main():
    parser = argparse.ArgumentParser(
        description="Re-extract Knowledge DB files with pymupdf"
    )
    parser.add_argument("--files", nargs="+", help="Specific MD files to re-extract")
    parser.add_argument("--csv", help="CSV from audit with score filter")
    parser.add_argument(
        "--score-below",
        type=int,
        default=70,
        help="Re-extract files scoring below this",
    )
    parser.add_argument(
        "--mode", choices=["auto", "table", "ocr"], default="auto"
    )
    parser.add_argument(
        "--source-base", required=True, help="Base directory for source PDFs"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Report only, don't modify files"
    )
    args = parser.parse_args()

    source_base = Path(args.source_base)
    targets = []

    if args.files:
        targets = [Path(f) for f in args.files]
    elif args.csv:
        import csv as csv_mod

        with open(args.csv) as f:
            for row in csv_mod.DictReader(f):
                if int(row["score"]) < args.score_below:
                    targets.append(Path(row["file"]))

    if not targets:
        print(
            "No target files specified. Use --files or --csv with --score-below"
        )
        sys.exit(1)

    print(
        f"{'[DRY RUN] ' if args.dry_run else ''}Re-extracting {len(targets)} files (mode={args.mode})"
    )

    success = 0
    failed = 0
    for md_path in targets:
        ok, info, _ = reextract_file(md_path, source_base, args.mode, args.dry_run)
        status = "OK" if ok else "FAIL"
        print(f"  [{status}] {md_path.name}: {info}")
        if ok:
            success += 1
        else:
            failed += 1

    print(f"\nDone: {success} success, {failed} failed")


if __name__ == "__main__":
    main()
