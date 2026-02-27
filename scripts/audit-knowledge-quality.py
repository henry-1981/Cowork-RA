#!/usr/bin/env python3
"""Knowledge DB 전수 품질 감사 — 파일별 가독성 점수 산출."""
import re, sys, yaml, csv
from pathlib import Path

KNOWLEDGE_BASE = Path("aria/knowledge")


def parse_frontmatter(text):
    """Extract YAML frontmatter from MD file."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("---", 3)
    if end == -1:
        return {}, text
    try:
        meta = yaml.safe_load(text[3:end])
        return meta or {}, text[end + 3 :].strip()
    except Exception:
        return {}, text


def score_file(filepath):
    """Score a single MD file for LLM readability. Returns dict with metrics."""
    text = filepath.read_text(encoding="utf-8", errors="replace")
    meta, body = parse_frontmatter(text)
    source = meta.get("source", {}) if isinstance(meta, dict) else {}
    method = source.get("method", "unknown")
    pages = source.get("pages", 0)

    lines = body.split("\n")
    total_lines = len(lines)
    non_empty_lines = [l for l in lines if l.strip()]

    issues = []

    # 1. Garbage character ratio (non-printable, non-standard)
    garbage_chars = len(
        re.findall(
            r"[^\x20-\x7E\u3000-\u9FFF\uAC00-\uD7AF\n\r\t\u00A0-\u00FF\u2000-\u206F\u2190-\u27FF]",
            body,
        )
    )
    garbage_ratio = garbage_chars / max(len(body), 1)
    if garbage_ratio > 0.05:
        issues.append(f"garbage_chars:{garbage_chars}({garbage_ratio:.1%})")

    # 2. Orphaned short lines (broken table/column indicator)
    short_lines = [l for l in non_empty_lines if 0 < len(l.strip()) <= 3]
    short_ratio = len(short_lines) / max(len(non_empty_lines), 1)
    if short_ratio > 0.15:
        issues.append(f"orphaned_lines:{len(short_lines)}({short_ratio:.1%})")

    # 3. Reversed/garbled text detection (uppercase gibberish sequences)
    garbled = re.findall(r"[A-Z]{5,}[^a-z\s]{2,}", body)
    if len(garbled) > 2:
        issues.append(f"garbled_sequences:{len(garbled)}")

    # 4. Empty line density (too many = destroyed layout)
    empty_lines = total_lines - len(non_empty_lines)
    empty_ratio = empty_lines / max(total_lines, 1)
    if empty_ratio > 0.6:
        issues.append(f"empty_dense:{empty_ratio:.1%}")

    # 5. Body too small for page count
    chars_per_page = len(body) / max(pages, 1) if pages else 0
    if pages and pages > 1 and chars_per_page < 100:
        issues.append(f"thin_content:{chars_per_page:.0f}chars/page")

    # Composite score (0-100, higher = better)
    score = 100
    score -= min(30, garbage_ratio * 600)  # up to -30
    score -= min(25, short_ratio * 167)  # up to -25
    score -= min(20, len(garbled) * 5)  # up to -20
    score -= min(15, max(0, empty_ratio - 0.4) * 75)  # up to -15
    score -= (
        min(10, max(0, 500 - chars_per_page) / 50) if pages and pages > 1 else 0
    )
    score = max(0, round(score))

    return {
        "file": str(filepath.relative_to(".")),
        "method": method,
        "pages": pages,
        "body_chars": len(body),
        "total_lines": total_lines,
        "non_empty_lines": len(non_empty_lines),
        "short_lines": len(short_lines),
        "garbage_chars": garbage_chars,
        "garbled_seqs": len(garbled),
        "empty_ratio": round(empty_ratio, 3),
        "score": score,
        "issues": "; ".join(issues) if issues else "",
    }


def main():
    results = []
    for md_file in sorted(KNOWLEDGE_BASE.rglob("*.md")):
        if md_file.name.startswith("_") or md_file.name == "README.md":
            continue
        results.append(score_file(md_file))

    if not results:
        print("No MD files found in", KNOWLEDGE_BASE)
        sys.exit(1)

    # Write CSV report
    out_path = Path("reports/knowledge-quality-audit.csv")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    # Summary
    total = len(results)
    excellent = sum(1 for r in results if r["score"] >= 90)
    good = sum(1 for r in results if 70 <= r["score"] < 90)
    degraded = sum(1 for r in results if 50 <= r["score"] < 70)
    poor = sum(1 for r in results if r["score"] < 50)

    print(f"\n=== Knowledge DB Quality Audit ===")
    print(f"Total files: {total}")
    print(f"  Excellent (90+): {excellent}")
    print(f"  Good (70-89):    {good}")
    print(f"  Degraded (50-69): {degraded}")
    print(f"  Poor (<50):      {poor}")
    print(f"\nReport: {out_path}")

    # Print worst files
    worst = sorted(results, key=lambda r: r["score"])[:20]
    print(f"\n--- Worst 20 files ---")
    for r in worst:
        print(f"  [{r['score']:3d}] {r['method']:15s} {r['file']}")
        if r["issues"]:
            print(f"        → {r['issues']}")


if __name__ == "__main__":
    main()
