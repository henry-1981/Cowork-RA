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

    # Handle multi-file sources (path is directory + files list)
    src_files = source.get("files", [])
    src_path = source_base / src_path_rel

    if src_files and src_path.is_dir():
        # Multi-file source: concatenate all PDFs
        pdf_paths = [src_path / f for f in src_files]
        missing = [p for p in pdf_paths if not p.exists()]
        if missing:
            return None, f"missing PDFs: {[str(m) for m in missing]}", None
        if dry_run:
            return True, f"would re-extract (multi-file, {len(pdf_paths)} PDFs): {mode}", None
        docs = [pymupdf.open(str(p)) for p in pdf_paths]
    elif src_path.is_file():
        if dry_run:
            return True, f"would re-extract: {mode}", None
        docs = [pymupdf.open(str(src_path))]
    else:
        return None, f"source not found: {src_path}", None

    # Detect mode if auto (check first page of first doc)
    if mode == "auto":
        first_text = docs[0][0].get_text("text").strip()
        if len(first_text) < 50:
            mode = "ocr"
        else:
            mode = "table"

    # Extract all pages from all docs
    new_parts = []
    for doc in docs:
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


def resolve_source_base(md_path, source_base=None, source_map=None):
    """Resolve the source base directory for a given MD file path."""
    if source_map:
        md_str = str(md_path)
        for prefix, base in source_map.items():
            if md_str.startswith(prefix):
                return Path(base)
    if source_base:
        return Path(source_base)
    return None


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
        "--source-base", help="Base directory for source PDFs (single jurisdiction)"
    )
    parser.add_argument(
        "--source-map",
        nargs="+",
        help="Jurisdiction mappings: prefix=base_dir (e.g. aria/knowledge/fda/=/path/to/fda)",
    )
    parser.add_argument(
        "--exclude-methods",
        nargs="+",
        default=[],
        help="Skip files with these extraction methods",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Report only, don't modify files"
    )
    args = parser.parse_args()

    # Parse source map
    source_map = {}
    if args.source_map:
        for mapping in args.source_map:
            prefix, base = mapping.split("=", 1)
            source_map[prefix] = base

    if not args.source_base and not source_map:
        print("ERROR: --source-base or --source-map required")
        sys.exit(1)

    targets = []

    if args.files:
        targets = [Path(f) for f in args.files]
    elif args.csv:
        import csv as csv_mod

        with open(args.csv) as f:
            for row in csv_mod.DictReader(f):
                if int(row["score"]) < args.score_below:
                    if args.exclude_methods and row["method"] in args.exclude_methods:
                        continue
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
    skipped = 0
    for md_path in targets:
        base = resolve_source_base(md_path, args.source_base, source_map)
        if not base:
            print(f"  [SKIP] {md_path.name}: no source base mapped")
            skipped += 1
            continue
        ok, info, _ = reextract_file(md_path, base, args.mode, args.dry_run)
        status = "OK" if ok else "FAIL"
        print(f"  [{status}] {md_path.name}: {info}")
        if ok:
            success += 1
        else:
            failed += 1

    print(f"\nDone: {success} success, {failed} failed, {skipped} skipped")


if __name__ == "__main__":
    main()
