#!/usr/bin/env python3
"""Split 공정경쟁규약 KD source files into topic-based files.

Reads fair-competition-topic-map.yaml config and extracts line ranges
from 3 source MD files, assembling per-topic files with source attribution.

Usage:
    python3 scripts/split-fair-competition-by-topic.py --topic 07-자사제품설명회 --dry-run
    python3 scripts/split-fair-competition-by-topic.py --topic 07-자사제품설명회
    python3 scripts/split-fair-competition-by-topic.py --all --dry-run
    python3 scripts/split-fair-competition-by-topic.py --all
    python3 scripts/split-fair-competition-by-topic.py --verify
"""
import argparse
import re
import sys
from pathlib import Path

import yaml


SCRIPT_DIR = Path(__file__).parent
CONFIG_PATH = SCRIPT_DIR / "fair-competition-topic-map.yaml"

# Section headers for each source in topic output files
SOURCE_HEADERS = {
    "framework": "## 안내서 (2022.04)",
    "definitions": "## 배포본 해설",
    "override": "## 내부지침 (24.07.12 개정)",
}


def load_config():
    with open(CONFIG_PATH, encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_source_files(config, base_dir):
    """Load all 3 source files into memory as line arrays (1-indexed)."""
    sources = {}
    for key, filename in config["sources"].items():
        path = base_dir / filename
        if not path.exists():
            print(f"ERROR: Source file not found: {path}", file=sys.stderr)
            sys.exit(1)
        with open(path, encoding="utf-8") as f:
            lines = f.readlines()
        # Prepend dummy element so index matches line number (1-indexed)
        sources[key] = [""] + lines
    return sources


def compile_artifact_patterns(config):
    """Compile artifact removal regex patterns."""
    patterns = []
    for pat in config.get("artifact_patterns", []):
        patterns.append(re.compile(pat))
    return patterns


def extract_lines(source_lines, ranges, artifact_patterns):
    """Extract lines from a source given a list of [start, end] ranges.

    Returns (extracted_lines, artifact_count).
    """
    extracted = []
    artifact_count = 0
    for start, end in ranges:
        for i in range(start, end + 1):
            if i >= len(source_lines):
                break
            line = source_lines[i]
            # Check for artifacts
            is_artifact = False
            for pat in artifact_patterns:
                if pat.match(line.rstrip("\n")):
                    is_artifact = True
                    artifact_count += 1
                    break
            if not is_artifact:
                extracted.append(line)
    return extracted, artifact_count


def build_topic_content(topic, sources, artifact_patterns):
    """Build the full content for a topic file."""
    parts = []

    # Frontmatter
    parts.append("---\n")
    parts.append(f'topic: "{topic["id"]}"\n')
    parts.append(f'title: "{topic["title"]}"\n')
    if topic.get("article"):
        parts.append(f'article: "{topic["article"]}"\n')
    if topic.get("operating_standard"):
        parts.append(f'operating_standard: "{topic["operating_standard"]}"\n')
    parts.append(f'type: {topic["type"]}\n')
    source_names = []
    for src_key in ["framework", "definitions", "override"]:
        if topic.get(src_key):
            source_names.append(src_key)
    parts.append(f'sources: [{", ".join(source_names)}]\n')
    parts.append("---\n\n")

    # Title
    parts.append(f'# {topic["title"]}\n\n')

    total_artifacts = 0

    # Extract from each source
    for src_key in ["framework", "definitions", "override"]:
        ranges = topic.get(src_key)
        if not ranges:
            continue

        header = SOURCE_HEADERS[src_key]
        lines, artifacts = extract_lines(sources[src_key], ranges, artifact_patterns)
        total_artifacts += artifacts

        if lines:
            parts.append(f"{header}\n\n")
            parts.extend(lines)
            # Ensure trailing newline
            if parts[-1] and not parts[-1].endswith("\n"):
                parts.append("\n")
            parts.append("\n")

    return "".join(parts), total_artifacts


def generate_topic(topic, sources, artifact_patterns, output_dir, dry_run=False):
    """Generate a single topic file."""
    content, artifact_count = build_topic_content(topic, sources, artifact_patterns)
    line_count = content.count("\n")
    topic_id = topic["id"]

    if dry_run:
        print(f"  [{topic_id}] {topic['title']}")
        for src_key in ["framework", "definitions", "override"]:
            ranges = topic.get(src_key)
            if ranges:
                total = sum(e - s + 1 for s, e in ranges)
                print(f"    {src_key}: {ranges} ({total} lines)")
            else:
                print(f"    {src_key}: null")
        print(f"    artifacts removed: {artifact_count}")
        print(f"    output lines: {line_count}")
        print()
        return content, line_count

    # Write the file
    output_path = output_dir / f"{topic_id}.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"  [{topic_id}] {output_path} ({line_count} lines, {artifact_count} artifacts removed)")
    return content, line_count


def verify_topics(config, base_dir, output_dir):
    """Run verification checks on generated topic files."""
    sources = load_source_files(config, base_dir)
    artifact_patterns = compile_artifact_patterns(config)
    errors = []
    warnings = []

    # 1. Check file count
    topic_files = list(output_dir.glob("*.md"))
    expected = len(config["topics"])
    if len(topic_files) != expected:
        errors.append(f"File count: expected {expected}, found {len(topic_files)}")
    else:
        print(f"[PASS] File count: {len(topic_files)} files")

    # 2. UTF-8 check
    for f in topic_files:
        try:
            f.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(f"UTF-8 error: {f.name}")
    if not any("UTF-8" in e for e in errors):
        print(f"[PASS] UTF-8 encoding: all files valid")

    # 3. Keyword check — each topic file contains its article keyword
    for topic in config["topics"]:
        article = topic.get("article")
        if not article:
            continue
        topic_path = output_dir / f"{topic['id']}.md"
        if not topic_path.exists():
            errors.append(f"Missing file: {topic['id']}.md")
            continue
        content = topic_path.read_text(encoding="utf-8")
        if article not in content:
            warnings.append(f"Keyword '{article}' not found in {topic['id']}.md")
        else:
            pass  # Quiet success

    keyword_warns = [w for w in warnings if "Keyword" in w]
    if not keyword_warns:
        print(f"[PASS] Article keywords: all present")
    else:
        for w in keyword_warns:
            print(f"[WARN] {w}")

    # 4. Verbatim check — spot-check 3 topics
    spot_checks = ["07-자사제품설명회", "04-기부행위", "14-전시및광고"]
    for tid in spot_checks:
        topic = next((t for t in config["topics"] if t["id"] == tid), None)
        if not topic:
            continue
        topic_path = output_dir / f"{tid}.md"
        if not topic_path.exists():
            continue

        # Regenerate expected content
        expected_content, _ = build_topic_content(topic, sources, artifact_patterns)
        actual_content = topic_path.read_text(encoding="utf-8")

        if expected_content == actual_content:
            print(f"[PASS] Verbatim: {tid}")
        else:
            errors.append(f"Verbatim mismatch: {tid}")

    # 5. Coverage check for framework activity guide (lines 257-766)
    framework_activity_lines = set(range(257, 767))
    covered_by_topics = set()
    for topic in config["topics"]:
        if topic["id"] == "00-general":
            continue
        ranges = topic.get("framework")
        if not ranges:
            continue
        for start, end in ranges:
            for i in range(start, end + 1):
                if i in framework_activity_lines:
                    covered_by_topics.add(i)

    uncovered = framework_activity_lines - covered_by_topics
    if not uncovered:
        print(f"[PASS] Framework activity guide coverage: 100%")
    else:
        warnings.append(f"Framework lines {len(uncovered)} uncovered in activity guide")

    # Summary
    print()
    if errors:
        print(f"ERRORS: {len(errors)}")
        for e in errors:
            print(f"  - {e}")
        return False
    elif warnings:
        print(f"PASS with {len(warnings)} warnings")
        return True
    else:
        print("ALL CHECKS PASSED")
        return True


def main():
    parser = argparse.ArgumentParser(description="Split 공정경쟁규약 KD by topic")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--topic", help="Generate a single topic by ID (e.g. 07-자사제품설명회)")
    group.add_argument("--all", action="store_true", help="Generate all topic files")
    group.add_argument("--verify", action="store_true", help="Verify generated topic files")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing files")
    args = parser.parse_args()

    config = load_config()
    repo_root = SCRIPT_DIR.parent
    base_dir = repo_root / config["base_path"]
    output_dir = base_dir / config["output_dir"]

    if args.verify:
        ok = verify_topics(config, base_dir, output_dir)
        sys.exit(0 if ok else 1)

    sources = load_source_files(config, base_dir)
    artifact_patterns = compile_artifact_patterns(config)

    if args.topic:
        # Single topic mode
        topic = next((t for t in config["topics"] if t["id"] == args.topic), None)
        if not topic:
            print(f"ERROR: Topic '{args.topic}' not found in config", file=sys.stderr)
            sys.exit(1)
        print(f"{'[DRY RUN] ' if args.dry_run else ''}Generating topic: {args.topic}")
        generate_topic(topic, sources, artifact_patterns, output_dir, args.dry_run)

    elif args.all:
        # All topics mode
        print(f"{'[DRY RUN] ' if args.dry_run else ''}Generating all {len(config['topics'])} topics...")
        print()
        total_lines = 0
        for topic in config["topics"]:
            _, lines = generate_topic(topic, sources, artifact_patterns, output_dir, args.dry_run)
            total_lines += lines
        print(f"Total output: {total_lines} lines across {len(config['topics'])} files")


if __name__ == "__main__":
    main()
