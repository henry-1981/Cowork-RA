#!/bin/bash
# PDF → Markdown 기계적 변환 스크립트
# 원문을 그대로 변환. 요약/재구성/선택적 추출 금지.
# Usage: bash scripts/convert-pdfs-to-md.sh

set -euo pipefail

SRC_BASE="/Users/hb/Documents/01.Regulatory/01. MFDS"
DST_BASE="aria/knowledge/mfds"

# Counters
converted=0
skipped=0
failed=0

# Sanitize filename: remove special chars, replace spaces/+ with hyphens
sanitize_filename() {
  echo "$1" | \
    sed 's/\.pdf$//i' | \
    sed 's/[+]/-/g' | \
    sed 's/[「」]//g' | \
    sed 's/[()]/-/g' | \
    sed 's/\[/(/g; s/\]/)/g' | \
    sed 's/  */ /g' | \
    sed 's/ /-/g' | \
    sed 's/--*/-/g' | \
    sed 's/^-//; s/-$//' | \
    sed 's/-\././'
}

# Convert a single PDF to markdown
convert_pdf() {
  local src_path="$1"
  local dst_dir="$2"
  local filename
  filename=$(basename "$src_path")
  local ext="${filename##*.}"

  # Skip non-PDF files (case-insensitive check without bash 4 syntax)
  local ext_lower
  ext_lower=$(echo "$ext" | tr '[:upper:]' '[:lower:]')
  if [ "$ext_lower" != "pdf" ]; then
    echo "SKIP (not PDF): $filename"
    skipped=$((skipped + 1))
    return
  fi

  local sanitized
  sanitized=$(sanitize_filename "$filename")
  local dst_path="${dst_dir}/${sanitized}.md"

  # Extract text
  local text
  if ! text=$(pdftotext "$src_path" - 2>/dev/null); then
    echo "FAIL: $filename — $text"
    failed=$((failed + 1))
    return
  fi

  # Get page count
  local pages
  pages=$(pdfinfo "$src_path" 2>/dev/null | grep "^Pages:" | awk '{print $2}') || pages="unknown"

  # Write markdown file with metadata header
  cat > "$dst_path" << HEADER
---
source:
  title: "${filename%.pdf}"
  path: "$(echo "$src_path" | sed "s|$SRC_BASE/||")"
  pages: ${pages}
  converted: $(date +%Y-%m-%d)
  method: pdftotext
---

HEADER

  echo "$text" >> "$dst_path"

  echo "OK ($pages p): $filename → $(basename "$dst_path")"
  converted=$((converted + 1))
}

# === Folder mappings (bash 3 compatible) ===

SRC_FOLDERS=(
  "01. 법령/01.의료기기법"
  "01. 법령/02.체외진단의료기기법"
  "01. 법령/03.디지털의료제품법"
  "01. 법령/04.공정경쟁규약"
  "02. 가이드라인"
)

DST_FOLDERS=(
  "01-법령/01-의료기기법"
  "01-법령/02-체외진단의료기기법"
  "01-법령/03-디지털의료제품법"
  "01-법령/04-공정경쟁규약"
  "02-가이드라인"
)

echo "=== PDF → Markdown Conversion ==="
echo "Source: $SRC_BASE"
echo "Destination: $DST_BASE"
echo ""

i=0
while [ $i -lt ${#SRC_FOLDERS[@]} ]; do
  src_rel="${SRC_FOLDERS[$i]}"
  dst_rel="${DST_FOLDERS[$i]}"
  src_dir="${SRC_BASE}/${src_rel}"
  dst_dir="${DST_BASE}/${dst_rel}"

  echo "--- ${src_rel} ---"

  # Ensure destination exists
  mkdir -p "$dst_dir"

  # Process each file
  for f in "$src_dir"/*; do
    [ -f "$f" ] || continue
    convert_pdf "$f" "$dst_dir"
  done
  echo ""

  i=$((i + 1))
done

echo "=== Summary ==="
echo "Converted: $converted"
echo "Skipped: $skipped"
echo "Failed: $failed"
