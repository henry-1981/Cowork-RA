#!/usr/bin/env python3
"""Extract Compliance Checklist tables from 안내서 and insert into topic files.

Reads the 안내서 source (from git history since it was deleted in PR #27),
extracts checklist rows per activity type, and appends them to the matching
topic file with a ## Compliance Checklist header.
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

TOPICS_DIR = Path("aria/knowledge/mfds/01-법령/04-공정경쟁규약/topics")

# Git ref where the 안내서 file last existed (before PR #27 deletion)
SOURCE_REF = "d3d5b5e"
SOURCE_PATH = "aria/knowledge/mfds/01-법령/04-공정경쟁규약/의료기기-리베이트-예방-및-공정경쟁을-위한-안내서2022-04.md"

# Checklist section line range in the source (approximate, will be refined)
CHECKLIST_START_MARKER = "의료기기 공정경쟁규약 심의 Compliance Checklist"
CHECKLIST_END_MARKER = "국내외 교육훈련 행사 주관 시 Checklist"

# Page break patterns to strip
PAGE_BREAK_RE = re.compile(
    r"^\d+\s*$|"
    r"^2022 KMDIA|"
    r"^의료기기 거래에 관한 공정경쟁규약|"
    r"^\s*$"
)

# Activity type to topic file mapping
# Key: activity label as it appears in the | 구분 | column
ACTIVITY_MAP = {
    "기부": "04-기부행위.md",
    "견본품 제공": "03-견본품.md",
    "학술대회 개최운영 지원": "05-학술대회개최지원.md",
    "학술대회 참가지원": "06-학술대회참가지원.md",
    "제품 설명회": "07-자사제품설명회.md",
    "교육 훈련": "08-교육훈련.md",
    "강연/자문": "09-강연및자문.md",
    "임상시험 지원": "10-임상시험지원.md",
    "시판후 조사": "12-시판후조사.md",
}

TABLE_HEADER = "| 구분 |  | KMDIA Compliance Checklist |\n| --- | --- | --- |"


def get_source_content() -> str:
    """Retrieve 안내서 content from git history."""
    result = subprocess.run(
        ["git", "show", f"{SOURCE_REF}:{SOURCE_PATH}"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"ERROR: Could not retrieve source from git: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    return result.stdout


def extract_checklist_section(content: str) -> list[str]:
    """Extract lines between checklist start and end markers."""
    lines = content.splitlines()
    start_idx = None
    end_idx = None
    for i, line in enumerate(lines):
        if CHECKLIST_START_MARKER in line:
            start_idx = i + 1  # Skip the marker line itself
        if CHECKLIST_END_MARKER in line and start_idx is not None:
            end_idx = i
            break
    if start_idx is None:
        print("ERROR: Could not find checklist start marker", file=sys.stderr)
        sys.exit(1)
    if end_idx is None:
        # Use remaining content up to 전시 및 광고 첨부자료 end
        end_idx = len(lines)
    return lines[start_idx:end_idx]


def parse_checklists(lines: list[str]) -> dict[str, list[str]]:
    """Parse checklist lines into per-activity row lists.

    Returns dict mapping activity label to list of table rows (without header).
    """
    activities: dict[str, list[str]] = {}
    current_activity = None

    for line in lines:
        stripped = line.strip()

        # Skip page break artifacts and empty lines
        if PAGE_BREAK_RE.match(stripped):
            continue

        # Skip table headers (they repeat on each page)
        if stripped.startswith("| 구분 |") or stripped.startswith("| --- |"):
            continue

        # Parse table rows
        if stripped.startswith("|"):
            # Extract first column (activity label)
            cols = [c.strip() for c in stripped.split("|")]
            # cols[0] is empty (before first |), cols[1] is 구분
            if len(cols) >= 4:
                activity_label = cols[1].strip()
                if activity_label and activity_label in ACTIVITY_MAP:
                    current_activity = activity_label
                    if current_activity not in activities:
                        activities[current_activity] = []
                if current_activity:
                    activities[current_activity].append(stripped)

    return activities


def build_checklist_section(activity: str, rows: list[str]) -> str:
    """Build the ## Compliance Checklist section content."""
    result = ["\n## Compliance Checklist\n"]
    result.append(TABLE_HEADER)
    for row in rows:
        result.append(row)
    result.append("")  # trailing newline
    return "\n".join(result)


