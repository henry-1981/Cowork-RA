#!/bin/bash
# EU MDCG/MEDDEV PDF → Markdown conversion script
# Verbatim conversion. No summarization/restructuring/selective extraction.
# Usage: bash scripts/convert-eu-pdfs-to-md.sh

set -euo pipefail

SRC_BASE="/Users/hb/Documents/01.Regulatory/03. EU"
DST_BASE="aria/knowledge/eu"

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
  local family="$3"
  local filename
  filename=$(basename "$src_path")
  local ext="${filename##*.}"

  # Skip non-PDF files (case-insensitive check)
  local ext_lower
  ext_lower=$(echo "$ext" | tr '[:upper:]' '[:lower:]')
  if [ "$ext_lower" != "pdf" ]; then
    echo "SKIP (not PDF): $filename"
    skipped=$((skipped + 1))
    return
  fi

  # Skip known duplicate
  if [ "$filename" = "md_cybersecurity_en (1).pdf" ]; then
    echo "SKIP (duplicate): $filename"
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

  # Get relative path from SRC_BASE
  local rel_path
  rel_path=$(echo "$src_path" | sed "s|$SRC_BASE/||")

  # Write markdown file with metadata header
  cat > "$dst_path" << HEADER
---
source:
  family: "${family}"
  title: "${filename%.pdf}"
  path: "${rel_path}"
  pages: ${pages}
  converted: $(date +%Y-%m-%d)
  method: pdftotext
---

HEADER

  echo "$text" >> "$dst_path"

  echo "OK ($pages p): $filename → $(basename "$dst_path")"
  converted=$((converted + 1))
}

# === MDCG Folder mappings ===

SRC_FOLDERS=(
  "02.MDCG/Annex XVI products"
  "02.MDCG/Article 10a – interruption or discontinuation of supply"
  "02.MDCG/Authorised Representatives, Importers, Distributors"
  "02.MDCG/Borderline and Classification"
  "02.MDCG/Class I Devices"
  "02.MDCG/Clinical investigation and evaluation, performance studies and evaluation"
  "02.MDCG/COVID-19"
  "02.MDCG/Custom-Made Devices"
  "02.MDCG/EUDAMED"
  "02.MDCG/European Medical Device Nomenclature (EMDN)"
  "02.MDCG/Implant Cards"
  "02.MDCG/In Vitro Diagnostic medical devices (IVD)"
  "02.MDCG/In-house devices"
  "02.MDCG/New Technologies"
  "02.MDCG/Notified bodies"
  "02.MDCG/Other guidance documents"
  "02.MDCG/Other topics"
  "02.MDCG/Person responsible for regulatory compliance (PRRC)"
  "02.MDCG/Post-Market Surveillance and Vigilance (PMSV)"
  "02.MDCG/Standards"
  "02.MDCG/Unique Device Identifier (UDI)"
)

DST_FOLDERS=(
  "02-mdcg/annex-xvi-products"
  "02-mdcg/article-10a"
  "02-mdcg/authorised-representatives"
  "02-mdcg/borderline-and-classification"
  "02-mdcg/class-i-devices"
  "02-mdcg/clinical-investigation"
  "02-mdcg/covid-19"
  "02-mdcg/custom-made-devices"
  "02-mdcg/eudamed"
  "02-mdcg/emdn"
  "02-mdcg/implant-cards"
  "02-mdcg/ivd"
  "02-mdcg/in-house-devices"
  "02-mdcg/new-technologies"
  "02-mdcg/notified-bodies"
  "02-mdcg/other-guidance"
  "02-mdcg/other-topics"
  "02-mdcg/prrc"
  "02-mdcg/pmsv"
  "02-mdcg/standards"
  "02-mdcg/udi"
)

FAMILY_TAGS=(
  "MDCG" "MDCG" "MDCG" "MDCG" "MDCG" "MDCG" "MDCG" "MDCG" "MDCG" "MDCG"
  "MDCG" "MDCG" "MDCG" "MDCG" "MDCG" "MDCG" "MDCG" "MDCG" "MDCG" "MDCG"
  "MDCG"
)

echo "=== EU PDF → Markdown Conversion ==="
echo "Source: $SRC_BASE"
echo "Destination: $DST_BASE"
echo ""

# Process MDCG folders
i=0
while [ $i -lt ${#SRC_FOLDERS[@]} ]; do
  src_rel="${SRC_FOLDERS[$i]}"
  dst_rel="${DST_FOLDERS[$i]}"
  family="${FAMILY_TAGS[$i]}"
  src_dir="${SRC_BASE}/${src_rel}"
  dst_dir="${DST_BASE}/${dst_rel}"

  echo "--- ${src_rel} ---"

  # Ensure destination exists
  mkdir -p "$dst_dir"

  # Process each file
  for f in "$src_dir"/*; do
    [ -f "$f" ] || continue
    convert_pdf "$f" "$dst_dir" "$family"
  done
  echo ""

  i=$((i + 1))
done

# Process MEDDEV folder
echo "--- 03.MEDDEV Guidance ---"
meddev_src="${SRC_BASE}/03.MEDDEV Guidance"
meddev_dst="${DST_BASE}/03-meddev"
mkdir -p "$meddev_dst"

for f in "$meddev_src"/*; do
  [ -f "$f" ] || continue
  convert_pdf "$f" "$meddev_dst" "MEDDEV"
done
echo ""

echo "=== Summary ==="
echo "Converted: $converted"
echo "Skipped: $skipped"
echo "Failed: $failed"
