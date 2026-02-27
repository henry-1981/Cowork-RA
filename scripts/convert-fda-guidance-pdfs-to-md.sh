#!/bin/bash
# FDA Guidance PDF → Markdown conversion script
# Verbatim conversion with CSV metadata enrichment.
# Usage: bash scripts/convert-fda-guidance-pdfs-to-md.sh

set -euo pipefail

SRC_BASE="/Users/hb/Documents/01.Regulatory/02. FDA/03.Guidance"
DST_BASE="aria/knowledge/fda/03-guidance"
CSV_FILE="${SRC_BASE}/_download_summary.csv"

# Counters
converted=0
skipped=0
failed=0

# Sanitize filename: lowercase, remove special chars, replace spaces with hyphens
sanitize_filename() {
  echo "$1" | \
    sed 's/\.pdf$//i' | \
    tr '[:upper:]' '[:lower:]' | \
    sed 's/[+]/-/g' | \
    sed 's/[「」]//g' | \
    sed 's/[()]/-/g' | \
    sed 's/[:]/-/g' | \
    sed 's/[,]//g' | \
    sed 's/  */ /g' | \
    sed 's/ /-/g' | \
    sed 's/--*/-/g' | \
    sed 's/^-//; s/-$//' | \
    head -c 120  # Truncate very long filenames
}

# Load CSV metadata into associative-style lookup (bash 3 compatible)
# We build a temp file mapping PDF filename prefix (NNN_) to title and docket
META_FILE=$(mktemp)
trap "rm -f $META_FILE" EXIT

if [ -f "$CSV_FILE" ]; then
  # Skip header, parse CSV: rownum,title,docket,status,path_or_url
  tail -n +2 "$CSV_FILE" | while IFS= read -r line; do
    # Extract path_or_url (last field)
    path_field=$(echo "$line" | awk -F',' '{print $NF}')
    pdf_basename=$(basename "$path_field" 2>/dev/null || echo "")
    # Extract prefix number (001_, 002_, etc.)
    prefix=$(echo "$pdf_basename" | grep -oE '^[0-9]+' || echo "")
    if [ -z "$prefix" ]; then
      continue
    fi
    # Extract title (field 2) — handle quoted fields
    title=$(echo "$line" | sed 's/^[^,]*,//' | sed 's/,[^,]*,[^,]*,[^,]*$//')
    # Remove surrounding quotes if present
    title=$(echo "$title" | sed 's/^"//; s/"$//')
    # Extract docket (field 3)
    docket=$(echo "$line" | awk -F',' '{print $(NF-2)}')
    echo "${prefix}|${title}|${docket}" >> "$META_FILE"
  done
  echo "Loaded metadata for $(wc -l < "$META_FILE" | tr -d ' ') entries"
fi

# Look up metadata by prefix number
lookup_meta() {
  local prefix="$1"
  grep "^${prefix}|" "$META_FILE" 2>/dev/null | head -1 || echo ""
}

# Convert a single PDF to markdown
convert_pdf() {
  local src_path="$1"
  local dst_dir="$2"
  local filename
  filename=$(basename "$src_path")
  local ext="${filename##*.}"

  # Skip non-PDF files
  local ext_lower
  ext_lower=$(echo "$ext" | tr '[:upper:]' '[:lower:]')
  if [ "$ext_lower" != "pdf" ]; then
    skipped=$((skipped + 1))
    return
  fi

  # Skip metadata files
  if echo "$filename" | grep -q '^_'; then
    skipped=$((skipped + 1))
    return
  fi

  # Extract prefix number for metadata lookup
  local prefix
  prefix=$(echo "$filename" | grep -oE '^[0-9]+' || echo "")

  # Look up metadata
  local meta_line title docket
  meta_line=$(lookup_meta "$prefix")
  if [ -n "$meta_line" ]; then
    title=$(echo "$meta_line" | cut -d'|' -f2)
    docket=$(echo "$meta_line" | cut -d'|' -f3)
  else
    title="${filename%.pdf}"
    docket=""
  fi

  # Build output filename: preserve numeric prefix
  local sanitized
  sanitized=$(sanitize_filename "$filename")
  local dst_path="${dst_dir}/${sanitized}.md"

  # Get page count
  local pages
  pages=$(pdfinfo "$src_path" 2>/dev/null | grep "^Pages:" | awk '{print $2}')
  if [ -z "$pages" ] || ! echo "$pages" | grep -qE '^[0-9]+$'; then
    pages="unknown"
  fi

  # Extract text: try pdftotext first, fall back to tesseract OCR for image PDFs
  local text method
  method="pdftotext"
  if ! text=$(pdftotext "$src_path" - 2>/dev/null); then
    echo "FAIL: $filename"
    failed=$((failed + 1))
    return
  fi

  # If pdftotext returned empty body, try OCR via tesseract
  local body_chars
  body_chars=$(echo "$text" | tr -d '[:space:]' | wc -c | tr -d ' ')
  if [ "$body_chars" -lt 50 ] && command -v tesseract >/dev/null 2>&1 && [ "$pages" != "unknown" ]; then
    method="tesseract-ocr"
    local ocr_text=""
    local p
    for p in $(seq 1 "$pages"); do
      local tmp_prefix="/tmp/fda-ocr-p${p}"
      pdftoppm -f "$p" -l "$p" -r 300 -png "$src_path" "$tmp_prefix" 2>/dev/null
      local img_file
      img_file=$(ls "${tmp_prefix}"*.png 2>/dev/null | head -1)
      if [ -n "$img_file" ] && [ -f "$img_file" ]; then
        local page_text
        page_text=$(cat "$img_file" | tesseract stdin stdout -l eng 2>/dev/null) || true
        ocr_text="${ocr_text}${page_text}"$'\n'
        rm -f "$img_file"
      fi
    done
    local ocr_chars
    ocr_chars=$(echo "$ocr_text" | tr -d '[:space:]' | wc -c | tr -d ' ')
    if [ "$ocr_chars" -gt 50 ]; then
      text="$ocr_text"
      echo "  OCR fallback: ${ocr_chars} chars extracted"
    else
      echo "WARN (empty): $filename — pdftotext and OCR both returned empty"
    fi
  fi

  # Get relative path from SRC_BASE
  local rel_path
  rel_path=$(echo "$src_path" | sed "s|$SRC_BASE/||")

  # Escape title for YAML
  local safe_title
  safe_title=$(echo "$title" | sed 's/"/\\"/g')

  # Write markdown file with metadata header
  {
    echo "---"
    echo "source:"
    echo "  family: \"GUIDANCE\""
    echo "  instrument: \"FDA Guidance\""
    echo "  title: \"${safe_title}\""
    if [ -n "$docket" ]; then
      echo "  docket: \"${docket}\""
    fi
    echo "  path: \"${rel_path}\""
    echo "  pages: ${pages}"
    echo "  converted: $(date +%Y-%m-%d)"
    echo "  method: ${method}"
    echo "---"
    echo ""
    echo "$text"
  } > "$dst_path"

  echo "OK ($pages p): $filename → $(basename "$dst_path")"
  converted=$((converted + 1))
}

echo "=== FDA Guidance PDF → Markdown Conversion ==="
echo "Source: $SRC_BASE"
echo "Destination: $DST_BASE"
echo ""

# Ensure destination exists
mkdir -p "$DST_BASE"

# Process each PDF file
for f in "$SRC_BASE"/*.pdf; do
  [ -f "$f" ] || continue
  convert_pdf "$f" "$DST_BASE"
done

echo ""
echo "=== Summary ==="
echo "Converted: $converted"
echo "Skipped: $skipped"
echo "Failed: $failed"