def append_to_topic(topic_file: Path, checklist_content: str, apply: bool) -> bool:
    """Append checklist content to topic file. Returns True if changed."""
    current = topic_file.read_text(encoding="utf-8")

    # Check if checklist already exists
    if "## Compliance Checklist" in current:
        print(f"  SKIP: {topic_file.name} already has Compliance Checklist")
        return False

    if apply:
        # Ensure file ends with newline before appending
        if not current.endswith("\n"):
            current += "\n"
        topic_file.write_text(current + checklist_content, encoding="utf-8")

    return True


def verify_verbatim(source_content: str, topic_file: Path) -> list[str]:
    """Verify that checklist content in topic file matches source."""
    issues = []
    content = topic_file.read_text(encoding="utf-8")

    if "## Compliance Checklist" not in content:
        issues.append(f"{topic_file.name}: missing ## Compliance Checklist section")
        return issues

    # Extract checklist section from topic file
    checklist_start = content.index("## Compliance Checklist")
    checklist_text = content[checklist_start:]

    # Extract table rows from the topic file checklist
    topic_rows = [
        line.strip() for line in checklist_text.splitlines()
        if line.strip().startswith("|") and not line.strip().startswith("| ---")
        and not line.strip().startswith("| 구분 |")
    ]

    # Check each row exists in source
    for row in topic_rows:
        # Normalize whitespace for comparison
        row_normalized = " ".join(row.split())
        source_normalized = " ".join(source_content.split())
        # Check key content from each row
        cells = [c.strip() for c in row.split("|") if c.strip()]
        if len(cells) >= 2:
            # Check last cell (the question text) exists in source
            question = cells[-1].strip()
            if len(question) > 20 and question not in source_content:
                # Try with normalized whitespace
                q_norm = " ".join(question.split())
                s_lines = [" ".join(l.split()) for l in source_content.splitlines()]
                found = any(q_norm in sl for sl in s_lines)
                if not found:
                    issues.append(f"{topic_file.name}: question not found in source: {question[:60]}...")

    if not issues:
        print(f"  OK: {topic_file.name} — {len(topic_rows)} rows verified")

    return issues


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--dry-run", action="store_true", help="Preview extractions")
    group.add_argument("--apply", action="store_true", help="Apply extractions")
    group.add_argument("--verify", action="store_true", help="Verify verbatim match")
    args = parser.parse_args()

    print("Retrieving source from git history...")
    source_content = get_source_content()

    print("Extracting checklist section...")
    checklist_lines = extract_checklist_section(source_content)
    print(f"  Found {len(checklist_lines)} lines in checklist section")

    print("Parsing per-activity checklists...")
    activities = parse_checklists(checklist_lines)

    if args.verify:
        all_issues = []
        for activity, topic_file in ACTIVITY_MAP.items():
            path = TOPICS_DIR / topic_file
            if path.exists():
                all_issues.extend(verify_verbatim(source_content, path))
        if all_issues:
            print("\nVERIFICATION ISSUES:")
            for issue in all_issues:
                print(f"  - {issue}")
            sys.exit(1)
        else:
            print(f"\nAll {len(ACTIVITY_MAP)} checklists verified against source")
        return

    total_inserted = 0
    for activity, topic_filename in ACTIVITY_MAP.items():
        topic_path = TOPICS_DIR / topic_filename
        if activity not in activities:
            print(f"\n  WARNING: No checklist found for '{activity}'")
            continue

        rows = activities[activity]
        checklist = build_checklist_section(activity, rows)
        question_count = sum(1 for r in rows if "내용" in r.split("|")[2] if len(r.split("|")) > 2)
        # Count actual question rows (not 첨부자료)
        q_count = len([r for r in rows if "|  |  |" in r or f"| {activity} |" in r])

        print(f"\n{topic_filename} ({activity}):")
        print(f"  Rows: {len(rows)}, Questions: ~{q_count}")

        if args.dry_run:
            # Show first and last few rows
            for row in rows[:3]:
                print(f"  {row[:100]}...")
            if len(rows) > 3:
                print(f"  ... ({len(rows) - 3} more rows)")
        else:
            changed = append_to_topic(topic_path, checklist, apply=True)
            if changed:
                total_inserted += 1

    action = "would insert into" if args.dry_run else "inserted into"
    count = len(activities) if args.dry_run else total_inserted
    print(f"\nTotal: {count} checklists {action} topic files")


if __name__ == "__main__":
    main()
