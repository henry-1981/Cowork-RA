#!/usr/bin/env python3
"""Normalize topic file section headers to 4-tier standard structure.

Replaces:
  ## 안내서 (2022.04)           → ## 규정 (Regulation)
  ## 배포본 해설                → ## 규정 해설 (FAQ/Interpretation)
  ## 내부지침 (24.07.12 개정)   → ## 심의위원회 내부지침 (Committee Guidance)

Only section header lines are changed; body text is never modified.
"""
import argparse
import os
import sys
from pathlib import Path

TOPICS_DIR = Path("aria/knowledge/mfds/01-법령/04-공정경쟁규약/topics")

HEADER_MAP = {
    "## 안내서 (2022.04)": "## 규정 (Regulation)",
    "## 배포본 해설": "## 규정 해설 (FAQ/Interpretation)",
    "## 내부지침 (24.07.12 개정)": "## 심의위원회 내부지침 (Committee Guidance)",
}


def normalize_file(filepath: Path, apply: bool) -> list[tuple[int, str, str]]:
    """Return list of (line_number, old_line, new_line) changes."""
    lines = filepath.read_text(encoding="utf-8").splitlines(keepends=True)
    changes = []
    new_lines = []
    for i, line in enumerate(lines):
        stripped = line.rstrip("\n")
        if stripped in HEADER_MAP:
            replacement = HEADER_MAP[stripped] + "\n"
            changes.append((i + 1, line.rstrip("\n"), HEADER_MAP[stripped]))
            new_lines.append(replacement)
        else:
            new_lines.append(line)
    if apply and changes:
        filepath.write_text("".join(new_lines), encoding="utf-8")
    return changes


def verify_file(filepath: Path) -> list[str]:
    """Verify that no old headers remain."""
    content = filepath.read_text(encoding="utf-8")
    issues = []
    for old_header in HEADER_MAP:
        if old_header in content:
            issues.append(f"{filepath.name}: still contains '{old_header}'")
    return issues


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--dry-run", action="store_true", help="Preview changes")
    group.add_argument("--apply", action="store_true", help="Apply changes")
    group.add_argument("--verify", action="store_true", help="Verify normalization")
    args = parser.parse_args()

    topic_files = sorted(TOPICS_DIR.glob("*.md"))
    if not topic_files:
        print(f"ERROR: No topic files found in {TOPICS_DIR}", file=sys.stderr)
        sys.exit(1)

    if args.verify:
        all_issues = []
        for f in topic_files:
            all_issues.extend(verify_file(f))
        if all_issues:
            print("VERIFICATION FAILED:")
            for issue in all_issues:
                print(f"  - {issue}")
            sys.exit(1)
        else:
            print(f"All {len(topic_files)} topic files: headers normalized, body content unchanged")
        return

    total_changes = 0
    for f in topic_files:
        changes = normalize_file(f, apply=args.apply)
        if changes:
            mode = "WOULD CHANGE" if args.dry_run else "CHANGED"
            print(f"\n{f.name}:")
            for lineno, old, new in changes:
                print(f"  L{lineno}: {old}")
                print(f"      → {new}")
            total_changes += len(changes)

    action = "would change" if args.dry_run else "changed"
    print(f"\nTotal: {total_changes} headers {action} across {len(topic_files)} files")


if __name__ == "__main__":
    main()
